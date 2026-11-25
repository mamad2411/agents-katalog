---
name: gtm-machine
description: >
  Validate startup ideas with evidence and test them with real outbound — the
  full loop from raw idea to booked calls. Use this skill whenever an idea-stage
  founder wants to validate a startup or product idea, assess AI-platform
  kill-risk, check if a market is worth entering, build an ICP or personas,
  source leads from Apollo, write cold outbound copy, run an email campaign, or
  measure whether anyone actually wants what they're building. Trigger on
  phrases like "validate my idea", "is this idea any good", "should I build",
  "find my ICP", "test demand", "cold outreach", "book calls with prospects",
  "GTM test" — and also when a founder describes an idea and asks what to do
  next, even without naming validation explicitly.
---

# GTM Machine

Turn a startup idea into evidence, and evidence into booked calls. Five stages,
each with a hard gate. The north-star metric is **booked calls per idea
tested** — not reports generated, not leads sourced, not emails sent.

## Honest status of this skill

The process encoded here passed its own evals (11/11 on a golden set of ideas,
live-validated Apollo ICPs, a verified end-to-end send-and-classify loop). What
it has NOT yet done is book a call — the full outbound loop was proven
mechanically, not commercially. Treat the reply-rate bars below as starting
hypotheses, and tell the founder this when setting expectations. A validation
tool that oversells itself commits the exact sin it exists to catch.

## The one rule that outranks everything

**Never state anything about a prospect's business that you have not
verified.** A cold email that says "your chat widget does X" to a hotel with no
chat widget is dead on arrival — worse than generic, because being wrong proves
you never looked. Every claim about a recipient needs a scan record with
evidence and a timestamp, or it does not ship. This rule was learned the
expensive way; enforce it programmatically (see `scripts/s4_write/lint.py`,
the `CLAIM_FIELDS` gate), never by good intentions.

## The five stages

Work through them in order. Each stage's full rubric lives in `references/` —
read the relevant file when you reach that stage, not before.

### S1 — Validate → `references/s1-validate.md`
Score the idea on demand, AI-platform kill-risk, and GTM viability (1–5 each),
verdict pursue/park/kill. Every score cites gathered evidence by id — a score
without a trace is invalid output. Honest by construction: it must be willing
to kill the founder's favorite idea, disagree openly, and score ideas
resembling its own creator's without flattery. Output: a shareable teardown
report. Runnable module: `scripts/s1_validate/` + golden-set eval in
`scripts/eval/`.

### S2 — Hypothesize → `references/s2-hypothesize.md`
Convert a pursue verdict into 2–3 personas and 1–3 prioritized, falsifiable
outbound hypotheses, each with an ICP emitted directly as Apollo search
parameters (validated live: 100–2,000 people or the filter is wrong). If
incumbents exist — and they almost always do — at least one hypothesis must
test displacement, not greenfield. Module: `scripts/s2_hypothesize/`.

### S3 — Source → `references/s3-source.md`
Execute the ICP against Apollo: search free, enrich only post-filter survivors
(credits are the budget), score fit 1–5 with a reason, dedupe by **sending
domain** (not company name), and site-scan each lead to verify the claims the
copy will make. Leads failing the scan gate are blocked, not sent generic.
Module: `scripts/s3_source/`.

### S4 — Write → `references/s4-write.md`
2–3 first-touch variants testing different *mechanisms* (observation-led,
number-led, question-led), ≤90 words rendered, one CTA with a booking link, an
opt-out line, zero spam triggers. Lint every **rendered** (email × lead) pair —
template-level linting is insufficient because merge fields expand. Module:
`scripts/s4_write/`.

### S5 — Send & Learn → `references/s5-send.md`
3-touch sequence (day 0, +3, breakup at +10), state machine over reply classes,
intent and sentiment classified separately, last-touch attribution. **Nothing
sends without a fresh, batch-scoped human approval** — approving touch 1 grants
no authority over touch 2. The approval binds to the exact lead set and a hash
of the rendered copy; any change kills it. Modules: `scripts/s5_send/`
(gate.py is the enforcement, classify.py the reply classifier).

## Hard gates (enforced in code, not vibes)

1. **Approval per batch.** The scheduler prepares and notifies; it has no send
   path. `scripts/s5_send/gate.py` — refuses unapproved, mutated, or stale
   (>24h) batches.
2. **Verified claims only.** No `property_observation` without
   `scan_evidence`. The scanner fails closed: if it cannot render the page
   (JS execution required — chat widgets are runtime-injected), it blocks the
   lead rather than reporting a false "no widget".
3. **negative ≠ opt_out.** "No, thanks" suppresses one hypothesis; "remove me"
   suppresses globally and forever. Over-suppressing polite refusals silently
   destroys future addressable market; under-suppressing removals is a legal
   breach. Deterministic regex catches opt-outs/bounces before any LLM call.
4. **Caps belong to the mailbox, not the campaign.** ≤30 sends/day across ALL
   campaigns; one live thread per sending domain; bounce >3% per rolling 50
   auto-pauses; a kill-switch cell halts everything.
5. **Compliance by geography.** UK PECR / IE S.I. 336: corporate subscribers
   may be cold-emailed with identification + opt-out; sole traders need
   consent. Registry-check any lead below ~50 employees
   (`scripts/compliance/soletrader_check.py` — fails closed). Not legal
   advice; say so.

## System of record

Everything the machine does must be inspectable by the founder without asking.
Default: one Drive folder per idea (teardown, hypothesis pack, campaign copy)
plus sheets for ideas / hypotheses / leads / campaigns / sends / replies —
schemas in `references/operations.md`. Every verdict, score, and send carries
its evidence and timestamps. If the founder can't audit it, don't do it.

## Connections & setup → `references/setup.md`

On first use — and at every stage boundary — check what's connected and
hand-hold the founder through what's missing: Apollo (plan tier, API key,
mailbox link, signature toggle), Google Drive (and its create-only
limitation), email read vs send paths, Firecrawl for the scan gate, and the
script env keys. `references/setup.md` has the per-connector walkthroughs,
what each stage requires vs what degrades gracefully, and a first-run
verification checklist (probe everything live; never trust "connected"
status). Two principles: S1 needs nothing — never block idea validation on
outbound tooling; and state costs out loud before spending anything
(Apollo credits, API tiers).

## Where to start with a founder

1. Ask for the idea (or offer to suggest ideas in a domain they know).
   Check connections per `references/setup.md` — but start S1 regardless.
2. Run S1. Show the teardown, including the uncomfortable parts.
3. If pursue: S2 hypotheses, and push the founder to do the one thing the
   machine cannot — talk to 4–5 real buyers. Interview evidence outranks
   everything scraped.
4. S3–S5 only with their budget consent (Apollo credits) and per-batch send
   approval.
5. Record outcomes. The accumulated angle × ICP × conversion data is the
   compounding asset — instrument it from campaign one.
