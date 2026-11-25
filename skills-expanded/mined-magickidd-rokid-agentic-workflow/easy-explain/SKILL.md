---
name: easy-explain
description: Explain technical terms in plain, non-engineering language. This skill should be used when users ask "用容易理解的方式解释一下", "说人话", "通俗解释", or similar requests.
license: Complete terms in LICENSE.txt
---

# Easy Explain

Use this skill to translate technical names, function names, and architecture terms into business-friendly explanations.

Target audience:
- Non-engineers
- Product/operations stakeholders
- Any user asking for plain language

## Output Style

Always explain each term with this 5-part template:

1. `它是什么`:
   - One short sentence in plain language

2. `它在流程里的作用`:
   - Why this exists in the system

3. `它接收什么`:
   - Input in everyday words

4. `它产出什么`:
   - Output in everyday words

5. `如果没有它会怎样`:
   - Practical impact or risk

Then add:
- `一句话总结`: 1 sentence
- Optional `生活类比`: only when it makes understanding easier

## Hard Rules

- Do NOT assume coding knowledge
- Do NOT use unexplained jargon
- Prefer Chinese
- Keep each term concise (5-8 lines)
- If name is ambiguous, state assumptions explicitly

## Examples of Trigger Phrases

- "用容易理解的方式解释一下"
- "说人话解释"
- "我不是研发，听不懂"
- "把这个技术词翻译成业务语言"

## Good Explanation Example

Term: `intent_summary`

- 它是什么：把用户意图的处理结果整理成一页简明结论。
- 它在流程里的作用：给后续模块或前端一个“可直接展示”的统一摘要，而不是零散字段。
- 它接收什么：识别出的意图、置信度、相关证据等中间结果。
- 它产出什么：一段结构化摘要（例如“用户想做什么、系统判断是否通过、下一步建议”）。
- 如果没有它会怎样：下游需要自己拼装结果，容易出现口径不一致。
- 一句话总结：它是“把分析结果翻译成统一报告”的步骤。
