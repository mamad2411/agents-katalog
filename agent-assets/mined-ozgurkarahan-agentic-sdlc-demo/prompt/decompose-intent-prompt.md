---
mode: agent
description: Decompose one intent into a Work Plan — Issues with acceptance criteria + DoD + test/eval strategy, plus a dependency graph. EXAMPLE prompt file.
---

# Decompose intent → Work Plan (EXAMPLE — copy to `.github/prompts/decompose-intent.prompt.md`)

You are decomposing a single intent into a **fleet-ready Work Plan**. Follow this exactly.

## Input
- **Intent:** `${input:intent}` *(one sentence of what to build)*
- Repo context: this repo's `AGENTS.md`.

## Produce
1. **Units.** Break the intent into the smallest **independent** units. Each unit = one Issue.
2. **Per unit**, write:
   - **Acceptance criteria** (objective, testable).
   - **Definition of Done** (explicit).
   - **Test + eval strategy** (which tests prove correctness; which evals prove quality/trajectory).
3. **A dedicated end-to-end "real-results" acceptance unit** (always present; **ordered**, depends on the
   implementation units). Its acceptance is measured against the **live deployed URL** — the running
   system, not a stub or mock — and it is wired as a **post-deploy gate**. Spell out the observable
   contract in its DoD (for a rate-limit intent: *under the threshold → live API returns **200**; past
   the threshold → **429** with a numeric `Retry-After` and `RateLimit-*` headers*). You **specify** it;
   the Development agent **writes the test**.
4. **Dependency graph.** For every pair of units, decide **parallel-safe** or **ordered**, and list
   each dependency edge. When unsure, mark **ordered** (safer). The E2E unit is **never** parallel-safe.
5. **Concurrency.** Note the recommended fleet concurrency cap (set per your fleet's capacity).

## Output format
- A tracking issue body + one `work-unit` issue body per unit (see `ISSUE_TEMPLATE/work-unit.yml`).
- A short dependency-graph table: `unit | parallel-safe? | depends on`.
- An embedded machine-readable plan block the issue-native plan-lint can parse, e.g.:
  ` ```json agentic-plan ` … `{ "intent": "...", "units": [ { "id": "U1", "paths": [...], "parallelSafe": true, "dependsOn": [] }, ... ] }` … ` ``` `

## Hard rules
- Do **not** propose implementation steps or write code — this is planning only.
- Do **not** assert a parallel-safe edge you cannot justify against shared state/schema/files.
- Do **not** emit a plan without a **real-results E2E unit** that asserts against the live deployed URL;
  a suite that only checks local stubs/mocks is **insufficient** and must be rejected.
- Hand the result to the **rubber-duck** validation prompt before anything is built.
