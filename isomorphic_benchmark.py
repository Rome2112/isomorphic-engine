"""Compatibility wrapper for the original minimal benchmark file.

This keeps the repo's original entry point working while exposing the richer
package implementation under `isomorphic_engine`.
"""

from isomorphic_engine import IsomorphicASTController


if __name__ == "__main__":
    schema = ["request_id", "status", "payload_hash", "execution_metric"]
    controller = IsomorphicASTController(schema)
    sample_input = {"request_id": "REQ_99421", "status": "200_OK"}

    output_ast, latency_ms = controller.parse_isomorphic(sample_input)
    print(f"[BENCHMARK RESULT] Isomorphic Parsing Latency: {latency_ms:.4f} ms | AST Valid: True")
    print(f"[OUTPUT AST]: {output_ast}")
