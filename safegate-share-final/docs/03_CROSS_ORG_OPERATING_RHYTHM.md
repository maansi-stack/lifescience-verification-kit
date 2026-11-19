# 03. Operating Rhythm

## Teams

- **Safeguards and Biosecurity Science:** thresholds, red-team evals, utility benchmarks.
- **Identity, Trust and Provisioning:** verification pipeline, claims, revocation.
- **Platform and Infrastructure:** ZDR, residency, classifier routing, audit sink.
- **Product Surfaces:** UX, banners, human-in-the-loop gates, connectors.
- **Legal, Privacy and Regulatory:** BAA terms, Part 11 posture, retention schedules.
- **Trust and Safety Ops / Support:** manual review queue, appeals, abuse response.

## RACI

R = does the work, A = single accountable owner, C = consulted, I = informed.

| Milestone | TPM | Safeguards | Identity | Platform | Product | Legal | T&S Ops |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| Persona/vertical scope | A/R | C | C | I | R | C | C |
| Safety eval thresholds | C | A/R | I | I | I | C | C |
| Credential schema and claims | C | C | A/R | C | I | C | I |
| ZDR and audit pipeline | C | I | C | A/R | I | C | I |
| UX and review gates | C | C | I | I | A/R | I | I |
| Manual review playbook | R | C | C | I | I | C | A |
| Go/No-Go | R (runs gate) | RR | RR | RR | RR | RR | RR |

For Go/No-Go there is one **Accountable decision-maker**, named in the charter (typically the program sponsor). Function leads are **Required Reviewers (RR)**: each can issue a No-Go on their domain, and only the sponsor can approve a waiver. This avoids the unowned "five approvers" pattern.

## Cadence

| Forum | Frequency | Purpose | Output |
|---|---|---|---|
| Core standup | Weekly | Blockers, gate status | Weekly status (template) |
| Dependency review | Bi-weekly | Cross-team slips, trade-offs | Decision log entries |
| Verification ops review | Weekly in Waves 1-2 | Queue age, false rejects, appeals | KPI snapshot |
| Launch gate review | Per cohort | Go/No-Go | Scorer output + signed checklist |
| Exec readout | Monthly | Progress vs KPIs, asks | One-page summary |

## Escalation

| Sev | Trigger | Response |
|---|---|---|
| 1 | Safeguard bypass, PHI or ZDR leak risk, verified-credential fraud with elevated access | Circuit-breaker (suspend affected claims), incident bridge within 2h, TPM coordinates comms and timeline |
| 2 | Verified labs blocked by false-positive refusals, or verification queue breaches SLA | 24h triage Safeguards + Product (refusals) or T&S Ops (queue) |
| 3 | Cross-team dependency slip > 3 working days | TPM escalates at next dependency review with 2-3 pre-scoped options |

Rule: the TPM never escalates a problem without options and a recommended one.
