# 09. TPM Narrative and Wave 1 Plan

## One-page program narrative

**Problem.** Verification Program is in beta and gives verified life science professionals a refined, more permissive safeguard set for biology work. Expanding it (new plan and account types, new platforms, new org categories) touches many teams, and no one owns the whole path. Life sciences customers need the AI system to be more useful on legitimate biology and clinical work than a one-size-fits-all safeguard setting allows. The elevated capabilities carry dual-use risk, so access depends on knowing who the user is. Today that decision is bespoke, slow, and hard to repeat.

**Program.** Build a verification program that turns "is this org and persona legitimate, and what may they do?" into a repeatable pipeline: intake, auto-checks, human review by exception, a signed claim, runtime enforcement, re-attestation, revocation.

**Principles.**
1. Verification calibrates safeguards inside limits that Safeguards defines and owns. The TPM never sets those limits.
2. Strictest rule wins. Unknown input is rejected. Revocation fails closed.
3. Policy is data under review by Safeguards and Legal, so new verticals are config, not bespoke engineering.
4. Pair every speed metric with a quality metric.
5. Each wave needs less bespoke work than the last.

**Waves.** Design partners (manual, learn) -> templated verticals (automate the common path) -> self-serve (hand to steady-state).

**What I would own as TPM.** Single-threaded program plan across Safeguards, Identity, Platform, Product, Legal, and Trust and Safety Ops. Decision log, dependency reviews, launch gates, KPI definitions, and the trade-off RFCs that put options in front of decision-makers.

## Wave 1 plan (13 weeks, relative dates)

| Week | Milestone | Owner | Gate or output |
|---|---|---|---|
| 0-1 | Charter, sponsor, scope (2 personas x 2 verticals x 2 surfaces), KPI definitions | TPM | Charter signed |
| 1-2 | Surface parity matrix: ZDR, BAA, connectors per surface | TPM + Product | Matrix, drives surface scope |
| 1-3 | Tier boundaries and Tier 3 criteria | Safeguards | Written tier policy |
| 2-4 | `policy.json` v1 reviewed by Safeguards, Legal, Identity | TPM | Approved policy diff |
| 2-5 | Verification intake + auto-check MVP (domain, SSO, ORCID, entity) | Identity | G2.1 |
| 3-6 | Domain eval suites (benign utility, bypass) | Safeguards | G1.1, G1.2 |
| 3-6 | Customer-held audit log design and Legal review | Platform + Legal | G3.2 |
| 4-7 | Manual review playbook, reviewer training, capacity model | T&S Ops | G4.3 |
| 5-8 | ZDR verification and revocation drill | Platform + Identity | G3.1, G2.3 |
| 7-8 | Support runbooks, appeals path, KPI dashboard | T&S Ops + TPM | G4.2, G4.4, G4.5 |
| 9 | Launch gate review (scorer + signed checklist) | TPM | GO / GO_WITH_WAIVERS / NO_GO |
| 10-12 | Soft launch to allowlisted 5-15 partners, weekly KPI review | TPM | Baselines |
| 13 | Wave 1 exit review, classify every manual decision as rule, template, or judgment | TPM | Wave 2 plan |

Critical path: surface parity matrix -> tier policy -> policy review -> auto-checks -> launch gate. Biggest schedule risk: Legal sign-off on the audit log (R4). Start it in week 3 at the latest.
