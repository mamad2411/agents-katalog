---
name: outreach-execution
description: Execute a cold-outbound campaign that has already been planned — write and refine cold email sequences (signal-led first touch under 100 words, follow-up + breakup, VP variant, quality checklist), execute LinkedIn/cold-call/video-outreach channel touches, triage and respond to inbound replies (8 reply types), benchmark pipeline performance stage by stage, and automate the whole sequence via n8n. Use after `outreach-planning` has produced an outreach brief with ICP, personas, contact list, and campaign architecture. Also use when replies are coming in, when campaign numbers need interpreting, or when a validated manual process is ready to automate.
---

# Outreach Execution

Consolidates: `outreach-copywriting`, `outreach-channels`, `outreach-replies-pipeline`, `outreach-automation`.

This skill runs after `outreach-planning` produces the brief. It covers everything from first message to closed deal or opt-out: writing the copy, executing across channels, handling what comes back, reading the pipeline, and automating the whole thing.

---

## PART 1: COPYWRITING

Consumes `outreach-planning`'s persona cards, offer statements, and per-contact trigger data.

### 1.1 First touch: signal-led, under 100 words

Open with the specific trigger from the list (not a generic compliment or "I noticed you're in [industry]") — the trigger is proof the email isn't mass-blasted. State the implied pain in one sentence, the outcome-framed offer in one sentence, and a low-friction ask (a question, not "let's book 30 minutes") in one sentence. Under 100 words total — anything longer reads as a pitch, not a message from a person who did their homework.

### 1.2 Follow-up sequence + breakup email

Touch 2 adds new information rather than repeating touch 1 (a relevant proof point, a different angle on the same pain) — a follow-up that just re-sends the ask reads as pressure, not persistence. The final message in the sequence is an explicit breakup email: state that this is the last outreach, remove the pressure ("no hard feelings if now isn't the time"), and leave one easy path back in. Breakup emails routinely outperform earlier touches because removing pressure lowers the reply bar.

### 1.3 VP/executive-level variant

Rewrite for a persona with less time and patience for detail: shorter than the standard first-touch (not just meeting the bar — beating it), lead with business outcome over tactical detail, drop any line that requires understanding the product before understanding why it matters. Match the tone to the persona card from `outreach-planning`, not a fixed "executive voice."

### 1.4 Refiner checklist

Before any sequence ships, verify: exactly one CTA per message, no unverifiable superlatives ("industry-leading," "revolutionary"), the trigger/personalization is specific enough that it couldn't be copy-pasted to a different prospect unchanged, sentence length varies (a wall of same-length sentences reads as templated), and the ask matches the touch number (touch 1 asks less than touch 3).

### 1.5 Performance benchmarking

Compare the sequence's structure against known outbound patterns — first-touch length, personalization depth, CTA friction, touch count — flagging deviations from what reliably performs (e.g., first touches over 150 words, sequences with no breakup email, identical CTA repeated across all touches) versus deviations that are deliberate for this specific ICP.

Run a `humanizer` pass as the final step on any drafted sequence — cold outbound is exactly the kind of copy that reads as AI-written if this step is skipped.

---

## PART 2: CHANNEL EXECUTION

Reuses `outreach-planning`'s persona/pain/offer framing, adapted to each channel's constraints. Typically complements cold email rather than replacing it.

### 2.1 LinkedIn: 2-DM max rule

LinkedIn tolerates far less volume than email before a profile gets reported or restricted. Cap direct outreach at two DMs per contact: one connection-request note (short, references the trigger, no pitch) and one follow-up DM after acceptance (the actual offer, still under LinkedIn's shorter effective attention span than email). Do not chain additional DMs after silence — that's where automation tools get accounts flagged. A LinkedIn touch is one data point inside a multi-channel sequence, not the whole campaign; let email carry the follow-up cadence.

### 2.2 Cold-call: 6-part framework

1. **Pattern interrupt** — open with something other than "how are you doing today," which triggers an automatic hang-up reflex.
2. **Permission-based opener** — ask for the specific amount of time being requested, not an open-ended "got a minute."
3. **Reason for the call, trigger-anchored** — same trigger used in written outreach, spoken concisely.
4. **One diagnostic question** — confirm the assumed pain actually applies before pitching anything.
5. **Value statement, conditional on the answer** — tailor to what was just said, not a memorized pitch.
6. **Close with a specific next step** — a concrete date/time ask, not "I'll follow up."

Script this as a framework with branches, not a word-for-word read — a call that sounds scripted loses the prospect immediately.

### 2.3 AI-personalized video outreach

Tools like Tavus or HeyGen generate personalized video at outbound scale. Use for higher-value accounts where the novelty and personalization justify the extra production step — not as a blanket replacement for email. Keep videos under 60 seconds and lead with the same trigger-based hook as the written first touch, since the opening seconds determine whether it gets watched at all. Verify Tavus/HeyGen API access via `outreach-planning`'s pre-flight check before building video sequences.

---

## PART 3: REPLIES PIPELINE

Runs continuously once a campaign is live. Classifies every reply before drafting a response — the right response depends entirely on type.

### 3.1 Eight reply types

1. **Interested / wants more info** — move fast, answer the specific question, propose a concrete next step.
2. **Wrong person, referred elsewhere** — thank them, ask for a warm intro if offered, don't just re-pitch the referral cold.
3. **Not now, timing objection** — respect it, ask for a reasonable check-back point, don't argue the timing.
4. **Price/budget objection** — this early, it's usually a qualification question in disguise; answer briefly and redirect to value, don't discount preemptively.
5. **Already using a competitor** — differentiate specifically using `competitor-profiling`'s battle-card output; don't disparage.
6. **Explicit no / not interested** — acknowledge and stop; don't push back, it only damages the sender's reputation for future campaigns.
7. **Unsubscribe / stop contacting** — action immediately and permanently; treat as non-negotiable regardless of campaign performance pressure.
8. **Out-of-office / auto-reply** — not a real reply; note the return date and let the sequence continue rather than treating it as engagement.

### 3.2 Outbound benchmarking

Compare reply rate, positive-reply rate, and booking rate against known outbound benchmarks for the channel and sequence length, adjusted for list quality (a highly-targeted small list should outperform a broad list on rate, even with fewer total replies). Flag when a number is being read as "good" or "bad" without that context — a 2% reply rate is a different result on a cold broad list versus a tightly-triggered one.

### 3.3 Pipeline analysis: stage by stage

Track the funnel explicitly — sent → opened (if trackable) → replied → positive reply → meeting booked → meeting held → closed — and diagnose the stage where the drop is sharpest rather than treating the whole pipeline as one number:

- **Good reply rate but no bookings** → the ask in the sequence is wrong (too vague, too high-friction), not the targeting or copy.
- **High open, low reply** → the message didn't land despite the subject/hook working.
- **Low open rate** → deliverability or subject line, not the message body.

---

## PART 4: AUTOMATION (n8n)

Automate a step only after it's been run manually enough times to know it's worth automating — automating a broken process just fails faster at higher volume.

### 4.1 n8n workflow builder

Structure outbound workflows around the pipeline stages defined in `outreach-planning`: a trigger (new row in the contact list, or a scheduled poll), an enrichment/dedup step, a send step per channel, a wait/branch step keyed to reply detection (feeding reply-type classification in Part 3), and an exit condition matching the campaign architecture. Build workflows as JSON exports that can be imported directly — n8n's own format is the actual deliverable, not a prose summary of it. Keep credentials and API keys out of the exported JSON; reference them via n8n's credential store.

### 4.2 n8n debugger

Common failure patterns to check first: rate-limit errors from sending too fast on a channel with volume caps (LinkedIn especially), auth/credential expiry on a connected service, malformed data reaching a node because an upstream step's output schema changed, and infinite-loop risk in reply-triggered branches without a clear exit condition. Reproduce the specific failing execution before proposing a fix — n8n's execution history shows the actual data at each node, which is more reliable than guessing from the workflow diagram alone.

### 4.3 Website scraper for enrichment

When a target isn't covered by `outreach-planning`'s standard sourcing tools (a niche site, a company's own team/about page, a job board for hiring-trigger detection), scrape directly — respecting robots.txt and rate limits, preferring a site's own structured data (JSON-LD, sitemaps) over brittle HTML parsing where available. This supplements the standard sourcing pipeline, not replaces it; scraped data typically needs more verification before trusting it as a trigger signal.

---

## Related skills in this repo

- **outreach-planning**: produces the brief this skill consumes — ICP, personas, list, campaign architecture.
- **competitor-profiling**: feeds directly into reply type 5 (already using a competitor) and sharpens campaign angles.
- **humanizer**: run as a final pass on all drafted sequences.
- **business-intelligence-report**: for a pipeline report going to leadership rather than an internal working diagnosis.
- **outreach-data-connections** (deprecated): pre-flight check is now step 5 inside `outreach-planning`.
