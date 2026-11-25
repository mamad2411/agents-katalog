# Skill: Migrate CLAUDE.md

**Purpose:** Bring existing CLAUDE.md to current intake standard without losing data.
**When:** After validate-claude-md found issues; on standard change; onboarding old project.
**Output:** Updated CLAUDE.md with added sections and fixed placeholders. Each change confirmed.

---

## PROCESS

### Step 1 — Read and prepare plan

1. Read `CLAUDE.md` fully
2. Check if `plan.md` already exists in same directory
3. Read `~/.claude/skills/intake/SKILL.md` — OUTPUT TEMPLATE section (current standard)
4. List discrepancies in three categories:
   - **Plan extraction** — `## PHASES` section exists in CLAUDE.md → must be moved to plan.md
   - **Structural** — missing sections (QUICK CONTEXT, INFRA, SECURITY, PLAN line)
   - **Format** — Russian prose where English key-value is expected

Show plan before any changes:
```
Найдено несоответствий: N

ПЛАН:
1. Извлечь ## PHASES из CLAUDE.md → создать plan.md (новый формат с YAML frontmatter)
2. Убрать ## PHASES из CLAUDE.md, добавить строку PLAN: → plan.md в QUICK CONTEXT

СТРУКТУРНЫЕ:
3. Добавить SECURITY (первой секцией, с OPERATOR_TOKEN)
4. Добавить QUICK CONTEXT блок (9 строк key-value)
5. Добавить INFRA строку в QUICK CONTEXT
...

ФОРМАТ:
6. Session Log: сжать в однострочный формат S[N] [date]: [summary]
7. ADR таблица: перенести в docs/adr.md если >3 записей
...

Применяю по одному. Начать?
```

### Step 2 — Apply changes one by one

For each missing section:

**1. Show what you're adding:**
```
── Добавление N/M: [section name] ──────────────

ДОБАВЛЯЮ:
[new section content, filled with data from existing CLAUDE.md]

Куда: [after section X / before section Y]
Данные взяты из: [source]

Добавить? (да / нет / изменить)
```

**2. When adding SECURITY:**
- Generate unique OPERATOR_TOKEN (4 words: adjective-noun-noun-number)
- Adapt stop-ops to project stack (from Architecture / Dependencies)
- Insert as FIRST section

**3. When adding missing sections with data:**
- Extract from existing sections (e.g., Dependencies from Architecture)
- No empty placeholders — only concrete data or explicit TODO

**4. When updating stale data (⚠):**
- Show BEFORE / AFTER
- Explain where updated data comes from

### Step 3 — Final validation

After all changes — run `validate-claude-md`:
```
── Финальная валидация ──────────────────────────
[validate-claude-md output]
```

If ⚠ or ✗ remain — offer to fix manually with hint.

### Step 4 — Report

```
── Migrate CLAUDE.md — Итог ────────────────────

Добавлено секций:   N
Обновлено полей:    M
Пропущено:          K

CLAUDE.md приведён к стандарту intake ✓
```

---

## RULES

- **Never delete existing content** — only add and fix
- **No empty placeholders** — if data missing, ask user
- **Don't change project-specific sections** (Detectors Map, Stage Plan, etc.) — project specifics
- **OPERATOR_TOKEN** — always new, unique; don't copy from other projects
- **One change at a time** — don't combine sections in one step

## BATCH MODE

**When:** target format already known; 5+ files to migrate with identical rules.
**Difference from normal mode:** no per-file confirmation — applies rules silently, summary at end.

### Trigger
Use Batch Mode when user says:
- "migrate all files in [folder]"
- "apply same format to N files"
- "batch migrate, no questions"
- explicitly: "just apply, don't ask for each"

### Batch Process

**Step B1 — Confirm rules once:**
```
Batch migration: [N] files
Rules:
1. [rule — e.g. Translate RU prose → EN]
2. [rule — e.g. Keep RU user-facing strings]
3. [rule — e.g. Move heavy tables → docs/]

Apply to all [N] files? (да / нет)
```
One confirmation for all files. Wait for "да".

**Step B2 — Process silently:**
For each file: Read → apply rules → Write.
No diff shown per file. On error — log and continue.

**Step B3 — Summary:**
```
── Batch Migrate ────────────────────────────
Done:    N files
Skipped: M (errors below)
Errors:  [file]: [reason]

Files: ✓ [file1] ✓ [file2] ...
```

---

## NEW FORMAT RULES

When converting to current standard:

**PHASES → plan.md extraction:**

If `## PHASES` section exists in CLAUDE.md:

1. Check if `plan.md` already exists in same directory:
   - Exists → skip creation, only remove PHASES from CLAUDE.md and add PLAN line
   - Not found → create plan.md from PHASES content

2. Convert PHASES content to plan.md format:
   ```
   BEFORE (in CLAUDE.md):
   ## PHASES
   > Gate between phases — do NOT proceed without explicit "go"
   Phase 1: Foundation — [ ] pending
   - [ ] task A
   - [ ] Gate: criterion

   AFTER (plan.md):
   ---
   project: "[name from CLAUDE.md PROJECT line]"
   updated: YYYY-MM-DD
   session: [session number from CLAUDE.md SESSION line]
   active_phase: [first phase without all [x]]
   ---

   ## Phase 1: Foundation — active
   - [ ] task A
   **Gate:** criterion
   ```

3. Conversion rules:
   - `Phase N: Name — [ ] pending` → `## Phase N: Name — pending`
   - `Phase N: Name — [x] done` → `## Phase N: Name — done`
   - First phase not fully done → status `active`, others stay `pending`/`done`
   - `- [ ] Gate: criterion` → `**Gate:** criterion` (remove checkbox, bold prefix)
   - `> Gate between phases...` line → drop entirely (redundant)
   - `active_phase` = N of first phase with status `active`

4. After creating plan.md — remove entire `## PHASES` section from CLAUDE.md
5. Add `PLAN:     → plan.md` line to QUICK CONTEXT (after IN_PROG line)



**Language:** all new content in English. Existing Russian prose → convert when compressing.

**Session Log compression:**
```
BEFORE (multi-line block):
### 2026-03-10 — Session 16
DONE: implemented 3-screen architecture...
NEXT: Stage 13

AFTER (one line):
S16 2026-03-10: 3-screen arch, pos_map pattern | next: Stage 13
```
Keep only last 5 sessions in CLAUDE.md. Others → offer to move to `docs/session-log.md`.

**ADR compression:**
If ADR table > 3 rows → create `docs/adr.md`, move there, leave in CLAUDE.md:
```
ADR: → docs/adr.md
```

**QUICK CONTEXT:**
Fill from existing CLAUDE.md sections.
INFRA line: take from ENV, ENVIRONMENT, or README sections.
If INFRA not found anywhere — ask user one question.
