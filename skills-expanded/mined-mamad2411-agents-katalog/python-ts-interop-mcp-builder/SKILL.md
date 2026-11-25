---
name: python-ts-interop-mcp-builder
description: Design Python and TypeScript interoperability patterns, including MCP-style tool contracts and typed boundaries.
---

# Python + TS Interop (MCP Builder)

## Objective
Implement reliable interop between Python services and TypeScript apps through typed, testable contracts.

## Interop Strategy
1. Define shared request/response contracts first.
2. Generate or hand-maintain compatible types in Python and TypeScript.
3. Normalize errors into a stable cross-language format.
4. Add tracing IDs and structured logs for observability.

## Implementation Guidelines
- Python: pydantic/dataclass schemas where possible.
- TypeScript: strict types with runtime validation for unknown inputs.
- Never trust unvalidated payloads across process boundaries.
- Keep transport-agnostic adapters (HTTP, RPC, MCP tool calls).

## Testing
- Contract tests on both sides.
- Golden payload fixtures for backward compatibility.
- Failure-path tests (timeouts, malformed payloads, partial responses).

## Output Format
- Contract spec.
- Python and TS adapter plan.
- Error model and observability plan.
- Test matrix.
