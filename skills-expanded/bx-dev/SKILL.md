---
name: bx-dev
description: "Use only when the user invokes $bx-dev or explicitly asks to start/resume an ad-hoc bx-dev development session. Orchestrates Codex subagents for implementation/review on a session branch without an external issue tracker. Do not use for ordinary direct edits."
---

# bx-dev - Ad-hoc Development Session (public edition)

## Codex Runtime Contract

This workflow was originally written for long-running Agent Teams. In bx-codex,
public instructions use **natural-language Codex subagent spawns**. Most bx-dev
teammates are single-shot: Lead spawns a role with a full brief, waits for one
final response, consumes the report, then calls `close_agent` for that agent id.
If a subagent is still live/running before its final response, Lead may use
`send_input` for a correction. If the subagent is completed, closed, missing, or
stale, Lead must spawn a fresh role with the full relevant context. The
authoritative runtime contract is
`docs/CODEX-ORCHESTRATION.md`.

When this skill is invoked, treat it as explicit user consent to use Codex
subagents unless `--solo` is set. The legacy primitives `TeamCreate`,
`Task(team_name=...)`, `SendMessage`, `WaitNextSendMessage`, `TaskList`,
`TaskUpdate`, `TeamDelete`, and `shutdown_request` do NOT exist in Codex —
ignore any inline references to them as historical wording.

Runtime mapping:

| Legacy term in this file | Codex action |
|---|---|
| `Task(... team_name=..., prompt=...)` / `TeamCreate` | Spawn a fresh subagent via natural language: "Spawn the <name> subagent with the following input: ...". |
| `SendMessage(recipient=teammate, content=...)` | If that exact Codex agent is still live/running, use `send_input` with `<content>`. If it has completed, is closed, or no live id exists, spawn a fresh subagent of that role with updated full context including `<content>`. |
| Wait for SendMessage / `WaitNextSendMessage` | `wait_agent` against the spawned worker id recorded in `codex_agents`. |
| `TaskList` / `TaskUpdate` | Use the `/plan` slash command (or skip — Codex tracks state itself). |
| shutdown / `shutdown_request` / `TeamDelete` | `close_agent(target=<agent_id>)`, then clear `state.teammates.{role}` and mark `state.codex_agents.{role}.status = "closed"`. |

Keep `teammates` as logical role labels if existing state uses it, but store
real Codex ids under `codex_agents.{role}.agent_id`.

You are **Lead**. Orchestrator. In team mode, you do NOT implement code,
perform semantic code review, or conduct acceptance QA. You MAY run
deterministic orchestration commands and gates: `git status`, `git diff --stat`,
branch/PR probes, configured test commands, lint/build commands, and smoke
commands needed to route the workflow. You coordinate teammates.

Exception: `--solo` flag — Lead works directly, no subagents. See "Solo Mode" section.

Global AGENTS.md rules (executor, delegation matrix) are DISABLED during bx-dev.

## State Files

```
.bx-dev/<session-id>/state.json  — session state (one active session at a time)
.bx-dev/<session-id>/brief.md      — latest Scout brief (overwritten per task)
.bx-dev/<session-id>/context.md   — session progress log (Lead appends after each major event)
```

State JSON shape:
```json
{
  "active": true,
  "branch": "dev/auth-fixes",
  "topic": "auth fixes",
  "team_name": "bx-dev-super-test",
  "mode": "team",
  "teammates": {
    "dev": "dev-1",
    "bug_reviewer": null,
    "security_reviewer": null,
    "compliance_reviewer": null,
    "qa": null,
    "merger": null
  },
  "codex_agents": {
    "dev": {
      "agent_id": "agent_...",
      "role": "dev",
      "status": "running"
    }
  },
  "waiting_for": "",
  "lead_session_id": "",
  "task_count": 0,
  "push_count": 0,
  "flags": {
    "solo": false,
    "careful": false,
    "no_review": false,
    "plan_approve": false,
    "squash_on_push": true
  },
  "dev_server_url": "",
  "completed_tasks": []
}
```

**STATE FILE RULE**: NEVER use `apply_patch` for `.bx-dev/<session-id>/` state files. Use shell commands instead:
- **state.json**: all updates via `jq`:
  ```bash
  jq '.field = "value"' .bx-dev/<session-id>/state.json > .bx-dev/<session-id>/state.json.tmp && mv .bx-dev/<session-id>/state.json.tmp .bx-dev/<session-id>/state.json
  ```
  For initial creation: `echo '{"active":true, ...}' > .bx-dev/<session-id>/state.json`
- **brief.md**: overwrite via heredoc:
  ```bash
  cat > .bx-dev/<session-id>/brief.md <<'BRIEF'
  ...scout report...
  BRIEF
  ```

## Delegation rule (team mode)

Lead works ONLY through Codex subagents for implementation, semantic review,
and QA (when not `--solo`). Each role —
Dev, Bug Reviewer, Security Reviewer, Compliance Reviewer, QA, Merger — is
spawned as a fresh single-shot subagent via natural language: "Spawn the
<name> subagent with the following input: ...". Dev, Bug Reviewer, Security
Reviewer, Compliance Reviewer, and QA prompts are inline in this file. Merger
uses the bundled `templates/agents/bx-dev-merger.md` template. Most follow-up
work happens by spawning a fresh role with the new full context. The only
exception is a live/running agent that has not produced a final response yet;
Lead may send that agent a correction via `send_input`.

**Lead does NOT do:** write code, semantic review, code-quality assessment, or
acceptance QA. Lead may run deterministic gates and git/runtime probes to route
the workflow, but teammate judgement remains with subagents.

Exception: `--solo` mode — Lead does everything directly.

## Rules

1. **Single-shot subagents only (when not --solo).** Every teammate is a fresh spawn via natural language ("Spawn the <name> subagent with the following input: ..."). There is no team registration, no `team_name`, no long-running session.
2. **Lead does not implement or judge teammate work.** Lead may do file reads,
   subagent orchestration (natural-language spawn), git status/log/add/commit/push,
   deterministic test/lint/build/smoke gates, branch/PR probes, and shell
   commands for `.bx-dev/<session-id>/` state files. Lead never uses
   `apply_patch` on state files.
3. **Dev does not commit/push — Lead does.** Dev implements and returns the diff summary in its final response. Lead commits, pushes, and manages the session branch.
4. **Track and close teammates in state.** Always keep `teammates` object in state.json up to date. Update on every spawn. Immediately after consuming a subagent final response, call `close_agent(target=<agent_id>)`, then clear that role and mark `codex_agents.<role>.status = "closed"`.
5. **Wait for real subagent completion.** Spawn first, persist the returned agent id in `codex_agents`, then wait via `wait_agent`. Do not treat the spawn itself as the worker result.
6. **No persistent Dev across tasks.** Each task spawns a fresh Dev subagent with full briefing — single-shot model has no implicit context carryover. Lead must re-state the relevant prior context in each new spawn input.
7. **Reviewers are fresh per task.** Spawn, review, results returned in the spawn response.
8. **`waiting_for` is still updated** for recovery, but each wait is an explicit `wait_agent` on the spawned worker id.
   ```bash
   jq '.waiting_for = "<role>"' .bx-dev/<session-id>/state.json > .bx-dev/<session-id>/state.json.tmp && mv .bx-dev/<session-id>/state.json.tmp .bx-dev/<session-id>/state.json
   ```
   Where `<role>` is `"dev"`, `"reviewers"`, `"qa"`, `"merger"` (waiting on Merger subagent during Push Step 5 or Step 6 — team mode only), `"exit-finalize"` (waiting on Dev's finalize file/report pass in Exit Step 2), or `"exit-kill"` (waiting on Dev's background-kill report in Exit Step 4). Clear it with `""` when the spawn result arrives.

9. **Close every subagent after final response.** This applies to Dev, QA,
   reviewers, Merger, and any exit/finalize helper. The sequence is always:
   consume final response → persist report/state → `close_agent(target=<agent_id>)`
   → set `codex_agents.<role>.status = "closed"` → clear `teammates.<role>`.

10. **Spawn lifecycle transaction.** Every spawn step for Dev, reviewers, QA,
    Merger, and helper roles MUST follow this transaction before any wait:
    natural-language spawn → capture returned `agent_id` → persist
    `codex_agents.<role> = {agent_id, role, status:"running"}` and
    `teammates.<role> = "<logical-name>"` → set `waiting_for` → call
    `wait_agent`. After consuming the final report, close the agent and mark it
    `closed` before routing to the next step.
## Liveness Doctrine (simplified)

Two invariants, NON-NEGOTIABLE.

### Invariant 1 — Waiting protocol
Before waiting for any subagent result, set `state.waiting_for` to the role name. Then call `wait_agent` with the current `codex_agents.<role>.agent_id`. Clear `waiting_for` to `""` when the final worker report is received. One atomic jq per set; batch co-updates into the same jq when they belong to the same logical step. The user can always interrupt.

**KEY: "Idle · subagent running" in the HUD means the MAIN THREAD is idle in `wait_agent`, but the subagent is ACTIVELY WORKING.** This is the NORMAL state during a subagent's task. Do NOT report this to user as "subagent went idle / dropped" — that misrepresents reality.

### Invariant 1a — Interrupted waits and late notifications
If the user interrupts while Lead is in `wait_agent`, or if `wait_agent` is aborted and a `subagent_notification` lands afterward, Lead MUST treat the notification path as first-class completion:

1. Do NOT immediately re-spawn the role.
2. Inspect the recent thread events/messages for the waited role's final report.
3. If a final report exists, consume it as the authoritative completion event:
   - persist any payload into `.bx-dev/<session-id>/brief.md` / `context.md` as appropriate
   - call `close_agent(target=<agent_id>)`
   - set `.waiting_for = ""`
   - set `.teammates.<role> = null`
   - set `.codex_agents.<role>.status = "closed"`
4. Resume the next workflow step from that final report.
5. Only if no final report exists should Lead resume `wait_agent` or enter Recovery.

Never tell the user "still waiting on Dev" after a final `subagent_notification` has already arrived.

### Invariant 2 — Close is explicit
Single-shot subagents return one final response, but their Codex panels may
remain open until Lead closes them. There is no `shutdown_request`, no
handshake, no `TeamDelete`. After consuming the spawn result, Lead calls
`close_agent(target=<agent_id>)`, then clears `state.teammates.{role}` and marks
`state.codex_agents.{role}.status = "closed"`.

### Doctrine precedence
If any per-step procedure elsewhere in this skill describes a shutdown that waits for approval or any indefinite block — this doctrine OVERRIDES that procedure.

## Flags

Parse from `$ARGUMENTS`:

| Flag | Effect |
|---|---|
| `--solo` | No team, no agents. Lead works directly. Old bx:dev behavior. |
| `--careful` | Adds QA phase after review passes. |
| `--no-review` | Skip reviewers entirely for the whole session. |
| `--plan-approve` | Dev waits for user OK before coding (default: show plan, proceed immediately). |
| `--sop` | DEPRECATED no-op. Squash-on-push is now the default; this flag is accepted for backward compatibility and silently ignored. Use `--no-sop` to opt out. |
| `--no-sop` | Disable default squash. Push uses `--merge` (preserves all per-task commits in `dev` log) instead of `--squash`. |

## Public Spawn Syntax

Use natural-language spawn requests in public instructions:

```text
Spawn a worker subagent named `<role-name>` with the following input:
<substituted role prompt + task brief + write/read ownership>
```

If an implementation exposes an internal primitive named `spawn_agent(...)`,
treat examples of that shape as pseudocode for the runtime, not callable public
syntax. Regardless of the surface, record the returned `agent_id` in
`state.codex_agents.<role> = {agent_id, role, status:"running"}` before waiting,
and keep `state.teammates.<role>` as the human-readable logical role label.

### Role priority

| Role | Priority | When spawned |
|---|---|---|
| Dev | High-capability coding worker | Fresh per task or fix cycle |
| Bug Reviewer | Fast correctness reviewer | Every non-trivial task |
| Security Reviewer | High-capability security reviewer | When diff touches auth/input/db/secrets patterns |
| Compliance Reviewer | Fast rules reviewer | When project has AGENTS.md (or legacy CLAUDE.md) with substantive rules |
| QA | High-capability acceptance tester | Only with `--careful` flag |

## Commit Convention

All commits follow [Conventional Commits](https://www.conventionalcommits.org/) with scope `dev`:

```
<type>(dev): <description>
```

### Types

| Type | When | Example |
|---|---|---|
| `feat` | New feature (default) | `feat(dev): add user authentication flow` |
| `fix` | Bug fix | `fix(dev): restore validation for empty input` |
| `test` | Test-only changes | `test(dev): add pytest coverage for auth module` |
| `docs` | Documentation only | `docs(dev): add API usage examples` |
| `refactor` | Restructuring without behavior change | `refactor(dev): extract style logic into lookup table` |
| `chore` | Tooling, config, non-functional | `chore(dev): update pyproject.toml dependencies` |

### Rules

1. **Scope is always `dev`** — no Story IDs in this mode.
2. **Description language must match existing commits.** Run `git log --oneline -10` and detect the language. Use the same.
3. **Description is lowercase**, imperative mood, no period at end.
4. **BREAKING CHANGE**: add `!` before `:` — `feat(dev)!: redesign auth API`.
5. **Team mode:** one commit per task after review passes. If many unrelated changes, still ONE commit — this is ad-hoc mode.
6. **Solo mode:** changes accumulate without commits during the Working Phase, then Push Step 1 creates one conventional commit for all relevant dirty session changes before pushing.

## Session Lifecycle

```
/bx:dev [topic] [flags]     <-- enter session, create branch, spawn team
  user: do X                 <-- Scout + implement + review + commit
  user: now do Y             <-- Scout + implement + review + commit
  user: push                 <-- tests, push, PR -> dev, merge
  user: do Z                 <-- more work
  user: push                 <-- another push cycle
  user: exit                 <-- end session, cleanup
```

---

## Phase 0: Enter Session

`{project}` = `basename $(pwd)`. Used for session names throughout the session.
`{lead_name}` = "lead" (the orchestrator label). Use this as `{lead_name}` in all spawn prompts so subagents know who they are reporting to.

### Step 1: Check for conflicts

```bash
git status --porcelain
```
If dirty -> tell user, STOP. Don't auto-commit someone else's work.

Check for active `/bx:dev` session (recovery):
```bash
active_state="$(
  find .bx-dev -mindepth 2 -maxdepth 2 -name state.json -print 2>/dev/null |
  while IFS= read -r state_file; do
    if jq -e '.active == true' "$state_file" >/dev/null 2>&1; then
      printf '%s\n' "$state_file"
      break
    fi
  done
)"
if [ -n "$active_state" ]; then
    SESSION_ID="$(basename "$(dirname "$active_state")")"
    echo "EXISTING_SESSION ${SESSION_ID}"
fi
```
If found -> go to Recovery section.

### Step 2: Ensure dev branch exists

```bash
git fetch origin
if ! git show-ref --verify --quiet refs/remotes/origin/dev; then
    git checkout -b dev main && git push -u origin dev
fi
```

### Step 3: Create session branch

- If user passed a topic (`/bx:dev auth fixes`): `slug` = kebab-case of topic, max 30 chars.
- If no topic: `slug` = `adhoc-{YYYYMMDD-HHmm}`

> Naming convention: `dev/${slug}` by default. If a leaf ref `dev` exists locally (refs collision), fallback to `adhoc/${slug}`. Both prefixes are still branched from `origin/dev` — only the name differs. Never invent a new prefix on the fly; use exactly these two.

```bash
session_branch="dev/${slug}"

# Refs collision check: cannot have both ref `dev` (leaf) and ref `dev/<slug>` (under dir).
# Git stores refs as files: `.git/refs/heads/dev` is either a file OR a directory, not both.
if git show-ref --verify --quiet refs/heads/dev; then
  # `dev` exists as a leaf ref → can't create `dev/<slug>` under it.
  # Fallback: use `adhoc/` prefix (no collision risk).
  session_branch="adhoc/${slug}"
  echo "⚠ Refs collision: leaf branch 'dev' exists locally → using fallback prefix 'adhoc/' for session branch."
fi

git checkout -b "$session_branch" origin/dev
git push -u origin "$session_branch"
```

### Step 4: Detect commit language

```bash
git log --oneline -10
```
Detect language of existing commits (Russian / English). Use the same for all commits this session.

### Step 5: Parse flags

⛔ **STRICT PARSING — NO INFERENCE.** Lead parses ONLY the literal flag tokens listed below. Lead does NOT infer flags from context (\"this is just tests, let's skip review\"), does NOT alias unknown flags to known ones, does NOT silently drop or substitute flags. If a flag is not explicitly in `$ARGUMENTS`, its value is the default below — period.

Extract from `$ARGUMENTS`:
```
--solo           -> flags.solo = true, mode = "solo"
--careful        -> flags.careful = true
--no-review      -> flags.no_review = true
--plan-approve   -> flags.plan_approve = true
--sop            -> (no-op, DEPRECATED — squash is now the default; accepted for backward compatibility, silently ignored)
--no-sop         -> flags.squash_on_push = false   # disable default squash; use regular merge commit on push (preserves per-task commits in dev log)
```
Default: `solo=false`, `careful=false`, `no_review=false`, `plan_approve=false`, `squash_on_push=true` (squash is the default; `--no-sop` opts out). `mode = "team"`.

**Unknown flag handling**: any token starting with `--` that is NOT in the list above → **STOP, surface to user**: `"Unknown flag: '{flag}'. Recognized flags: --solo, --careful, --no-review, --plan-approve, --sop (deprecated no-op), --no-sop. Did you mean one of these? Drop or correct the flag and re-run."`. Do NOT guess. Do NOT proceed with default behavior. Do NOT alias.

**Flag echo (MANDATORY)**: immediately after parsing, BEFORE creating team or spawning Dev, Lead MUST echo the resolved flag set to user in one line:

> `Flags resolved: solo={true|false}, careful={true|false}, no_review={true|false}, plan_approve={true|false}, squash_on_push={true|false}, mode="{team|solo}".`

This makes silent flag-misinterpretation impossible — user sees what Lead understood and can stop the session if wrong before any work happens.

**Flag compatibility (explicit):**
- `--solo` forces `mode = "solo"`. Solo has no agents, no SCOUT, no review — so flags that presuppose those CANNOT coexist:
  - `--solo` + `--careful` -> **ERROR, STOP**: `"--solo and --careful are incompatible: --solo has no agents, --careful needs a QA agent. Drop one flag and re-run."`
  - `--solo` + `--plan-approve` -> **ERROR, STOP**: `"--solo and --plan-approve are incompatible: --plan-approve waits for your OK on a Scout Report, but --solo skips SCOUT entirely. Drop one flag and re-run."`
  - `--solo` + `--no-review` -> **INFO, proceed**: `"--no-review is redundant with --solo (solo already skips review). Continuing."` (keep `flags.no_review=true` for state completeness)
- `--sop` is DEPRECATED and now a no-op — squash is the default for push. Passing `--sop` is accepted (no error) but changes nothing; Lead may optionally print `"--sop is deprecated: squash-on-push is now the default. Ignoring."`. Use `--no-sop` to opt out of the default squash.
- `--no-sop` is compatible with every other flag (including `--solo`). It only affects Push Step 5 (PR merge strategy): when set, Push uses `--merge` instead of `--squash`. It does NOT affect review, QA, or any other phase.

Rationale: silent flag-dropping or silent flag-inference leaves users confused when a promised agent (QA, reviewers, user-approval gate) never appears, OR a promised flag (squash) is silently swapped for an unrelated one (skip-review). Prefer a clear error / mandatory echo at Phase 0 over a mysterious missing/extra behavior mid-session.

### Step 5.5: Collect dev-server URL (if --careful with web interface)

If `flags.careful == true`:
- Ask user once: "`--careful` spawns a QA subagent that opens a browser MCP. What dev-server URL should QA use? (e.g., `http://localhost:3000`, or `none` if this is a CLI/API project, or `later` to set it via `set dev-server <url>` once the server is up)"
- Record answer as `dev_server_url` in state:
  - Valid URL (`http://...` or `https://...`) -> store as-is.
  - `none` -> store empty string; QA will skip browser checks and only run CLI/API tests.
  - `later` or empty -> store empty string; remind user: "You can set it anytime during the session with `set dev-server <url>`. Until then, QA will block on browser tasks."
- This skill does NOT start the server. If user hasn't started it yet, tell them to do so before the first `--careful` task, or use `later` and set the URL after starting it.

### Step 6: Spawn Dev (if not --solo)

`{lead_name}` is the literal string `"lead"` — used inside spawn prompts so the Dev subagent knows who to address its result to.

Spawn Dev for the FIRST task only when there is a real first task to brief — bx:dev does NOT pre-spawn a Dev that sits idle. The first Dev spawn happens at the start of Main Loop iteration 1 (see "Spawn Dev" inside the Main Loop), with the actual task brief.

For now (Phase 0 Step 6) record no live Dev:
`state.teammates.dev = null` and `state.codex_agents.dev = null`. The spawn
happens when the user provides their first task in the Main Loop.

### Step 7: Save session state

```bash
SESSION_ID="${session_id:-$(date +%Y%m%d-%H%M%S)}"
mkdir -p ".bx-dev/${SESSION_ID}"
cat > ".bx-dev/${SESSION_ID}/state.json" <<EOF
{
  "active": true,
  "branch": "${session_branch}",
  "topic": "${topic}",
  "team_name": "bx-dev-${project}",
  "mode": "${mode}",
  "teammates": {"dev": null, "bug_reviewer": null, "security_reviewer": null, "compliance_reviewer": null, "qa": null, "merger": null},
  "codex_agents": {"dev": null, "bug_reviewer": null, "security_reviewer": null, "compliance_reviewer": null, "qa": null, "merger": null},
  "waiting_for": "",
  "task_count": 0,
  "push_count": 0,
  "flags": {"solo": ${solo}, "careful": ${careful}, "no_review": ${no_review}, "plan_approve": ${plan_approve}, "squash_on_push": ${squash_on_push:-true}},
  "dev_server_url": "${dev_server_url:-}",
  "completed_tasks": []
}
EOF
```

### Step 8: Tell user

"Session started on `{session_branch}`. [team mode / solo mode]. Tell me what to do. Say `push` when ready to merge into dev, `exit` to end."

---

## Task Loop

When user says something that is not push/exit/done:

### Step 1: Lead formats task brief

Extract the user's request. Compose a task message:

```
## Task
{user's request, verbatim}

## Project context
Read CLAUDE.md and AGENTS.md for project rules and conventions.

## Session context
Branch: {session_branch}
Previous tasks this session:
{for each completed task: "- {description} (files: {file list})"}
```

### Step 2: Spawn Dev

There is no live Dev to message — single-shot subagents do not persist between tasks. For every iteration, spawn a fresh Dev with the FULL brief (task + any session context the new Dev needs).

Choose the Dev mode before spawning:
- `MODE: IMPLEMENT` when `flags.plan_approve == false`. Dev performs SCOUT internally, implements, verifies, and returns one final implementation report containing the Scout Report plus changed files.
- `MODE: SCOUT_ONLY` when `flags.plan_approve == true`. Dev performs SCOUT only, returns the Scout Report as its final response, and stops. Lead must close that scout agent before asking the user for approval.

Spawn Dev:

Spawn a worker subagent named `bx-dev-dev` with the following input: `<DEV PROMPT (Spawn Prompts section) with MODE plus task brief and session context appended>`.

After the spawn returns an agent id, persist the lifecycle state before waiting:
```bash
jq --arg id "<agent_id>" --arg name "dev-{N}" \
  '.teammates.dev = $name
   | .codex_agents.dev = {"agent_id": $id, "role": "dev", "status": "running"}
   | .waiting_for = "dev"' \
  .bx-dev/<session-id>/state.json > .bx-dev/<session-id>/state.json.tmp && \
  mv .bx-dev/<session-id>/state.json.tmp .bx-dev/<session-id>/state.json
```

### Step 3: Wait for Dev final response

WAIT for Dev's final response via `wait_agent` on `codex_agents.dev.agent_id`. If interrupted, first check for a late `subagent_notification` before deciding Dev is still pending.

If Dev returns `STATUS: BLOCKED_QUESTION`, persist the question, call `close_agent(target=<agent_id>)`, set `codex_agents.dev.status="closed"`, clear Dev state, ask the user, then spawn a fresh Dev with the user's answer included using the Dev spawn lifecycle transaction. Do not keep the blocked Dev panel open.

When the final response is received, persist the Scout Report section to `.bx-dev/<session-id>/brief.md`. For `MODE: IMPLEMENT`, also persist the implementation report to `.bx-dev/<session-id>/dev-report.md`. Then call `close_agent(target=<agent_id>)`, clear `waiting_for`, clear `teammates.dev`, and mark `codex_agents.dev.status = "closed"`:
```bash
jq '.waiting_for = "" | .teammates.dev = null | .codex_agents.dev.status = "closed"' .bx-dev/<session-id>/state.json > .bx-dev/<session-id>/state.json.tmp && mv .bx-dev/<session-id>/state.json.tmp .bx-dev/<session-id>/state.json
```

### Step 4: Lead handles Scout Report

**If `--plan-approve`:**
Show plan to user only after the `SCOUT_ONLY` Dev final response has been persisted and the scout agent has been closed.
- User says OK/go/proceed -> spawn a fresh Dev in `MODE: IMPLEMENT` with the approved Scout Report and original task included, using the Dev spawn lifecycle transaction. Go back to Step 3.
- User says "no, do it differently" / provides corrections -> spawn a fresh Dev in `MODE: SCOUT_ONLY` with the corrections included, using the Dev spawn lifecycle transaction. Go back to Step 3.

**Default (no `--plan-approve`):**
There is no second message to Dev. The same `MODE: IMPLEMENT` spawn already performed SCOUT, implemented, verified, returned final response, and was closed.

If user intervenes before Dev finishes ("wait, do it differently") -> send
input only if the agent is still running. If a final response already arrived,
close that agent first, mark it `closed`, then spawn a fresh Dev with the new
constraints using the Dev spawn lifecycle transaction.

### Step 5: Lead receives Dev implementation report

Dev has already written tests where appropriate, implemented the approach from the Scout Report, run tests/linter, self-verified, returned "Done, files: [...]", and been closed by Lead.

### Step 6: Lead receives Dev's "Done"

If `--no-review` flag -> skip to Step 9 (Commit).

Otherwise -> proceed to Step 7 (Smart Reviewer Selection).

### Step 6.5: Smoke tests (Lead runs BEFORE review)

Find tests related to Dev's changed files:
```bash
changed_src=$(git diff --name-only HEAD | grep -E '\.(py|ts|js|go|rs)$' | grep -v test | grep -v spec\.)
```

For each source file, find matching test file (heuristic: `test_{name}`, `{name}_test`, `{name}.test`, `{name}.spec`):
```bash
for src in $changed_src; do
    base=$(basename "$src" | sed 's/\.[^.]*$//')
    find . -name "test_${base}*" -o -name "${base}_test*" -o -name "${base}.test.*" -o -name "${base}.spec.*" 2>/dev/null
done
```

Run found tests. Detect framework:
```bash
# Python
.venv/bin/pytest <test_files> -v --tb=short 2>/dev/null
# Node
npx jest <test_files> 2>/dev/null
# Go
go test <packages> -v 2>/dev/null
```

- **Tests pass** — proceed to Step 7.
- **Tests fail** — spawn a fresh Dev in `MODE: IMPLEMENT` with input: "Tests fail on your changes. Fix before review: {failed test output}". Follow the Dev spawn lifecycle transaction: persist `teammates.dev`, `codex_agents.dev = {agent_id, role:"dev", status:"running"}`, and `waiting_for="dev"` before waiting. Wait for Dev's final response, persist the fix report, then close the Dev agent with `close_agent(target=<agent_id>)`, set `codex_agents.dev.status="closed"`, clear `teammates.dev`, and clear `waiting_for`.

  Re-run tests. Max 2 rounds. After 2 — show failures to user, ask "Proceed to review anyway?"
- **No test files found** — proceed to Step 7 (no blocking).

### Step 7: Smart Reviewer Selection

Lead analyzes what changed:
```bash
changed_files=$(git diff --name-only HEAD)
diff_stat=$(git diff --stat HEAD)
```

**Pre-step — TRIVIAL fast path:**
Read the Scout Report complexity line from `.bx-dev/<session-id>/brief.md`:
```bash
# Relies on the Scout Report template in Section 0g of the Dev Spawn Prompt,
# specifically the `### Complexity` heading followed by `TRIVIAL/MODERATE/COMPLEX`
# on the next line. If you edit that template, keep this grep in sync.
complexity=$(grep -iE '^### Complexity' -A 1 .bx-dev/<session-id>/brief.md | tail -1 | grep -oE 'TRIVIAL|MODERATE|COMPLEX' | head -1)
```
If `complexity` extraction fails (empty output) -> **safe fallback**: treat as non-TRIVIAL and continue with normal reviewer selection below. Do NOT skip review on ambiguity.

If `complexity == "TRIVIAL"` AND `diff_stat` is small (<20 lines changed, ≤2 files) AND no security-regex match below AND no Compliance trigger below:
-> Skip ALL reviewers. Tell user: "TRIVIAL task — skipping review. Proceed to commit."
-> Jump to Step 9 (Commit).

This preserves review for MODERATE/COMPLEX tasks and for TRIVIAL tasks that happen to touch a security-regex file or a Compliance-gated repo. Rationale: a Bug Reviewer round-trip per one-line CSS tweak is pure overhead; the SCOUT already classified the task as safe.

Decision logic for which reviewers to spawn (non-TRIVIAL path):

**ALWAYS:** Bug Reviewer

**IF** any changed file matches security-sensitive patterns -> **+ Security Reviewer**:
```bash
echo "$changed_files" | grep -iE '(auth|login|session|cookie|token|password|secret|credential|jwt|oauth|csrf|sanitiz|encrypt|decrypt|sql.?injection|migration|\.env|deserializ|exec|eval|child_process|webhook)'
```
If any match -> spawn Security Reviewer.

**Rationale:** the pattern deliberately omits everyday tokens like `api`, `url`, `config`, `role`, `redirect`, `callback`, `admin`, `cors`, `tls`, `ssl`, `helmet`, `rate-limit`, `cert`, `upload`, `download`, `input`, `valid`, `db`, `database`, `query`, `hash`, `spawn`, `permission`, `middleware`, `acl`. Those matched too many neutral filenames (e.g. `url-helper.ts`, `webpack.config.js`, `RoleSelect.vue`, `useCallback.ts`) and produced security-review false-positive spawns. Keep the list narrow; add tokens back only with a concrete false-negative.

**IF** CLAUDE.md or AGENTS.md exists with substantive content (>10 lines) -> **+ Compliance Reviewer**:
```bash
[ -f CLAUDE.md ] && [ $(wc -l < CLAUDE.md) -gt 10 ] && echo "COMPLIANCE"
[ -f AGENTS.md ] && [ $(wc -l < AGENTS.md) -gt 10 ] && echo "COMPLIANCE"
```
If either matches -> spawn Compliance Reviewer.

Show user which reviewers are being spawned:
"Spawning reviewers: Bug Reviewer [+ Security Reviewer] [+ Compliance Reviewer]"

### Step 8: Review cycle

Initialize `review_round = 0`.

#### 8a: Compose review brief

```
## Review Brief
**User request:** {what user asked}
**Scout analysis:** {approach and risks from .bx-dev/<session-id>/brief.md}
**Dev's report:** {Done message with file list}
**Changed files:**
{git diff --stat output}
```

#### 8b: Spawn selected reviewers in parallel

- Bug Reviewer: spawn a fresh reviewer subagent with `<BUG REVIEWER PROMPT with review brief>`.
- Security Reviewer, if selected: spawn a fresh reviewer subagent with `<SECURITY REVIEWER PROMPT with review brief>`.
- Compliance Reviewer, if selected: spawn a fresh reviewer subagent with `<COMPLIANCE REVIEWER PROMPT with review brief>`.

For each spawned reviewer, capture the returned agent id and persist it before
waiting:

```bash
jq --arg id "<agent_id>" --arg name "<logical-reviewer-name>" --arg role "<bug_reviewer|security_reviewer|compliance_reviewer>" \
  '.teammates[$role] = $name
   | .codex_agents[$role] = {"agent_id": $id, "role": $role, "status": "running"}' \
  .bx-dev/<session-id>/state.json > .bx-dev/<session-id>/state.json.tmp && \
  mv .bx-dev/<session-id>/state.json.tmp .bx-dev/<session-id>/state.json
```

#### 8c: Wait for all reviewers

```bash
jq '.waiting_for = "reviewers"' .bx-dev/<session-id>/state.json > .bx-dev/<session-id>/state.json.tmp && mv .bx-dev/<session-id>/state.json.tmp .bx-dev/<session-id>/state.json
```

WAIT for ALL spawned reviewers to report via `wait_agent` on their recorded `codex_agents` ids. If interrupted mid-wait, first reconcile any late `subagent_notification` results before re-waiting or re-spawning.

Once ALL replied, persist the review reports, close every reviewer agent, mark
each closed, clear the logical teammate slots, and clear `waiting_for`:
```bash
jq '.waiting_for = ""
    | .teammates.bug_reviewer = null
    | .teammates.security_reviewer = null
    | .teammates.compliance_reviewer = null
    | if .codex_agents.bug_reviewer then .codex_agents.bug_reviewer.status = "closed" else . end
    | if .codex_agents.security_reviewer then .codex_agents.security_reviewer.status = "closed" else . end
    | if .codex_agents.compliance_reviewer then .codex_agents.compliance_reviewer.status = "closed" else . end' \
  .bx-dev/<session-id>/state.json > .bx-dev/<session-id>/state.json.tmp && \
  mv .bx-dev/<session-id>/state.json.tmp .bx-dev/<session-id>/state.json
```

#### 8d: Merge findings

Combine issues from all reviewers. Deduplicate (same file:line AND same root cause = one issue; keep both if they describe different problems).

#### 8e: Decide

**CASE A — CLEAN:**
Zero issues across all reviewers.
-> Reviewers were already closed and state was cleared in Step 8c.
-> Proceed to Step 9 (Commit).

**CASE B — MINOR/INFO ONLY:**
Zero [CRITICAL] + zero [MAJOR], but [MINOR] or [INFO] issues exist.
-> Show summary to user (informational).
-> Spawn fresh Dev in `MODE: IMPLEMENT` with input: "Review passed. Fix these items: {merged list}"
-> Follow the Dev spawn lifecycle transaction: persist `codex_agents.dev = {agent_id, role:"dev", status:"running"}` and `waiting_for="dev"` before waiting. Wait for Dev's final response, persist the fix report, then close the Dev agent with `close_agent(target=<agent_id>)`, set `codex_agents.dev.status="closed"`, clear `teammates.dev`, and clear `waiting_for`.
-> Re-run smoke tests (Dev's MINOR fixes may have broken something):
   Same targeted tests as Step 6.5. If fail — spawn fresh Dev with the smoke
   failure using the Dev spawn lifecycle transaction, fix, retest (max 2
   rounds).
-> Reviewer agents were already closed and state was cleared in Step 8c.
-> Proceed to Step 9 (Commit).

**CASE C — CRITICAL/MAJOR FOUND:**
Any [CRITICAL] or [MAJOR] survived.
-> Spawn fresh Dev in `MODE: IMPLEMENT` with input: "Review found issues. Fix these: {merged list with all severities}"
-> Follow the Dev spawn lifecycle transaction: persist `codex_agents.dev = {agent_id, role:"dev", status:"running"}` and `waiting_for="dev"` before waiting. Wait for Dev's final response, persist the fix report, then close the Dev agent with `close_agent(target=<agent_id>)`, set `codex_agents.dev.status="closed"`, clear `teammates.dev`, and clear `waiting_for`.
-> Increment `review_round`.

If `review_round >= 2`:
-> Reviewer state is already clear for the completed review round.
-> Show remaining issues to user: "Review didn't converge after 2 rounds. Remaining: {issues}. Commit anyway? [y/n]"
  - User says yes -> proceed to Step 9 (Commit).
  - User says no -> spawn fresh Dev in `MODE: IMPLEMENT` with the specific
    issues using the Dev spawn lifecycle transaction. User drives manually, but
    every Dev final response is still closed with `close_agent`.

Otherwise (`review_round < 2`):
-> Old reviewer state is already clear for the completed review round.
-> Spawn fresh reviewers (Step 8b) with updated review brief including Dev's "Fixed" report.
-> Repeat from Step 8c.

### Step 9: Commit (local, on session branch)

After review passes (or user overrides, or `--no-review`):

```bash
git add <all changed project files from git status>
git commit -m "<type>(dev): <description>"
```

Type: `feat` / `fix` / `refactor` / `chore` / `docs` / `test` — pick based on what was done.
Description: concise summary in the detected language.

Update state:
```bash
jq --arg desc "<description>" '.task_count += 1 | .completed_tasks += [$desc]' .bx-dev/<session-id>/state.json > .bx-dev/<session-id>/state.json.tmp && mv .bx-dev/<session-id>/state.json.tmp .bx-dev/<session-id>/state.json
```

### Step 10: QA (--careful only)

If `--careful` flag is NOT set -> skip to Step 11.

Before spawning, read `dev_server_url` from state:
```bash
dev_server_url=$(jq -r '.dev_server_url // ""' .bx-dev/<session-id>/state.json)
```

Spawn QA:

Spawn a worker subagent named `bx-dev-qa` with the following input: `<QA PROMPT with task context + all changed files + Scout brief + dev_server_url inlined into the dev_server_url: field>`. Empty string for dev_server_url means QA will skip browser checks and report the blocker.

After the spawn returns an agent id, persist QA lifecycle state before waiting:

```bash
jq --arg id "<agent_id>" --arg name "qa-{task_count}" \
  '.teammates.qa = $name
   | .codex_agents.qa = {"agent_id": $id, "role": "qa", "status": "running"}
   | .waiting_for = "qa"' \
  .bx-dev/<session-id>/state.json > .bx-dev/<session-id>/state.json.tmp && \
  mv .bx-dev/<session-id>/state.json.tmp .bx-dev/<session-id>/state.json
```

WAIT for QA result via `wait_agent` on `codex_agents.qa.agent_id`. If
interrupted, first reconcile any late `subagent_notification` from QA.

After consuming the QA report, close QA and clear state before routing:

```bash
jq '.waiting_for = "" | .teammates.qa = null | .codex_agents.qa.status = "closed"' \
  .bx-dev/<session-id>/state.json > .bx-dev/<session-id>/state.json.tmp && \
  mv .bx-dev/<session-id>/state.json.tmp .bx-dev/<session-id>/state.json
```

**QA passed:** proceed to Step 11.

**QA failed:** Spawn fresh Dev in `MODE: IMPLEMENT` with input:
"QA found issues: {QA's report}. Fix these."
Follow the Dev spawn lifecycle transaction before waiting. WAIT for Dev's final
response, persist the fix report, then close Dev with
`close_agent(target=<agent_id>)`, set `codex_agents.dev.status="closed"`, clear
`teammates.dev`, and clear `waiting_for`.
Amend the commit:
```bash
git add <fixed files>
git commit --amend --no-edit
```
Spawn fresh QA with the same QA lifecycle transaction. Re-test. Max 2 QA
rounds. After 2 -> show failures to user, ask "Proceed anyway?"

### Step 11: Task complete

Close any remaining reviewer/QA agent ids with `close_agent(target=<agent_id>)` and clear their state slots.

Update context file:
```bash
cat >> .bx-dev/<session-id>/context.md <<CTX

## Task ${task_count}: ${description}
- Scout: ${complexity}
- Review: ${N} reviewers, ${M} issues found
- Files: ${file_list}
- Status: committed
CTX
```

Tell user: "Task done. [{N} reviewers, {M} issues found/fixed]. {task_count} tasks this session. Continue or `push`."

---

## Set Dev-Server Command

When user says `set dev-server <url>`, `dev-server <url>`, `set server <url>`, or similar:

Extract the URL (first `http://...` or `https://...` token after the trigger phrase). If no valid URL found, ask: `"What URL? e.g. http://localhost:3000"` and STOP.

Validate shape only (no network call):
```bash
echo "$url" | grep -qE '^https?://'
```
If invalid -> `"Not a valid URL (needs http:// or https:// prefix)."` STOP.

Update state:
```bash
jq --arg u "$url" '.dev_server_url = $u' .bx-dev/<session-id>/state.json > .bx-dev/<session-id>/state.json.tmp && mv .bx-dev/<session-id>/state.json.tmp .bx-dev/<session-id>/state.json
```

Tell user: `"Dev-server URL set to {url}. QA (--careful) will use this for browser MCP checks."`

Use case: user started `/bx:dev feat-x --careful` but answered `none` in Phase 0 Step 5.5 (or forgot to start the server), then later started the dev-server and wants QA to actually check the browser. This command updates state without restarting the session.

Note: this command ONLY sets the URL. It does NOT start a dev-server — that is your responsibility. See Step 5.5 for the initial collection flow.

---

## Push Command

When user says `push`, `go`, `ship`, `merge`, `push`, or similar:

### Step 1: Check changes to push

First normalize solo-mode dirty changes into a commit, because solo mode
intentionally accumulates work until `push`.

Read mode and dirty state:
```bash
mode=$(jq -r '.mode' .bx-dev/<session-id>/state.json)
dirty=$(git status --porcelain --untracked-files=all)
```

If `mode == "solo"` and `dirty` is non-empty:
- Inspect the dirty path list and the diff. Treat non-ignored worktree changes
  made during the solo session as relevant session changes.
- If any dirty path is clearly unrelated to the session, generated/local-only,
  or unsafe to include, STOP and ask the user which paths to include. Do not
  push until the commit boundary is explicit.
- Stage the relevant session paths. Use `git add -A` only when every dirty path
  is relevant to the session; otherwise stage explicit paths.
- Create exactly one conventional commit before checking commits to push:
  ```bash
  git commit -m "<type>(dev): <description>"
  ```
  Pick `type` from the Commit Convention section (`feat` for feature work,
  `fix` for bug fixes, `docs`, `test`, `refactor`, or `chore` as appropriate).
  Use `feat(dev): ...` only when the accumulated solo work is feature-like.
- Record the commit SHA and continue with the normal push checks.

Now check committed changes:
```bash
git log origin/dev..HEAD --oneline
```
If nothing -> "Nothing to push." Continue session.

### Step 2: Run tests

Detect test framework (pyproject.toml / package.json / go.mod).
If found:
```bash
.venv/bin/pytest tests/ -v --tb=short 2>/dev/null
npm test 2>/dev/null
go test ./... -v 2>/dev/null
```

- Tests pass -> proceed.
- Tests fail -> show failures. Ask user: "Tests fail. Push anyway? [y/n]"
  User decides.
- No test framework detected -> skip.

### Step 3: Push session branch

Lead pushes directly in both team and solo mode:
```bash
git push origin ${session_branch}
```

### Step 4: Create PR

Lead creates the PR directly in both team and solo mode (Lead already has the full context for the title/body):

```bash
pr_url=$(gh pr create \
  --base dev \
  --head "${session_branch}" \
  --title "<summary of all tasks since last push>" \
  --body "$(cat <<'PR_BODY'
Ad-hoc changes from /bx:dev session.

Tasks:
$(git log origin/dev..HEAD --oneline)
PR_BODY
)")
```

If `gh pr create` fails (e.g., PR already exists) — check for existing PR:
```bash
pr_url=$(gh pr list --head "${session_branch}" --base dev --json url -q '.[0].url')
```
If still no PR — tell user the error, STOP.

Capture `pr_url` — it is passed to Merger in Step 5 (team mode) or used by Lead directly (solo mode).

### Step 5: Merge PR

Read merge-strategy flag from state:
```bash
squash=$(jq -r '.flags.squash_on_push' .bx-dev/<session-id>/state.json)
# merge_op: "pr-merge-squash" if squash==true else "pr-merge-merge"
if [ "$squash" = "true" ]; then merge_op="pr-merge-squash"; else merge_op="pr-merge-merge"; fi
```

**Merge strategy:** default is `--squash` (clean linear log in `dev`, one commit per push). Use session flag `--no-sop` to fall back to `--merge` (all per-task commits preserved on `dev` as a merge commit).

#### Step 5 — Team mode (state.mode == "team")

Lead does NOT run `gh pr merge` directly. Lead spawns a **Merger teammate** to execute the PR merge.

1. **Assemble MERGE_BRIEF.** Capture read-only git context first:
   ```bash
   commits_summary=$(git log origin/dev..${session_branch} --oneline)
   diff_stat=$(git diff --stat origin/dev..${session_branch})
   recent_target=$(git log --oneline -10 origin/dev)
   N=$(echo "$commits_summary" | wc -l | tr -d ' ')
   one_line_summary=$(echo "$commits_summary" | head -1)
   ```

2. **Read Merger template and merge protocol** + append the merge brief:
   - Read `templates/agents/bx-dev-merger.md`.
   - Read `docs/MERGE-PROTOCOL.md`.
   - Append the full merge protocol first so the Merger input is
     self-contained:
     ```
     ## MERGE_PROTOCOL
     <contents of docs/MERGE-PROTOCOL.md>
     ```
   - Append the following `MERGE_BRIEF` block after the protocol:
     ```
     Operation: ${merge_op}
     Source branch: ${session_branch}
     Target branch: dev
     PR URL: ${pr_url}
     Scope / intent: Ad-hoc /bx:dev session push — ${N} commits since last push: ${one_line_summary}
     What changed (diff summary):
     ${commits_summary}

     ${diff_stat}
     Recent commits on target:
     ${recent_target}
     Expected post-merge state: dev tip contains session's changes (as a single squashed commit if Operation is pr-merge-squash, as a merge commit preserving per-task history if Operation is pr-merge-merge); session branch ${session_branch} preserved (delete_branch=false) for continued work.
     Delete branch: false
     ```

3. **Spawn Merger** as a fresh single-shot subagent:

   Spawn a worker subagent named `bx-dev-merger` with the following input: `<Merger template with substitutions above>`.

   After the spawn returns an agent id, persist it before waiting:
   ```bash
   jq --arg id "<agent_id>" --arg name "merger-push-{push_count}" \
      '.teammates.merger = $name
       | .codex_agents.merger = {"agent_id": $id, "role": "merger", "status": "running"}' \
      .bx-dev/<session-id>/state.json > .bx-dev/<session-id>/state.json.tmp && \
      mv .bx-dev/<session-id>/state.json.tmp .bx-dev/<session-id>/state.json
   ```

4. **Set waiting_for**:
   ```bash
   jq '.waiting_for = "merger"' \
      .bx-dev/<session-id>/state.json > .bx-dev/<session-id>/state.json.tmp && \
      mv .bx-dev/<session-id>/state.json.tmp .bx-dev/<session-id>/state.json
   ```

5. **Wait for Merger's verdict via `wait_agent`.** If interrupted, first reconcile any late `subagent_notification` from Merger before deciding the merge is still pending.

6. **Persist, close, and clear Merger state** after consuming the verdict,
   before routing on the status:
   - Persist Merger's full report to the session context or push log.
   - Call `close_agent(target=<codex_agents.merger.agent_id>)`.
   ```bash
   jq '.teammates.merger = null | .codex_agents.merger.status = "closed" | .waiting_for = ""' \
      .bx-dev/<session-id>/state.json > .bx-dev/<session-id>/state.json.tmp && \
      mv .bx-dev/<session-id>/state.json.tmp .bx-dev/<session-id>/state.json
   ```

7. **Route on Merger verdict status:**
   - **`CLEAN`** (or `CONFLICT_RESOLVED` — same success semantics): proceed.
   - **Any other exact template status** (`ESCALATION_CC`, `ESCALATION_PROTOCOL`,
     `ROLLBACK_SMOKE_FAIL`, `ROLLBACK_TEST_REGRESSION`,
     `ROLLBACK_COVERAGE_DEGRADATION`, `ROLLBACK_SEMANTIC_FAIL`,
     `ROLLBACK_CONTINUE_FAIL`, `ROLLBACK_COMMITS_MISSING`, `STALE_BASELINE`,
     `BASELINE_UNUSABLE`, `TEST_INFRA_FAIL`,
     `UNRECOVERABLE_AFTER_PR_MERGE`, `OTHER_GIT_FAIL`,
     `BRANCH_PROTECTION_BLOCKED`): show Merger's verbatim verdict text to user.
     **STOP Push. Keep session intact** (same spirit as Exit Command 3b —
     session branch + Dev + state all preserved; user can fix the underlying
     issue and re-run `push`). Do NOT proceed to Step 6 (sync).
   Proceed to Step 6 (sync).

#### Step 5 — Solo mode (state.mode == "solo")

Lead runs `gh pr merge` directly (no Merger spawn — solo has no agents):
```bash
if [ "$squash" = "true" ]; then
  gh pr merge "$pr_url" --squash --delete-branch=false
else
  gh pr merge "$pr_url" --merge --delete-branch=false
fi
```
`--delete-branch=false` — keep the session branch alive for more work.

If `gh pr merge` fails → show the error to user, STOP. Do NOT proceed to Step 6.

### Step 6: Sync session branch with dev

After PR merge lands on `dev`, pull it back into the session branch so the next task starts from the merged tip:

```bash
git pull origin dev --ff-only
```
If ff-only succeeds → proceed to Step 7.

If ff-only fails (divergent — e.g., a concurrent push to `dev` from elsewhere landed between Step 5 and now):

**Team mode:**
Lead does NOT run `git merge` directly. Lead spawns a **Merger teammate** (operation `merge`) for the local sync.
1. Assemble brief:
   ```
   Operation: merge
   Source branch: origin/dev
   Target branch: ${session_branch}    (already checked out)
   PR URL: N/A (local merge, not pr-merge)
   Scope / intent: Post-push sync — pull concurrent origin/dev changes back into session branch ${session_branch} after our own push merged.
   What changed (diff summary): <git log --oneline ${session_branch}..origin/dev> + <git diff --stat ${session_branch}..origin/dev>
   Recent commits on target: <git log --oneline -10 ${session_branch}>
   Expected post-merge state: session branch tip contains origin/dev's latest commits merged in.
   ```
   (`Delete branch` is omitted — N/A for local merge.)

2. Spawn Merger with name `merger-sync-{push_count}`, same spawn lifecycle as
   Step 5 team-mode. Persist
   `codex_agents.merger = {agent_id, role:"merger", status:"running"}` and
   `teammates.merger = "merger-sync-{push_count}"` before waiting.

3. Set `waiting_for="merger"`. Wait for Merger's final verdict via `wait_agent` on `codex_agents.merger.agent_id`.

4. Persist the Merger report, call `close_agent(target=<agent_id>)`, set
   `codex_agents.merger.status="closed"`, clear `teammates.merger`, and clear
   `waiting_for`.

5. Route on verdict:
   - **`CLEAN`** / **`CONFLICT_RESOLVED`**: proceed to Step 7.
   - **Any other exact template status**: show Merger's verdict to user. STOP Push. Session intact. Do NOT proceed to Step 7 (push_count is NOT incremented on sync failure — the main PR-merge already landed on `dev`, but the session branch is now out of sync with `dev` and needs user attention).

**Solo mode:**
Lead resolves directly:
```bash
git merge origin/dev --no-edit
```
If merge conflicts → apply **Merge Protocol** (`docs/MERGE-PROTOCOL.md`), Steps 0 through 6:
- **Step 0** — DETECT `operation="merge"` via `.git/MERGE_HEAD` (NOT `REBASE_HEAD`); record for later `--abort` / `--continue`.
- **Step 1** — SETUP `diff3` + `rerere`.
- **Step 2** — CLASSIFY each conflicted file: `T` / `SEM` / `S` / `DR` / `B` / `SM` / `CC` / `E` / `L`. Most files here will be `T` (textual) or `L` (lock-file).
- **Step 3-<type>** — RESOLVE per type. `Type CC + -s resolve` is the one unconditional NEVER.
- **Step 4** — SEMANTIC-CHECK (import chain, API shape, test alignment).
- **Step 5** — SMOKE-TEST (detect stack via `pyproject.toml` / `package.json` / `go.mod` / `Cargo.toml` / `build.gradle`; run the corresponding compile + test commands).
- **Step 6** — VERIFY: no markers, diff sane, merge commit message conventions.

Step 7 (ROLLBACK) applies only if a broken merge is discovered AFTER commit — use `git reset --hard ORIG_HEAD` (pre-push CASE A) or `git revert -m 1 <merge-sha>` (post-push CASE B/C).

On unresolvable conflict (Type CC or protocol escalation) → show to user, STOP.

### Step 7: Update state + tell user

```bash
jq '.push_count += 1' .bx-dev/<session-id>/state.json > .bx-dev/<session-id>/state.json.tmp && mv .bx-dev/<session-id>/state.json.tmp .bx-dev/<session-id>/state.json
```

Tell user (include `"via Merger"` only in team mode):
- Team mode: `"Pushed ({squash ? "squash" : "merge"}) into dev via Merger. Continue or exit."`
- Solo mode: `"Pushed ({squash ? "squash" : "merge"}) into dev. Continue or exit."`

---

## Exit Command

When user says `exit`, `done`, `end`, or similar.

**Philosophy:** `exit` is a full teardown. It auto-commits leftover work, auto-pushes unpushed commits, kills background processes, then cleans up team + state + branch. No confirmations for obvious cleanup — user already said `exit`.

**Ordering rule:** reversible actions first (commit), then the make-or-break gate (push), then irreversible cleanup (kill background, shutdown, delete branch, rm state). If the push gate fails, STOP and leave the session fully workable — do NOT proceed to shutdown.

**Abort semantics:** any failure in Steps 2 or 3 aborts the exit. Steps 4+ are never reached. If Step 2 created a finalize commit, that commit remains on the session branch; abort does not automatically roll it back. Tell the user they can undo only that finalize commit with `git reset --soft HEAD~1` if they want the changes staged again before the next push.

### Step 1: Plan (read-only)

Collect facts without mutating anything:
```bash
dirty=$(git status --porcelain)
unpushed=$(git log origin/dev..HEAD --oneline 2>/dev/null | wc -l)
```
Record the initial `dirty` state and pre-exit `HEAD` (in-memory) for reporting
and explicit user-requested discard options. Do not automatically roll back a
finalize commit on abort.

### Step 2: Auto-commit dirty changes (reversible)

If `dirty` is non-empty:
- In `team` mode: Spawn a fresh worker subagent named `bx-dev-dev` only when the
  pending changes need a final file/report pass before committing. Input:
  "Before exit: inspect pending changes, finish any incomplete file edits only if
  required, do not run git add, do not commit, do not push, then report Done with
  changed files and a one-line commit summary." After the spawn returns an agent
  id, persist `teammates.dev = "dev-exit-finalize"` and
  `codex_agents.dev = {agent_id, role:"dev", status:"running"}` with
  `waiting_for="exit-finalize"` before waiting. Wait for the final response,
  persist the one-line commit summary (if useful), call
  `close_agent(target=<agent_id>)`, set `codex_agents.dev.status="closed"`, clear
  `teammates.dev`, and clear `waiting_for`.

- Lead commits directly in both `team` and `solo` mode:
  ```bash
  summary=$(git diff --stat | tail -1)
  git add -A
  git commit -m "chore(dev): finalize session — ${summary}"
  ```
- Record the Lead-created commit SHA as `finalize_sha` (in-memory).
- Tell user: `"Auto-committed {N} uncommitted file(s) as finalize commit {SHA short}."`

If `dirty` was empty, set `finalize_sha=""` and skip.

Recompute `unpushed` (it may have grown by 1 after the finalize commit).

### Step 3: Auto-push if anything unpushed — THE GATE

If `unpushed == 0`: nothing to push, proceed to Step 4.

If `unpushed > 0`: run **Push Command** (all 7 steps: 1 check changes, 2 run tests, 3 push branch, 4 create PR, 5 merge PR, 6 sync session with dev, 7 state + tell user). Uses `--squash` if `flags.squash_on_push == true` (default), otherwise `--merge` (`--no-sop`). Intercept failures and abort exit:

#### 3a. Tests fail (Push Step 2)
ABORT exit. Tell user:
```
Exit aborted: test suite failed on {N} test(s).
  Session is intact. Dev, team, branch, state — all preserved.
  {if finalize_sha set:} Your finalize commit {SHA} is on the branch. Run `git reset --soft HEAD~1` to unstage it if you want to keep editing before next push.
  Failing tests:
    {list}
  Options:
    1. Fix the failures, then say `exit` again.
    2. `push anyway` → re-run push with tests skipped, then exit.
    3. `discard` → `git reset --hard {pre-exit SHA}` to drop finalize commit and exit without pushing (keeps uncommitted dev-server etc. alive).
```
STOP. Do NOT touch teammates, background processes, branch, or state.

#### 3b. PR creation or merge fails (Push Step 4 — `gh pr create`, OR Push Step 5 solo-mode `gh pr merge`)
ABORT exit with the same "session intact" preservation logic as 3a. Show the exact `gh` error to the user. Common causes: no `dev` branch on remote, auth expired, PR permission denied. Options shown:
```
  1. Fix the remote issue, then `exit` again.
  2. `discard` → keep everything local, exit without push.
```
STOP.

#### 3c. Merge conflict during sync (Push Step 6)
Apply MERGE-PROTOCOL.md (solo mode) or Merger teammate resolves per `CONFLICT_RESOLVED` (team mode). Most types (`T`, `L`, `SEM`) resolve automatically — exit continues as if nothing happened. For `CC` (concurrent change on same line), protocol escalates:
```
Exit paused: concurrent conflict in {file}:{line}.
  Your change: {diff}
  Origin/dev change: {diff}
  Resolution? (your / theirs / custom)
```
Wait for user. After resolution → continue Push. If the user types `abort` instead of a resolution → treat as 3b abort (session intact, push reverted via `git merge --abort`).

In team mode: if Merger returns any verdict other than `CLEAN` or
`CONFLICT_RESOLVED` on the sync merge (for example `ROLLBACK_SMOKE_FAIL`,
`ROLLBACK_TEST_REGRESSION`, `ESCALATION_CC`, `ESCALATION_PROTOCOL`,
`STALE_BASELINE`, `OTHER_GIT_FAIL`) → ABORT exit with the same session-intact
preservation as 3a. Show Merger's verbatim verdict text to user. Note that the
PR merge in Push Step 5 has already landed on `dev` at this point — only the
session branch is out of sync. `push_count` is NOT incremented (Push Step 7 was
not reached).

#### 3d. Push succeeded (Push Steps 5 + 6 both CLEAN)
Increment `push_count` (done by Push Step 7). Tell user briefly: `"Pushed ({squash ? "squash" : "merge"}) into dev{ via Merger if team mode}."` Proceed to Step 4.

#### 3e. Merger failure during PR merge (Push Step 5 — team mode only)
Team mode only. Merger returned a non-CLEAN / non-CONFLICT_RESOLVED verdict on the PR merge itself (examples: `ROLLBACK_TEST_REGRESSION`, `ROLLBACK_COVERAGE_DEGRADATION`, `ROLLBACK_SMOKE_FAIL`, `ROLLBACK_SEMANTIC_FAIL`, `ROLLBACK_COMMITS_MISSING`, `ROLLBACK_CONTINUE_FAIL`, `ESCALATION_CC`, `ESCALATION_PROTOCOL`, `STALE_BASELINE`, `BASELINE_UNUSABLE`, `TEST_INFRA_FAIL`, `UNRECOVERABLE_AFTER_PR_MERGE`, `OTHER_GIT_FAIL`, `BRANCH_PROTECTION_BLOCKED`).

ABORT exit with the same "session intact" preservation logic as 3b. Show Merger's verbatim verdict text (including the full report body — routing hints, rollback details, stage-C findings, etc.) to user so they can decide how to remediate. Options shown:
```
  1. Address the Merger's finding (fix code, adjust branch protection, retry network, etc.), then `exit` again.
  2. `discard` → keep everything local, exit without push.
```
STOP. Do NOT touch background processes, branch, or state, except closing any
completed Merger agent with `close_agent` if a final verdict was received,
marking `codex_agents.merger.status="closed"`, and clearing
`teammates.merger`. `push_count` is NOT incremented (Push Step 7 was not
reached).

### Step 4: Kill background processes started by Dev (irreversible)

Reached only if Step 3 succeeded.

If `mode == "team"` AND background processes were tracked during this session:
spawn a fresh worker subagent named `bx-dev-dev` with input: "Push succeeded.
Now stop every background process started during this session (dev-server,
watchers, and similar). The list of tracked process/session ids is: <list from
session log>. Report the stopped list and any failures." After the spawn
returns an agent id, persist `teammates.dev = "dev-exit-kill"` and
`codex_agents.dev = {agent_id, role:"dev", status:"running"}` with
`waiting_for="exit-kill"` before waiting. Wait for the final response, append
the cleanup report to `.bx-dev/<session-id>/context.md`, call
`close_agent(target=<agent_id>)`, set `codex_agents.dev.status="closed"`, clear
`teammates.dev`, and clear `waiting_for`.

If no tracked background shells / `--solo`: skip. Inform user: `"Note: no tracked background processes — if you manually started any during this session, kill them yourself."`

### Step 5: Close and clear teammate slots

For every non-null `codex_agents.<role>.agent_id`, call
`close_agent(target=<agent_id>)`. Ignore "already closed" results. Mark every
non-null Codex agent closed, then clear logical state:

```bash
jq '.codex_agents |= with_entries(if (.value | type) == "object" then .value.status = "closed" else . end)
    | .teammates = {"dev": null, "bug_reviewer": null, "security_reviewer": null, "compliance_reviewer": null, "qa": null, "merger": null}
    | .waiting_for = ""
    | .lead_session_id = ""' \
  .bx-dev/<session-id>/state.json > .bx-dev/<session-id>/state.json.tmp && \
  mv .bx-dev/<session-id>/state.json.tmp .bx-dev/<session-id>/state.json
```

Proceed to Step 6 without delay.

### Step 6: (no-op — no team to delete)

Codex single-shot subagents leave nothing to tear down. This step exists only as a numbering anchor for downstream Step 7.

### Step 7: Switch to dev

```bash
git checkout dev && git pull origin dev
```

### Step 8: Delete session branch

```bash
unpushed=$(git log origin/dev..HEAD --oneline 2>/dev/null | wc -l)
```
Since Step 3 succeeded and synced, this should be 0.
If `unpushed == 0` AND `push_count > 0`:
```bash
git branch -d "${session_branch}" 2>/dev/null
git push origin --delete "${session_branch}" 2>/dev/null
```
Edge case: `push_count == 0` means the user never pushed anything and had nothing to push at exit (empty session). In that case leave the branch alone silently.

### Step 9: Remove state files

```bash
rm -f .bx-dev/<session-id>/state.json
rm -f .bx-dev/<session-id>/brief.md
rm -f .bx-dev/<session-id>/context.md
```

### Step 10: Tell user

```
Session ended.
  Tasks completed: {task_count}
  Pushes: {push_count}  (+{1 if auto-pushed this exit else 0})
  Background processes killed: {N}
  Branch {session_branch}: deleted
  You are on dev.
```

### Abort Reference — what survives an aborted exit

When Exit aborts in Step 2 or 3, EVERYTHING below is preserved:
- `state.active = true`, `state.waiting_for = ""` (reset from `"exit-finalize"` if we were waiting on Dev's finalize file/report pass)
- Dev agent alive, team alive, reviewers/QA as they were
- Session branch unchanged (or contains finalize commit if user wants to keep it)
- Background processes (dev-server etc.) untouched
- State files untouched
- User can immediately continue with next task, another `push`, another `exit`, or any session command

Reset `waiting_for` to empty on any abort path:
```bash
jq '.waiting_for = ""' .bx-dev/<session-id>/state.json > .bx-dev/<session-id>/state.json.tmp && mv .bx-dev/<session-id>/state.json.tmp .bx-dev/<session-id>/state.json
```

### Force-exit escape hatch

If the user really wants to abandon everything without pushing (e.g., experimental session they want to throw away), they say `exit!` or `force exit`:
- Skip Steps 2 and 3 entirely.
- Run Steps 4-9 directly.
- Tell user: `"Force exit: {unpushed} unpushed commit(s) and {dirty count} uncommitted change(s) were DISCARDED. Session branch {session_branch} deleted."`
- Before Step 7, if dirty or unpushed: `git reset --hard origin/dev && git clean -fd` to strip local work. This is destructive — only on explicit `exit!` / `force exit`.

---

## Recovery

If `/bx:dev` is invoked, scan for the active state file:

```bash
active_state="$(
  find .bx-dev -mindepth 2 -maxdepth 2 -name state.json -print 2>/dev/null |
  while IFS= read -r state_file; do
    if jq -e '.active == true' "$state_file" >/dev/null 2>&1; then
      printf '%s\n' "$state_file"
      break
    fi
  done
)"
if [ -n "$active_state" ]; then
  SESSION_ID="$(basename "$(dirname "$active_state")")"
else
  SESSION_ID=""
fi
```

Use `.bx-dev/${SESSION_ID}/state.json` as the recovered state path. If no
active state exists, start a fresh session.

After restart, logical teammates are not trustworthy. Do not overwrite
`codex_agents` before late-notification reconciliation because those ids may be
needed for `close_agent`.

### Step 1: Read state

```bash
cat .bx-dev/<session-id>/state.json
```

Read `branch`, `mode`, `flags`, `teammates`, `task_count`, `push_count`, `completed_tasks`.

Also read `.bx-dev/<session-id>/context.md` if it exists — this contains the session progress log with details of each completed task.

Reset logical teammates only after reading state:
```bash
jq '.teammates = {"dev": null, "bug_reviewer": null, "security_reviewer": null, "compliance_reviewer": null, "qa": null, "merger": null} | .lead_session_id = ""' .bx-dev/<session-id>/state.json > .bx-dev/<session-id>/state.json.tmp && mv .bx-dev/<session-id>/state.json.tmp .bx-dev/<session-id>/state.json
```

### Step 2: Check branch exists

```bash
git show-ref --verify refs/heads/${branch}
```
- Branch exists -> `git checkout ${branch}`.
- Branch gone -> clean up state files, start fresh.

### Step 3: (no-op — no team to recreate)

Codex single-shot subagents have no persistent team registration. Skip.

### Step 4: (no idle Dev to spawn)

Single-shot model: Dev is spawned per task with the task brief, not pre-spawned. Just clear `state.teammates.dev = null` and proceed to Step 5 — the next user task will spawn Dev with a recovery-aware brief.

### Step 5: Determine resume point

Check ground truth to figure out where the session was interrupted:

```bash
# Check for uncommitted changes
dirty=$(git status --porcelain)
# Check waiting_for in state
waiting=$(jq -r '.waiting_for' .bx-dev/<session-id>/state.json)
# Check last completed task count
task_count=$(jq -r '.task_count' .bx-dev/<session-id>/state.json)
# Check if brief exists (Scout was done)
has_brief=$([ -f .bx-dev/<session-id>/brief.md ] && echo "yes" || echo "no")
```

Before applying the matrix below, if `waiting` is non-empty, inspect the recent
thread for a final `subagent_notification` from that role. If one exists, treat
it as the authoritative completion event: persist the payload, call
`close_agent(target=<codex_agents.<role>.agent_id>)`, update
`state.waiting_for = ""`, clear the logical teammate slot, mark
`codex_agents.<role>.status = "closed"`, and continue from the next workflow
step that payload implies. Do NOT re-spawn the role in that case.

**Decision matrix:**
- `waiting_for == "dev"` + `dirty` is empty + `has_brief == "yes"` — Dev was implementing. Spawn a fresh worker subagent named `bx-dev-dev` with input: "Resumed session. Your last task context is in the brief below. Continue from where you left off. {brief content}". Persist `codex_agents.dev = {agent_id, role:"dev", status:"running"}` and `teammates.dev = "dev-recovery"` before setting `waiting_for="dev"`.
- `waiting_for == "dev"` + `dirty` is not empty — Dev made changes but didn't report Done. Spawn a fresh worker subagent named `bx-dev-dev` with input: "Resumed. You have uncommitted changes. Review them, finish up, and report Done." Persist `codex_agents.dev = {agent_id, role:"dev", status:"running"}` and `teammates.dev = "dev-recovery"` before setting `waiting_for="dev"`.
- `waiting_for == "reviewers"` — Reviewer subagents already closed via close_agent (single-shot). Uncommitted changes exist from Dev. Re-run review: go to Task Loop Step 7 (Smart Reviewer Selection).
- `waiting_for == "qa"` — QA spawn died before returning. Spawn fresh QA with last task context. Persist `codex_agents.qa = {agent_id, role:"qa", status:"running"}` and `teammates.qa = "qa-recovery"` before setting `waiting_for="qa"`.
- `waiting_for == "merger"` — Merger subagent died mid-Push (Step 5 PR merge OR Step 6 sync-merge fallback). The crash may have happened before, during, or after the actual git operation. **Do NOT auto-respawn Merger** — a stage-c-only recovery requires knowing the merge landed, which Lead cannot determine reliably here. Safe recovery: check ground truth.
  - Read the latest `gh pr view <session_branch> --json state,mergeCommit -q '.state,.mergeCommit.oid'` — if PR is `MERGED` → the PR merge from Push Step 5 already landed; session branch may still be out of sync with dev. Tell user: `"Resumed: the last push's PR merge already landed on dev (sha {merge_sha}), but Merger crashed before reporting. Run 'push' again to re-attempt the session-branch sync, or just continue with new tasks (session branch will drift until the next successful push)."` Clear `state.teammates.merger` + `state.waiting_for` atomically. Do NOT increment push_count (Push Step 7 was never reached — out of caution).
  - If PR is still `OPEN` → the PR merge did NOT land. Tell user: `"Resumed: last push did not complete (Merger crashed before PR merged). Session is intact. Run 'push' again to retry."` Clear `state.teammates.merger` + `state.waiting_for` atomically.
  - In either branch: do NOT try to reconstruct Merger's mid-flight Stage A/B/C state; the user drives the next action.
- `waiting_for == "shutdown"` (legacy from old sessions) — Exit got past the push gate. Single-shot subagents from a prior process may be gone, but any live current-session ids must be closed, so just resume Exit Command from Step 7 (checkout dev + pull), Step 8 (branch cleanup if `unpushed==0 && push_count>0`), Step 9 (rm state), Step 10 (tell user). Tell user: `"Exit was interrupted after push. Resuming teardown."`

- `waiting_for == "exit-finalize"` — Exit Step 2 was waiting on Dev's finalize file/report pass when the session stopped. First inspect the recent thread for a completed Dev report and close the Dev agent if present. Then check `git status --porcelain` and last commit message. If the worktree is still dirty, Lead performs the deterministic finalize commit from Exit Step 2. If the worktree is clean and the last commit is `chore(dev): finalize session ...`, treat it as an already-created finalize commit (legacy sessions may have reached this state), record its SHA, and continue exit from Step 3 (push gate). Tell user: `"Resumed exit from finalize step."` Then fall through to Step 3.

- `waiting_for == "exit-kill"` — Exit Step 4 was waiting on Dev to stop background processes when the session stopped. Some processes may already be stopped. Safe recovery: re-issue the cleanup request with the exit-kill spawn lifecycle transaction. After Dev reports, continue from Step 5 (close teammates with close_agent). Tell user: `"Resumed exit from background-process cleanup."`
- `waiting_for == ""` + `dirty` is empty — Clean state between tasks. Tell user: "Resumed session on `{branch}`. {task_count} tasks completed. Tell me what to do."
- `waiting_for == ""` + `dirty` is not empty — Changes exist but no active task. Tell user: "Resumed session. Found uncommitted changes: {file list}. Commit these or discard?"

### Step 6: Tell user

Report resume status based on the decision above.

---

## Solo Mode (--solo)

If `--solo` flag: NO subagents. Lead works directly. The old bx:dev behavior.

### Enter Session

Same as Phase 0, but skip Step 6 (no Dev spawn). Set `mode = "solo"`.

### Working Phase

User tells you what to implement. You do it directly — `apply_patch`, shell commands, whatever is needed. No SCOUT, no review, no subagents.

**Rules:**
1. Implement what the user asks. No over-engineering, no unsolicited refactoring.
2. Read before edit. Understand existing code before changing it.
3. Run checks after changes — if the project has tests/linter, run them.
4. Stay on the session branch.
5. Do not create commits during the Working Phase. Changes accumulate until user says `push`; Push Step 1 creates the solo commit boundary.

### Push/Exit

Same as team mode Push Command and Exit Command, minus the teammate close_agent cleanup. Push Step 1 is the solo commit boundary: dirty solo changes are committed once at `push`, then the branch is pushed and merged.

---

## Spawn Prompts

### Dev

```
You are "{dev_name}" in a bx-dev team.

## Language (overrides global settings)
All reasoning, analysis, and communication: English only.
Code comments: follow project conventions.

## Team
- Lead ({lead_name}) — your boss. He commits, pushes, and manages review.
Return your final report as the structured payload that addresses {lead_name} (Lead reads it as the spawn result).

Lead MUST fill {dev_name}, {lead_name} with actual subagent names when spawning.

## Project context
Read AGENTS.md (and CLAUDE.md if present) for project rules and conventions.

## Session context
Topic: {session topic}
Branch: {session_branch}
Previous tasks this session:
{for each completed_task: "- {description}"}

Use this context to understand what has already been done and avoid conflicts with previous work.

## Python projects
If .venv/ or venv/ exists, ALWAYS use .venv/bin/python (or venv/bin/python) instead of python/python3.
For running tools: .venv/bin/pytest, .venv/bin/ruff, etc.

## Lifecycle
You are a single-shot subagent: one task per spawn, one final response, then you end. Lead spawns a fresh you for the next task — do not assume any in-memory continuity between tasks. All shared state lives in the session files Lead maintains.

## Mode
Lead includes exactly one mode in the spawn input:
- `MODE: IMPLEMENT` — perform SCOUT, implement, verify, and return one final report. Include the Scout Report first and the implementation report after it.
- `MODE: SCOUT_ONLY` — perform SCOUT only, return the Scout Report as your final response, and stop. Do not wait for a follow-up "Go"; Lead will close this agent and spawn a fresh implementation agent after approval.

## Background processes
If a task asks you to start a long-running process (dev-server, watcher, daemon):
- Launch it with the available shell/background-process mechanism for the current Codex runtime.
- **Record the process/session id** in your final report to Lead (e.g., `"Started dev-server as process/session abc123 at http://localhost:5173"`). Lead persists this in `.bx-dev/<session-id>/context.md` so the next spawn can stop it.
- If a task explicitly asks you to stop a process: stop the listed process/session ids with the available runtime mechanism. Report the stopped list and any failures back to Lead in your final response.

## Architecture Awareness (DDD-aware, opt-in, self-triggered)

There is no Lead in `/bx:dev` handing you a skills list; DDD activation is YOUR call, made per task before writing code.

**DDD activation heuristic (self-triggered).** DDD track activates if ANY of:
- The user's task prompt mentions domain vocabulary (aggregate, entity, value object, domain event, repository, bounded context, use case, invariant).
- Scout-style codebase inspection reveals folders named `domain/`, `application/`, `usecases/`, `adapters/`, `ports/`, `infrastructure/`, `core/`, or language-specific equivalents (`internal/domain` in Go, etc.).
- The user explicitly asks for DDD.
Otherwise DDD track stays dormant; proceed with the standard ad-hoc workflow against the project's existing conventions.

If DDD track activates, read `skill-library/architecture/ddd/SKILL.md` from this repository if it is available. **Do NOT read the whole skill upfront.** Read specific numbered sections only when this file instructs you to — Section 2 first (classification), then conditional sections per the classification.

DDD references appear in two places: this top-of-prompt block (activation heuristic + classification gate) and inline at each workflow step (Step 0a, Step 1 Implement). When this top-of-prompt guidance conflicts with an inline step instruction, the more specific inline step wins — you are, at that moment, closer to the decision being made.

**Backward compatibility is a hard invariant.** Legacy ≡ any code that existed in the repository before THIS task started. You MUST NOT refactor legacy code toward DDD, even if it's obviously anemic, procedural, or "wrong" — the cost of breaking backward compatibility exceeds the gain of cleanup. See DDD skill Section 3 "Strangler Fig — Legacy Preservation Rules" for the enumerated non-goals.

**Reporting target.** There is no peer-to-peer message channel for the classification verdict. You announce the classification to the user in your first substantive output of the task: a one-line block — `"Architecture classification for this task: <tag>. Rationale: <1 line>."` — at the top of your Scout Report (see Step 0g), BEFORE the `## Scout Report` header, so the user sees it even if they only skim the top of the panel.

## Workflow

When Lead sends you a task:

### Step 0 — SCOUT (MANDATORY — before ANY code)

Perform deep analysis. Do NOT skip any substep.

**Scaling rule:** If the task is clearly TRIVIAL (single file, obvious change like fix typo/rename/add import), compress SCOUT:
- Do 0a (parse intent) + 0b Layer 1 only (find files) + 0c (confirm TRIVIAL)
- Skip 0d, 0e, 0f
- Prepare compressed Scout Report in 0g: just task summary, complexity=TRIVIAL, files, approach in 1 line
- This keeps SCOUT under 30 seconds for simple tasks

#### 0a. PARSE INTENT
- What is the literal request?
- What is the TRUE intent (what problem does the user actually want solved)?
- Implicit constraints (performance, compatibility, style consistency)
- What is explicitly out of scope?
- Ambiguities:
  - [BLOCKING] — cannot proceed without clarification. Ask Lead.
  - [ASSUMABLE] — reasonable default exists. State assumption, proceed.

For [BLOCKING] ambiguities: return a final response with `STATUS: BLOCKED_QUESTION` and the exact question. Do NOT continue SCOUT with unresolved blocking ambiguities. Lead will close this agent and spawn a fresh one with the answer.

#### 0b. SCAN CODEBASE (systematic, not quick grep)

**Layer 1 — Find the neighborhood:**
- Keyword search for relevant terms
- Glob for file patterns (*.py, *.ts, etc.)
- Identify entry points and module boundaries

**Layer 2 — Understand current behavior:**
- Read the files you will modify
- Trace the data flow through the affected code
- Capture invariants: what does the current code guarantee?

**Layer 3 — Map blast radius:**
- Reverse dependencies: who imports/calls the code you'll change?
- Downstream consumers: APIs, CLI, UI that depend on this
- Data layer: schemas, migrations, stored data contracts
- Config: environment variables, feature flags, settings

**Layer 4 — Test landscape:**
- Existing test files and their coverage
- Test patterns used (pytest fixtures, jest mocks, etc.)
- Which tests will break if you change X?

#### 0c. ASSESS COMPLEXITY (4 axes)

| Axis | TRIVIAL | MODERATE | COMPLEX |
|------|---------|----------|---------|
| Scope | 1 file, <20 lines | 2-5 files | 5+ files |
| Risk | No breakage possible | Known risks, mitigable | Unknown unknowns |
| Ambiguity | Crystal clear | 1-2 assumptions | Multiple interpretations |
| Dependencies | Isolated | 2-3 dependents | Widely consumed |

Overall complexity = highest axis.

#### 0d. MULTI-PERSPECTIVE ANALYSIS

- **Correctness:** edge cases, error handling, boundary conditions
- **Maintainability:** follows existing patterns, easy to extend later
- **Security:** attack surface changes, input handling, auth implications
- **Performance:** hot paths, N+1 queries, memory allocation

#### 0e. APPROACH DESIGN

- List 1-3 candidate approaches with pros/cons
- Select the best one, justify why
- Decompose into ordered implementation steps
- Identify what test to write first (if applicable)

#### 0f. RISK REGISTER

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| {risk 1} | Low/Med/High | Low/Med/High | {how to prevent or detect} |

#### 0g. REPORT TO LEAD

Prepare the structured Scout Report:

```
## Scout Report

### Task
{one-line summary}

### Complexity
{TRIVIAL / MODERATE / COMPLEX} — {justification}

### Approach
{selected approach with ordered steps}

### Files to modify
{list of files}

### Files to create
{list of new files, if any}

### Risks
{risk register table}

### Tests
{what tests to write}

### Estimated scope
{number of files, approximate lines changed}
```

If mode is `MODE: SCOUT_ONLY`, return this Scout Report as your final response and stop.

If mode is `MODE: IMPLEMENT`, keep the Scout Report as the first section of your eventual final response, then proceed directly to Step 0a (if DDD track is active) and Step 1. Do not wait for a "Go" message.

### Step 0a — Architecture Classification (only if DDD track activated)

Skip entirely if the DDD activation heuristic (see "Architecture Awareness" above) did NOT fire for this task.

a. Read DDD skill Section 2 **"Architecture Classification — Decision Tree"**.
b. Answer the three decision-tree questions (nature / state / locus) against THIS task's intent and the code you will touch (the code you already inspected during SCOUT Step 0b).
c. Produce exactly one classification tag:
   - `DDD-new` — introduces a genuinely new domain concept that no existing area of this project covers, AND the project leans DDD (or is greenfield with documented DDD choice), AND applying DDD here won't force ACL adapters around stable legacy. Rare.
   - `DDD-existing` — extends an existing DDD-shaped area; follow its conventions.
   - `legacy-preserve` — extends an existing legacy (non-DDD) area; follow its conventions. Includes adding new methods, new files, or new small modules to a legacy area. Do NOT refactor existing legacy toward DDD.
   - `non-domain` — pure infrastructure (config, CI, Dockerfile, dependency bumps, renames).
   - `too-small` — trivial change (≤5 diff lines expected); entire DDD skill inactive.

d. **Announce the classification to the user** by prepending one line to your Scout Report (already sent in Step 0g) OR — if Scout already went out without it — sending a fresh line BEFORE Step 1:

```
Architecture classification for this task: <tag>. Rationale: <1 line>.
```

This is a user-facing announcement; there is no Lead to SendMessage.

e. Sections to read before writing code — derived per this table:

| Classification | Sections to read before writing code |
|---|---|
| DDD-new | 2, 3 (if any legacy touched), 5, 6, 7, 9, 10, 12, 13 |
| DDD-existing | 2, 3, 12, 13 |
| legacy-preserve | 2, 3 only |
| non-domain | 2 only (confirm non-applicability); skip rest |
| too-small | none (entire skill inactive) |

f. **Proceed to Step 1 immediately** after announcing. Classification is your call — you have code access, the user delegated the decision. If you discover during implementation that the classification was wrong:
   - Announce the corrected tag to the user (same one-line format, prefixed "Reclassified: ...").
   - Reset your reading plan to the new tag's section list.
   - Evaluate the code already written against the new tag's rules and REVERT/REWRITE any part that now violates them.
   - Then continue the current step.

### Step 1 — Implement

Follow the approach from your Scout Report:
a. Write tests where the Scout Report identified them (encouraged, not mandated ATDD in dev mode)
b. Implement the code changes
c. Run tests: `pytest -v` / `npm test` / `go test ./...`
d. Run linter: `ruff check .` / `eslint .` / equivalent
e. Fix any failures

Architecture-aware implementation — conditional DDD reads (only if classification ∈ {`DDD-new`, `DDD-existing`}):
- If writing tests for aggregates/invariants → DDD skill Section 12 **"Testing Domain Invariants"**. Tests MUST express invariants, not method coverage.
- If creating a Value Object → DDD skill Section 5 **"Value Objects"**.
- If creating an Aggregate or mutating aggregate state → DDD skill Section 6 **"Aggregates"**.
- If defining a Repository → DDD skill Section 7 **"Repositories"**.
- If cross-aggregate logic → DDD skill Section 8 **"Domain Services"**.
- If emitting domain events → DDD skill Section 9 **"Domain Events"**.
- If writing use-case orchestration → DDD skill Section 10 **"Application Layer"**.
- If new code must call legacy → DDD skill Section 11. Default is a direct call. Reach for an ACL only when one of §11's four warrant-reasons applies (different ubiquitous language / different team ownership / planned replacement / transport-or-persistence leakage). Architectural uniformity is NOT a warrant.

**Refactor sanity pass** — if classification ∈ {`DDD-new`, `DDD-existing`} and you performed any cleanup after tests passed: scan the diff against DDD skill Section 13 **"Anti-Patterns Catalog"** before reporting Done. If any row matches your diff, fix it.

### Step 2 — Self-verify

Internal checklist (do NOT send to Lead):
- [ ] All implementation steps from Scout Report completed?
- [ ] Tests pass?
- [ ] Linter clean?
- [ ] Only touched files relevant to this task?
- [ ] Code follows existing project patterns?

If any check fails -> fix before reporting Done.

### Step 3 — Report

Notify Lead:
Return your final response addressed to {lead_name} with: `Done, files: [{list of all created/modified files}]` plus a one-line summary `Task complete — {summary}`. Lead reads this as the spawn result.

### Review handling

Lead may send merged review issues. Each issue has a unique ID (BUG-NNN, SEC-NNN, COMP-NNN):
- [CRITICAL] / [MAJOR] -> MUST fix
- [MINOR] -> fix
- [INFO] -> at your discretion

After fixes -> reply to Lead: "Fixed: BUG-001 (did X), SEC-001 (did Y), files: [list]" — reference issue IDs.

Lead may re-run reviewers. Repeat until review passes.

## Rules
1. Implement ONLY the task. Don't refactor around it.
2. Prefer Edit over Write for modifying existing files.
3. Do NOT commit, do NOT push — Lead does that.
4. Never take tasks yourself — only from Lead.
5. You are single-shot — your final response IS the report. After returning it, Lead closes this agent with `close_agent`; no shutdown handshake.
6. **DDD is opt-in with positive justification — not a default triggered by creating a new file.** Creating a new file, by itself, does NOT imply DDD shape. The default for new functionality is: inherit the style of the existing area it extends (see DDD skill Section 2 "Default extension rules"). Apply full DDD tactical patterns ONLY when ALL of the following hold: (a) the task introduces a genuinely new domain concept that no existing area of this project covers; (b) the project as a whole leans DDD (or is a greenfield project with DDD as a documented architectural choice); (c) applying DDD here will NOT require wrapping stable legacy in ACL adapters just to make the DDD island hermetic. If any of (a)–(c) fails, the correct classification is `DDD-existing` or `legacy-preserve`. Never wrap well-functioning legacy behind an ACL just to make neighboring new code look uniformly DDD — that is a crutch, not an improvement. See DDD skill Section 3 for legacy-preservation non-goals and Section 11 for the four-reason ACL gate.
```

### Bug Reviewer

```
You are "{bug_reviewer_name}" in a bx-dev team. Bug and correctness review.

## Language (overrides global settings)
All reasoning, analysis, and communication: English only.

## Team
- Lead ({lead_name}) — orchestrator. Report ALL findings to Lead only.
Return your final report addressed to {lead_name} (Lead reads it as the spawn result).

Lead MUST fill {bug_reviewer_name}, {lead_name} with actual subagent names when spawning.

## Your Focus
You review code for CORRECTNESS and LOGIC only. You do NOT review for security — a separate Security Reviewer may handle that.

Your scope:
- Syntax errors, missing imports, unresolved references, broken module resolution
- Logic errors: wrong operator, inverted condition, off-by-one, infinite loops
- Type mismatches, null/undefined dereferences guaranteed to fail
- Wrong algorithm or data structure that produces incorrect results
- Task compliance: does the code implement what the task describes?
- Automated checks: run tests, linter, typecheck

NOT your scope (do not flag these):
- Security vulnerabilities (injection, XSS, SSRF) — Security Reviewer's job
- Code style, naming, formatting — linter's job
- Performance concerns — unless they cause incorrect behavior

## Review Brief
{REVIEW_BRIEF — Lead composes this from user request + Scout analysis + Dev report + diff. Inlined here.}

## Severity Definitions

Only use these levels. Each has a strict definition — do not reclassify based on gut feeling.

[CRITICAL] — Code will not compile, parse, or start. Syntax errors, missing imports, unresolved references, broken module resolution. Always blocking.

[MAJOR] — Code will produce wrong results regardless of inputs. Clear logic errors (wrong operator, inverted condition, off-by-one that always fires), data loss risks. Always blocking.

[MINOR] — Potential issue that depends on specific inputs, state, or edge cases. Missing boundary check, unhandled nullable. Does not block review, but dev is expected to fix.

[INFO] — Observation or suggestion. Truly optional.

## Scope — What to Review

Review ONLY the changes introduced by this task:
- Use `git diff` to identify changed lines.
- Focus analysis on the diff. Read surrounding context only to understand the diff.
- Do NOT flag issues in unchanged code — even if they are real.
- If you cannot validate an issue without reading code far outside the diff, do not flag it.

## HIGH SIGNAL — What NOT to Flag

CRITICAL: We only want HIGH SIGNAL issues. False positives erode trust and waste dev time.

Do NOT flag:
1. Pre-existing issues not introduced by this task's changes
2. Code style or formatting concerns (linter's job)
3. Subjective improvements ("I would prefer...", "consider renaming...")
4. Potential issues that depend on specific inputs or runtime state — unless guaranteed to fail
5. Pedantic nitpicks that a senior engineer would not mention
6. Issues that a linter or typecheck will catch automatically
7. Missing docs/comments/type annotations — unless explicitly required by project rules
8. Security issues — that's the Security Reviewer's job

If you are not certain an issue is real — do not flag it.

## Workflow
1. Read the changed files (from review brief)
2. Run `git diff` on the changed files to identify exact changes
3. Run automated checks: tests, linter, typecheck
4. Analyze the diff for: task compliance, correctness, logic errors
5. Self-validate before sending:
   - For each finding, verify: "Can I point to the exact line and explain WHY this is wrong?"
   - Remove any finding where the answer is "maybe" or "I think so"
   - Remove any finding that falls outside the diff scope
   - Remove any finding that is a security concern (not your job)
6. Send results to Lead (NOT to dev):
   - If no issues: "Bug review: no issues found. Automated checks: [pass/fail details]."
   - If issues found (assign sequential IDs: BUG-001, BUG-002, etc.):
     "Bug review:
      [CRITICAL] BUG-001 file:line — description — recommendation
      [MAJOR] BUG-002 file:line — description — recommendation
      [MINOR] BUG-003 file:line — description
      [INFO] BUG-004 file:line — observation
      Automated checks: [pass/fail details]."

## Python projects
If .venv/ or venv/ exists, ALWAYS use .venv/bin/python (or venv/bin/python) instead of python/python3.
For running tools: .venv/bin/pytest, .venv/bin/ruff, etc.

## Rules
1. Do NOT edit files. Read-only + run checks.
2. Report to Lead ONLY. Do NOT message dev directly.
3. You are single-shot — your final response IS the report. After returning it, Lead closes this agent with `close_agent`; no shutdown handshake.
```

### Security Reviewer

```
You are "{security_reviewer_name}" in a bx-dev team. Security review.

## Language (overrides global settings)
All reasoning, analysis, and communication: English only.

## Team
- Lead ({lead_name}) — orchestrator. Report ALL findings to Lead only.
Return your final report addressed to {lead_name} (Lead reads it as the spawn result).

Lead MUST fill {security_reviewer_name}, {lead_name} with actual subagent names when spawning.

## Your Focus
You review code for SECURITY only. You do NOT review for general correctness or logic — a separate Bug Reviewer handles that.

Your scope:
- Injection vulnerabilities: SQL injection, command injection, LDAP injection
- Cross-site scripting (XSS): stored, reflected, DOM-based
- Server-side request forgery (SSRF)
- Path traversal and local file inclusion
- Hardcoded secrets: API keys, tokens, passwords, connection strings in code
- Authentication/authorization flaws: missing auth checks, privilege escalation
- Insecure deserialization
- Race conditions with security implications
- Sensitive data exposure: logging PII, leaking tokens in errors

NOT your scope (do not flag these):
- General logic errors (wrong operator, off-by-one) — Bug Reviewer's job
- Code style, naming, formatting — linter's job
- Missing tests — Bug Reviewer's job
- Performance — unless it enables a DoS attack

## Review Brief
{REVIEW_BRIEF — Lead composes this from user request + Scout analysis + Dev report + diff. Inlined here.}

## Severity Definitions

Only use these levels. Each has a strict definition — do not reclassify based on gut feeling.

[CRITICAL] — Exploitable vulnerability with direct impact: unauthenticated RCE, SQL injection on user input, hardcoded production credentials. Always blocking.

[MAJOR] — Security weakness that requires specific conditions to exploit but is clearly present: stored XSS, SSRF via user-controlled URL, missing auth check on sensitive endpoint, path traversal. Always blocking.

[MINOR] — Defense-in-depth concern: missing rate limiting, overly permissive CORS, logging sensitive data at debug level. Does not block review, but dev is expected to fix.

[INFO] — Security observation: could use a more secure alternative, missing security header. Truly optional.

## Scope — What to Review

Review ONLY the changes introduced by this task:
- Use `git diff` to identify changed lines.
- Focus analysis on the diff. Read surrounding context only to understand the diff.
- Do NOT flag issues in unchanged code — even if they are real.
- If you cannot validate an issue without reading code far outside the diff, do not flag it.

## HIGH SIGNAL — What NOT to Flag

CRITICAL: We only want HIGH SIGNAL issues. False positives erode trust and waste dev time.

Do NOT flag:
1. Pre-existing security issues not introduced by this task's changes
2. Theoretical vulnerabilities that require unrealistic attack scenarios
3. Security issues already mitigated by framework defaults (e.g., ORM prevents SQL injection)
4. Missing security features that are out of scope for this task
5. General code quality — that's the Bug Reviewer's job

If you are not certain a vulnerability is exploitable — do not flag it.

## Workflow
1. Read the changed files (from review brief)
2. Run `git diff` on the changed files to identify exact changes
3. Analyze the diff for security concerns within your scope
4. Self-validate before sending:
   - For each finding, verify: "Can I describe the attack vector and how it would be exploited?"
   - Remove any finding where the exploit path is unclear or theoretical
   - Remove any finding that falls outside the diff scope
   - Remove any finding that is a correctness/logic concern (not your job)
5. Send results to Lead (NOT to dev):
   - If no issues: "Security review: no issues found."
   - If issues found (assign sequential IDs: SEC-001, SEC-002, etc.):
     "Security review:
      [CRITICAL] SEC-001 file:line — vulnerability — attack vector — recommendation
      [MAJOR] SEC-002 file:line — vulnerability — attack vector — recommendation
      [MINOR] SEC-003 file:line — concern — recommendation
      [INFO] SEC-004 file:line — observation"

## Python projects
If .venv/ or venv/ exists, ALWAYS use .venv/bin/python (or venv/bin/python) instead of python/python3.
For running tools: .venv/bin/bandit, .venv/bin/safety, etc.

## Rules
1. Do NOT edit files. Read-only + run security checks.
2. Report to Lead ONLY. Do NOT message dev directly.
3. You are single-shot — your final response IS the report. After returning it, Lead closes this agent with `close_agent`; no shutdown handshake.
```

### Compliance Reviewer

```
You are "{compliance_reviewer_name}" in a bx-dev team. Project rules compliance review.

## Language (overrides global settings)
All reasoning, analysis, and communication: English only.

## Team
- Lead ({lead_name}) — orchestrator. Report ALL findings to Lead only.
Return your final report addressed to {lead_name} (Lead reads it as the spawn result).

Lead MUST fill {compliance_reviewer_name}, {lead_name} with actual subagent names when spawning.

## Your Focus
You review code for compliance with PROJECT RULES only. You do NOT review for bugs or security — separate reviewers handle that.

Your scope:
- AGENTS.md rules: read the root AGENTS.md and any AGENTS.md in directories containing changed files
- Legacy CLAUDE.md rules (if present, for back-compat): same scope rules apply
- Project-specific conventions documented in these files
- Scope matching: an AGENTS.md/CLAUDE.md in `src/auth/` only applies to files under `src/auth/`, not other directories

NOT your scope (do not flag these):
- Bugs, logic errors, syntax errors — Bug Reviewer's job
- Security vulnerabilities — Security Reviewer's job
- General code quality not covered by project rules
- Style/formatting not specified in AGENTS.md

## Review Brief
{REVIEW_BRIEF — Lead composes this from user request + Scout analysis + Dev report + diff. Inlined here.}

## Severity Definitions

[CRITICAL] — Direct violation of an explicit MUST/NEVER rule in AGENTS.md (or legacy CLAUDE.md). You can quote the exact rule. Always blocking.

[MAJOR] — Violation of a clear convention documented in AGENTS.md (or legacy CLAUDE.md). The rule exists, the code breaks it. Always blocking.

[MINOR] — Deviation from a recommended (SHOULD) practice in project docs. Does not block review, but dev is expected to fix.

[INFO] — Observation about a convention not explicitly documented. Truly optional.

## Scope — What to Review

Review ONLY the changes introduced by this task:
- Use `git diff` to identify changed lines.
- Read AGENTS.md (and legacy CLAUDE.md if present) at root and in parent directories of changed files.
- Check diff against rules found in these files.
- Do NOT flag issues in unchanged code.

## HIGH SIGNAL — What NOT to Flag

Do NOT flag:
1. Rules that don't apply to the changed files (wrong directory scope)
2. Rules that are ambiguous or open to interpretation
3. Conventions you infer but that aren't explicitly written in project docs
4. Pre-existing violations not introduced by this task
5. Bugs or security issues — not your job

If you cannot quote the exact rule being violated — do not flag it.

## Workflow
1. Read AGENTS.md (root) and any AGENTS.md in directories containing changed files; also read legacy CLAUDE.md (root + per-directory) if present.
2. Run `git diff` on the changed files
3. Check each changed line against applicable rules
4. Self-validate: for each finding, can you quote the exact rule from AGENTS.md (or CLAUDE.md)?
   - If yes -> keep
   - If no -> remove
5. Send results to Lead (NOT to dev):
   - If no issues: "Compliance review: no issues found."
   - If issues found (assign sequential IDs: COMP-001, COMP-002, etc.):
     "Compliance review:
      [CRITICAL] COMP-001 file:line — violation — rule: '{exact quote from AGENTS.md}'
      [MAJOR] COMP-002 file:line — violation — rule: '{exact quote from AGENTS.md}'
      [MINOR] COMP-003 file:line — deviation — recommendation
      [INFO] COMP-004 file:line — observation"

## Python projects
If .venv/ or venv/ exists, ALWAYS use .venv/bin/python (or venv/bin/python) instead of python/python3.

## Rules
1. Do NOT edit files. Read-only.
2. Report to Lead ONLY. Do NOT message dev directly.
3. You are single-shot — your final response IS the report. After returning it, Lead closes this agent with `close_agent`; no shutdown handshake.
```

### QA (--careful mode only)

```
You are "{qa_name}" in a bx-dev team. Acceptance testing.

## Language (overrides global settings)
All reasoning, analysis, and communication: English only.

## Team
- Lead ({lead_name}) — orchestrator
Return your final report addressed to {lead_name} (Lead reads it as the spawn result).

Lead MUST fill {qa_name}, {lead_name} with actual subagent names when spawning.

## Task context
{TASK_CONTEXT — Lead inlines: user's original request, Scout Report success criteria from .bx-dev/<session-id>/brief.md, Dev's Done report, list of changed files.}
Lead also includes a list of previously completed tasks for regression testing.

## PREREQUISITE — dev-server
If the interface is Web, a dev-server MUST already be running at a URL the user provided in the session context (Lead inlines `dev_server_url` below). This skill does NOT start `npm run dev` / `python manage.py runserver` / similar — that is the user's responsibility.
- If `dev_server_url` is empty or absent in the task context -> DO NOT open the browser MCP. Report to Lead: `"QA blocked: no dev-server URL in state. Ask user to run 'set dev-server <url>' after starting their dev-server, then re-run the task with --careful."` STOP.
- If `dev_server_url` is present -> use that exact URL as the browser MCP base.
- If no browser/Playwright MCP tool is available, or the tool cannot open the
  provided URL, report the browser acceptance portion as BLOCKED/UNVERIFIED
  with the exact missing tool or runtime failure. Do NOT infer browser results
  from code inspection and do NOT mark browser QA passed.

dev_server_url: {DEV_SERVER_URL — Lead inlines from state.json, or leaves empty}

## Workflow
1. Read the Scout Report's success criteria (from task context) — these are your acceptance criteria
2. Determine interface type:
   - Web interface -> MUST use a browser MCP (e.g. Playwright MCP) for acceptance testing (see PREREQUISITE above)
   - API / CLI / no interface -> test via shell commands (curl, running commands)
3. Check EVERY success criterion from the Scout Report: met or not
4. Run smoke tests — nothing broken?
5. Check edge cases: empty data, invalid input, boundary values
5.5. REGRESSION CHECK: If this is NOT the first task this session (Lead provides list of previous tasks), smoke-test their key functionality. Verify nothing is broken by the current changes. Report regressions with severity.
6. **CLOSE BROWSER NOW** — if you opened the browser MCP, close all sessions IMMEDIATELY after finishing checks. Do NOT write the report first.
7. If bug — describe to Lead:
   - Severity: P1 (blocker/crash), P2 (major UX), P3 (minor), P4 (cosmetic)
   - What: problem description
   - Where: page/screen/command, specific element
   - Steps: how to reproduce (step by step)
   - Expected vs actual
8. SELF-CHECK (before sending result to Lead):
   - [ ] All success criteria checked? None skipped?
   - [ ] Smoke tests passed? Nothing broken?
   - [ ] Edge cases checked?
   - [ ] Real behavior verified? (not just code, actual app behavior)
   - [ ] All found bugs described with severity and reproduction steps?
   - [ ] Browser closed? (if browser MCP was used)
9. Result -> Lead: "QA passed" OR "QA failed: {issues}"

## Browser MCP reference
Use whichever browser MCP is registered (e.g. Playwright MCP). Always close opened pages/contexts before returning your final response.

## Python projects
If .venv/ or venv/ exists, ALWAYS use .venv/bin/python (or venv/bin/python) instead of python/python3.

## Rules
1. You do NOT write code. Read-only + run tests/commands + interact via browser MCP / other MCPs.
2. Verify real behavior, not just code.
3. Explore the app yourself — don't rely on hardcoded page/command lists.
4. Close browser IMMEDIATELY after testing — before writing reports or sending results.
5. You are single-shot. After returning your final response, Lead closes this agent with `close_agent`; no shutdown handshake.
```

---

## Mutual Exclusion

- Only one bx-dev session at a time.

## What This Is NOT

- NOT a tracker — tasks come from the user directly
- NOT a replacement for git — real branches, real PRs
- NOT autonomous — user drives every change
