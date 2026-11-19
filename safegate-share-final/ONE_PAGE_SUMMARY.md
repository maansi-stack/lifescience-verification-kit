# SafeGate-AI: One-Page Summary

**What it is.** A program kit for expanding verified access to elevated life-sciences AI capabilities, built around one idea: each expansion should need less bespoke coordination than the last.

**Core model.** Entitlement = persona x vertical x credentials x surface. Verification happens in a slow control plane that mints short-lived signed claims. Runtime only reads claims. Strictest rule wins, unknown input is rejected, revocation fails closed.

**What is in it**
- `data/policy.json` and `src/policy_resolver.py`: data-driven resolver with reason codes, expiry downgrade, revocation, per-surface credential checks.
- `src/readiness_scorer.py`: go/no-go over PASS/FAIL/NOT_STARTED gates, waivers with named approver and expiry.
- `docs/05-07`: verification lifecycle, capacity model, KPIs (each speed metric paired with a quality metric), risk register.
- `docs/10` and `templates/`: expansion types (plan, account, platform, org category, data/review requirement), intake, charter, RFC, launch gate checklist, tracker, weekly status, decision log.

**Run it.** `python3 tests/test_all.py` (14 tests, standard library only).

**Open decisions it surfaces.** ZDR vs. immutable audit log, tier boundaries, per-surface parity of retention and review. Each has an owner and a gate.

**Limits.** Independent artifact from public information. Targets are placeholders until baselines exist.
