---
name: skill-generator
description: Create new Claude Code skills with proper structure and best practices. Use when the user wants to create a new skill, extend Claude's capabilities, or needs help structuring a SKILL.md file.
---

# Skill Generator

Generate concise, focused Claude Code skills through guided questions.

## Process

Follow these steps:

### 1. Understand the Purpose

Ask:
- "What should this skill help you accomplish?"
- "Give me 2-3 concrete examples of when you'd use it"
- "What would you say to Claude to trigger this?"

### 2. Recommend Structure

Based on use cases:
- **Workflow-based**: Sequential steps (pipeline, workflow)
- **Task-based**: Distinct operations (toolkit with separate commands)
- **Reference/Guidelines**: Standards or specs to follow
- **Capabilities-based**: Integrated system with related features

### 3. Recommend Resources (if needed)

- **Scripts** (`scripts/`) - for automation or repetitive code
- **References** (`references/`) - for API docs, schemas, specs
- **Assets** (`assets/`) - for templates or boilerplate

Most simple skills don't need resources.

### 4. Generate SKILL.md

Create directory and SKILL.md:

```bash
# Personal: ~/.claude/skills/[skill-name]/
# Project: .claude/skills/[skill-name]/
```

**SKILL.md template** (краткость — цель <200 строк):

```yaml
---
name: [hyphen-case-name]
description: [Что делает + когда использовать + триггерные слова]
---

# [Название скилла]

[1-2 предложения — суть]

## [Основная секция]

[Инструкции — конкретно, без воды]

### [Подсекция если нужна]

[Примеры важнее объяснений]
```

**Key requirements:**
- Description includes what, when, and triggers
- Use hyphen-case for name
- Keep concise - split long content to references/
- Provide examples over explanations
- Validate YAML frontmatter

### 5. Валидация и интеграция в систему

**Чеклист качества — проверь перед финальным показом:**

- [ ] Язык: скилл написан на русском (кроме технических терминов и кода)
- [ ] YAML frontmatter валиден: `---` на отдельных строках, name в hyphen-case
- [ ] Description содержит: что делает + когда использовать + триггерные слова
- [ ] Объём: SKILL.md < 200 строк (длинное → в `references/`)
- [ ] Уникальность: проверь `~/.claude/skills/index.md` — нет ли дубликата
- [ ] Примеры есть — не только объяснения

**Обнови index.md** (`~/.claude/skills/index.md`):
Добавь строку в нужную группу:
```
| `[name]` | [назначение] | [теги] | 0 | ✅ Ready |
```

**Обнови dispatch-таблицу** в `~/.claude/CLAUDE.md` (Правило 4):
Если у скилла есть чёткие триггеры — добавь строку в таблицу:
```
| [триггер в запросе пользователя] | `[name]` |
```
Если триггеры размытые — пропусти, не засоряй таблицу.

**Финальный вывод:**
```
Создан: ~/.claude/skills/[name]/SKILL.md
index.md: обновлён ✓
dispatch-таблица: [обновлена ✓ / пропущена — размытый триггер]

Для использования: перезапусти Claude Code
Тест: "[пример триггерной фразы]"
```

## Quick Templates

**Workflow-based:**
```markdown
## Workflow
### Step 1: [Action]
### Step 2: [Process]
### Step 3: [Output]
```

**Task-based:**
```markdown
## Tasks
### 1. [Task]
[Brief description + example]
### 2. [Task]
[Brief description + example]
```

**Reference/Guidelines:**
```markdown
## Guidelines
### [Category]
[Standard/spec + example]
```

## Best Practices

**Effective descriptions:**
- State what it does + when to use + trigger words
- ✅ "Extract PDF text, fill forms, merge docs. Use when working with PDFs."
- ❌ "Helps with data" (too vague)

**Keep it concise:**
- Aim for <200 lines in SKILL.md
- Move details to references/ files
- Prefer examples over lengthy explanations

**Resource organization:**
```
skill-name/
├── SKILL.md           # Main (required)
├── references/        # Docs (optional)
├── scripts/          # Utils (optional)
└── assets/           # Templates (optional)
```

## Common Issues

- **Skill not triggering**: Add more trigger keywords to description
- **YAML invalid**: Check `---` markers are on their own lines
- **Scripts fail**: `chmod +x scripts/*.py`
