#!/usr/bin/env python3
"""SafeGate-AI v3: persona x vertical entitlement resolver.

Pure function over data/policy.json. Stdlib only. Every decision carries
reason codes and the policy version so outcomes are explainable and auditable.
"""
import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

POLICY_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "policy.json")


def load_policy(path: str = POLICY_PATH) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


@dataclass
class AccessRequest:
    user_id: str
    organization: str
    persona: str
    vertical: str
    credentials: List[str]
    requested_surfaces: List[str]
    attestation_expires_at: Optional[str] = None  # ISO-8601 UTC, e.g. 2027-05-01T00:00:00Z
    revoked: bool = False


def _parse(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def _decision(req: AccessRequest, policy: dict, status: str, reasons: List[str], **extra) -> dict:
    out = {
        "user_id": req.user_id,
        "organization": req.organization,
        "status": status,
        "reason_codes": reasons,
        "policy_version": policy["policy_version"],
    }
    out.update(extra)
    return out


def resolve_entitlement(req: AccessRequest, policy: Optional[dict] = None,
                        now: Optional[datetime] = None) -> dict:
    policy = policy or load_policy()
    now = now or datetime.now(timezone.utc)

    # 1. Revocation beats everything. Fail closed.
    if req.revoked:
        return _decision(req, policy, "REVOKED", ["REVOKED_BY_TRUST_AND_SAFETY"],
                         profile=policy["downgrade_profile"], allowed_surfaces=[])

    # 2. Input validation: unknown enums are rejected, never defaulted.
    persona = policy["personas"].get(req.persona)
    vertical = policy["verticals"].get(req.vertical)
    reasons = []
    if persona is None:
        reasons.append("UNKNOWN_PERSONA")
    if vertical is None:
        reasons.append("UNKNOWN_VERTICAL")
    if reasons:
        return _decision(req, policy, "REJECTED_INVALID_REQUEST", reasons)
    if req.vertical not in persona["allowed_verticals"]:
        return _decision(req, policy, "REJECTED_INVALID_REQUEST", ["PERSONA_VERTICAL_NOT_SUPPORTED"])

    # 3. Credentials: vertical-level plus persona-level.
    required = set(vertical["required_credentials"]) | set(persona["extra_credentials"])
    missing = sorted(required - set(req.credentials))
    if missing:
        return _decision(req, policy, "PROVISIONING_BLOCKED", ["MISSING_CREDENTIALS"],
                         missing_credentials=missing, profile=policy["downgrade_profile"],
                         allowed_surfaces=[])

    # 4. Expiry: graceful downgrade, not lockout.
    if req.attestation_expires_at and _parse(req.attestation_expires_at) <= now:
        return _decision(req, policy, "EXPIRED_DOWNGRADED", ["ATTESTATION_EXPIRED"],
                         profile=policy["downgrade_profile"], allowed_surfaces=["web"],
                         history_access="READ_ONLY_BENIGN")

    # 5. Surfaces: grant only what credentials support; report what was denied.
    granted, denied = [], {}
    for s in req.requested_surfaces:
        spec = policy["surfaces"].get(s)
        if spec is None:
            denied[s] = ["UNKNOWN_SURFACE"]
            continue
        gap = sorted(set(spec["requires"]) - set(req.credentials))
        if gap:
            denied[s] = ["MISSING_" + c for c in gap]
        else:
            granted.append(s)

    # 6. Retention: strictest of vertical default and persona floor wins.
    rank = policy["retention_rank"]
    retention = vertical["retention"]
    floor = persona["retention_floor"]
    if floor and rank[floor] < rank[retention]:
        retention = floor

    modules = {
        "safeguard_profile": persona["safeguard_profile"],
        "audit_mode": persona["audit_mode"],
        "ux_guardrail": persona["ux_guardrail"],
        "data_retention": retention,
        "allowed_surfaces": granted,
    }
    # ZDR vs immutable audit: vendor keeps no content; customer holds the log.
    if persona["audit_mode"] in policy["audit_modes_requiring_customer_held_log"]:
        modules["audit_payload"] = (
            "HASHES_AND_METADATA_ONLY_CUSTOMER_HELD" if retention == "ZERO_DATA_RETENTION"
            else "FULL_CONTENT_CUSTOMER_HELD")

    exp = now + timedelta(hours=policy["claim_ttl_hours"])
    if req.attestation_expires_at:
        exp = min(exp, _parse(req.attestation_expires_at))
    return _decision(req, policy, "VERIFIED_ACTIVE", ["ALL_CHECKS_PASSED"],
                     persona=req.persona, vertical=req.vertical, resolved_modules=modules,
                     denied_surfaces=denied, claim_expires_at=exp.isoformat())


if __name__ == "__main__":
    # All organizations and user IDs below are fictional examples.
    pol = load_policy()
    reqs = [
        AccessRequest("usr_bio_01", "Cascade Protein Design Inc.", "BENCH_SCIENTIST", "BIOTECH_RND",
                      ["ENTITY_VETTED", "BIOSECURITY_ATTESTATION", "PI_BIOSAFETY_ATTESTATION"],
                      ["web", "batch_api"], "2027-05-01T00:00:00Z"),
        AccessRequest("usr_clin_02", "Meridian Global Pharma", "CLINICAL_TRIAL_MGR", "PHARMA_ENTERPRISE",
                      ["ENTERPRISE_SSO", "BAA_SIGNED", "GXP_TENANT_FLAG", "IRB_PROTOCOL_REF"],
                      ["web", "ctms_connector", "eln_lims_connector"], "2027-05-01T00:00:00Z"),
        AccessRequest("usr_reg_03", "CardioPulse Medical Devices", "REGULATORY_QA_LEAD", "MEDTECH_DEVICES",
                      ["ENTERPRISE_SSO"], ["web"]),
        AccessRequest("usr_acad_04", "Pacific University Structural Biology Lab", "BENCH_SCIENTIST",
                      "ACADEMIC_RESEARCH",
                      ["INSTITUTIONAL_IDP", "ORCID_VERIFIED", "PI_BIOSAFETY_ATTESTATION"],
                      ["web"], "2026-01-01T00:00:00Z"),
    ]
    print(json.dumps([resolve_entitlement(r, pol) for r in reqs], indent=2))
