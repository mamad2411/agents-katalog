---
name: agent-writing
description: >-
  Write instructions that agents actually follow: skills (name, description, trigger phrases, body),
  CLAUDE.md / AGENTS.md rule files, and briefs for subagents or other agents (objective, DONE criteria,
  verification, report shape). Covers what to cut, length budgets, examples over adjectives, and a
  pre-ship checklist. Use for a subagent or agent brief, a system prompt, trimming a rules file that
  has grown too long, or when an agent keeps ignoring an instruction. For the full style reference on
  writing skill and doc files, use `writing-for-agents`.
---

# Agent writing

An agent reads every word, every time, and acts on what is concrete. Vague text costs tokens on every
run and still gets ignored. Write less, and make each line something the agent can do or check.

## When it applies

- Writing or editing a skill, a CLAUDE.md / AGENTS.md, a system prompt, or a brief for another agent.
- An agent keeps skipping a rule: the wording is usually the bug.

## Skills

- **Name:** short, lowercase, hyphenated, a verb or a noun the user would say.
- **Description is the trigger.** It is always loaded; the body loads only when it fires. Write what
  the skill does in one sentence, then "Use for/when" with the phrases a user really types and the
  situations that should fire it. One phrase per distinct case; drop synonyms.
- **Body:** when it applies (and when to skip), the procedure as numbered steps, rules, output format.
  Each step ends on something checkable.
- **Budget:** 40-150 lines. Push rare branches and long reference into a sibling file, named from the
  step that needs it ("for X, read `ref/x.md`").

## Rule files (CLAUDE.md, AGENTS.md)

- Every line costs on every turn. Keep only rules the agent would get wrong without them.
- Each rule: the instruction, then a short why. The why lets the agent handle cases you didn't list.
- Put the exact command, path or pattern in the rule. "Use bun" beats "prefer our package manager".
- Move anything used rarely into a referenced file with a trigger line.

## Briefs to another agent

The brief is all the agent knows. Include:

1. **Objective:** one or two sentences, including why.
2. **Context:** paths to read, what is already ruled out, constraints.
3. **DONE means:** checkable criteria, e.g. "`bun test` passes and `GET /x` returns 200".
4. **Verification:** the exact command to run and what to report from it.
5. **Limits:** scope, files not to touch, iteration caps ("stop after 2 fix cycles and report").
6. **Report shape:** outcome first, files changed, evidence, open items, assumptions made. Long output
   goes to a file; return the path.

Give the brief the facts, not your conclusion, when you want an independent view.

## What to cut

- Adjectives that ask for quality ("be thorough", "carefully", "high-quality"). Replace each with the
  check that would prove it.
- Shouting (CAPS, "CRITICAL", "MUST") except for the one or two rules that really are hard limits.
- Restating what the model already does by default.
- Background and history the agent can't act on.
- Duplicates: the same rule in two places drifts apart.

## Examples over adjectives

One concrete example (a command, a filled-in template, a before/after) fixes behaviour better than a
paragraph of description. Use a placeholder format like `<path>` so it isn't copied literally. Show a
bad example only next to the good one.

## Pre-ship checklist

- [ ] Description says what it does and lists real trigger phrases.
- [ ] Every step ends on something the agent can check.
- [ ] Every "be X" adjective replaced by a check or an example.
- [ ] No rule that the model would follow anyway.
- [ ] Within the length budget; rare branches moved out.
- [ ] Host-neutral if shared: "a subagent, if your host has them", no tool names from one product.
- [ ] Tried once: give it to a fresh agent on a small real task, watch where it goes wrong, fix
      that line.
