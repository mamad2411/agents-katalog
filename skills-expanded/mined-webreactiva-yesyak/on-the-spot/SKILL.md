---
name: on-the-spot
description: Puts the user on the spot with rounds of multiple-choice questions, each with a recommended option, until no implementation doubt is left, before any spec or code is written. Use it whenever the user asks you to grill them, interview them, ask questions until everything is clear, clarify requirements, or when a feature request is vague ("I want an admin panel", "add authentication", "let users export data"). Also use it as the first phase of the feature-delivery-pipeline.
---

# On the spot

Turn a vague request into a set of explicit decisions. Ask; do not implement, and do not start the spec without an answer.

## Before the first question

1. Read the code that the feature touches: entry points, data model, config, tests, docs such as AGENTS.md. Questions grounded in real code are faster to answer.
2. Search whether the feature, or a part of it, already exists. Tell the user what you found before the first question.
3. Note facts the user may not know, and put them in the question text. Example: "the import script deletes every order before it loads the file; should it keep them?"

## How to ask

- Ask in rounds of up to four questions, with the question tool if the environment has one, otherwise in the chat.
- Every question has two to four options, the recommended one first and marked "(Recommended)", each with a one-line trade-off. Allow multiple selection when the options are not exclusive.
- Read free-text answers carefully. They often change the direction, add an option you did not offer, or ask you to stop.

## What to cover

Order the rounds from foundations to details. Skip topics that do not apply.

| Round | Topics |
| --- | --- |
| 1 Foundations | Form of the solution, scope, source of truth for data, users and roles |
| 2 Security and access | Who can do what, authentication, sessions, secrets, abuse limits |
| 3 Interface and structure | Rendering, styling, routes, module layout |
| 4 Behavior details | Ids, deletes, validation rules, lists, filters, messages |
| 5 Operations | CLI, setup scripts, configuration, languages of UI and docs, feedback messages |
| 6 Delivery | Tests, documentation, OpenAPI, branch and commit strategy |

Keep asking until you could write the spec without guessing. Two signals that you are done: your next question would only confirm a default, and every decision in the summary has an owner (the user or an explicit recommended default).

## After the last round

1. Write a summary of every decision, grouped by topic, in the user's language.
2. List the details that you decided by default and still need confirmation.
3. Save the summary to `.scratchpad/<slug>/interview-decisions.md`.
4. Ask whether to see prototypes first (`prototype-options`, when the result has a form a user can look at) or to continue with the spec (`write-acceptance-spec`).
