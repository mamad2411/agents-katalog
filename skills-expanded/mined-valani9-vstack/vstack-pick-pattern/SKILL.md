---
name: vstack-pick-pattern
description: Interview the user about the situation they want to diagnose and recommend 1-3 of the 34 vstack patterns to run. Reads the live pattern catalogue from vstack://patterns/index and tailors the recommendation to what artifacts the user can actually produce.
---

# /vstack-pick-pattern

A conversation-driven router from "we have a problem with our agents" to "here is the precise vstack tool to call." Use when the user doesn't know which pattern fits.

## When to invoke

- The user asks "which pattern should I use?"
- The user describes a situation but hasn't named a pattern.
- `/vstack` defaulted here because no other route matched.
- The user names a vague concept ("they don't collaborate well") that maps to several patterns.

## Preflight

Fetch the live catalogue and ground your recommendations against the real registry — patterns may have been added since this skill was written.

```
read vstack://patterns/index
```

The response is a JSON document with one entry per pattern: `name`, `friendly`, `group`, `tool`, `summary`, `input_class`, `output_class`, `modes`, and the resource URIs for citations / playbooks / composition. Use the `summary` field when explaining a recommendation to the user.

## Workflow

### Step 1 — Two-question interview

Ask exactly TWO questions, one per turn:

**Q1 — Scale.** "Is this a single agent's behavior, a multi-agent crew's coordination, or an organizational/structural design question? (rough is fine)"

**Q2 — Artifact.** "What do you have on hand: an execution trace, a chat transcript, a team config, a written postmortem, or just a verbal report? (multiple is fine)"

Don't ask a third. If you don't have enough after two, recommend the broadest applicable pattern with a caveat about the data gap.

### Step 2 — Filter the catalogue

Based on Q1 and Q2:

| Scale | Likely patterns |
|---|---|
| Single agent | Module 1 (12 patterns): Lewin, Goleman EI, Johari, DANVA, Reappraisal, Yerkes-Dodson, HEXACO, Grant strengths, Motivation traps, SDT, McGregor, Vroom |
| Multi-agent crew | Module 2 (18 patterns): GRPI, process gain/loss, social loafing, superflocks, Lencioni, Trust Triangle, McAllister, Edmondson, Glaser, Stone-Heen, Plus/Delta, SMART, Group decision, Debate pathology, Bias stack, Devil's advocate, Thomas-Kilmann, AAR |
| Organization / structure | Module 3 (4 patterns): Schein, Robbins-Judge, Org-Structure Matrix, Span-of-Control |

| Artifact | Patterns whose input it covers |
|---|---|
| Execution trace (steps + outcome) | Lewin, AAR, Yerkes-Dodson, most Module 1 |
| Chat / debate transcript | Lencioni, debate pathology, Trust Triangle, Edmondson, Glaser |
| Team config (roles + responsibilities) | GRPI, Org-Structure, Span-of-Control |
| Postmortem narrative | AAR, Lewin (with extraction help) |
| Verbal report only | Schein (culture inference), pick-pattern can still suggest a target shape |

### Step 3 — Recommend 1-3 patterns

Output in this format:

```
Recommended (in order):

1. **<friendly>** — <summary from catalogue, 1 sentence>
   Tool: vstack_<name>
   Mode: <quick | standard | forensic>
   Why this one: <one sentence connecting to the user's situation>

2. <if a clear secondary diagnostic helps>

3. <if a clear tertiary diagnostic helps; otherwise skip>

If you want to run them: invoke vstack_<top_pick> now.
```

When two patterns are equally good (e.g. Lencioni vs Edmondson for a "team isn't speaking up" situation), recommend the more **diagnostic** one first (Lencioni's pyramid surfaces the layer; Edmondson scores the symptom).

### Step 4 — If the user agrees, hand off

If the user says "yes" or "do it" or anything affirmative, invoke the top-ranked tool directly. Provide a minimal trace shape from the user's earlier answers; ask only for the fields you cannot infer.

If the user wants the full chain, hand off to `/vstack-audit-crew` (for Module 2 bundles) or `/vstack-post-incident` (for AAR + Lewin chains) instead of calling tools one by one.

## Failure modes

- **Catalogue resource not available.** Fall back to this list of canonical entry points and tell the user the registry couldn't be read: Lewin (single-agent attribution), AAR (postmortem), Lencioni (multi-agent dysfunctions), Schein (culture), Span-of-Control (load/structure).
- **The user gives one-word answers.** Recommend AAR. It's the universal foundational diagnostic; every other pattern composes off it.
- **The user names a pattern that isn't in the catalogue.** Either it's been renamed (search the catalogue for similar `friendly` labels) or it never existed (suggest the closest documented pattern).

## Composition

Downstream skills don't call this one back. This is itself a routing skill, like `/vstack`, but specialized for catalogue-aware pattern picking instead of skill picking.

## What you don't do here

- Don't run the analyzer. The user explicitly came here to *pick*, not to *run*. Wait for confirmation.
- Don't list all 34 patterns. The catalogue is too long; filter first.
- Don't ask more than two questions before recommending. People bounce off interview skills that drag.
