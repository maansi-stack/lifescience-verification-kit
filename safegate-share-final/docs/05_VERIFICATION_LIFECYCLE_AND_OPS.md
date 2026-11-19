# 05. Verification Lifecycle and Operations

## States

```
SUBMITTED -> AUTO_CHECKS -> AUTO_VERIFIED ---------> PROVISIONED -> ACTIVE
                  |                                                  |  ^
                  +-> MANUAL_REVIEW -> APPROVED -----> PROVISIONED   |  |
                  |         |                                        v  |
                  |         +-> NEEDS_INFO (customer, clock paused)  EXPIRING (T-30)
                  |         +-> REJECTED -> APPEAL -> (UPHELD | OVERTURNED)       |
                  +-> REJECTED                                       v            |
                                                         RE_ATTEST --+            |
                                                              |                    |
                                                              v                    |
                                                         DOWNGRADED (expired) -----+ (re-verify)
Any state --(Trust and Safety action)--> REVOKED
```

## Risk-based tiers (proposal)

| Tier | Access | Proof | Review |
|---|---|---|---|
| 1 | Standard life-sciences use, no elevated capability | Org email domain or SSO | Automated |
| 2 | Regulated-data workflows (PHI, GxP) | Tier 1 + BAA, vertical credentials | Automated, manual on anomaly |
| 3 | Elevated biosecurity-calibrated capability | Tier 2 + entity vetting + persona attestation (PI/biosafety officer) | Always human review |

Which capabilities sit at Tier 3 is a Safeguards decision. The TPM's job is to make the tier boundary explicit and testable.

## What auto-checks do

Domain ownership and SSO match, entity existence and sanctions screening (via approved provider), credential registry lookups (ORCID, NPI, CLIA), duplicate or look-alike org detection, requester seniority vs claimed role. Outcome is pass, fail, or "route to human" with reason codes.

## Manual review standards

- Reviewer sees: auto-check output, submitted documents, reason codes. Not free-form guesses.
- Decision template: approve, reject, need info. Each with a coded reason.
- Second reviewer required for Tier 3 approvals and any override of an auto-check failure.
- Weekly sample of auto-verified cases audited for false accepts.

## SLAs (initial targets)

| Step | Target |
|---|---|
| Auto-verified to active | < 1 hour |
| Manual review first response | 2 business days |
| Manual review decision (complete package) | 5 business days |
| Appeal decision | 5 business days, different reviewer |
| Revocation takes effect | < 60 seconds (claim TTL 24h backstop) |
| Expiry notices | T-30, T-7, T-0 |

## Capacity model (illustrative numbers)

reviewers needed = (weekly applications x manual share x minutes per review) / productive minutes per reviewer-week

Example: 80 applications/week x 50% manual x 45 min = 1,800 min. At 1,500 productive minutes per reviewer-week that is about 1.2 reviewers. Add 30% for appeals, second-review, and re-attestation. Recompute whenever the auto-verification rate changes. Raising it from 50% to 80% cuts the manual load by 60%.

## Fraud and abuse patterns to design for

- Shell entities or look-alike domains posing as biotech.
- Legitimate org, illegitimate user (insider or departed employee). Mitigation: re-attestation, SSO deprovisioning events, admin-owned seat lists.
- Credential resale or sharing. Mitigation: per-user claims, anomaly detection on usage.
- Attestation shopping after a rejection (reapply under another org name). Mitigation: shared rejection signals.
- Social engineering of reviewers. Mitigation: coded decisions, second review on Tier 3.

## Appeals

Rejected applicants get a coded reason (without revealing detection methods), a path to supply more evidence, and an appeal reviewed by someone who did not make the original decision. Track overturn rate. A high rate means the auto-check or reviewer rules are wrong.

## Re-attestation

Cadence is 180 days for academic (turnover) and 12 months for enterprise (ASSUMPTION). Re-attestation is a lighter flow: confirm org, confirm persona still holds, confirm no change in use. Offboarded users are removed through SSO events, not only through the calendar.
