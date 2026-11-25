---
name: improve
group: cycle
triggers: []
output: "updated SKILL.md files, ~/.claude/skills/index.md, ~/.claude/skills/changelog.md"
calls: [skill-generator]
---

# Skill: Improve

**Purpose:** Update skills based on `~/.claude/reflection.md` and user's correction string. Closes the self-improving loop.
**When:** After user has filled the correction string in `~/.claude/reflection.md`.
**Output:** Updated skills (explicit approval per change) + updated `~/.claude/skills/index.md`.

---

## PROCESS

### Step 1 — Read inputs

1. `~/.claude/reflection.md` — fully (global file, not in project folder)
2. User's correction string — **top priority**, overrides everything else
3. Current versions of all skills mentioned in "Proposals" section
4. `~/.claude/skills/index.md` — current registry state
5. `~/.claude/skills/cross-cutting-principles.md` — mandatory reference for all changes

If `~/.claude/reflection.md` not found or correction string empty — report and stop:
```
~/.claude/reflection.md не найден / строка коррекции пуста.
Запусти Reflect Skill и заполни строку коррекции перед Improve.
```

### Step 1.1 — Parse YAML frontmatter

Extract from the `---` block at the top of reflection.md:

- **`confidence`** — if < 0.5, warn before building change plan:
  ```
  ⚠️ Низкий confidence ([N]). Данные сессии ненадёжны.
  Изменения применять с повышенной осторожностью, особенно L2.
  Продолжить? (да / нет)
  ```
  Wait for answer. If "нет" — stop.

- **`root_causes`** — use as context when evaluating proposed changes.
  A proposed change that addresses a listed root_cause = higher priority.

- **`improvements.workflows`** — treat as L2-level candidates in Step 2 change plan.

- **`improvements.skills`** — cross-check against "Proposals" section.
  If a skill appears in frontmatter but not in Proposals — flag as possible omission.

If frontmatter is missing or malformed (no `---` block) — continue without it, but note:
```
⚠️ Frontmatter отсутствует — reflection.md создан до RSIm Phase 2.
Proceeding without structured metadata.
```

### Step 1.5 — Context analysis before changes

For each skill from "Proposals" section, check:

1. **Change history:** read `~/.claude/skills/changelog.md` (if exists).
   How many times changed? What changed last time?
   → 3+ changes in last 5 cycles = instability signal. Flag explicitly in plan.

2. **Recurring ❌:** scan `~/.claude/reflection-*.md` archive.
   Does this skill have ❌ in previous reflections?
   → Yes = recurring pattern, not one-off. Propose deeper fix, not cosmetic.

3. **Conflicts:** compare proposed change with last changelog entry for that skill.
   Does new change undo what was just added?
   → Conflict → show before diff: `⚠️ Конфликт с правкой от [дата]: [суть]`

If changelog doesn't exist — skip point 1, proceed with 2-3.

Result of this step: **internal context only**, not shown to user.
Flag instability signals or conflicts in the change plan.

---

### Step 2 — Build change plan

#### Level definitions

Every proposed change must be classified before adding to the plan:

- **L1 — Knowledge Update:** adds or edits entries in memory files
  (`hard-problems.md`, `best-practices.md`, `patterns.md`, heuristics).
  Does NOT modify skill behavior. Low risk.

- **L2 — Workflow Update:** modifies skill steps, sequences, rules, or CLAUDE.md dispatch.
  Changes how the agent behaves. Apply with scrutiny — one session of friction
  is usually not enough justification for an L2 change.

- **L3 — Strategy Update:** NOT IMPLEMENTED (requires scoring system).
  If a proposed change would fall here — add as TODO in plan, do not apply:
  ```
  [L3-TODO] [описание] — отложено до реализации scoring (#10)
  ```

#### Classification rules

| Proposed change | Level |
|----------------|-------|
| Add entry to hard-problems / best-practices / patterns | L1 |
| Update heuristic or tip in a skill | L1 |
| Modify a step, sequence, or rule in a skill | L2 |
| Create a new skill | L2 |
| Edit CLAUDE.md dispatch table (Rule 4) | L2 |
| Edit CLAUDE.md Rule 1.5 / Rule 1.7 | L2 |
| Change agent strategy across projects | L3 |

#### Priority order

1. **User's correction string** — always first (classify L1 or L2 based on content)
2. L2 changes from friction with specific proposals
3. L1 changes from friction
4. New skills (L2)
5. CLAUDE.md edits (L2)
6. Simplifications (classify individually)

#### Plan format

Show plan in one message before any changes:

```
Предлагаю следующие изменения (в порядке приоритета):

[L1] 1. [скилл/файл]: [суть изменения] ← строка коррекции
[L2] 2. [скилл/файл]: [суть изменения]
[L1] 3. [скилл/файл]: [суть изменения]

L1 = knowledge (низкий риск) | L2 = workflow (меняет поведение) | L3-TODO = отложено

Применяю по одному, каждый раз жду подтверждения.
Начинаем с №1?
```

Wait for "да" / "продолжай" / "пропусти" before first change.

### Step 3 — Apply changes one by one

For each change in plan:

**1. Show diff before applying:**

For L1 changes:
```
── [L1] Изменение N/M: [скилл] ──────────────────

БЫЛО:
[exact quote from current file]

СТАНЕТ:
[new text]

Причина: [one line from reflection.md]

Применить? (да / нет / изменить)
```

For L2 changes:
```
── [L2] Изменение N/M: [скилл] ──────────────────
⚠️ Это изменение меняет поведение скилла. Одна сессия фрикций — слабое основание.

БЫЛО:
[exact quote from current file]

СТАНЕТ:
[new text]

Причина: [one line from reflection.md]
Повторялось в предыдущих reflections: [да — N раз / нет]

Применить? (да / нет / изменить)
```

**2. Wait for explicit answer:**
- `да` / `продолжай` / `apply` → apply change
- `нет` / `пропусти` / `skip` → skip, move to next
- `изменить` + correction → apply corrected version
- any other → clarify intent, don't guess

**3. After applying — confirm and write to changelog:**
```
✓ [файл] обновлён.
```

Immediately add line to `~/.claude/skills/changelog.md`:
```
YYYY-MM-DD | [skill-name] | [one-line summary] | [source: correction / friction / new skill]
```
If file doesn't exist — create it with header before writing.

**4. Move to next item.**

### Step 3б — Create new skill (if plan includes new skills)

If plan item = "create new skill":

1. Show skill description (name, purpose, when to use) — wait for "да"
2. Verify design against `~/.claude/skills/cross-cutting-principles.md` before generating
3. Use `skill-generator` to create `~/.claude/skills/[name]/SKILL.md`
3. After creation — add row to `~/.claude/skills/index.md` (in correct group):
   ```
   | `[name]` | [purpose] | [tags] | 0 | ✅ Ready |
   ```
4. **Required:** sync Rule 4 dispatch table from skill frontmatter:
   - Read `triggers:` field from new skill's frontmatter
   - If triggers is non-empty → show diff to add row to Rule 4 in `~/.claude/CLAUDE.md`:
     ```
     | [trigger1] / [trigger2] / ... | `[skill-name]` |
     ```
     Apply with confirmation.
   - If triggers is empty → skip, note "triggers: [] — skill called explicitly, no Rule 4 row"
5. Confirm:
   ```
   ✓ ~/.claude/skills/[name]/SKILL.md создан.
   ✓ index.md обновлён.
   ✓ Rule 4: [добавлена строка с триггерами / не требуется — triggers пуст]
   ```

Don't skip the description step — user must confirm the skill is what they want.

### Step 3в — Semantic Distillation check

After all L1/L2 changes are applied — scan episodic memory for recurring patterns.

**Trigger:** Run this step automatically after every Improve session.

**Process:**

1. Read all entries from:
   - `~/.claude/memory/episodic/hard-problems.md`
   - `~/.claude/memory/episodic/best-practices.md`
   - `~/.claude/memory/episodic/failures/*.md` (all files)

2. Group entries by **Tags:** field. Count entries per tag.

3. For each tag with **3+ entries** across episodic memory:
   - Check `~/.claude/memory/semantic/patterns.md` — does a pattern for this tag already exist?
   - If YES → skip (already distilled).
   - If NO → candidate for distillation.

4. For each candidate, show proposed entry (one at a time):
   ```
   ── [DISTILL] Паттерн для тега: [tag] ──────────────────

   Найдено [N] episodic записей с тегом "[tag]":
     - [entry 1 title] (hard-problems / best-practices / failures)
     - [entry 2 title]
     - [entry N title]

   Предлагаю добавить в semantic/patterns.md:

   ## [Domain] — [Pattern title]

   **Tags:** [tag, ...]

   Generalization:  [timeless rule extracted from the N entries]
   Evidence:        [N] episodic observations
   Applicable:      [when to apply]
   Counter-cases:   [when it does NOT apply, if derivable]

   Добавить? (да / нет / изменить)
   ```

5. On "да" — append entry to `~/.claude/memory/semantic/patterns.md`.
   Log to changelog:
   ```
   YYYY-MM-DD | semantic/patterns | [tag] pattern distilled from N episodic entries | distillation
   ```

**Rules:**
- Generalization must be **timeless** — no dates, no project names
- Only distill what is clearly consistent across all N entries
- If entries contradict each other → skip, note: `⚠️ [tag]: записи противоречат друг другу — не дистиллируем`
- If 0 candidates found → skip silently, do not mention to user

---

### Step 4 — Update ~/.claude/skills/index.md

After all applied changes:

**Required — usage counters:**
Take skills table from reflection.md (with ✅/⚠️/❌ ratings) — all mentioned skills were used this session. Increment their "Uses" counter by 1. Non-optional step.

Also: if skill got `❌` — add `⚠️ Review` next to status in index.md. If skill had `❌` in previous reflection too (check archive) — recurring signal, candidate for priority Improve.

**Other:**
- Update status of changed skills
- Add rows for new skills if created
- Move to archive section if skill was deleted

Show diff for index.md — also with confirmation.

### Step 5 — Archive and final report

**Automatically** (no confirmation) rename `~/.claude/reflection.md`:
→ `~/.claude/reflection-YYYY-MM-DD.md` (date from reflection.md header)

Then show final report:

```
── Итог Improve сессии ─────────────────────────

Применено изменений:  N
Пропущено:            M
Файлы обновлены:
  ✓ ~/.claude/skills/[name]/SKILL.md
  ✓ ~/.claude/skills/index.md
Архив:
  ✓ ~/.claude/reflection.md → reflection-YYYY-MM-DD.md

Цикл завершён:
  intake → работа → reflect → improve ✓

Следующий проект начнётся с улучшенными скиллами.

[If applied changes ≥ 1]:
  Новые улучшения готовы к экспорту → /rsim-export
```

---

## CURATOR RULES

**Conservative changes:**
- Prefer targeted edits over rewrites
- Don't change what clearly worked (section "Помогло" in reflection.md)
- Correction string overrides reflection.md proposals if they conflict

**Boundaries:**
- Never apply without explicit "да"
- Never combine multiple changes in one diff — one at a time
- Don't touch project `CLAUDE.md` without explicit instruction
- Don't delete skills — only archive (move to Archive section in index.md)

**Uncertainty:**
- Vague reflection proposal → clarify with user before showing diff
- Change affects multiple skills → show all related diffs together
- Unclear how to implement correction → show 2 options, ask user to choose

---

## PRE-FLIGHT

Before final report: re-read ## CURATOR RULES and this checklist. Verify every item. Fix before delivery.

## PRE-FINAL-REPORT CHECKLIST

- [ ] User's correction string applied (or explicitly declined by user)
- [ ] Every change shown as diff and confirmed
- [ ] All changes verified against `~/.claude/skills/cross-cutting-principles.md`
- [ ] `~/.claude/skills/index.md` updated — counters, statuses, archive
- [ ] No change applied without explicit "да"
- [ ] `~/.claude/reflection.md` archived automatically in Step 5
- [ ] Step 3в ran — semantic distillation check completed (even if no candidates found)
