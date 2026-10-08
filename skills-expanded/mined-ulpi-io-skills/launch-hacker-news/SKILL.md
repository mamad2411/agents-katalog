---
name: launch-hacker-news
version: 1.0.0
description: |
  Prepare and run a Hacker News "Show HN" launch end to end — HN is STRICTER than every other channel: it
  **forbids all vote mobilization** (no supporter waves, no asking anyone to upvote, ever). Grounds in the
  real product (real stack, honest limits), then writes a small, paste-ready package to
  `.ulpi/launch/hacker-news/`: `POST.md` (the standard `Show HN: <thing> – <plain description>` title + the
  URL + the founder's technical, no-hype first comment), `PLAN.md` (US-Eastern timing, the first-1–2-hours
  plan, a thread-engagement plan with prepared answers to hard questions, and the post-launch / second-chance
  plan), and `CHECKLIST.md` (a blocking readiness gate). The HN runner of the launch-* family: it owns Show
  HN rules, HN policy, the thread runbook, and the gate, and composes the shared `launch-copy` (title + first
  comment) and `launch-analytics` (UTM + conversion tracking), degrading to built-in fallbacks if a companion
  isn't installed. Rewards technical honesty and a present, non-defensive founder; punishes hype and
  signup-walled products. Use when the user wants to post a Show HN or plan an HN launch.
allowed-tools:
  - AskUserQuestion
  - Read
  - Write
  - Skill
argument-hint: "[product or Show HN goal]"
arguments:
  - request
when_to_use: |
  Use when the user wants to launch on Hacker News, post a "Show HN", or plan an HN launch — the title, the
  first comment, timing, and running the thread. Examples: "help me post a Show HN", "write my Show HN title
  and first comment", "plan my HN launch". For a Product Hunt launch use `launch-product-hunt`, for X use
  `launch-x`, for LinkedIn use `launch-linkedin`. Do NOT use this skill to mobilize votes — HN forbids it and
  this skill refuses; it coaches genuine, compliant posting only.
effort: high
---

<EXTREMELY-IMPORTANT>
This skill prepares and coaches a Hacker News launch. Non-negotiable rules:

1. NO VOTE MOBILIZATION — EVER. HN is stricter than Product Hunt: never orchestrate supporter waves,
   never ask anyone (friends, team, users, your audience) to upvote, never coordinate voting. HN detects
   voting rings and penalizes them hard (rank penalty, [dead]/showdead, account or domain ban). If asked, decline
   and explain. The only compliant moves: post it yourself, optionally share the link genuinely with a few
   individuals who'd actually care, and be present in the thread. Every line must pass the banned-phrase
   scan in `references/policy-compliance.md`.
2. NO HYPE, NO MARKETING-SPEAK, NO EMOJI. HN's audience is skeptical engineers who punish spin. The voice
   is technical, humble, plain, and honest about tradeoffs and limitations. The `Show HN` title follows a strict, standard form:
   `Show HN: <thing> – <plain, literal description>` — no clickbait, no "revolutionary".
3. READY-TO-SHIP IS A GATE. HN is one-shot and unforgiving: the product must be **finished enough to try
   now**, work **without a signup wall** (a demo/repo accessible without an account), and the site must
   survive a traffic spike ("the HN hug of death"). If it isn't ready, say so before posting.
4. GROUND EVERY WORD IN THE REAL PRODUCT. Read `.ulpi/launch/positioning.md` if present, else the README,
   the live site (via `browse`), and the repo. Never invent features or metrics. For HN, name the real
   stack and the real limitations.
5. COMPOSE THE SHARED SKILLS, DEGRADE GRACEFULLY. Invoke `launch-copy` (HN asset profile) and
   `launch-analytics` (source `hackernews`). If a companion isn't installed, give the one-line install
   (`npx skills add https://github.com/ulpi-io/skills --skill <name>`) and fall back to the built-in
   reference — never hard-fail.
6. RUN THE PRE-FLIGHT GATE before declaring ready (`references/preflight-gate.md`). If one box can't be
   honestly ticked, it isn't ready — fix and re-run.
7. WRITE THE PACKAGE TO DISK under `.ulpi/launch/hacker-news/` (+ the shared `.ulpi/launch/positioning.md`).
</EXTREMELY-IMPORTANT>

# launch-hacker-news

## Inputs

- `$request`: the product to post, or a specific Show HN goal (e.g. "write my title and first comment",
  "plan the thread"), plus optional links (live URL, repo/demo).

## Goal

Produce a small, HN-appropriate, paste-ready launch package under `.ulpi/launch/hacker-news/` (+ the
shared `.ulpi/launch/positioning.md`):

- `POST.md` — the `Show HN` title (standard format), the URL to submit, and the founder's explanatory first
  comment (technical, honest about tradeoffs, names the stack, asks for feedback — no hype, no upvote ask).
- `PLAN.md` — when to post (US-Eastern weekday morning), the first-1–2-hours plan, a thread-engagement plan
  (prepared, non-defensive answers to the hardest likely questions), and the post-launch/second-chance plan.
- `CHECKLIST.md` — the readiness pre-flight gate.

## Step 0: Discovery & companions

Resolve, asking only what you can't determine: the product (what it does, who for, live URL, repo/demo);
whether it's genuinely **ready** (finished, tryable without signup, can take a traffic spike); whether the
user wants a URL post or a text post. Note which companion skills are installed (`launch-copy`,
`launch-analytics`); install-hint if missing, but proceed. **Success criteria**: product, readiness, and
post type are known.

## Step 1: Ground the product → `.ulpi/launch/positioning.md`

Reuse `.ulpi/launch/positioning.md` if present; else build it from the README, the live site (via
`browse`), the repo, and `project-context.md`/`.ulpi/design`. For HN, additionally capture the **real
stack** and the **honest limitations**. Save it as the shared source of truth. **Success criteria**: a
brief no line will contradict — including the tradeoffs.

## Step 2: Readiness check (HN-specific early gate)

Load `references/show-hn-rules.md`. Verify the product **qualifies** for Show HN (something people can try
now — not a waitlist, landing page, or blog post) and is ready: tryable **without a signup wall**, a
demo/repo reachable without an account, and the site can survive a spike. If it doesn't qualify or isn't
ready, **say so plainly** and advise what to fix before posting. **Success criteria**: an honest go/no-go
on whether this should be a Show HN at all yet.

## Step 3: Write the post → `POST.md`

Hand the **HN asset profile** (`references/show-hn-rules.md` + `references/first-comment.md`) to the
**`launch-copy`** skill to draft the **`Show HN: <thing> – <plain description>` title** (standard format, no
hype) and the **founder's first comment** (what it is → why you built it → honest tradeoffs/limits → the
stack → an explicit ask for feedback). *Fallback:* if `launch-copy` isn't installed, draft from those
references. Before assembling `POST.md`, load `references/policy-compliance.md` and run its banned-phrase
scan over the drafted title and first comment; rewrite any line that trips it. Assemble `POST.md` with the
title, the submit URL (or the text-post body), and the first comment to paste **immediately** after posting.
**Success criteria**: a compliant title and an honest, technical, hype-free first comment — paste-ready,
scan-clean.

## Step 4: Timing & thread runbook → `PLAN.md`

Load `references/hn-mechanics.md` and `references/first-comment.md`. Write into `PLAN.md`: **when to post**
(US-Eastern weekday morning for the longest front-page daylight; the first 1–2 hours on `/newest` decide
whether it reaches the front page), post the first comment immediately, then **be present and reply fast**.
Add a **thread-engagement plan**: list the hardest likely questions/criticisms and a prepared, **honest,
non-defensive** response to each (converting a skeptic in public is the win). **Success criteria**: the
user knows exactly when to post and how to run the thread without improvising or getting defensive.

## Step 5: Wire measurement → tag links & events

Invoke the **`launch-analytics`** skill — **channel `hacker-news`** (output dir) with **`utm_source`
`hackernews`** (GA value) — to set UTMs on the links and wire signup/activation tracking. *Fallback:* a
minimal inline UTM scheme (`utm_source=hackernews&utm_medium=show-hn&utm_campaign=<launch>`). Note: HN
strips/penalizes obviously campaign-tagged primary URLs in some cases — keep the submitted URL clean and
put UTMs on links inside the first comment / your site's own analytics. **Success criteria**: traffic and
signups are attributable without gaming the submitted link.

## Step 6: Pre-flight gate → `CHECKLIST.md`

Load `references/preflight-gate.md` and `references/policy-compliance.md`, run the gate end to end
(including the banned-phrase scan) and write the result into `CHECKLIST.md`: title format correct, product
qualifies + is tryable without signup, site can take the spike, first comment ready and hype-free, **zero**
vote-soliciting/mobilization anywhere, honest about limitations. Fix any failing box and re-run. **Success
criteria**: every box ticked; the launch is genuinely ready and compliant.

## Step 7: Post-launch plan → append to `PLAN.md`

Load `references/postlaunch.md`. Append: the **second-chance pool** (HN may re-surface a good post — you
can't game it), the **repost etiquette** (do not spam-repost; HN's rules), converting the skeptical traffic
(no signup wall; genuine value), and the failure-mode reminders. **Success criteria**: the user knows what
to do whether it hits the front page or stalls.

## Guardrails

- Never mobilize votes or ask for upvotes — HN forbids it and detects rings; decline and redirect.
- No hype, no marketing-speak, no emoji; be honest about tradeoffs and limitations.
- The product must be ready (tryable without signup, survives a spike) before posting.
- Keep the standard `Show HN: <thing> – <plain description>` title format.
- Ground all copy in the real product, including the real stack and limits.
- Compose the shared skills; if one is absent, install-hint + fall back — never hard-fail.
- Keep the submitted URL clean; don't tag the primary link in a way HN penalizes.
- Write the package to disk; don't leave it as ephemeral chat.

## When To Load References

- `references/show-hn-rules.md` — what qualifies as a Show HN, the standard title format, URL vs text post,
  the first-comment rule, and Launch HN (Steps 2, 3).
- `references/hn-mechanics.md` — ranking, `/newest`, the second-chance pool, and posting timing (Step 4).
- `references/first-comment.md` — the founder first-comment skeleton + the thread-engagement / responding-
  to-criticism craft (Steps 3, 4).
- `references/policy-compliance.md` — HN's anti-manipulation rules, the banned-phrase scan, and penalties
  (Steps 3, 6).
- `references/preflight-gate.md` — the blocking readiness + compliance gate (Step 6).
- `references/postlaunch.md` — the second-chance pool, repost etiquette, converting traffic, failure modes
  (Step 7).

## Output Contract

Write under `.ulpi/launch/` and report:

1. `.ulpi/launch/positioning.md` — the shared grounded brief (created or reused; includes the real stack + limits)
2. `hacker-news/POST.md` — the `Show HN` title, the submit URL/text body, and the founder's first comment
3. `hacker-news/PLAN.md` — posting time (ET), the first-hours plan, the thread-engagement plan, post-launch
4. `hacker-news/CHECKLIST.md` — the readiness gate result (every box ticked)
5. `hacker-news/analytics.md` — UTM map + signup/activation tracking (from `launch-analytics`)
6. a readiness verdict (qualifies / ready or not) and the compliance affirmation (zero vote-mobilization),
   plus which companion skills were used vs fell back to built-ins
