---
name: cv-bot
description: Work with the student CV Telegram workflow in hh-autoparcer. Use for questions about a student's CV status, workflow order, current responsible role, required data, or final links; for diagnosing @veu_support_bot commands, access errors, task buttons, and Telegram notifications; for reviewing or changing CV processing transitions, role permissions, protected bot API endpoints, and NocoDB persistence; and for CV workflow tests or documentation updates. Do not use for HH vacancy autoresponse orchestration or unrelated web-console features.
---

# CV Bot

## Сбор контекста

1. Полностью прочитать `docs/resume-workflow.md` как основную документацию процесса.
2. Для отправки, Bot API ошибок и команд также прочитать `docs/telegram-integration.md`.
3. Не полагаться на сохранённое описание поведения: перед выводами сверять документацию с актуальным кодом.
4. Читать только файлы, относящиеся к задаче, по карте ниже.
5. Если документация расходится с кодом, сообщить пользователю о расхождении и дождаться ответа перед продолжением.

## Карта файлов

- `docs/resume-workflow.md` — команды, роли, статусы, поля NocoDB, API, настройки, тестирование и ошибки.
- `docs/telegram-integration.md` — типизированный контракт отправки, failure stages, команды, endpoints и reporting.
- `src/integrations/telegram/resume-workflow.ts` — модель статусов, переходы, проверки ролей, обязательные данные и уведомления.
- `src/integrations/telegram/support-bot.ts` — Telegram-команды, callback-кнопки и вызовы защищённого API.
- `src/integrations/telegram/integration.ts` — shared Bot API facade и command registry.
- `src/features/web-console/backend/app.ts` — HTTP endpoints CV workflow и отправка уведомлений.
- `src/features/web-console/backend/types.ts` — типы клиента, platform accounts, provider-visible данных и `CV processing`.
- `src/features/web-console/backend/repository.ts` — чтение и запись `CV processing` в NocoDB.
- `src/features/web-console/frontend/src/App.vue` — ЛК клиента: профиль, platform accounts, provider drawer.
- `src/features/web-console/frontend/src/styles.css` — стили профильной формы, repeatable education и provider drawer.
- `src/integrations/noco/resume-workflow-schema/` — проверка/создание NocoDB-полей CV workflow и platform option `github`.
- `src/integrations/telegram/support-bot.test.ts` — тесты команд и поведения support-бота.
- `src/integrations/telegram/integration.test.ts` — unit и compile-time контракт Telegram facade.
- `src/integrations/telegram/resume-visible-e2e.test.ts` — изолированные E2E-тесты CV workflow.
- `src/integrations/telegram/resume-visible-e2e.ts` — живой видимый Telegram E2E-сценарий.
- `src/features/web-console/backend/app.test.ts` — тесты защищённого API и переходов.
- `src/features/web-console/backend/telegram-integration-routes.test.ts` — endpoint/auth contract.
- `src/features/web-console/e2e/web-console.e2e.ts` — браузерный e2e ЛК клиента и provider-visible деталей.
- `.env.example` — переменные `RESUME_WORKFLOW_*` и связанные настройки.
- `package.json` — команды запуска и тестирования.

## Выбор файлов по задаче

- Для вопроса о порядке работы прочитать документацию и `resume-workflow.ts`.
- Для вопроса о Telegram-команде прочитать `support-bot.ts` и соответствующий тест.
- Для вопроса об отправке или Telegram-ошибке использовать skill `telegram-bot` и shared integration; не создавать второй HTTP-клиент.
- Для вопроса об API прочитать `app.ts`, `app.test.ts` и типы backend.
- Для вопроса о данных или статусе в NocoDB прочитать `repository.ts` и схему `CV processing`.
- Для изменения клиентских обязательных данных прочитать `types.ts`, `repository.ts`, `App.vue`, web e2e и schema helper.
- Для изменения поведения прочитать весь путь от команды до NocoDB и затронутые тесты.

## Инварианты

- Считать `CV processing.status` источником истины для статуса CV.
- Сохранять продвижение ровно на один этап за действие.
- Сохранять разграничение ролей ученика, Киры, основного подрядчика и переводчика русской версии.
- Не повторять и не откатывать завершённый переход из-за неясного результата Telegram notification.
- Сохранять существующий warning/error path для сбоя уведомления.
- Считать истечение 30-минутного task context нормальным событием без error alert.
- Не записывать фиктивные ссылки и комментарии в обычном режиме.
- Не включать `RESUME_WORKFLOW_FAKE_DATA_MODE` в production или ручной приёмке.
- Не запускать живой `tg:resume:e2e:test-user` на реальных аккаунтах без явного запроса пользователя.
- Перед любой живой операцией проверить режим (`test` или `production`), конкретного клиента и Telegram-чат.

## Изменения и проверка

1. Вносить минимальные изменения в нужный слой.
2. Обновлять `docs/resume-workflow.md`, если меняются команды, статусы, роли, поля, API или процедура тестирования.
3. Запускать ближайшие целевые тесты; для более широких изменений использовать команды из раздела `Automated Tests` документации.
4. В отчёте указывать изменённый переход, ответственного, хранилище данных и выполненные проверки.
