import json

from isomorphic_engine import IsomorphicASTController, IsomorphicLLMBridge, IsomorphicValidator, MockLLM


class DemoLLM:
    def generate_sparse(self, prompt: str, schema: list[str]):
        base = {
            "request_id": "REQ_2026_007",
            "status": "200_OK",
            "currency": "USD",
        }
        if "payload_hash" in schema:
            base["payload_hash"] = "sha256:demo"
        return base


if __name__ == "__main__":
    schema = [
        "request_id",
        "status",
        "payload_hash",
        "execution_metric",
        "currency",
        "metadata",
    ]

    controller = IsomorphicASTController(schema)
    sample = {"request_id": "REQ_2026_001", "status": "200_OK"}
    mapped, latency_ms = controller.parse_isomorphic(sample)
    print(f"[controller] latency={latency_ms:.4f}ms")
    print(json.dumps(mapped, indent=2))

    bridge = IsomorphicLLMBridge(schema, DemoLLM())
    full_ast, diagnostics = bridge.parse_with_llm_assistance("Create a payment response")
    print(f"\n[bridge] filled_fields={diagnostics['filled_fields']}")
    print(json.dumps(full_ast, indent=2))

    validator = IsomorphicValidator(controller)
    validate_info = validator.diagnose(full_ast, {"request_id": "REQ_2026_007", "status": "200_OK", "currency": "USD"})
    print(f"\n[validator] structurally_complete={validate_info['structurally_complete']}")
    print(json.dumps(validate_info, indent=2))
