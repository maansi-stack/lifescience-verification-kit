# Launch Readiness Gates

**Cohort:** [vertical - persona - surface]  **TPM:** [name]  **Go-live:** [date]
Gate IDs match the `id` field in the scorer input JSON. Status is PASS, FAIL, or NOT_STARTED. Items marked (H) are hard blockers.

## Gate 1: Safeguards and utility
- [ ] G1.1 (H) Domain red-team and clinical hallucination evals meet thresholds
- [ ] G1.2 (H) Benign utility >= 98% non-refusal on benchmark
- [ ] G1.3 (H) Circuit-breaker tested in staging (suspend a cohort's claims)

## Gate 2: Identity and provisioning
- [ ] G2.1 (H) End-to-end verification tested for each credential type in scope
- [ ] G2.2 (H) Claim `modules` payload correct on every target surface
- [ ] G2.3 (H) Revocation purge < 60s and expiry downgrade verified by automated test
- [ ] G2.4 Re-attestation notices (T-30, T-7) tested

## Gate 3: Data, ZDR and compliance
- [ ] G3.1 (H) ZDR verified: no content in logs, traces, caches, or training data
- [ ] G3.2 (H) Customer-held audit log design signed off (if vertical needs it)
- [ ] G3.3 (H) Legal and Privacy sign-off for regions and residency in scope
- [ ] G3.4 Customer-facing wording reviewed ("supports validation", not "compliant")

## Gate 4: Operations and surfaces
- [ ] G4.1 Safeguard tier and retention status visible in UX
- [ ] G4.2 (H) Runbooks and escalation SLAs published, on-call named
- [ ] G4.3 (H) Manual review staffed for forecast volume (capacity model in `docs/05`)
- [ ] G4.4 (H) Appeals path live
- [ ] G4.5 KPI dashboard live with definitions from `docs/06`

## Decision
Scorer output: GO / GO_WITH_WAIVERS / NO_GO. Waivers need approver name and expiry date.

| Function | Required reviewer | Signed | Date |
|---|---|---|---|
| Safeguards | | | |
| Identity | | | |
| Platform | | | |
| Legal | | | |
| Product | | | |
| T&S Ops | | | |
| **Accountable decision-maker** | | | |
