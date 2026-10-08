---
type: decision
status: approved
iteration: interactive-chat
decision_id: ADR-0003
created: 2026-07-22
updated: 2026-07-22
aliases:
  - ADR-0003
  - TOML-конфигурация и system prompt
tags:
  - sdd/decision
---

# ADR-0003: TOML-конфигурация и внешний system prompt

[Главная](../../README.md) · [Карта документации](../README.md) ·
[Итерация](../iterations/interactive-chat.md)

- Архитектура: [[docs/architecture/interactive-chat-architecture#Конфигурация и filesystem|конфигурация и filesystem]]
- Требования: [[docs/requirements/interactive-chat-requirements#Конфигурация и запуск|конфигурация и запуск]]
- Исследование: [Rust-стек](../research/rust-llm-chat-stack.md)

## Контекст

Локальный запуск требует URL, model и параметры генерации. System prompt является
поведением продукта и должен редактироваться и рецензироваться отдельно от transport
settings. Для первого этапа не нужна сложная иерархия источников конфигурации.

## Решение

- Единственный источник настроек — `config.toml` в текущем каталоге.
- Парсер строгий: неизвестные и некорректные поля завершают запуск до TUI.
- `system_prompt_path` разрешается относительно `config.toml`.
- `prompts/system.md` версионируется, локальный `config.toml` игнорируется.
- Конфигурация и prompt загружаются один раз при запуске.
- Переменные окружения, CLI override и hot reload отсутствуют.

## Последствия

- Запуск воспроизводим и понятен без приоритета нескольких источников.
- Изменение system prompt видно в review как изменение поведения.
- `api_key` может находиться в локальном ignored-файле и должен исключаться из логов.
- Для смены конфигурации требуется перезапуск.
- Системные config directories и secret stores можно рассмотреть отдельно.

## Рассмотренные альтернативы

- JSONC: поддерживает комментарии, но менее идиоматичен для Cargo/Rust-проекта.
- Только environment variables: удобны для deployment, но хуже для локального набора
  связанных параметров.
- Встроенный prompt: упрощает startup, но смешивает поведение модели с Rust-кодом.
