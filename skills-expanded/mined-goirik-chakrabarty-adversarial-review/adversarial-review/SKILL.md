---
name: adversarial-review
description: Review a research paper, proposal, or technical writeup by spawning five constructive reviewer archetypes — the Steelman-Builder, Assumption Auditor, Mechanism Seeker, Generous Skeptic, and Contextualizer — each of whom reads critically and curiously and writes a focused review, then synthesizes them into a meta-review with the crux and a decision. Use whenever the user wants a paper, draft, abstract, experiment plan, or research idea pressure-tested, red-teamed, or "reviewed like ICLR/NeurIPS," asks for "reviews of my paper," wants to know how reviewers will react before submitting, or asks to find the weaknesses in a technical argument. Trigger even when the user just says "review this," "tear this apart," or "what would reviewers say," as long as the artifact is a research or technical document.
---

# Adversarial Review

Spawn five reviewer archetypes against a research artifact. Each is **critical and curious**: they attack the work to find what is true, not to gatekeep. Every review names a **crux** — the one thing that would change its verdict — so the author's response time is usable.

The panel is deliberately diverse: five reviewers reading for five different failure modes catch more than one reviewer reading five times. Run them independently so their concerns don't collapse into a single voice, then synthesize.

## Inputs and setup

The artifact is whatever the user wants reviewed: a paper (PDF, `.tex`, `.md`), an abstract, a proposal, an experiment plan, or a pasted argument. Read it fully before spawning anyone — a reviewer working from a summary reviews the summary.

If the artifact is long or the venue matters (ICLR, NeurIPS, a specific journal, an internal bar), ask the user once for that context, then proceed. Don't interrogate; one round of clarification at most.

## The five archetypes

Each archetype is defined in its own reference file. Spawn all five, one per reviewer, giving each **only its own file plus the artifact** — a reviewer who has read the other archetypes' instructions drifts toward covering their ground instead of its own.

- `references/steelman-builder.md` — reconstructs the argument in its strongest form, then attacks *that*.
- `references/assumption-auditor.md` — surfaces the load-bearing assumptions and probes where the result is robust vs. fragile.
- `references/mechanism-seeker.md` — asks *why* it works; isolates the claimed mechanism from incidental causes.
- `references/generous-skeptic.md` — enthusiastic and doubtful at once; states exactly what evidence would convince it.
- `references/contextualizer.md` — situates the work in its lineage; names precisely what is new and what neighbor it must engage.

Read each file at spawn time. Do not paraphrase them into a single prompt.

## How to run

**With subagents** (Claude Code, Cowork): dispatch five subagents in one turn, each with its archetype file and the artifact, each writing to `reviews/<archetype>.md`. Independent context is the point — it keeps the reviews genuinely distinct.

**Without subagents** (Claude.ai): adopt each archetype in turn, in sequence. Before writing each review, re-read that archetype's file and hold *only* that lens. Finish one fully before starting the next. Between reviews, drop the previous reviewer's framing.

## Review format

Every reviewer, regardless of archetype, produces:

```
## Review — <Archetype Name>

**Summary of the work (in my words):** <2-4 sentences proving the reviewer understood it>

**Strengths:** <what genuinely holds; specific, not courtesy>

**Concerns:** <ordered by severity; each concrete and tied to a location in the artifact>

**The crux:** <the single result, argument, or change that would move my verdict — one sentence>

**What would convince me:** <the concrete evidence or revision that resolves the crux>

**Rating:** <weak reject / borderline / weak accept / accept> — **Confidence:** <low / medium / high>
```

The crux is mandatory and non-negotiable. A review without a crux is a Ghost review; the whole point of this panel is to avoid that. If a reviewer cannot name what would change its mind, it has not finished reviewing.

## Synthesis (the meta-review)

After all five reviews exist, write a meta-review as the Area Chair. This is the deliverable the user reads first.

```
# Meta-Review

**Decision:** <accept / borderline / reject> with reasoning that weighs the reviews, not just averages them.

**Consensus:** concerns raised by more than one reviewer — these are the real problems.

**The load-bearing crux:** across all five, the single thing most likely to decide the outcome. If the author fixes one thing, this is it.

**Split verdicts:** where reviewers genuinely disagree, and which side the evidence favors.

**Priority actions:** an ordered list the author can act on, hardest-hitting first.
```

Weigh, don't average. A high-confidence Mechanism Seeker concern that the effect comes from parameter count, not the proposed method, outweighs three reviewers who liked the writing. Name the crux that decides the paper and say what resolving it takes.

## What makes this useful, not theater

- **Every concern points to a location** in the artifact and to a fix. "Weak novelty" is useless; "the contribution overlaps [X]; here is precisely what remains new" is a review.
- **Reviewers update.** If the artifact already answers a concern, the reviewer says so and drops it rather than reciting it for completeness.
- **Positive where warranted.** A constructive reviewer states what genuinely holds; false balance and reflexive harshness are both noise. The goal is a collaborative search for what is true.
