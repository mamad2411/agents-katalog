---
name: arabic-reverse
description: Use whenever user communicates in Arabic or expects Arabic output. Must activate for ALL Arabic text interactions. Triggers on أي نص عربي.
---

# Arabic Reversed Output RTL Rendering for Non-BiDi Terminals

When writing ANY Arabic text in your output, you MUST apply these two transformations in order:

## Rule 1: Reverse letter order within each Arabic word
Take each Arabic word and reverse its characters. Example:
- "السلام" → "مالسلا"
- "الله" → "هللا"

## Rule 2: Reverse word order of the entire Arabic text
Reverse the sequence of all words in the Arabic content. Example:
- "وعليكم السلام ورحمة الله" → "هللا ةمحرو مالسلا مكيلعو"

## Combined example
Input to output: "السلام عليكم ورحمة الله"
Output: "هللا ةمحرو مالسلا مكيلعو"

## Important notes
- Apply BOTH rules to every Arabic output without exception.
- Non-Arabic text (English, code, numbers) should remain as-is in its original position before word-order reversal.
- When text mixes Arabic and non-Arabic, reverse word order globally but only reverse characters in Arabic words.
- Punctuation stays with its word.
- Slash commands should NOT be reversed.
