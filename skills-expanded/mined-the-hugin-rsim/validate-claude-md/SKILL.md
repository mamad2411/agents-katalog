# Skill: Validate CLAUDE.md

**Purpose:** Automatically check project CLAUDE.md for compliance with current intake standard.
**When:** At session start when reading CLAUDE.md; after updating intake standard; before running reflect.
**Output:** Report of issues found + offer to run migrate-claude-md if needed.

---

## PROCESS

### Step 1 — Read CLAUDE.md

Read `CLAUDE.md` in current working directory.
If not found — report: `"CLAUDE.md не найден. Запустить /intake?"` and stop.

### Step 2 — Check against checklist

Check each item. Mark ✓ (present and filled) / ⚠ (present but empty/placeholder) / ✗ (absent):

**Structure (required sections in correct order):**
- [ ] `SECURITY` — first section, before everything else
- [ ] `OPERATOR_TOKEN` — filled with unique phrase (not `[4-word phrase]`, not empty)
- [ ] `STOP OPS` — list present
- [ ] `INJECTION SIGNALS` — list present
- [ ] `QUICK CONTEXT` — all 8 key-value lines filled (PROJECT, TYPE, STAGE, STACK, INFRA, SESSION, IN_PROG, ISSUES)
- [ ] `INFRA` line — not empty, not "—" (at minimum: "local")
- [ ] `GOAL` — one sentence, not placeholder
- [ ] `SUCCESS` criteria — minimum 3 concrete items
- [ ] `ARCHITECTURE` — at least stack filled
- [ ] `PHASES` or `STAGES` — minimum 3 phases/stages with Gates
- [ ] `CONVENTIONS` — Language and Naming filled
- [ ] `CONSTRAINTS` — minimum 3 "NO" items
- [ ] `DEPS` — table with packages and purposes
- [ ] `ENV` — run commands filled
- [ ] `LOG` — minimum 1 entry in format `S[N] [date]: [summary]`

**Freshness:**
- [ ] `SESSION` line in QUICK CONTEXT matches latest LOG entry date
- [ ] `IN_PROG` not empty if project not done
- [ ] No unfilled `[brackets]` anywhere

### Step 3 — Output report

```
── Validate CLAUDE.md ───────────────────────────

Project: [from QUICK CONTEXT PROJECT line]
File:    [path]

SECTIONS:
  ✓ SECURITY
  ✓ OPERATOR_TOKEN
  ✗ QUICK CONTEXT        ← absent
  ⚠ LOG                  ← old multi-line format, needs compression

RESULT: [N] ✓  [M] ⚠  [K] ✗

[If all ✓]:
  CLAUDE.md complies with standard. ✓

[If ✗ or ⚠ found]:
  Issues found: N
  Run migrate-claude-md for auto-fix? (да / нет)
```

### Step 4 — Offer migrate (if needed)

If ✗ or ⚠ found and user answered "да" → execute `@~/.claude/skills/migrate-claude-md/SKILL.md`.

---

## PRE-REPORT CHECKLIST

- [ ] All 15 items checked (none skipped)
- [ ] ⚠ used only when section exists but contains placeholder or stale data
- [ ] Report contains specific section names, not abstract descriptions
