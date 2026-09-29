import json

from isomorphic_engine import IsomorphicASTController, CompositeIsomorphicController


def run_demo() -> None:
    schema = ["request_id", "status", "payload_hash", "execution_metric", "currency", "metadata"]
    controller = IsomorphicASTController(schema)
    payload = {"request_id": "REQ_99421", "status": "200_OK"}
    mapped, latency = controller.parse_isomorphic(payload)
    print("[controller]")
    print(json.dumps({"latency_ms": round(latency, 4), "mapped": mapped}, indent=2))

    composite = CompositeIsomorphicController(
        base_schema=["request_id", "status"],
        sub_schemas={
            "payment": ["amount", "currency", "receipt_id"],
            "meta": ["source", "region"],
        },
    )
    nested = {
        "request_id": "REQ_101",
        "status": "pending",
        "payment": {"amount": 100.0, "currency": "USD"},
        "meta": {"region": "US"},
    }
    composed, comp_latency = composite.parse_hierarchical(nested)
    print("\n[composite]")
    print(json.dumps({"latency_ms": round(comp_latency, 4), "mapped": composed}, indent=2))


if __name__ == "__main__":
    run_demo()
