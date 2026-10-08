---
name: launch-linkedin
version: 1.0.0
description: |
  Prepare and run a product/company launch on LinkedIn end to end — the launch link goes in the FIRST
  COMMENT, not the post body, and you never edit the post right after publishing. Grounds in the real
  product, then writes a paste-ready package to `.ulpi/launch/linkedin/`: `POST.md` (the launch **post** — a
  strong hook in the first ~2 lines before the "…see more" cut, a skimmable body, the reach-earning format,
  hashtags, and the product link as the **first comment**), `PLAN.md` (timing, the **golden-hour** engagement
  runbook, team amplification, and the post-launch plan), and `CHECKLIST.md` (a blocking pre-flight gate). The
  LinkedIn runner of the launch-* family: it owns LinkedIn mechanics, format rules, and the gate, and
  composes the shared `launch-copy` (post copy), `launch-outreach` (team amplification, mode `linkedin`), and
  `launch-analytics` (UTM + conversion tracking), degrading to built-in fallbacks if a companion isn't
  installed. Reads the shared `.ulpi/launch/positioning.md`. Engagement asks to your network and team are
  fine (no vote-ring rules), but it avoids what LinkedIn penalizes — a link-preview card in the body,
  engagement-bait, pods, and an early edit. Use when the user wants a LinkedIn launch post written and launch
  day planned.
allowed-tools:
  - AskUserQuestion
  - Read
  - Write
  - Skill
argument-hint: "[product or LinkedIn launch goal]"
arguments:
  - request
when_to_use: |
  Use when the user wants to launch a product or company on LinkedIn, write a launch post, or plan launch-day
  engagement. Examples: "write my LinkedIn launch post", "plan my LinkedIn launch", "help me announce on
  LinkedIn". For an X / Twitter launch use `launch-x`, for Product Hunt use `launch-product-hunt`, for Hacker
  News use `launch-hacker-news`. Do NOT use for the post copy alone (redirect to `launch-copy`) or the
  cross-channel supporter messages alone (`launch-outreach`) — this runs the whole LinkedIn launch and
  composes those.
effort: high
---

<EXTREMELY-IMPORTANT>
This skill prepares and coaches a LinkedIn launch. Non-negotiable rules:

1. KEEP A LINK-PREVIEW CARD OUT OF THE POST BODY. Put the launch link in the **first comment** (and say
   "link in the comments") — the low-risk default. The reach hit is mainly on the rich preview *card*, and
   the link penalty is contested/smaller in 2026 (see `references/li-format-rules.md`); don't over-engineer
   it — a native, dwell-worthy post matters more.
2. WIN THE HOOK. Only the first ~2 lines (~140–210 chars) show before "…see more" — that hook decides who
   expands. Lead with the strongest concrete line; no "I'm excited to announce…" throat-clearing.
3. ENGAGEMENT IS ALLOWED — BAIT IS NOT. You MAY ask your network and team to engage genuinely (employee
   amplification is fine and effective); there is no vote-ring rule. But never use engagement-bait that
   LinkedIn demotes ("comment YES below", "tag 3 people"), never use engagement pods, and don't buy
   engagement. Coach genuine asks.
4. DON'T EDIT RIGHT AFTER POSTING. Editing a post in the first ~hour can suppress its reach — proof the
   post (and the first comment) BEFORE publishing.
5. GROUND EVERY WORD IN THE REAL PRODUCT. Read `.ulpi/launch/positioning.md` if present, else the README,
   the live site (via `browse`), and the repo. Never invent features or metrics.
6. WIN THE GOLDEN HOUR. Early engagement (~first 60–90 min) decides reach — be present and reply to every
   comment fast, with substance. Bake this into `PLAN.md`.
7. COMPOSE THE SHARED SKILLS, DEGRADE GRACEFULLY. Invoke `launch-copy` (LinkedIn asset profile),
   `launch-outreach` (mode `linkedin`), and `launch-analytics` (source `linkedin`). If a companion isn't
   installed, give the one-line install (`npx skills add https://github.com/ulpi-io/skills --skill <name>`)
   and fall back to the built-in reference — never hard-fail. Run the pre-flight gate
   (`references/preflight-gate.md`) before posting, and WRITE the package to disk under
   `.ulpi/launch/linkedin/`.
</EXTREMELY-IMPORTANT>

# launch-linkedin

## Inputs

- `$request`: the product to launch, or a specific LinkedIn goal (e.g. "write the post", "plan launch
  day"), plus optional links (live URL, demo, media).

## Goal

Produce a paste-ready LinkedIn launch package under `.ulpi/launch/linkedin/` (+ the shared
`.ulpi/launch/positioning.md`):

- `POST.md` — the launch **post**: the hook (first ~2 lines), the skimmable body, the format/media plan,
  hashtags, and the product link as the **first comment** (UTM-tagged).
- `PLAN.md` — when to post, the golden-hour engagement runbook, team amplification, and the post-launch plan.
- `CHECKLIST.md` — the pre-flight gate.

## Step 0: Discovery & companions

Resolve, asking only what you can't determine: the product (what it does, who for, live URL, demo/media);
whether it posts from a **personal profile** (usually higher reach) or the **company page**; the user's
network/team who'll engage. Note which companion skills are installed (`launch-copy`, `launch-outreach`,
`launch-analytics`); install-hint if missing, but proceed. **Success criteria**: product, posting identity,
and reach are known.

## Step 1: Ground the product → `.ulpi/launch/positioning.md`

Reuse `.ulpi/launch/positioning.md` if present; else build it from the README, the live site (via
`browse`), the repo, and `project-context.md`/`.ulpi/design`. Distill: one-line what-it-is, ICP, core
value, top 3 differentiators, proof points, links — nothing invented. Save it as the shared source of
truth. **Success criteria**: a brief no line will contradict.

## Step 2: Mechanics, timing & targets

Load `references/li-mechanics.md`. Decide and record (into `PLAN.md`): **when to post** (a weekday morning
window the user can attend live), realistic reach expectations, and the **format** that fits (text+image,
native document/carousel, or native video — the higher-reach formats). **Success criteria**: a concrete
post time, a chosen format, and an honest reach target.

## Step 3: Write the post → `POST.md`

Hand the **LinkedIn asset profile** (`references/li-format-rules.md` + `references/post-copy.md`) to the
**`launch-copy`** skill to draft the **hook** (first ~2 lines before "…see more") and the **post body**
(hook → story/problem → what we built → proof → CTA), in a professional-but-human voice — no hype. *Fallback:*
if `launch-copy` isn't installed, draft from those references. Then LinkedIn-owned: assemble `POST.md` with
the formatted post (line breaks for skimmability), the **format/media plan**, **3–5 niche hashtags**, the
tags (people/company page), and the **product link as the first comment** (write it with
`utm_source=linkedin` and a `<launch>` campaign placeholder — Step 6 finalizes the scheme and back-fills the
exact tagged URL). **Success criteria**: a hook that earns the expand, link in the first comment not the
body — paste-ready.

## Step 4: Plan timing & engagement → `PLAN.md`

Load `references/li-mechanics.md` and `references/timing-engagement.md`. Write into `PLAN.md`: the **post
time**, the **golden-hour runbook** (post → add the link as the first comment → reply to every comment with
substance in the first ~60–90 min → don't edit the post → keep it alive), and the post-launch plan
(repurpose, follow up). **Success criteria**: the user knows exactly when to post and how to run the first
90 minutes.

## Step 5: Cross-promotion & team amplification → `OUTREACH.md`

Invoke the **`launch-outreach`** skill with compliance mode **`linkedin`**, `positioning.md`, and the post
time — it writes `.ulpi/launch/linkedin/OUTREACH.md` with the genuine, compliant asks: notify your email
list / other channels, ask your team/employees to engage early (employee amplification, genuine — not a
pod), and a few personal shares. *Fallback:* if it isn't installed, draft these to
`.ulpi/launch/linkedin/OUTREACH.md` yourself from `references/antipatterns-compliance.md`
(engagement-allowed, bait-free). **Success criteria**: paste-ready, genuine engagement asks in
`OUTREACH.md` — zero engagement-bait or pods.

## Step 6: Wire measurement → tag links & events

Invoke the **`launch-analytics`** skill — **channel `linkedin`** (output dir) with **`utm_source`
`linkedin`** (GA value) — to UTM-tag the product link (the one in the first comment) and wire signup/
activation tracking, writing `.ulpi/launch/linkedin/analytics.md`. Then **update `POST.md`**: replace the
first-comment placeholder link with the final UTM-tagged URL so `POST.md` and `analytics.md` match.
*Fallback:* if `launch-analytics` isn't installed, write a minimal `.ulpi/launch/linkedin/analytics.md`
yourself — the UTM scheme (`utm_source=linkedin&utm_medium=launch-post&utm_campaign=<launch>`), the tagged
link, and brief signup/activation notes — so the artifact exists either way. **Success criteria**: the link
is attributable and signups are trackable — not just reactions.

## Step 7: Pre-flight gate → `CHECKLIST.md`

Run `references/preflight-gate.md` end to end and write the result into `CHECKLIST.md`: hook earns the
expand (counted ≤ the see-more cut), link is in the first comment (not the body), format chosen, hashtags
3–5, **zero** engagement-bait/pods, link UTM-tagged, post proofed (won't be edited after), post time set,
golden-hour availability blocked. Fix any failing box and re-run. **Success criteria**: every box ticked.

## Step 8: Post-launch plan → append to `PLAN.md`

Load `references/timing-engagement.md` (post-launch section): keep replying with substance through the
day, repost/repurpose into other channels, follow up with new connections, and reuse the post as social
proof. **Success criteria**: the user knows what to do after the golden hour.

## Guardrails

- Keep the external link out of the post body — link in the first comment; UTM-tag it.
- Win the hook (≤ the see-more cut); never open with "I'm excited to announce…".
- Don't edit the post right after publishing; proof it first.
- Engagement asks are fine; engagement-bait, pods, and bought engagement are not.
- Ground all copy in the real product; never invent features or metrics.
- Compose the shared skills; if one is absent, install-hint + fall back — never hard-fail.
- Write the package to disk; don't leave it as ephemeral chat.

## When To Load References

- `references/li-mechanics.md` — the algorithm, dwell time, comments-over-reactions, the link penalty,
  the golden hour, the edit penalty, realistic outcomes (Steps 2, 4).
- `references/li-format-rules.md` — char limit, the see-more hook, formats that earn reach, hashtags, the
  link-in-first-comment tactic (Step 3).
- `references/post-copy.md` — the LinkedIn asset profile passed to `launch-copy`, the hook + post skeleton,
  and the inline copy fallback (Step 3).
- `references/timing-engagement.md` — post timing, the golden-hour runbook, team amplification, and the
  post-launch section (Steps 4, 8).
- `references/antipatterns-compliance.md` — what LinkedIn penalizes, the engagement-bait/pod line, and the
  engagement-ask fallback (Steps 5, 7).
- `references/preflight-gate.md` — the blocking readiness gate (Step 7).

## Output Contract

Write under `.ulpi/launch/` and report:

1. `.ulpi/launch/positioning.md` — the shared grounded brief (created or reused)
2. `linkedin/POST.md` — the hook, the post body, the format/media plan, hashtags, the link as a UTM-tagged
   first comment
3. `linkedin/PLAN.md` — the post time, the golden-hour runbook, the post-launch plan
4. `linkedin/CHECKLIST.md` — the pre-flight gate result (every box ticked)
5. `linkedin/OUTREACH.md` — the cross-promo / team-amplification asks (from `launch-outreach`, mode `linkedin`)
6. `linkedin/analytics.md` — UTM map + signup/activation tracking (from `launch-analytics`)
7. a report of which companion skills were used vs fell back to built-ins
