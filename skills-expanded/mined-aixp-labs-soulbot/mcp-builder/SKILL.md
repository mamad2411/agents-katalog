---
name: "mcp-builder"
description: "AISP-backed bridge for AISP V1.0.0 skill that guides building MCP servers in Python (FastMCP) or Node/TypeScript SDK via the four-phase flow Research-and-Plan -> Implement -> Review-and-Test -> Create-Evaluations, producing a server plus a read-only evaluation suite. Nine sys.assert/tools-bound non-negotiable rules cover strict schemas, tool annotations, actionable errors, offset pagination, no-stdout-on-stdio, read-only evals, open-world docs, http-auth presence, and allow-list-only (default-deny) SSRF egress. Use when The user wants to build an MCP (Model Context Protocol) server that lets an LLM call an external service or API through well-designed tools.; The user is writing an MCP server in Python with FastMCP or in Node/TypeScript with the MCP SDK and wants the recommended structure, strict input schemas, annotations, error handling, and pagination. Do not use when The user wants generic (non-MCP) application or API code generation with no MCP server involved.; The user wants to run destructive or st..."
license: "Apache-2.0"
metadata:
  generated_from_aisp: "true"
  aisp_program: "aisp.aisop.json"
  protocol: "AISP V1.0.0"
  bridge_mode: "native_sidecar"
---

# MCP Server Builder (AISP-backed Agent Skill)

<!-- generated_from_aisp: true -->
<!-- source: aisp.aisop.json -->
<!-- generator: tools/aisp_skill_md.py -->

This `SKILL.md` is a thin Agent Skills discovery bridge, not the source of truth. The executable source of truth is the same-folder `aisp.aisop.json` AISP program.

Deleting this file does not change the native AISP skill. A conforming AISP/AISOP runtime should load `aisp.aisop.json`, read `user.content.aisp_contract`, and run `user.content.aisop.main` exactly as declared.

## How to use

1. Load `aisp.aisop.json` from this folder.
2. Read `user.content.aisp_contract` before following any workflow.
3. Follow `user.content.instruction`: `STRICTLY OBEY aisp_contract; its non_negotiable rules are inviolable and bound to real enforcement mechanisms; then RUN aisop.main.`.
4. Load declared resources only when the AISP graph reaches the node that needs them.
5. Enforce every non-negotiable rule through the mechanism named by `enforced_by`.

## Declared resources

- `reference/mcp_best_practices.md` (doc, read_only)
- `reference/python_mcp_server.md` (doc, read_only)
- `reference/node_mcp_server.md` (doc, read_only)
- `reference/evaluation.md` (doc, read_only)

## Non-negotiable boundaries

- NN1 — Evaluation questions MUST be read-only, non-destructive, and idempotent: every authored qa_pair may only require tool calls whose readOnlyHint=true / destructiveHint=false, and any qa_pair that would require a WRITE or DESTRUCTIVE operation is dropped. Source: reference/evaluation.md (questions must require only non-destructive and idempotent tool use; verification step flags and removes any qa_pair requiring write/destructive operations). (`EvalGen.step3:sys.assert`)
- NN5 — Tool/API errors MUST be actionable: the generated server returns helpful, specific error messages with a suggested next step INSIDE the result object (isError), never throwing raw exceptions and never leaking internal implementation details. Source: SKILL.md (error messages should guide agents toward solutions with specific suggestions and next steps) + reference/mcp_best_practices.md L206-211. (`ReviewTest.step2:sys.assert`)
- NN6 — Every tool MUST declare all four annotation hints (readOnlyHint, destructiveHint, idempotentHint, openWorldHint) as booleans. This is a STRUCTURAL presence + boolean-type check, NOT a proof of semantic truthfulness — the annotations are hints, not security guarantees. Source: SKILL.md L119-124 + reference/mcp_best_practices.md L60/L190-201. (`ImplementPy.step3:sys.assert`)
- NN7 — Tool input validation MUST use a strict schema: Pydantic ConfigDict(extra='forbid') in Python or Zod .strict() in TypeScript, forbidding extra fields; ad-hoc hand-written if-checks are rejected. Source: reference/python_mcp_server.md (Pydantic models handle input validation, ConfigDict extra='forbid') + reference/node_mcp_server.md (Zod .strict() to forbid extra fields) + reference/mcp_best_practices.md L172. (`ImplementPy.step4:sys.assert`)
- NN8 — List/collection tools MUST paginate: respect the limit parameter and return has_more and next_offset (plus total_count). next_offset is the tool-RESULT offset pagination convention faithful to reference/mcp_best_practices.md L20-23 / L84-104; it is a DISTINCT layer from the MCP protocol-transport opaque cursor (nextCursor) and MUST NOT be rewritten to nextCursor. (`ReviewTest.step3:sys.assert`)
- NN9 — stdio servers MUST NOT log to stdout: stdout is the JSON-RPC channel, so all logging goes to stderr (Python logging->stderr, Node console.error, never console.log/print on the stdio transport path). Source: reference/mcp_best_practices.md L139 + reference/node_mcp_server.md (console.error for stdio logging). (`ReviewTest.step4:sys.assert`)
- NN10 — External MCP/SDK documentation is ON-DEMAND / OPEN-WORLD: it is fetched at runtime via web_fetch (modelcontextprotocol.io spec pages, python-sdk README, typescript-sdk README) and is NEVER bundled as static skill content. The skill therefore declares web_search/web_fetch with openWorldHint=true and marks those external URLs as open_world/runtime, not as static read_only resources. Source: SKILL.md L41-43/L61/L65/L203/L212-213. (`tools`)
- NN11 — When transport is http/remote, the generated server MUST declare an authorization section: a STRUCTURAL presence + type check that an auth/authorization block exists on the http/remote transport path (i.e. it is NOT left unauthenticated). This is presence-only, mirroring NN6's framing — it verifies the auth section is PRESENT and structured, NOT that the auth is cryptographically correct or unbypassable (no semantic security guarantee). For stdio transport the check is vacuously satisfied (no network auth surface). The recommended shape (OAuth 2.1 authorization-code + mandatory PKCE(S256) + token-audience validation per RFC 8707/RFC 9068, and no raw client-token passthrough to upstream APIs) lives in discovery.guidance; this red line only asserts the presence of the section, not its semantic strength. Source: MCP 2025-11-25 authorization spec + reference/mcp_best_practices.md. (`ReviewTest.step5:sys.assert`)
- NN12 — Outbound fetch MUST be SSRF-safe under an ALLOW-LIST-ONLY (default-deny) egress policy: any LLM-provided / user-provided URL the generated server would fetch MUST be validated against an explicit, statically-declared allow-list, and ONLY hosts on that allow-list may egress — every undeclared host is blocked (default-deny). There is NO default public-internet egress: an outbound-fetch path that permits arbitrary public URLs so long as private/loopback/link-local ranges are blocked is REJECTED, because blocking private ranges alone still leaves the whole public internet reachable. Private / loopback / link-local egress remains blocked as before, but is now a subset of the default-deny posture rather than the whole guarantee. This is a DETERMINISTICALLY assertable structural check over the emitted server (a default-deny allow-list gate is present on the outbound-fetch path: the URL host is checked against an explicit allow-list and rejected when absent). The non-deterministic threats — prompt-injection, tool-poisoning, confused-deputy, and token-passthrough — are NOT asserted here; they remain LLM-judgement guidance in discovery.guidance with no fabricated enforced_by. Source: MCP 2026 security best practices + reference/mcp_best_practices.md security section + OWASP SSRF default-deny allow-list guidance. (`ReviewTest.step6:sys.assert`)

## Runtime boundary

Agent Skills platforms can use this bridge to discover and inspect the package. Hard guarantees such as `sys.assert`, `sys.io.confirm`, tool gating, dispatch behavior, and path confinement require a conforming AISP/AISOP runtime. A generic non-AISOP agent can only follow the contract on a best-effort basis.

Passing `SKILL.md` generation or bridge validation proves only projection consistency and bridge shape. It does not prove external trust, safety, registry approval, or hard execution on a non-AISOP platform.

Align Axiom 0: Human Sovereignty and Wellbeing. AISP - AI Skill Protocol V1.0.0. www.aisp.dev
