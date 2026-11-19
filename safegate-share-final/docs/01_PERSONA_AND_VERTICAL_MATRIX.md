# 01. Persona and Vertical Matrix

Entitlement = who the user is (persona) x where they work (vertical) x what proof they hold (credentials) x where they want to use it (surface). Canonical identifiers below match `data/policy.json`.

## Personas

| Persona ID | Workflows | Persona credential | Safeguard profile | Audit mode | Retention floor |
|---|---|---|---|---|---|
| `BENCH_SCIENTIST` | Protein analysis, assay design, literature synthesis, guide-RNA design, cheminformatics | `PI_BIOSAFETY_ATTESTATION` | `BIO_RESEARCH_CALIBRATED` | `STANDARD_TELEMETRY` | none |
| `CLINICAL_TRIAL_MGR` | Protocol synopses, eligibility criteria, site feasibility, AE narrative triage | `IRB_PROTOCOL_REF` | `CLINICAL_SAFETY_STRICT` | `IMMUTABLE_GXP_LOG` | ZDR |
| `LAB_OPS_DIRECTOR` | ELN/LIMS automation, SOP standardization, inventory, instrument QC | `ADMIN_ROLE_BINDING` | `SOP_WORKFLOW_STANDARD` | `VERSIONED_SOP_AUDIT` | none |
| `REGULATORY_QA_LEAD` | Submission drafting, Part 11 prep, ISO 13485 design history, post-market surveillance | `COMPLIANCE_ADMIN_ATTESTATION` | `DETERMINISTIC_CITATION_STRICT` | `21_CFR_PART_11_ARCHIVE` | ZDR |

## Verticals

| Vertical ID | Pressure | Required credentials | Default retention |
|---|---|---|---|
| `BIOTECH_RND` | Dual-use screening, sequence IP, small fast teams | `ENTITY_VETTED`, `BIOSECURITY_ATTESTATION` | ZDR |
| `PHARMA_ENTERPRISE` | Multi-region GxP, Part 11 records, multi-org RBAC | `ENTERPRISE_SSO`, `BAA_SIGNED`, `GXP_TENANT_FLAG` | ZDR |
| `MEDTECH_DEVICES` | ISO 13485, 510(k)/PMA traceability | `ENTERPRISE_SSO`, `ISO_13485_SCOPE` | ZDR |
| `GENOMICS_DX` | CLIA/CAP, variant interpretation, genomic privacy | `CLIA_CAP_CERT`, `BAA_SIGNED` | ZDR |
| `ACADEMIC_RESEARCH` | Turnover, grant budgets, open science vs biosecurity | `INSTITUTIONAL_IDP`, `ORCID_VERIFIED` | 30-day ephemeral, no training |

## Supported persona x vertical pairs (ASSUMPTION)

| | Biotech | Pharma | MedTech | Genomics | Academic |
|---|:-:|:-:|:-:|:-:|:-:|
| Bench Scientist | Y | Y | | Y | Y |
| Clinical Trial Mgr | Y | Y | | Y | |
| Lab Ops Director | Y | Y | Y | Y | Y |
| Regulatory/QA Lead | Y | Y | Y | Y | |

Unsupported pairs are rejected with `PERSONA_VERTICAL_NOT_SUPPORTED`. Each rejected pair seen in production is a demand signal for the next wave.

## Surfaces

| Surface | Extra credential |
|---|---|
| `web`, `batch_api` | none |
| `ctms_connector` | `BAA_SIGNED` |
| `eln_lims_connector` | `ADMIN_ROLE_BINDING` |

## Governance modules

- **A. Dual-use safeguards:** refusal boundaries calibrated to verified credentials. Owned by Safeguards.
- **B. Data and retention:** ZDR, residency, PHI controls. Owned by Platform and Privacy.
- **C. GxP auditability:** logging, model pinning, human approval gates. Owned by Platform and Regulatory.
- **D. Connectors:** read/write scope into ELN, LIMS, CTMS. Owned by Product.
