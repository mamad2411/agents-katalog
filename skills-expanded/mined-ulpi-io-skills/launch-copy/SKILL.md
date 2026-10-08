---
name: launch-copy
version: 1.0.0
description: |
  Draft the copy a launch needs, in multiple angles, all bound to the REAL product — never generic
  placeholders. Produces taglines/headlines, one-liners, short and long descriptions, and the launch post /
  first comment in feature-led, benefit-led, comparison, and audience-led versions with one recommended each.
  Reads and reuses `.ulpi/launch/positioning.md` (the platform-agnostic product brief) so the product is
  described once and reused everywhere; grounds via the `browse` skill + repo when it's absent. Honors the
  caller's **asset profile** — hard character limits, voice, and compliance rules — to the letter. Shared
  copy block of the launch-* family, feeding the per-platform runners' posts (`launch-product-hunt` listing,
  `launch-hacker-news` Show HN, `launch-x` / `launch-linkedin` threads) or run standalone; writes to
  `.ulpi/launch/<channel>/copy.md` or hands drafts back. Use when a launch needs on-brand, within-limit copy
  grounded in one real product.
allowed-tools:
  - AskUserQuestion
  - Read
  - Write
  - Skill
argument-hint: "[channel + assets to draft, e.g. 'Product Hunt tagline + first comment']"
arguments:
  - request
when_to_use: |
  Use when drafting launch copy that must be grounded in a specific product — taglines, headlines,
  descriptions, a launch post or first comment, across one or more channels. Examples: "write my Product Hunt
  tagline and first comment", "draft copy for our directory listings", "give me 4 tagline options for the
  hero". Also invoked by the platform runners, which pass an asset profile. Do NOT use for long-form content
  (blog posts, docs), the PH gallery shot-list (redirect to `launch-product-hunt`), or person-to-person
  outreach (`launch-outreach`); this drafts the on-listing copy, nothing else.
effort: high
---

<EXTREMELY-IMPORTANT>
This skill drafts launch copy. Non-negotiable rules:

1. GROUND EVERY LINE IN THE REAL PRODUCT. Read `.ulpi/launch/positioning.md` if present; else ground from
   the live site (via `browse`), README, and product docs. Never invent features, metrics, customers, or
   awards. If you cannot determine what the product does and who it is for, ask — do not guess.
2. HONOR THE ASSET PROFILE EXACTLY. Respect every hard limit (character counts), the requested voice, and
   any compliance rules the caller passes. Count characters; never ship copy over a hard limit.
3. OBEY COMPLIANCE NOTES. If the caller passes a compliance rule (e.g. "Product Hunt: never solicit
   upvotes"; "Hacker News: no hype, no marketing-speak"), every line must pass it. When in doubt, ask the
   caller; never produce copy that would violate a platform's rules.
4. PRODUCE OPTIONS, NOT ONE GUESS. Draft each requested asset in multiple angle versions (see
   `references/angles.md`) and mark a recommended one with a one-line rationale.
5. NO SLOP. Lead with the benefit/outcome, be specific (a real noun or number), and pass the cold-read
   test. Ban buzzword soup, empty superlatives, and (unless the voice asks for it) emojis and hype.
6. WRITE THE BRIEF ONCE. If you ground the product fresh, save it to `.ulpi/launch/positioning.md` so
   every other channel and launch skill reuses it instead of re-deriving.
</EXTREMELY-IMPORTANT>

# launch-copy

## Inputs

- `$request`: the channel(s) and asset(s) to draft, plus optional links. When invoked by a launch skill,
  the caller also passes an **asset profile** (below). When run standalone, gather the profile from the
  user with one or two focused questions.

### The asset profile (the contract callers pass)

```
channel:     e.g. product-hunt | hacker-news | directory | landing | email
voice:       e.g. "benefit-led, concrete, no hype"  |  "technical, humble, no marketing-speak"
compliance:  any phrasing rules, e.g. "never solicit upvotes" | "no superlatives/emoji"
assets:      a list of —
  - id:       e.g. tagline | short-desc | long-desc | first-comment | gallery-headlines
    purpose:  what this asset does / where it renders
    limit:    hard character/word limit (if any)
    versions: how many angle variants to draft (default 3–4)
    notes:    format, a skeleton to fill, or examples to calibrate against
```

If a launch skill invoked you, **use its profile verbatim** and skip re-asking. If anything is missing
(voice, a limit), infer a sensible default and state it.

## Goal

Return **grounded, on-brand, within-limit copy** for every requested asset, in labeled angle versions
with one recommended each. Persist where the caller expects it (default `.ulpi/launch/<channel>/copy.md`,
or hand the drafts back for the caller to assemble), and keep `.ulpi/launch/positioning.md` current.

## Step 0: Resolve the brief

If invoked with an asset profile, adopt it (see `references/asset-profiles.md` for how to read/normalize a
profile). If standalone, ask at most a couple of questions — the channel, the product/URL, and what assets
are needed — then build a profile from the matching baseline in `references/asset-profiles.md`. **Success
criteria**: channel, product, and asset list are known.

## Step 1: Ground the product → `.ulpi/launch/positioning.md`

Read `.ulpi/launch/positioning.md` if it exists and reuse it. Otherwise ground from the live site (visit
it with the `browse` skill), the README, and product docs; also read a `.claude`/`.cursor`
`project-context.md` (Sections 1–9) and `.ulpi/design/DESIGN.md` if present. Distill: one-line what-it-is,
ICP, the core value in the user's words, **top 3 differentiators**, concrete proof points, the category,
and links. Save it so it's reused. Load `references/copy-craft.md`. **Success criteria**: a real product
brief no line will contradict — nothing invented.

## Step 2: Choose angles

Pick the angle set that fits the channel and product (load `references/angles.md`): **A feature-led ·
B benefit-led · C comparison/alternative · D audience-led**. For most launches benefit-led and
audience-led win; comparison-led shines when the reference product is well known. **Success criteria**: a
palette of distinct angles is chosen for the channel (not rewordings of one); each multi-version asset
draws on as many distinct angles as its profile `versions` requests, while single-version assets (e.g.
first-comment, gallery-headlines) get one well-chosen angle. The per-asset `versions` field is the single
source of truth for how many to draft.

## Step 3: Draft each asset, in versions, within limits

For every asset in the profile, draft the requested number of versions across the chosen angles, in the
requested voice, **within the hard limit** (count the characters). Fill any skeleton the profile provides
(e.g. a first-comment structure). Mark one version **recommended** with a one-line why. Use
`references/copy-craft.md` for the craft rules and `references/asset-profiles.md` for common per-channel
profiles and how to read them. **Success criteria**: every asset has labeled options, each within limit
and on-voice, with a recommendation.

## Step 4: Self-check (the copy gate)

Before returning, verify each line: grounded in the real product? specific (a real noun/number)? within
the hard limit (counted)? matches the requested voice? passes every compliance rule? passes the cold-read
test (a stranger gets it)? zero banned slop tells? Fix anything that fails, then return.
**Success criteria**: every box holds; nothing invented, over-limit, or non-compliant.

## Guardrails

- Ground everything; never invent features, metrics, logos, or social proof.
- Respect hard limits to the character; respect the voice and compliance rules to the letter.
- Give options with a recommendation, not a single take.
- Write the gallery slide **headlines** (copy) when the profile asks; never the gallery visual design or
  shot-list — that's the platform skill — nor long-form content.
- Reuse `.ulpi/launch/positioning.md`; don't re-derive the product brief if it already exists.
- Degrade gracefully if `browse` or a site is missing — ask the user for the key facts and proceed.

## When To Load References

- `references/copy-craft.md` — the craft: ground-in-product, benefit-led, specificity, the cold-read
  test, and the banned slop tells (Steps 1, 3, 4).
- `references/angles.md` — the A/B/C/D angle framework with patterns and real examples (Step 2).
- `references/asset-profiles.md` — how to read an asset profile, plus ready profiles for Product Hunt,
  Hacker News, directories, and landing pages (Steps 0, 3).

## Output Contract

Return / write:

1. `.ulpi/launch/positioning.md` — created or reused (the shared product brief)
2. for each requested asset: the profile's requested number of labeled versions (default 3–4 for
   taglines/headlines/one-liners; fewer where the profile specifies — e.g. 1 for first-comment and
   gallery-headlines, 2 for descriptions), each within its hard limit (character counts shown), with one
   marked **recommended** and a one-line rationale
3. when run standalone, the drafts written to `.ulpi/launch/<channel>/copy.md`; when invoked by a launch
   skill, the drafts handed back for the caller to assemble (per the Goal)
4. a one-line confirmation that every line is grounded, within limit, on-voice, and compliant
