---
name: japanese-to-chinese-translator
description: Translate Japanese text into Chinese with support for tone, context, and output style preferences.
metadata:
  category: plain
  tag:
    - translation
    - japanese
    - chinese
    - language
---

# Japanese to Chinese Translator

## Overview
This skill translates Japanese text into Chinese. It is designed for general-purpose translation, including casual, formal, and business-style content.

Because translation is a native language capability of the AI agent, this is a plain skill and does not require runtime execution.

## Usage
Provide:
- Source Japanese text
- Preferred Chinese variant (Simplified or Traditional)
- Optional tone/style guidance (literal, natural, formal, concise)

## Suggested Prompt Pattern
- "Translate this Japanese to Simplified Chinese in a natural tone: <text>"
- "Translate this Japanese to Traditional Chinese, keep honorific politeness: <text>"

## Output Guidelines
- Preserve meaning and intent
- Keep names and technical terms consistent
- Adapt idioms naturally where appropriate
- Maintain formatting (lists, line breaks, punctuation) unless asked otherwise

## Example
Input (JA):
"お世話になっております。来週の会議は水曜日の午後2時からでお願いします。"

Output (ZH-CN):
"承蒙关照。下周会议请安排在星期三下午2点开始。"

Output (ZH-TW):
"承蒙關照。下週會議請安排在星期三下午2點開始。"