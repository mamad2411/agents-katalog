---
description: Build a campaign's creative structure — personas, pain points, and a mapped set of ad concepts. Writes briefs, builds no ads
argument-hint: [business or campaign to plan, or "promote <campaign> 03,07,11"]
---

Plan a campaign: **$ARGUMENTS**

This stage produces the *creative structure* — who we're talking to, which pain
we're pressing, and the set of distinct ads that covers it. It writes
`campaigns/<slug>/` and nothing else. **No ad is scaffolded, authored or
rendered here** — `/build-ad` does that, one brief at a time.

Invoke the **`campaign-strategy`** skill and follow it. It owns the craft:
what makes a persona real, what makes a set of concepts genuinely diverse
rather than nine rewordings, and why the count matters.

Two modes, chosen by the arguments:

| Arguments | Mode |
|---|---|
| a business, a campaign idea, or empty | **new** — steps 1–7 below |
| `promote <campaign> <ids>` | **promote** — step 8 only |

---

## 1. Start from the client profile

**Read `brands/<name>.json` before asking the user anything.** Its `business`
block already holds what the client is, where they trade, which languages they
publish in, their socials, and every product line with its URL. That's most of
what this stage would otherwise interview them for, and it was captured when
the profile was built.

If no profile matches, stop and run `/brand` first — ideally with the client's
URL, which builds the profile and the token set in one pass. A campaign of
briefs naming a brand that doesn't exist is fifteen scaffolds that fail the
same way.

If the profile exists but has no `business` block, it predates this step. Offer
to fill it in via `/brand` rather than gathering the same facts into a campaign
where the next campaign can't reuse them.

## 2. Scope it to one line

One campaign is **one product or service line, one placement set, one
language**. The profile's `business.lines` is the list — offer it and let the
user pick. Four service lines are four campaigns, not one: a life insurance
buyer and a tax client share no persona and no claim boundary.

If the request spans several, say so and plan one. Settle the slug now
(`elevia-health-q1`); everything else hangs off it.

Then ask only for what the profile genuinely can't supply:

| | Why it's needed |
|---|---|
| **Placement** | Decides formats, ratios and length |
| **Goal** | What this campaign is for — leads, enrolments, a season |
| **Compliance boundary** | Regulated categories carry rules that vary by state and platform. Ask; don't assume one. |
| **Anything off-limits** | Banned phrasing, competitors, topics |

### Agree the shape of the map

**Ask for these four numbers. Don't decide them silently** — they set how much
work this campaign is and how much render time it implies, which is the user's
call, not yours.

| | Recommended | What moving it does |
|---|---|---|
| **Personas** | 3–5 | More personas = more of the market addressed. Capped by the differentiation test, not by appetite. |
| **Pain points per persona** | 2–3 | The axis that matters most for delivery — breadth across problems beats depth on one. |
| **Concepts per pain point** | 3 | Each must be a distinct format *and* angle, so this is bounded by how many pairs the campaign can actually use. |
| **Distinct angles, minimum** | 4 | Below four the set stops being diverse; above six it usually means angles the brief can't support. |

Offer the recommended values as the default so the answer can be one word, and
**state the arithmetic before they choose**: personas × pain points × concepts
is the size of the map. At the recommendation that's 18–45.

Take the numbers from the arguments if they're already there
(`/campaign health, 4 personas, 2 pain points, 3 concepts`) and don't re-ask.

Two things to say plainly when you ask:

- **A map is cheap; a build is not.** Mapping 40 concepts costs one pass.
  Nothing gets scripted until `promote`, and nothing renders until `/build-ad`.
- **These are targets, not quotas.** If the differentiation test or the claim
  boundary can't support the number requested, you'll deliver fewer and say
  which one bound — never padding to hit a count.

Record the agreed shape in `campaign.md` so a later run doesn't re-derive it.

## 3. Fetch the claims fresh

**The profile deliberately caches no claims.** Prices, offers, response times,
savings figures and testimonials go stale silently, and a stale claim in a
regulated ad is the failure this whole boundary exists to prevent.

So fetch the chosen line's page now — the profile hands you the exact URL — and
build the claim boundary from what it says today, dated to this run. Everything
the campaign may state, sourced line by line, into `campaign.md`. A line
qualifies only if the business published it: that page, the profile itself, or
the user's own statement.

**Research is not a claim licence.** A statistic from an industry article is not
a fact this brand may assert. Anything a concept wants but can't source becomes
a bracketed placeholder and a flag, never a plausible number.

Two optional passes, neither a blocker:

- **Socials** — the accounts are in the profile. They frequently refuse to
  fetch; don't fight it and don't guess at what's on them. Say so and ask for a
  few recent captions, or proceed and note the gap.
- **Competitors** — if the Meta MCP tools respond, `ads_library_search` shows
  what the category is actually running, which is how you find the angle
  everyone has saturated. If the tools error or aren't there, skip silently and
  note it.

## 4. Personas and pain points

Follow the skill, at the persona and pain-point counts agreed in step 2.

If you can't hit a count honestly — two personas would be convinced by the same
ad, or a persona has only one pain point the research actually supports — build
the smaller set and say which one bound. A padded persona produces padded pain
points, which produce padded concepts, and the whole branch is dead weight.

## 5. Concept map

Follow the skill, at the concepts-per-pain-point and minimum-angle counts agreed
in step 2. Each concept is a distinct format **and** a distinct angle within its
pain point. The skill's diversity rules are the point of this step — a map of
near-identical concepts is worse than a smaller map.

Report the shape you actually produced against the shape that was asked for, and
name any gap.

## 6. Write the files

```
campaigns/<slug>/
├── campaign.md      context, shared brief fields, claim boundary + sources
├── strategy.md      personas → pain points → concepts → production map
└── briefs/          one file per *promoted* concept — empty at first
```

### `campaign.md`

```markdown
# Campaign: <Name>

**Slug:** <slug>
**Brand:** <brand file in brands/ — the profile this inherits from>
**Planned:** <YYYY-MM-DD>
**Line:** <business.lines[].id> — <its url>
**Goal:** <what this campaign is for>
**Placement:** <platforms and surfaces>
**Language:** <e.g. es-US — and whether copy is written in it>
**Shape:** <P> personas × <N> pain points × <K> concepts = <total>, ≥<A> angles
  — as agreed; note anything delivered short of it and why

Business context (what it is, where it trades, socials) is **not repeated
here** — it's in the brand profile, and duplicating it is how the two disagree.

## Shared brief fields

Every brief in this campaign inherits these. A brief may override any of them.

**Brand:** …
**Placement:** …
**Ratios:** …
**Do not say:** …
**Assets:** …

## Proof / claims allowed

The complete set of facts any ad in this campaign may state on screen, read
fresh on the date below — **not** inherited from the brand profile, which
caches no claims for exactly this reason.

- <claim> — <source URL or "user-supplied">, read <YYYY-MM-DD>
- …

Nothing outside this list appears in an ad. A concept that needs more gets a
visible placeholder and a note in its brief. Re-read the sources before a paid
delivery if this campaign has been sitting.

## Off-limits

<regulatory constraints, banned phrasing, competitor rules>

## Sources

| What | URL | Read |
|---|---|---|
```

### `strategy.md`

The human deliverable — the thing to read and approve, and the record of why
each ad exists.

```markdown
# Strategy: <Name>

<one paragraph: the campaign's argument and who it's aimed at>

## Persona 1 — <descriptive name>

**Profile:** who they are, what they do
**What matters to them:** …
**How they decide:** what makes them act, what stalls them
**Voice:** the words they use for the problem

### Pain point 1.1 — <short label>

**The problem:** in their words, not the brand's
**Desired outcome:** what they actually want
**Already tried:** what failed, and why they're sceptical

| # | Format | Angle | Hook | Core message | CTA |
|---|---|---|---|---|---|
| 01 | image | problem-solution | "…" | … | … |
| 02 | ugc | testimonial | "…" | … | … |
| 03 | carousel | educational | "…" | … | … |

### Pain point 1.2 — …

## Production map

| # | Persona | Pain point | Format | Angle | Status |
|---|---|---|---|---|---|
| 01 | … | … | image | problem-solution | mapped |
```

`Status` is the campaign's state machine: `mapped` → `promoted` (a brief file
exists) → `built` (an ad exists in `ads/`). Keep it current; it's the only
record of what's been produced.

### `briefs/`

**Write no brief files in this pass.** The map is cheap and complete; briefs
carry finished scripts and are written on promotion, for the concepts actually
going into production. Create the empty directory and stop.

## 7. Promote — `promote <campaign> <ids>`

Turn mapped concepts into buildable briefs. For each id, write
`campaigns/<campaign>/briefs/<nn>-<name>.md`:

```markdown
# Brief

<!-- Inherits campaigns/<slug>/campaign.md. Only what differs appears here. -->

**Concept:** 03
**Name:** <campaign-slug>-03-<short-name>
**Format:** carousel
**Ratios:** 1x1
**Duration:** <video/ugc only>

**Angle:** educational
**Persona:** <name from strategy.md>
**Pain point:** <the problem, one line, in their words>
**Hook:** "…"

**Script:**
- <beat>
- <beat>

**CTA:** …

**Assets:** none — placeholder treatments
```

**`none` is the normal answer at promote time.** Ads are built with placeholder
treatments and real imagery is added afterwards with `/adjust`, which drops the
files into that ad's own `assets/` and re-renders. Only name files here if they
already exist.

Rules for this step:

- **The script is written here, in full.** Carousel cards, video beats with
  timings, UGC lines as a person would say them. Read the format's file in the
  `create-ad` skill's `references/` first — the beat structure differs a lot
  per format and it's most of the quality.
- **Only fields that differ from `campaign.md`.** Repeating the claim list into
  every brief is how it goes stale.
- **The `Name` is the ad's folder slug.** Prefix it with the campaign so the
  set sorts together in `ads/` and `pnpm dev`.
- **Check the concept against its claims before scripting it.** A concept that
  needs a number you don't have gets a bracketed placeholder — or say it can't
  be built as mapped and propose the angle that can.
- Set the concept's `Status` to `promoted` in the production map.

Then say the briefs are ready and how to build one:
`/build-ad campaigns/<slug>/briefs/<file>.md`.

## Report

Condensed. What the campaign covers, the persona and pain-point counts, the
concept count and how it splits across formats and angles, what's promoted, and
— most important — **what you had to ask for, what you assumed, and which
concepts are blocked on proof you weren't given.**

Say what came from the profile versus what you fetched or asked for. If the
profile was missing something a campaign will want again, say so — that's a
`/brand` fix, not a thing to re-gather next time.

Then the next move: `/campaign promote …` for more briefs, or `/build-ad` on
one that exists.
