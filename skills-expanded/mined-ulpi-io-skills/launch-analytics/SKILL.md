---
name: launch-analytics
version: 1.0.0
description: |
  Instrument a launch so the traffic spike is ATTRIBUTABLE, not a vanity number — one consistent UTM scheme
  on every launch link, the conversion funnel (visit → signup → activation) wired into GA4 or the project's
  existing analytics, and a validate + read-out step. Writes the UTM map + event plan to
  `.ulpi/launch/<channel>/analytics.md`, parameterized by launch source (e.g. producthunt, hackernews) so
  each link and report is correctly attributed. Shared measurement block of the launch-* family — invoked by
  the per-platform runners (`launch-product-hunt`, `launch-hacker-news`, `launch-x`, `launch-linkedin`) to
  close the loop, or run standalone. Measures durable outcomes (signups, activation), extends the real stack,
  and NEVER puts PII in links or events. Use when a launch needs UTMs on every link and signup tracking, not
  just an upvote count.
allowed-tools:
  - AskUserQuestion
  - Read
  - Write
  - Glob
  - Grep
  - Skill
argument-hint: "[launch source + site, e.g. 'Product Hunt, our Next.js app with GA4']"
arguments:
  - request
when_to_use: |
  Use when a launch needs attribution — a UTM scheme for the links plus signup/activation tracking and a way
  to read the spike. Examples: "add UTMs and tracking for my Product Hunt launch", "measure launch-day
  signups", "wire GA4 events for the launch". Also invoked by the platform runners to tag links and
  instrument conversions. Do NOT use for full product-analytics architecture or BI dashboards, and do NOT
  write channel copy or outreach (redirect to `launch-copy` / `launch-outreach`) — this is launch-scoped
  attribution only.
effort: medium
---

<EXTREMELY-IMPORTANT>
This skill instruments a launch for attribution. Non-negotiable rules:

1. NO PII IN LINKS OR EVENTS. Never put emails, names, or identifiers in UTM parameters or event params.
   Honor the project's consent/cookie/GDPR setup; if consent gating exists, don't bypass it.
2. ONE CONSISTENT SCHEME. Define the UTM convention once (lowercase, documented), and use it for every
   launch link across listing, outreach, and social — inconsistent tags fragment the report.
3. DON'T BREAK EXISTING ANALYTICS. Detect the project's current stack first; extend it, never duplicate a
   tag manager or double-fire `page_view`. If GA4 isn't present, propose adding it — don't assume it.
4. MEASURE DURABLE OUTCOMES. Track the funnel to **signup and activation**, not just visits/upvotes — the
   launch's value is the emails and activated users it produces, not the vanity spike.
5. VERIFY THE SNIPPET AGAINST CURRENT DOCS. GA4/gtag specifics change; confirm event syntax against the
   current Google docs (use a docs/`find-docs` skill) before pasting code, and adapt to the real stack.
6. NEVER FABRICATE NUMBERS. Set up the measurement; report only what the tools actually show.
7. WRITE THE KIT TO DISK at `.ulpi/launch/<channel>/analytics.md` (create the directory if needed) — a
   durable, paste-ready artifact, not advice that scrolls away.
</EXTREMELY-IMPORTANT>

# launch-analytics

## Inputs

- `$request`: the launch source and the site/stack. When invoked by a launch skill, the caller passes the
  **channel** (the hyphenated on-disk launch slug, e.g. `product-hunt` — this is the output dir), the
  **`utm_source`** GA value (e.g. `producthunt`, no hyphen), and the target links. Standalone, ask for the
  source, the site URL, and the current analytics stack (default the channel slug from the source).

## Goal

A **launch attribution kit** written to `.ulpi/launch/<channel>/analytics.md`: a consistent UTM scheme, a
per-link UTM map, the GA4 (or existing-stack) event plan for the conversion funnel, the wiring snippets,
and a validation + read-out plan.

## Step 0: Resolve source & stack

Determine the **channel** (output dir slug, e.g. `product-hunt`) and the **`utm_source`** GA value (e.g.
`producthunt`) — keep them distinct — and detect the current analytics: look for GA4/`gtag.js`, Google Tag
Manager, Plausible/Fathom/PostHog, or none. **Success criteria**: the channel, the `utm_source`, and the
real analytics stack are known.

## Step 1: Define the UTM scheme & link map

Load `references/utm-and-events.md`. Set a single convention (lowercase, hyphenated) and produce the **UTM
map** — every launch link tagged by where it appears:

- `utm_source` = the platform (e.g. `producthunt`)
- `utm_medium` = the placement (e.g. `launch`, `maker-comment`, `email`, `social`)
- `utm_campaign` = the launch (e.g. `ph-launch-2026-06`)
- `utm_content` = the specific link (e.g. `x-thread`, `wave1-email`, `gallery-cta`)

When invoked by a launch skill, hand the tagged links back to the caller (listing/outreach) so every link
is attributable; standalone, the tagged-link map in the written artifact is the deliverable for the user
to apply. **Success criteria**: one scheme, and a tagged link for every place a link appears.

## Step 2: Map the funnel & events

Define the conversion funnel and the events that mark each step — typically `page_view` (automatic) →
`sign_up` → a key **activation** event (the first real value moment). Mark `sign_up` and activation as
**conversions/key events** in GA4. **Success criteria**: each funnel step has a named event and the
key ones are flagged as conversions.

## Step 3: Wire it

Provide the tracking snippets for the real stack (GA4 `gtag('event', …)` or the equivalent), verified
against current docs, plus where to add them. Keep it minimal and consent-aware.
**Success criteria**: copy-paste wiring that fits the stack and doesn't double-fire.

## Step 4: Validate & read out

Give a validation step (GA4 **DebugView** / **Realtime** to confirm events fire with the right params) and
a simple read-out plan: where to see launch-day traffic by `utm_source`, signups by source, and the
funnel conversion. **Success criteria**: the user can confirm tracking works before launch and read the
result after.

## Step 5: Persist the kit

Write everything above to `.ulpi/launch/<channel>/analytics.md` (creating the directory if needed): the UTM
scheme + tagged-link map, the funnel/events plan, the wiring snippets, and the validate/read-out steps. The
`<channel>` is the hyphenated launch slug the caller passes (e.g. `product-hunt`), distinct from
`utm_source`. **Success criteria**: a durable, paste-ready `analytics.md` exists on disk.

## Guardrails

- No PII in UTMs or event params; honor consent/GDPR.
- One documented scheme; lowercase; reused across every link.
- Extend the existing stack; don't double-instrument or break consent gating.
- Track signups/activation, not just visits; durable outcomes over vanity.
- Verify GA4/gtag syntax against current docs; adapt to the real stack.
- Report only real numbers; never fabricate.

## When To Load References

- `references/utm-and-events.md` — the UTM convention + per-link map, the GA4 event taxonomy and
  conversion setup, the wiring snippet pattern, and validation (Steps 1–4).

## Output Contract

Write / return `.ulpi/launch/<channel>/analytics.md`:

1. the UTM scheme + a tagged-link map for every launch link
2. the funnel and its events, with `sign_up`/activation flagged as conversions
3. the wiring snippet(s) for the real stack (verified against current docs)
4. a validation step (DebugView/Realtime) and a read-out plan (traffic/signups by source)
