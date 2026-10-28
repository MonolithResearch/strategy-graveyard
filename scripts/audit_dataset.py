"""Audit public historical summaries without treating missing evidence as failure."""
from __future__ import annotations

from collections import Counter
import csv
from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COLUMNS = ("rank", "name", "family", "status", "tier", "tier_name", "IS_Sharpe",
           "N_trials", "OOS_Sharpe", "blind_OOS_DSR", "OOS_trades", "net_3x_cost_SR",
           "PBO", "description", "why_it_died")


def _number(text: str, name: str, *, probability=False, integer=False):
    if not text.strip():
        return None
    try:
        value = Decimal(text)
    except InvalidOperation as exc:
        raise ValueError(f"{name}: not numeric") from exc
    if not value.is_finite():
        raise ValueError(f"{name}: must be finite")
    if probability and not 0 <= value <= 1:
        raise ValueError(f"{name}: must be in [0, 1]")
    if integer and (value < 0 or value != value.to_integral_value()):
        raise ValueError(f"{name}: must be a non-negative integer")
    return value


def classify_row(row: dict[str, str]) -> str:
    """Three numeric conditions only; PASS would not establish deployability."""
    dsr = _number(row["blind_OOS_DSR"], "DSR", probability=True)
    pbo = _number(row["PBO"], "PBO", probability=True)
    trades = _number(row["OOS_trades"], "trades", integer=True)
    if any(value is None for value in (dsr, pbo, trades)):
        return "INCOMPLETE"
    return "PASS" if dsr >= Decimal("0.5") and pbo <= Decimal("0.2") and trades >= 50 else "FAIL"


def audit(path: Path = ROOT / "data" / "gate_ranking_public.csv") -> dict:
    path = Path(path)
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if tuple(reader.fieldnames or ()) != COLUMNS:
            raise ValueError("Unexpected CSV columns")
        rows = list(reader)
    if not rows:
        raise ValueError("Empty summary dataset")
    counts = Counter({"PASS": 0, "FAIL": 0, "INCOMPLETE": 0})
    ranks, names = set(), set()
    for row in rows:
        if None in row or any(value is None for value in row.values()):
            raise ValueError("Malformed CSV row: check quoting and field count")
        rank = _number(row["rank"], "rank", integer=True)
        name = row["name"].strip()
        if rank is None or rank < 1 or rank in ranks or not name or name in names:
            raise ValueError("Rank/name must be present and unique")
        ranks.add(rank)
        names.add(name)
        counts[classify_row(row)] += 1
        for key in ("IS_Sharpe", "OOS_Sharpe", "net_3x_cost_SR"):
            _number(row[key], key)
        _number(row["N_trials"], "N_trials", integer=True)
    if ranks != set(range(1, len(rows) + 1)):
        raise ValueError("Ranks must be contiguous from 1")
    return {"evidence_class": "HISTORICAL_SUMMARY_NOT_RECOMPUTED",
            "rows": len(rows), "gate_counts": dict(counts),
            "rows_with_dsr": sum(bool(row["blind_OOS_DSR"].strip()) for row in rows),
            "dataset_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "note": "INCOMPLETE is missing reported evidence, not a tested failure. "
                    "This audit does not rerun the underlying strategies."}


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True, allow_nan=False))
