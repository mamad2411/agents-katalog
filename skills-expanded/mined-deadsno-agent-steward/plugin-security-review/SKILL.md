---
name: Plugin Security Review
description: Security-ревью плагина agent-steward — секреты, HMAC-вебхуки, permissions, path safety, XSS в дашборде, инъекции в schtasks/cron, аудит и безопасность публикации. Использовать перед релизом и при правках core/permissions.
project: agent-steward
---

# Plugin Security Review

Специализированный скилл для проверок безопасности плагина. Не заменяет OWASP-аудит,
но закрывает реальные поверхности этого репозитория.

## Поверхности и проверки

1. **Секреты.** `src/core/secrets.ts`: AES-256-GCM, `secrets.json`, маскирование в логах,
   истории, аудите и подстановках в промпты. Тесты: `npm run test:secrets`, `test:audit`.
   Устаревшее утверждение «Secrets are not encrypted» в `docs/FEATURES.md` — ложное.
2. **Вебхуки.** HMAC-подпись, constant-time сравнение, replay-защита; тесты `test:integrations`.
3. **Permissions.** `defaultPolicy` hybrid/secure/legacy; `deniedTools` всегда побеждает;
   порядок `resolvePermissions`; ограничения субагентов (политика не наследуется); qualityGate/afterScript
   выполняются вне агента. Тест: `test:permissions-policy`, `test:role-scoped`, `test:profile-isolation`.
4. **Path safety.** Запись только в разрешённые каталоги, защита от `..`-traversal в watchPath,
   worktree, template, secrets. Тесты: `test:path-safety`, `test:watch-paths`, `test:worktree`.
5. **Дашборд.** `esc()` для всех пользовательских строк, CSP nonce, отсутствие inline-eval;
   тесты `test:dashboard-xss`, `test:dashboard-trust`. Smoke в Playwright: console/network без ошибок.
6. **ОС-команды.** сборка cron/schtasks/launchd команд без интерполяции непроверенного ввода;
   fail-closed watchdog, корректный argv после `--`. Тесты: `test:schtasks-*`, `test:cron-to-schtasks`,
   `test:prompt-argv`, `test:ps-watchdog`.
7. **Аудит и опубликованные артефакты.** Каждая мутация имеет audit-запись (90 дней / 10k);
   `secrets.json` не попадает в тарбол; `npm pack --dry-run` и `test-package-exports.mjs`;
   Least-privilege в `.github/workflows/release.yml` (OIDC, `--provenance`).

## Метод

- Сначала воспроизвести finding тестом или реальным запросом; без доказательства — статус
  «требует верификации».
- Для каждой находки: `<что>: <файл/проверка> — <P0|P1|P2>. Действие: <...>`.
- P0: утечка секрета, обход permissions, RCE через schtasks/cron, XSS с сохранением скрипта.
- P1: отсутствует аудит-запись, слабый HMAC, traversal без записи.
- P2: информационные улучшения.

## Ограничения

Это не замена полноценного OWASP/ASVS-аудита. При подозрении на уязвимость в V2 Plugin API
или OpenCode Core — использовать скилл `report` для корректного репорта, а не чинить в плагине.
