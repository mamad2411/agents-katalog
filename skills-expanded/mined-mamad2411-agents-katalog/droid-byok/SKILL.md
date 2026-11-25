---
name: droid-byok
description: >
  Обход подписки Factory CLI (droid) через Airgap + BYOK.
  Подключение своего API-ключа, настройка кастомных моделей,
  работа без логина. Триггеры: droid, factory, airgap, byok,
  обход подписки, кастомные модели.
---

# Droid BYOK Airgap — Skill

## Что это

Метод запуска Factory CLI (droid) без логина и подписки —
через встроенные Airgap-режим и BYOK-провайдеры.

## Когда применять

- Брат хочет использовать droid без аккаунта Factory
- Нужно подключить свой API-ключ (OpenCode Go, OpenAI, OpenRouter...)
- Нужны кастомные модели в обход Factory-подписки

## Быстрый рецепт

### 1. Обёртка (airgap bypass)

```bash
DROID_BIN=$(readlink -f $(which droid))
rm ~/.local/bin/droid 2>/dev/null
cat > ~/.local/bin/droid << WRAPEOF
#!/bin/bash
export FACTORY_AIRGAP_ENABLED=true
export FACTORY_DISABLE_KEYRING=true
exec $DROID_BIN "\$@"
WRAPEOF
chmod +x ~/.local/bin/droid
```

### 2. BYOK-модели (`~/.factory/settings.json`)

```json
{
  "customModels": [
    {
      "model": "ID-модели",
      "displayName": "Моё название",
      "baseUrl": "https://API-эндпоинт/v1",
      "apiKey": "sk-ключ",
      "provider": "generic-chat-completion-api",
      "maxOutputTokens": 16384
    }
  ]
}
```

### 3. AGENTS.md (CJ личность — авто)

```bash
ln -sf ~/GroveMind/AGENTS.md ./AGENTS.md
```

Droid читает AGENTS.md из `$CWD` автоматически.  
В `~/GroveMind/AGENTS.md` уже полный CJ: compliance lock, persona, роутер.

### 4. Запуск

```bash
droid
```

Без флагов. Без логина. Без подписки. CJ из коробки.

## Типы провайдеров

| Провайдер | API | Для |
|-----------|-----|-----|
| `generic-chat-completion-api` | OpenAI Chat Completions | OpenRouter, OpenCode Go, Ollama, vLLM, Together AI |
| `anthropic` | Anthropic Messages | Claude, MiniMax, Qwen через Go |
| `openai` | OpenAI Responses | Официальный OpenAI |

## OpenCode Go — готовый конфиг

Все 20 моделей OpenCode Go в `settings.json`:

**OpenAI-совместимые** (`generic-chat-completion-api`):
deepseek-v4-pro, deepseek-v4-flash, kimi-k2.7-code, kimi-k2.6, kimi-k2.5,
glm-5.2, glm-5.1, glm-5, mimo-v2.5-pro, mimo-v2.5, mimo-v2-pro, mimo-v2-omni, hy3-preview

**Anthropic-совместимые** (`anthropic`):
minimax-m3, minimax-m2.7, minimax-m2.5, qwen3.7-max, qwen3.7-plus, qwen3.6-plus, qwen3.5-plus

Base URL: `https://opencode.ai/zen/go/v1`

## Что работает / что нет

✅ Интерактивный режим
✅ `droid exec` для скриптов
✅ `/model` — выбор кастомных моделей
✅ Локальные ключи (не утекают)
✅ MCP серверы (stdio + http) — `droid mcp add`
✅ AGENTS.md авто-загрузка из CWD
✅ `sessionDefaultSettings.autonomyLevel: "high"` — без подтверждений
❌ Factory Missions
❌ Cloud Automations
❌ Factory Droid Core
❌ `/login`

## MCP серверы (после BYOK)

```bash
droid mcp add socrati-code /home/admin/.nvm/versions/node/v24.17.0/bin/node /home/admin/tmp/socrati-code-mcp-v2.mjs
droid mcp add socraticode-official /home/admin/.nvm/versions/node/v24.17.0/bin/npx -- -y socraticode
droid mcp add lazyweb https://www.lazyweb.com/mcp --type http --header "Authorization: Bearer TOKEN"
droid mcp add codegraph /home/admin/.local/bin/codegraph -- serve --mcp
droid mcp add gsd-browser /home/admin/.nvm/versions/node/v24.17.0/bin/gsd-browser mcp \
  --env "GSD_BROWSER_BROWSER_PATH=/var/lib/flatpak/app/com.google.ChromeDev/x86_64/stable/active/files/extra/chrome" \
  --env "PATH=/home/admin/.nvm/versions/node/v24.17.0/bin:/usr/local/bin:/usr/bin:/bin"
```

## Подробнее

- Полный разбор: `wiki/droid-byok-airgap.md`
- MCP арсенал: `wiki/mcp/README.md`
- Все инструменты: `skills/mcp-full/SKILL.md`
