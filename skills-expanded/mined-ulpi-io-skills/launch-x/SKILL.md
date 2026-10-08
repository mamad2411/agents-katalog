---
name: launch-x
version: 1.0.0
description: |
  Prepare and run a product launch on X (formerly Twitter) end to end — the external link goes in a REPLY,
  not the main tweet, so reach isn't penalized. Grounds in the real product, then writes a paste-ready
  package to `.ulpi/launch/x/`: `POST.md` (the launch **thread** — a scroll-stopping hook tweet, the thread
  body, native media, and the product link in a reply), `PLAN.md` (timing, the **golden-hour** engagement
  runbook, cross-promotion, and the post-launch plan), and `CHECKLIST.md` (a blocking pre-flight gate). The X
  runner of the launch-* family: it owns X mechanics, format rules, and the gate, and composes the shared
  `launch-copy` (thread copy), `launch-outreach` (team amplification, mode `x`), and `launch-analytics` (UTM
  + conversion tracking), degrading to built-in fallbacks if a companion isn't installed. Reads the shared
  `.ulpi/launch/positioning.md`. Engagement asks to your own audience are fine (no vote-ring rules), but it
  avoids what X penalizes — a link in the main tweet, engagement-bait, and bought engagement. Use when the
  user wants an X launch thread written and launch day planned.
allowed-tools:
  - AskUserQuestion
  - Read
  - Write
  - Skill
argument-hint: "[product or X launch goal]"
arguments:
  - request
when_to_use: |
  Use when the user wants to launch a product on X / Twitter, write a launch thread, or plan launch-day
  engagement. Examples: "write my X launch thread", "plan my Twitter launch", "help me launch on X". For a
  LinkedIn launch use `launch-linkedin`, for Product Hunt use `launch-product-hunt`, for Hacker News use
  `launch-hacker-news`. Do NOT use for the on-listing copy alone (redirect to `launch-copy`) or the
  cross-channel supporter messages alone (`launch-outreach`) — this runs the whole X launch and composes those.
effort: high
---

<EXTREMELY-IMPORTANT>
This skill prepares and coaches an X (Twitter) launch. Non-negotiable rules:

1. KEEP THE EXTERNAL LINK OUT OF THE MAIN TWEET. X down-ranks posts that contain an outbound link, so the
   product link goes in a **reply** to the thread (or the user's pinned reply), never in the hook tweet.
2. THE HOOK IS EVERYTHING. The first tweet must stop the scroll on its own (it's what shows in the feed).
   No "a thread 🧵👇" with no substance; lead with the strongest concrete line.
3. ENGAGEMENT IS ALLOWED — BAIT IS NOT. On X you MAY ask your own audience and team to check it out and
   repost; there is no vote-ring rule. But never use engagement-bait ("like & RT to win", follow-for-
   follow, "reply DONE"), never buy engagement/followers, and never mass-DM strangers. Coach genuine asks.
4. GROUND EVERY WORD IN THE REAL PRODUCT. Read `.ulpi/launch/positioning.md` if present, else the README,
   the live site (via `browse`), and the repo. Never invent features or metrics.
5. WIN THE GOLDEN HOUR. Early reply/repost velocity drives distribution — be present and reply to every
   reply fast in the first ~30–60 minutes. Bake this into `PLAN.md`.
6. COMPOSE THE SHARED SKILLS, DEGRADE GRACEFULLY. Invoke `launch-copy` (X asset profile), `launch-outreach`
   (mode `x`), and `launch-analytics` (source `x`). If a companion isn't installed, give the one-line
   install (`npx skills add https://github.com/ulpi-io/skills --skill <name>`) and fall back to the
   built-in reference — never hard-fail.
7. RUN THE PRE-FLIGHT GATE before posting (`references/preflight-gate.md`); fix any unticked box.
8. WRITE THE PACKAGE TO DISK under `.ulpi/launch/x/` (+ the shared `.ulpi/launch/positioning.md`).
</EXTREMELY-IMPORTANT>

# launch-x

## Inputs

- `$request`: the product to launch, or a specific X goal (e.g. "write the thread", "plan launch day"),
  plus optional links (live URL, demo, media).

## Goal

Produce a paste-ready X launch package under `.ulpi/launch/x/` (+ the shared `.ulpi/launch/positioning.md`):

- `POST.md` — the launch **thread**: the hook tweet, the thread body, the native media plan, and the
  product link as a **reply** (plus the pin instruction).
- `PLAN.md` — when to post, the golden-hour engagement runbook, cross-promotion, and the post-launch plan.
- `CHECKLIST.md` — the pre-flight gate.

## Step 0: Discovery & companions

Resolve, asking only what you can't determine: the product (what it does, who for, live URL, demo/media);
whether it's a **thread** or a single post (a launch is usually a thread); the user's reach (followers,
team who'll engage). Note which companion skills are installed (`launch-copy`, `launch-outreach`,
`launch-analytics`); install-hint if missing, but proceed. **Success criteria**: product, format, and reach
are known.

## Step 1: Ground the product → `.ulpi/launch/positioning.md`

Reuse `.ulpi/launch/positioning.md` if present; else build it from the README, the live site (via
`browse`), the repo, and `project-context.md`/`.ulpi/design`. Distill: one-line what-it-is, ICP, core
value, top 3 differentiators, proof points, links — nothing invented. Save it as the shared source of
truth. **Success criteria**: a brief no line will contradict.

## Step 2: Mechanics, timing & targets

Load `references/x-mechanics.md`. Decide and record (into `PLAN.md`): **when to post** (a US weekday
window the user can attend live), realistic reach expectations, and the format (thread vs single). **Success
criteria**: a concrete post time and an honest reach target — no hype.

## Step 3: Write the thread → `POST.md`

Hand the **X asset profile** (`references/x-format-rules.md` + `references/thread-copy.md`) to the
**`launch-copy`** skill to draft the **hook tweet** and the **thread body** (hook → problem → what it is →
demo media → what's different → [proof] → CTA), in the user's authentic voice. *Fallback:* if `launch-copy`
isn't installed, draft from those references. Then X-owned: assemble `POST.md` with the numbered thread, the
**native media plan** (per tweet), the **product link as a reply** (write it with `utm_source=x` and a
`<launch>` campaign placeholder — Step 6 finalizes the scheme and back-fills the exact tagged URL), and the
**pin** note.
**Success criteria**: a scroll-stopping hook, a tight thread, the link in a reply not the hook —
paste-ready.

## Step 4: Plan timing & engagement → `PLAN.md`

Load `references/x-mechanics.md` and `references/timing-engagement.md`. Write into `PLAN.md`: the **post
time**, the **golden-hour runbook** (post → pin → reply to every reply fast in the first ~30–60 min →
quote-post milestones → keep the thread alive), and the post-launch plan (pin the thread, repurpose,
follow up). **Success criteria**: the user knows exactly when to post and how to run the first hours.

## Step 5: Cross-promotion & team amplification → `OUTREACH.md`

Invoke the **`launch-outreach`** skill with compliance mode **`x`**, `positioning.md`, and the post time —
it writes `.ulpi/launch/x/OUTREACH.md` with the genuine, compliant asks: notify your email list / other
channels to come see the thread, ask your team to engage in the golden hour, and a few personal 1:1 shares.
*Fallback:* if it isn't installed, draft these to `.ulpi/launch/x/OUTREACH.md` yourself from
`references/antipatterns-compliance.md` (engagement-allowed, bait-free). **Success criteria**: paste-ready,
genuine engagement asks in `OUTREACH.md` — zero engagement-bait.

## Step 6: Wire measurement → tag links & events

Invoke the **`launch-analytics`** skill — **channel `x`** (output dir) with **`utm_source` `x`** (the GA
value; use `twitter` only if your existing GA reports already standardize on it, then use it for every
launch link) — to UTM-tag the product link (the one in the reply) and wire signup/activation tracking,
writing `.ulpi/launch/x/analytics.md`. Then **update `POST.md`**: replace the reply's placeholder link with
the final UTM-tagged URL so `POST.md` and `analytics.md` match. *Fallback:* if `launch-analytics` isn't
installed, write a minimal `.ulpi/launch/x/analytics.md` yourself — the UTM scheme
(`utm_source=x&utm_medium=launch-thread&utm_campaign=<launch>`), the tagged reply link, and brief signup/
activation notes — so the artifact exists either way. **Success criteria**: the link is attributable and
signups are trackable — not just likes.

## Step 7: Pre-flight gate → `CHECKLIST.md`

Run `references/preflight-gate.md` end to end and write the result into `CHECKLIST.md`: hook stops the
scroll, link is in a reply (not the hook), media attached, thread tight, **zero** engagement-bait, link
UTM-tagged, post time set, golden-hour availability blocked. Fix any failing box and re-run. **Success
criteria**: every box ticked; the launch is ready.

## Step 8: Post-launch plan → append to `PLAN.md`

Load `references/timing-engagement.md` (post-launch section): pin the thread to the profile, keep replying
through the day, quote-post a "what we learned / milestone" update, repurpose the thread into other
channels, and follow up with new followers. **Success criteria**: the user knows what to do after the
golden hour.

## Guardrails

- Keep the external link out of the main tweet — link in a reply; UTM-tag it.
- Lead with the hook; never post a contentless "thread 🧵" opener.
- Engagement asks are fine; engagement-bait, bought engagement, and mass-DM are not.
- Ground all copy in the real product; never invent features or metrics.
- Compose the shared skills; if one is absent, install-hint + fall back — never hard-fail.
- Write the package to disk; don't leave it as ephemeral chat.

## When To Load References

- `references/x-mechanics.md` — the For You algorithm, reach signals, the link penalty, the golden hour,
  Premium/reach, realistic outcomes (Steps 2, 4).
- `references/x-format-rules.md` — char limits, thread structure, native media, the link-in-reply tactic,
  hashtags, pinning (Step 3).
- `references/thread-copy.md` — the X asset profile passed to `launch-copy`, the hook + thread skeleton,
  and the inline copy fallback (Step 3).
- `references/timing-engagement.md` — post timing, the golden-hour runbook, and the post-launch section
  (Steps 4, 8).
- `references/antipatterns-compliance.md` — what X penalizes, the engagement-bait line, and the
  engagement-ask fallback (Steps 5, 7).
- `references/preflight-gate.md` — the blocking readiness gate (Step 7).

## Output Contract

Write under `.ulpi/launch/` and report:

1. `.ulpi/launch/positioning.md` — the shared grounded brief (created or reused)
2. `x/POST.md` — the hook tweet, the thread body, the media plan, the link as a UTM-tagged reply, the pin note
3. `x/PLAN.md` — the post time, the golden-hour runbook, the post-launch plan
4. `x/CHECKLIST.md` — the pre-flight gate result (every box ticked)
5. `x/OUTREACH.md` — the cross-promo / team-amplification asks (from `launch-outreach`, mode `x`)
6. `x/analytics.md` — UTM map + signup/activation tracking (from `launch-analytics`)
7. a report of which companion skills were used vs fell back to built-ins
