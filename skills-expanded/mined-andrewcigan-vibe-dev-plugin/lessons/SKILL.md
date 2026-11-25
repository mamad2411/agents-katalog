---
name: lessons
description: Показать журнал ошибок и promoted уроки текущего проекта. Опционально — export в retrospectives. Триггеры — "/lessons", "что мы тут уже учли", "уроки", "ошибки".
when_to_use: Когда пользователь хочет посмотреть какие грабли уже найдены и зафиксированы. Также для экспорта в retrospectives при /ship или конце фазы.
---

# /lessons [export]

Управление подсистемой Learning — журнал ошибок и зафиксированные уроки.

## По умолчанию (без аргументов): показать

### Active errors (этой фазы / последние 30 дней)

```bash
# Парсим error-journal.md
# Показываем последние записи + статус promotion
```

Формат вывода в SESSION.md или в чате:
```
📓 Errors этой фазы: 7

Top-3 классы ошибок:
1. api_research (3) — закрыто? да (feedback_api_research_first.md)
2. concurrent_write (2) — закрыто? да (feedback_concurrent_writes.md)
3. scope_leak (2) — НЕ закрыто (нужен pre-commit hook)

Recurrence rate: 0% ✓ (или X% ⚠️)
Error velocity: 1.4/неделя
```

### Promoted lessons (память проекта)

```bash
ls ~/.claude/projects/<dashed-path>/memory/feedback_*.md
```

Показать список:
```
📚 Lessons в памяти проекта: <count>

- feedback_api_research_first.md (4 KB) — главный урок из проекта с документным ассистентом
- feedback_concurrent_writes.md (1.5 KB)
- feedback_no_technical_choices.md (3 KB)
- ...
```

### Глобальные уроки (применимые к пользователю)

```bash
cat ~/.claude/memory/MEMORY.md
```

## С аргументом `export`: выгрузить

`/lessons export` — собирает всё в один документ для анализа:

```bash
mkdir -p ~/.vibe-dev/retrospectives/YYYY-MM-DD-<project>-export/
cd ~/.vibe-dev/retrospectives/YYYY-MM-DD-<project>-export/

# Объединить
cat \
  <project>/error-journal.md \
  ~/.claude/projects/<dashed-path>/memory/MEMORY.md \
  ~/.claude/projects/<dashed-path>/memory/feedback_*.md \
  > ALL_LESSONS_<project>.md

# Создать summary
echo "# Lessons Summary <project>" > SUMMARY.md
echo "" >> SUMMARY.md
echo "Generated: $(date)" >> SUMMARY.md
# ... группировка по классам, частоте, severity
```

Файлы:
- `ALL_LESSONS_<project>.md` — полный архив
- `SUMMARY.md` — сводка с группировкой
- `RECURRENCE_ANALYSIS.md` — что повторялось и почему

## С аргументом `add "<urok>"`: вручную добавить урок

`/lessons add "при работе с Telegram-ботами всегда использовать webhook не polling"`:

- Создать `feedback_<auto_slug>.md` в `~/.claude/projects/.../memory/`
- Добавить строку в MEMORY.md этого проекта
- Спросить пользователя: «Это применимо ко всем твоим проектам? Если да — добавлю в ~/CLAUDE.md»

## Anti-patterns

- ❌ Дублировать урок если он уже в feedback файле
- ❌ Промоутить в ~/CLAUDE.md без confirm
- ❌ Удалять старые feedback файлы — это история, ценность

## Под капотом

- error-journal.md — live журнал текущего проекта
- ~/.claude/projects/<dashed-path>/memory/feedback_*.md — promoted уроки (закрытые)
- ~/.claude/projects/<dashed-path>/memory/MEMORY.md — индекс с указателями
- ~/.claude/memory/MEMORY.md — глобальный индекс пользователя
- ~/.vibe-dev/retrospectives/ — крупные ретроспективы
- ~/CLAUDE.md — системные правила (только confirmed)
