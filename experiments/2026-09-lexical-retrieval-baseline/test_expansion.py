"""Behavior and failure boundaries for the controlled expansion diagnostic."""

import subprocess
import sys
from pathlib import Path

from expansion import evaluate, expand_query


def test_expansion_normalizes_deduplicates_and_preserves_unknown_terms():
    assert expand_query("RESTORE restore unknown!", {"restore": ("Checkpoint", "checkpoint")}) == (
        "restore unknown checkpoint"
    )
    assert expand_query("", {"restore": ("checkpoint",)}) == ""


def test_expansion_is_one_hop_even_with_cycles():
    mapping = {"restore": ("checkpoint",), "checkpoint": ("restore", "state")}
    assert expand_query("restore", mapping) == "restore checkpoint"
    assert mapping["checkpoint"] == ("restore", "state")


def test_recovery_improves_but_ambiguous_query_regresses():
    scores = {(row["case"], row["variant"]): row["reciprocal_rank_at_k"] for row in evaluate()}
    assert scores == {
        ("recovery", "baseline"): 0.0,
        ("recovery", "expanded"): 1.0,
        ("ambiguous", "baseline"): 1.0,
        ("ambiguous", "expanded"): 0.0,
    }


def test_runner_refuses_to_overwrite_evidence(tmp_path):
    output = tmp_path / "evidence.json"
    command = [
        sys.executable,
        str(Path(__file__).with_name("expansion.py")),
        "--output",
        str(output),
    ]
    subprocess.run(command, check=True, capture_output=True, timeout=10)
    before = output.read_bytes()
    result = subprocess.run(command, capture_output=True, timeout=10)
    assert result.returncode != 0
    assert output.read_bytes() == before
