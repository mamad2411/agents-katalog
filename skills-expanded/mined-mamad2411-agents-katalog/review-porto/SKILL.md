---
name: review-porto
description: Code review для Hyper-Porto проекта. Проверяет архитектуру, Result[T,E], UoW, импорты, DTOs, CQRS паттерны. Use when user says "проверь код", "code review", "ревью", "review porto", "проверь архитектуру", or asks to review code in Hyper-Porto project.
---

# Code Review для Hyper-Porto

Проверка кода на соответствие архитектуре.

## Источники (ОБЯЗАТЕЛЬНО загрузи перед выполнением)

| Тип | Путь |
|-----|------|
| **Checklist** | `agent-os/checklists/code-review.md` |
| **Anti-patterns** | `agent-os/anti-patterns/common-mistakes.md` |
| **Standards** | `agent-os/standards/` |
| **Docs** | `docs/03-components.md`, `docs/04-result-railway.md` |

## Формат Feedback

```
🔴 Critical — обязательно исправить
🟡 Suggestion — рекомендуется улучшить
🟢 Nice to have — опционально
```

## Что проверять

### 1. Архитектура
- [ ] Импорты **абсолютные** от `src.`
- [ ] Нет импортов между Containers (только Events)
- [ ] Компоненты в правильных папках
- [ ] Именование по конвенции

### 2. Actions
- [ ] Возвращает `Result[T, E]`
- [ ] Использует UoW (`async with self.uow:`)
- [ ] События через `uow.add_event()`
- [ ] Декоратор `@audited` если нужен

### 3. Queries (CQRS)
- [ ] НЕ возвращает Result
- [ ] НЕ использует UoW
- [ ] Метод `execute()`, не `run()`

### 4. DTOs
- [ ] Pydantic `BaseModel` (не dataclass!)
- [ ] Request с валидацией
- [ ] Response с `from_entity()`
- [ ] Error с `http_status`

### 5. Async
- [ ] `anyio` вместо `asyncio`
- [ ] `anyio.to_thread` для CPU-bound

## Red Flags 🚩 (Critical)

| ❌ Запрещено | ✅ Правильно |
|--------------|-------------|
| `from ....` (relative) | `from src.Containers...` |
| `raise Exception()` | `return Failure(Error())` |
| `@dataclass` для DTO | `class X(BaseModel)` |
| `asyncio.create_task()` | `anyio.create_task_group()` |
| Direct module import | Events для cross-module |

## Review Template

```markdown
## Code Review: {файл}

### Summary
{краткое описание}

### Findings

🔴 **Critical**
- {issue}: {описание} → {как исправить}

🟡 **Suggestion**
- {recommendation}

### Verdict
{APPROVED / NEEDS CHANGES / BLOCKED}
```
