---
name: verify-then-advise
description: "Governs any recommendation that depends on facts OUTSIDE the codebase that change faster than training data — vendor products, certifications, exam codes, SKUs, APIs, pricing, licensing, partner programs, job markets, industry trends, hype cycles. Use this skill whenever the user asks which certification or exam to take, whether a product/API/SKU/exam is still current or supported or retired, what a job market wants, whether to adopt a technology, what the trends are in a field, how a field will look in N years, or asks for any 1–5 year career or technology roadmap — and ALSO whenever your own answer is about to name a specific vendor product, credential, price, or market claim, even when the user never asked you to verify anything. The failure it prevents is confident, well-structured advice built on facts that quietly expired: model memory is stale by construction and vendors retire things faster than anyone expects. Do NOT use for questions answerable from the user's own code or system (that is study-design-verify), for a single fact lookup with no recommendation attached, or for pure preference questions with no external facts at stake."
argument-hint: "[the recommendation or question to verify]"
effort: max
---

# Verify, Then Advise

Some advice is wrong the moment you give it, and nothing in the answer reveals it. The structure is sound, the reasoning holds, the tone is confident — and the central fact retired six weeks ago.

This skill exists for recommendations that rest on **facts you do not own**: what a vendor still sells, what an exam still certifies, what a market actually pays for. Those facts have a half-life, and your memory of them does not come with an expiry date attached.

The governing idea, borrowed from the skills-lifecycle literature: *a stale skill is worse than no skill, because it gives confident but outdated instructions.* Stale **model knowledge** fails the same way, and is harder to notice, because there is no file to check the date on.

## When to invoke

"Which certification should I take?" · "Is X still supported?" · "What's the market for Y?" · "Should we adopt Z?" · "What are the trends in…?" · "Where should my career go in five years?" · any roadmap spanning more than a few months.

**Also invoke unprompted** when your own draft answer is about to name a specific product, credential, exam code, price, or market claim. The user asking a soft question does not make the underlying facts soft. This is the common miss: the skill fires on *what you are about to assert*, not only on what was asked.

## When not to

- The answer lives in the user's own code or system → `study-design-verify`
- A single fact lookup with no recommendation riding on it → just look it up
- Pure preference or taste, no external facts at stake → just answer

## Why this is hard

Two forces work against you, and they pull in the same direction:

**Your knowledge has no timestamp.** You remember a given exam code as the architect certification because it was, for years. Nothing in that memory announces that it retired. Recall feels identical whether the fact is current or three years dead.

**Confident structure hides rot.** A well-organised recommendation — tiers, timelines, trade-offs — reads as researched. The scaffolding lends credibility to whatever sits inside it, including a dead product at the centre.

So the discipline cannot be "be careful." It has to be a mechanical pass that runs before the advice ships.

---

## The method

Six stages. Skipping one is a decision; make it out loud.

### 1. Inventory the moving parts

Before researching anything, list every external entity your recommendation will name: products, credentials, exam codes, SKUs, APIs, prices, programs, market claims. This list is your verification queue.

Do this first because it is much harder to notice an unverified fact once it is embedded in a persuasive paragraph. Extract them while they are still just a list.

### 2. Lifecycle-verify every entry

For each item: does it still exist, in the form you remember, today?

Go to the vendor's **retirement registry** — the authoritative list of what is dead and what is scheduled — not a blog, not a summary, and not memory. Most vendors publish one:

- Microsoft: `credentials/support/retired-certification-exams` and `credential-retirement`; individual exam study guides also carry a retirement warning banner at the top
- Cloud/API vendors: deprecation schedules, API version support matrices, end-of-life pages
- Partner/licensing programs: the program's own requirements page, which changes quietly

> **Why this stage is first and non-negotiable.** In the session that produced this skill, the recommendation was about to be "target PL-600." PL-600 had retired **six weeks earlier** — along with roughly ten other certifications inside a single quarter. Nothing about recalling it felt uncertain. One registry lookup caught it; no amount of careful reasoning would have.

When a vendor rewrites a whole product or credential line at once, that is itself a finding worth reporting — it is the clearest statement of direction you will get for free.

### 3. Hunt the counter-signal

Identify whose signal your recommendation currently rests on, and go find someone with a different incentive.

A vendor's own materials tell you what the vendor wants to be true. That is genuinely informative — but it is one party, and usually the most optimistic one. Before advising, deliberately look for the contradicting view: independent analysts, adoption data, post-mortems, practitioner reports.

> In the same session, the first five-year recommendation came entirely from one vendor's credential portfolio, read at the top of a hype wave. Deliberately hunting a counter-signal surfaced an analyst finding that the technology sat at peak expectations with **over 40% of projects expected to be cancelled within eighteen months**. That did not reverse the direction — but it changed the advice from "learn the shiny thing" to "learn to make the shiny thing survive production," which is a materially different plan.

If you cannot find a counter-signal, say so. "I looked for a contradicting view and did not find one" is a real finding. "I did not look" is not the same thing, and must not be reported as if it were.

### 4. Count primary artifacts before citing commentary

For any claim about what a market wants, count the actual artifacts before quoting anyone's summary of them.

Job postings, changelogs, release notes, package download counts, repository activity, pricing pages. Fifty real postings tell you more than any number of trend pieces — and trend pieces are written to rank in search, not to be accurate.

> This one reversed a published conclusion mid-session. Trend articles supported an "AI governance is in demand" positioning. Counting the actual listings — about 25 in one national market, 23 in another — found that phrasing in essentially **none** of them. The positioning was a forward bet on a later year, not a present-day hiring filter. Same underlying direction; completely different advice about timing.

Counting is usually cheap. Do it before, not after, someone asks whether you did.

### 5. Read the institutional incentive, not just the person's

The person asking has goals. The organisation around them has requirements, deadlines, and exposures — and those are often more actionable, because institutions pay for things individuals merely want.

Ask: what does the employer, the team, the customer, or the program need? What are they at risk of losing? What deadline is already running against them?

> The single most useful output of the originating session came from this stage. Reading the *employer's* partner-program requirements revealed that three of the four credentials qualifying for a scoring category had just retired, creating a dated cliff. That turned "please fund my exam" into "I can protect our designation" — a completely different conversation, and one the individual's own goals would never have surfaced.

### 6. Compute headline numbers; never sum rounded parts

Any number that carries the recommendation gets computed from source values, in a script, once.

Rounding each component and summing them compounds the error into exactly the figure people will quote back at you.

> A headline figure in that session's spec read 72.6%. Recomputing from the underlying weights gave **72.8%** — the earlier number had been assembled from per-item gains that were each already rounded. The conclusion survived; the number in the acceptance criterion did not.

---

## Grade every claim

The point of grading is not decoration. It tells the reader which parts of your advice they can act on directly and which they must re-check themselves — and it forces you to notice when a load-bearing claim is resting on a blog post.

| Grade | Means |
|---|---|
| **Verified-primary** | You read the authoritative source yourself — vendor registry, official docs, the actual postings |
| **Corroborated** | Two or more independent sources agree, but you did not read the primary |
| **Directional** | Single source, or an aggregator, or content with an incentive to inflate. Usable for direction; never as an anchor |
| **Unverified** | Asserted from memory or inference. Say so plainly, or cut it |

Salary aggregators are the canonical **directional** case: in the originating session the same job title was reported at both ~$124k and ~$176k. A number that disagrees with itself by 40% can indicate a trend, but it must never anchor a negotiation, and saying so is part of the deliverable.

**Corroboration between independent sources is worth flagging explicitly.** When two unrelated parties measuring different things land on the same answer, that agreement is stronger evidence than either alone — and readers will miss it unless you point it out.

## Deliverable shape

Whatever the format, three things are required:

1. **Every load-bearing claim carries its source and its grade.** Inline is fine; a table is fine. Ungraded assertions read as verified whether or not they are.
2. **Weak evidence is named, not smoothed.** "Directional only — sources disagree by 40%" is more useful than a confident average that hides the spread.
3. **State what you did not check.** Geographies you skipped, sources that blocked you, questions you left open. A gap the reader knows about is a caveat; a gap they discover later is a defect.

Where a recommendation depends on something with a date attached — a retirement, a deadline, a cliff — surface the date prominently. That is the part that will silently invalidate the advice.

## Red flags

Recognise these as the moment to run the method, not skip it:

| Thought | Reality |
|---|---|
| "I know this product well" | Knowing it well is exactly how you miss that it retired. Familiarity is not currency. |
| "The user only asked casually" | The facts are not casual. Soft question, hard facts. |
| "This is the obvious industry direction" | Obvious directions are usually one vendor's marketing, well distributed. |
| "The trend articles all agree" | Articles cite each other. Agreement among secondary sources is not corroboration. |
| "Counting postings is overkill" | It is usually ten minutes, and it has reversed conclusions. |
| "Close enough on the number" | The rounded number is the one that gets quoted back at you. |
| "I'll caveat it at the end" | A caveat under a confident recommendation does not survive being skimmed. Grade inline. |

## Relationship to neighbouring skills

- **`career-growth`** — a five-station quarterly career review: evidence-graded skill inventory, job-market survey, a four-test "moat" selection gated on the user's own pick, then a certification-driven study plan. It owns the person-side analysis and the decision structure; it delegates all outside-world fact verification — certifications, exam codes, market demand — to this skill. Precedence: reach for `career-growth` for the full periodic review; reach for this skill for a single verified recommendation, or to check whether one named product or credential is still current.
- **`study-design-verify`** — same evidence-grounded stance, aimed at *the user's own system*. That one studies code, schemas, and live data. This one handles facts nobody in the room controls. They compose: study the system with that, verify the outside world with this.
- **`scrutinize`** — reviews a plan or change already on the table. This runs earlier, while the advice is still being formed.
- **`reflect`** — where the lessons from a mis-advised session get routed, including into this skill.
