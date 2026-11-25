# Skill: Skill Creator

**Purpose:** Create a new skill using the standard system template.
**When:** Improve Skill proposes a new skill, or user wants to automate a recurring action.
**Output:** Ready `~/.claude/skills/[name]/SKILL.md` + row in `~/.claude/skills/index.md`.

---

## PROCESS

### Step 1 — Ask 3 questions

```
Создаём новый скилл. Три вопроса:

1. НАЗВАНИЕ и назначение?
   Название — kebab-case (например: code-review, deploy, test-runner)
   Назначение — одно предложение: что делает и когда использовать

2. ТРИГГЕР?
   При каком условии этот скилл должен запускаться?

3. ЕСТЬ ЛИ ПОХОЖИЙ СКИЛЛ в ~/.claude/skills/index.md?
   Проверь индекс — если есть похожий, лучше расширить его
```

### Step 2 — Check for duplicates

Read `~/.claude/skills/index.md`.
If similar skill exists — offer to extend it instead:

```
Скилл [existing] уже делает [similar thing].
Предлагаю добавить [new behavior] в него, а не создавать отдельный.
Согласен?
```

### Step 3 — Check cross-cutting principles

Read `~/.claude/skills/cross-cutting-principles.md`.
Verify the new skill will satisfy every principle before generating.
Flag any principle that the skill design might violate — resolve before proceeding.

### Step 4 — Generate SKILL.md

Create file `~/.claude/skills/[name]/SKILL.md` using template:

````markdown
# Skill: [Name]

**Purpose:** [one sentence]
**When:** [trigger]
**Output:** [concrete artifact or action]

---

## PROCESS

### Step 1 — [First action]
[What agent does]

### Step 2 — [Next step]
[What agent does]

---

## OUTPUT

[Result template or description of expected output]

---

## CHECKLIST

- [ ] [quality criterion]
- [ ] [quality criterion]

---

## PRE-FLIGHT

Before delivering output, re-read ## RULES and ## CHECKLIST.
Verify output complies with every item. Fix before delivery.
````

### Step 5 — Update ~/.claude/skills/index.md

Add row in the correct group table:

```
| [name] | [purpose] | [tags] | 0 | ✅ Ready |
```

Tags: `meta` `loop` `start` `tools` `code` `test` `deploy` `review` `security` `data`

### Step 6 — Show result

```
Created: ~/.claude/skills/[name]/SKILL.md
Added to: ~/.claude/skills/index.md

Invoke: "@~/.claude/skills/[name]/SKILL.md" or "use skill [name]"
Optional: create ~/.claude/commands/[name].md?
```

---

## RULES

- One skill = one responsibility. Don't combine unrelated actions.
- Name in lowercase, kebab-case.
- Process must be step-by-step — agent must know what to do at each step.
- Output template required if skill creates a file.
- Checklist before final — minimum 2 criteria.
