---
name: tutorial-check
description: |
  Homework validator — checks that user completed the QUICKSTART tutorial
  correctly. Runs 5 SQL/file checks (routing.db populated, project registered,
  demo workspace, skill invocations logged, task folder structure) plus an
  optional 6th self-audit step. Reports ✅/❌ per check with remediation hints.

  Use when: after completing QUICKSTART § 5 walkthrough, "/tutorial-check",
  "check my setup", "проверь мою установку", "run homework checks".
---

# Tutorial-Check Protocol

Homework validator for the QUICKSTART walkthrough. Runs 5 checks against
the user's workspace to confirm they set up their first real project
correctly. Reports ✅/❌ per step with a one-line remediation hint.

Read-only — never modifies files or DB.

---

## When to invoke

After the user completes the 5-step homework in `docs/QUICKSTART.md` § 5:

1. Create a project named `my-tutorial`
2. Start a task in that project (`/go-start` + `/go-fast`)
3. Approve the full chain (ok, ok, 1)
4. Verify 5 artifact files exist in `tasks/log/{slug}/`
5. Confirm the task appears in Flow UI

Then the user runs `/tutorial-check` and gets pass/fail per step.

---

## Step 0 — Detect workspace root

Find the workspace root by walking up from CWD until we find `framework.yml`
or `manifest.yml` at the same level. If none found within 5 levels — abort:

```
⚠️ Not inside a framework workspace. Run this from anywhere inside your
   framework directory (where framework.yml lives).
```

Set `{workspace_root}` for all subsequent checks.

---

## Step 1 — Run the 5 checks

Each check is independent — a failure in one doesn't skip the others.

### Check 1: Project `my-tutorial` created

```bash
test -d "{workspace_root}/projects/my-tutorial" && D1=✅ || D1=❌
grep -q "id: my-tutorial" "{workspace_root}/aihub/projects.yml" && D2=✅ || D2=❌
test -L "{workspace_root}/projects/my-tutorial/.agents/skills" && D3=✅ || D3=❌
```

Pass = D1 AND D2 AND D3.
Remediation: `bash bin/new-project my-tutorial`

### Check 2: Task started in that project

```bash
COUNT=$(sqlite3 "{workspace_root}/tasks/routing.db" \
  "SELECT COUNT(*) FROM artifacts WHERE project = 'my-tutorial'")
test "$COUNT" -gt 0 && CHECK2=✅ || CHECK2=❌
```

Pass = at least one artifact row exists.
Remediation: `cd projects/my-tutorial && claude`, then `/go-start` and `/go-fast "..."`.

### Check 3: Chain approved (plan-first artifact exists)

```bash
COUNT=$(sqlite3 "{workspace_root}/tasks/routing.db" \
  "SELECT COUNT(*) FROM task_artifacts ta
   JOIN artifacts a ON ta.task_id = a.id
   WHERE a.project = 'my-tutorial' AND ta.artifact_type = 'plan-first'")
test "$COUNT" -gt 0 && CHECK3=✅ || CHECK3=❌
```

Pass = plan-first ran, meaning user approved flow-first + library-first gates.
Remediation: rerun `/go-fast` and reply `ok`/`ok`/`1` at each gate.

### Check 4: 5 artifact files exist on disk

For each task folder under `{workspace_root}/tasks/log/` where task belongs to
project `my-tutorial`, count files matching these 5 patterns:

- `flow-first-*.md`
- `library-first-*.md`
- `plan-first-*.md`
- `report-*.md`
- `user-note-*.md`

Pass = all 5 files present.
Remediation: chain likely errored mid-execution. Check for empty/missing artifacts, rerun /go-fast.

### Check 5: Task visible in Flow UI

Flow UI reads from `routing.db`. If the task registered → it's visible.

```bash
COUNT=$(sqlite3 "{workspace_root}/tasks/routing.db" \
  "SELECT COUNT(*) FROM artifacts
   WHERE project = 'my-tutorial'
   AND datetime(created_at) > datetime('now', '-24 hours')")
test "$COUNT" -gt 0 && CHECK5=✅ || CHECK5=❌
```

Pass = recent activity registered in DB → Flow UI will show it.
Remediation: check `sqlite3 tasks/routing.db "SELECT * FROM artifacts WHERE project='my-tutorial'"`. If empty — task never registered. Rerun `/go-start`.

### Check 6 (optional): Self-audit — tutorial-check invocation logged

```bash
COUNT=$(sqlite3 "{workspace_root}/tasks/routing.db" \
  "SELECT COUNT(*) FROM skill_invocations
   WHERE skill_name = 'tutorial-check'
   AND datetime(invoked_at) > datetime('now', '-5 minutes')")
test "$COUNT" -gt 0 && CHECK6=✅ || CHECK6=⚠️
```

Not required for pass — informational only.

---

## Step 2 — Report

Output a compact table:

```
╭──────────────────────────────────────────────────────────╮
│  Tutorial-Check Report                                   │
├──────────────────────────────────────────────────────────┤
│  ✅ 1. Project my-tutorial created                       │
│  ✅ 2. Task started                                      │
│  ❌ 3. Chain approved       — plan-first missing         │
│  ❌ 4. Artifacts exist      — 3/5 found                  │
│  ✅ 5. Task in Flow UI                                   │
│  ✅ 6. Self-audit (invocation logged)                    │
├──────────────────────────────────────────────────────────┤
│  Score: 3/5 core checks + 1 self-audit                   │
│  Status: ❌ Homework incomplete                          │
╰──────────────────────────────────────────────────────────╯
```

If all 5 pass — congratulate the user and point at CONCEPTS.md +
next-step suggestion (try `/go-fast` on a real change).

---

## Step 3 — Exit

Don't invoke other skills. Don't modify files. Report only.

---

## Anti-patterns

### ❌ Auto-fixing failures

The skill diagnoses; it doesn't repair. Auto-remediation hides the learning
opportunity — the user needs to see what step failed and do it themselves.

**Rule:** report only. Suggest commands, don't run them.

### ❌ Running on non-my-tutorial projects

Someone runs `/tutorial-check` in a real production project — the skill
reports 5 ❌ because it hardcodes `my-tutorial`. Confusing.

**Rule:** the report explicitly names `my-tutorial` and mentions
QUICKSTART.md § 5 so context is unambiguous.

### ❌ Silent failure on missing DB

If `tasks/routing.db` doesn't exist yet (fresh workspace, never ran
init-demo or any task) — each SQL check will error, and users see raw
sqlite errors.

**Rule:** Step 0 detects workspace root; if `tasks/routing.db` missing,
show explicit "Workspace not initialized — run `bash bin/init` first"
message.

### ❌ Modifying routing.db during check

Read-only guarantee. Never `INSERT`, never `UPDATE`, never `DELETE`
except the Step 99 self-invocation log.

---

## Related skills

- **plan-first** — the skill that produces the artifact Check 3 verifies
- **flow-first**, **library-first** — sibling skills the tutorial exercises
- **ship-first** — closes tasks the tutorial creates
- **check-first** — sibling coverage validator with similar report-and-exit shape

---

## Step 99 — Log invocation

```bash
sqlite3 "{workspace_root}/tasks/routing.db" \
  "INSERT INTO skill_invocations (task_id, block_num, skill_name, invoked_at)
   VALUES ('tutorial-check', NULL, 'tutorial-check', datetime('now'))" 2>/dev/null || true
```

The `|| true` guard prevents failure if DB is missing or table doesn't
exist yet (fresh workspace).
