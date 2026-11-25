---
name: tune-skills-and-agents
description: Analyze, test, and improve skills, subagents, and their context layout — what lives HOT vs COLD, whether a grep/file index earns its cost, why a subagent won't read its references, cutting per-turn token bloat, and A/B testing a prompt or rule change.
---

# Tuning skills, subagents, and their context layout

This skill is about making skills and subagents **cheaper per use** and **more correct**, and
about not getting fooled by plausible-but-wrong intuitions while doing it. The guidance here is
**empirically grounded** — the headline verdicts below came from A/B tests, and a few of them
overturned the "obvious" design. When you apply this skill, you measure before you presume.

## The one mental model: hot vs cold

Every piece of context lives in one of two states. Internalize this — every decision flows from it.

| state | where it lives | cost |
| --- | --- | --- |
| **HOT** | CLAUDE.md, an agent's `.md` body, a `skills:`-preloaded SKILL.md, the system prompt | in context **every turn / every invocation** — paid N times |
| **COLD** | `references/*`, a blueprint doc, any file reached by Read/Grep | paid **only when read** — a tool call away |

The whole game is putting the right things in the right state. Hot is a standing tax; cold is
pay-per-use. Optimizing is mostly **moving rarely-needed detail from hot to cold**, and keeping
hot to {what's needed almost every time + what must never be skipped}.

## Hard-won verdicts (measured, often counter-intuitive)

Lead with these. Several contradict the natural guess — that's exactly why they're worth stating.

1. **A grep/anchor index over a *small, well-structured* doc gives ~no retrieval benefit.**
   Markdown headers are *already* grep targets; an agent greps `## 7.` or a keyword on its own.
   Adding `<!-- tag -->` anchors + a token index measured *worse* (more lines read, same tool
   calls) on docs in the hundreds of lines. Don't add index machinery by reflex. → `references/file-indexes.md`

2. **An index inside HOT content is pointless.** If the whole file is already in context, there
   is nothing to "grep to" — the agent has every line. Anchors in a hot file are dead weight.

3. **The real token win is the TRIM, not the index.** Moving mid-depth prose out of an
   always-loaded file (CLAUDE.md / agent body) into a cold reference is what actually saves
   tokens. The index that often accompanies it is usually ceremony. → `references/hot-vs-cold.md`

4. **Cold references are read *reluctantly*.** On a neutral prompt, a subagent will answer from
   its hot context + training and *not* open a relevant cold reference — even one engineered to
   be needed. It reads when: the fact is clearly **project-specific or version-sensitive** (a
   ground truth it knows it lacks), when it **senses it can't recall a precise value**, or when
   the prompt induces it. → `references/ab-test-harness.md`

5. **The silent-skip failure is the dangerous one.** If a critical fact lives *only* in a cold
   reference and the model's training is stale/wrong, the agent never looks and answers
   confidently wrong — silently. Fixing this is a rules problem, and the fix is layered and
   measurable. → `references/subagent-verification-rules.md`

6. **Provenance forcing is the cheapest robust fix.** Requiring an agent to state *where* a
   specific claim came from converts a silent confident-wrong answer into a visibly-flagged
   estimate, even when it still doesn't read the reference. It fired reliably across tests where
   the read-trigger only fired sometimes. → `references/subagent-verification-rules.md`

7. **Measure, don't presume — and clean up after yourself.** The A/B harness below is how every
   verdict above was earned. Agent memory contaminates repeat tests; clean it between runs. →
   `references/ab-test-harness.md`, `references/memory-hygiene.md`

## When to reach for what

| The user wants to… | Do this | Reference |
| --- | --- | --- |
| Decide CLAUDE.md vs reference; cut a long hot file | Hot/cold triage + trim | `references/hot-vs-cold.md` |
| Add/judge a grep index, anchors, table-of-contents | Apply the index cost test (usually: don't) | `references/file-indexes.md` |
| Know if a prompt/rule/skill change actually helped | Run the A/B harness with transcript instrumentation | `references/ab-test-harness.md` |
| Fix a subagent that won't read its docs / answers stale | Add the verification + provenance rules | `references/subagent-verification-rules.md` |
| Run tests on subagents without poisoning future runs | Clean agent-memory / reflection_store / index | `references/memory-hygiene.md` |

## Core workflow

Whatever the specific ask, the shape is the same: **characterize → hypothesize → A/B → keep what wins.**

1. **Characterize.** Read the target (skill, agent `.md`, CLAUDE.md, the doc). For every chunk,
   ask: hot or cold? Used almost-every-time or occasionally? Load-bearing (must-never-skip) or
   optional depth? This classification *is* most of the analysis.

2. **Hypothesize a change**, and predict its effect in hot/cold terms. "Move §X to a reference"
   → saves hot tokens. "Add an anchor index" → predict ~no retrieval gain on a small doc (verdict
   1); say so. "Add a verify rule" → predict it fires for project/version-specific facts.

3. **A/B test it** when the effect is non-obvious or the user wants proof. Same prompt, change
   only the one variable (the rule, the skill, the doc layout) → clean causal attribution.
   Instrument via the **transcript**, not self-report: count tool calls, lines read (input
   proxy), correctness, and provenance honesty (claimed source vs actual tool call). Full
   protocol in `references/ab-test-harness.md`.

4. **Keep what wins, revert what doesn't, and say what you measured.** Don't ship ceremony. If
   the index didn't help, drop it; if the trim saved tokens, keep it; if a rule fired only
   partially, report the limit honestly rather than overclaiming.

5. **Clean up.** If you ran subagent tests, scrub the memory they generated
   (`references/memory-hygiene.md`) so it can't contaminate later work.

## Anti-patterns this skill exists to stop

- **Index-by-reflex.** Adding anchors/TOC/grep-tokens to every doc "for navigability." Measure
  first; on small docs it's cost without benefit (verdict 1).
- **Hoarding hot.** Letting CLAUDE.md / an agent body accrete mid-depth prose that's needed 5% of
  the time. That prose is a per-turn tax. Push it cold.
- **Burying must-apply rules cold.** A non-negotiable, divergent-from-default, or version-pinned
  fact placed only in a reference will be silently skipped (verdict 5). Critical → hot, or guard
  it with a verify/provenance rule.
- **Presuming instead of measuring.** "This is obviously better" is how the grep-index almost
  shipped as dogma. Run the A/B; let the transcript decide.
- **Leaving test memory behind.** Subagent runs write `agent-memory` + `reflection_store` +
  index entries that re-inject into later runs. Always clean.
