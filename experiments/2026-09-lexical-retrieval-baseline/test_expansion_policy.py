"""Check policy tradeoffs, bounded work, and evidence preservation."""

import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import Mock

import pytest
from expansion_policy import evaluate, search_with_policy
from retrieval import Retriever


def test_policy_quality_tradeoffs():
    scores = {(row["case"], row["policy"]): row["recall_at_k"] for row in evaluate()}
    assert scores == {
        ("lexical_miss", "never"): 0,
        ("lexical_miss", "always"): 1,
        ("lexical_miss", "on_empty"): 1,
        ("ambiguous_term", "never"): 1,
        ("ambiguous_term", "always"): 0,
        ("ambiguous_term", "on_empty"): 1,
        ("nonempty_wrong_hit", "never"): 0,
        ("nonempty_wrong_hit", "always"): 1,
        ("nonempty_wrong_hit", "on_empty"): 0,
    }


def test_fallback_does_not_expand_a_nonempty_result():
    retriever = Mock(spec=Retriever)
    retriever.search.return_value = [("wrong", 0.1)]
    assert search_with_policy(
        retriever, "resume", {"resume": ("checkpoint",)}, policy="on_empty"
    ) == ([("wrong", 0.1)], "resume", 1)
    retriever.search.assert_called_once_with("resume", k=1)


def test_fallback_stops_after_two_empty_searches():
    retriever = Mock(spec=Retriever)
    retriever.search.return_value = []
    hits, query, calls = search_with_policy(
        retriever, "restore", {"restore": ("checkpoint",)}, policy="on_empty"
    )
    assert (hits, query, calls) == ([], "restore checkpoint", 2)
    assert retriever.search.call_count == 2


@pytest.mark.parametrize("query,mapping", [("", {}), ("unknown", {}), ("A!", {"a": ("a",)})])
def test_no_duplicate_search_without_new_terms(query, mapping):
    retriever = Mock(spec=Retriever)
    retriever.search.return_value = []
    assert search_with_policy(retriever, query, mapping, policy="on_empty")[2] == 1
    assert retriever.search.call_count == 1


def test_invalid_policy_rejected_before_search():
    retriever = Mock(spec=Retriever)
    with pytest.raises(ValueError, match="Unknown"):
        search_with_policy(retriever, "query", {}, policy="typo")
    retriever.search.assert_not_called()


def test_runner_reproduces_and_preserves_existing_output(tmp_path):
    script = Path(__file__).with_name("expansion_policy.py")
    artifacts = []
    for name in ("first.json", "second.json"):
        output = tmp_path / name
        subprocess.run(
            [sys.executable, str(script), "--output", str(output)],
            check=True,
            capture_output=True,
            timeout=10,
        )
        artifacts.append(output.read_bytes())
    assert artifacts[0] == artifacts[1]
    assert len(json.loads(artifacts[0])["results"]) == 9
    refused = subprocess.run(
        [sys.executable, str(script), "--output", str(tmp_path / "first.json")],
        capture_output=True,
        timeout=10,
    )
    assert refused.returncode != 0
    assert (tmp_path / "first.json").read_bytes() == artifacts[0]
