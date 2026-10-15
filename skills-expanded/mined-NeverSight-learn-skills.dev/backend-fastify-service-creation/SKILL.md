---
name: backend-fastify-service-creation
description: Guides implementation of Fastify backend services using the project architecture with src/modules, src/utils, src/core/models, app.ts, and server.ts. Use when creating or changing backend modules, repository/service/routes layers, Fastify route plugins, Mongoose-backed data access, or when tasks mention app.ts, server.ts, backend service, module architecture, repository, service, routes.
metadata:
  tags: backend, fastify, mongoose, repository, service, routes, modules, architecture
---

# Backend Fastify Service Creation

## Когда использовать

Применяй этот skill, когда задача связана с:
- созданием или изменением бэкенд-сервисов;
- созданием нового модуля в `src/modules`;
- реализацией слоев `repository -> service -> routes`;
- Fastify route plugins;
- доступом к данным через Mongoose;
- изменениями в `app.ts` или `server.ts`.

## Базовая структура бека (source of truth)

```text
src/
  modules/
    <module-name>/
      <module files>
  utils/            # общие файлы
  core/models/      # фундаментальные mongoose модели
  app.ts            # инициализация сервера
  server.ts         # запуск сервиса
```

## Правила работы

1. Для новой функциональности сначала определить модуль в `src/modules/<module-name>/`.
2. Общие хелперы и переиспользуемую инфраструктуру класть в `src/utils/`.
3. Базовые модели предметной области на Mongoose хранить в `src/core/models/`.
4. В `src/app.ts` оставлять только инициализацию Fastify-инстанса и регистрацию плагинов.
5. В `src/server.ts` оставлять только старт сервиса (listen/shutdown wiring).

## Дополнительный справочник

Подробные правила по реализации модулей вынесены в отдельный файл:
- `module-implementation.md`

Читай его только при необходимости:
- если создается новый модуль с нуля;
- если нужна детализация по слоям `repository -> service -> routes`;
- если нужно проверить распределение ответственности по слоям.
