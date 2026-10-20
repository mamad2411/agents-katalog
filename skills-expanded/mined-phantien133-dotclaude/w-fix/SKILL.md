---
description: Lightweight workflow for bug fixes and small changes (1-3 files, <2h). Reads project config from .claude/workflow.yaml. Pass a GitHub issue URL, #N, or free description to start.
argument-hint: <issue-url | #N | description>
allowed-tools: Bash, Read, Write, Edit, Skill
---

# w-fix

Lightweight dev workflow for bug fixes and small changes.

**Use this when:** 1–3 files affected, no DB schema changes, no new API surface, estimated <2h.  
**Use `/w-task` instead when:** new feature, cross-module changes, DB migrations, estimated >2h.

**First run:** `$ARGUMENTS` is an issue reference or free description → starts Phase 0.  
**Subsequent runs:** `$ARGUMENTS` is empty or `continue` → reads `state.yaml` and advances.

---

## ⚠️ Invocation gate — read on every run

The workflow advances **only** when the developer explicitly runs `/w-fix`.

- During a gate pause: freely chat, ask questions, request edits — **do NOT advance**.
- A phase transition happens **only** when this skill is invoked with empty / `continue` args.
- Any other `$ARGUMENTS` = a question or correction within the current phase — respond and stay.

```
$ARGUMENTS present (URL / #N / description)?
  └─ Yes → First run: start Phase 0
  └─ No (empty or "continue") →
       state.yaml exists?
         └─ No  → Ask for issue reference or description
         └─ Yes → Read phase + status, advance
```

---

## Setup check

Before Phase 0, read config:

```bash
cat .claude/workflow.yaml 2>/dev/null
```

If file missing: say "Run `/w-setup` first to configure this project." Stop.

Extract:
- `issue_tracker.type`, `.url`, `.workspace`, `.project`, `.mcp_available`
- `workflow.state_root` → default `.workflow`
- `project.test_command`, `.typecheck_command`, `.lint_command`
- `project.codegraph.*` — probe once with `w-codegraph detect` and store the result in
  `state.yaml.codegraph`; drives file location in 0.3 and test targeting in Phase 1
- `repos[]` (version 2) — per-repo `{path, default_branch, remote}`; if absent, synthesize
  a single `.` entry from `pr.default_branch` (default `main`). Drives Phase 3 per-repo PRs.
- `pr.draft`, `.default_branch`

---

## Phase 0 — Intake & Locate (INTERACTIVE → GATE 0)

### 0.1 Resolve issue

Parse `$ARGUMENTS` based on `issue_tracker.type`:

**github:**
- URL (`github.com/.*/issues/\d+`): extract issue number → `gh issue view <N> --json title,body --repo <org/repo>`
- `#N` or bare number: `gh issue view <N> --json title,body`
- Free text: use as-is, no fetch.
- If `gh` fails: proceed with `$ARGUMENTS` as description.

**plane (mcp_available: true):**
- URL matching configured `url`: extract identifier → call `mcp__plane__retrieve_work_item_by_identifier`
- Identifier (e.g. `PROJ-42`): same MCP call
- Free text: use as-is.
- If MCP unavailable: fall back to free text.

**plane (mcp_available: false) / jira / linear:**
- URL or identifier: ask developer to paste the ticket description.
- Free text: use as-is.

**none:** always use `$ARGUMENTS` as-is.

### 0.2 Derive task-slug

- Issue with ID: `<ID>-<short-slug>` (kebab-case, max 25 chars for title part)
  Example: `#42` + "Fix login timeout" → `42-login-timeout`
- Free text: kebab-case of description, max 40 chars.

Create directory `<state_root>/<task-slug>/`.

### 0.3 Locate affected files

Targeted search — not a full codebase scan.

**With CodeGraph** (`state.yaml.codegraph` is `ready`/`stale`) — the graph is faster and
catches the caller a grep misses:
```bash
codegraph sync -q
codegraph query "<symbol or error identifier>" --limit 10 --json
codegraph callers "<suspect symbol>" --json      # who reaches the broken code
codegraph affected <suspect files> --quiet       # which tests should have caught it
```
A bug with no covering test in the `affected` list tells you what to write before fixing.

**Without it:**
- Parse description/title for file names, function names, class names, error strings.
- Grep for relevant identifiers in source dirs (from `project.src_dirs` if set, else repo root).
- Read only specific implicated files (max 5).

Either way: form a root cause hypothesis before editing anything.

### 0.4 Scope check

If any of the following: stop and recommend `/w-task`:
- DB schema changes needed
- New API surface required
- Changes span >3 files or >2 modules
- Estimated implementation time >2h

Say: "This is beyond w-fix scope. Run `/w-task <description>` to use the full workflow."

### 0.5 Write intake.md

```markdown
# Quick Fix — <title>

## Source
- Input: <URL / identifier / "free description">
- Issue ID: <ID or n/a>

## Description
<description>

## Root Cause Hypothesis
<what is wrong and why>

## Affected Files
- `<path>` — <reason>

## Approach
<one paragraph: what to change and how>
```

### 0.6 Pause

Display:
```
Root cause: <hypothesis>
Files:      <list>
Approach:   <one-line summary>

Confirm or correct (reply in chat), then run /w-fix to implement.
```

Write `state.yaml`:
```yaml
task: <task-slug>
phase: "0"
status: gate_pending
started_at: <timestamp>
last_updated: <timestamp>
```

**GATE 0:** developer confirms or corrects in chat → runs `/w-fix`.

---

## Phase 1 — Fix (AUTO → GATE 1)

*Triggers when `phase: "0"` + `status: gate_pending`.*

1. Read developer's reply from GATE 0. Update `intake.md § Affected Files` and `§ Approach` if corrected.

2. **Implement the fix** — edit only files listed in `intake.md § Affected Files`.

3. **Run existing tests** — only if test files already exist (do not write new tests):

   Resolve test command:
   - `check_commands.test` in state.yaml if set (developer override from setup)
   - `project.test_command` from config (expand `auto` via detection)
   - Append `--passWithNoTests` or equivalent if supported

   ```bash
   <test_command> 2>&1 | tail -20
   ```

4. **Inline checks** on affected files:

   Resolve commands same way (config → auto-detect):
   - typecheck: run on whole project (`npx tsc --noEmit` etc.)
   - lint: run on affected files only

5. Write `fix.md`:

```markdown
# Fix — <title>

## Changes
| File | What changed |
|------|-------------|
| `<path>` | <one-line summary> |

## Test results
<PASS / FAIL / no tests found — include relevant output>

## Check results
| Check     | Result |
|-----------|--------|
| typecheck | ✅ / ❌ <note> |
| lint      | ✅ / ❌ <note> |
```

6. Update `state.yaml`: `phase: "1"`, `status: gate_pending`, `last_updated: <now>`.

Output: "Fix implemented. Review the diff and fix.md. Run `/w-fix` to commit."

**GATE 1:** developer reviews diff + fix.md → runs `/w-fix`.

---

## Phase 2 — Commit & Docs (AUTO → GATE 2)

*Triggers when `phase: "1"` + `status: gate_pending`.*

1. **Commit** — stage only files from `intake.md § Affected Files`:

   ```bash
   git add <affected files>
   git commit -m "fix(<scope>): <one-line summary from intake.md>"
   ```
   
   `<scope>` = inferred from affected file paths (module name, package, etc.).  
   Do NOT use `git add -A`.

2. **Assess doc update** — update only if meaningful:

   | Situation | Action |
   |-----------|--------|
   | Bug in a named feature, `docs_root` is set | Append row to feature doc § Implementation history |
   | Truly trivial (typo, log, comment) | No update needed |
   | `docs_root` is null | Skip |

   If ambiguous: ask "Worth a note in docs? (provide path or skip)"

3. Update `state.yaml`: `phase: "2"`, `status: gate_pending`, `last_updated: <now>`.

Output: "Committed. Run `/w-fix` to create the PR."

**GATE 2:** developer confirms → runs `/w-fix`.

---

## Phase 3 — PR (AUTO → complete, **terminal**)

*Triggers when `phase: "2"` + `status: gate_pending`.*

Creating the PR is the **final** action. For each repo that has commits (the main
workspace, plus any submodule the fix touched — see `repos[]` in workflow.yaml),
run `/w-pr <task-slug> --repo <path> --target <that repo's default_branch>`. A
single-repo fix is just one `/w-pr <task-slug>` against `.`.

Output: "Run `/w-pr <task-slug>` to create the PR (add `--repo <path>` per submodule if the fix spans modules)."

**GATE 3:** developer runs `/w-pr`.

After the PR(s) exist, perform a **single** final state write:
`state.yaml`: `phase: "3"`, `status: complete`, `prs: [...]`, `last_updated: <now>`.

**Then ship that state — the workflow does not end with a dirty tree.** Unless
`state_root` is gitignored (`git check-ignore -q <state_root>` → nothing to do):

```bash
git -C <repo> add <state_root>/<task-slug>/
git -C <repo> commit -m "chore(<task-slug>): finalize workflow state"
git -C <repo> push <remote> HEAD:<current-branch>      # plain push — never --force
```

A rejected push means someone else pushed to the branch: merge (`pull --rebase=false`)
and push again. Never force, never rewrite — the PR may already carry review comments.
If it still fails, say so and leave the commit local.

Output: "Task complete. Final state committed and pushed to <branch> — the PR carries the
full record. state.yaml is final." A later `/w-fix` on a `complete` task is a no-op that
reprints the PR URL(s).

---

## State transitions

| phase | status | Next `/w-fix` triggers |
|-------|--------|--------------------------|
| "0" | gate_pending | Phase 1 — implement fix |
| "1" | gate_pending | Phase 2 — commit + docs |
| "2" | gate_pending | Phase 3 — create PR → complete |

---

## Escalation to /w-task

At any phase, if you discover the fix has grown beyond scope:

> "This has grown beyond w-fix scope. Run `/w-task <description>` to restart with the full workflow."

Stop the current workflow.
