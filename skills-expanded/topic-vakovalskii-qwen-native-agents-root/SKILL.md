---
name: qwen-native-agents
description: >-
  Build and prompt agents for Qwen3.x-family models the way Alibaba does it —
  aligned with the conventions baked into qwen-code and Qwen-Agent. Use when
  writing a system prompt for a Qwen agent, defining tools, choosing a
  function-calling format, configuring the thinking mode, or debugging why a
  Qwen model ignores your instructions. Qwen "sticks to" its trained-in habits;
  speak its native dialect instead of fighting it.
---

# Qwen Native Agents

Модели Qwen3.x обучались в связке с фреймворками Alibaba. Форматы tool-calling, thinking, структура системного промпта — это конвенции, зашитые в веса. **Не переучивай модель — воспроизводи её родной диалект.** Детали и цитаты из исходников — в [`references/`](./references/).

## Когда применять

Задача касается: написания системного промпта для Qwen-агента · определения инструментов · выбора формата function-calling · настройки thinking-режима · отладки «Qwen игнорирует инструкцию».

## 10 правил родного диалекта

1. **Работаешь через OpenAI-совместимый API — используй нативный `tools` (проще и без потерь).** Бенчмарк (1296 задач): у qwen нативные `tools` дают 99% верных вызовов против 100% у «родного» NOUS — разница маржинальна, сервер сам нормализует диалект. **NOUS нужен на уровне raw-инференса / vLLM-конфига / отладки**, а не в прикладном вызове. Тогда объявляй тулы блоком `# Tools` внутри `<tools>...</tools>`, модель вызывает `<tool_call>{"name":..,"arguments":..}</tool_call>`, а результат возвращаешь в `<tool_response>...</tool_response>` **под ролью `user`**. Нюанс: gpt-oss заметно лучше в coder-XML (+6 п.п.). → [`03-tool-calling.md`](./references/03-tool-calling.md)

2. **Инструменты — строгий OpenAI JSON-schema.** Ровно `{name, description, parameters}`, где `parameters` = `{type:"object", properties, required}`. У каждого параметра своё `description`. → [`02-tools.md`](./references/02-tools.md)

3. **Нейминг тулов — `snake_case`, глагол+существительное:** `read_file`, `write_file`, `run_shell_command`, `list_directory`, `grep_search`, `glob`, `todo_write`. Модель видит именно wire-name. → [`02-tools.md`](./references/02-tools.md)

4. **Chat-обёртка — ChatML:** `<|im_start|>{role}\n{content}<|im_end|>`, стоп `<|endoftext|>`. В проде используй `tokenizer.apply_chat_template(..., add_generation_prompt=True)`, а не ручную склейку. → [`03-tool-calling.md`](./references/03-tool-calling.md)

5. **Thinking: для Qwen-агента держи ON.** Бенчмарк (3 прогона, 1890 задач): у qwen3.6 включённый thinking поднял tool-call 75→100% и следование инструкциям 69→85%. Либо провайдер отдаёт отдельный `reasoning_content`, либо inline `<think>...</think>` в `content`; внутри `<think>` теги `<tool_call>` **не парсятся**. Включение — `enable_thinking`, прокидывается по-разному для native DashScope / OAI-mode / vLLM. → [`04-thinking.md`](./references/04-thinking.md)

6. **Системный промпт: держи конвенции qwen-code, не инвертируй их.** Тон — «concise & direct», < 3 строк текста, no chitchat, GitHub-flavored Markdown. Комментарии в коде — по умолчанию НЕ добавлять. Это то, за что модель «держится» — совпадение снижает шум. → [`01-system-prompt.md`](./references/01-system-prompt.md) · [`06-habits-and-antipatterns.md`](./references/06-habits-and-antipatterns.md)

7. **Структура системного промпта — по секциям qwen-code:** identity → `# Core Mandates` → `# Task Management` → `# Primary Workflows` → `# Operational Guidelines` (Tone / Security / Using Tools) → `# Final Reminder`. → [`01-system-prompt.md`](./references/01-system-prompt.md)

8. **Few-shot и разметка — XML-теги.** Примеры оборачивай в `<example>...</example>` (диалоги маркируй `user:` / `model:`), хорошо/плохо — `<good-example>` / `<bad-example>`. → [`05-tags-and-markup.md`](./references/05-tags-and-markup.md)

9. **Параллельные tool-calls поощряй явно** («make all independent tool calls in parallel»), но зависимые — последовательно. Это прямая формулировка из системного промпта qwen-code. → [`01-system-prompt.md`](./references/01-system-prompt.md)

10. **Стоп-слова зависят от формата.** NOUS — по закрывающим тегам; legacy `✿`-формат — `✿RESULT✿` / `✿RETURN✿`; ReAct — `Observation:`. Не забудь их выставить, иначе модель не остановится. → [`03-tool-calling.md`](./references/03-tool-calling.md)

## Выбор формата function-calling

- **NOUS (`<tool_call>` + JSON)** — дефолт для Qwen3.x. Начинай отсюда.
- **`✿FUNCTION✿/✿ARGS✿/✿RESULT✿/✿RETURN✿`** — legacy-диалект (Qwen1/2), только если явно нужен.
- **qwen-coder XML (`<function=...><parameter=...>`)** — для coder-моделей (qwen-coder / coder-model).
- **qwen-vl JSON-в-`<tool_call>`** — для vision-моделей (qwen-vl, qwen3-vl-plus).
- **ReAct (Thought/Action/Observation)** — отдельный текстовый режим, не смешивать с выше.

Детали — [`03-tool-calling.md`](./references/03-tool-calling.md).

## Чек-лист перед запуском Qwen-агента

- [ ] Формат tool-calling выбран под семейство модели (coder / vl / general).
- [ ] Инструменты — валидный OpenAI JSON-schema, `snake_case`, у каждого параметра `description`.
- [ ] Результаты тулов оборачиваются правильно (`<tool_response>` под ролью user для NOUS).
- [ ] Стоп-слова выставлены под формат.
- [ ] `enable_thinking` прокинут способом, соответствующим бэкенду (DashScope native / OAI / vLLM).
- [ ] Тул-теги внутри `<think>` не парсятся.
- [ ] Системный промпт не инвертирует привычки qwen-code (тон, комментарии, markdown).
- [ ] Chat-шаблон — через `apply_chat_template`, не руками.
