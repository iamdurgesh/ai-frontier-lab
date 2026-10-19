"""Controlled one-hop query expansion diagnostic; no external dependencies or services."""

import argparse
import hashlib
import json
from collections.abc import Mapping, Sequence
from pathlib import Path

from retrieval import Retriever, metrics, tokenize

EXPANSIONS = {"restore": ("checkpoint",), "resume": ("checkpoint",)}
DOCUMENTS = [
    {"id": "checkpoint", "text": "checkpoint"},
    {"id": "career", "text": "resume developer experience skills education"},
]
CASES = [
    ("recovery", "restore", "checkpoint"),
    ("ambiguous", "resume", "career"),
]


def expand_query(query: str, expansions: Mapping[str, Sequence[str]]) -> str:
    """Append unique normalized terms once; never expand newly added terms recursively."""
    original = list(dict.fromkeys(tokenize(query)))
    terms = dict.fromkeys(original)
    for term in original:
        for replacement in expansions.get(term, ()):
            for token in tokenize(replacement):
                terms.setdefault(token, None)
    return " ".join(terms)


def evaluate() -> list[dict[str, object]]:
    """Compare identical BM25 settings on co-designed improvement and regression cases."""
    retriever = Retriever(DOCUMENTS)
    rows = []
    for case, query, relevant in CASES:
        expanded = expand_query(query, EXPANSIONS)
        for variant, effective in (("baseline", query), ("expanded", expanded)):
            hits = retriever.search(effective, k=1)
            rows.append(
                {
                    "case": case,
                    "variant": variant,
                    "query": query,
                    "effective_query": effective,
                    "relevant": [relevant],
                    "hits": hits,
                    **metrics([doc_id for doc_id, _ in hits], {relevant}, k=1),
                }
            )
    return rows


def main() -> None:
    """Write new evidence without overwriting earlier measurements."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    evidence = {
        "source_sha256": {
            name: hashlib.sha256((root / name).read_bytes()).hexdigest()
            for name in ("expansion.py", "retrieval.py")
        },
        "configuration": {"k": 1, "k1": 1.2, "b": 0.75, "expansions": EXPANSIONS},
        "documents": DOCUMENTS,
        "limitations": "Co-designed synthetic diagnostic; no held-out quality claim or timing.",
        "api_requests": 0,
        "results": evaluate(),
    }
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(evidence, stream, indent=2)
        stream.write("\n")
    print(json.dumps(evidence["results"], indent=2))


if __name__ == "__main__":
    main()
