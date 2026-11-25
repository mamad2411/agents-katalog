---
name: craft-survey
description: One-shot prior-art survey — study comparable prompts, skills, or repo assets, extract recurring patterns worth adopting, flag patterns to avoid, and synthesize actionable improvements for the current artifact. Use this whenever the user wants to ground a prompt or skill in proven patterns, references older assets to learn from, asks "how do others do this," mentions "survey," "prior art," or "research," or is designing something new and wants a literature-review pass before committing — even if they don't say "survey." Distinct from craft-autoresearch (which runs an eval-driven optimization loop, not a prior-art survey).
---

# craft-survey

## Purpose

Study comparable prompts, skills, or repo assets, extract the best patterns, and turn them into actionable improvements.

A grounded survey matters because agents that invent from scratch often rediscover bad shapes the community has already outgrown. A focused pass through prior art surfaces the handful of patterns that genuinely carry their weight — and, just as importantly, identifies the ones that shouldn't be copied.

## Use this when

- there are older assets worth learning from
- a new skill should be grounded in proven patterns
- the current artifact feels under-informed
- best practices should be incorporated without cargo-culting them

## Inputs

- target artifact or problem
- local references if available
- optional public references if allowed
- constraints and intended audience

## Steps

1. Start with local or in-repo references first. They're closest to the current context and cheapest to verify.
2. Identify comparable assets and group them by purpose. Grouping makes recurring shapes visible.
3. Extract repeated patterns that seem genuinely useful. Prefer patterns that show up across multiple sources.
4. Separate core patterns from optional stylistic choices. Confusing the two is how cargo-culting starts.
5. Synthesize a small set of recommended changes. Synthesis beats quotation — don't just paste from sources.
6. Apply only the changes that improve clarity, reuse, or quality. Novelty alone isn't a reason to adopt a pattern.

## Output format

### Survey target
One or two sentences naming the specific artifact being improved and the concrete survey question driving this pass. A reader seeing only this section should know what would count as a useful answer — not a generic "strengthen the artifact."

### Reference patterns
Short list of patterns found in comparable assets. Every pattern must cite its provenance — either inline per item, or via a section-opening source map that binds each pattern to its source file + section. A pattern with no traceable source doesn't belong on the list.

### Adopt
Patterns worth bringing into CraftKit. Each item is two parts: the pattern (short handle) AND a rationale clause naming a concrete benefit — what failure it prevents, what friction it removes, what quality it raises. Bare phrases don't satisfy the section; they model without grounding.

### Avoid
Patterns that should not be copied. Each item is two parts: the pattern AND a rationale clause naming the specific harm — what it breaks, what coupling it introduces, what portability it costs. Bare phrases don't satisfy the section.

### Recommended edits
Concrete file or section changes. Each item must name three things: (a) the target file (path or skill name), (b) the specific section/heading/location within that file, and (c) the edit verb (add / tighten / remove / replace / refactor). Scale the number of edits to the scope of the research ask — a narrow question deserves 1–3 edits, not a full rewrite list.

### Risks
Survey-specific risks only. At least one risk must reference either the actual source set surveyed or a named constraint of the target artifact. Generic risks that could appear verbatim in any prior-art survey don't count — if the risk is portable across unrelated survey passes, it hasn't engaged this survey.

## Guardrails

- prefer first-principles synthesis over copy-paste
- do not import provider-specific quirks into core assets
- cite provenance in docs when relevant
- use a few strong patterns, not a giant laundry list

## Failure modes

- treating one strong reference as a template and overfitting to its quirks
- turning the output into a literature review instead of actionable edits
- importing provider-specific phrasing that breaks portability
- skipping the "avoid" list and copying every pattern uncritically

## Example

### Input
Improve a tuning skill using older prompt-builder assets and meta-skills as references.

### Output

**Survey target**
Strengthen the tuning skill so it produces more consistent and portable edits.

**Reference patterns**
- explicit inputs and outputs
- minimal-diff editing
- critique before revision
- examples embedded in docs

**Adopt**
- revised artifact plus changelog structure
- failure-mode note
- preservation of original intent

**Avoid**
- overly vendor-specific phrases
- giant all-in-one instructions

**Recommended edits**
- tighten the output template in `craft-tune`
- add a short failure-mode section
- add one compact example

**Risks**
- overfitting to one repo's naming conventions
