---
name: port-external-api
description: Port a TagMango endpoint from apps/api or apps/core-api to the external API surface, driven by a linked GitHub issue. Grills the public contract, preserves legacy behavior, and lands the capability-complete use case in libs/services with data access in libs/repository so core-api can later replace the legacy route. Produces an implementation handoff; never writes tests. For review-only requests use audit-external-api-port.
argument-hint: <github-issue-url>
disable-model-invocation: true
---

# Port External API

Port behavior, not legacy representation: preserve the complete business decision path while designing a deliberate public contract that an unfamiliar integrator can use safely.

## The same-outcome rule

**Given the same request, actor, and stored state, the ported path must produce the same persisted state, same response semantics, same side effects in the same order, and same error surface as the pinned legacy source.** Code structure may change; outcomes may not.

Allowed without a decision: renaming, decomposition, typed models, provably-dead code removal, and optimizations with identical results — including rounding, ordering, projection, and null handling.

Forbidden without a recorded `D-###`: changing defaults, reordering side effects, tightening or loosening validation, changing rounding/precision/timezone handling, altering query filters or sorts, removing "useless-looking" writes, and fixing apparent legacy bugs. A suspected bug is preserved and escalated as a decision — never silently fixed, never silently kept.

An optimization ships only with an equivalence note in the packet arguing outcome-equality against each affected `B-###`, flagged for the testing workflow to verify. **When the source and your intuition disagree, the source wins.**

## The shared-capability rule

Every port lands one transport-neutral use case in `libs/services/src/lib/<domain>/` with typed data access in `libs/repository/src/repositories/<domain>/`. The external controller and every equivalent current core controller are thin adapters over that use case: each parses its own DTOs, authenticates, calls the shared use case, and maps the domain result to its own response contract.

The use case stays complete for the whole scoped legacy capability even when the external contract deliberately exposes a subset. The test for "complete": a future core controller could replace the legacy route by adding only authentication, DTOs, mapping, and wiring — never another business rule, repository query, state transition, or side-effect path. Never branch on `external` versus `core` inside domain code; express real permission or capability differences as domain context and injected policies. "Generic" means exactly this rule — not speculative TypeScript generics, a catch-all service, or configuration for imagined consumers.

## The reuse rule

Reusability flows both ways through every port.

**Consume:** a new wrapper, adapter, parser, pipe, interface, or factory is presumed unnecessary until repository inspection proves no existing primitive covers the concern — that proof is the `P-###` row. Existing DTO transformers, canonical representations, error registries, DI modules, clients, cache services, and derivable types come first.

**Produce:** everything this port creates — the use case, repository methods, representation tiers, named policies, error definitions — is a canonical primitive placed where the next port's `P-###` inspection will find it: shared modules and registries, never endpoint-local. The test: the next port touching this domain adopts your primitives unchanged. An endpoint-local helper the next port would have to duplicate is a defect, not a convenience.

Reusable means one canonical owner, not speculative generality — configuration for imagined consumers is still an invented abstraction.

## Outcomes

1. **Behavioral fidelity** — confirmed defaults, eligibility rules, validation, state transitions, persistence, side effects and their order, error cases, transaction boundaries, and absent/null/false/zero/empty semantics match the pinned sources.
2. **Deliberate public contract** — URL, method, auth, parameters, bodies, responses, errors, and examples are designed for external consumers. Never expose an internal DTO or database document because it already exists.
3. **The shared-capability rule**, satisfied and evidenced in the packet's `M-###` mapping.

Promote a frontend-only restriction into backend enforcement only when evidence shows it is a business rule. Record a decision before promoting anything ambiguous; never promote UI convenience.

## Stopping points

- No readable GitHub issue → request it and keep the packet `BLOCKED`. Every port requires one.
- Research or design request → stop after the grill and the designed `M-###` mapping, before any product-code edit.
- Full port → pause for the developer's contract confirmation; implement only when the packet is `READY` and no material decision is open.
- Implementing an already-approved packet → first re-verify its source pins and assumptions are still current.
- Retrofit (completing a packet that predates the current gates while the code is already committed) → set the packet to `IMPLEMENTING`, fill every missing section from committed-code and source evidence exactly as if porting fresh — pattern rows, migration mapping, and traceability must be true, not synthesized to pass — and set `IMPLEMENTED` only when both gate checks are green. A gate that cannot honestly pass is a finding to fix or a `D-###`, never a row to fudge.
- Review-only request → wrong skill; use `audit-external-api-port`.
- Never create, modify, or run tests. Existing tests are read-only source evidence; certification belongs to a separate testing workflow.

## Batches

For several endpoints, keep one inventory (issue, operation, source route, shared dependencies, readiness, packet path, status) and one packet per operation, grouped by domain capability rather than legacy controller file. Research shared auth/tenant/error/pagination policy once per source pin and cite it from each packet. Extract shared domain code before wiring endpoints, and finish an operation's design gate before implementing it. Parallel read-only research is fine; never let parallel agents implement competing versions of one domain rule, and never template an unaudited first port across the batch.

## Workflow

### 1. Ingest the issue and pin authority

Read repository instructions, coding standards, architecture maps, and the working-tree diff before searching broadly; preserve unrelated changes. Then read [issue-contract-grill.md](references/issue-contract-grill.md) and capture the live issue as `I-###` entries — it is scope and product intent, not proof of runtime behavior.

Pin in the packet: the operation and consumer use case; target branch and external surface; every source repository at an exact commit; whether `apps/api`, `apps/core-api`, or both hold authoritative behavior; the user-designated `tagmango-web-platform` checkout; and the nearest current, intentional external-endpoint conventions. When several checkouts or branches exist, run `git log -1` and `git status` in each and choose by content; ask only if two checkouts implement different product decisions.

### 2. Create the packet

```sh
python3 <skill-directory>/scripts/port_packet.py init \
  --operation <operation-slug> --source <legacy|core-api|both> \
  --issue <github-issue-url> \
  --output .scratch/external-api-ports/<operation-slug>/port-packet.md
```

Use the repository's established scratch/spec location instead of `.scratch/` when one exists; keep the packet uncommitted unless the user requests publication. Update it while you work — never reconstruct it at the end from memory.

### 3. Reconstruct the complete behavior

Read [behavior-parity.md](references/behavior-parity.md) and trace every backend layer and frontend flow listed in its §2 — route registration through side effects, form initialization through payload assembly — plus the downstream consumer of every caller-controlled URL, file reference, callback, redirect, or provider identifier.

Record each externally meaningful rule as a `B-###` row with a `repository@commit:path:line` anchor, and classify each frontend observation with the table in behavior-parity.md §4. Write scenarios with executable concrete values — real field names, sample payloads, expected persisted fields and responses — so the testing workflow can turn rows into characterization tests verbatim. Work breadth-first (map all layers and fields once), then risk-first (deepen public fields, cross-field rules, permissions, persistence, side effects). Research converges when every public input/output and material capability behavior has pinned evidence or a `D-###` decision; do not expand into unrelated domain behavior.

### 4. Draft the contract from the consumer inward

Read [public-contract-design.md](references/public-contract-design.md). Design the wire contract before implementation shapes: complete versioned URL, method, auth and tenant context, idempotency, every field's semantics, errors, pagination, and compatibility. The packet's `C-###`, `E-###`, and `X-###` tables define exactly what to record per parameter, field, error, and exposure decision.

Before shaping the response, inventory existing canonical representations for every resource concept it returns or embeds; reuse the matching tier or record a `D-###` for a new one. An embedded resource composes the owning concept's summary representation — never an inline field selection (public-contract-design.md §6).

Add an `S-###` threat entry for each caller-controlled value that reaches a fetcher, queue, file/media processor, redirect, provider, bulk query, or cross-tenant lookup; record the implemented controls plus the risk the testing workflow must verify.

Write the three consumer examples — minimal valid request, one important optional combination, one invalid combination with its exact error — before coding. If they need internal knowledge to interpret, redesign the contract.

### 5. Grill the contract (G-001–G-008)

Follow the frontier discipline in [issue-contract-grill.md](references/issue-contract-grill.md). When the host can compose installed skills, load `grill-with-docs` for this bounded phase — invoking this skill is consent to be grilled; the reference is the self-contained fallback. Resolve or justify `N/A` for all eight `G-###` dimensions, and surface contradictions with settled issue decisions instead of silently overriding them.

Before each question round, write the evidence, options, and recommendations into the packet rows and set status `BLOCKED`. Never present recommendations from private notes while the packet is an untouched template. Do not implement after merely proposing a reasonable contract — wait until the developer confirms the frontier is empty.

### 6. Resolve remaining behavioral decisions

Investigate discoverable facts yourself; ask only when two plausible answers materially change business behavior, security, data exposure, or scope. Do not label a missing fact as a product decision.

```text
Q<D-###> — <decision>
Evidence: <what each source does, with anchors>
Why unresolved: <the contradiction or missing product rule>
Recommended: <one option and rationale>
Impact: <wire or behavior consequence of each option>
```

Batch only independent questions, record answers in the packet, and stay `BLOCKED` while any material `G-###` or `D-###` is open.

### 7. Implement one shared semantic model

Read [tagmango-implementation.md](references/tagmango-implementation.md) first and follow it for repository surfaces, the external framework seams, the shared implementation boundary, validation layers, kebab-case file naming, and module/documentation wiring. Gate decisions this workflow owns:

- Before writing code, resolve the packet's Repository Pattern Conformity table (`P-001`–`P-010`): for each concern, pin a recent *intentional* external port as the exemplar — not merely nearby files, which may carry legacy debt — name the existing primitive or owning module, and decide `ADOPTED` or a `DEVIATION (D-###)`. Both halves of the reuse rule apply here: prove reuse first, and place what you create where the next port will find it.
- Reuse an existing canonical domain service when it already owns the behavior; otherwise characterize app-local behavior first, then extract the complete scoped decision model into `libs/services` and `libs/repository`. Never call or copy a legacy controller, and never add app-local business or repository code.
- When one legacy handler bundles several capabilities, split them deliberately and port the scoped one completely.
- When an equivalent core API exists, rewire its controller to the shared use case in this same port, preserving both observable contracts through separate adapters and mappers. If safe rewiring is materially blocked, stop and record a `D-###` instead of duplicating logic.
- When none exists, the `M-###` mapping must show a future core route needs transport-only work; otherwise keep core-migration readiness `BLOCKED` and do not call the port complete.
- Keep external exposure in an explicit allowlisted mapper/DTO. Never narrow the domain model to the external subset, and never spread a document or internal DTO into a response.
- Preserve side-effect order, retry safety, atomicity, and legacy failure semantics unless the packet records an approved change; hold every touched file to current repository standards.
- **No unmapped code:** every branch, default, and mutation in new domain code traces back to a `B-###`, `V-###`, or `D-###`. Logic with no rule is invented behavior — delete it or record it.
- Readability bar: an engineer who has never opened the legacy controller must understand the shared use case from its code alone; the legacy file is not documentation. Where a preserved quirk looks wrong on purpose, one comment states the business reason.
- Implement in narrow slices: one behavior cluster at a time, checks passing between slices. Do not stage, commit, push, or publish unless the user explicitly asks.

### 8. Traceability and checks — no tests

Map every `B/V/G/P/M/S-###` rule to an `H-###` row: the implemented files and symbols, how the rule is represented, what remains runtime-unverified, and the evidence the later testing workflow needs. Then reverse the mapping: scan the new domain code for branches, defaults, and mutations with no ledger rule, and record or remove each before handoff.

Run the non-test checks from tagmango-implementation.md §7 (format, lint, typecheck, build, generated OpenAPI inspection, final diff review); skip and record any command that would run tests. Inspect every added and scoped untracked filename, then record `New-file naming audit` as `PASS` with any justified exceptions.

Set the packet to `IMPLEMENTED`, never `VERIFIED` — traceability shows where the intended behavior was placed, not that it executes correctly.

### 9. Validate the gates

```sh
python3 <skill-directory>/scripts/port_packet.py check <packet-path> --stage design
python3 <skill-directory>/scripts/port_packet.py check <packet-path> --stage implementation
```

Stop at `IMPLEMENTED`. Preserve the packet, pins, ledgers, examples, and unresolved runtime risks for `test-external-api-port` (runtime verification and the only workflow allowed to set `VERIFIED`) or `audit-external-api-port`; do not invoke either automatically.

## Handoff

Report: the endpoint and consumer goal; issue URL with resolved grill decisions; source pins; packet path and status; public-contract summary; preserved behavior and newly backend-enforced frontend rules; files changed; shared service/repository paths and every consumer rewired to them; `M-###` coverage and the exact work a future core adapter still needs; the drift watchlist — every legacy route that keeps a live duplicated implementation of this capability until core replacement, each entry directly callable as `<apps/api | core-api> METHOD /full/path`; equivalence notes for any optimization; check outcomes; deferred-testing risks; and open decisions or deviations.

Separate confirmed parity from inference. Never describe a partial port as complete.
