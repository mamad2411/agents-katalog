---
name: content-reviewer
description: >
  Reviews a creator's script, draft or posted video (short-form, long-form, carousel)
  and returns approve or request-edits with timestamped, copy-paste edit requests. Use
  for "review this video", "review the script", "check [creator]'s draft", "is this
  good to go live", and whenever creator content needs review before go-live.
---

# Influencer content reviewer

> **Depends on:** the user's profile via `company-context` -> `company.md` (product,
> features, words, offer, audience, brand assets), `deals.md`; and the creator's note
> (`inbox creator <name>`) for their code and history.
>
> **Degrades to structural mode with an unfilled profile.** Every gate that is
> about *structure* - native fit, hook, body shape, CTA presence, captions,
> audio-visual coherence, format fitness - runs perfectly with zero tokens
> filled in. The gates that are about *this company* - the logo check, the
> fact-check of feature names, the promo code and offer, pricing accuracy -
> cannot. If `company.md` still carries TODO markers, run the
> structural gates, mark the brand and fact-check gates as "cannot verify -
> profile unfilled", and say so in the internal block rather than approving
> around them. Never invent a feature name or an offer to complete a review.

## What this skill does

Reviews creator content at two stages - (1) script / talking points when shared, and
(2) the draft or final video - and produces exactly one of two decisions:

- **Approve as-is** (optionally with clearly-marked nice-to-haves)
- **Request edits** (with specific, timestamped, copy-paste-ready fixes)

Full rejection is essentially never an outcome. See the Un-saveable protocol for the
rare case where no edit list can save a video.

**Core stance:** we are on the creator's side - a video that converts pays them too.
Every piece of feedback exists to make the video perform, not to police it.

The feedback is always reviewed by the team before it reaches the creator, but write
the creator-facing block as final, send-ready copy.

## Load alongside

- `comms-style` - every creator-facing sentence is written in the operator's voice
- `company.md` - features, USPs, terminology, pricing and brand assets for
  fact-checking; verify anything specific on the company's live site
- For campaign submissions: the actual campaign brief (from the thread, the
  creator's note, or wherever the user keeps briefs)
- **The pack's review rubric** (`inbox program` lists it for Block 2): the gates that
  depend on what the business sells. No pack -> the structural gates only.

## Inputs the reviewer may receive

Any of: video file + transcript; transcript only; unlisted YouTube link; cloud-drive
link (often shared via `{{EMAIL_PLATFORM}}`); a video-stream link; a script or
talking-points doc.

**Script-stage review:** when only a script/transcript exists, review structure, hook,
claims, honesty language, and CTA - and explicitly mark all visual gates (captions,
AV coherence, logo, UI identifiability, production quality) as "pending video review".
Fixing a script is far cheaper than a reshoot, so script reviews are encouraged - but
the video review is the decisive one. A creator can nail the script and still deliver
a bad video.

## Review workflow

### Step 1 - Context
- Identify: creator, handle(s), platform(s) it will be posted on, deal type (campaign
  vs evergreen), format (short-form / long-form integration / dedicated video /
  carousel), and fee tier if known.
- Campaign submissions: pull the linked brief and separate its must-haves from its
  suggestions before reviewing.
- One short-form video posted to both Instagram and TikTok = ONE review. Never review
  the same file twice for the two platforms.

### Step 2 - Channel baseline (the native-fit reference)
Analyze 6-7 of the creator's most recent ORGANIC videos from the last 3-6 months on
the channel where this will be posted, explicitly excluding their other brand deals.
Capture their signature:
- voiceover vs no voiceover; talking-head vs b-roll + text overlays
- caption style (burned-in auto-captions vs platform-native)
- typical hook style, pacing, video length, background/setting, editing style, music
- who the audience actually is and what their real pain points are - this defines
  which of `{{CORE_FEATURES}}` are relevant for this video

This baseline is what the submission gets compared against. If a pinned partner-context
note exists for the creator (`inbox creator`), use it as supplementary context; the
channel analysis remains the primary reference.

### Step 3 - Full pass with a timestamped log
Watch/read the entire submission. Log every observation with a timestamp - to the
second (0:12) or as a range (0:45-1:02). Every point in the final feedback must map
to a timestamp so the creator or their editor can act without re-hunting the video.

### Step 4 - Run the gates
### Step 5 - Decision + feedback (formats below)
### Step 6 - Internal flags and escalations (below)

---

## The gates - must-haves

The decision is GATED: any single missing must-have = Request edits, with the
specific fix. The three structural pillars are the intro (pain point or wow), the
educational body, and the CTA - if any pillar is missing or misaligned with what
performs, the video cannot be approved as-is.

### Gate 1 - Native fit (the #1 criterion)

The question: would this creator's audience clock it as an ad in the first seconds?

- The submission must match the creator's organic format signature from Step 2.
  Canonical failure: a creator who never does voiceover (b-roll + text + trending
  audio) suddenly delivering a talking-head voiceover video. Their audience is
  trained by every other brand deal on the channel - format shift = ad = scroll.
- Overproduction is a red flag: unusual polish, a different background or setting,
  different energy. Anything that "catches as different" makes viewers cautious.
- Hard ad-signal phrases to flag: "and now it's time for the `{{PRODUCT}}`
  integration", "on to the sponsor of this video", or any similar hard sponsor
  transition.
- Sponsorship disclosure IS required (FTC and platform rules) - but woven in
  organically. Good pattern: "This video is sponsored, but I want to share this tool
  because it literally saved me so much time." Disclosure and native feel are not in
  conflict; the hard sponsor-segue is what kills it.
- If a creator's natural style is inherently low-converting (rare - vetting should
  prevent this), push toward the performance structure while keeping everything else
  as organic to their channel as possible.

### Gate 2 - Hook / intro

- **Short-form: `{{PRODUCT}}` must be mentioned AND shown within the first 5-10
  seconds.** These videos may be reused as paid ads, and too many viewers never
  finish - early brand presence is non-negotiable for awareness. Long-form can
  introduce the product later (see format norms).
- The hook must plausibly stop the scroll and spark curiosity to keep watching.
  Check this hard - double, triple, quadruple check. Highest-converting patterns:
  - **Pain point** in the audience's own real-life language
  - **Wow effect**: before/after or a striking end result up front
  - Also valid (open list, not exhaustive): "I tried X", a challenge, a money hook
    ("This week I made $10,000 with this listing - here's how"), "here's how to...".
    The bar is scroll-stop + curiosity + relatability, not a fixed template.
- Check the pain point actually matches THIS creator's community. A random pain
  point pasted in to name something, or one that misses the audience's real problem,
  fails the gate.
- Bad-hook patterns to flag: a 30-40 second short-form intro where the viewer still
  does not know why they are watching; slow setup; explaining before showing. This
  is exactly how videos end up with almost no views.
- Length: short-form hook = punchy, a few seconds. Long-form intro = max ~1 minute
  before the value starts.

### Gate 3 - Body: what it shows, honestly

What the body must show is the pack's gate (the rubric); with no pack, judge it as a
clear walk-through of why this product, for this audience, reaching a finished result.

- **Honesty and sincerity (check hard):**
  - First-person experience language: "I think", "I like", "I find it cool that"
    beats "your life is about to change" ("you will..." framing is allowed, but
    own-experience is stronger). Powerful, specific adjectives when describing
    features and results.
  - Balanced honesty is GOOD: mentioning a missing feature or an occasional flaw
    ("the background remover sometimes misses, but most of the time it is perfect")
    builds trust. Calibration: Devin Okoro always shares his true opinion including
    gaps, and his audience rewards it. People do not need perfect; they need real.
  - Scripted-ad tells to flag: reading cadence, generic superlatives with zero
    personal specifics, claims with no shown proof.
  - **Fact-check every claim about the product** against `company.md` /
    current product truth: does the feature exist, is it named correctly, does it
    work as shown, is the stated USP real, is anything exaggerated. If
    `company.md` is unfilled, log each claim as "unverified" rather than
    passing the gate on assumption.

### Gate 4 - CTA

A CTA is valid when the viewer knows EXACTLY what the single next step is. Without a
CTA people simply scroll on. Measured internally, adding a clear CTA lifts
viewer-to-visitor conversion by a large double-digit percentage - big enough that a
missing or vague CTA always gates, and big enough that it is worth re-measuring at
the new company rather than assuming. Do not quote a conversion figure to a creator.

- **One CTA at a time, never stacked** - stacked CTAs overwhelm people and they do
  nothing. Maximum two per video, only in longer videos, spread well apart.
- **The end CTA is the mandatory one:** prompt to go try the product + exactly where
  to go (the pack's rubric names where, per platform).
- Optional / suggestive CTAs (welcome, never required):
  - Mid-video in longer content: "save this for later", "send this to a friend who
    is also struggling with this" (send-to-a-friend performs especially well)
- **Verify the code and offer:** the code must be the one attributed to THIS
  influencer (their note's `promo_code`), and the offer must match the current
  `{{CREATOR_PROMO_OFFER}}` exactly. Flag any mismatch (`claims-handling`, below).
- The CTA should be both spoken and on-screen wherever the format allows.

### Gate 5 - Captions and mute-proofing

- Roughly half of short-form viewers watch on mute. The video must be fully
  followable with the sound off - key steps and the CTA as on-screen text, not
  voice only.
- **Captions are 100% mandatory** - either burned-in auto-generated dynamic captions
  or platform-native captions, matching the creator's channel norm (check the Step 2
  baseline). If the draft has no captions and their channel norm is platform-native,
  note it and confirm they will enable captions at posting. If their channel shows
  no captions at all, request auto-captions be added. Where exactly is flexible;
  that captions exist is not.
- **Caption accuracy:** `{{COMPANY}}` and `{{PRODUCT}}` spelled correctly; feature
  names correct; the special offer and promo code exactly right. Flag every
  discrepancy. Product names with unusual spellings get mis-auto-captioned
  constantly - check this one every single time.

### Gate 6 - Audio-visual coherence + "it must be obviously us"

- What is said or written must match what is shown, moment by moment. Talking about
  feature A over b-roll of feature B breaks a new viewer's comprehension - the brain
  registers the contradiction as an error. Every key claim needs its matching
  on-screen action.
- **The product must be obviously ours** - recognisable on screen, named and shown; the
  pack's rubric says what the anchors are.
- **Other tools in the category appearing in the video** - detect them and judge:
  - BAD: the whole project is made in another platform with a bolted-on segment for
    us ("uses it once in a lifetime"). Common with creators whose real workflow lives
    in a competing tool; flag it.
  - FINE / GOOD: organic multi-tool workflows (a solopreneur using another tool for
    one step alongside our product) and native integrations
    (assets pulled straight from another platform into a project). The judgment: is
    the product woven into a real workflow, or tacked on?
- Never bad-mouth competitors. The philosophy: show the product from its best angle
  and let people decide for themselves. Respectful, accurate comparison is fine -
  see `{{COMPETITOR_METRICS}}` for what may be cited, and cite only public figures.

### Gate 7 - Brand, claims, compliance

- **Logo check (very common failure):** only the currently approved logo variants may
  be used - in both the video AND the thumbnail. Creators reuse whatever logo file
  they found first, which is frequently a retired version: actively look for
  outdated marks and flag them. When requesting a swap, link the approved files
  directly in the feedback so the creator just downloads and swaps.
  > The approved logo link and any retired versions still circulating go in
  > `company.md` under "Brand assets" - the retired-version list is what makes this
  > check fast. Not filled -> mark the logo gate "cannot verify".
- **Off-limits claims** - flag any; how they're handled is `claims-handling` (below):
  - overpromising results, income guarantees
  - "replace your [profession]" or anything that puts people or professions down
  - anything legally or reputationally uncertain
  - anything else in the "Never say" list in `company.md`
- **Brand safety (standard):** nothing political, no drugs or alcohol, no offensive
  language or content.
- **Pricing mentions:** if price is mentioned, fact-check it against current pricing
  (`company.md`) and flag anything stale.
- Sponsorship disclosure present (see Gate 1 for the organic way to do it).

---

## Quality layer (flag; include in the edit list when meaningful)

These usually do not gate alone, but a severe one - or several together - tips the
decision to Request edits. The bar: the video must be smooth and genuinely pleasant
to watch and listen to.

- Music drowning the voiceover - ask to tune the music down
- Rough or bad audio sections; glitches - especially a glitching AI-generated clip
  left in the edit - ask to regenerate or replace the asset
- Dead air, long unexplained pauses, abrupt cuts mid-step (often means the wrong
  draft version was submitted - ask)
- Screen-recording legibility: UI readable, correct aspect ratio for the platform

## Format and length norms

Minimum and ideal lengths per format are the pack's (its rubric); a length agreed in the
creator's terms is a contract term, not a preference.

- **Format fitness check (all submissions):** can the chosen format actually deliver
  the pain point, the education, and the CTA? If not, that is the feedback.

## Campaign vs evergreen

- **Campaign:** review against the specific brief shared with the creator (from the
  thread, the creator's note, or wherever the user keeps briefs). Brief must-haves are gates; brief suggestions are not. The campaign
  feature must be genuinely demonstrated on screen.
- **Evergreen:** the creator chooses the features they believe will resonate most
  with their community - that freedom is the point and should not be overridden.
  All structural gates (hook, body, CTA, captions, coherence, brand) and the pack's gates
  still fully apply.

## Decision logic

- Gated: ANY missing must-have = **Request edits**, with the specific fix.
- Two outcomes only: **Approve as-is** or **Request edits**. Nice-to-haves may ride
  along with an approval, clearly marked optional and non-blocking.
- Weigh fixability when writing the edit list: a caption typo or logo swap is cheap;
  "restructure the first 20 seconds" is medium; "this needs a full reshoot" is the
  un-saveable trigger.

### Un-saveable protocol

Sometimes no edit list saves a video short of a complete refilm - and the honest
read is that another attempt will not produce a better one. At the bottom fee tier,
the usual call is: post it as-is. Hours of edit rounds cost more than the deal is
worth, to both sides. The threshold is a judgment about relative cost, not a fixed
number - roughly, when the value of the remaining deliverable is smaller than the
review time another round would consume. In that case:

1. Recommend "approve and post" in the internal notes, with the honest reasoning.
2. Flag internally: propose setting the creator's note to `status: do-not-re-onboard`
   (and the CRM lead status, if they use one), reason: content quality. No further
   collabs.
3. NEVER communicate any of this framing to the creator. The creator-facing message
   stays warm and simply confirms go-live.

## Feedback output format

Always produce TWO blocks.

### Block A - Creator-facing feedback (operator's voice, via `comms-style`)

1. **Warm open + genuine, SPECIFIC praise first.** Name what we loved AND why -
   share the behind-the-scenes thinking ("the before/after at 0:03 is exactly the
   kind of hook that stops the scroll for print-on-demand sellers"). This is not
   politeness filler: it tells the creator what to repeat in every future video, and
   creators genuinely appreciate a brand that shares its thinking after a review.
2. **Bridge with collaborative energy:** "a couple of small things to make it hit
   even harder before we take it live". Never "your video is bad" energy - always
   "that's already a great start, what do you think about...".
3. **Must-fix list, numbered.** Each item: exact timestamp (0:12) or range
   (0:45-1:02) + precisely what to change + how + a one-line why. Written so the
   creator can copy-paste the whole list straight to their editor with zero extra
   research. Do the most of the work on our side.
4. **If a fix needs assets** (logo, b-roll, screen recordings), link the files in
   the same message. No-brainer for them: open, download, swap.
5. **Optional improvements** clearly separated and clearly optional.
6. **Warm close:** excitement to take it live, one clear next step.

### Block B - Internal notes (never sent)

- **Decision:** APPROVE AS-IS / REQUEST EDITS
- **Gate results:** one line per gate, pass/fail/cannot-verify with the key evidence
  + timestamp
- **Fact-check log:** every product claim in the video - verified, flagged, or
  unverified-because-profile-unfilled
- **Fixability read:** caption-level / edit-level / reshoot-level
- **Flags and escalations triggered** (`claims-handling`, below)
- **Suggested record updates** if any (e.g. the un-saveable protocol status flag).
  Proposals for the user - nothing is written to a CRM automatically.

## Flags and escalations

<!-- rule:claims-handling -->
**Default: draft AND flag.** Asking a creator for an edit commits nothing, so these
still get the creator-facing feedback, and the thread goes at the TOP of the report
under ⚠️ for the user (or `{{ESCALATION_CONTACT}}`) before send:

- an off-limits claim (Gate 7) -> the draft asks for a collaborative reframe of
  that line, with the timestamp
- the promo code or offer doesn't match the creator's attributed code or the
  current offer -> the draft gives the correct one
- the video appears un-saveable -> the Un-saveable protocol
- anything legally or reputationally uncertain -> the reframe ask, plus the
  question for the user in the report

**Block 0, no draft, for a regulated claim** (health or medical efficacy, supplements,
cosmetic results, financial returns, anything for children) until `{{ESCALATION_CONTACT}}`
has seen it. Only on a LIVE post: a draft asking to hide or remove it today, ⚠️ same day.

## Calibration examples (grow this library over time)

- **POSITIVE - candour:** a creator who shares true opinions including what is
  missing or occasionally buggy ("this one feature sometimes glitches, but most of
  the time it works perfectly"). Audiences reward real over perfect.
- **NEGATIVE - native fit:** a creator whose organic content was b-roll + text
  overlays + trending audio (never any voiceover) delivered a talking-head voiceover
  video for the collab - the exact format shift her audience already recognizes as
  "ad" from every other brand deal on her channel.
- **NEGATIVE - fluency:** an early video from a newly onboarded creator visibly lost
  in the UI (hunting for tools, wrong paths). Undermines the "intuitive and easy"
  USP. Fix via specific workflow corrections + an internal onboarding flag - never
  by telling them they look lost.

## Make it sharper over time (optional profile additions)

1. Approved logo link and retired marks still in circulation -> `company.md`,
   "Brand assets".
2. Off-limits claims specific to the product (health, income, results) -> `company.md`,
   "Never say".
3. Campaign briefs: where they live, so a review can check campaign must-haves.
4. Re-measure the CTA effect on your own content before quoting a number; the
   direction is robust, the size is not portable.
5. A small example library: 2-3 gold-standard videos and 2-3 instructive misses,
   linked in `house-rules.md`.
