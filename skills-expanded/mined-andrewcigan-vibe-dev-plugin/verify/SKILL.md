---
name: verify
description: Four-layer verification фичи. syntax → runtime → e2e → user-reported. Только passing all 4 = feature в done. Триггеры — "/verify", "проверь работает", "запусти тесты".
when_to_use: По завершению implementation фичи. Это единственный путь перевести feature_list.json state из active в passing.
---

# /verify

Four-layer verification (4-уровневая проверка) активной фичи.

## Layer 0: Enforcement жив? (v6.2 F2)

```bash
P="$(cat .harness/profile 2>/dev/null)"; HB=.harness/hooks-heartbeat
case "$P" in pending-*) echo "❌ профиль $P не подтверждён живым хуком"; esac
[ -f "$HB" ] && [ $(( $(date +%s) - $(awk '{print $1;exit}' "$HB") )) -le 1800 ] \
  || echo "❌ heartbeat несвежий — хуки в этой сессии НЕ работают"
```

❌ → СТОП: verify при мёртвых сторожах легко станет «зелёным враньём» (passing-гейт
не проверит evidence). Сначала `/doctor`.

## Layer 1: Syntax & Static Analysis

Минимальный gate, фундамент.

```bash
# JavaScript/TypeScript
npm run check          # tsc --noEmit
npm run lint           # eslint

# Python
ruff check .
mypy src/

# Common
git diff --check       # whitespace
```

Если хоть что-то красное — STOP, чинить.

## Layer 2: Runtime Behavior (unit + integration)

```bash
# из feature_list.json[active].verification.layer_2_runtime
npm test -- --filter=<feature>
# или
pytest tests/test_<feature>.py -v
```

Все тесты зелёные = pass.

## Layer 3: End-to-End

Закрывает lecture-10 (E2E меняет результат).

```bash
# Из feature_list.json[active].verification.layer_3_e2e
./e2e/test-<feature>.sh
# или
playwright test e2e/<feature>.spec.ts
# или chrome-devtools-mcp scenarios
```

Кейс из реального проекта: unit-тесты прошли 3/3, e2e нашёл 5 дефектов на границах. Этот слой не пропускать.

### Evidence по поверхности (v6.2 F5)

Тип доказательства обязан соответствовать `surface` фичи — полная таблица:
[rules/verification-lanes.md](../../rules/verification-lanes.md). Кратко: ui → браузер +
layer_4/5; api → curl + статус; cli → команда + exit; job → лог реального прогона;
service → behavior-probe (НЕ pgrep). Hook не пустит passing с пустым evidence у этих поверхностей.

**«Не могу прогнать живьём» → Live-Target Probe, 4 яруса** (см. ту же таблицу): найти живой
сервер → поднять самому → preview-деплой → только после задокументированного провала всех трёх —
честный `UNIT_VERIFIED` (не passing). Skip молча — не вариант.

## Layer 4: User-reported (НОВОЕ в v5.1)

Закрывает CRITICAL инсайт: «если verification passing, но пользователь говорит не работает — у нас плохие verification commands».

**Этот слой = реальное использование пользователем.**

Если layer 1-3 зелёные:
- Если фича без UI → автоматический pass (нет user-facing)
- Если UI → попросить пользователя протестировать кратко ОДИН раз
  - «Готово feat-XXX. Проверь поведенческий сценарий: <описание из verification.layer_4_user>. Работает?»
  - Ответ «да» → layer 4 pass
  - Ответ «нет / не так» → запись в error-journal.md + откат фичи в active + улучшение тестов

## Negative-Verification self-check

Перед промоушеном в passing — повторно прогнать negative-test:
```bash
# Специально внести ошибку → verification должна упасть
# Если verification всё равно зелёная — verification сломана, не код
```

Это единоразовая проверка на фичу. Закрывает реальный случай (ожидаемое значение «утекло» в контекст теста) и общий «verification not verified» gap.

## Adversarial verifier (v8 L5-F4) — независимый эшелон перед passing

Layer 1-4 + negative прогнал сам имплементатор — тот же агент, что писал код. Финальный слой — **независимый** свежий взгляд: запусти агента `stage-verifier` (fresh context, `disallowedTools=Write/Edit` — физически не может подгонять код) в **adversarial-режиме**.

- Передай ему **claim** (что фича делает — из feature.description + business_invariant) + **diff** фичи.
- Он работает по установке **assume broken until proven**: НЕ доверяет твоему «зелёному», прогоняет edge-cases сам (пустой/граничный ввод, error-пути, конкурентность, шов changed/unchanged) и возвращает **CONFIRMED** или **REFUTED** с repro.
- **REFUTED** → фича НЕ идёт в passing: заводишь дефект, чинишь (Шаг «Если что-то падает»), повторяешь /verify. **CONFIRMED** → можно в passing.

Обязателен на M/L (surface=logic/ui). На S — по усмотрению. Гарантия независимости — `disallowedTools` во фронтматтере (self-check раздел 4 флагует verifier с Write/Edit).

## State transition

Все 4 слоя + negative passed → feature_list.json:
```json
"state": "passing",
"evidence": {
    "layer_1_at": "ISO timestamp",
    "layer_2_at": "...",
    "layer_3_at": "...",
    "layer_4_at": "...",
    "negative_verified_at": "...",
    "commit_hash": "abc123"
}
```

Auto-commit:
```bash
git add -A
git commit -m "feat(<feature-id>): <feature-name>

Implements: <feature-id>
Verified-By: <verification_command_hash>
State-Transition: active→passing"
```

## Если что-то падает

### Counter увеличивается, до 3
```python
d['features'][f]['verify_attempts'] = d['features'][f].get('verify_attempts', 0) + 1
```

При **3 неуспешных попытках** на layer 2+3 (не syntax — syntax чинить сразу) → **auto-trigger /stuck**.

## Запись в error-journal

При любом fail записываем в error-journal.md:
```markdown
## err-NNN | <date> | <feature_id>
**Триггер**: verification fail (layer N)
**User reported**: no (auto-detected)
**5 Why**: 1) ... 5) корневая причина ...
**Класс ошибки**: <verification_gap / scope_leak / state_drift / ...>
```

## Anti-patterns

- ❌ Помечать passing если хоть один слой не зелёный
- ❌ Использовать `--skip-layer` флаги
- ❌ Игнорировать negative-verification self-check
- ❌ Скрывать verify_attempts от пользователя
- ❌ Считать что unit pass = feature passing (реальный случай: unit пройдены, e2e нашёл 5 дефектов на границах)
