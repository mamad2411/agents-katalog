# skills/validate-rules/SKILL.md
# Slash command: /validate-rules
# Trigger: User types /validate-rules to check rules files for drift against current codebase

---

## What This Does

Scans all files in `.claude/rules/` and checks whether the conventions they describe still match the actual codebase. Flags rules that reference:
- Files, paths, or modules that no longer exist
- Libraries or packages not in `package.json` / `requirements.txt` / `go.mod`
- Patterns that contradict what's actually in the code

This is a read-only audit. It produces a report — it does not edit rules files. The engineer decides what to update.

Run this:
- When the tech stack changes (new library added, old one removed)
- After a major refactor changes the folder structure
- At the start of a new project phase
- Periodically every 4–6 sprints

---

## Step-by-Step

### Step 1 — Inventory

List all rules files:
```bash
find .claude/rules -name "*.md" | sort
```

### Step 2 — For Each Rules File

Read the file. Extract:
- **File path references:** Any path mentioned (e.g. `src/lib/logger`, `rules/_shared/logging.md`)
- **Package/library references:** Any import or package name (e.g. `@aws-sdk/client-s3`, `vitest`, `prisma`)
- **Convention claims:** Patterns described as "always" or "never" — verify against real code samples

Then check each:

```bash
# Check if referenced paths exist
ls src/lib/logger.ts 2>/dev/null || echo "MISSING"

# Check if referenced packages are in dependencies
cat package.json | grep "aws-sdk/client-s3" || echo "NOT FOUND"

# Spot-check a convention claim (e.g. "all handlers use middy middleware")
grep -r "middy" src/handlers/ --include="*.ts" | wc -l
```

### Step 3 — Produce Report

```
## Rules Validation Report — [date]

### Files Checked: [N]

| Rules File | Status | Issues Found |
|---|---|---|
| rules/backend.md | 🔴 DRIFT | References `src/lib/powertools` — path moved to `src/shared/powertools` |
| rules/testing.md | 🟢 CURRENT | All paths and packages verified |
| rules/frontend.md | 🟡 REVIEW | References `TanStack Query` as banned — but package.json shows it was added in Sprint 5 |
| rules/_shared/logging.md | 🔴 DRIFT | Import path `@/lib/logger` — file is now `@/shared/logger` |

### Detailed Findings

**rules/backend.md — DRIFT**
- Line 23: References `src/lib/powertools/logger` → actual path: `src/shared/powertools/logger`
- Line 47: Import example uses `aws-sdk` v2 → project is on v3 (`@aws-sdk/client-*`)

**rules/frontend.md — REVIEW**
- Line 12: "No TanStack Query" listed as banned → TanStack Query found in package.json (added Sprint 5?)
  - Engineer decision needed: update the rule or remove the package?

### CLAUDE.md Cross-reference
Non-goals listed in CLAUDE.md vs. actual package.json:
| Non-goal | In package.json? | Flag |
|---|---|---|
| No TanStack Query | YES — @tanstack/react-query@5.x | ⚠️ CONFLICT |
| No CDK | No | ✅ |

### Actions Required

**Update rules files (drift detected):**
- [ ] `rules/backend.md` line 23 — update path reference
- [ ] `rules/_shared/logging.md` line 8 — update import path

**Engineer decision needed:**
- [ ] TanStack Query in package.json vs. Non-goal in CLAUDE.md — which is correct?

**All clear:**
- [list files with no issues]
```

---

## Refusal Triggers

- `.claude/rules/` directory doesn't exist — report and stop
- Rules directory is empty — report "No rules files found. Add your first rules file before validating."
- Request to auto-fix rules drift — this skill is read-only. Fixing rules is a PR from tech-writer or the engineer directly.

---

## Notes

Rules rot is silent. The model reads stale rules and confidently generates code that doesn't match the actual project structure. Running `/validate-rules` before a sprint catches drift before it causes agent mistakes.

The highest-risk moment for rules drift: after a major dependency upgrade or a folder restructure. Always run this after those events.
