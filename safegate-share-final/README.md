# SafeGate-AI: Life Sciences Verification Program Kit For TPMs

A working kit for a TPM who owns a **verification program for life sciences**: deciding who gets verified for elevated life-sciences capabilities, binding the right safeguards and data controls to them, and scaling that across personas, verticals, and product surfaces without bespoke work per customer.

**Independent artifact.** This kit was written from public information and general program-management practice. It is not the organization process or system and does not describe any internal the organization tooling. Organizations and users in the code samples are fictional.

**Targets are illustrative.** Every threshold, SLA, and KPI target is a placeholder until a Wave 1 baseline exists. Files in `templates/` contain placeholders such as `[name]` and `[date]` by design.

All names, thresholds, and credential lists are illustrative defaults. Items marked ASSUMPTION need confirmation from Safeguards, Legal, or Identity before real use. Nothing here is legal advice.

## What the TPM owns

| Question | Where answered |
|---|---|
| Who do we verify, and with what proof? | `docs/01`, `data/policy.json` |
| How does verification turn into runtime behavior? | `docs/02`, `src/policy_resolver.py` |
| How does a request move from submitted to active, expired, or revoked? | `docs/05` |
| Who decides what, and when do we escalate? | `docs/03` |
| How do we scale from design partners to self-serve? | `docs/04` |
| How do we know it is working? | `docs/06` |
| What can go wrong? | `docs/07` |
| How does this map to the organization public context? | `docs/08` |
| How does this map to the Verification Program TPM posting, and what are the expansion types? | `docs/10`, `templates/PROGRAM_TRACKER.csv` |
| What would the program narrative and Wave 1 plan look like? | `docs/09` |

## Layout

```
README.md
data/policy.json           all entitlement rules (edit this, not code)
data/wave2_gates.json      sample launch-gate input
docs/01..10                persona matrix, architecture, operating rhythm, waves,
                           verification lifecycle, metrics, risk register,
                           the organization public-context mapping, program narrative + Wave 1 plan, posting alignment + expansion types
templates/                 program charter, trade-off RFC, launch gate checklist,
                           weekly status, decision log
src/policy_resolver.py     entitlement resolver (reason codes, expiry, revocation)
src/readiness_scorer.py    go/no-go scorer (tri-state gates, waivers)
tests/test_all.py          14 tests
```

## Run

```bash
python3 tests/test_all.py
python3 src/policy_resolver.py
python3 src/readiness_scorer.py data/wave2_gates.json
```

Python 3.9+, standard library only.

## Design stance

1. Verification is a control-plane decision. Runtime only reads signed claims.
2. Unknown input is rejected. Missing credentials block. Expiry downgrades. Revocation fails closed.
3. The strictest applicable rule wins (for example retention: persona floor vs vertical default).
4. Every decision carries reason codes and a policy version, so support and auditors can explain it.
5. Policy is data. Changing a credential requirement is a reviewed config change, not an engineering ticket.

