---
name: scoped-grill-with-docs
description: Runs a relentless, documentation-aware grilling session with numbered questions and a strict temporary scope ledger. Use when the user wants a plan or design grilled against domain documentation without losing question count or drifting outside the agreed scope.
disable-model-invocation: true
---

# Scoped Grill With Docs

Run a `/grilling` session, using the `/domain-modeling` skill. Those skills own the interview workflow, question content, and domain documentation. Apply only the scope, persistence, numbering, and output rules below.

## Initialize the scope ledger

Before asking Question 1:

1. Resolve the operating system's temporary directory with a platform-native facility. Do not hardcode a platform-specific path or write the ledger into the repository.
2. Create a uniquely named Markdown file for this session.
3. Write exactly these two semantic blocks:

```markdown
## TL;DR

<Concise description of what is being grilled.>

## IN SCOPE

- <Current scope item>
```

Update the ledger when the user's answers explicitly refine or change the goal or scope. Do not broaden `IN SCOPE` merely to permit a proposed question.

If the ledger cannot be created, read, or updated, stop before asking another question and report the failure.

## Control conversational state

Begin the session in **GRILLING**.

Enter **DISCUSSION** when the user does not directly answer the pending question and instead asks for context, asks a follow-up, challenges a premise, expresses uncertainty, wants to reason through the decision, or otherwise starts a conversational detour. When uncertain whether the user answered, prefer DISCUSSION.

While in DISCUSSION:

- Respond normally without displaying `TL;DR`, `IN SCOPE`, `SCOPE EXCEPTION`, or `Question N`.
- While the discussion remains unresolved, do not generate, restate, or rephrase the pending question.
- While the discussion remains unresolved, do not generate a new grilling question or increment the question number.
- Silently update the ledger only when the user explicitly changes or refines the goal or scope.
- Remain in DISCUSSION across any number of turns when the user is still exploring, challenging, asking follow-ups, or expressing uncertainty.
- Infer that DISCUSSION has ended when the user clearly and definitively resolves the pending question or clearly signals readiness to continue. Examples include agreement such as "yes, agreed," confirmation that the explanation answered the concern, or a request for the next question.
- When inferring that DISCUSSION has ended, record the resolution, reread the ledger, return to GRILLING, and ask the next appropriate question with the next number in the same response. Do not require or suggest the phrase `resume grilling`.
- When the user's intent is ambiguous, remain in DISCUSSION and do not advance.

The user may always return to GRILLING explicitly by saying `resume grilling`, ignoring capitalization. Reread the ledger before continuing. If the discussion resolved the pending question, ask the next appropriate question using the next number. Otherwise, show the pending question again using its original number.

## Gate every question

Only while in GRILLING, immediately before asking each question:

1. Reread the ledger.
2. Let `/grilling` and `/domain-modeling` determine the proposed question.
3. Compare the complete proposed question with `IN SCOPE`.
4. Reject it if it is outside scope and let the underlying skills choose an in-scope question instead.

Ask an out-of-scope question only when it is necessary to advance the stated `TL;DR` and no in-scope question can resolve the need. Explain that exceptional reason in a `SCOPE EXCEPTION` block before the question.

## Number and display every question

Start at Question 1. Determine each next number from the highest `## Question N` already shown in this session, then increment by one. Never replace the number with wording such as "next question."

Every question response must reproduce the current ledger content and use this shape:

```markdown
## TL;DR

<Current TL;DR from the ledger>

## IN SCOPE

<Current IN SCOPE from the ledger>

<Optional SCOPE EXCEPTION block and concrete reason>

## Question N

<Question produced by the underlying skills>
```

Do not prescribe, replace, or rewrite the underlying question content beyond rejecting a proposed out-of-scope question.
