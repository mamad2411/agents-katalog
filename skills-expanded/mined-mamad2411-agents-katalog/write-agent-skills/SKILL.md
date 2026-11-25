---
name: write-agent-skills
description:
  Use when creating a new Claude Code skill or tightening one that has grown too long. Authors
  skills test-first (baseline the failure without the skill, then write only what closes it) and
  runs a ruthless economy pass — a teammate subagent that cuts filler — to hold skills near the
  budget where they still perform. Triggers include "write a skill", "create a skill", "this skill
  is too long", "tighten/trim this skill", "cut the filler", "the description is too verbose".
---

# Write Agent Skills

A skill's reader is a capable agent with repo access — it derives the obvious. So write only what it
_can't_ derive, and treat every token as cost: `name`+`description` are always in context (every
request, every installed skill); the body loads on invocation; scripts never load unless executed.

The counterpart reviewer is `review-agent-skills` — run it after this.

## Budget

- **Body ≤ ~150 lines / ~1.5–2K tokens.** Past ~150, quality degrades across all rules, not just the
  new ones — bloat weakens the instructions you care about.
- **`description` ≤ 1024 chars, triggers-dense — it alone decides whether the skill fires.**

## Workflow

A skill is a **path** (the steps that work), its **paving** (task-specific context that isn't
derivable), and **signage** (warnings at the pitfalls). Build it test-first so the signage is real,
not imagined — and the eval is what lets you cut hard later, since it catches an overcut.

1. **FORGE** _(RED)_ — run the skill's real job end-to-end **without** the skill, across a few
   _varied_ scenarios (one run overfits to its own errors). If the job is to _do_ something,
   actually do it (stand up the service, run the pipeline), not edit a doc about it; if it's to
   _hold a line_ under pressure, stack the pressures (time + sunk cost). The route that works is the
   path; every stumble or rationalization is a pitfall.
2. **PAVE** _(GREEN)_ — write the minimal skill: the path as tight steps, the non-derivable context
   that smooths it, and signage only at pitfalls you actually hit. Nothing speculative.
3. **CRITIC** — spawn a teammate subagent to cut filler. Hand it the draft, the cut-list below, and
   the line target. It returns a trimmed draft plus a kill-list; anything it's unsure is
   load-bearing it **flags rather than deletes**.
4. **ITERATE** — re-run the scenarios, plus new ones, against the trimmed skill. A regression means
   the critic overcut → restore that line. A fresh stumble means missing signage → add it and re-run
   CRITIC. Loop until varied runs pass clean.
5. **REVIEW** — run `review-agent-skills` over the result to catch what you're too close to see
   (jargon, bloat, routing contention). Keeps you honest.
6. **REFLOW** — `prettier --prose-wrap always --print-width 100 --write SKILL.md` before committing,
   so long lines don't fight inline-review tools.

## Cut these

- Explanations of what the model already knows, or anything a competent agent does anyway.
- Trigger phrases in the _body_ — they belong in `description`; the body doesn't route.
- Duplication: within the file, and between SKILL.md and its references.
- Multiple options — give one default plus one escape hatch, not a menu.
- Hand-written flag lists, directory maps, or time-sensitive notes — reference `--help`, let paths
  live in code, and they can't rot.
- Repeated long literals — a command prefix, path, recurring identifier — left in full. Define a
  shorthand once, reusing a name the material already uses, when it recurs enough to pay for itself
  and stays unambiguous.
- Bare prohibitions — a lone "don't X" makes the model think about X. Pair every "don't" with the
  positive behavior, or state only the positive.

## Keep these

- **Progressive disclosure:** SKILL.md is overview + links; depth goes in references loaded on
  demand; deterministic/fragile steps go in scripts (executed, never loaded).
- **One skill, one job** — split by domain so only relevant context loads.
- **`description` = `<what it does>. Use when <triggers, symptoms, tool names, error strings>`**,
  third person (it is injected into the system prompt).
- **Explain WHY** for any rule that needs compliance — the agent generalizes from motivation better
  than from authority. Reserve imperatives for true boundaries.
- **Markdown tables** for structured references — polyglot-safe across harnesses; avoid XML in
  tool-agnostic skills.

## Anti-patterns

- Session-specific / narrative examples ("in the 2026-07 run we found…") — not reusable.
- Multi-language example dilution (`example-js` + `example-py`) — mediocre and a maintenance tax;
  one excellent example beats three.
- Code inside flowcharts (uncopyable); generic labels (`helper1`, `step3`) that carry no meaning.
- Undefined jargon — a coined term or type-taxonomy used without defining it inline or linking where
  it's defined; the reader can't resolve it from common knowledge or accessible docs/memories.

---

_Distilled from cross-ecosystem research (Anthropic skill/tool guidance, Augment AGENTS.md,
Cursor/Copilot rules, MCP description economy) and from
[@ed3d](https://github.com/ed3dai/ed3d-plugins)'s `writing-claude-directives`, `writing-skills`, and
`testing-skills-with-subagents` — install that plugin for the deeper TDD-and-rationalization
methodology._
