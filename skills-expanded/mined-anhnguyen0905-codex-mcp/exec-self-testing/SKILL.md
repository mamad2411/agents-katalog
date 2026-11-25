---
name: exec-self-testing
description: Self-testing requirements to embed into Codex execution prompts — test-first workflow, what to test, and the never-finish-red rule.
---

# Self-Testing (embed into Codex prompts)

A senior developer proves their own work. Include this block in every `codex_execute` prompt:

```
Testing requirements (mandatory):
- Every new behavior gets a test in the same task: happy path + at least one failure/edge case
  (empty input, boundary value, error propagation).
- Write the test alongside or before the implementation; use the project's existing test
  framework, file layout, and naming style.
- Tests assert behavior (inputs → outputs, state changes), not implementation details.
- Use Arrange-Act-Assert structure with descriptive names ("returns empty list when no match").
- Targeted tests only: run the test file or pattern for the current task using the project's
  targeted command (for example, `npx vitest run tests/<file>.test.ts`), plus the build/typecheck
  once before finishing. Do NOT run the full test suite — the orchestrator's `verifyCommand` is the
  single authoritative acceptance run for this task, and the full suite runs once per merged
  parallel wave and once in the whole-feature review.
- While iterating: re-run only that targeted command; never run the full suite mid-task.
- Environment failure: if a test command fails with a sandbox or environment error (EMFILE, EPERM,
  out-of-memory, or file-watcher limits), STOP and report the verbatim error in the final summary;
  do NOT re-run the full suite hoping it passes.
- Long test commands: name every test command expected to take more than two minutes in the final
  summary and explain why it was needed.
- NEVER finish with failing tests or a broken build. If a pre-existing test fails for reasons
  outside this task, stop and report it instead of "fixing" the test to pass.
- Fix the implementation, not the test — unless the test itself is provably wrong, and say so.
```

## Claude's verification duty

Trust but verify: pass the task's acceptance command as `verifyCommand` so the server runs it after
the Codex run settles and returns `verification` (`exitCode`, `passed`, `outputTail`) and the
payload's `accepted` verdict — those fields are evidence, Codex's "tests pass" is not. Claude does
NOT re-run the full suite per task; it reads `accepted`/`verification`, runs the full suite once
per merged parallel wave and once in the whole-feature review, and checks the tool result's `commands`
list for what Codex actually ran.
