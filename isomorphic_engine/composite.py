from __future__ import annotations

from typing import Any

from .controller import IsomorphicASTController


class CompositeIsomorphicController:
    """Compose multiple bounded schemas into a single hierarchical deterministic AST."""

    def __init__(self, base_schema: list[str], sub_schemas: dict[str, list[str]]):
        self.base = IsomorphicASTController(base_schema)
        self.sub_schemas = {name: IsomorphicASTController(fields) for name, fields in sub_schemas.items()}

    def parse_hierarchical(self, payload: dict[str, Any]) -> tuple[dict[str, Any], float]:
        import time

        start = time.perf_counter()
        base_payload = {k: v for k, v in payload.items() if k in self.base.schema_map}
        base_ast, _ = self.base.parse_isomorphic(base_payload)

        for name, controller in self.sub_schemas.items():
            nested = payload.get(name, {})
            if not isinstance(nested, dict):
                nested = {}
            sub_ast, _ = controller.parse_isomorphic(nested)
            base_ast[f"sub_{name}"] = sub_ast

        total_time = (time.perf_counter() - start) * 1000.0
        return base_ast, total_time
