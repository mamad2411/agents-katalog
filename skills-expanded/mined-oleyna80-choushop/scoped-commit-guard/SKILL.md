---
name: scoped-commit-guard
description: Безопасный commit в dirty worktree только по whitelist файлам.
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

# Skill: Scoped Commit Guard

## Triggers
- "scoped commit"
- "грязное дерево"
- "не захвати лишнее"

## Objective
Сделать предсказуемый commit без утечки чужих/вне-scope изменений.

## Workflow
1. Зафиксировать whitelist файлов stage.
2. `git add <whitelist only>`.
3. Проверить staged set через `git status --short -- <whitelist>`.
4. Проверить diff только по whitelist.
5. Для security-sensitive staged set выполнить `scripts/secret-scan.sh staged`,
   если скрипт доступен, или зафиксировать эквивалентную staged-diff проверку.
   Минимум: проверить staged diff на `DATABASE_URL`, `token`, `secret`,
   `password`, `api_key`, `api-key`, `PRIVATE KEY`, `BEGIN RSA`,
   `BEGIN OPENSSH`, `BEGIN EC`. Любое совпадение должно быть удалено или явно
   классифицировано как benign public identifier до commit.
6. Сделать commit с осмысленным message.
7. Попытка push; при SSH fail — передать точную ручную команду.

## Constraints
- Запрещено: `git add .`, `git commit -a`, `git reset --hard`, `git checkout -- .`.
- Не включать untracked noise (`.cache`, `output`, browser artifacts).
- Не включать `.env`, private keys, credentials, tokens, connection strings,
  raw DB dumps, provider payload dumps, or full client/admin messages.

## Output
- Commit hash + message
- Файлы в commit
- Push status (ok / manual required)

## Handoff
- **Success condition**: commit сделан только по whitelist, hash зафиксирован.
- **Next**: Control Tower (продолжение pipeline) или vps-registry-pull-deploy (если далее нужен deploy)
- **Auto-proceed**: 🟢 YES
- **Hard stop**: NO
