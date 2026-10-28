"""Compare explicit expansion policies without changing historical diagnostics."""

import argparse
import hashlib
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Literal

from expansion import DOCUMENTS, EXPANSIONS, expand_query
from retrieval import Retriever, metrics, tokenize

Policy = Literal["never", "always", "on_empty"]
POLICIES: tuple[Policy, ...] = ("never", "always", "on_empty")
CASES = (
    ("lexical_miss", "restore", "checkpoint"),
    ("ambiguous_term", "resume", "career"),
    ("nonempty_wrong_hit", "restore resume", "checkpoint"),
)


def search_with_policy(
    retriever: Retriever,
    query: str,
    expansions: Mapping[str, Sequence[str]],
    *,
    policy: Policy,
    k: int = 1,
) -> tuple[list[tuple[str, float]], str, int]:
    """Return hits, effective query, and search count; fallback uses at most two searches."""
    if policy not in POLICIES:
        raise ValueError("Unknown expansion policy")
    if policy == "always":
        expanded = expand_query(query, expansions)
        return retriever.search(expanded, k=k), expanded, 1
    hits = retriever.search(query, k=k)
    if policy == "never" or hits:
        return hits, query, 1
    expanded = expand_query(query, expansions)
    # Avoid a duplicate search if expansion adds no searchable vocabulary.
    if set(tokenize(expanded)) == set(tokenize(query)):
        return hits, query, 1
    return retriever.search(expanded, k=k), expanded, 2


def evaluate() -> list[dict[str, object]]:
    """Expose gains and regressions per case rather than hiding them in an average."""
    retriever = Retriever(DOCUMENTS)
    rows = []
    for case, query, relevant in CASES:
        for policy in POLICIES:
            hits, effective_query, calls = search_with_policy(
                retriever, query, EXPANSIONS, policy=policy
            )
            rows.append(
                {
                    "case": case,
                    "query": query,
                    "relevant": [relevant],
                    "policy": policy,
                    "effective_query": effective_query,
                    "search_calls": calls,
                    "hits": hits,
                    **metrics([doc_id for doc_id, _ in hits], {relevant}, k=1),
                }
            )
    return rows


def main() -> None:
    """Write a fresh artifact with exact input and implementation provenance."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    rows = evaluate()
    evidence = {
        "source_sha256": {
            name: hashlib.sha256((root / name).read_bytes()).hexdigest()
            for name in ("retrieval.py", "expansion.py", "expansion_policy.py")
        },
        "configuration": {"k": 1, "k1": 1.2, "b": 0.75, "expansions": EXPANSIONS},
        "documents": DOCUMENTS,
        "limitations": "Co-designed synthetic diagnostic; labels are explicit intended meanings.",
        "api_requests": 0,
        "results": rows,
    }
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(evidence, stream, indent=2)
        stream.write("\n")
    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
