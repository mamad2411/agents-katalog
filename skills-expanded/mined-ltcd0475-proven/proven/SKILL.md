---
name: proven
description: |
  AST context extraction, call-graph analysis, and mutation testing CLI for coding agents. Use when asked to write tests for changed code, PRs, or specific functions, find untested changes, or verify test suites against AST mutations.
version: 1.0.0
author: LTCD
license: MIT OR Apache-2.0
tags:
  - testing
  - mutation-testing
  - ast
  - call-graph
  - code-coverage
---

# Proven — Coding Agent Skill

**Proven (`proven`)** pairs a coding agent with external specification discovery, scoped AST/call-graph context extraction, sibling guard omission checks, and on-the-fly AST mutation testing:

- **You (the Agent)** derive behavioral expectations from external specs before inspecting implementation code, then expand tests for integration slices, concurrency barriers, and surviving AST mutants.
- **Proven (`proven`)** handles four deterministic tasks:
  1. **Change & Config Audit (`proven scan` / `scan_impact.py`)**: Finds untested changed functions, emits `blind_context_cmd` fan-out tasks, and compares environment variable reads in changed code against `.env.example` / `.env.sample` / `.env.template` (`config_audit`, without reading secret `.env` files).
  2. **Blind Spec & Scoped Context (`proven context [--blind] [--spec]` / `get_target_context.py`)**:
     - `--blind` mode hides `source_code` and returns only `signature`, `docstring`, `callers`, `discovered_specs` (docstrings across all 9 languages, `README*`/`SPEC*`/`docs/**`/`openapi.*`, `git log`, caller usage, `--spec`), `inferred_invariants` (signature domain probes), and `missing_sibling_guards` (guards enforced by sibling functions in the module).
     - Full mode adds `source_code`, 1-hop `callees`, 3-hop Personalized PageRank call-graph neighbors (`< 120 tokens`), `unverified_literals` (hardcoded numeric constants not backed by external specs or named module constants), `integration_slice` (`sql_query`, `json_serde`, internal callees, entry callers), and `concurrency_risk` (`async_fn`, `mutex_or_atomic`, `concurrent_workers`, `shared_state_mutation`).
  3. **AST Mutation & Transitive Slice Gate (`proven verify-proof --mutation-check` / `verify_runtime_proof.py`)**: Verifies direct or 1–3 hop transitive slice tests against boundary, logical, membership, state/boolean, bitwise, and arithmetic AST mutations across the full function body with automatic RAII file restoration (`FileRestoreGuard`) and Go multi-core/`-race` scheduling.
  4. **Failure Memory (`proven sleep` / `consolidate_memory.py`)**: Records survived-mutant diagnoses and consolidates recurring patterns into reusable `.proven/meta_axioms.json` rules.

> **Invocation Note**: Run the wrapper scripts inside this skill's `scripts/` folder (e.g. `python <skill_dir>/scripts/scan_impact.py ...`), or call `proven` directly if it is on `PATH`. On first run after `npx skills add minhquang0407/proven`, the wrapper automatically downloads or builds the `proven` binary into `<skill_dir>/bin/`.

---

## Reference Index

| Situation | Reference | Purpose |
| :--- | :--- | :--- |
| CLI flags & JSON output schemas | [`references/scripts_api_reference.md`](references/scripts_api_reference.md) | Schemas for `proven` subcommands and wrapper scripts. |
| Multi-round mutation feedback | [`references/tri_agent_arena.md`](references/tri_agent_arena.md) | Iterative mutation verification (`proven arena`, max 3 rounds). |
| Test failed execution or mutation check | [`references/proof_gate_guide.md`](references/proof_gate_guide.md) | Diagnosis codes (`WEAK_ASSERTION`, `UNCHECKED_SIDE_EFFECT`, `MISSING_EXCEPTION_CONTRACT`). |
| Impact analysis or reviewer lookup | [`references/tier2_guide.md`](references/tier2_guide.md) | Call-graph PageRank impact estimation and `git log` triage. |
| Polyglot projects (Rust, Go, JS, TS, C, C++, Java, C#) | [`references/universal_lcov_guide.md`](references/universal_lcov_guide.md) | 9-language AST extraction and custom test runner configuration. |
| Installing across agent tools | [`references/agent_integration.md`](references/agent_integration.md) | Setup via `npx skills add minhquang0407/proven` or local installer. |

---

## Two-Phase Verification Workflow

### Stage 1: SCAN — Find Untested Changes & Config Drift
```bash
python <skill_dir>/scripts/scan_impact.py --path . --fan-out --json
# Or directly if `proven` is on PATH: proven scan --path . --fan-out --json
```
- Check `config_audit.missing_env_example_keys` and report undocumented environment variable keys read by changed files.

### Stage 2: PHASE A (BLIND SPEC-FIRST) — Extract Specs Without Reading Implementation
```bash
python <skill_dir>/scripts/get_target_context.py --target "FUNC:<target_name>" --file "<optional_rel_file>" --blind [--spec "<user_prompt_or_doc_path>"] --path . --json
```
- **Do not read the production implementation yet.** Write Turn-1 behavioral tests strictly from:
  1. `discovered_specs` (external requirements, docstrings, repo docs, commit messages, and caller usage).
  2. `missing_sibling_guards` (probe security, state, permission, or null guards enforced by sibling functions in the same module).
  3. `inferred_invariants` (probe `0`, `-1`, empty collections/strings, `None`/`null`/`nil`, and restricted entity states).
- If a Turn-1 spec/omission test fails against the current code, treat that failure as a candidate production bug or missing guard: **do not rewrite the test to match broken implementation output**.

### Stage 3: PHASE B (FULL IMPLEMENTATION, SLICE & CONCURRENCY) — Inspect Full Context
```bash
python <skill_dir>/scripts/get_target_context.py --target "FUNC:<target_name>" --file "<optional_rel_file>" --path . --json
```
1. **Integration Slice (`integration_slice != null`)**: Avoid mocking internal project callees (`internal_callees`), SQL queries, or JSON serialization boundaries (`io_boundaries_detected`). Write at least one real slice test using an in-memory database (e.g. `sqlite3.connect(":memory:")`), temporary directory, or real project caller (`entry_callers`, verified up to 3 call-graph hops by `verify-proof`).
2. **Concurrency Barrier (`concurrency_risk != null`)**: Inspect `concurrency_risk.signals` and `recommended_harness`, and add a multi-worker barrier test (`threading.Barrier`, `asyncio.gather`, `Promise.all`, Go goroutines + `sync.WaitGroup` with `--pytest-args "-race"`, Rust threads, etc.) asserting exact post-concurrency invariants (no negative balances, lost updates, or race conditions).
3. **Unverified Business Literals (`unverified_literals`)**: Do not blindly hardcode magic numbers from `source_code` as oracle truth when they appear in `unverified_literals`; surface each item under `[ORACLE_REVIEW]` in your final summary so the user can confirm the business rule.
4. **Config Drift (`config_audit != null`)**: Surface any `config_audit.missing_env_example_keys` read by the target file in your final summary.
5. **Do not modify production source files**: Only create or edit test files unless the user explicitly asks you to fix production bugs as well.

### Stage 4: RUNTIME & AST MUTATION GATE
```bash
python <skill_dir>/scripts/verify_runtime_proof.py \
  --target "FUNC:<target_name>" \
  --test "tests/test_<module>.py" \
  --mutation-check \
  --path . \
  --json
```
- **`proof_grade: "TITANIUM"`** (`mutants_survived == 0`): All tested mutants were killed. Proceed to Stage 6.
- **`proof_grade: "SILVER"`** (`mutants_survived > 0`): Inspect `mutation_proof.details` and `mutation_proof.causal_reflexion`, add assertions covering the surviving mutant, and re-run.

### Stage 5: REPAIR & DEFECT REPORTING
- Add assertions in the test file targeting the exact line and operator reported in `mutation_proof.details`, or run an arena round:
  ```bash
  python <skill_dir>/scripts/run_arena.py --target "FUNC:<target_name>" --test "tests/test_<module>.py" --round 1 --path . --json
  ```
- **Real Bugs, Missing Guards & Equivalent Mutants**: If a test fails due to an actual defect or omitted guard in the production source code—or if a surviving mutant stems from dead/equivalent code—keep the production file unchanged and report the exact file, line, and diagnosis (along with any `[ORACLE_REVIEW]` literals and `config_audit` warnings) to the user.

### Stage 6: CONSOLIDATE — Persist Failure Rules
```bash
python <skill_dir>/scripts/consolidate_memory.py --force --meta --path . --json
```
