---
name: launch-product-hunt
version: 1.0.0
description: |
  Prepare and run a Product Hunt launch end to end — COMPLIANT promotion ONLY: never vote manipulation,
  rings, bought/incentivized votes, or "please upvote". Grounds every word in the real product, then writes a
  complete, paste-ready package to `.ulpi/launch/product-hunt/`: `LISTING.md` (every PH field — tagline
  options ≤ the current limit, description, topics, a gallery shot-list, demo-video outline, the maker's
  first comment), `PLAN.md` (a T-minus countdown + an hour-by-hour Pacific-time launch-day runbook + the
  post-launch plan), `OUTREACH.md` (segmented supporter outreach + social posts), and `CHECKLIST.md` (a
  blocking pre-flight gate). The PH orchestrator of the launch-* family: it owns field specs, policy, and the
  day-of runbook, and composes the shared `launch-copy` (listing), `launch-outreach` (mode `product-hunt`),
  and `launch-analytics` (UTM + conversion tracking), degrading to built-in fallbacks if a companion isn't
  installed. Reads the shared `.ulpi/launch/positioning.md`. Treats Product Hunt as a credibility amplifier,
  not primary acquisition, and sets realistic expectations. Use when the user wants a full Product Hunt
  launch prepared and run.
allowed-tools:
  - AskUserQuestion
  - Read
  - Write
  - Skill
argument-hint: "[product, launch date, or PH launch goal]"
arguments:
  - request
when_to_use: |
  Use when the user wants to launch on Product Hunt, prepare a PH submission, or plan launch day — tagline,
  first comment, gallery, timing, supporter outreach, Product of the Day. Examples: "help me launch on
  Product Hunt", "write my PH tagline and first comment", "plan my Product Hunt launch day". For a Hacker
  News launch use `launch-hacker-news`, for X use `launch-x`, for LinkedIn use `launch-linkedin`. Do NOT use
  this skill to manipulate votes — it refuses that and coaches compliant promotion only.
effort: high
---

<EXTREMELY-IMPORTANT>
This skill prepares and coaches a Product Hunt launch. Non-negotiable rules:

1. COMPLIANT PROMOTION ONLY. Never help with vote manipulation in any form: vote rings/pods,
   upvote-exchange sites, bought or incentivized votes, fake/sock/clustered accounts, asking people to
   click an upvote link, or "please upvote us" solicitation. Paying anyone to hunt or send traffic is also
   prohibited and risks removal/permanent ban. If asked for any of these, decline that part, explain the
   risk, and redirect to compliant tactics. Every message must pass the banned-phrase scan in
   `references/policy-compliance.md`.
2. GROUND EVERY WORD IN THE REAL PRODUCT. Read the product before writing one tagline — `.ulpi/launch/
   positioning.md` if present, else the README, the live landing page (via `browse`), `.ulpi/design/`, and
   a `.claude`/`.cursor` `project-context.md`. No generic placeholder copy. If you can't tell what the
   product does and who it's for, ask.
3. COMPOSE THE SHARED SKILLS, DEGRADE GRACEFULLY. At the delegated steps, invoke `launch-copy`,
   `launch-outreach` (mode `product-hunt`), and `launch-analytics` (source `producthunt`). If a
   companion isn't installed, tell the user the one-line install (`npx skills add
   https://github.com/ulpi-io/skills --skill <name>`) and **fall back to the built-in reference** so the
   launch still completes — never hard-fail.
4. HONOR EXACT, CURRENT FIELD SPECS. Limits and dimensions change — treat `references/field-specs.md` as
   authoritative; when a number is critical and might be stale, verify against the live PH submission flow
   via `browse`.
5. RUN THE PRE-FLIGHT GATE before declaring the package done (`references/preflight-gate.md`). Several
   checks are mechanical counts. If one box can't be honestly ticked, the launch isn't ready — fix and re-run.
6. SET REALISTIC EXPECTATIONS. PH is a credibility/visibility amplifier, not primarily customer
   acquisition, and most submissions are never featured. Never promise virality, a rank, or Product of the Day.
7. WRITE THE PACKAGE TO DISK under `.ulpi/launch/product-hunt/` (and the shared brief to
   `.ulpi/launch/positioning.md`). Produce durable, paste-ready artifacts — not advice that scrolls away.
</EXTREMELY-IMPORTANT>

# launch-product-hunt

## Inputs

- `$request`: the product to launch, a launch date/stage, or a specific PH goal (e.g. "write my tagline
  and first comment", "plan launch day"), plus optional links.

## Goal

Produce a **complete, compliant, paste-ready Product Hunt launch package**, grounded in the real product,
under `.ulpi/launch/product-hunt/` (+ the shared `.ulpi/launch/positioning.md`):

- `LISTING.md` — every PH field, filled and paste-ready (name, tagline options with one chosen, description,
  topics, gallery shot-list, demo-video outline, the maker's first comment, UTM-tagged links).
- `PLAN.md` — the T-minus countdown, the hour-by-hour Pacific-time launch-day runbook, the hunter/date
  decision, and the post-launch plan.
- `OUTREACH.md` — supporter segments and paste-ready, PH-compliant messages + social posts.
- `CHECKLIST.md` — the pre-flight gate result and the launch-day checklist.

## Step 0: Discovery & companions

Resolve, asking only what you can't determine: the product (name, what it does, who for, live URL);
stage & date (imminent or weeks out; date chosen?); audience/reach; team; hunter (self-hunt default).
Note which companion skills are installed (`launch-copy`, `launch-outreach`, `launch-analytics`); if
any are missing, mention the install command but proceed either way (fallbacks exist). Ask at most a
couple of focused questions. **Success criteria**: product, stage/date, and reach are known.

## Step 1: Ground the product → `.ulpi/launch/positioning.md`

Reuse `.ulpi/launch/positioning.md` if it exists. Otherwise build it from `.ulpi/design/DESIGN.md`, a
`.claude`/`.cursor` `project-context.md` (Sections 1–9), the README/docs, and the **live landing page**
(visit it with the `browse` skill — extract the real value prop, features, screenshots, proof points). If
`browse` or a site is missing, ask the user for the key points. Distill: one-line what-it-is, ICP, core
value in the user's words, **top 3 differentiators**, proof points, category, links — nothing invented.
Save it as the shared source of truth. **Success criteria**: a brief no asset will contradict.

## Step 2: Mechanics, timing & realistic targets

Load `references/ph-mechanics.md`. Decide and record (into `PLAN.md`): the **date/day** (Tue–Thu default,
12:01am **PT**; weekend only as a deliberate low-competition play), the **hunter** decision (self-hunt by
default; never paid), and an **honest outcome range** (featuring/Product of the Day not guaranteed).
**Success criteria**: a concrete date, a hunter decision, and a realistic target — no hype.

## Step 3: Write the listing → `LISTING.md`

Hand the **PH asset profile** (`references/copywriting.md`) and the exact limits (`references/field-specs.md`)
to the **`launch-copy`** skill to draft the tagline options (≤60, one recommended), description (≤500),
gallery slide headlines, and the maker first comment — all bound to `positioning.md`, in PH voice, with
zero upvote asks. *Fallback:* if `launch-copy` isn't installed, draft them directly from
`references/copywriting.md`. Then PH-owned: assemble `LISTING.md`, add the **gallery shot-list** (image 1 =
the scroll-stopping poster + caption, then 3–5 value slides — **4–6 total** at 1270×760), the demo-video
outline, topics
(≤3), makers, any offer (tied to *trying*, never voting), and the links. **Success criteria**: every field
filled, on-brand, within spec (characters/dimensions counted), paste-ready — nothing says "[insert tagline]".

## Step 4: Plan the ramp & launch day → `PLAN.md`

Load `references/prelaunch-playbook.md` and `references/launchday-runbook.md`. Write the **T-minus
countdown** (scaled to the real timeline — build the off-platform supporter list since PH's native teaser
pages are gone, warm the audience, finalize assets, schedule the launch) and the **hour-by-hour launch-day
runbook** (Pacific): 12:01am publish + first comment → notify in **waves** → reply to every comment fast →
midday push → final-hours push → day-wrap thanks. Assign team roles if there's a team. **Success
criteria**: a teammate could run the day from `PLAN.md` without improvising.

## Step 5: Outreach & amplification → `OUTREACH.md`

Invoke the **`launch-outreach`** skill with compliance mode **`product-hunt`**, `positioning.md`, and
the launch date — it produces the segmented plan and paste-ready, compliant messages (teaser DM, waitlist
email, launch-day email waves, community heads-up, 1:1 DM, X thread, LinkedIn) plus the wave schedule.
*Fallback:* if it isn't installed, draft them from `references/policy-compliance.md` (the safe-vs-unsafe
phrasing and templates there). **Success criteria**: every message is paste-ready, personalized, and
passes the no-vote-solicitation scan.

## Step 6: Wire measurement → tag links & events

Invoke the **`launch-analytics`** skill for this launch — **channel `product-hunt`** (the on-disk slug, so
it writes `.ulpi/launch/product-hunt/analytics.md` alongside the rest of the package) with **`utm_source`
`producthunt`** (the GA value) — to set the UTM scheme, tag every launch link in `LISTING.md` and
`OUTREACH.md`, and wire signup/activation tracking. *Fallback:* if it isn't installed, apply a minimal
inline UTM scheme (`utm_source=producthunt&utm_medium=<placement>&utm_campaign=<launch>`) and **write the
UTM map + signup/activation plan to `.ulpi/launch/product-hunt/analytics.md`** so the artifact exists either
way. **Success criteria**: every link is attributable and signups are trackable — not just upvotes.

## Step 7: Pre-flight gate → `CHECKLIST.md`

Run `references/preflight-gate.md` end to end and write the result into `CHECKLIST.md`. Several items are
mechanical: tagline ≤60 (counted), description ≤500, gallery count/dimensions, first comment present,
**zero** banned vote-soliciting phrases across all outreach, links UTM-tagged, topics ≤3, supporter list
realistic. Then append a short **launch-day checklist** — the `launchday-runbook.md` cadence distilled to
tickable go-live steps (publish 12:01am PT, post first comment, notify wave 1, reply to comments, midday
push, final-hours push, day-wrap thanks) — so `CHECKLIST.md` carries both the readiness gate and the
day-of checklist. Fix any failing box and re-run. **Success criteria**: every box ticked; the package is
internally consistent and compliant.

## Step 8: Post-launch plan → append to `PLAN.md`

Load `references/postlaunch.md`. Append: claim/embed the badge if earned, ride the leaderboards/
newsletters/Orbit reviews, **convert the traffic spike** (emails, onboarding, retargeting via
`launch-analytics`), send thank-yous, repurpose into social proof, the re-launch rules (6+ months + a
significant update), and the **"if it's flopping" contingency** (keep engaging, never panic-blast or beg).
**Success criteria**: the user knows exactly what to do the moment the 24-hour window ends.

## Guardrails

- Coach compliant promotion only; never manipulate votes; decline and redirect if asked. No paid hunts.
- Ground all copy in the real product; never ship invented features, fake metrics, or generic taglines.
- One positioning, bound across every field and message; reuse `.ulpi/launch/positioning.md`.
- Compose the shared skills; if one is absent, install-hint + fall back — never hard-fail.
- Honor exact, current field specs; verify a critical number via `browse` when it might be stale.
- Set realistic expectations; never promise a rank, featuring, or virality.
- This skill specifies the gallery and video; it does not render images or edit video.
- Write the package to disk; don't leave the launch plan as ephemeral chat.

## When To Load References

- `references/ph-mechanics.md` — ranking/featuring, the day window, awards, best-day timing, realistic
  outcomes (Step 2).
- `references/field-specs.md` — exact current specs for every submission field (Step 3). Authoritative.
- `references/copywriting.md` — the PH listing asset profile passed to `launch-copy`, and the inline copy
  fallback (Step 3).
- `references/prelaunch-playbook.md` — the T-minus countdown, supporter-list building, self-hunt vs hunter,
  scheduling (Step 4).
- `references/launchday-runbook.md` — the hour-by-hour Pacific runbook, waves, engagement, roles, hard
  rules (Step 4).
- `references/policy-compliance.md` — prohibited behavior, shadowban triggers, the banned-phrase scan, and
  the outreach fallback (Steps 5, 7).
- `references/preflight-gate.md` — the blocking readiness + compliance gate (Step 7).
- `references/postlaunch.md` — badges, leaderboards, Orbit reviews, converting the spike, thank-yous,
  re-launch rules, and the flop contingency (Step 8).

## Output Contract

Write under `.ulpi/launch/` and report:

1. `.ulpi/launch/positioning.md` — the shared grounded brief (created or reused)
2. `product-hunt/LISTING.md` — name, tagline options (one recommended), description, topics, gallery
   shot-list, demo-video outline, maker first comment, UTM-tagged links
3. `product-hunt/PLAN.md` — the countdown, the hour-by-hour runbook, the hunter/date decision, the
   post-launch plan
4. `product-hunt/OUTREACH.md` — supporter segments and paste-ready compliant messages + social posts
5. `product-hunt/CHECKLIST.md` — the pre-flight gate result (every box ticked) and the launch-day checklist
6. `product-hunt/analytics.md` — the UTM map + signup/activation tracking (from `launch-analytics`)
7. a realistic expectation set and the compliance affirmation (zero vote-soliciting language in any
   message), plus which companion skills were used vs fell back to built-ins
