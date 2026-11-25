---
name: superforge-roast
description: >
  Deliver an unsparing, compliment-free critique of a design, PRD, plan,
  architecture, copy, or UI to expose flaws before they ship. Strips AI
  politeness and names the weakest point first. Use when the user says
  "roast", "be brutal", "tear this apart", "what's wrong with", "honest
  feedback", "critique", "poke holes", "don't be nice", "辛口で", "ダメ出し",
  "批評して", "欠点を指摘", "忖度なしで", or runs /superforge-roast.
license: MIT
metadata:
  author: Takao Umehara
  version: "2.2"
compatibility: >
  Standalone.
  Reads any docs/ artifact as the critique target, writes docs/critique.md.
---

# Superforge Roast — Uncompromising Critique Engine

Use this skill to subject designs, code, PRDs, copy, or architecture plans to a ruthless, zero-fluff critique. This engine strips away AI politeness, highlights hidden flaws, and forces radical polish before shipping.

---

## 1. Critique Mindset (Zero AI Compliments)

- **Ban False Praise**: Never open with *"Great start!"*, *"Looks awesome!"*, or polite agreement.
- **Direct & Unsparing**: Point out confusion, bad assumptions, ugly layout math, unnecessary complexity, or weak copy immediately.
- **Constructive Solution**: For every flaw roasted, specify the exact, actionable path to fix it.

---

## 2. Roast Dimensions

Analyze the artifact across 4 ruthless lenses:

1. **UX & Friction Roast**:
   - Where will a user get confused, annoyed, or abandon the flow?
   - Are there hidden edge cases or missing error states?
2. **Design & Aesthetic Roast**:
   - Does it look like generic AI template code?
   - Is the typography scale inconsistent? Are margins arbitrary?
3. **Architecture & Code Roast**:
   - Is there over-engineering or premature abstraction?
   - Where will this break when data scales or network drops?
4. **Copy & Positioning Roast**:
   - Is the copy preachy, jargon-filled, or vague?
   - Does it sound like corporate filler instead of direct human communication?

### Before the lenses: audit the numbers

When the target argues from evidence — 「3日で77%離脱」「短いオンボーディングが
鉄則」「売上2,000%」 — trace every figure to its primary source and tag it
A / B / C / D with year and scope before critiquing anything built on it. A
design critiqued on top of an untraced number has had its decoration roasted and
its foundation accepted → **`references/claim-audit.md`**.

### The lenses have to be independent, and in one context they are not

Running all four in a single pass is the compromised version of this skill. By
the fourth lens the same context has already read the first three and agrees with
them — the later critics inherit the earlier ones' framing, and a flaw that only
shows up when you have *not* been told what to look for never surfaces. Worse,
the pass that generates findings is also the pass that decides which ones are
real, and it has no reason to kill its own.

Where Claude Code is available, run **`workflows/superforge-roast-council.js`**
instead: five critics on separate contexts that never see each other, then an
Opus skeptic per lens whose only job is to kill findings that turn out to be
absent, taste, already handled, or fixed at a cost higher than the defect. Then
one judge writes `docs/critique.md`. Eleven agents; say *"use a workflow"* or run
`/superforge-roast-council`.

Everywhere else, run the four lenses in one pass — but read the target once per
lens before writing anything, and refuse your own findings on those four grounds
before they reach the artifact.

It is the weaker version, and both paths write `docs/critique.md`, so **the first
line of that file states which one ran**: `Mode: single-pass fallback` here,
`Mode: council (5 lenses, 11 agents)` from the workflow. A reader deciding how
much to trust a critique should not have to infer it from tone.

---

## 3. Output Format

```text
🔥 THE ROAST (Unfiltered Flaws)
- [Flaw 1]: <Exact callout of what is weak/broken>
- [Flaw 2]: <Exact callout>

🔨 THE FORGE (Actionable Upgrades)
- [Fix 1]: <Specific code/design/copy change to execute>
- [Fix 2]: <Specific change>
```

---

## Deeper reference

**`references/evaluation-methods.md`** — heuristic evaluation, accessibility
audit, cognitive load analysis, simulated persona testing, strategic fit, and
the synthesis rules that turn thirty findings into a usable verdict.

**`references/claim-audit.md`** — the A/B/C/D evidence tiers applied to design
claims, the five-step trace, the industry folklore already checked (with what
the source really says), and the `## Evidence base` table for the critique.

## Artifact

Write `docs/critique.md`, led by the single worst thing in one sentence.
Group findings by cause, not by screen. Every finding carries a fix.

## Findings must reach someone

`docs/critique.md` is not the end of the job. A critique nobody is assigned to
act on is a document, and documents do not fix products.

When handing back, name the destination for each finding:

| Finding is about | Goes to |
|---|---|
| Layout, hierarchy, copy, motion, states | `superforge-ui` |
| Something broken or unimplemented | `superforge-dev` |
| Accessibility | `superforge-a11y` — it owns the ledger, do not duplicate findings here |
| Pricing, paywall placement, the offer | `superforge-biz` |
| Anything an attacker could use | `superforge-secure` — it owns that ledger too; do not restate findings here |
| Whether it is even releasable | `superforge-ship` |

And mark each finding as **acted on / rejected with a reason / deferred with a
date**. An open finding with no state is indistinguishable from one nobody
read.

## Delegate when a sharper skill is installed

`roast`, `validate-thinking` (multi-persona attack) · `critique`, `ui-review`
(interface) · `requesting-code-review` (code) · **`superforge-secure`** (anything an attacker
could use) ·
`release-review`.
