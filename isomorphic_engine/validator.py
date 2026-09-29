from __future__ import annotations

from typing import Any

from .controller import IsomorphicASTController


class IsomorphicValidator:
    """Diagnostic validator for partial / sparse payloads against the schema."""

    def __init__(self, controller: IsomorphicASTController):
        self.controller = controller

    def coverage(self, parsed_ast: dict[str, Any], original_input: dict[str, Any]) -> dict[str, dict[str, Any]]:
        """Return source metadata for each field: user-supplied vs engine-generated."""
        coverage: dict[str, dict[str, Any]] = {}
        for key in self.controller.schema:
            raw_value = original_input.get(key)
            value = parsed_ast.get(key)
            coverage[key] = {
                "value": value,
                "source": "input" if raw_value is not None else "engine_fallback",
                "is_fallback": value is not None and str(value).startswith("validated_token_"),
            }
        return coverage

    def is_valid(self, parsed_ast: dict[str, Any], required_fields: set[str] | None = None) -> bool:
        """Check that required fields passed through without relying on engine tokens."""
        if required_fields is None:
            required_fields = set()

        for key in required_fields:
            value = parsed_ast.get(key)
            if value is None or str(value).startswith("validated_token_"):
                return False
        return True

    def diagnose(self, parsed_ast: dict[str, Any], original_input: dict[str, Any]) -> dict[str, Any]:
        """Return a compact assessment of structural integrity."""
        coverage = self.coverage(parsed_ast, original_input)
        fallback_fields = [key for key, meta in coverage.items() if meta["is_fallback"]]
        required_missing = [key for key, meta in coverage.items() if meta["source"] == "engine_fallback"]
        return {
            "fallback_fields": fallback_fields,
            "required_missing": required_missing,
            "coverage": coverage,
            "structurally_complete": not fallback_fields,
        }
