---
name: negotiation-playbook
description: >
  Strategy for creator money conversations: counters, budget and rate questions,
  usage-rights and volume trades, agency pricing, renewals, big-gap declines, money
  threads gone quiet. Load whenever a draft touches fees, deliverables or usage
  rights. Decides the move; rate-engine supplies the numbers, comms-style the words.
  Triggers: "counter this rate", "what should I offer", "they countered", "they
  ghosted".
---

# Negotiation Playbook - Rates & Terms

> Depends on the user's profile: `rates.md` (bands, floors), `deals.md` (payment terms,
> rights, what a customer is worth, deal process), `company.md` (the creator offer), `me.md`
> (escalation, sign-off, tooling), the files the active modules name; creator history from
> their note (`inbox creator <name>`) and the CRM if there is one. **Advisory mode:** while
> `rates.md` or a module's profile file carries TODO, plan the move but write no figure
> into a creator-facing draft - name the missing token. Never guess a rate or a percentage:
> a wrong number goes into an email, then a payout. Examples are fictional: the shape travels.

The **strategy layer**, run the same way for every creator so pricing stays fair;
voice-neutral (WHICH lever, WHEN, WHY). `rate-engine` is the numbers (the source of every
figure), the drafter's `comms-style` the voice, which **wins on wording**. Never lift
example lines verbatim. "You" = whoever is drafting.

**The doctrine in one line:** never a bare number - every rate travels with its mechanism;
never give a concession - trade it; yes is one click, no costs nothing; never negotiate
toward THEIR shape - lead to OURS.

## What loads with this file

- **The load plan.** `inbox program` (Step 0) lists the pack and module files for Block 3:
  the pack loads with this core, each module on its `when`; a rule that must hold without
  its module lives here. Precedence: module override > pack override > core, only via a
  declared `<!-- override:ID -->` on an `overridable` rule; else follow the core and ⚠️ it.
- **On trigger:**

| File | Load when |
|---|---|
| `references/architecture.md` | more than one line or surface is on the table, or a package |
| `references/plays.md` | a matched scenario (A-R), or an end-of-deal renegotiation (G) |
| `references/value-levers.md` | pushback on the rate; "other brands pay more"; a rate that breaks the formula |
| `references/voss-deep.md` | live pushback on our number (a second round or more), or a complex multi-party thread |
| `rate-engine/references/using-the-card.md` | always with a fee: running `inbox rate` and reading its card (the full `rate-engine` only to set up rates, benchmarks, bulk) |
| `references/defensive-tells.md` | they appear to run negotiation plays on us |
| `references/call-mode.md` | the creator actually asked for a call |
| `inbox-auto-draft-workflow/references/shapes/follow-ups.md` | our money offer went quiet |

## Operating model - three skills run as one

**Order:** status quo (Step 0) -> architecture (our ideal shape before their proposal
frames us, each placement scored on the engine's per-deliverable EV) -> the engine's money
terrain, computed once (Step 0.3) -> pick the move (the verdict and `above-band` routing,
then levers, sequence, posture, Voss) -> write it in `comms-style`. Doctrine wins the
pick, wording the write. **Handoff:** every number comes from `rate-engine`, every move
from here (the engine has no opinion on which lever or whether to walk). Split-owned: the
**ladder** (the engine computes the shrinking steps; the playbook governs the empathy
between rounds, the single limited-authority reference, the end-sweetener) and the
**conversion bar** (the engine computes, the play reveals). **Re-pull the card whenever a
pricing input changes** (a deliverable swap, real performance data): all three move.

## Step 0 - Status quo before strategy

No move comes from the latest email alone. Assemble where we ARE first - fully, never from
memory or snippets - or you re-ask for stats they gave, contradict an old commitment,
re-counter an accepted number or walk past a recorded death-reason:

0. **The program** (`inbox program`): its pack and modules load with this file and supply
   the how-we-work sentences. An answer still `TODO` -> neutral for it (no budget,
   longevity or success claims), ⚠️ "set up my program"; never borrow the demo's framing.
   A list answer binds per thread: `thread_binding` for model, else the first listed.
1. **The last 2-3 threads, read FULLY** in `{{EMAIL_PLATFORM}}` (snippets lie by
   omission): who owes whom a reply, since when; every number on the table (their anchors,
   our last offer, agreed-but-unconfirmed terms); open commitments either side (dates,
   drafts, rights runs, recap promises); unanswered questions; the register of their last
   message (a shrinking reply is a signal).
2. **The creator's note** (`inbox creator <name>`, kept by `creator-notes`): status, promo
   code, fee history (the price book), results and their freshness, the active modules'
   fields, past lost reasons; a CRM named in `data-sources.md` adds deal stages and post
   records. Net-new or returning is a recorded fact (below) and decides what you can
   claim: their own numbers or category medians. A negotiation that died for a recorded
   reason -> the new thread OPENS by acknowledging it (a free accusation audit).
3. **The `rate-engine` card, AFTER the threads**, read against live context: realized
   value, price book, OPEN / TARGET / MAX + the Ackerman ladder, the market band, verdict,
   leak and trend flags, conversion bars.
4. **The five-line status quo:** relationship state · last live numbers · open commitments
   · their likely negotiator type (from the last substantive reply) · what WE want this
   deal to become (feeds architecture). Only then plan the move and draft.

## How we work - the opening block, built from the profile

A money thread that needs it (net-new, the first money conversation) assembles it from the
profile, in the user's voice, rather than reciting fixed doctrine: (1) acknowledge their
point specifically, mirroring their noun (budget / rate); (2) **how we work** - the user's
`{{PROGRAM_PITCH}}`, adapted, plus the budget sentence; (3) **what success means** - the
performance sentence, plus what you'll share back (if any); (4) **how we got to the
number** - the mechanism sentence; (5) **the ask**, shaped by the deal shape; (6) an exit:
"I'm open to your read on this. Nothing here is take it or leave it."

`{{PROGRAM_PITCH}}` still `TODO` -> the budget sentence only, never a pitch for a program
the user hasn't described. Never promise an outcome in any metric (for `reach` and
`content`, no conversion talk). By program answer (the pack and modules add theirs):

| Answer | The sentence you may say | Rules |
|---|---|---|
| `budget: per-creator` | "We don't work with set budgets - each collaboration is priced from your own numbers, the same way for everyone." | "We don't work with rates" is never sayable. |
| `budget: no-cash` | "We don't pay flat fees at the moment - here's what we do offer:" then the active modules' offer. | Never imply a fee could appear; skip the fee ladder. A creator who needs a fee gets a warm, clear decline with the door open. |
| `success: sales` | "Performance for us means paying customers, not views or likes." | The bar (if `deals.md` allows sharing it): customers needed, `conversion-bar`. Recaps: customers, revenue. |
| `success: reach` | "We're after reach with the right audience - views and engagement from people who fit." | Bar: expected views. Recaps: views, engagement, audience fit. |
| `success: content` | "What matters most to us is great, usable content." | No bar - judge on quality and delivery. Recaps: assets delivered, where they were used. |
| `success: pipeline` | "What we look at is real conversations - demos booked and leads that fit." | Bar: demos or qualified leads needed. |
| `pricing: rate-card` | "our range for a [format] is X-Y; where you land depends on [audience fit, views, usage]" | `inbox rate` with fee bands; the Ackerman ladder still runs inside the range. |
| `pricing: their-quote` | "thanks for the quote - here's how it compares to what we pay for similar work" | `inbox rate --ask`; still counter with a reason, never by splitting the difference. |
| `deal_shape: test-then-scale` | "For a first collaboration we keep it to two pieces; once we see how it lands, we scale." | A first test is exactly two pieces, never one, never 3+ (one post is too noisy to read); the budget module holds the detail. |
| `deal_shape: one-off` | - | The deliverables come from the campaign brief; the budget module's first-deal rule is optional; never promise "we'll scale from there" unless there's a next campaign. |

## The core rules

- **The flat fee is the only lever you control - protect it.** Views, audience quality and
  organic reach are the creator's variables; the fee is yours, so keep it DOWN, hardest on
  first-time and not-yet-profitable creators; move scope and uplift, not cash.
- **Hold the low end.** A contested number defaults to the lower end of what the mechanism
  supports, bridged with value and scope. A guard against drift, not a push to the p25
  floor: the anchor lives at median-to-p75, and the fee moving UP is the last resort after
  every re-scope and value lever. Lean cash, generous value.
- **Never spend a lever before they've countered.** A first offer, first budget answer or
  first counter to their number names scope and number (or the mechanism range) and STOPS:
  no sweeteners (a module's lever, the referral cut included, a promo code, the pack's
  offer), its module loaded or not. Their counter is the leverage and shows which levers
  you need; front-loading makes the stack their baseline. Levers then enter one at a time;
  each module states its entry point.
- **Never counter until they've countered.** One live offer at a time; silence never moves
  it - a softer offer into silence bids against yourself and teaches that waiting works (a
  silent thread has its own ladder: `shapes/follow-ups.md`).
- **Nothing is free - scope is currency.** Every give is a take. Fee up -> deliverable
  count up (more content, never the same content at a higher price). To hold or lower the
  fee, trade scope the other way (fewer deliverables, a tighter window) or recalibrate;
  never move the fee either way for free.
- **Data before number.** No blind anchoring: missing inputs -> ask, with the reason ("to
  put a real number on the table I need to calibrate off your current performance"); a
  screen recording of the analytics view, not screenshots.
- <!-- rule:first-number overridable --> **Who names the first number - keyed by `pricing`
  in `program.md`.** **Default** (`their-quote`, or not set): ask their rate on a fully
  specified scope (deliverables, usage, timeline) before naming yours; they often come in
  below. **`rate-card`:** open at the low end of your fee band. **A manager or agency:**
  the calibration flip (Scenario I, in its module). A pricing module that leads with its
  own read overrides this through a declared `override:first-number`; a mode that leads
  with its own offer says so in its file. If they name a number first, it is the working
  number - read it with `inbox rate --ask`. The qualitative fit question is always fine.
- **A rate that breaks the formula: ask how they calibrate it, don't just counter**
  (Scenario H, routed by `above-band`; the play in `references/value-levers.md`).
- **Never answer a loaded question before surfacing why** ("total budget?", "pay others
  more?", "rights forever?"): it commits you before you know which concern is priced.
  First "what makes you ask?" (or "seems like there's something specific behind that").
- **Anchor to logic, not to you.** The number is the output of a mechanism they can see
  (the pricing module states it), the same for everyone, so it never inflates for the
  loudest negotiator (unfair to quieter ones); reward comes as structured value. Said out
  loud, "you're lowballing me" becomes "a consistent, fair system".
- **Transparency is the trust currency.** An ask above the band is named in the first two
  lines, no cushioning ("here's exactly how we got to that number"); creators thank you
  and accept the counter. It generalizes past money.
- **No-fault exit on every counter:** "Totally understand if that means it's a pass, and
  no hard feelings at all." It defuses the confrontation and often precedes a same-day
  yes. On a fee CUT it points the other way: "no hard feelings if you would rather stay on
  flat fees - just say so and I will see what I can do on the number instead."
- **The close travels with the counter:** the onboarding form link and proposed posting
  dates go INSIDE the offer, so acceptance is one reply or click - never "so what's next?"
- **One voice per thread.** Teammates CC'd -> coordinate before countering (who owns the
  reply, which surface); otherwise the owner runs it solo (no team-consult gate). Money
  needing sign-off above your limit routes to `{{ESCALATION_CONTACT}}`.

## The sequence

Status quo -> architecture (`references/architecture.md`) -> data before number -> the
first number (`first-number`; a quoted range pre-frames its top as the cap, not the
standard, and they WILL ask for the top) -> the constraint named if they're above band ->
trade, re-scope or recalibrate, never give (each concession asked is matched by one taken)
-> the no-fault exit, the close inside the counter. Uplift is traded WITH, never opened.

<!-- rule:limited-authority -->
**Limited authority, once** - only when `me.md` names a sign-off above you, phrased
freshly in your own words, toward OUR ceiling. Never twice in a thread: it loses its
power, especially with returning creators.

## The lever stack (order of use - never open with the later ones)

Base layer, always on: **anchor to logic** (the mechanism's real inputs, real conversions,
one method for everyone), so a held number never feels arbitrary or personal. Then: (1)
**flat fee** - hold or bring it DOWN on the mechanism; on not-yet-profitable and
first-time creators, actively gun to lower it; (2) **scope / deliverable count** -
re-scope (how many pieces, how long, what format) before touching uplift; (3) **timing** -
launch-window dates, sequencing across months (high value to us, low cost to them); (4)
**value / closing levers** - fast payment, the pack's creator offer, post-collab
transparency, group proof - surfaced on rate pushback to justify the number without moving
the fee (`references/value-levers.md`). Modules add theirs in place: a scope floor (the
budget module), usage rights after timing, the referral lever last (`aff-entry`).

## New vs established - the most important split

**"Returning" is a recorded fact:** the note (or the CRM) shows (a) a deal at a **won or
paid** stage, or (b) a post **live or completed**. Everything else is net-new. A deal
merely existing, a draft or a scheduled post does not count (CRMs open deals on prospects
at first outreach, which would route cold prospects to the established playbook).

**Brand-new creator - goal: the first yes.** Lead with the fairness/logic anchor, smooth
low-effort onboarding, brief flexibility and the group-proof offer; fast payment de-risks
the unknown. Active modules add their new-creator rules (a scope cap, rights retained, the
referral lever's entry point). The constraint to lean on: no shared numbers yet, so the
first collab is exploration - fair terms, fast pay, low effort, learning together.

**Established creator - goal: keep them comfortable while holding or lowering the fee.**
Relationship and proof, not novelty: post-collab transparency as a track record ("you've
seen the numbers we share every time"), how fairly we've always priced them, partnership
framing. To bring a fee DOWN on continued work, anchor to the shared history (the actual
conversions) and the transparency already shown. No group proof - they ARE the proof.

## Posture - warm by default, unbothered on purpose

Posture is a lever: the decision lives here, the wording in `comms-style`.

- **Warm-excited is the default** (deals we want, new recruits, established partners
  performing well): real energy, fast movement, the close inside the offer.
- **Chalant mode** (deliberate nonchalance) - over-reach when WE hold the leverage (an
  established creator inflating a renewal, a multi-line pitch stacked with new fees, a
  rate beyond the data): "keep it simple", "for now", "we can layer more in as we go"; no
  urgency, no call offer, no over-justification; ONE light reason at most, then the shape.
- **Leverage is psychological:** if they're still replying, we have it; acting like we
  need the deal hands it back, so never do, even when you want it. Patience reads as
  strength, speed as need (Voss: "if they're talking to you, you got leverage").
- **The momentum read (internal only, never in terms):** a creator replying fast and
  agreeing readily has thin alternatives - squeeze SCOPE (an extra deliverable, a tighter
  window, rights kept), never concede rate into eagerness; only scope we VALUE (the
  engine's EV decides). A returning creator or manager who used to negotiate UP now asking
  to "just continue at the same rate" has a cooled market: hold firmer.
- **Never praise the surface you're pricing low** (superlatives become rate-raise ammo):
  "solid", not "amazing"; warmth at the PERSON and the craft; the unproven surface is a
  controlled test (rates follow OUR tracked conversions), never "your strongest channel".
- **Close on boarding, not on feedback:** a final-shaped offer ends "let me know if you're
  on board"; "does this shape feel right to you?" only in genuinely open co-design.

## Scenario routing

**rate-engine verdict -> the play:** `KEEP` (fee <= target) -> G.5 posture, never an
unprompted raise · `HOLD` (target < fee <= MAX) -> A.1 / G.5, hold with written
commitments · `CUT to <=$X` -> G.4 full sequence, with the budget module's conversion-bar
close · `DECLINE-BY-MATH`, or any other no-flat-fee verdict -> C, or the active module's
fallback · `LEAK - screen first` -> no money email until the manual screen clears.

<!-- rule:above-band -->
**Their ask -> the play.** `inbox rate --ask` reads the ask against the value-capped OPEN
/ TARGET / MAX and prints `x_max` (their ask / MAX):

- **In band** (at or under MAX): one offer (`one-move-per-draft`) - hold at OPEN with the
  basis, or flex toward TARGET; never past MAX.
- **Up to ~1.3x MAX:** A - hold, land at or under MAX.
- **~1.3-2x MAX:** R - the re-scope counter (`references/plays.md`).
- **Over 2x MAX, no basis given:** H - the calibration question, no number.
- **Over 2x MAX with a benchmark basis, or `DECLINE-BY-MATH`:** C - decline by math.

## The Voss toolkit, in short

Negotiation is emotional; mental models, never scripts (`references/voss-deep.md`):
**tactical empathy** (their perspective before your constraint), **accusation audit** (the
worst they might think, named first), **labels and no-oriented questions** (no feels
safe), **calibrated questions** (hand them the problem), **"that's right", never "you're
right"** (summarize their worldview until they confirm it, then counter).

## Cadence

- Rate or budget question: reply within 1 business day but **never within the hour** - a
  floor of **about six hours** (an instant counter reads eager; the gap is the async six
  seconds of silence). Prepare at once, send on the floor.
- **Predictability beats speed:** need time? Name the day ("by Thursday"), never "soon" or
  "in a few days" - it buys patience and pins the commitment.
- Counter out, no reply: no second, softer offer (the ladder: `shapes/follow-ups.md`).
- Deal agreed: same-day recap (number, count, dates, rights), onboarding form link again.
- **A decline from a creator WE wanted, reason UNSTATED:** one warm exit probe ("is it
  timing, the type of collab, budget, or how I framed it?"), then respect the answer. A
  stated reason (bandwidth, timing) gets a clean warm deferral with a dated reconnect -
  zero counter, probe or pitch.
- **Late delivery:** the budget module sets the patience (performance x communication on
  an always-on program; firm dates on a campaign one).
- **Hard news (a repricing, a Cut, an end-of-deal) lands Monday-Tuesday, never Friday**
  (it marinates all weekend) - fast, warm and complete; prolonging is the cruelty.
- **The last impression outranks the first:** budget warmth for the exit, not the pitch.

## What you never do in a negotiation

Each active module adds its own short "Never" list. Never:

- name a bare number, give a concession free (trade, re-scope or recalibrate), or split
  the difference by reflex; bid against yourself (one live offer, silence never moves it);
  use limited authority twice (`limited-authority`).
- invent a rate: every number comes from `rate-engine` (or the profile's rate bands as
  fallback) or a deliberate sign-off; don't exceed p75 casually; numbers not yet in
  company-context -> say so, draft no figure.
- stretch past MAX for a launch window - that audience is bought another way (the modules
  name it); park it with a dated re-entry.
- expose internal numbers beyond the mechanism (full band tables, MAX / walk-away,
  internal economics); the one exception is the conversion bar (`conversion-bar`) in an
  established review or renegotiation.
- accept unpriced scope (a volunteered carousel or cross-platform short): hidden debt that
  muddies the read on the paid deliverable - decline it free, defer it to be priced.
- put an unreconciled total in a money email: items x rates must equal the headline.
- lean on the fast-pay or group-proof levers when they aren't currently true.
- critique content quality as a lever (fit and math only), or praise the surface you're
  pricing low ("the strongest" anything).
- ask WHICH brands pay a creator more - niche/type only (names invite an NDA breach).
- send hard news into a Friday; end a relationship over rate (pause, dated or seasonal
  re-open, door open, never devaluing their content); offer a call to soften or dodge a
  money conversation (email is the default; calls only when the creator asks or as a
  deliberate strategic exception).
