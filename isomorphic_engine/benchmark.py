import time
from typing import Any

from .controller import IsomorphicASTController


def benchmark_scaling(max_schema_size: int = 200, trials: int = 50) -> dict[str, Any]:
    """Benchmark the engine across increasing schema sizes and payload sizes."""
    results: dict[str, Any] = {}

    for schema_size in [10, 25, 50, 100, max_schema_size]:
        schema = [f"field_{idx}" for idx in range(schema_size)]
        controller = IsomorphicASTController(schema)
        sizes = [10, 50, 100]
        result_rows: list[dict[str, float]] = []

        for payload_size in sizes:
            payload = {schema[idx % schema_size]: f"value_{idx}" for idx in range(payload_size)}
            latencies: list[float] = []
            for _ in range(trials):
                _, latency_ms = controller.parse_isomorphic(payload)
                latencies.append(latency_ms)
            result_rows.append({
                "payload_size": payload_size,
                "avg_latency_ms": round(sum(latencies) / len(latencies), 6),
                "p95_latency_ms": round(sorted(latencies)[int(len(latencies) * 0.95)], 6),
            })

        results[f"schema_{schema_size}"] = result_rows

    return results


def benchmark_demo() -> None:
    """Small CLI benchmark for local demonstration."""
    start = time.perf_counter()
    report = benchmark_scaling()
    elapsed = (time.perf_counter() - start) * 1000.0
    print(f"[IST BENCHMARK] completed in {elapsed:.3f} ms")
    for schema_name, rows in report.items():
        print(schema_name)
        for row in rows:
            print(f"  payload={row['payload_size']} avg={row['avg_latency_ms']:.6f}ms p95={row['p95_latency_ms']:.6f}ms")


if __name__ == "__main__":
    benchmark_demo()
