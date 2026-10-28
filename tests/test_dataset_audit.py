"""Data integrity and incomplete-evidence tests for the historical summary."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from audit_dataset import audit, classify_row


def row(**changes):
    return {"name": "synthetic", "blind_OOS_DSR": "0.7", "PBO": "0.1",
            "OOS_trades": "100", **changes}


def test_complete_pass_and_failure_are_distinct():
    assert classify_row(row()) == "PASS"
    assert classify_row(row(PBO="0.3")) == "FAIL"


@pytest.mark.parametrize("key", ["blind_OOS_DSR", "PBO", "OOS_trades"])
def test_missing_evidence_is_never_counted_as_tested_failure_or_pass(key):
    assert classify_row(row(**{key: ""})) == "INCOMPLETE"


@pytest.mark.parametrize("changes", [{"PBO": "nan"}, {"PBO": "1.01"},
    {"blind_OOS_DSR": "inf"}, {"blind_OOS_DSR": "-0.1"},
    {"OOS_trades": "1.5"}, {"OOS_trades": "-1"}, {"OOS_trades": "nan"},
    {"PBO": "nan", "blind_OOS_DSR": ""}])
def test_bad_available_evidence_is_rejected_even_if_other_fields_missing(changes):
    with pytest.raises(ValueError):
        classify_row(row(**changes))


def test_historical_dataset_has_unique_ranks_names_and_explicit_coverage():
    result = audit(ROOT / "data" / "gate_ranking_public.csv")
    assert result["rows"] == 39
    assert result["gate_counts"]["PASS"] == 0
    assert sum(result["gate_counts"].values()) == 39
    assert result["gate_counts"]["INCOMPLETE"] > 0
    assert result["evidence_class"] == "HISTORICAL_SUMMARY_NOT_RECOMPUTED"


def test_cli_is_replayable_outside_repo(tmp_path):
    proc = subprocess.run([sys.executable, str(ROOT / "scripts" / "audit_dataset.py")],
        cwd=tmp_path, capture_output=True, text=True, check=True)
    assert json.loads(proc.stdout)["rows"] == 39
