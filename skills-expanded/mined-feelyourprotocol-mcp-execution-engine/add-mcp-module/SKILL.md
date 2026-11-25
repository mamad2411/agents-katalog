---
name: add-mcp-module
description: >-
  Add an MCP twin for a protocol change: engine capability module (when a
  shipped verb can honestly run it) and human catalogue page. Use for
  round-trip phase 3, or after website canonical.ts exists.
---

# Add an MCP module

Executable playbook for **`mcp-execution-engine`** + human page in **`website/mcp-docs/use/eips/`**. Phase 3 of the website [round-trip](https://github.com/feelyourprotocol/website/blob/main/.cursor/skills/round-trip-protocol-change/SKILL.md).

**Read first:** website `src/explorations/eip-NNNN/canonical.ts` — twin source of truth ([eip-canonical-data.mdc](https://github.com/feelyourprotocol/website/blob/main/.cursor/rules/eip-canonical-data.mdc)). On twin-metadata conflict, website `CANONICAL` wins. Fold in briefing prompts and **carry to MCP** hints from the exploration report. MCP findings go back into `canonical.ts` first, then replicas.

Concepts: [eip-canonical-data.mdc](https://github.com/feelyourprotocol/website/blob/main/.cursor/rules/eip-canonical-data.mdc), [website-relation.mdc](../rules/website-relation.mdc), [structure.mdc](../rules/structure.mdc), [design-principles](https://github.com/feelyourprotocol/website/blob/main/mcp-docs/internals/design-principles.md).

## What users want (intents)

MCP is the **lab**, not a second widget. Same **core question** as the exploration; the caller brings **their** bytecode / inputs. These intents must hold for any EIP nature — do not cargo-cult EIP-8024.

1. **Ask in their words** — play, understand, or check *their* data. Catalogue prompts come from the briefing (“what they would ask”), not from widget preset hex.
2. **Generic verbs only** — `describe_capabilities` + `run_bytecode` + `run_transaction` + `run_block` + `generate_artifact` + `inspect_artifact`. Never `run_eip_NNNN`.
3. **BYOS / constructible** — catalog exposes encoding facts (opcodes, precompile ABI, immediates) so an agent can *build* a request, including prestate (accounts, code, storage). No demo programs in the module.
4. **Honest observation** — a module is `runnable` only if a **shipped** verb can show the EIP’s effect in the result the engine actually returns today. Bytecode (`SimulateBytecodeResult`): success, call-frame `gasUsed`, stack, optional trace/logs (and optional `stateGasSpilled` on Glamsterdam). Transaction (`RunTransactionResult`): paid `gasUsed`, optional `txRegularGas` / `txStateGas`, receipt logs. Block (`RunBlockResult`): per-tx receipts + header snapshot (`slotNumber`, `number`, `timestamp`). If the core question needs BAL JSON we do not return yet → **`planned-module`**. Wallet gasLimit and paid-tx questions use **`run_transaction`**, not `run_bytecode`. Opcode / program-gas questions (including SSTORE write cost) use **`run_bytecode`**. Multi-tx / header-slot questions use **`run_block`**.
5. **Superset, not clone** — exploration is a curated slice; MCP runs arbitrary caller programs under a fork. Do not replay widget examples in the catalog or as the only tests.
6. **Compare when it teaches** — repricing / on-vs-off capability: `comparison` forks and “run twice.” New-capability with no meaningful baseline: valid vs invalid (see 7951), not a fake gas delta.
7. **Twin page always** — every **live** exploration gets `use/eips/eip-NNNN.md` (Runnable or Planned). Engine module only when (4) holds. Do **not** drop the module or page when `introducedAt` becomes `current` or later `historical`. `sunset` is for no honest verb (or a later explicit cleanup).

## Pattern (do not assume opcodes)

Match `CANONICAL.question.changeNature` + `mcp.shapes`. Closest **engine** siblings:

| Job | Reference module | Catalog exposes | Tests prove |
| --- | --- | --- | --- |
| New opcodes | `src/modules/eip-8024/` | opcode + immediate encoding | valid exec + invalid encoding / depth |
| Precompile repricing | `eip-7883/` | CALL address + input layout + comparison forks | gas predecessor vs introducedAt; bound rejection |
| Precompile new-capability | `eip-7951/` | CALL address + input layout | valid return vs invalid — not a fork gas compare |
| New structure (BAL, …) | **generate_artifact** + optional **inspect_artifact** | runnable module (see `eip-7928.md`) | MCP curriculum tests |
| Header slot / multi-tx receipts | `run_block` | header snapshot + per-tx receipts | slot / N txs / Fusaka vs Glamsterdam |
| Limit / economic / exec-model | `run_transaction` if the unit is a tx (gasLimit, receipt, `txStateGas`); `run_bytecode` if opcodes / program gas | encoding + fork notes | hit the limit / fee path; beyond-edge |
| Needs BAL JSON | **planned-module** until **generate_artifact** can return it | page says what is observable today | do not list in `EIP_MODULES` until honest |

Copy the closest **module**, not the closest **website folder**. Helpers: `opcodes.ts` or `input.ts` — facts, not programs.

## Before coding

1. Read website `CANONICAL` + exploration **carry to MCP** + briefing prompts.
2. **Honest verb check** (intent 4). Then branch on `docsStatus`:
   - **`runnable`** — shipped verb can show the effect → engine module + page.
   - **`planned-module`** — page + coverage (+ matching fork page) only; **no** `runnable: false` row in `EIP_MODULES`.
3. Human MCP page must exist or ship now. Flesh out a phase-2 stub.

## Exception gates

Stop and ask:

- Effect is not in today’s simulate result (logs, receipts, BAL, …) — do not stretch traces into a fake answer
- Would require a **new MCP tool** or a new query-shape export (a small additive field on an existing result is not this)
- New **runtime** dependency
- Briefing/`CANONICAL` said planned but EthereumJS can already run it (or the reverse)
- Process-global EVM / session snapshot memory (layer 3) — still later, not a side-trip

## Side-trips (structural, same phase)

Phase 3 may include a **well-scoped structural expansion or re-arrangement** discovered while wiring the twin — for example the shipped verb cannot honestly show the EIP because of a lab-path gap (`runCode` vs a VM message-call), not because the EIP itself needs a fifth tool.

**In scope when all of these hold:**

- Same generic verbs (no `run_eip_NNNN`, no new tool)
- Honest observation improves on a **shipped** result (or a small additive field on that result)
- No new runtime dependency
- Can finish tests + docs in this phase

**Do it now** (do not wait for another GO). Apply the change **once**, then update every MCP surface that taught the old limitation:

1. Engine verb + types + lab helpers
2. Gateway Zod/JSON schemas and tool descriptions if input, output, or routing changed
3. mcp-docs tool pages, `llms.txt` / `llms-full.txt`, internals, and **every** live EIP catalogue page / engine module note that mentioned the old path
4. Tests: the expansion itself **and** regressions on other EIPs that use the adjusted verb (gas, success, stack — no silent deltas)
5. Close with the **Side-trip** section in the phase-3 report (required when this path ran)

Do **not** use a side-trip to start the comic, add session memory, or skip the round-trip STOP after the MCP report.

## Module steps (`runnable`)

1. `src/modules/eip-NNNN/index.ts` — descriptor only.
2. Optional helpers for **constructible** encoding.
3. Comment: `canonicalSource: 'website/src/explorations/eip-NNNN/canonical.ts'`.
4. Copy from `CANONICAL`: `coreQuestion` → `summary` (capability voice), `changeNature`, `identity.status` / `specUrl` / `specDate` / `testReleaseUrl` / `testReleaseName`, keywords, comparison. Do not re-resolve pins from a local `ethereum/EIPs` checkout.
5. Runtime fields: `runnable: true`, internal `shapes` (query-shape ids; probe serializes them to `tools` MCP names), opcodes or input encoding.
6. Register in `src/modules/index.ts`.
7. Tests in `src/__tests__/` — CALL/exec fixtures you construct; **not** website widget bytecode. Happy path **and** beyond-edge (junk encoding, out of range, “too big”).
8. Catalogue page + `use/coverage.md` + the matching `use/forks/<id>.md` twins list + `llms.txt` if the index changed. Do **not** add the EIP to the VitePress sidebar.

## Catalogue page (every live twin)

Follow existing pages (`eip-8024.md`, `eip-7883.md`, `eip-7951.md`, planned `eip-7928.md`):

1. Status banner (ready for public MCP vs planned; public MCP not launched — do not advertise self-host)
2. **What became possible** — core question; what the caller supplies
3. **What you can ask** — 3–5 prompts from the briefing (play + understand + their data). No tool names in the prompt list
4. **What the server does** — discover, then the verb (plain labels)
5. **Fork caveat** — or “no before/after; look at valid vs invalid”
6. Twins + spec + coverage
7. Changelog entry on the page

## Invariants

- Do **not** add per-EIP MCP tools — generic verbs only.
- Do **not** import from `website/src/explorations/`.
- Do **not** list `runnable: false` modules in `EIP_MODULES`.
- Demo bytecode belongs in `src/__tests__/fixtures/`, not module descriptors.

## Finish gates

```bash
cd mcp-execution-engine && npm run typecheck && npm run test:ci && npm run lf:ci
```

Rebuild gateway if tool descriptions changed; restart MCP in Cursor.

## Smoke-test prompts (always in the report)

The human will paste these into a **fresh** agent chat with Feel Your Protocol MCP connected. They are **not** catalogue inspiration prompts — they are a short, ordered check that the twin actually runs.

**How many:** 1–3, scaled to complexity.

| Count | When |
| --- | --- |
| **1** | Thin twin (one observation, one fork or a simple valid/invalid) |
| **2** | Typical runnable module (discover + the teaching compare or happy/fail pair) |
| **3** | Richer EIP (extra path: bound rejection, funded vs empty, new slot, invalid encoding, …) |

**Rules:**

- Plain language a human can paste. No “call tool X with JSON …”.
- First prompt should force **discover** (`describe_capabilities` / catalog row) when the module is `runnable`.
- Later prompts should force the **verb** and the **observation** the report claimed (`gasUsed`, logs, return value, …).
- Include **expected tell** (what “pass” looks like) next to each prompt — for the human, not for the agent under test to be spoon-fed if they only paste the quoted prompt.
- For `planned-module`, 1 prompt is enough (catalog/docs honesty: Planned, not a fake run).
- Do **not** paste widget demo hex. Addresses/values may be generic (`1 wei`, empty account, Fusaka vs Glamsterdam).
- **MCP-only prefix** (same line on every prompt, or once above the list): the tester’s workspace often already contains this repo, so the model will otherwise read our source instead of the server. Prefix:

  > Answer using only the installed Feel Your Protocol MCP server. Do not use workspace files, git history, or other background knowledge.

## Report template — then round-trip is complete

```markdown
## Phase 3 — MCP (eip-NNNN)

**Intent:** same core question; caller-supplied; observation = …
**docsStatus:** runnable | planned-module
**Shapes:** …
**Honest verb:** shipped result fields that show the effect — or why planned
**Engine module:** path or none
**Catalogue page:** `website/mcp-docs/use/eips/eip-NNNN.md`
**Also updated:** coverage / fork page / llms — yes/no

**Canonical:** copied from website `CANONICAL`; conflicts (none | resolved toward website)
**Tests:** `npm run test:ci` — N specs (happy + beyond-edge), pass/fail
**Quality:** typecheck, `lf:ci`

**Twin:** exploration slice vs MCP superset (one line)
**Prompts sourced from:** briefing / carry-to-MCP
**What we did not clone:** widget demo bytecode, …

**Smoke-test prompts** (paste into a fresh MCP-connected chat; 1–3). Prefix every paste with the MCP-only line from the skill.

1. *“…“* — expected: …
2. *“…“* — expected: …

### Side-trip (omit if none)

**What:** …
**Why in this phase:** well-scoped / same verbs / honest observation — …
**Applied to:** engine / gateway / mcp-docs / EIP modules …
**Tests:** change + no side-effects (which specs)
**Docs:** …
```
