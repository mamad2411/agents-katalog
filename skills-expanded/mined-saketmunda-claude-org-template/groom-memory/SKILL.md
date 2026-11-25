# skills/groom-memory/SKILL.md
# Slash command: /groom-memory
# Trigger: User types /groom-memory to detect and flag stale memory files

---

## What This Does

Scans all memory files in `~/.claude/projects/<project>/memory/`, checks them against current git state and codebase, and flags entries that are likely stale or need updating.

This is a read-only skill. It produces a report — it does not update memory files automatically. The engineer reviews the report and decides what to update.

Run this:
- At the start of a new sprint
- After a large batch of PRs merge
- When you suspect the model is citing outdated information
- Periodically every 3–5 sprints as maintenance

---

## Step-by-Step

### Step 1 — Inventory

List all memory files:
```bash
ls ~/.claude/projects/$(basename $(pwd))/memory/
```

For each file, read the header (type, name, description, created/updated date).

### Step 2 — Check Each Memory Type

**`project_*` files — check against current state:**
- Does the file reference a specific count or status? (e.g. "47 fields missing", "Sprint 3 in progress")
  - Check if that number/status is still accurate against the current codebase or git log
- Does the file reference a branch, PR, or task that no longer exists?
  - Run: `git branch -a | grep [branch-name]` and `git log --oneline --grep="[keyword]"`
- Does the file describe work that appears to be complete?
  - Check: do the referenced files now exist? Does the referenced behavior now work?

**`feedback_*` files — check if rule is still active:**
- Does CLAUDE.md still contain this rule?
- Has the project moved past the sprint/phase where this rule applied?
- Is there a newer feedback that supersedes this one?

**`reference_*` files — check if referenced info is current:**
- Do the referenced files or APIs still exist?
- Have versions or endpoints changed?

### Step 3 — Produce Report

```
## Memory Groom Report — [date]

### Files Reviewed: [N]

| File | Type | Status | Reason |
|---|---|---|---|
| project_backlog_post_qa.md | project | 🔴 STALE | References "47 missing fields" — git log shows all implemented in Sprint 4 |
| feedback_complete_cutover.md | feedback | 🟢 CURRENT | Rule still in CLAUDE.md, still in active sprints |
| project_branch_policy.md | project | 🟡 REVIEW | Branch name changed from event-system-reborn to main-replatform — verify |
| feedback_no_feature_flags.md | feedback | 🟡 REVIEW | Scoped to "Sprints 1-5" — currently in Sprint 6, may be expired |

### Actions Required

**Must update (stale data):**
- [ ] `project_backlog_post_qa.md` — update or delete; the 47-field count is inaccurate
- [ ] `project_pr_3_4_followup.md` — PRs 3 and 4 merged 3 sprints ago; archive or delete

**Engineer review needed:**
- [ ] `feedback_no_feature_flags.md` — is this rule still active past Sprint 5?
- [ ] `project_branch_policy.md` — confirm current working branch name

**Current and accurate:**
- [list files that are fine]

### MEMORY.md Index Check
Does MEMORY.md list all current memory files? Missing entries:
- [any files in memory/ not listed in MEMORY.md index]
```

---

## After the Report

The engineer:
1. Reviews the STALE items and deletes or updates them
2. Reviews REVIEW items and confirms whether they're still active
3. Updates MEMORY.md index if files were added or removed

The engineer does this manually — the skill does not auto-delete or auto-update memory files.

---

## Refusal Triggers

- Memory directory doesn't exist — report the path and suggest running `/groom-memory` after memory is initialized
- No memory files found — report "Memory is empty. Add your first memory when you make a significant project decision or correction."

---

## Notes

Memory drift is the most common failure mode in long-running projects. A model citing "47 missing fields" from a 3-sprint-old memory file gives confidently wrong guidance. Groom memory at least once per sprint to keep the model's context accurate.
