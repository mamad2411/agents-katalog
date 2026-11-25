---
name: clarifying-questions
description: Ask one structured implementation decision at a time, with a recommendation and result-focused options. Use when code and documentation cannot resolve a decision that materially changes behavior, risk, cost, or scope.
---

# Clarifying Questions

Use this skill only when implementation needs a material user decision.

Do not ask if:

- the code or documentation supplies the answer
- an established repository pattern supplies a safe answer
- a safe and reversible default exists
- the ambiguity does not affect behavior, risk, cost, or scope

Inspect the relevant code and documentation before asking.

## Ask one decision

Ask one decision per question. Do not bundle independent decisions.
Make each question understandable without source-code knowledge or earlier chat context. Include all context needed for the decision.

Before the question, explain:

- what the system does now
- what decision is necessary
- why the decision matters
- how each choice changes the result
- which choice you recommend and why

Use two to four short sentences. Use plain language before technical terms.

Use this pattern when it fits:

> Today, [current behavior]. We need to decide [decision] because [reason].
> I recommend [choice] because [reason]. Which result do you want?

## Describe the options

Describe options by their results, not by implementation names.

For each option, state:

- what the user gets
- the main tradeoff or risk
- whether the choice is easy to change later

Put the recommended option first. Add `(Recommended)` to its label.

Provide no more than three authored options. Add `Give additional context` as the last authored option.

Use this description for that option:

`Explain the situation and tradeoffs in plain, simple English. Do not use jargon. If possible, use an example to show the problem. Then ask me again.`

The questionnaire adds `Type something.` automatically. Do not author that reserved option.

If the user selects `Give additional context`, explain the situation and tradeoffs in plain, simple English without jargon. If possible, use a concrete example to show the problem. Then ask the same decision again.

## Use the available interface

Use `ask_user_question` when it is available. Ask in plain text only when the tool is unavailable.

Do not use the questionnaire for casual conversation, direct answers, routine commands, progress updates, or trivial confirmations.

After the user decides, record the decision in the active plan when one exists. Then continue implementation unless another material decision blocks it.
