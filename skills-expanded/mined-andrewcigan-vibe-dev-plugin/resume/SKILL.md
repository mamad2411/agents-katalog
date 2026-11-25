---
name: resume
description: Возврат к проекту после паузы. Запускает cold-start test (5 вопросов) + diff с прошлой сессией + восстановление контекста. Триггеры — "вернёмся к X", "продолжаем", "/resume <project>".
when_to_use: Когда пользователь возвращается к ранее начатому проекту, особенно после паузы >1 дня. Восстанавливает state и проверяет что harness не разъехался.
---

# /resume <project-name>

Подхват проекта после паузы. Закрывает боль «вернулся через неделю — не помню что делал».

## Что происходит

### Шаг 0: Enforcement жив? (v6.2 F2)

```bash
P="$(cat .harness/profile 2>/dev/null)"; HB=.harness/hooks-heartbeat
case "$P" in pending-*) echo "❌ профиль $P не подтверждён живым хуком — enforcement НЕ активен"; esac
[ -f "$HB" ] && [ $(( $(date +%s) - $(awk '{print $1;exit}' "$HB") )) -le 1800 ] \
  || echo "❌ heartbeat несвежий/отсутствует — хуки в этой сессии НЕ работают"
ls .harness/hook-crashes/ 2>/dev/null && echo "⚠️ сторожа падали в прошлых сессиях — см. /doctor"
```

Любая строка с ❌ → СНАЧАЛА `/doctor` и починка активации, потом resume. Продолжать
с мёртвыми сторожами = строгость только на бумаге.

### Шаг 1: Cold-start test (внешний evaluator)

Запусти subagent (Sonnet, fresh context, не видит .harness/assessment.json) с инструкцией:

```
Прочитай только: CLAUDE.md, feature_list.json, SESSION.md, domain-rules.yaml, 
docs/PRODUCT.md (если есть), error-journal.md (если есть).

Ответь на 5 вопросов из .harness/cold-start.yaml (или templates если файла нет):
1. Что это за продукт и для кого?
2. Какой сейчас bottleneck по 7-tuple?
3. Какая фича active + verification_command?
4. Какие 3 последних архитектурных решения и почему?
5. Какие anti-patterns (что НЕ делать)?

Грейдинг: 1-5 по каждому. Pass threshold = 4/5.
```

### Шаг 2: Анализ результата

- **Pass (≥4/5)**: state здоров, продолжаем
- **Fail (<4/5)**: state разъехался — нужен `/handoff` recovery + спросить пользователя что было

### Шаг 3: Diff с прошлой сессией

```bash
# Последний git commit
git log -1 --format='%h %ai %s'

# Что менялось с last_session
LAST_SESSION_END=$(grep "Last Updated" SESSION.md | head -1)
git log --since="$LAST_SESSION_END" --oneline
```

### Шаг 4: Прочитать error-journal (если есть)

Если `error-journal.md` существует — прочитай последние 5 записей. Это для context awareness — какие грабли уже найдены.

### Шаг 5: Прочитать memory проекта

```bash
# Системная память проекта
ls ~/.claude/projects/<dashed-path>/memory/
cat ~/.claude/projects/<dashed-path>/memory/MEMORY.md
```

Прочитай feedback_*.md — это уроки из прошлого.

### Шаг 6: Запустить init.sh (verification что окружение здорово)

```bash
./init.sh
```

Если падает — сначала чинить, потом возобновлять разработку.

### Шаг 7: Отчёт пользователю

```
✓ /resume <project>: state восстановлен

📊 Cold-start: 5/5 (или N/5 с указанием что упало)
📋 Active feature: feat-XXX (verification: <command>)
🎯 Bottleneck: <subsystem> (out of 7-tuple)
⚠️  Active blockers: <count> (из SESSION.md)
💰 Cost spent in project: $X.XX
📚 Lessons learned: <count> (из feedback_*.md)

Что менялось с last session (YYYY-MM-DD):
- <commit 1>
- <commit 2>

Дальше: продолжить feat-XXX или /audit для общей оценки?
```

## Anti-patterns

- ❌ НЕ продолжать работу если cold-start fail без обсуждения с пользователем
- ❌ НЕ скрывать что state разъехался ради «давайте просто продолжать»
- ❌ НЕ предлагать technical A/B что чинить первым — Quality > Speed, сам реши

## Когда сработать

- Пользователь сказал: «вернёмся к X», «продолжим Y», «открой Z», «/resume X»
- Прошло >1 дня с последней сессии
- CLAUDE.md существует в указанной папке
