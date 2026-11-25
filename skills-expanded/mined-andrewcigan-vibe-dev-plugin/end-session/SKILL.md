---
name: end-session
description: Закрытие сессии одной командой. Полный handoff (5-dim clean-exit + memory sync + final commit) + готовая команда для рестарта в новой сессии. Триггеры — "/end-session", "/end", "закрываем сессию", "на сегодня всё", "конец сессии".
when_to_use: В конце сессии работы. Заменяет ручной /handoff + повторный старт Claude Code. После выполнения — пользователь получает одну команду для копипаста чтобы стартовать новую сессию в той же папке.
---

# /end-session

Однокомандное закрытие сессии. Обёртка над `/handoff` + auto-commit + restart helper.

> 🔒 **Режим закрытия (v6.2 F7).** Фраза закрытия уже включила closing-mode (хук поставил
> `.harness/locks/closing-mode`): запись возможна ТОЛЬКО в state-файлы (SESSION.md,
> feature_list.json, memory/, error-journal, .session-state/, docs/retrospectives|decisions),
> Bash — только git/read-only/скрипты плагина. Любая «дописать фичу напоследок» — BLOCK:
> новую работу фиксируй строкой в backlog. Режим снимет следующее сообщение пользователя
> без слов закрытия.

## Что происходит

### Шаг 1: Memory sync (E6 — критичный)

Перед запуском скрипта **обязательно**:

1. Открой `~/.claude/projects/<dashed-path>/memory/project_*.md` (если есть)
2. Обнови поля:
   - Pipeline stage (актуальная фаза)
   - Активные фичи (PASSING / active / blocked / paused)
   - Next command
   - MVP path
   - Архитектурные решения за сессию
3. Проверочный вопрос: «Если сейчас новая сессия сделает /resume — увидит cold-start то же что я вижу в SESSION.md?»

Если нет — обнови ДО продолжения. См. `rules/memory-stays-in-sync.md` (по правилу E6).

### Шаг 2: Промоушн уроков из error-journal

Прочитай `error-journal.md` (если есть). Группируй похожие записи. Для каждой группы:
- Класс ошибки
- Lesson scope (project / user / system)
- Предложи пользователю promotion одной строкой:

```
3 ошибки → 2 урока на promotion:
- "concurrent_writes_to_same_file" (project) — запишу в feedback_concurrent_writes.md
- "execute_dont_ask" (user) — confirm? (д/н)
```

При confirm — создай feedback_*.md в `~/.claude/projects/.../memory/`.

### Шаг 3: TTL cleanup в SESSION.md

Удалить из SESSION.md → Implementation Notes:
- Open Questions старше 5 рабочих дней (эскалировать как блокеры)
- Design Decisions старше 5 рабочих дней (продвинуть в `docs/decisions/` или удалить если неактуально)

### Шаг 4: Запуск bash скрипта

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/end-session.sh"
```

(скрипт автоматически возьмёт `pwd` как project path)

Скрипт делает:
- 5-dim clean-exit (build / tests / progress / artifacts / startup)
- .gitignore защита .env*
- Запись `.session-state/last-session.md`
- Auto-commit (с проверкой что секреты не в staged)
- Создаёт `restart-here.sh` в папке проекта
- Печатает готовую команду для рестарта

### Шаг 4б: Эстафета по направлениям (если волна разрезана)

Если в проекте есть `.harness/relay.json` — волна идёт эстафетой по направлениям
(решение владельца: направление = отдельная сессия). Закрывая сессию, передай эстафету:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/wave-relay.sh" done
```

Скрипт закроет текущее направление и назовёт следующее. В финальном сообщении скажи, какое
направление берётся дальше и какие именно задачи в него входят — границы лежат в файле,
а не в памяти, поэтому новая сессия начнёт ровно с них.

Если волна ещё не разрезана, а задач в очереди много — предложи разрезать:
`bash "${CLAUDE_PLUGIN_ROOT}/scripts/wave-relay.sh" plan`

### Шаг 5: Финальное сообщение пользователю

После завершения скрипта — финализируй шаблоном B (см. `rules/message-finalization.md`):

```
Готово. /end-session завершён clean. Commit: <hash>. Сессия упакована.

Следующий старт — одна из команд (скрипт уже напечатал):

  cd <папка-проекта> && claude

ИЛИ через restart helper:

  cd <папка-проекта> && bash restart-here.sh

После запуска — скажи /resume <project>, я подниму cold-start (5 вопросов из репо).

Вопросов от меня нет. Закрывай эту сессию когда готов. Доброго дня!
```

## Триггеры

- `/end-session`
- `/end`
- «закрываем сессию», «на сегодня всё», «конец сессии», «всё, заканчиваем»
- (опционально через auto-handoff-watcher) — 4 часа неактивности → автозапуск

## Когда применять

- Конец рабочего дня
- Перед длительным перерывом (>4 часов)
- Смена проекта (когда хочешь переключиться на другой)

## Когда НЕ применять

- Просто пауза 30 минут — не нужно, продолжишь в этой же сессии
- Если в середине активной /feature без verify — сначала /verify, потом /end-session

## Возвращение

В новой сессии после рестарта:
1. Claude Code открывается в папке проекта
2. Сразу скажи: `/resume <project>` — cold-start test (5 вопросов из репо через external evaluator)
3. Если cold-start ≥4/5 — продолжай работу
4. Если <4/5 — state разъехался, читай `.session-state/last-session.md` и SESSION.md вручную

## Anti-patterns

- ❌ Запускать /end-session без обновления memory project_*.md (E6 violation)
- ❌ Не делать промоушн уроков из error-journal (learning gap)
- ❌ Игнорировать warnings из 5-dim checks (накопление technical debt)
- ❌ Закрывать сессию с staged секретами в git

## Особые случаи

- **Если build/tests failed**: скрипт всё равно делает commit (handoff важнее), но записывает в SESSION.md Open Issues. Следующая сессия начнёт с починки.
- **Если в проекте нет CLAUDE.md / AGENTS.md** (не Vibe Dev проект): скрипт предупредит, но продолжит.
- **Если git не настроен**: skip auto-commit.

## Связано

- `skills/handoff/SKILL.md` — низкоуровневый handoff (вызывается под капотом)
- `rules/memory-stays-in-sync.md` — E6 правило
- `scripts/end-session.sh` — bash скрипт
- `rules/message-finalization.md` — формат финального сообщения
