---
name: figma-verify-parity
description: Verify that an implemented screen matches its Figma design 1:1 by rendering it in a real browser and diffing computed styles and assets against the Figma spec. Use after implementing UI from Figma, before opening a PR, or whenever someone says the build "looks a bit off" from the design.
argument-hint: <url-or-route> [--spec <figma-spec.md>] [--width <px>] [--out <report-path>]
allowed-tools: Bash, Read, Write, Glob, Grep, Task
---

# figma-verify-parity

Parity gate for Figma-driven UI. Delegates the actual comparison to the
`figma-visual-verifier` agent so the screenshots, DOM snapshots and computed-style dumps
never enter the main context — only the defect list comes back.

## Input

```
/figma-verify-parity <url-or-route>
/figma-verify-parity http://localhost:3000/login --spec .tasks/login/figma-spec.md
/figma-verify-parity /checkout --width 1440 --out .tasks/checkout/figma-parity-report.md
```

- `<url-or-route>` — required. A bare route (`/login`) is resolved against the project's
  dev server base URL.
- `--spec` — path to the `figma-spec.md` written by `figma-context-extractor`. If omitted,
  search the current task folder, then the repo root, for `figma-spec.md`.
- `--width` — viewport width. Defaults to the frame width recorded in the spec.
- `--out` — report path. Defaults to `figma-parity-report.md` beside the spec.

## Step 0 — Preconditions

1. Resolve the spec. **No spec → stop.** There is nothing to verify against; say so and
   point at `figma-context-extractor`. Do not fall back to "eyeball it".
2. Confirm the reference screenshots referenced by the spec exist on disk. If they are
   missing, re-extraction is needed — stop and say which files are absent.
3. Confirm the dev server answers. Read `dev_server_command` from `.claude/workflow.yaml`
   when present; otherwise probe the URL. If it is down, start it in the background, wait
   for the port, and note that you started it.
4. Confirm the `chrome-devtools` MCP server is available. If not, stop with the install
   hint — a skipped verification must be visible, never silent.

## Step 1 — Run the verifier

Invoke the `figma-visual-verifier` agent with:

- the spec path and its screenshot directory,
- the resolved URL and viewport width,
- the asset manifest (`figma-assets.md`) if one exists,
- the list of files changed for this screen (`git diff --name-only` against the base
  branch, filtered to UI paths) so defects can be anchored to `file:line`.

The agent writes the report and returns a verdict plus the blocker/major rows.

## Step 2 — Act on the verdict

**PASS** — print the one-line summary and the report path. Done.

**FAIL** — print every blocker and major with its `file:line`, then:

```
Parity FAIL — <n> blockers, <m> major.
Report: <path>

Fix these before the PR. Re-run /figma-verify-parity when done.
```

Fix the defects if the caller asked for a fix pass; otherwise leave them for the caller.
Either way, re-run this skill after any fix — a defect list is only closed by a fresh
PASS, never by reasoning that the fix must have worked.

**NOT RUN** — surface the reason (dev server down, route 404, MCP missing) and stop.
Do not report PASS, and do not let a caller treat NOT RUN as a pass.

## Step 3 — Record

Append a one-line entry to the task's state or notes file when a task context exists:

```
figma-parity: <PASS|FAIL> <n> blockers / <m> major — <report path> — <ISO timestamp>
```

## Rules

- Blockers are non-negotiable: a generated or substituted asset, a missing element, a
  wrong colour, a wrong icon. None of these ship.
- Never widen the tolerance to make a report pass. If a delta is real and intended,
  the design or the mapping file changes first, then verification re-runs.
- This skill reports and gates. It does not redesign, and it does not decide that the
  implementation is "better" than the design.
