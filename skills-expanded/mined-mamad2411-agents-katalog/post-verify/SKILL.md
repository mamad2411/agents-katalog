---
name: post-verify
description: Use after completing a task, feature, fix, refactor, release step, or handoff when the agent must verify the real runtime behavior before saying it is done. Applies to backend, frontend, CLI, batch jobs, integrations, docs-generated artifacts, and fullstack work. Use curl/http clients for HTTP checks, playwright-cli for browser checks, screenshots, command-line probes, logs, or manual evidence; proactively start local services when safe. Includes explicit fresh mode for local development verification when the user asks to resolve port conflicts, clear local data, start a clean session, or restart from scratch.
---

# Post-Verify

## Principle

Prove the finished work in the running system or final artifact. Passing tests, typechecks, or build commands are useful evidence, but they do not replace a runtime or artifact check.

Report observations from this session only. Mark checks as passing only when directly verified.

## Operating Modes

Use **default mode** unless the user explicitly asks for fresh mode.

Default mode:

- Discover and use the real project entry point before declaring verification blocked.
- Start missing local services when the boot command is clear from project instructions, scripts, or config.
- If verification is blocked by a port conflict, stale browser/session state, stale local data, or a wedged dev server, ask before switching to fresh mode.

Fresh mode:

- Use only when the user says `fresh`, `start from fresh`, `restart clean`, `kill and start`, `clear data`, `start from scratch`, `new session`, `resolve port conflict`, or equivalent wording.
- Identify the project command, expected URL or port, conflicting process, and stale state candidate before acting.
- Stop only clearly project-owned local development processes. Send a graceful interrupt or terminate first; use force only after a short timeout.
- Ask before killing an unknown process or a process that may belong to another project or user workflow.
- Allow clearing project-local development data so verification starts from a scratch session: Playwright/browser session state for this project, app cookies/localStorage/sessionStorage, documented temp/cache artifacts, local containers, local volumes, seed/dev databases, or documented local development reset commands.
- Prefer documented reset commands over manual deletion. When no reset command exists, clear only paths or resources that are clearly scoped to the project.
- Never clear production data, shared credentials, global user caches, unrelated browser profiles, or unrelated processes.
- Restart from the documented local command and wait for readiness before running checks.

## Workflow

### 1. Classify the Surface

Inspect the task, changed files, and expected user impact. Choose every lane that applies:

| Lane | Use for |
|---|---|
| Backend/API | HTTP routes, services, workers, queues, databases, auth, migrations, server config |
| Frontend/UI | Pages, components, forms, navigation, visual states, client-side data flow |
| CLI/tooling | Commands, scripts, generated files, developer workflows |
| Integration | External APIs, webhooks, email, storage, payments, auth providers |
| Docs/artifact | Rendered docs, generated reports, exports, templates |

Output one line:

```text
Mode: default|fresh
Scope: <lanes> - touched: <files or areas>
```

### 2. Choose the Smallest Real Check

Create a short verification matrix before running probes:

- Golden path: the main behavior the user expects.
- Edges: one or two realistic failure, empty, invalid, permission, or rollback cases.
- Regression guard: one nearby behavior that should still work.

Prefer checks that exercise the actual entry point users or systems call. Avoid checking only an internal helper when a route, UI, command, or artifact can be verified.

### 3. Adapt to Available Tools

Use the best tools available in the current agent and environment:

| Need | Prefer | Fallback |
|---|---|---|
| HTTP/API | `curl -i`, `http`, repo test client | small script, framework client, documented manual request |
| Browser/UI | `playwright-cli` | `playwright-cli` snapshot, screenshot, and dev server logs |
| CLI/tooling | run the installed command exactly as a user would | dry-run, fixture command, help/version plus output artifact check |
| Worker/job | enqueue or invoke the job entry point | local fixture invocation, log inspection with known input |
| Generated artifact | open/render/parse the output format | checksum, schema validation, text extraction |

Respect project instructions for how to boot services. If they are missing, infer from common commands such as `make dev`, `npm run dev`, `pnpm dev`, `docker compose up`, or the repository README. Record the command used.

Use `playwright-cli` for browser work. When the user asks for `--headed`, headed, or non-headless mode, run `playwright-cli open --headed <url>`.

Do not hard-code ports, credentials, tenant names, or skill names from another project. Discover them from config, environment, seed data, docs, or the user request. Mask secrets in the report.

When a needed local service is not running, proactively try to start it if the command is clear. If the expected port is occupied, inspect it first:

```bash
lsof -nP -iTCP:<port> -sTCP:LISTEN
```

In default mode, use an alternate port only when the project supports it and the changed behavior does not depend on the original port. In fresh mode, stop the project-owned conflicting process, clear project-local stale state when relevant, restart the service, and record the evidence.

### 4. Fresh Mode Setup

Skip this section unless fresh mode is active.

1. Find the local boot command from project docs, package scripts, make targets, compose files, or framework config.
2. Find expected ports and readiness probes from config, logs, health routes, or dev server output.
3. Inspect any conflicting port with `lsof` and confirm the process is project-owned before stopping it.
4. Stop stale project-owned servers, containers, or workers. Prefer graceful commands such as Ctrl-C, `docker compose down`, or the package manager's documented stop command.
5. Clear project-local development data needed for a clean session: Playwright profiles, browser storage, app session data, local temp/cache folders, local containers/volumes, seed/dev databases, or documented dev reset commands.
6. Recreate required seed data or run documented migrations when the clean session needs them.
7. Restart the service from the documented command. Capture the command, URL, port, PID or container name, and readiness signal.
8. Continue to lane checks only after the restarted system responds or produces a clear blocking error.

### 5. Run Lane Checks

#### Backend/API

Verify status codes and meaningful response fields. Include negative cases where relevant.

Example shape:

```bash
curl -sS -i "$BASE_URL/health" | sed -n '1,20p'
curl -sS -i "$BASE_URL/path-under-test" \
  -H "authorization: Bearer $TOKEN" \
  | sed -n '1,40p'
curl -sS -o /dev/null -w '%{http_code}\n' "$BASE_URL/path-under-test"
```

Record status, key body fields, and any relevant log line or trace id.

#### Frontend/UI

Exercise each acceptance step through the UI:

1. Open the actual route.
2. Interact with the relevant controls.
3. Re-check the page after every submit, navigation, or state change.
4. Capture a screenshot when visual state matters or when it helps future review.

Use `playwright-cli` for every browser step. Save screenshots in a sortable timestamped work directory using local time: `YYYYMMDD-HHMMSS-feature-or-work-name`, such as `20260529-143012-settings`. Use one timestamp for all screenshots from the same verification pass.

Save screenshots only under:

```text
<project_dir>/screenshots/<YYYYMMDD-HHMMSS-feature-or-work-name>/<filename>.png
```

Do not save screenshots directly under `<project_dir>/`.

Example shape:

```bash
playwright-cli open --headed "$WEB_URL/path"
playwright-cli snapshot
playwright-cli click <ref>
playwright-cli snapshot
playwright-cli screenshot --filename="<project_dir>/screenshots/<YYYYMMDD-HHMMSS-feature>/01-state.png"
playwright-cli close
```

#### CLI/Tooling

Run the command as documented or as installed:

```bash
<command> --help
<command> <representative arguments>
```

Verify exit code, stdout/stderr, and produced files. For destructive commands, use a fixture, temp directory, dry-run, or test environment.

#### Integrations And Jobs

Use local fakes, sandbox credentials, fixtures, or recorded payloads when available. Verify both the request/enqueue side and the observable result: response, persisted record, emitted event, log, email preview, or output object.

#### Docs And Artifacts

Open, render, parse, or validate the produced artifact. Examples: preview markdown, inspect generated HTML, extract text from PDF/DOCX, validate JSON/schema, or open an exported file.

### 6. Report

Always emit a report, even when checks fail:

```markdown
## Post-Verify Report

Mode: default|fresh
Scope: <lanes>

### Checks
- [x] <golden path> -> <observed evidence>
- [x] <edge case> -> <observed evidence>
- [ ] <failed or blocked check> -> expected <x>, got <y> FAILED

### Verdict
PASSED|FAILED|BLOCKED - <n> of <m> checks passed.

### Evidence
- command: `<exact command or tool action>`
- artifact: `<path or URL>`
- service: `<boot command, URL/port, PID/container, readiness signal>`
- fresh: `<stopped process, cleared project-local data/session state, seed/reset command, restart evidence, or n/a>`
- log/trace: `<short reference>`
```

Use these rules:

- `[x]` means personally observed passing in this run.
- `[ ]` means failed, blocked, skipped, or not run.
- `PASSED` only when every check is `[x]`.
- `FAILED` when a check ran and behavior was wrong.
- `BLOCKED` when verification could not run because of missing services, credentials, tooling, or access.
- Include enough evidence for another agent to repeat the check.

### 7. Recommend Next Action

Suggest one to three concrete next steps based on the verdict and the agent's available workflow names:

| Result | Suggest |
|---|---|
| FAILED with clear cause | fix the cause, then rerun post-verify |
| FAILED with unclear cause | run the local debugging/diagnosis workflow |
| BLOCKED | state the missing prerequisite and exact command/access needed |
| PASSED after code changes | run code review or prepare commit/PR |
| PASSED after UI changes | run visual QA if available |
| PASSED for broad behavior | run deeper QA or regression sweep if risk is high |

Prefer generic wording when skill names differ between agents. If a known local skill exists, name it explicitly.

## Red Flags

- Claiming success from tests alone.
- Marking `[x]` without a probe, interaction, command, or artifact inspection in this session.
- Reusing another project's ports, credentials, paths, or screenshots.
- Skipping edge cases because the golden path passed.
- Reporting `PASSED` while any check is `[ ]`.
- Hiding a blocked check inside a vague summary.
- Killing a process without identifying it and confirming it is project-owned or user-approved.
- Clearing unscoped local data, global caches, shared browser profiles, credentials, or production resources.
- Claiming fresh verification without cleared-session, service restart, and readiness evidence.

## Quick Reference

```text
mode -> classify -> matrix -> start or fresh clear/restart -> run real checks -> report checkbox evidence -> next action
```
