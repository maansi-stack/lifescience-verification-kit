# 06. KPIs and Metrics

Report weekly in Waves 1-2, monthly in Wave 3. Every metric has an owner and a source of truth.

## Verification funnel

| Metric | Definition | Initial target | Owner |
|---|---|---|---|
| Time to verify, p50 / p90 | Submit to ACTIVE, excluding customer-wait time | Auto < 1h; manual p90 < 5 business days | T&S Ops |
| Auto-verification rate | Auto-verified / total decided | >= 80% by end of Wave 2 | Identity |
| False reject rate | Legit orgs rejected, found via appeal or audit | Set after Wave 1 baseline | T&S Ops |
| False accept rate | Sampled auto-verified cases that should not pass | Bound agreed with Safeguards | Safeguards |
| Appeal overturn rate | Overturned / appeals | < 15% (higher means rules are wrong) | T&S Ops |
| Queue age p90 | Age of oldest 10% of open manual cases | < SLA | T&S Ops |
| Re-attestation completion | Completed before expiry / due | >= 90% | Identity |

## Safeguards and utility

| Metric | Initial target | Owner |
|---|---|---|
| Benign false-positive refusal rate (benchmark) | < 2% | Safeguards |
| Benign non-refusal on lab/clinical prompts | >= 98% | Safeguards |
| Red-team bypass rate on verified tier | At or below agreed bound | Safeguards |
| Escalations per 100 verified orgs | Track trend | TPM |

## Platform and compliance

| Metric | Target | Owner |
|---|---|---|
| Revocation propagation p99 | < 60s | Identity |
| Claim validation latency added p99 | Set in Wave 1 | Platform |
| ZDR audit defects (30-day) | 0 | Platform |
| Audit-log verification failures | 0 | Platform |

## Program and business

| Metric | Definition |
|---|---|
| Onboarding lead time | Contract signed to first verified use |
| Bespoke-work ratio | Engineering tickets per newly onboarded org (should fall each wave) |
| Verified orgs / active users by vertical and persona | Demand and adoption |
| Unsupported persona-vertical requests | Demand signal for next wave |
| Support tickets per 100 verified orgs | Operational load |
| Milestone slip days | Plan vs actual per workstream |

## Rules for using the numbers

- Publish definitions before launch. Do not redefine mid-wave.
- Pair every speed metric with a quality metric (time to verify with false accept rate).
- Targets in this kit are placeholders until Wave 1 baselines exist. Say so in readouts.
