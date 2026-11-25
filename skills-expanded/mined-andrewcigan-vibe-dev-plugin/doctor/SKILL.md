---
name: doctor
description: Самодиагностика enforcement — живы ли сторожа (хуки) в этом проекте. Проверяет профиль/heartbeat/краши/plugin. Триггеры — "/doctor", "проверь харнес", "хуки работают?", "почему сторожа молчат", "диагностика плагина".
when_to_use: Когда есть подозрение, что enforcement не активен (профиль pending, нет подтверждения активации после bootstrap, pre-commit заблокировал коммит, сторожа падали) или просто для проверки здоровья harness перед важной работой.
---

# /doctor — жив ли enforcement

Профиль строгости в файле — это заявление. Этот скилл проверяет ФАКТЫ: работают ли хуки
физически. Запускай диагностику сам (правило 8: не отправляй пользователя в терминал).

## Шаг 1: Снять показания (одним bash-блоком)

```bash
echo "=== Vibe Dev /doctor ==="
echo "— Папка: $(pwd)"
echo "— Vibe-проект: $([ -d .harness ] || [ -f feature_list.json ] && echo да || echo НЕТ)"
echo "— Профиль: $(cat .harness/profile 2>/dev/null || echo '(нет файла)')"
echo "— Движок проекта (пин): $(cat .harness/engine-version 2>/dev/null || echo '(нет — legacy)')"
PV=$(jq -r '.version // "?"' "${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json" 2>/dev/null)
echo "— Установлен плагин: ${PV:-?} ($(git -C "${CLAUDE_PLUGIN_ROOT}" log -1 --format='%h %cd' --date=short 2>/dev/null || echo 'не git-копия'))"
PIN=$(tr -d '[:space:]' < .harness/engine-version 2>/dev/null); PINMAJ="${PIN%%.*}"
SOFT=0; [ -z "$PIN" ] && SOFT=1
case "$PINMAJ" in ''|*[!0-9]*) : ;; *) [ "$PINMAJ" -lt 6 ] 2>/dev/null && SOFT=1 ;; esac
[ "$SOFT" = 1 ] && echo "— ⚠️ Проект в МЯГКОМ режиме (движок не закреплён/устарел, major<6) → /upgrade-project для полной строгости. Пин 6.x/7.x уже строгий — апгрейд не нужен (новые механизмы v7 работают и так)."
if [ -f .harness/hooks-heartbeat ]; then
  HB_TS=$(awk '{print $1; exit}' .harness/hooks-heartbeat); NOW=$(date +%s)
  echo "— Heartbeat: $((NOW - HB_TS))с назад ($(cat .harness/hooks-heartbeat))"
else
  echo "— Heartbeat: НЕТ (ни один хук ни разу не сработал в этом проекте)"
fi
echo "— Краши сторожей: $(ls .harness/hook-crashes/ 2>/dev/null | tr '\n' ' ' || echo нет)"
[ -f .harness/last-checkpoint.md ] && echo "— Слепок сжатия (M2): есть ($(awk -F'trigger=' '/trigger=/{print $2; exit}' .harness/last-checkpoint.md 2>/dev/null))"
# Аудит журнала (read-only, G5 + дешёвый дедуп): только отчёт, без правок.
bash "${CLAUDE_PLUGIN_ROOT}/scripts/journal-audit.sh" "$(pwd)" 2>/dev/null
[ -f .harness/hooks-disabled ] && echo "— ⚠️ hooks-disabled: backstop ОСОЗНАННО выключен"
# Где git реально ищет pre-commit: в рабочей копии (worktree) .git — файл, хуки общие с основной
# папкой; при перенаправленных хуках (core.hooksPath) — в их каталоге (v9.0.3).
PC="$(git rev-parse --git-path hooks/pre-commit 2>/dev/null)"
[ -n "$PC" ] && grep -q "Vibe Dev" "$PC" 2>/dev/null \
  && echo "— pre-commit backstop: установлен ($PC)" || echo "— pre-commit backstop: НЕ установлен${PC:+ ($PC)}"
# Подсказки сторожа коммитов называют скрипты плагина путём, вписанным при установке (v9.0.3).
if [ -n "$PC" ] && grep -q "Vibe Dev" "$PC" 2>/dev/null && [ -n "${CLAUDE_PLUGIN_ROOT}" ]; then
  BAKED="$(eval "$(grep -m1 '^VIBE_PLUGIN_ROOT=' "$PC")" 2>/dev/null; printf '%s' "${VIBE_PLUGIN_ROOT:-}")"
  [ "$BAKED" = "${CLAUDE_PLUGIN_ROOT}" ] \
    && echo "— pre-commit: подсказки ведут в этот плагин" \
    || echo "— ⚠️ pre-commit поставлен старой версией или плагин переехал (путь в копии: ${BAKED:-не вписан}): его подсказки называют команды, которых нет"
fi
# Копия проверки рамок фичи лежит в проекте и сама не обновляется (v9.0.4): копия до v9.0.4 читала
# мёртвое поле «active» и не проверяла ни одного коммита. Путь к плагину при этом мог быть верным.
SC="$(git rev-parse --show-toplevel 2>/dev/null)/.harness/hooks/pre-commit-scope.sh"
if [ -f "$SC" ] && [ -n "${CLAUDE_PLUGIN_ROOT}" ] && [ -f "${CLAUDE_PLUGIN_ROOT}/hooks/pre-commit-scope.sh" ]; then
  cmp -s "$SC" "${CLAUDE_PLUGIN_ROOT}/hooks/pre-commit-scope.sh" \
    && echo "— проверка рамок фичи: копия совпадает с плагином" \
    || echo "— ⚠️ проверка рамок фичи: копия в проекте отличается от плагина (поставлена старой версией)"
fi
echo "— Claude Code: $(claude --version 2>/dev/null || echo '(CLI не найден)')"
claude plugin list 2>/dev/null | grep -i vibe || echo "— Плагин: не виден в claude plugin list (или команда недоступна)"
```

## Шаг 2: Диагноз по таблице

| Симптом | Диагноз | Лечение |
|---|---|---|
| Профиль `pending-*` + heartbeat НЕТ | Хуки не работали ни разу: плагин не установлен/не включён, или сессия не в этой папке | `claude plugin list` → установить/включить; перезапустить сессию В папке проекта; первое сообщение активирует |
| Профиль `strict/standard` + heartbeat старше 30 мин | В ТЕКУЩЕЙ сессии хуки не работают (плагин выключили? `--safe-mode`? сессия в другой папке?) | Перезапустить сессию в папке проекта; проверить, что плагин enabled |
| Краши сторожей в `.harness/hook-crashes/` | Сторож падал — его проверки в те моменты НЕ выполнялись | Открыть лог, починить причину (или сообщить о баге плагина), удалить лог |
| pre-commit backstop НЕ установлен | Независимого канала нет — «театр строгости» не ловится на коммитах | `bash "${CLAUDE_PLUGIN_ROOT}/scripts/install-precommit.sh" "$(pwd)"` |
| pre-commit поставлен старой версией или плагин переехал | Подсказки сторожа коммитов называют команды, которых в проекте нет; так проект однажды написал собственного писателя истории, который голову истории не ведёт | `bash "${CLAUDE_PLUGIN_ROOT}/scripts/install-precommit.sh" "$(pwd)"` — переустановка вписывает путь к этому плагину (работает и из рабочей копии: хуки общие), прежний файл сохраняет рядом (`pre-commit.vibe-prev-<время>`, три последних) |
| Копия проверки рамок фичи отличается от плагина | Проект проверяет коммиты прежней версией проверки; копия до v9.0.4 не видела активную фичу и пропускала всё | `bash "${CLAUDE_PLUGIN_ROOT}/scripts/install-precommit.sh" "$(pwd)"` — копирует текущую проверку в `.harness/hooks/`; копия под git — закоммить её |
| `hooks-disabled` существует | Backstop выключен осознанно | Если работа в Claude Code возобновилась — удалить файл |
| Проект в мягком режиме (нет пина движка / major<6) | Структурные проверки только предупреждают, не блокируют. Пин 6.x/7.x уже строгий — не нудим | `/upgrade-project` (dry-run → пин на текущий мажор + strict). Новые механизмы v7 работают независимо от пина |
| Всё зелёное | Enforcement жив | Ничего не делать |

## Шаг 3: Доложить пользователю

Одной короткой сводкой без жаргона: «сторожа работают» / «сторожа НЕ работают, причина — X,
чиню так-то». Если чинится командой — выполни сам и перепроверь Шаг 1, потом докладывай.

## Границы честности

- Heartbeat пишут SessionStart и UserPromptSubmit: свежий heartbeat = хуки этих событий живы.
  Это сильное свидетельство и для остальных (один hooks.json), но не прямой тест каждого.
- Диагностика читает артефакты; она не может «включить» плагин сама — включение делает
  пользователь/рестарт сессии. Команды для этого давай готовыми, выполняй что можешь сам.
