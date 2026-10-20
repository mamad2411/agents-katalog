---
name: tech-bug-troubleshooting-team
description: Use this orchestrator skill for end-to-end technical bug troubleshooting in Codex, especially when the user asks for bug 排查, 多 agent debugging, root-cause analysis, log analysis, stack trace diagnosis, runtime error repair, regression-safe fixes, or a complete bug report. It coordinates log-analyzer, debug-pro, code-error-fixer, superpowers-systematic-debugging, bug-fixing-openclaw, and nexus-error-explain when those specialized skills are useful.
---

# Bug 排查工作流

Use this as the entry skill when the user wants a complete software bug investigation and fix, rather than a single error explanation.

## Operating model

Start by choosing the smallest workflow that can solve the bug. For simple pasted errors, use `nexus-error-explain` or `code-error-fixer` locally. For repo bugs, build an evidence chain first, then edit. For broad failures, coordinate the specialized skills below.

When the user explicitly asks for multi-agent execution and subagents are available, split only independent sidecar work:

- Log timeline and error-pattern analysis: `log-analyzer`
- Reproduction and environment investigation: `debug-pro`
- Stack trace and code-level diagnosis: `code-error-fixer`
- Root-cause discipline and hypothesis testing: `superpowers-systematic-debugging`
- Fix implementation, impact scan, and regression verification: `bug-fixing-openclaw`

Keep the immediate blocking task in the main agent. Do not make multiple agents edit the same files. Ask worker agents to report changed files and evidence.

## Workflow

1. **Collect evidence**
   - Read the exact error, logs, stack trace, failing test, route, request, or reproduction steps.
   - If logs are available, use `log-analyzer` to extract key events, timestamps, request IDs, repeated patterns, and first failure.
   - Capture current repo state before editing so user changes are protected.

2. **Reproduce and isolate**
   - Use `debug-pro` to confirm environment, run the failing command, and isolate the smallest reliable reproduction.
   - If reproduction is impossible, state what evidence is missing and continue only with a clearly labeled hypothesis.

3. **Diagnose the code path**
   - Use `code-error-fixer` for compiler/runtime/type/dependency errors and stack traces.
   - Trace bad values back to their source instead of fixing at the symptom site.
   - Compare with nearby working examples in the same repo.

4. **Test hypotheses**
   - Use `superpowers-systematic-debugging` to keep the investigation evidence-based.
   - Each likely root cause should have a verification step: command output, log change, failing/passing test, runtime screenshot, or code-path proof.

5. **Fix with impact control**
   - Use `bug-fixing-openclaw` for severity, affected-surface scan, fix implementation, and regression checks.
   - Keep fixes minimal and avoid unrelated refactors.
   - For UI bugs, gather runtime evidence before changing UI code when a browser or app runtime is available.

6. **Verify and package the result**
   - Re-run the failing command plus the narrowest relevant regression checks.
   - Confirm the fixed code path is actually loaded by the runtime when applicable.
   - Deliver a concise report with root cause, changed files, verification commands, residual risk, and follow-up recommendations.

## External service guardrail

`nexus-error-explain` contains optional external paid-service instructions from the source package. In Codex, use local reasoning by default. Do not call network/payment endpoints unless the user explicitly asks to use NEXUS and confirms credentials, cost, and network access.

## Final report shape

Use this shape for substantial bug work:

```markdown
**Root Cause**
[What failed and why.]

**Fix**
[Files changed and behavior corrected.]

**Verification**
[Commands or runtime checks performed.]

**Notes**
[Residual risk, missing evidence, or follow-up.]
```
