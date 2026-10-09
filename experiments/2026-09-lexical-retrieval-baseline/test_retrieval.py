import math

import pytest
from retrieval import Retriever, metrics, tokenize


def test_tokenization():
    assert tokenize("Retry, RETRY! café") == ["retry", "retry", "café"]


def test_hand_calculated_bm25():
    index = Retriever([{"id": "a", "text": "cat cat"}, {"id": "b", "text": "dog dog"}])
    hits = index.search("cat")
    assert hits[0][0] == "a"
    assert hits[0][1] == pytest.approx(math.log(2) * 2 * 2.2 / 3.2)


def test_length_normalization_ablation():
    index = Retriever([{"id": "a", "text": "cat extra extra extra"}, {"id": "z", "text": "cat"}])
    assert index.search("cat")[0][0] == "z"
    assert index.search("cat", b=0)[0][0] == "a"  # Equal score; tie uses ID.


def test_no_arbitrary_hits():
    index = Retriever([{"id": "a", "text": "checkpoint"}])
    assert index.search("restore progress") == []
    assert index.search("") == []
    assert Retriever([]).search("anything") == []
    assert Retriever([{"id": "a", "text": ""}]).search("anything") == []


def test_metrics_with_multiple_relevant_documents():
    result = metrics(["x", "a", "y", "b"], {"a", "b"}, 3)
    assert result == {"recall_at_k": 0.5, "reciprocal_rank_at_k": 0.5}
    assert metrics([], {"a"}) == {"recall_at_k": 0, "reciprocal_rank_at_k": 0}


@pytest.mark.parametrize(
    "kwargs", [{"k": 0}, {"b": 2}, {"k1": 0}, {"k1": float("nan")}, {"method": "unknown"}]
)
def test_invalid_search_parameters(kwargs):
    with pytest.raises(ValueError):
        Retriever([]).search("cat", **kwargs)


def test_duplicate_ids_rejected():
    with pytest.raises(ValueError):
        Retriever([{"id": "a", "text": "cat"}, {"id": "a", "text": "dog"}])


def test_runner_reproducibility_and_existing_output_refusal(tmp_path):
    import json
    import subprocess
    import sys
    from pathlib import Path

    script = Path(__file__).with_name("run.py")
    artifacts = []
    for name in ("first.json", "second.json"):
        output = tmp_path / name
        subprocess.run(
            [sys.executable, str(script), "--output", str(output)],
            check=True,
            capture_output=True,
            timeout=60,
        )
        artifacts.append(json.loads(output.read_text()))
    assert artifacts[0]["sha256"] == artifacts[1]["sha256"]
    for method, result in artifacts[0]["results"].items():
        other = artifacts[1]["results"][method]
        assert result["summary"] == other["summary"]
        assert [q["ranked"] for q in result["queries"]] == [q["ranked"] for q in other["queries"]]
    existing = tmp_path / "first.json"
    before = existing.read_bytes()
    refused = subprocess.run(
        [sys.executable, str(script), "--output", str(existing)],
        capture_output=True,
        timeout=60,
    )
    assert refused.returncode != 0
    assert existing.read_bytes() == before
