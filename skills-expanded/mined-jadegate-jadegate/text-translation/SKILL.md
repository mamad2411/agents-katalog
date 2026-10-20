---
name: text-translation
description: Translate text between languages using free translation APIs with fallback
---

# Multi-Language Translation

Translate text between languages using free translation APIs with fallback

## When to Use

- User wants to translate text
- User wants to translation
- Keywords: translate, language, i18n, multilingual

## Required Parameters

- **text** (string): Text to translate
- **target_lang** (string): Target language code (en, zh, ja, etc)

## Output

- **translated** (string): Translated text
- **source_lang** (string): Detected source language
- **provider** (string): Translation provider

## Security

- Sandbox level: strict
- Max execution time: 30000ms
- Network whitelist: libretranslate.com, api.mymemory.translated.net
- JadeGate verified: Yes (5-layer security check passed)

## Execution Flow

Entry: `encode` -> 10 steps -> Exit: `ret_libre`, `ret_mm`, `ret_fail`
