---
name: launch-outreach
version: 1.0.0
description: |
  Build and notify a launch's supporter audience with paste-ready, platform-COMPLIANT outreach — the
  messages you send to PEOPLE, never the on-listing copy. Recruits an audience before launch, segments it
  (team · friends · users/waitlist · communities · public followers), and notifies it in timed waves on the
  day. Drafts the teaser DMs, waitlist and launch-day emails, community heads-ups, 1:1 DMs, and X/LinkedIn
  amplification posts, and writes them to `.ulpi/launch/<channel>/OUTREACH.md`. Parameterized by a
  per-platform COMPLIANCE MODE the caller passes (Product Hunt: supporter waves allowed, ask for feedback not
  upvotes; Hacker News: NO vote mobilization at all); grounds every message in `.ulpi/launch/positioning.md`
  and NEVER solicits/incentivizes votes or mass-spams. Shared audience block of the launch-* family, invoked
  by the per-platform runners (`launch-product-hunt`, `launch-hacker-news`, `launch-x`, `launch-linkedin`) or
  run standalone. Use when a launch needs who-to-tell and what-to-say, compliant to each platform's rules.
allowed-tools:
  - AskUserQuestion
  - Read
  - Write
argument-hint: "[platform + audience to reach, e.g. 'Product Hunt launch, ~200 email + X']"
arguments:
  - request
when_to_use: |
  Use when planning who to tell about a launch and what to say — recruiting a pre-launch audience, segmenting
  supporters, and drafting compliant DMs/emails/community posts/social broadcasts. Examples: "who do I notify
  for my launch and what do I say", "draft my launch-day emails", "write the supporter outreach without
  breaking the rules". Also invoked by the platform runners, which pass a compliance mode. Do NOT use to
  write the listing copy — tagline, description, first comment (redirect to `launch-copy`) — and do NOT use
  to manipulate votes; this skill refuses that.
effort: high
---

<EXTREMELY-IMPORTANT>
This skill drafts outreach for a launch. Non-negotiable rules:

1. THE COMPLIANCE MODE IS LAW. The caller passes a per-platform mode (`references/compliance-modes.md`);
   it overrides every default. If the mode forbids vote mobilization (e.g. Hacker News), do NOT produce
   supporter-wave plans or "we're live, come engage" broadcasts — coach presence-in-thread only. Never
   produce copy that violates the platform's rules.
2. NEVER SOLICIT OR INCENTIVIZE VOTES. No "please upvote", "support us", "give us a vote", "help us hit
   #1", and never tie any discount/perk to a vote. Ask people to **visit, try, and give honest feedback**.
   Every message passes the banned-phrase scan in `references/compliance-modes.md` before it ships.
3. PERSONALIZE; DON'T SPAM. 1:1 DMs go only to people the user actually knows, personalized each time.
   Identical copy-pasted blasts to strangers and scraped cold emails are prohibited "mass messaging".
   Opt-in waitlist/customer email framed for feedback is fine; cold mass-DM is not.
4. GROUND IT IN THE REAL PRODUCT. Read `.ulpi/launch/positioning.md` if present; if it's missing (e.g. run
   standalone before a platform skill produced it), gather the product summary from the caller or via one
   or two focused questions. Never invent features or proof.
5. BE HONEST ABOUT REACH. If the user has little or no audience, say so plainly and coach building one —
   don't imply outreach can manufacture a result it can't.
6. STAGGER, DON'T BLAST (when the mode allows waves). Notify in waves across the day to sustain genuine
   velocity; a single mass spike both underperforms and looks like manipulation.
</EXTREMELY-IMPORTANT>

# launch-outreach

## Inputs

- `$request`: the platform/launch and the audience/channels available. When invoked by a launch skill,
  the caller passes the **compliance mode**, the product (`positioning.md`), and the launch date/time.
  Standalone, gather these with one or two focused questions.

## Goal

Produce a **segmented outreach plan + paste-ready, compliant messages** for the launch, written to
`.ulpi/launch/<channel>/OUTREACH.md` (the `<channel>` is the hyphenated launch slug the caller passes, e.g.
`product-hunt`; or handed back to the caller). Covers recruiting the audience
before launch and notifying it on the day, in the platform's compliance mode.

## Step 0: Resolve context & compliance mode

Adopt the caller's compliance mode, or pick it from `references/compliance-modes.md` by platform. Confirm
the product, the launch date/time (timezone), and what audience/channels exist. **Success criteria**: the
mode, product, date, and available reach are known.

## Step 1: Recruit / assess the audience (pre-launch)

Load `references/outreach-playbook.md`. If there's runway before launch, coach building a warm list
**off-platform** (a simple email-capture landing page + building-in-public on X/LinkedIn) — many platforms
no longer offer a native pre-launch notify list. Inventory what the user already has (list size, social
following, communities they're a real member of, existing users). **Be realistic** about what that reach
can produce. **Success criteria**: an honest picture of available reach and a plan to grow it if there's time.

## Step 2: Segment & plan reach

Segment the audience and decide how each is reached (load `references/outreach-playbook.md`):

1. **Team / co-founders** — briefed, on-call.
2. **Friends & peers** — personal, low-pressure heads-up.
3. **Existing users / customers / waitlist** — highest intent; a genuine "we're live, tell us what to fix".
4. **Communities** you're a real member of — a single organic heads-up where allowed, never a vote drive.
5. **Public audience** (X/LinkedIn followers) — launch-day posts.

**DM the top ~20–50 supporters personally** (personalized each time); reach the rest via segmented email
and broadcast posts. **Success criteria**: each segment has a channel, a message type, and a send time.

## Step 3: Draft the message set (grounded + compliant)

Load `references/templates.md`. Draft, personalized to the product from `positioning.md`, in the
compliance mode: the pre-launch teaser DM, the waitlist "we launch soon, I'd love your honest feedback"
email, the launch-day email wave(s), the community heads-up, the personal 1:1 DM, and the social
amplification posts (X thread, LinkedIn). Every message asks for a **visit / try / feedback**, never a
vote. **Success criteria**: every message is paste-ready, personalized, and on-mode.

## Step 4: Wave plan (only if the mode allows mobilization)

If the compliance mode allows supporter waves (e.g. Product Hunt), lay out a **staggered send schedule**
across the launch day (closest circle first, then list waves by engagement/timezone, holding a reserve for
the midday lull and final hours) so velocity is sustained, not spiked. If the mode forbids mobilization
(e.g. Hacker News), **skip this** and coach genuine in-thread presence instead. **Success criteria**: a
wave schedule that fits the mode — or a clear note that waves don't apply here.

## Step 5: Compliance scan

Run the banned-phrase scan (`references/compliance-modes.md`) over every message. Any hit → rewrite.
**Success criteria**: zero vote-soliciting/incentivizing/mass-spam language anywhere.

## Guardrails

- The compliance mode overrides all defaults; when unsure, ask the caller.
- Never solicit or incentivize votes; never tie a perk to a vote.
- Personalize 1:1 outreach; no identical blasts to strangers, no scraped cold email.
- Ground messages in the real product; reuse `.ulpi/launch/positioning.md`.
- Be honest about reach; don't imply outreach can fake momentum.
- Respect each community's self-promo rules; share only where the user genuinely participates.
- This skill writes person-to-person and broadcast outreach — not the listing/first-comment copy (that's
  `launch-copy`).

## When To Load References

- `references/outreach-playbook.md` — recruiting an audience, the five segments, reach plan, and the
  wave strategy with timing (Steps 1, 2, 4).
- `references/templates.md` — the paste-ready, compliant message library: teaser DM, waitlist email,
  launch-day email waves, community heads-up, 1:1 DM, X thread, LinkedIn post (Step 3).
- `references/compliance-modes.md` — per-platform compliance dials and the banned-phrase scan
  (Steps 0, 5).

## Output Contract

Write / return:

1. an `OUTREACH.md` with the segmented plan and the paste-ready, compliant messages per segment
2. (if the mode allows) a staggered launch-day wave schedule; otherwise a note that waves don't apply
3. the compliance affirmation: zero vote-soliciting/incentivizing/mass-spam language, scan passed
