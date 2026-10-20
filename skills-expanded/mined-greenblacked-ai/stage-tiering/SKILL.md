---
name: stage-tiering
description: "Set a model tier and effort level per FAMILY stage by the cost of being wrong there: framer, maker, launcher and yielder survey and plan, so run them on a mid tier at medium effort; architect and inspector decide and judge, so run them on the top tier. Fan out at most two agents in parallel on disjoint questions, then synthesise in the main conversation as a named step. Covers where each is set, which setting beats an environment override, and how to opt out. Written in tiers, not product models. Use when choosing which model runs which agent, when survey agents are burning cost, or when a cheap model made the decision. Not for estimating API spend or prompt caching (llm-cost), coordinating live coding agents (agent-orchestration) or briefing one agent (agent-delegation)."
allowed-tools: Read, Grep, Glob
---

# Stage tiering

The stages are tiered when each FAMILY agent runs on the model and effort its stage's cost of error calls for, the choice is written in the agent's own file rather than remembered, parallel fan-out is capped at two agents on disjoint questions, and the main conversation has a named step where their returns become one decision.

The failure runs in both directions. Every stage on the top tier spends the expensive model on throwaway reading: the survey of a codebase costs fifty files to produce two sentences. Every stage on a cheap tier puts the weak model where being wrong costs most, at the architecture whose key decision is hard to reverse, and at the inspection that is the one independent check. Tiering by what an error costs at that stage, rather than by habit, fixes both.

## Scope

Use for: choosing the model and effort for each FAMILY agent; deciding how many agents to run at once; deciding what the main conversation does with their returns; explaining why a setting did or did not take effect.

Do not use for: estimating or reducing API spend, prompt caching or model routing inside a product, which is `llm-cost`; coordinating several live coding agents on one repository task, which is `agent-orchestration`; briefing one agent, which is `agent-delegation`; or the stage definitions, which are `family-workflow`.

## The rule

| Stage | Agent | Tier | Effort | Why an error here is bounded or not |
| --- | --- | --- | --- | --- |
| Frame | `framer` | mid | medium | Reads and organises; Architect returns `NEEDS FRAME` if it is wrong |
| Architect | `architect` | top | tool default | Names the hard-to-reverse decision; nothing downstream re-derives it |
| Make | `maker` | mid | medium | A plan; Inspect and the plan check catch a bad one |
| Inspect | `inspector` | top | tool default | The independent check; a weak one passes defects through |
| Launch | `launcher` | mid | medium | A checklist read; its gate is written and owned |
| Yield | `yielder` | mid | medium | A retro; a poor one is corrected by the next |

The tiers are relative: mid is the capable, economical model your tool offers, and top is its most capable one. You map them; this skill names no product. Raise a mid stage one tier when nothing downstream re-reads its output, for example Launch on a migration that cannot be rolled back. Never lower architect or inspector. Read `references/tier-table.md` for the reasoning per stage and for where each setting lives.

## Workflow

### 1. Read the shipped defaults

Each agent ships with the table above in its own frontmatter, mapped to Claude Code's aliases: `framer`, `maker`, `launcher` and `yielder` carry `model: sonnet` and `effort: medium`, and `architect` and `inspector` carry `model: opus` and leave effort at the tool's default. Read the agent file to confirm what is in force before changing anything. A `model` there wins over the `CLAUDE_CODE_SUBAGENT_MODEL` variable, but `CLAUDE_CODE_EFFORT_LEVEL` wins over every agent's `effort`, so unset it when the per-stage effort has to hold.

### 2. Change a tier without editing the installed plugin

The installed plugin is a cached copy, and the next version replaces it, so an edit there is lost on update. Pass a model in the delegation to change one call, or set the environment variables in `references/tier-table.md` to change every agent. Edit the agent file only where you own the plugin's source, such as a `--plugin-dir` checkout. Read `references/tier-table.md` for both orders of precedence and how to opt out.

### 3. Cap the fan-out at two

Run at most two survey agents in parallel, on questions that do not overlap. The stage being served, for example architect drafting beside two claim agents, is not one of the two. Two overlapping returns leave the main conversation to reconcile them, which costs more than the reading saved. Read `references/fan-out.md` for how to split a question and what disjoint means.

### 4. Name the synthesis step

After a fan-out, the main conversation does one named step: read both returns, reconcile them, and state the decision in a paragraph before the next stage starts. The decision stays in the main conversation, because it depends on the session and travels badly through a cold prompt.

### 5. Record the opt-out if you take it

A user who wants one model everywhere may. Say so where the team will see it, because it removes the tiering silently.

## Anti-patterns

**Everything on the top tier.** The survey stages overspend, and nobody notices because the output is the same.

**The cheap architect.** The hard-to-reverse decision made by the model chosen for being cheap.

**Three in parallel.** More returns than anyone reads closely, with overlapping answers.

**Synthesis by omission.** Two returns pasted forward with no step that decides between them.

**Vendor names in the rule.** A table of product models that is wrong by the next release; write tiers and map them.

## References

- `references/tier-table.md`: read at step 2 for the reasoning per stage, where tier and effort are set, the precedence, and how to opt out.
- `references/fan-out.md`: read at step 3 for splitting a question into two disjoint ones and the shape of the synthesis step.
