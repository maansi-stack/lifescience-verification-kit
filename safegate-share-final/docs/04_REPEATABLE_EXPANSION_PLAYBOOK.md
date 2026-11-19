# 04. Expansion Playbook

Principle: each wave needs less bespoke work than the last. Exit criteria are numeric and measured by `docs/06`. Starting thresholds are targets until Wave 1 sets baselines.

| | Wave 1: Design partners | Wave 2: Templated verticals | Wave 3: Self-serve GA |
|---|---|---|---|
| Cohort | 5-15 orgs (biotech R&D, academic compbio) | 50-200 orgs (clinical, genomics, medtech) | Global pharma, broad academic federation |
| Verification | Manual entity review, signed addendum, allowlisted org IDs | Automated domain/SSO checks, self-serve BAA/attestation, manual review by exception | Federated IdP/ORCID/NPI, continuous re-attestation |
| Surfaces | Web, batch API | + CTMS, ELN/LIMS connectors | All, partner-built connectors |
| TPM objective | Instrument baselines, learn failure modes | Replace tickets with config (`policy.json` profiles) | Hand off to steady-state KPI ownership |

## Entry criteria (all waves)

- Charter signed, single accountable sponsor named.
- Gate checklist instantiated for the cohort, gate IDs loaded in scorer.
- Support runbook and escalation owners named.
- Rollback path tested (suspend cohort claims without redeploy).

## Exit criteria

**Wave 1 -> 2**
- False-positive refusal rate on benign benchmark < 2%.
- Zero ZDR or audit defects over 30 days.
- Manual review time per case measured (baseline for capacity model).
- Every manual decision classified into a rule, a template, or "true judgment call".

**Wave 2 -> 3**
- Onboarding lead time 4 weeks -> under 48 hours for auto-verified orgs.
- Auto-verification pass rate >= 80% with sampled false-accept audit under agreed bound.
- Appeals SLA met 4 consecutive weeks.
- Re-attestation completion >= 90% before expiry in at least one full cycle.

**Wave 3 steady state**
- Program in KPI-monitoring mode, TPM load < 20% of Wave 2.
- New vertical or persona onboarded using only config, tests, and a checklist.

## Standard play for adding a vertical

1. Charter and RFC (trade-offs, options, recommendation).
2. Add vertical to `policy.json`, with credentials and retention. Legal reviews diff.
3. Safeguards builds or validates the domain eval suite.
4. Identity adds verification inputs and tests the claim.
5. Run scorer on gate file. Hold launch gate review.
6. Soft launch to allowlist. Review KPIs after 2 weeks. Open to cohort.
