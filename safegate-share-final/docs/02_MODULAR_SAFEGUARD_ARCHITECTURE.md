# 02. Architecture: Control Plane vs Data Plane

Slow, human-in-the-loop vetting must not sit in the request path. Two planes:

- **Control plane (async):** verifies org and persona, binds modules, mints signed claims.
- **Data plane (per request):** validates the claim signature and expiry, then routes to the safeguard classifier, retention pipeline, and audit sink. Latency budget is a **target to measure** in Wave 1 (initial proposal: single-digit to low-double-digit ms p99 added).

## Claim schema (v3)

```json
{
  "claim_version": "3",
  "policy_version": "3.0.0",
  "subject_id": "usr_98a71bc",
  "org_id": "org_example",
  "persona": "CLINICAL_TRIAL_MGR",
  "vertical": "PHARMA_ENTERPRISE",
  "status": "VERIFIED_ACTIVE",
  "attestation_expires_at": "2027-05-01T00:00:00Z",
  "claim_expires_at": "2026-11-20T07:00:00Z",
  "modules": {
    "safeguard_profile": "CLINICAL_SAFETY_STRICT",
    "data_retention": "ZERO_DATA_RETENTION",
    "audit_mode": "IMMUTABLE_GXP_LOG",
    "audit_payload": "HASHES_AND_METADATA_ONLY_CUSTOMER_HELD",
    "ux_guardrail": "HUMAN_IN_LOOP_CLINICAL_GATE",
    "allowed_surfaces": ["web", "ctms_connector"]
  }
}
```

Claims are short-lived (default 24h) and re-minted. Short TTL bounds revocation lag even if cache purge fails.

## Resolver decision order

1. Revoked: stop, deny.
2. Unknown persona/vertical or unsupported pair: reject.
3. Missing vertical or persona credentials: block, fall back to standard public safeguards.
4. Attestation expired: downgrade (below).
5. Surfaces: grant those whose credentials are present, report the rest.
6. Retention: strictest of vertical default and persona floor.

## Resolving ZDR vs immutable audit

Clinical and regulatory personas need an immutable audit trail and zero data retention. Read literally these conflict, because an audit log of prompts and responses is retained data. The kit's position (ASSUMPTION, Legal and Regulatory must confirm):

- The vendor retains **no content**.
- The audit trail is **hashes plus metadata** (timestamp, model snapshot ID, claim ID, prompt/response digest, reviewer sign-off), written to a **customer-held** immutable store.
- The customer, who owns Part 11 validation, can prove a record is unaltered by re-hashing their own copy.
- `audit_payload` in the claim tells surfaces which mode applies.

If a customer needs full content in the audit log, they hold it. The vendor does not.

## Expiry and revocation

- **Expiry:** downgrade to `STANDARD_PUBLIC_SAFEGUARDS`, web only, read-only access to prior benign history. No hard lockout. Notify at T-30 and T-7 days.
- **Revocation:** event-driven cache purge target under 60s, backed by the 24h claim TTL. Revocation always wins over valid credentials.
- **Policy version bumps:** a new `policy_version` triggers re-resolution at next claim mint. Never silently loosen existing claims.
