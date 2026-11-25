---
name: new-project
description: Старт нового проекта в Vibe Dev — бизнес-интервью + harness bootstrap (4 файла) + выбор FAST/FULL режима. Триггеры — "новый проект", "начнём новый", "стартуем", "/new-project".
when_to_use: Когда пользователь начинает новую разработку с нуля. Создаёт папку проекта с 4 harness-файлами и проводит первичное бизнес-интервью.
---

# /new-project

Запускает старт нового проекта по Vibe Dev архитектуре.

## Что происходит

### Шаг 0: Проверка портрета (как с тобой общаться)

Проверь, есть ли файл `~/.vibe-dev/portrait.md`. Если НЕТ — это первый запуск; предложи одной
фразой, не навязывая:
> Прежде чем строить — за минуту настрою, как мне с тобой разговаривать (6 коротких вопросов,
> разово). Сделать сейчас (`/setup`) или пропустить и работать на стандартном стиле?

- Согласен → запусти `/setup`, затем вернись к Шагу 1.
- Пропускает / портрет уже есть → сразу к Шагу 1 (без портрета работает нейтральный дефолт `medium`).

### Шаг 1: Подтверждение и выбор папки

Спроси у пользователя:
1. **Название проекта** (kebab-case, для папки) — ОДИН вопрос
2. **Тип проекта** (для выбора режима): «маркет-продукт / внутренний инструмент / эксперимент-пэт» — ОДИН вопрос

По ответу определяй режим:
- market product → **FULL** (10 этапов)
- внутренний / эксперимент / уверен в стеке → **FAST** (5 этапов)

### Шаг 2: Создать папку и harness bootstrap

```bash
cd <рабочая-папка>
mkdir <project-name>
cd <project-name>

# Скопировать 4 стартовых файла из templates/
cp ${CLAUDE_PLUGIN_ROOT}/templates/CLAUDE.md ./CLAUDE.md
cp ${CLAUDE_PLUGIN_ROOT}/templates/feature_list.json ./feature_list.json
cp ${CLAUDE_PLUGIN_ROOT}/templates/SESSION.md ./SESSION.md
cp ${CLAUDE_PLUGIN_ROOT}/templates/domain-rules.yaml ./domain-rules.yaml

# Harness-метка движка: новый проект рождается на актуальном движке = strict by default (H2).
# Проекты без этой метки = legacy (структурные проверки warn, UI-evidence всё равно hard),
# переводятся на strict командой /upgrade-project.
# Двухфазная активация (v6.2 F2): пишем pending-strict — в боевой strict переведёт ТОЛЬКО
# живой хук на следующем сообщении (факт перевода = доказательство, что enforcement активен).
# Если профиль остался pending-strict — хуки НЕ работают: НЕ продолжай молча, чини активацию (/doctor).
mkdir -p .harness
# Пин на АКТУАЛЬНЫЙ мажор плагина (динамически — новый проект не должен сам себе слать «обновись»).
echo "$(jq -r '.version // "7"' "${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json" 2>/dev/null | cut -d. -f1).0" > .harness/engine-version
echo "pending-strict" > .harness/profile

# Создать стандартный .gitignore сразу (closes security gap)
cat > .gitignore <<'EOF'
node_modules/
.env
.env.*
*.pem
*.key
secrets/
.harness/cost-log.json
.harness/tools-audit.jsonl
.harness/locks/
.DS_Store
EOF

# Init git
git init -q

# Pre-commit backstop (v6.2 F2): activation-страж + WIP=1 scope. Независимый канал —
# блокирует коммиты, если профиль строгости заявлен, а живые хуки не работают.
bash "${CLAUDE_PLUGIN_ROOT}/scripts/install-precommit.sh" "$(pwd)"

git add .
git commit -q -m "init: vibe-dev harness bootstrap"
```

После bootstrap скажи пользователю одной строкой: enforcement активируется на следующем
сообщении (профиль pending-strict → strict переведёт живой хук). Если в следующем ходе
НЕ появилось подтверждение активации — запусти `/doctor` и чини, не продолжай молча.

### Шаг 3: Бизнес-интервью (заполнение CLAUDE.md + domain-rules.yaml)

Пройди по блокам ниже. **ОДИН вопрос за раз.** Каждый ответ → сразу записываешь в файлы (не копи в чате).

**Блок 1: Главная функция**
- «Опиши одной фразой: что пользователь сможет делать в этом продукте?»
- → пиши в CLAUDE.md (первая строка после title)
- → дублируй в domain-rules.yaml → product_semantics.main_function

**Блок 2: Целевой пользователь и рынок**
- «Кто пользователь? География?»
- → если есть региональная специфика — пометь в domain-rules.yaml → target_markets (countries, languages)

**Блок 3: «Не-баги» и инварианты**
- «Что должно быть всегда так, как бы странно это ни выглядело со стороны? Что НЕ ошибка а фича?»
- → domain-rules.yaml → product_semantics.not_a_bug + invariants

**Блок 4 (только FULL): Бизнес-модель**
- «Платный или бесплатный? Кто платит?»
- → domain-rules.yaml + CLAUDE.md

**Блок 5: Бюджет**
- «Сколько готов потратить на LLM/инфраструктуру в месяц?»
- → domain-rules.yaml → cost_policy.monthly_total_budget_usd

**Блок 6: Канал доставки**
- «Telegram-бот? Веб? CLI? Десктоп?»
- → CLAUDE.md + предполагай стек (см. Шаг 4)

### Шаг 4: Tech-defaults (НЕ спрашивай пользователя — Quality > Speed)

По умолчанию:
- **Frontend**: Next.js + shadcn/ui + Tailwind v4 + Inter
- **Backend**: Node.js + TypeScript ИЛИ Python (по контексту)
- **Telegram бот**: aiogram (Python) ИЛИ Telegraf (Node)
- **Database**: Supabase (если облако) или PostgreSQL локально
- **AI**: Claude через подписку Claude Code (НЕ Anthropic direct API)
- **Deploy**: Vercel Free + DigitalOcean Droplet $4/мес
- **Email/file**: opendataloader-pdf, VoxCPM2 для TTS
- **UI-тесты**: chrome-devtools-mcp

**Объяви** пользователю одной фразой: «Беру стек X, потому что Y. Если хочешь иначе — скажи сейчас.»

### Шаг 5: Заполнить SESSION.md

- Last Updated: сегодня
- Active Feature: null (пока ни одной)
- Mode: FAST или FULL
- Notes for Next Session: «Завершено новое-проектное интервью. Дальше: /architecture»

### Шаг 6: Записать в реестр проектов

```markdown
- **<project-name>** — [одна фраза] | mode: FAST/FULL | started: YYYY-MM-DD
```

### Шаг 7: Запустить cold-start test (валидация что bootstrap прошёл)

```bash
./init.sh  # будет создан позже на /architecture, пропустить если ещё нет
```

Прочитай CLAUDE.md обратно, убедись:
- ≤200 строк ✓
- 4 файла существуют ✓
- domain-rules.yaml заполнен ключевыми полями ✓

### Шаг 8: Финальное сообщение пользователю

```
✓ Проект <name> создан в <рабочая-папка>/<name>
✓ Harness bootstrap: 4 файла (CLAUDE.md, feature_list.json, SESSION.md, domain-rules.yaml)
✓ Режим: FAST (5 этапов) / FULL (10 этапов)
✓ Стек: <выбранный>

Дальше: /architecture — V0 архитектура + TOC bottleneck-анализ.

Прежде чем продолжить — есть ли специфика ниши которую важно сразу записать в domain-rules.yaml?
(например: "у нас СНГ", "клиенты с глюками в ИНН", "продаём через Telegram") — ОДНО предложение если есть.
```

## Anti-patterns (не делай так)

- ❌ НЕ задавать technical A/B (Postgres vs Mongo) — выбирай сам, объясняй последствия
- ❌ НЕ задавать больше 1-2 вопросов за раз
- ❌ НЕ создавать `.planning/` папку (v5 убрал)
- ❌ НЕ создавать INBOX.md (нет Telegram-дайджеста)
- ❌ НЕ создавать BUSINESS-RATIONALE.md (дублирует DECISIONS.md)
- ❌ НЕ заполнять domain-rules.yaml целиком на старте — только ключевое, остальное дополнится
- ❌ НЕ запрашивать у пользователя дедлайны или сроки

## Когда сработать

- Пользователь сказал: «новый проект», «начнём новый», «стартуем проект X», «/new-project»
- Текущая папка пустая или есть только `.git`
- Нет CLAUDE.md в текущей директории
