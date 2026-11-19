# 07. Risk Register

Likelihood and impact are L/M/H. Review bi-weekly at dependency review.

| ID | Risk | L | I | Early signal | Mitigation | Owner |
|---|---|:-:|:-:|---|---|---|
| R1 | Fraudulent entity or user obtains elevated access | M | H | Look-alike domains, new org with Tier 3 request, usage anomalies | Tiered review, second reviewer on Tier 3, anomaly alerts, fast revocation | Safeguards / T&S Ops |
| R2 | Over-refusal blocks legitimate scientists, erodes adoption | M | H | Refusal rate above 2%, support tickets citing refusals | Domain eval suite, calibrated profiles, 24h triage SLA | Safeguards |
| R3 | ZDR claim violated by logs, traces, or caches | L | H | Log-scrub test failures | Automated ZDR tests in launch gate, quarterly audit | Platform |
| R4 | ZDR vs audit-log conflict unresolved at launch | M | H | Legal has not signed off on customer-held log | Make G3.2 a hard blocker, decide in RFC | Legal / TPM |
| R5 | Manual review becomes the bottleneck | H | M | Queue age p90 rising | Capacity model, auto-check coverage, templates, surge plan | T&S Ops |
| R6 | Revocation lag leaves access live after trust withdrawn | L | H | Purge test p99 over 60s | 24h claim TTL backstop, drills each quarter | Identity |
| R7 | Dependency slips (Identity, Platform) delay waves | H | M | Milestone slip > 3 days | Bi-weekly review, pre-scoped options, de-scope plan | TPM |
| R8 | Policy drift: config changes loosen controls without review | M | H | Unreviewed edits to `policy.json` | Code-owner review (Safeguards + Legal), policy version in every decision | TPM |
| R9 | Regulatory interpretation changes (Part 11, GINA/HIPAA, EU) | L | H | Legal advisory notices | Legal watch, region flags in policy | Legal |
| R10 | Re-attestation wave causes mass downgrades | M | M | Completion rate < 70% at T-14 | Staged notices, admin-level bulk re-attest, grace period | Identity / T&S Ops |
| R11 | Customers misread "verified" as "compliant" | M | M | Sales or customer language | Standard wording: platform supports customer validation, does not certify compliance | Legal / Product |
| R12 | Reviewer inconsistency across manual decisions | M | M | Overturn rate, audit variance | Decision templates, calibration sessions, sampled QA | T&S Ops |
