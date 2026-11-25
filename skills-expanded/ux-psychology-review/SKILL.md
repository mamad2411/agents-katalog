---
name: ux-psychology-review
description: Apply design psychology — cognitive biases and behavioral principles — to review UI/UX work and generate ideas, recommendations, and critiques grounded in named principles. Use this skill whenever the user asks for a UX review, design critique, conversion analysis, onboarding/checkout/pricing/paywall feedback, "why might users drop off here," "how do I get users to X," or any product-design task where human psychology matters. Also trigger when the user wants to brainstorm UX improvements, evaluate a flow against best practices, name the principle behind a pattern they've seen, or check a design for dark patterns. Don't wait for the user to say "psychology" — design reviews and UX recommendations are this skill's bread and butter even when phrased casually ("does this signup flow look ok?", "ideas for our pricing page", "review this dashboard").
---

# UX Psychology Review

A working knowledge base of **106 cognitive biases and design principles** for reviewing UI/UX work and generating recommendations grounded in named psychology. Adapted from growth.design's "Psychology of Design" framework, which builds on Buster Benson's cognitive bias codex.

## What this skill does

Two jobs, often blended:

1. **Review** — Given a design (screenshot, description, flow, or live URL), diagnose which principles it leverages well, which it violates, and which dark patterns it risks.
2. **Generate** — Given a UX problem ("how do we improve activation", "what should the pricing page do"), propose concrete, principle-backed ideas.

Both modes name principles explicitly. A recommendation like "add social proof near the CTA — this leverages the Bandwagon Effect and reduces decision anxiety" is more useful than an unattributed gut call, because the user can challenge it, extend it, or check it against literature.

## The framework: 4 stages of user cognition

Buster Benson's codex sorts cognitive biases by the *problem* the brain is trying to solve. Every time someone interacts with your product, they:

1. **Filter information** — too much input, the brain ignores most of it. *(Visual hierarchy, Hick's Law, Cognitive Load, Selective Attention, Banner Blindness…)*
2. **Search for meaning** — gaps in the input get filled with assumptions and stories. *(Mental Models, Familiarity Bias, Halo Effect, Authority Bias, Confirmation Bias…)*
3. **Act within time pressure** — decisions get rushed; shortcuts win. *(Loss Aversion, Sunk Cost, Default Effect, Scarcity, Reciprocity…)*
4. **Store what mattered** — memory is selective and reconstructive. *(Peak-End Rule, Serial Position Effect, Zeigarnik Effect, Spacing Effect…)*

Good design respects all four. Bad design fights one or more.

## How to work through a request

### When reviewing a design

1. **Get the artifact in front of you.** If the user shared a URL, fetch it. If a screenshot, look carefully. If only a description, ask one or two specific questions before guessing — designs are visual, and a vague description leads to vague feedback.

2. **Identify the user's goal at this surface.** Onboarding? Checkout? Re-engagement? Pricing decision? You can't review a design without knowing what success looks like.

3. **Walk the four stages.** For each, note which principles are in play:
   - *Filter:* Where does the eye go? Is the hierarchy clear? Is there cognitive overload?
   - *Meaning:* What story will the user tell themselves? Do labels/icons match their mental models?
   - *Action:* What's the easiest path? What friction exists? What's the cost of choosing wrong?
   - *Memory:* What will they remember tomorrow? What's the peak? The end?

4. **Output a structured review.** Use this shape:
   - **Strengths** — 2-4 principles the design uses well (named, with the specific element)
   - **Issues** — 2-5 principles being violated or missed (named, with the specific element and why it matters)
   - **Dark pattern flags** — anything that risks crossing the line (see *Dark Patterns* below)
   - **Recommendations** — concrete changes, each tied to a named principle

### When generating ideas

1. **Restate the problem in terms of user behavior.** "How do we improve activation?" → "What makes a new user reach their first 'aha' moment faster?"
2. **Pick 3-5 principles most relevant to that behavior.** Use the use-case index in `references/by-use-case.md`.
3. **For each, propose one concrete tactic.** Tactic + principle + rationale. Skip principles that don't yield a concrete idea — don't pad.
4. **Flag tradeoffs.** Many principles have "when it backfires" notes. If a recommendation could backfire, say so.

### When the user names a single principle

Just answer their question. Pull the entry from the relevant reference file, give them the definition, examples, and tips. Don't run the whole review framework.

## The full index — all 106 principles

Each principle is listed with its category, a one-line summary, and the reference file where the full entry lives. Read the reference file when you need the definition, examples, "when to apply," "when it backfires," and citations for a specific principle.

### 🙈 Filter information *(the user's brain ignores most of what you put in front of it)*
*Full entries: `references/01-filter-information.md`*

| # | Principle | One-liner |
|---|---|---|
| 1 | Hick's Law | More choices → slower decisions. Reduce options or chunk them. |
| 2 | Visual Hierarchy | Size, position, contrast, and whitespace tell the eye what matters. |
| 3 | Cognitive Load | Every element costs mental effort. Strip what doesn't earn its place. |
| 4 | Selective Attention | Users see what they're looking for and miss the rest. |
| 5 | Banner Blindness | Anything that looks like an ad gets skipped, even when relevant. |
| 6 | Fitts's Law | Bigger and closer targets are faster to hit. Make CTAs accordingly. |
| 7 | Anchoring Bias | The first number/option seen frames everything that follows. |
| 8 | Centre-Stage Effect | Items in the middle of a row are perceived as the default/best. |
| 9 | Contrast | Difference draws attention. Use it deliberately, not decoratively. |
| 10 | Von Restorff Effect | The element that stands out from a set is the one remembered. |
| 11 | Aesthetic-Usability Effect | Pretty designs feel easier to use, even when they aren't. |
| 12 | Progressive Disclosure | Hide complexity until the user needs it. |
| 13 | Signifiers | Visual cues that hint at how to interact (underlines, shadows, hover states). |
| 14 | Law of Proximity | Things close together are perceived as related. |
| 15 | Law of Similarity | Things that look alike are perceived as a group. |
| 16 | Law of Common Region | Items inside the same boundary are grouped, even if far apart. |
| 17 | Law of Closure | The brain completes incomplete shapes — useful for icons, hurtful for cut-off content. |
| 18 | Visual Anchors | Eye-leading elements (arrows, gaze, lines) that guide attention. |
| 19 | Juxtaposition | Place two elements together to create comparison or association. |
| 20 | Framing Effect | The same fact lands differently depending on how it's worded ("90% fat free" vs "10% fat"). |
| 21 | Priming Effect | Prior stimuli shape later perception. What the user saw 10 seconds ago matters. |
| 22 | Nudge | Subtle defaults and cues that steer without coercion. |
| 23 | External Trigger | Notifications, emails, banners that prompt return. |
| 24 | Internal Trigger | The user's own emotional state (boredom, anxiety) that prompts return. |
| 25 | Spark Effect | Tiny animations and microinteractions that delight without distracting. |
| 26 | Tesler's Law | Every system has irreducible complexity. Don't push it onto the user. |
| 27 | Decoy Effect | Adding a clearly-worse option makes a target option look better. |
| 28 | Attentional Bias | Users notice what aligns with their current concerns and ignore the rest. |
| 29 | Confirmation Bias | Users seek evidence that supports what they already believe. |
| 30 | Expectations Bias | Prior expectations color the perceived experience, sometimes more than reality. |
| 31 | Survivorship Bias | Studying only "winners" hides the lessons in failures. |
| 32 | Empathy Gap | We underestimate how much our future emotional state will differ from our current one. |
| 33 | Feedback Loops (Retroaction) | Visible response to action reduces uncertainty and builds confidence. |
| 34 | Curiosity Gap | A teased-but-incomplete piece of information demands closure. |

### 👀 Search for meaning *(users invent stories to fill gaps in what they see)*
*Full entries: `references/02-search-for-meaning.md`*

| # | Principle | One-liner |
|---|---|---|
| 35 | Mental Model | Users arrive with prior beliefs about how things work. Match those, or pay the cost. |
| 36 | Familiarity Bias | Familiar = trusted. Reusing patterns reduces friction. |
| 37 | Skeuomorphism | Mimicking real-world objects helps users transfer expectations. |
| 38 | Halo Effect | One strong positive trait spreads to color overall perception. |
| 39 | Authority Bias | Endorsements, certifications, and expert framing carry disproportionate weight. |
| 40 | Social Proof | "Others did this" reassures the hesitant. |
| 41 | Bandwagon Effect | The pull to do what the crowd does, even against personal preference. |
| 42 | Aha! Moment | The first concrete value the user feels — make it fast. |
| 43 | Spotlight Effect | Users assume they're being watched/judged more than they are. |
| 44 | Hindsight Bias | After the fact, outcomes seem inevitable. Useful for confidence-building UX. |
| 45 | Survey Bias | Asking the question changes the answer. Question design shapes data. |
| 46 | Cheerleader Effect | Items presented as a group look more attractive than alone. |
| 47 | Singularity Effect | One unique element commands disproportionate attention. |
| 48 | Scarcity | Rare = valuable. Often abused; use real, verifiable scarcity only. |
| 49 | Streisand Effect | Suppressing information amplifies it. |
| 50 | Cashless Effect | Abstracting payment (cards, points, in-app currency) reduces felt cost. |
| 51 | Pseudo-set Framing | Showing progress toward a "set" (3 of 5 done) drives completion. |
| 52 | Storytelling Effect | Narrative is remembered and trusted more than facts alone. |
| 53 | Fluency Heuristic | Easy to process = perceived as more true, more valuable. |
| 54 | Pratfall Effect | A small visible flaw makes something more relatable, not less. |
| 55 | Barnum Effect | Vague personality descriptions feel personally accurate. |
| 56 | Picture Superiority Effect | Images are remembered far better than words. |
| 57 | Self-Reference Effect | "Your" beats "the." Personalized framing sticks. |
| 58 | IKEA Effect | Effort invested in something raises its perceived value. |
| 59 | Endowment Effect | Once owned, things feel more valuable than equivalent unowned ones. |
| 60 | Curse of Knowledge | Experts forget what it's like not to know. Designers especially. |
| 61 | False Consensus | Designers overestimate how many users think like them. |
| 62 | In-group Bias | Users trust voices that signal membership in their tribe. |
| 63 | Negativity Bias | Bad experiences/reviews weigh more than good ones. |

### ⏰ Act within time pressure *(decisions are rushed and shortcut-driven)*
*Full entries: `references/03-act-within-time.md`*

| # | Principle | One-liner |
|---|---|---|
| 64 | Loss Aversion | Losing $10 hurts more than gaining $10 pleases. Frame accordingly. |
| 65 | Sunk Cost Fallacy | Past investment makes users reluctant to abandon a path. |
| 66 | Default Effect | Whatever's pre-selected is what most users will keep. |
| 67 | Status Quo Bias | Change feels risky. Inertia keeps users where they are. |
| 68 | Reciprocity | Free value creates a felt obligation to return the favor. |
| 69 | Commitment & Consistency | Small initial commitments lead to larger ones. |
| 70 | Foot-in-the-Door | Yes to a small ask makes yes to a bigger ask easier. |
| 71 | Door-in-the-Face | An over-large ask makes a moderate ask feel reasonable. |
| 72 | Goal-Gradient Effect | Effort accelerates near the finish line. Show progress. |
| 73 | Endowed Progress Effect | Pre-filled progress (2 of 10 stamps free) speeds completion. |
| 74 | Investment Loop | Users invest (data, customization, friends) → switching cost rises. |
| 75 | Variable Reward | Unpredictable rewards drive engagement (and addiction). |
| 76 | Hyperbolic Discounting | Now beats later, even when later is much better. |
| 77 | Temptation Bundling | Pairing a "should" with a "want" raises adherence. |
| 78 | Decision Fatigue | Each choice depletes will. Reduce choices late in a flow. |
| 79 | Choice Overload | Too many options paralyze. Default + filter + recommend. |
| 80 | Paradox of Choice | More options often reduce satisfaction with the chosen one. |
| 81 | Reactance | Users push back against perceived loss of autonomy. |
| 82 | Forer/Barnum (Action) | "This was made for you" framing increases buy-in. |
| 83 | Labor Illusion | Visible effort (loading bars, "searching 1,200 hotels…") makes results feel valuable. |
| 84 | Occam's Razor | Simpler explanations and paths are preferred. |
| 85 | Friction | Strategic difficulty: where to add it, where to remove it. |
| 86 | Confirmation (Action) | Make destructive actions take a second step. |
| 87 | Convenience Bias | Easier > better, in the moment. |
| 88 | Optimism Bias | Users overestimate good outcomes ("I'll cancel before the trial ends"). |
| 89 | Planning Fallacy | Users underestimate how long tasks take, including yours. |
| 90 | Risk Aversion | Faced with equal expected value, users prefer the certain option. |

### 💾 Store what mattered *(memory is selective and reconstructed)*
*Full entries: `references/04-store-what-mattered.md`*

| # | Principle | One-liner |
|---|---|---|
| 91 | Peak-End Rule | An experience is remembered by its peak moment and its end. |
| 92 | Serial Position Effect | First and last items in a list are remembered best. |
| 93 | Primacy Effect | First impressions disproportionately shape lasting judgment. |
| 94 | Recency Effect | The most recent item/interaction is most available in memory. |
| 95 | Zeigarnik Effect | Unfinished tasks linger in memory better than completed ones. |
| 96 | Spacing Effect | Spread-out exposure beats massed exposure for retention. |
| 97 | Method of Loci / Spatial Memory | Spatial layout helps recall. Consistent placement matters. |
| 98 | Chunking | Group information into 5-9 unit clusters; users can hold those in working memory. |
| 99 | Miller's Law | "7 ± 2" working memory limit. Don't ask the user to hold more. |
| 100 | Storytelling Recall | Stories are remembered as wholes; bullet lists are not. |
| 101 | Mere Exposure Effect | Repeated exposure increases liking, even without explicit reasoning. |
| 102 | Google Effect | If users can look it up, they don't memorize it. Don't expect them to. |
| 103 | Levels of Processing | Deep engagement (think, do, teach) outlasts shallow (read, watch). |
| 104 | Picture Superiority (Memory) | Visuals outlast text in long-term recall. |
| 105 | Tesler's Law (Memory side) | Complexity the user has to remember is complexity you failed to absorb. |
| 106 | Method of Repetition | Spaced repetition cements habits — for better and worse. |

## Dark patterns: when these principles hurt users

Most of these principles are neutral tools. Some, deployed against the user's interest, become **dark patterns** — and reviewing for them is part of this skill's job.

The line is roughly: *Is the principle being used to help the user reach their goal, or to extract from the user against their goal?*

Common conversions to watch for:

| Principle | Ethical use | Dark pattern variant |
|---|---|---|
| Scarcity | Real low-stock warnings | Fake countdown timers, fabricated "only 2 left!" |
| Loss Aversion | Save-progress nudges | "You'll lose your discount forever!" pressure |
| Default Effect | Sensible pre-selection | Pre-checked email opt-ins, hidden subscriptions |
| Sunk Cost | Show progress earned | Trapping users in cancellation mazes ("but you've earned 47 points!") |
| Social Proof | Real testimonials | Fake reviews, inflated user counts |
| Reciprocity | Genuine free value | Manufactured "gifts" with strings attached |
| Authority | Real credentials | Fake awards, manufactured expert quotes |
| Friction | Reduce on goal paths | Add to cancellation, refunds, account deletion |
| Confirmshaming | (no ethical version) | "No thanks, I hate saving money" decline buttons |
| Forced Continuity | (no ethical version) | Auto-renew with hidden cancel, free trials with no reminder |

When reviewing, flag these explicitly — even if the user didn't ask. A "Dark pattern flags" line in the review with zero items is a reassuring signal too.

When the user asks for ideas, prefer ethical framings. If a tactic *only* works as a dark pattern (confirmshaming, forced continuity), say so and suggest a non-coercive alternative that still moves the metric.

## How to use the reference files

Each category file has the full entry for every principle in that category, in this shape:

```
## [Number]. [Principle Name]
**Category:** [Filter / Meaning / Time / Memory]
**Also known as:** [aliases if any]
**Use cases:** [pricing, onboarding, retention, …]

**Definition.** [1-2 sentences, plain English.]

**Why it works.** [The cognitive/emotional mechanism.]

**Examples in the wild.**
- [Concrete UX example with what it does and why]
- [Second example, different surface]

**When to apply.** [Specific UX situations where this is the right tool.]

**When it backfires.** [Failure modes, dark-pattern adjacency, overuse.]

**Citations.**
- [Source 1]
- [Source 2]
```

There's also `references/by-use-case.md` — a cross-index from common UX problems (pricing, onboarding, paywall, cart abandonment, retention, error states…) to the principles most relevant. Use this when generating ideas: pick the use case, look up the relevant principles, then pull their full entries.

## Output style

- **Name principles when you use them.** "This works because of the Peak-End Rule" beats "users will remember this."
- **Be concrete.** "Move the testimonial above the CTA" beats "consider social proof."
- **Don't list everything.** A review of 15 principles is unreadable. Pick the 5-7 that matter most for *this* design.
- **Disagree when warranted.** If the user pushes a principle that's wrong for their context, say so and explain. The skill exists to be useful, not validating.
- **Cite when uncertain.** If you're stretching beyond what the reference files contain, say "I'm extrapolating here" and note it.

## Notes on sources

This knowledge base draws from:
- **growth.design** — the original 106-principle framework (the structure and category approach come from here)
- **Buster Benson's cognitive bias codex** — the 4-stage organizing model
- **Nielsen Norman Group, Interaction Design Foundation** — applied UX research
- **Behavioral economics literature** — Kahneman, Thaler, Cialdini for the underlying mechanisms
- **Wikipedia + The Decision Lab** — for cross-checking definitions

Specific citations live in each principle's entry. When the literature disagrees on a definition or effect size, note the disagreement rather than picking one.
