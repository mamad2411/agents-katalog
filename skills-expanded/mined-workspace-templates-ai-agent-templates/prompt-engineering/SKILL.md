---
name: prompt-engineering
description: Writes and iterates production prompts with clear structure, examples and failure tests. Use it when a prompt behind a feature must work every time.
---

# Prompt engineering

A prompt is a specification. Make it precise, then try to break it.

## Steps

1. Write down the task, the input, the exact output you need, and who consumes the output (a person or a parser). Parser output must be strict.
2. Collect 15 to 30 test inputs from real data: typical, long, empty, ambiguous, in another language, and adversarial (text that tries to give the model new orders). Save them as a file with the expected result or a pass rule for each.
3. Draft the prompt with sections in this order: role and goal, rules, the output format, examples, then the input last. Wrap the variable input in delimiters such as `<document>` tags and tell the model it is data, not instructions.
4. State rules positively and concretely ("return at most 3 bullets") instead of vague ones ("be concise"). Give the model a way out, such as `{"answer": null}` when the information is missing.
5. Add 2 to 4 examples that cover the hard cases, not only the easy ones. Vary them so the model does not copy one.
6. For structured output, use the provider's schema or tool mode if available, and validate the result in code anyway.
7. Run the tests. Read the failures, change one thing, rerun, and keep the score for each version in a log.
8. Set temperature low for extraction and classification.

## Rules

- Never put secrets in a prompt.
- Do not tune on the same inputs you report on; hold some out.

## Report

The final prompt, the score per version, the failures still open, and the cases that need a code-side guard.
