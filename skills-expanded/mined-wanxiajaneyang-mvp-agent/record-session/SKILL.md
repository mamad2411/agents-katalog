---
name: record-session
description: "Record work progress in the Trellis workspace without creating hidden commits by default"
---

[!] **Purpose**: Update `.trellis/workspace/` and task tracking after implementation, review, or planning work.

Session recording in this repo **does not auto-commit by default**.
Use `--auto-commit` only when the user explicitly wants the workspace/task metadata committed as part of the current workflow.

---

## Record Work Progress

### Step 1: Get Context & Check Tasks

```bash
python ./.trellis/scripts/get_context.py --mode record
```

[!] Archive tasks whose work is **actually done**:
- Acceptance criteria met and the task is no longer active -> archive it
- If the task is still the active implementation umbrella, leave it open
- Do not archive planning-only or audit sessions just because they were recorded

```bash
python ./.trellis/scripts/task.py archive <task-name>
python ./.trellis/scripts/task.py archive <task-name> --no-commit
```

`task.py archive` still auto-commits `.trellis/tasks` by default.
Use `--no-commit` when the current workflow should not mutate git state.

### Step 2: Add the Session Entry

```bash
# Planning or audit session
python ./.trellis/scripts/add_session.py \
  --title "Session Title" \
  --commit "-" \
  --summary "Brief summary of what was done"

# Implementation session with detailed notes via stdin
cat << 'EOF' | python ./.trellis/scripts/add_session.py --title "Title" --commit "hash"
| Feature | Description |
|---------|-------------|
| Runtime | Updated orchestration rules |
| Tests | Added regression coverage |
EOF

# Explicitly opt into workspace auto-commit
python ./.trellis/scripts/add_session.py \
  --title "Session Title" \
  --commit "hash1,hash2" \
  --summary "Brief summary" \
  --auto-commit
```

**Default behavior**:
- [OK] Appends session to `journal-N.md`
- [OK] Updates workspace `index.md`
- [OK] Leaves git state unchanged unless `--auto-commit` is supplied

---

## Script Command Reference

| Command | Purpose |
|---------|---------|
| `python ./.trellis/scripts/get_context.py --mode record` | Get context for record-session |
| `python ./.trellis/scripts/add_session.py --title "..." --commit "-"` | Record planning/audit work |
| `python ./.trellis/scripts/add_session.py --title "..." --commit "..." --auto-commit` | Record and explicitly auto-commit workspace/task metadata |
| `python ./.trellis/scripts/task.py archive <name>` | Archive a completed task and auto-commit `.trellis/tasks` |
| `python ./.trellis/scripts/task.py archive <name> --no-commit` | Archive a completed task without a git commit |
| `python ./.trellis/scripts/task.py list` | List active tasks |
