#!/usr/bin/env python3
"""SafeGate-AI v3: launch readiness scorer.

Decisions: GO, GO_WITH_WAIVERS, NO_GO. Gate status is tri-state
(PASS / FAIL / NOT_STARTED); anything but PASS on a hard blocker is NO_GO unless
covered by an unexpired waiver that names an approver.
"""
import json
import sys
from datetime import date
from typing import Optional

REQUIRED_WORKSTREAMS = {"Safeguards", "Identity", "Platform Infra", "Legal/Compliance", "Product Surfaces"}
VALID_STATUS = {"PASS", "FAIL", "NOT_STARTED"}


def _label(g: dict) -> str:
    return f"[{g['id']}] [{g['workstream']}] {g['check']} ({g['status']}; owner: {g['owner']})"


def evaluate_launch(cohort: str, gates: list, waivers: Optional[list] = None,
                    today: Optional[date] = None) -> dict:
    today = today or date.today()
    waivers = waivers or []
    errors = []
    for g in gates:
        if g.get("status") not in VALID_STATUS:
            errors.append(f"{g.get('id', '?')}: invalid status {g.get('status')!r}")
    if errors:
        return {"cohort": cohort, "decision": "NO_GO", "errors": errors}

    valid_waivers = {}
    for w in waivers:
        if w.get("approver") and w.get("expires") and date.fromisoformat(w["expires"]) >= today:
            valid_waivers[w["gate_id"]] = w

    covered = {g["workstream"] for g in gates}
    missing_ws = sorted(REQUIRED_WORKSTREAMS - covered)

    failing = [g for g in gates if g["status"] != "PASS"]
    hard = [g for g in failing if g["hard_blocker"] and g["id"] not in valid_waivers]
    waived = [g for g in failing if g["hard_blocker"] and g["id"] in valid_waivers]
    soft = [g for g in failing if not g["hard_blocker"]]

    if not gates or missing_ws or hard:
        decision = "NO_GO"
    elif waived:
        decision = "GO_WITH_WAIVERS"
    else:
        decision = "GO"

    passed = sum(1 for g in gates if g["status"] == "PASS")
    return {
        "cohort": cohort,
        "decision": decision,
        "readiness_score_pct": round(100 * passed / len(gates), 1) if gates else 0.0,
        "workstreams_without_gates": missing_ws,
        "hard_blockers": [_label(g) for g in hard],
        "waived_blockers": [_label(g) + f" waived by {valid_waivers[g['id']]['approver']} until {valid_waivers[g['id']]['expires']}" for g in waived],
        "non_blocking_risks": [_label(g) for g in soft],
    }


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "data/wave2_gates.json"
    with open(path, encoding="utf-8") as f:
        cfg = json.load(f)
    print(json.dumps(evaluate_launch(cfg["cohort"], cfg["gates"], cfg.get("waivers")), indent=2))
