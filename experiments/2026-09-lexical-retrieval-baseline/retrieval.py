"""Readable lexical retrieval for a bounded teaching fixture; standard library only."""

import math
import re
from collections import Counter


def tokenize(text: str) -> list[str]:
    """Extract lowercase Unicode word tokens, without stemming or stopword removal."""
    return re.findall(r"\w+", text.casefold())


class Retriever:
    """Index unique document IDs; rank by overlap or positive-IDF BM25."""

    def __init__(self, documents: list[dict[str, str]]) -> None:
        ids = [doc["id"] for doc in documents]
        if len(set(ids)) != len(ids):
            raise ValueError("Document IDs must be unique")
        self.counts = {doc["id"]: Counter(tokenize(doc["text"])) for doc in documents}
        self.lengths = {key: sum(counts.values()) for key, counts in self.counts.items()}
        self.average_length = sum(self.lengths.values()) / len(ids) if ids else 0.0
        self.document_frequency: Counter[str] = Counter()
        for counts in self.counts.values():
            self.document_frequency.update(counts.keys())

    def search(
        self,
        query: str,
        *,
        method: str = "bm25",
        k: int = 3,
        k1: float = 1.2,
        b: float = 0.75,
    ) -> list[tuple[str, float]]:
        """Return positive-score hits; ties use document ID, never corpus position."""
        if method not in {"overlap", "bm25"}:
            raise ValueError("Unknown method")
        if k < 1 or not math.isfinite(k1) or k1 <= 0 or not math.isfinite(b) or not 0 <= b <= 1:
            raise ValueError("Require k >= 1, finite k1 > 0, and finite 0 <= b <= 1")
        if not self.average_length:
            return []
        terms = set(tokenize(query))
        hits = []
        for doc_id, counts in self.counts.items():
            score = 0.0
            for term in sorted(terms):
                frequency = counts[term]
                if not frequency:
                    continue
                if method == "overlap":
                    score += 1.0
                else:
                    df = self.document_frequency[term]
                    idf = math.log1p((len(self.counts) - df + 0.5) / (df + 0.5))
                    norm = k1 * (1 - b + b * self.lengths[doc_id] / self.average_length)
                    score += idf * frequency * (k1 + 1) / (frequency + norm)
            if score > 0:
                hits.append((doc_id, score))
        return sorted(hits, key=lambda hit: (-hit[1], hit[0]))[:k]


def metrics(ranked: list[str], relevant: set[str], k: int = 3) -> dict[str, float]:
    """Calculate Recall@k and reciprocal rank@k for binary relevance labels."""
    if k < 1 or not relevant or len(ranked) != len(set(ranked)):
        raise ValueError("Require positive k, nonempty relevance, and unique ranked IDs")
    top = ranked[:k]
    reciprocal_rank = next(
        (1 / rank for rank, doc_id in enumerate(top, 1) if doc_id in relevant), 0.0
    )
    return {
        "recall_at_k": len(set(top) & relevant) / len(relevant),
        "reciprocal_rank_at_k": reciprocal_rank,
    }
