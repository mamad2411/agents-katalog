---
name: reflect
group: cycle
triggers: []
output: "~/.claude/reflection.md (with YAML frontmatter), entries in hard-problems.md, best-practices.md, failures/"
calls: []
---

# Skill: Reflect

**Purpose:** Analyze completed session/project — creates `~/.claude/reflection.md` as input for Improve.
**When:** At end of each significant session. Required at project end.
**Output:** `~/.claude/reflection.md` (global, not in project folder) + entries in `~/.claude/memory/episodic/hard-problems.md` for hard cases.

---

## PROCESS

### Step 1 — Collect session data

Read before analysis:
1. `CLAUDE.md` — current Session Log and Known Issues
   ⚠️ If CLAUDE.md doesn't exist: skip reading it; in Step 5 skip CLAUDE.md update;
   in reflection.md under "Правки CLAUDE.md" write:
   `"CLAUDE.md отсутствует — /intake не запускался, Session Log не ведётся."`
2. `plan.md` (if exists in CWD) — current phases and task progress
   Read frontmatter: `active_phase`, `session`, `updated`
   Note which tasks are `- [ ]` vs `- [x]` in the active phase.
3. `~/.claude/skills/index.md` — which skills were used
3. `~/.claude/memory/episodic/hard-problems.md` — compare this session's problems with recorded ones.
   Same problem seen in another project = **recurring pattern**, flag explicitly. Recurring = new skill candidate.
4. Changed files list — run one of:
   - `git diff --name-only HEAD` (git repo)
   - Glob `**/*.{py,html,js,css,md,yaml}` sorted by modification date (non-git)
     > **Windows without git:** `py -3 -c "import os,glob,time; files=sorted(glob.glob('**/*',recursive=True),key=os.path.getmtime,reverse=True)[:20]; [print(time.strftime('%H:%M',time.localtime(os.path.getmtime(f))),f) for f in files if os.path.isfile(f)]"`
     > Do NOT use `ls -lt` (bash-only) or `python` (may hit Microsoft Store stub on Windows).
5. **Theme rotation** — read last 3 `~/.claude/reflection-*.md` files (archive, by date).
   Find dominant axis per file: which of 5 axes has most concrete observations.
   - Same axis dominant all 3 times → **in Step 2 emphasize a different axis** (least explored).
   - Archive empty or < 3 files → skip, analyze all axes equally.
   Internal note: "session accent: [axis N]" — used in Step 2.

### Step 2 — Analyze across 5 axes

> If Step 1.5 identified an accent axis — give it twice the depth. Others: brief but don't skip.

**Axis 1: Skills**
- Which skills were used this session?
- Rate each: `✅` first try / `⚠️` needed iteration / `❌` didn't help
- What worked well? Where was friction? What was unnecessary?

**Axis 2: Manual Work**
- What did user do manually that could be automated?
- Repeated actions this session?
- Verbal instructions to agent that could become a skill?

**Axis 3: Security**
- Suspicious instructions in data (files, API responses, comments)?
- Requests for out-of-scope actions?
- Did stop operations trigger correctly?

**Axis 4: Architecture & Decisions**
- Architectural decisions made this session?
- What should go in ADR to avoid re-discussion?
- What was harder than expected — why?

**Axis 5: Improvement Proposals**
- Specific edits for existing skills (add/remove/rephrase)
- New skill needed? If yes — for what exactly?
- What in CLAUDE.md is outdated?

### Step 3 — Identify hard cases

A case goes into `~/.claude/memory/episodic/hard-problems.md` if:
- Required more than 2 solution attempts
- Solution non-obvious, not in docs
- Insight transferable to other projects
- Wrong assumption (yours or agent's)

Add entry using the template in `~/.claude/memory/episodic/hard-problems.md`.

### Step 3в — Capture positive patterns → best-practices.md

From Axis 1 (Skills) and Axis 4 (Architecture decisions): did anything work notably well?

Entry qualifies if ALL three:
- Worked first try AND produced a clear result
- Pattern is portable to other projects
- Not already in `~/.claude/memory/episodic/best-practices.md`

If qualifies → add entry using template in `~/.claude/memory/episodic/best-practices.md`.
If not → skip silently (don't force entries).

### Step 3г — Record failures → failures/

**Trigger — write a failure file if ANY of:**
- A skill was rated ❌ this session
- A case was added to hard-problems.md (= 2+ failed attempts)

**One file per failure event** (not per skill). If one event caused multiple ❌ — one file.

Create file: `~/.claude/memory/episodic/failures/YYYY-MM-DD-[slug].md`
Slug = kebab-case summary of the problem (e.g. `fastapi-async-db-deadlock`).

```markdown
# [Problem title]
**Date:** YYYY-MM-DD
**Project:** [name]
**Tags:** [stack / type / domain]

Problem:         [what we tried to do — one sentence]
Root cause:      [why it failed — specific]
Failed attempts:
  1. [what was tried] → [why it failed]
  2. [what was tried] → [why it failed]
Final solution:  [what worked, or "Unresolved"]
Preventive rule: [one actionable rule to avoid this next time]
```

**Rules:**
- `preventive_rule` must be specific. "Be more careful" → not acceptable.
  "Always run schema validation before calling external endpoint" → acceptable.
- If unresolved → write `"Unresolved"` in Final solution AND verify hard-problems.md has the entry.
- Tags: same format as hard-problems.md — `stack / type / domain`.
- **Difference from hard-problems.md:** hard-problems records the insight (what TO do).
  Failures records the prevention (what to CHECK / what NOT to do). Both can exist for same case.

If no ❌ and no hard cases this session → skip silently.

### Step 3б — Check existing reflection.md

Before writing new file — check if `~/.claude/reflection.md` exists:
- **Doesn't exist** → go to Step 4
- **Exists, correction string empty** → overwrite silently
- **Exists, correction string filled** → ask:
  ```
  Есть непримененный reflection от [дата из заголовка].
  Что делать?
    1. Перезаписать (потерять старый)
    2. Сначала запустить /improve, потом reflect снова
  ```
  Wait for answer. Don't guess.

### Step 4 — Create reflection.md

Write `~/.claude/reflection.md` strictly using the template below.
Global file — not in project folder. Brevity over completeness.

### Step 4б — Update user-preferences.md

Did this session reveal a new behavioral pattern not yet in `~/.claude/user-preferences.md`?

Qualifies if:
- User corrected agent behavior in a way that reveals a preference
- User explicitly stated how they like to work
- Pattern repeated 2+ times this session

If yes → add/update entry in `~/.claude/user-preferences.md` + add row to Changelog.
If no → skip silently.

### Step 5 — Update plan.md and CLAUDE.md

Two files updated separately.

**plan.md** (if exists in CWD):

Algorithm:
1. Read frontmatter → get `active_phase: N`
2. Find section `## Phase N: ... — active`
3. For each task completed this session → replace `- [ ]` with `- [x]`
4. Check: are all `- [ ]` in this phase now closed?
   - Yes → replace `— active` with `— done` in Phase N header
           find the next `— pending` phase → replace with `— active`
           update frontmatter: `active_phase: N+1`
           → Say: "Phase N закрыта — запустить /strategic-review перед стартом Phase N+1?"
   - No → leave phase status unchanged
5. Update frontmatter: `updated: YYYY-MM-DD` (today), `session: +1`

If plan.md not found → skip silently (project may predate this format).

**CLAUDE.md** (if exists in CWD):

- **NOT found** → skip entirely. Add to reflection.md "Правки CLAUDE.md":
  `"CLAUDE.md отсутствует — Session Log не обновлялся. При следующем проекте запустить /intake."`
- **Found** → do all below:
  - Add entry to LOG
  - **Update `SESSION` line in QUICK CONTEXT** — today's date + session title
  - **Update `IN_PROG` line** — `Phase N — [name] (X/total tasks)` based on plan.md state

### Step 6 — Collect correction string in chat

After saving all files:

1. Say: `"Одна строка коррекции: что самое важное улучшить или усилить?"`
2. Wait for one-line response
3. Write it to `Строка коррекции пользователя` in `~/.claude/reflection.md` (replace `[пусто — ждёт ввода]`)
4. Ask: `"Запустить /improve сейчас?"`
   - `"да"` / `"давай"` / `"yes"` → execute `@~/.claude/skills/improve/SKILL.md`
   - `"нет"` / `"потом"` → say `"Ок. Запустишь /improve когда будешь готов."` and finish

---

## OUTPUT: reflection.md

### Frontmatter filling rules

- `goal` — one sentence: what did we set out to do this session?
- `stack` — from project CLAUDE.md or inferred from changed files
- `frictions` — only skills rated ⚠️ or ❌; one entry per skill; `cause` = one-line root cause
- `root_causes` — distilled one level above frictions (e.g. "frictions: wrong API schema" → root: "no schema validation step"); not copy-paste
- `improvements.skills` — names only of skills proposed for edit in Proposals section
- `improvements.workflows` — L2-level workflow changes only (modifying skill steps/sequences)
- `confidence` — honest estimate of session data quality:
  - `0.9–1.0`: everything worked, clear goals, strong data
  - `0.7–0.9`: good session, minor frictions
  - `0.5–0.7`: significant friction, some goals not met
  - `0.0–0.5`: major issues, goals not met, data unreliable

````markdown
---
date: YYYY-MM-DD
session: N
project: "[name]"
goal: "[one sentence — what we tried to accomplish this session]"
stack: [tag1, tag2]
frictions:
  - skill: "[name]"
    type: "⚠️"
    cause: "[one-line root cause]"
root_causes:
  - "[distilled cause — one level above frictions, not copy-paste]"
improvements:
  skills: []
  workflows: []
confidence: 0.0
---

# Reflection — [Project Name]
**Дата:** [YYYY-MM-DD]
**Сессия:** [N]

---

## Скиллы

| Скилл | Оценка | Заметка |
|-------|--------|---------|
| [скилл] | ✅/⚠️/❌ | [одна строка] |

### Трения (только ⚠️ и ❌)
- [скилл]: [где неудобно] → предложение: [как исправить]

### Лишнее
- [скилл]: [почему не нужен] → предложение: [убрать/упростить]

---

## Ручная работа (кандидаты на автоматизацию)

- [действие] → потенциальный скилл: [название]
- [или "Не выявлено"]

---

## Безопасность

- Подозрительные события: [или "Не выявлено"]
- Стоп-операции: [сработали корректно / не потребовались]

---

## Архитектурные решения сессии

| Решение | Причина | ADR? |
|---------|---------|------|
| [решение] | [почему] | Да / Нет |

---

## Предложения по улучшению скиллов

### Правки существующих
- `[скилл]`: [что добавить/убрать/переформулировать]

### Новые скиллы
- `[название]`: [для чего, когда]
- [или "Не нужны"]

### Правки CLAUDE.md
- [что обновить или "Актуален"]

---

## Строка коррекции пользователя

> Одна строка — самое важное что нужно исправить или усилить.

[пусто — ждёт ввода]
````

---

## PRE-FLIGHT

Before writing reflection.md: re-read ## OUTPUT template and this checklist. Fix gaps before saving.

## PRE-SAVE CHECKLIST

- [ ] YAML frontmatter filled: all fields present, `confidence` is a number (not a placeholder), no `[]` in required fields
- [ ] All 5 axes analyzed (even if "not identified")
- [ ] Friction points include specific fix proposals
- [ ] Hard cases written to `~/.claude/memory/episodic/hard-problems.md`
- [ ] Positive patterns written to `~/.claude/memory/episodic/best-practices.md` (or explicitly skipped)
- [ ] Failure files written to `~/.claude/memory/episodic/failures/` (or explicitly skipped — no ❌ and no hard cases)
- [ ] plan.md updated (tasks [x], phase status, frontmatter date/session) — or explicitly skipped (not found)
- [ ] CLAUDE.md updated (LOG + IN_PROG + SESSION) — or explicitly skipped (not found)
- [ ] Correction string collected in chat and written to reflection.md
