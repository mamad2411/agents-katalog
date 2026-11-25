---
name: ssot-sync-closeout
description: Точечный post-stage sync в memory-bank и tasklist без переписывания истории.
user-invocable: true
allowed-tools:
  - Read
  - Bash(git *)
  - Bash(ls *)
  - Bash(find *)
  - Bash(grep *)
  - Bash(cat *)
  - Bash(npm *)
  - Bash(npx *)
  - Bash(curl *)
  - Bash(fuser *)
  - Bash(node *)
  - Bash(rg *)
  - Bash(jq *)
---

# Skill: SSOT Sync Closeout

## Triggers
- "обнови memory bank"
- "закрыть stage"
- "sync tasklist/context/progress"

## Objective
Поддерживать согласованность между:
- `memory-bank/context.md`
- `memory-bank/progress.md`
- `docs/tasklist/*`

## Workflow
1. Сверить факт stage (что реально выполнено и проверено).
2. Проверить acceptance evidence: subagent `DONE` не равен принятию результата;
   нужен scope/AC/checks verdict от Control Tower или Verifier.
3. Обновить `progress.md` новой записью (done + notes + checks).
4. Обновить `context.md` (current focus + next execution queue + date).
5. Обновить `decisions.md` если в текущем stage принято архитектурное/runtime решение.
6. Обновить delivery notes в tasklist.
7. Прогнать `rg` на противоречивые старые формулировки.
8. Для local-only ignored SSOT проверить, что Git их действительно игнорирует:
   `git check-ignore -v <paths>`.
9. Прямо проверить новые маркеры статуса/evidence через `rg -n` или `sed -n`,
   потому что `git diff` может быть пустым для ignored files.

## Constraints
- Historical entries не переписывать.
- Если проверки не запускались — писать это явно.
- Не добавлять ADR без реального архитектурного решения.
- В closeout явно указать, являются ли SSOT-изменения local-only/ignored и
  попадут ли они в публичную историю Git.

## Output
- 5-пунктовый stream summary
- Список измененных SSOT файлов
- Local-only/ignored статус SSOT файлов
- Residual risks

## Handoff
- **Success condition**: memory-bank обновлён (context, progress, decisions при наличии ADR), tasklist обновлён, нет противоречий.
- **Next**: Control Tower (closeout report to Owner)
- **Auto-proceed**: 🟢 YES
- **Hard stop**: NO
