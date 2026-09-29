import unittest

from isomorphic_engine import CompositeIsomorphicController, IsomorphicASTController, IsomorphicLLMBridge, IsomorphicValidator


class MockLLM:
    def generate_sparse(self, prompt: str, schema: list[str]):
        return {"request_id": "REQ_11", "status": "200_OK", "currency": "USD"}


class TestISTEngine(unittest.TestCase):
    def test_controller_preserves_schema_and_fills_missing_tokens(self):
        schema = ["request_id", "status", "payload_hash", "execution_metric", "currency", "metadata"]
        controller = IsomorphicASTController(schema)
        payload = {"request_id": "REQ_001", "status": "200_OK"}

        mapped, latency_ms = controller.parse_isomorphic(payload)
        self.assertEqual(list(mapped), schema)
        self.assertEqual(mapped["request_id"], "REQ_001")
        self.assertEqual(mapped["status"], "200_OK")
        self.assertEqual(mapped["payload_hash"], "validated_token_2")
        self.assertGreaterEqual(latency_ms, 0.0)

    def test_validator_tracks_fallback_fields(self):
        schema = ["request_id", "status", "payload_hash"]
        controller = IsomorphicASTController(schema)
        validator = IsomorphicValidator(controller)

        mapped, _ = controller.parse_isomorphic({"request_id": "REQ_1"})
        diagnostics = validator.diagnose(mapped, {"request_id": "REQ_1"})
        self.assertTrue(diagnostics["fallback_fields"])
        self.assertFalse(diagnostics["structurally_complete"])

    def test_bridge_completes_sparse_llm_payload(self):
        schema = ["request_id", "status", "payload_hash", "execution_metric", "currency", "metadata"]
        bridge = IsomorphicLLMBridge(schema, MockLLM())
        full_ast, diagnostics = bridge.parse_with_llm_assistance("create payment payload")
        self.assertIn("request_id", full_ast)
        self.assertIn("status", full_ast)
        self.assertIn("payload_hash", full_ast)
        self.assertIn("currency", full_ast)
        self.assertTrue("filled_fields" in diagnostics)

    def test_composite_model_assembles_nested_schema(self):
        composite = CompositeIsomorphicController(
            base_schema=["request_id", "status"],
            sub_schemas={
                "payment": ["amount", "currency"],
                "meta": ["trace_id"],
            },
        )
        composed, _ = composite.parse_hierarchical({
            "request_id": "REQ_99",
            "status": "ok",
            "payment": {"amount": 42, "currency": "USD"},
            "meta": {"trace_id": "tr_1"},
        })
        self.assertEqual(composed["request_id"], "REQ_99")
        self.assertEqual(composed["sub_payment"]["amount"], 42)
        self.assertEqual(composed["sub_meta"]["trace_id"], "tr_1")


if __name__ == "__main__":
    unittest.main()
