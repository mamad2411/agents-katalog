---
name: typography-critique
description: Use when the question is quality or taste rather than compliance — "is this any good", "does this feel right", "why does this look generic or AI-generated", art-direction review, or judging whether a typographic risk pays off. Use typography-audit instead when checking against defined criteria.
---

# Typography critique

Audit asks "does this meet the criteria." Critique asks "is this any good."
Both are legitimate; conflating them produces vague audits and unaccountable
opinions.

## 1. When to invoke

- "Is this good?" / "Does this feel right?"
- "Why does this look generic / cheap / AI-generated?"
- Art-direction review, or judging an expressive risk.
- Choosing between options that all pass the audit.

**Do not** invoke when criteria exist and the question is compliance
(`typography-audit`).

## 2. Required context

- The **intent** — what should this feel like, to whom? Critique without intent is
  just preference.
- The **constraints** the work operated under.
- Whether it's a **template** or a one-off.
- What the author was **trying** to do. Critique the gap between intent and result.
- Whether the work already passes audit — if it doesn't, fix that first; broken
  accessibility isn't a taste question.

## 3. Invariant principles

- **Critique against stated intent, not personal preference.** "I'd have used a
  serif" is not critique. "The brief says authoritative; geometric construction
  reads technical, which is why it feels colder than intended" is.
- **Name the visible evidence.** Every judgment must trace to something observable —
  a proportion, a spacing relationship, a contrast, a form.
- **Aim at the work, not the author.** Specific, actionable, with a concrete next
  step.
- **Rules can be broken deliberately.** Lupton treats "when breaking a rule is
  appropriate" as part of the discipline. Distinguish a deliberate break (consistent,
  motivated, controlled) from a defect (inconsistent, unmotivated, accidental).
- **Familiarity is not a flaw.** Bias favors familiarity; readers prefer what they
  see most. "Generic" is only a criticism when distinctiveness was the goal.
- **Restraint is a position.** Not every page should be expressive.

## 4. What "generic" and "AI-generated" actually mean

When someone says work looks AI-generated or cheap, the cause is almost never the
typeface. In order of frequency:

1. **Uniform spacing everywhere.** Equal space above and below every element, so
   nothing groups and nothing is emphasised. Real typography has deliberate
   density variation.
2. **No microtypographic care.** Straight quotes, hyphens as dashes, untracked
   caps, orphans. See `microtypography` — this is the single strongest tell.
3. **Default everything.** Untouched line-height, no measure cap, default weights.
4. **Hierarchy by size alone**, in even steps, with no weight or spacing contrast.
5. **No compositional system.** Elements placed without axis, grid, or module — see
   `typography-layout-systems`.
6. **Safe centred symmetry** everywhere, which reads as absence of decision.

The fix is rarely a new font. It's spacing decisions, one deliberate contrast, and
microtypographic finish.

## 5. Context-dependent heuristics

**Nix's hierarchy of typographic needs.** Charles Nix (Monotype) maps Maslow onto
typography, and it's a fast way to locate what a piece of work actually needs before
you critique what it aspires to:

1. **Font functionality** — the typeface doesn't matter yet; there just has to be
   something rendering the message.
2. **Font security** — the licence is clean; no legal or financial exposure.
3. **Typographic love and belonging** — someone actually cares about the type.
4. **Typographic esteem** — the choices generate esteem; the work reads as considered.
5. **Typographic self-actualization** — expressive, distinctive, fully realised.

Critique at the wrong level wastes everyone's time. Telling a team their type lacks
expressive voice when their webfont licence doesn't cover the app, or when the text
fails contrast, is critique aimed three levels above the actual problem. Find the
lowest unmet level and start there.

**Typographic colour is the fastest diagnostic you have.** Squint at a block of text:
its overall grey density should be even. Blotchy or patchy colour means rivers,
uneven word spacing, or a weight mismatch — and it's usually what people are
reacting to when they say a page looks "cheap" without being able to say why. See
`microtypography`.

**Judge at reading distance and at a glance.** Squint first: does structure emerge?
Then read: does the detail hold up? Work that fails the squint test has a hierarchy
problem; work that passes the squint and fails the read has a micro problem.

**Separate three layers when giving feedback:**
- **Structure** — composition, hierarchy, system. Expensive to change.
- **Setting** — size, spacing, measure, scale. Moderate.
- **Finish** — punctuation, tracking, rag, orphans. Cheap, high impact.

Lead with the layer that has the best return. Usually finish, then setting, then
structure.

**Distinguish a break from a defect.** A deliberate break is *consistent* (it
happens every time the condition recurs), *motivated* (it serves the intent), and
*controlled* (its consequences were handled). Fail any of the three and it's a
defect.

**Taste is downstream of constraints.** If a choice was forced by licensing,
performance, or a system, say so rather than critiquing it as a free decision.

## 6. Failure patterns in critique itself

| Pattern | Why it's wrong |
|---|---|
| "I don't like it" | No evidence, no intent, unactionable |
| Critiquing a template from one populated example | Templates fail on edge content |
| Recommending a font swap for a spacing problem | Expensive fix for the wrong cause |
| Treating an accessibility failure as taste | It's a defect; fix before critiquing |
| Ignoring the constraints | Critiques decisions that weren't free |
| Only negatives | Doesn't tell the author what to preserve |
| Vague adjectives ("cleaner", "more modern") | Not actionable |
| Critiquing the author | Unhelpful and untrue |

## 7. Evaluation procedure

1. State the **intent** in one sentence. If you can't, ask — critique without it is
   preference.
2. Confirm it **passes audit**. If not, stop and route to `typography-audit`.
3. **Squint.** Does structure and reading order emerge? Note what you see first.
4. **Read it.** Does the detail hold?
5. Identify the **gap** between intent and result, with visible evidence.
6. Sort observations into structure / setting / finish.
7. For each: what to **keep**, what to **change**, and the concrete next step.
8. Identify deliberate breaks and say whether they earn their place.
9. Lead with highest-return, lowest-cost changes.

## 8. Output format

```
Intent: <one sentence>
Passes audit: <yes | no → route to typography-audit>

Working (keep):
- <observation> — evidence: <what's visible>

Gap (intent vs. result):
- <observation> — evidence: <visible> — layer: <structure|setting|finish>
  → <concrete next step>

Deliberate breaks: <break> — <earns it | reads as defect, because …>
Highest-return change: <one thing>
```

## 9. Examples

**"Our landing page looks AI-generated. Should we change the font?"**

> Intent is a confident, premium product page; it passes audit. The font isn't the
> problem — it's a competent, unobtrusive sans and swapping it would cost a week and
> change nothing.
>
> Working: the scale is sensible and the measure is capped correctly.
>
> The gap is almost entirely *finish* and *setting*. Every section has identical
> vertical space above and below, so nothing groups and the page reads as one
> undifferentiated column — that's the strongest generic signal. Second, the copy
> uses straight quotes and hyphens where en dashes belong, and the all-caps eyebrow
> labels are untracked. Third, hierarchy is carried by size alone in even steps,
> with every heading at the same weight.
>
> Highest-return change: vary the vertical spacing so related elements group
> tightly and sections separate clearly. That one change does more than any font
> swap. Then fix the punctuation and track the caps. Structure can stay.

**Art-directed feature that breaks the grid on one spread.**

> The break is deliberate by all three tests — it recurs consistently at every
> pull-quote spread, it serves the intent (a pause in a long read), and its
> consequences are handled (the measure stays capped, the rag stays clean). It
> earns its place. Keep it.

## 10. Counterexamples

- ❌ "It looks dated, use a modern sans." — No evidence, no intent, and "modern"
  isn't a typographic property.
- ❌ "Change the font, it looks AI-generated." — Misattributes a spacing and finish
  problem to typeface choice.
- ❌ "The contrast is too low for my taste." — That's an audit finding with a
  numeric threshold, not taste.
- ❌ "This breaks the rule about centred text, so it's wrong." — Rules can be broken
  deliberately; test consistency, motivation, and control first.
- ❌ Critique consisting only of problems. — The author needs to know what to keep.
- ❌ "Make it feel more premium." — Name the visible signals that would do that.

## 11. Source citations

- Lupton, *Thinking with Type* 3e — hierarchy and contrast; typographic
  conventions; **when breaking a rule is appropriate**; familiarity bias and reader
  preference.
- Santa Maria, *On Web Typography* — evaluating typefaces; matching type to content
  and tone; balancing aesthetic and technical constraints; art direction.
- Hochuli, *Detail in Typography* — texts where "all the details have been attended
  to — and yet they look so soporifically dull"; correctness is not sufficiency.
- Coles, *The Anatomy of Type* — reasoning from visible evidence rather than "this
  font looks modern."
- Elam, *Typographic Systems of Design* — compositional tension, contrast, and
  visual hierarchy; structure as the basis of judgment.
- Latin, *Better Web Typography* — explaining typography decisions to clients and
  developers.
- Stocks, *Universal Principles of Typography* — §15 "it's okay to just love type for
  no discernible reason," and the limits of that in professional critique; §53
  typographic colour as a squint test for density; §98 **Nix's hierarchy of
  typographic needs** (Charles Nix, Monotype) — font functionality → font security →
  typographic love and belonging → typographic esteem → self-actualization; §99 "it
  depends." Full index in `../type/references/universal-principles-index.md`.
