"""Isomorphic Structural Engine package.

This package captures the repository's IST philosophy: an LLM can focus on intent
while a deterministic controller enforces a known schema identity.
"""

from .controller import IsomorphicASTController
from .bridge import IsomorphicLLMBridge, SparseLLMAdapter
from .validator import IsomorphicValidator
from .composite import CompositeIsomorphicController
from .benchmark import benchmark_scaling

__all__ = [
    "IsomorphicASTController",
    "IsomorphicLLMBridge",
    "SparseLLMAdapter",
    "IsomorphicValidator",
    "CompositeIsomorphicController",
    "benchmark_scaling",
]
