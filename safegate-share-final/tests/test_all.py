import os, sys, unittest
from datetime import date, datetime, timezone
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from policy_resolver import AccessRequest, resolve_entitlement, load_policy
from readiness_scorer import evaluate_launch

NOW = datetime(2026, 11, 19, tzinfo=timezone.utc)
CLIN = ["ENTERPRISE_SSO", "BAA_SIGNED", "GXP_TENANT_FLAG", "IRB_PROTOCOL_REF"]


def req(**kw):
    base = dict(user_id="u", organization="o", persona="CLINICAL_TRIAL_MGR", vertical="PHARMA_ENTERPRISE",
                credentials=CLIN, requested_surfaces=["web"], attestation_expires_at="2027-05-01T00:00:00Z")
    base.update(kw)
    return AccessRequest(**base)


class ResolverTests(unittest.TestCase):
    def test_happy_path_zdr_with_customer_held_audit(self):
        r = resolve_entitlement(req(), now=NOW)
        self.assertEqual(r["status"], "VERIFIED_ACTIVE")
        m = r["resolved_modules"]
        self.assertEqual(m["data_retention"], "ZERO_DATA_RETENTION")
        self.assertEqual(m["audit_payload"], "HASHES_AND_METADATA_ONLY_CUSTOMER_HELD")

    def test_missing_persona_credential_blocks(self):
        r = resolve_entitlement(req(credentials=CLIN[:3]), now=NOW)
        self.assertEqual(r["status"], "PROVISIONING_BLOCKED")
        self.assertEqual(r["missing_credentials"], ["IRB_PROTOCOL_REF"])

    def test_unknown_persona_rejected_not_crash(self):
        self.assertEqual(resolve_entitlement(req(persona="NOPE"), now=NOW)["status"], "REJECTED_INVALID_REQUEST")

    def test_incompatible_persona_vertical(self):
        r = resolve_entitlement(req(vertical="MEDTECH_DEVICES"), now=NOW)
        self.assertIn("PERSONA_VERTICAL_NOT_SUPPORTED", r["reason_codes"])

    def test_expired_downgrades(self):
        r = resolve_entitlement(req(attestation_expires_at="2026-01-01T00:00:00Z"), now=NOW)
        self.assertEqual(r["status"], "EXPIRED_DOWNGRADED")
        self.assertEqual(r["profile"], "STANDARD_PUBLIC_SAFEGUARDS")

    def test_revoked_wins_over_valid_credentials(self):
        self.assertEqual(resolve_entitlement(req(revoked=True), now=NOW)["status"], "REVOKED")

    def test_connector_denied_without_credential(self):
        r = resolve_entitlement(req(credentials=CLIN, requested_surfaces=["web", "eln_lims_connector"]), now=NOW)
        self.assertEqual(r["resolved_modules"]["allowed_surfaces"], ["web"])
        self.assertIn("eln_lims_connector", r["denied_surfaces"])

    def test_persona_floor_tightens_academic_retention(self):
        pol = load_policy()
        pol["personas"]["CLINICAL_TRIAL_MGR"]["allowed_verticals"].append("ACADEMIC_RESEARCH")
        creds = ["INSTITUTIONAL_IDP", "ORCID_VERIFIED", "IRB_PROTOCOL_REF"]
        r = resolve_entitlement(req(vertical="ACADEMIC_RESEARCH", credentials=creds), pol, NOW)
        self.assertEqual(r["resolved_modules"]["data_retention"], "ZERO_DATA_RETENTION")


def gate(i, ws, status="PASS", hard=True):
    return {"id": i, "workstream": ws, "check": "c", "status": status, "hard_blocker": hard, "owner": "o"}


ALL = ["Safeguards", "Identity", "Platform Infra", "Legal/Compliance", "Product Surfaces"]


class ScorerTests(unittest.TestCase):
    def gates(self, **over):
        g = [gate(f"G{i}", ws) for i, ws in enumerate(ALL)]
        for k, v in over.items():
            for x in g:
                if x["id"] == k:
                    x["status"] = v
        return g

    def test_go(self):
        self.assertEqual(evaluate_launch("c", self.gates())["decision"], "GO")

    def test_not_started_hard_blocker_is_no_go(self):
        self.assertEqual(evaluate_launch("c", self.gates(G3="NOT_STARTED"))["decision"], "NO_GO")

    def test_waiver_needs_approver_and_unexpired(self):
        g = self.gates(G3="FAIL")
        w = [{"gate_id": "G3", "approver": "VP Legal", "expires": "2026-12-01"}]
        self.assertEqual(evaluate_launch("c", g, w, date(2026, 11, 19))["decision"], "GO_WITH_WAIVERS")
        self.assertEqual(evaluate_launch("c", g, w, date(2027, 1, 1))["decision"], "NO_GO")
        w[0]["approver"] = ""
        self.assertEqual(evaluate_launch("c", g, w, date(2026, 11, 19))["decision"], "NO_GO")

    def test_missing_workstream_no_go(self):
        self.assertEqual(evaluate_launch("c", self.gates()[:-1])["decision"], "NO_GO")

    def test_empty_gates_no_crash(self):
        self.assertEqual(evaluate_launch("c", [])["decision"], "NO_GO")

    def test_soft_failure_does_not_block(self):
        g = self.gates() + [gate("S1", "Product Surfaces", "FAIL", hard=False)]
        self.assertEqual(evaluate_launch("c", g)["decision"], "GO")


if __name__ == "__main__":
    unittest.main()
