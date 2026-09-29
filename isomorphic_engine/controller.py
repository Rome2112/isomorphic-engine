import json
import time
from typing import Any


class IsomorphicASTController:
    """Deterministic schema-bound projection for IST-oriented pipelines.

    This controller does not attempt to be a general-purpose graph matcher. Its
    role is to enforce a known structural identity: the input is projected into a
    fixed schema and missing values are filled by deterministic placeholders.
    """

    def __init__(self, schema_keys: list[str]):
        if not isinstance(schema_keys, list):
            raise TypeError("schema_keys must be a list of strings")
        if any(not isinstance(key, str) or not key for key in schema_keys):
            raise ValueError("schema_keys must be a list of non-empty strings")
        if len(set(schema_keys)) != len(schema_keys):
            raise ValueError("schema_keys must not contain duplicates")

        self.schema_map = {key: idx for idx, key in enumerate(schema_keys)}
        self.k_bound = len(schema_keys)
        self.schema = list(schema_keys)

    def parse_json(self, payload: str) -> tuple[dict[str, Any], float]:
        """Parse a JSON object string and project it into the bound schema."""
        try:
            decoded = json.loads(payload)
        except (TypeError, json.JSONDecodeError) as exc:
            raise ValueError("payload must be valid JSON") from exc

        if not isinstance(decoded, dict):
            raise TypeError("payload JSON must contain an object")

        return self.parse_isomorphic(decoded)

    def parse_isomorphic(self, input_vector: dict[str, Any]) -> tuple[dict[str, Any], float]:
        """Project the raw dict into the controller's canonical schema."""
        if not isinstance(input_vector, dict):
            raise TypeError("input_vector must be a dictionary")

        start_time = time.perf_counter()
        mapped_ast: dict[str, Any] = {}

        for key, index in self.schema_map.items():
            value = input_vector.get(key)
            mapped_ast[key] = value if value is not None else f"validated_token_{index}"

        exec_time_ms = (time.perf_counter() - start_time) * 1000.0
        return mapped_ast, exec_time_ms

    def missing_fields(self, input_vector: dict[str, Any]) -> list[str]:
        """Return fields that are absent or None in the input."""
        return [key for key in self.schema if input_vector.get(key) is None]

    def fill_missing(self, input_vector: dict[str, Any]) -> dict[str, Any]:
        """Return a canonicalized mapping with deterministic fallback values."""
        return self.parse_isomorphic(input_vector)[0]
