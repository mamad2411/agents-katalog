---
name: dev-ultraqa
description: QA cycling workflow — repeat build/lint/test/fix cycles up to 5 times until all checks pass. Stops early if the same error repeats 3 times (signals a fundamental issue, not a fixable one).
---

# Dev UltraQA

Derived from oh-my-claudecode (MIT, Yeachan Heo). Adapted for the EvoNexus Engineering Layer.

QA cycling: keep running build/lint/test/fix loops until all checks pass — but with a circuit breaker. If the same error persists across 3 cycles, stop and report: it's a fundamental issue, not a fixable one.

## Use When
- After a multi-file implementation (post-`dev-autopilot` or `@bolt-executor`)
- Pre-merge gate when you want all checks green before review
- Refactor that touches enough files to risk regressions

## Do Not Use When
- Single-file change → just run `dev-verify` once
- The first failure is structural → escalate to `@apex-architect`, don't loop

## Workflow

### Each cycle:
1. Run **build** (`npm run build`, `cargo build`, `go build`)
2. Run **lint** (`npm run lint`, `cargo clippy`, `golangci-lint`)
3. Run **tests** (`npm test`, `cargo test`, `pytest`)
4. **If green:** done, exit cycle, hand off to `@oath-verifier` for final verification
5. **If red:** delegate to `@bolt-executor` or `@hawk-debugger` to fix the failure
6. **Loop** back to step 1

### Circuit breaker (3-failure rule)
If the same error fingerprint (file:line + error message) appears in 3 consecutive cycles:
- STOP the loop
- Hand off to `@apex-architect` with full context dump
- The issue is no longer "fix the bug" — it's "question the architecture"

### Max iterations
- Default: 5 cycles
- After 5 cycles even with different errors: stop and report

## Output
Saved to `workspace/development/verifications/[C]ultraqa-{component}-{date}.md`:

```markdown
## UltraQA Report

### Cycles
1. Build ❌ → fixed by @bolt-executor
2. Build ✅ Lint ❌ → fixed by @bolt-executor
3. Build ✅ Lint ✅ Tests ❌ → fixed by @hawk-debugger
4. ✅ All green

### Final State
- Build: ✅
- Lint: ✅
- Tests: ✅ N passed, 0 failed

### Handoff
- → @oath-verifier for evidence-based verification
```

## Pairs With
- `@bolt-executor` (fixes during cycles)
- `@hawk-debugger` (fixes when bugs are non-trivial)
- `@oath-verifier` (final verification post-cycle)
- `@apex-architect` (escalation when 3-failure breaker trips)
