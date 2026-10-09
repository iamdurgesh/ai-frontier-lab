"""Run a fixed offline diagnostic and write a new, reproducible evidence artifact."""

import argparse
import hashlib
import json
import platform
import statistics
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter_ns

from retrieval import Retriever, metrics

ROOT = Path(__file__).resolve().parent


def main() -> None:
    """Evaluate fixed methods; refuse to overwrite an existing output artifact."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    fixture = json.loads((ROOT / "fixture.json").read_text())
    retriever = Retriever(fixture["documents"])
    all_ids = set(retriever.counts)
    for query in fixture["queries"]:
        if not query["relevant"] or not set(query["relevant"]) <= all_ids:
            raise ValueError("Invalid relevance labels")
    configs = [
        ("overlap", "overlap", 0.75),
        ("bm25", "bm25", 0.75),
        ("bm25_no_length_norm", "bm25", 0.0),
    ]
    results = {}
    for label, method, b in configs:
        rows = []
        for query in fixture["queries"]:
            retriever.search(query["text"], method=method, b=b)  # One warmup.
            timings = []
            expected = None
            for _ in range(20):
                start = perf_counter_ns()
                hits = retriever.search(query["text"], method=method, b=b)
                timings.append((perf_counter_ns() - start) / 1_000_000)
                if expected is not None and hits != expected:
                    raise AssertionError("Nondeterministic rankings")
                expected = hits
            ranked = [doc_id for doc_id, _ in hits]
            rows.append(
                {
                    "id": query["id"],
                    "category": query["category"],
                    "query": query["text"],
                    "relevant": query["relevant"],
                    "ranked": ranked,
                    "scores": [score for _, score in hits],
                    **metrics(ranked, set(query["relevant"])),
                    "latency_ms_runs": timings,
                }
            )
        summary = {}
        for category in ("all", "lexical", "paraphrase"):
            subset = [row for row in rows if category == "all" or row["category"] == category]
            summary[category] = {
                "queries": len(subset),
                "recall_at_3": statistics.mean(row["recall_at_k"] for row in subset),
                "mrr_at_3": statistics.mean(row["reciprocal_rank_at_k"] for row in subset),
            }
        results[label] = {
            "configuration": {"method": method, "k": 3, "k1": 1.2, "b": b},
            "summary": summary,
            "queries": rows,
        }
    revision = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout.strip()
    evidence = {
        "created_at_utc": datetime.now(UTC).isoformat(),
        "base_commit": revision,
        "source_note": "Working-tree source identified by hashes; base commit may not contain it.",
        "sha256": {
            name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            for name in ("retrieval.py", "run.py", "fixture.json")
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "machine": platform.machine(),
            "runtime_dependencies": "standard library",
        },
        "methodology": {
            "repeats": 20,
            "warmup_per_query": 1,
            "concurrency": 1,
            "timing_scope": "search only; excludes index build and file IO",
            "quality_repetitions": "identical deterministic rankings, not independent samples",
            "limitations": "co-designed synthetic diagnostic, no held-out generalization",
        },
        "api_requests": 0,
        "api_cost_eur": 0,
        "compute_cost": "not measured",
        "results": results,
    }
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(evidence, stream, indent=2)
        stream.write("\n")
    for label, value in results.items():
        print(label, json.dumps(value["summary"]))


if __name__ == "__main__":
    main()
