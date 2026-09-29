from __future__ import annotations

from typing import Any, Protocol

from .controller import IsomorphicASTController


class SparseLLMAdapter(Protocol):
    """Minimal protocol for LLM adapters used by the bridge layer."""

    def generate_sparse(self, prompt: str, schema: list[str]) -> dict[str, Any]:
        """Return a sparse dict of high-confidence fields for the given schema."""


class IsomorphicLLMBridge:
    """Bridge intent generation from an LLM with structural enforcement by the engine."""

    def __init__(self, schema_keys: list[str], llm_client: SparseLLMAdapter):
        self.controller = IsomorphicASTController(schema_keys)
        self.llm_client = llm_client

    def parse_with_llm_assistance(self, prompt: str) -> tuple[dict[str, Any], dict[str, Any]]:
        """Ask the LLM for sparse intent data, then complete it with the controller."""
        sparse_payload = self.llm_client.generate_sparse(prompt, self.controller.schema)
        full_ast, latency_ms = self.controller.parse_isomorphic(sparse_payload)
        diagnostics = {
            "schema": self.controller.schema,
            "sparse_payload": sparse_payload,
            "output": full_ast,
            "latency_ms": latency_ms,
            "filled_fields": [k for k, v in full_ast.items() if str(v).startswith("validated_token_")],
        }
        return full_ast, diagnostics


class MockLLM:
    """Simple test adapter for integration demos."""

    def generate_sparse(self, prompt: str, schema: list[str]) -> dict[str, Any]:
        base = {
            "request_id": "REQ_1001",
            "status": "200_OK",
        }
        if "payload_hash" in schema:
            base["payload_hash"] = "hash_abc123"
        if "metadata" in schema:
            base["metadata"] = {"source": "llm"}
        return base
