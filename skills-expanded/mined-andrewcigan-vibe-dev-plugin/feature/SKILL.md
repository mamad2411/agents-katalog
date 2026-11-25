---
name: feature
description: Запуск работы над одной фичей (WIP=1). Авто-запускает test-researcher + user-perspective-critic (dual critique), читает domain-rules.yaml, error-journal, выбирает light/heavy path по размеру. Триггеры — "/feature <id>", "берём feat-X", "поехали по feat-Y".
when_to_use: Когда пользователь начинает работу над конкретной фичей из feature_list.json. Это основной рабочий цикл FAST и FULL pipeline.
---

# /feature <feature-id>

Запуск одной фичи. WIP=1 enforced — другую фичу взять нельзя пока эта не passing.

## Pre-flight checks

### Check 0: Enforcement жив? (v6.2 F2; discipline-слой, несущий канал — pre-commit backstop)

```bash
P="$(cat .harness/profile 2>/dev/null)"; HB=.harness/hooks-heartbeat
case "$P" in pending-*) echo "❌ профиль $P не подтверждён живым хуком — enforcement НЕ активен"; esac
[ -f "$HB" ] && [ $(( $(date +%s) - $(awk '{print $1;exit}' "$HB") )) -le 1800 ] \
  || echo "❌ heartbeat несвежий/отсутствует — хуки в этой сессии НЕ работают"
ls .harness/hook-crashes/ 2>/dev/null && echo "⚠️ сторожа падали — см. /doctor"
```

Любая строка с ❌ → **STOP**: запусти `/doctor`, почини активацию, потом возвращайся к фиче.
Работать над фичей при мёртвых сторожах = «харнес не поднялся» (главный провал аудита 06-10).

### Check 1: WIP=1

```bash
# Активная фича = запись со state "active" (верхнее поле «active» не читается с v9.0.4 —
# его не вёл ни один писатель состояния). Кроме этой фичи в active не должно быть никого.
python3 -c "
import json
d = json.load(open('feature_list.json'))
feats = d.get('features') or {}
buckets = feats.items() if isinstance(feats, dict) else [('', feats)]
other = [f.get('id') for b, lst in buckets if isinstance(lst, list) for f in lst
         if isinstance(f, dict) and (f.get('state') or ('active' if b == 'active_list' else '')) == 'active'
         and f.get('id') != '<this-feature-id>']
if other:
    print(f'❌ WIP=1 violated: уже в active: {\", \".join(map(str, other))}. Закрой через /verify до passing или переведи в paused.')
    exit(1)
"
```

Если нарушено — STOP, скажи пользователю.

### Check 2: Feature существует в captured/up_next

Если фича в `done` — спроси пользователя зачем заново.
Если фича в `superseded`/`rejected` — STOP.

### Check 3: Зависимости

```python
# Если feat.dependencies = ["feat-001", "feat-002"] — все должны быть в done
```

Если нет — предложить взять зависимости сначала.

## Размер и ПОВЕРХНОСТЬ фичи → light/heavy path

Из feature_list.json смотрим `size_estimate` И `surface` (v6.2 F5 — урок П2 аудита:
«зелёные тесты лгут» именно на интерфейсных фичах, которые по размеру проскакивали мимо критика):

- **S (<1 час, ~30 строк, 1 файл)** → **light path** (syntax + scope check, без dual critique)
- **M (1-4 часа, 30-200 строк)** → **medium path** (single critic + verify)
- **L (1+ день, >200 строк)** → **heavy path** (dual critique + 4-layer verify)

**Поверхность ПЕРЕБИВАЕТ размер (монотонно — только ужесточение):**
- `surface: ui` (или интерфейсные файлы в affected_files) → **user-perspective-critic ОБЯЗАТЕЛЕН
  при любом размере** + evidence «нажми и подтверди» (layer_4/5) до passing. UI-фича размера S
  не существует с точки зрения проверки: кнопку видит пользователь, не линтер.
- `surface: api|job|service|cli` → evidence реального вызова по lane-таблице
  ([rules/verification-lanes.md](../../rules/verification-lanes.md)) до passing.
- Поле surface заполняй при создании фичи; hook проверит монотонность (заявить `lib`
  при .tsx в diff нельзя — файловая эвристика остаётся полом).

## Main flow (heavy path — для L)

> ⚠️ **Порядок enforced хуком, а не дисциплиной.** `hooks/checks/state-transition.sh` БЛОКИРУЕТ
> перевод M/L-фичи в `active`, пока нет `docs/test-strategy.md` с её id. Поэтому критика идёт
> ПЕРВОЙ (фича остаётся в `up_next`), перевод в `active` — последним. Это test-first: стратегия
> проверки рождается до реализации. Закрывает H7 (раньше критику просили «по-доброму» — и пропускали).

### Шаг 1: Параллельный dual critique (фича ещё в up_next)

Запусти 2 subagent **параллельно** через Task tool (детерминированный вариант через Workflow — Шаг 3-bis):

**Agent 1: test-researcher (engineering critique)**
- Читает: feature description, CLAUDE.md, ARCHITECTURE.md, существующий код в affected_files
- Делает: параллельный GitHub-ресёрч «как тестируют похожие фичи»
- Возвращает: 3-7 тестов с verification_commands (1 happy + 2-3 edge + 1-2 error + 1 e2e)

**Agent 2: user-perspective-critic (top-down user perspective)**
- Читает: PRODUCT.md, domain-rules.yaml (особенно invariants, disambiguation_triggers, anti_patterns, target_markets)
- Делает: смотрит на фичу глазами реального пользователя
- Возвращает:
  - Какие сценарии test-researcher НЕ покрыл (но пользователь bы делал)
  - Какие domain-rules invariants не отражены в тестах
  - Top-down вопросы: «оптимизируем по правильной метрике?», «фиксим продукт или тест?», «работает ли при голосовом вводе по-русски?»

### Шаг 2: Synthesizer merge → docs/test-strategy.md (артефакт-gate)

Третий subagent (synthesizer) читает оба выхода и пишет `docs/test-strategy.md`:
- объединённый список тестов; конфликты (engineering X vs user Y) — в пользу user perspective
- **ОБЯЗАТЕЛЬНО упомянуть id фичи** в файле (хук проверяет наличие id — без него active заблокируется)
- final verification_commands → записать в feature_list.json

### Шаг 2-bis: data-model-reviewer (если фича трогает БД-схему)

Если `affected_files` содержит `*/schema/*`, `*/migrations/*`, `prisma/`, `drizzle/`, `supabase/migrations/` ИЛИ `category=data` — **ОБЯЗАТЕЛЬНО** запусти агента `data-model-reviewer` (Opus, fresh context) ПЕРЕД реализацией. Он пишет `docs/data-model-review.md` (недостающие/лишние сущности, упущенные поля, спорные решения, UX-фичи которые врут о связях). Утверждение пользователя по вердикту — gate для старта. Это глобальное правило `~/CLAUDE.md` (модель данных застывает — переделка дороже ревью).

### Шаг 2-ter: Стадия детализации (v8 L2-F2/F3 — обязательна на M/L)

Для **M/L-фичи** (и любой с `detail_required: true`) разложи детальный план в `docs/changes/<feat-id>/` по образцу OpenSpec (шаблон — `templates/change-proposal.md`):
- `proposal.md` — что/зачем + **User Stories с приоритетом P1..Pn**, каждая independently testable, с Acceptance в **Given/When/Then** (это основа `verification_command`). **Минимум одна P1-US с G/W/T** — иначе хук заблокирует переход в active (L2-F3).
- `tasks.md` — чек-лист задач (`- [ ]`); незакрытые блокируют архивацию при `/ship` (L3-F6).

Крупную фичу нельзя протаскивать без разложенного плана (c2). **S-фича** освобождена (light path) — детализация не форсится, пока не помечена `detail_required: true`. Backlog-фичи детали НЕ несут — она ленивая, рождается здесь при взятии в работу (L2-F4).

### Шаг 3: Перевести feature в active (хук теперь пропустит)

```python
# feature_list.json — активность задаёт ТОЛЬКО state записи; его читает сторож рамок коммита
# (diff ⊆ affected_files). Верхнее поле «active» не ставить: его никто не читает (v9.0.4).
d['features'][f]['state'] = 'active'
d['features'][f]['started_at'] = today
```

Хук пропустит запись, т.к. для M/L существуют И `docs/test-strategy.md` (Шаг 2), И `docs/changes/<id>/proposal.md` с P1-US (Шаг 2-ter). Если хук заблокировал — не пройдена критика (Шаг 1) ИЛИ детализация (Шаг 2-ter); вернись и доделай.

### Шаг 3-bis (опционально): Workflow-оркестрация критиков

Если в среде доступен **Workflow-инструмент** — критику лучше запускать детерминированным скриптом, а не вручную: `parallel([test-researcher, user-perspective-critic]) → synthesizer пишет docs/test-strategy.md`. Преимущество: скрипт спавнит критиков САМ (не «агент решит и пропустит»), barrier на артефакт. ⚠️ Контракт Workflow-инструмента внутри скилла проверить на первом реальном `/feature` (first-use, как Bash-хук). Гарантия H7 в любом случае — хук active-gate (Шаг 3), Workflow лишь усиливает оркестрацию.

### Шаг 4: Pre-launch checklist (если намечается bulk API)

Если в тестах будут массовые API-вызовы:
- Заполнить `.harness/pre-launch-checklist.yaml` (см. templates)
- Без passing checklist — implementation не стартует

### Шаг 5: Negative-verification gate

Для каждой verification_command — test-researcher специально вводит ошибку в код и проверяет что команда падает. Только потом — её записываем как валидную в feature_list.json. Иначе verification — театр.

### Шаг 6: Test-First (Карпати)

Сначала пишем тесты (red), потом implementation (green), потом refactor. Не наоборот.

### Шаг 7: Implementation в worktree (для L размера)

```bash
git worktree add ../worktrees/<feature-id> -b <feature-id>
cd ../worktrees/<feature-id>
# implementer работает здесь
```

Pre-commit hook проверяет: `diff ⊆ feature.affected_files`. Нарушение = block.

### Шаг 8: Periodic updates

Каждые 10 минут или ключевое событие → запись в SESSION.md секцию «Today». Не молчать.

### Шаг 9: /verify (4-layer)

Когда implementation готова — `/verify`. Прохождение всех 4 уровней = можно ставить state=passing.

## Medium / Light path

**Light (S)**:
- Без dual critique
- Тесты: 1 happy + 1 error (минимум)
- Skip negative-verification gate
- Verify: только layer 1 (syntax) + layer 2 (runtime)
- Без worktree, прямо в main

**Medium (M)**:
- Только test-researcher (без user-perspective-critic в параллель — но quick sanity read domain-rules.yaml)
- 3-5 тестов
- Negative-verification gate включен
- Verify: layers 1+2+3

## Stuck protection (защита от залипания)

Background watcher в init.sh запускается. Считает:
- Время без commit
- Время без test pass

Триггеры:
- 30 мин без progress → prompt в SESSION.md
- 45 мин без progress → auto /stuck
- 2 одинаковых fail подряд → auto параллельный subagent на диагностику (без ожидания /stuck)

## Anti-patterns

- ❌ Брать вторую фичу пока эта не passing (WIP=1 enforced)
- ❌ Скипнуть test-researcher для «маленькой» фичи если она L
- ❌ Помечать passing вручную без verification_command
- ❌ Молчать >10 мин в длинной задаче
- ❌ Расширять scope мимоходом («заодно поправлю смежный файл») — pre-commit hook блокирует
