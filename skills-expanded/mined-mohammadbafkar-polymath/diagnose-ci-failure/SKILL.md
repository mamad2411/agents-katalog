---
name: diagnose-ci-failure
description: Diagnose a failed GitHub Actions run — fetch logs via MCP, identify the failing step, classify (flake / real / config), propose next action.
---

# diagnose-ci-failure

> One failed run. Fetch logs, find the failing step, classify, propose the next move.

> **MCP binding (read before any tool call):** resolve which server backs `ci` from `${POLYMATH_PLUGIN_DATA:-$HOME/.polymath/data}/polymath-core/project-context.json` `mcpResolution.github` — when `source` is `host`, the CURRENT host agent's own `github` MCP server is ALREADY registered: use its tools (`toolPrefix` gives the naming) and do NOT register or start a polymath copy. A server registered in a DIFFERENT agent is never a substitute. When `source` is `plugin`, the plugin-shipped `.mcp.json` server backs this skill. When `none`, credentials are unconfigured: ask the user to configure them or degrade gracefully. See the `polymath-core:mcp-bridge` skill.

## When to use

- A workflow run failed and the user wants to know why.
- The `Stop` hook flagged a failed run on the current branch.

## Inputs

- Run URL or `(owner, repo, run_id)`.

## Procedure

1. **Fetch** the run via the github MCP server (`get_workflow_run`, `list_workflow_jobs`, `get_workflow_run_logs` if available — else the `logs_url` from the run + `Bash` to download).
2. **Identify the failing job**. Pick the first non-green one (later jobs that depend on it will also fail; ignore for now).
3. **Identify the failing step** within that job. Look for the first non-zero exit.
4. **Classify**:
   - **Real failure** — a test assertion failed, a build broke, a lint rule fired. Cite the file:line and the assertion.
   - **Flake** — known-flaky test pattern (network sleep, timing race, port collision). Confidence: low unless the same test has flaked recently.
   - **Config / infra** — runner OOM, missing secret, network 5xx fetching a dependency. Not a code problem.
5. **Propose next action**:
   - Real failure → the change needed (or "we don't have the diff context — look at <file>").
   - Flake → re-run the failed job; file a tracking issue if the test has flaked 3+ times.
   - Config / infra → fix the workflow / secret / dependency pin; don't just re-run.

## Output

```text
CI diagnosis: <run url>

Failing job: build (ubuntu-latest, node 20).
Failing step: pnpm test (exit 1).

Root cause: REAL FAILURE
  tests/lib/rate-limit.test.ts:42
  expected: false
  actual:   true
  reason:   the window-eviction boundary moved when we switched to a
            monotonic clock in PR #123. Test still uses wall-clock.

Next action:
  Fix the test to inject the clock (use the project's fake-timer
  conventions — refer to the project's testing notes in
  `.polymath/project.yaml` or the vendor's official docs).
  Don't re-run; it will fail the same way.
```

## Anti-patterns to avoid

- Re-running a real failure.
- Diagnosing without reading the actual failing step's logs.
- "Looks like a flake; let me just re-run" — without checking if the test has flaked before.

