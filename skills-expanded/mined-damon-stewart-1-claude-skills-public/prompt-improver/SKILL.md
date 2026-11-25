---
name: prompt-improver
description: "Rewrites a natural-language prompt into a structured, high-quality prompt that follows Anthropic's prompting best practices: explicit role, XML-tagged inputs, clear output format, examples, chain-of-thought scaffolding when warranted, and concrete success criteria. Use when the user says 'improve this prompt,' 'make this prompt better,' 'rewrite this prompt,' 'design a better prompt,' 'tune this prompt,' 'output a better prompt,' 'design your own prompt,' 'prompt for me,' or invokes /prompt-improver. Also use when the user pastes a draft prompt and asks for feedback or a stronger version."
user_invocable: true
effort: high
---

# Prompt Improver

Rewrites a natural-language prompt into a structured prompt that follows Anthropic's prompting best practices. The depth of the rewrite scales to the job, set by a 2-question triage gate at the start.

## Step 1: Capture

Take whatever the user provided as the prompt-to-improve. It may be:
- A pasted draft prompt
- A natural-language task description ("write me a prompt that classifies tickets")
- A vague ask ("design your own prompt for X")

Treat all three the same way: they are inputs to the gate.

## Step 2: Triage gate (always)

Ask exactly these two numbered questions, then wait for answers. Do not skip, do not add a third.

```
1. How important is getting this exactly right?  low / medium / high
2. Will this prompt run once, or repeatedly?     once / repeatedly
```

Map the answers to a tier:

| Importance | Reuse | Tier |
|---|---|---|
| low | once | **One-shot** |
| medium | once | **Standard** |
| low | repeatedly | **Standard** |
| medium | repeatedly | **Interview** |
| high | once | **Standard** |
| high | repeatedly | **Interview** |

The user may also override directly with `--light` (one-shot), `--standard`, or `--full` (interview). If an override flag is present, skip the gate.

## Step 3: Mode-specific follow-ups

**One-shot mode:** no follow-ups. Go straight to Step 4.

**Standard mode:** ask these 3 follow-up questions, numbered:

```
1. What inputs will this prompt receive at runtime? (e.g. "a ticket title and body")
2. What output format do you want? (e.g. "one of: bug / feature / question")
3. What does "good enough" look like? (one line)
```

**Interview mode:** ask these 6 follow-up questions in one batch, numbered:

```
1. Who reads or consumes the output?
2. What inputs will this prompt receive at runtime?
3. What output format do you want?
4. What does "good enough" look like?
5. Do you have 1 to 3 example input/output pairs I can draw from?
6. Anything to explicitly avoid (anti-patterns, banned phrases, scope creep)?
```

If the user gave any of this in Step 1, fill it in yourself and ask only the missing items.

## Step 4: Diagnose

Read `references/checklist.md`. Score the original input against the 12 axes. Note the top 3 to 5 weaknesses the rewrite will address. Skip axes the chosen tier does not support.

## Step 5: Rewrite

Read `references/rewrite-template.md`. Use the template that matches the tier.

For shape and tone of the output, read `references/examples.md` and pattern-match to the example closest to the user's task.

Output the rewritten prompt in a fenced code block so the user can copy it directly.

## Step 6: Explain the diff

Below the rewritten prompt, add a short "What changed and why" block. Each change maps to one best-practice axis from the checklist. Two to four bullets max in One-shot, four to seven in Standard, seven plus in Interview.

## Step 7: Offer escalation

End with one line offering the next tier up if the user wants more rigor:

- After One-shot: "If this needs to run repeatedly or accuracy matters more than I assumed, run `/prompt-improver --standard` to add inputs, output format, and success criteria."
- After Standard: "If this is high-stakes or you have examples, run `/prompt-improver --full` for the full interview-style rewrite with chain-of-thought and examples."
- After Interview: no escalation line. Offer to run the rewritten prompt against a test input if the user provided one.

## Constraints

- Numbered questions only. Always.
- No em dashes or double-hyphens as em-dash substitutes in prose. Code blocks exempt.
- Never commit or push files. The user owns when to ship.
- If the user's input is already a strong prompt, say so directly and propose only the changes worth making. Do not rewrite for the sake of rewriting.

## Failure modes

When a rewrite misfires (user pushes back, the prompt does not produce the expected behavior), append a one-line gotcha to `gotchas.md` for next time.
