---
name: handoff
description: Закрытие сессии по 5-dimensions clean-exit (build / tests / progress / artifacts / startup) + группировка ошибок + предложение promotion в память. Триггеры — "/handoff", "закрываем", "на сегодня всё", "пора заканчивать".
when_to_use: В конце сессии, перед закрытием Claude Code или сменой проекта. Также auto-trigger на tmux detach. Без этого — следующая сессия начнётся с хаоса.
---

# /handoff

5-dimensions clean-exit. Закрывает боль «забываю что делал».

## 5 dimensions check

### 1. Build
```bash
# Проект собирается без ошибок
npm run build
# или эквивалент
```

### 2. Tests
```bash
# Все тесты зелёные (existing + новые)
npm test
```

### 3. Progress
- SESSION.md обновлён (Today / What's Done / What's In Progress / What's Next)
- feature_list.json обновлён (state changes, evidence)
- error-journal.md обновлён если были ошибки

### 4. Artifacts
```bash
# Нет stale temp файлов
find . -name "*.tmp" -mtime -1
find . -name ".DS_Store" -delete

# Секреты не в git
git status | grep -i "\.env\|secret\|key" || echo "✓ no secrets staged"
```

### 5. Startup
```bash
# Следующая сессия сможет запустить ./init.sh с нуля
# Симуляция:
git stash
./init.sh
git stash pop
# Если упало — что-то не в репо
```

## Если что-то не закрыто

Запиши в SESSION.md секцию `# Open Issues`:
```markdown
## Open Issues (handoff не чистый)
- [ ] Tests падают: <которые> — нужен fix в feat-XXX
- [ ] Build падает: <причина>
- [ ] Нет evidence для feat-YYY
```

Следующая `/resume` сразу увидит и предложит починить ДО продолжения.

## Группировка ошибок этой сессии

Прочитай error-journal.md записи **этой сессии** (по timestamp):
- Сгруппируй по `Класс ошибки`
- Для каждой группы: можно ли извлечь урок?

## Promotion в память

Для каждого извлекаемого урока:

**Lesson scope: project**
- → `~/.claude/projects/<dashed-path>/memory/feedback_<slug>.md`
- → Добавить строку в MEMORY.md этого проекта

**Lesson scope: user**
- → `~/.claude/memory/MEMORY.md` (глобальная)
- Например: «пользователь предпочитает state-machine over tool_use»

**Lesson scope: system**
- → Предложение пользователю: «Заметил системный паттерн X. Добавить в ~/CLAUDE.md? Это будет применяться во всех проектах»
- НЕ записывать без явного confirm

**Финальная фраза**: одной строкой пользователю:
```
Сессия закрыта. 3 ошибки → 2 урока для памяти:
- "concurrent_writes_to_same_file" (project) — записал в feedback_concurrent_writes.md
- "execute_dont_ask" (user) — confirm? (д/н)
```

## TTL cleanup в SESSION.md

Удалить из секции `Implementation Notes`:
- Open Questions старше 5 рабочих дней — эскалировать как блокер
- Design Decisions старше 5 рабочих дней — продвинуть в `docs/decisions/` или удалить если уже неактуально

## Auto-commit

```bash
git add -A
git commit -m "handoff: session $(date +%Y-%m-%d)

- Active feature: <id>
- Sessions today: $(grep -c 'Today' SESSION.md)
- Errors logged: <count>
- Lessons promoted: <count>

Co-Authored-By: Vibe Dev"
```

## Cold-start prep

Заполнить в SESSION.md секцию `# Cold-Start Test (next session)` — обновить 5 ответов на вопросы из `.harness/cold-start.yaml`. Чтобы при `/resume` evaluator-agent имел свежий референс.

## Финальное сообщение пользователю

```
✓ /handoff завершён

📊 Сессия: <duration>
✓ Build / Tests / Progress / Artifacts / Startup — all green
📝 Errors → lessons: <X promoted>
💰 Cost this session: $X.XX
⏰ Open Issues для следующей: <count>

Cold-start готов. Можно отдыхать.
```

## Anti-patterns

- ❌ Закрывать без всех 5-dim
- ❌ Не записывать Open Issues при не-чистом выходе
- ❌ Промотировать урок в `~/CLAUDE.md` без confirm пользователя
- ❌ Скипать TTL cleanup (накапливается)
- ❌ Auto-commit когда есть .env в staged

## Auto-trigger

Скрипт `scripts/auto-handoff-watcher.sh` слушает:
- tmux detach session-end signal
- 4 часа неактивности без явного pause

→ Автоматически запускает /handoff (с user notify).
