<!--
  SKILL.md — Ad Copy operating manual.
  Runtime: Claude Code + ACP (swappable coding CLI). Content stays LCD —
  no assumptions about a specific channel unless injected via a stack overlay.
  Channel-specific specs/limits are NOT here — they live in stacks/<channel>/
  overlays. Injection points are marked: `STACK: ...`
-->

# Skill: Ad Copy

## Invocation

```
/ad_copy <brief + channel>
```

Or picked up from a Signal Protocol entry / PR assigned to ad-copy. Either way:
**no brief, no work.** If there's no brief naming the offer and audience, ask
for one — do not invent the offer.

---

## Step 1 — Read the brief and confirm the four corners

Before writing a single line, confirm from the brief:

| Question | Why |
|---|---|
| What is the **offer**? (the one thing being sold / the single ask) | One ad, one ask. If the offer is fuzzy, every variant is fuzzy |
| Who is the **audience**? (who they are, what they want, what stops them) | The hook is aimed at a person, not a market |
| What is the **channel + placement**? | Sets the character limits, format, and tone — the hard constraints |
| What are the **constraints**? (char limits, claims allowed, brand rules, must-include) | Bounds what can ship; a great line outside the limit doesn't run |

**Rule:** If the offer, audience, or the single thing the ad must do is
ambiguous, ask once. If still unclear, escalate — do not invent the offer.

---

## Step 2 — Nail the angle

Pick the **single angle** before writing variants. The angle is the argument
the ad makes — not the wording.

- State it in one sentence: *"For <audience>, <offer> means <benefit>, because <reason-to-believe>."*
- Confirm the reason-to-believe is in the brief. If the only support is an unprovable claim, escalate (see SOUL → Escalation) — don't proceed on a claim you can't back.
- If the brief supports more than one strong angle, list them — each becomes a row in the matrix (Step 5). One angle per row; never blend two in one line.

---

## Step 3 — Write N hook variants

For each angle, write a spread of hooks that **disagree** with each other — the
point is to test approaches, not polish one:

- Hit the idea in the **first three words**.
- Cover distinct hook patterns: question, bold claim (defensible), pattern-interrupt, social proof, problem-callout, curiosity gap.
- One idea per hook. No hook carries two angles.
- Default to ~5 hooks per angle unless the brief says otherwise (see hook checklist).

<!-- STACK: channel-specific hook conventions (e.g. TikTok native vs. Google RSA headline) injected here -->

---

## Step 4 — Write headline + body variants per angle

For each angle, pair hooks with the rest of the unit:

- **Headline** — the promise, defensible, within the channel's headline limit.
- **Body** — supports the headline, names the benefit concretely, no padding.
- **CTA** — one clear ask that matches the offer.
- Keep claims to what the brief backs. Flag any superlative or figure for sign-off rather than softening it (see SOUL → Escalation).

---

## Step 5 — Build the A/B test matrix

Lay the variants out as an explicit matrix so what's being compared is legible
and every line is addressable:

```markdown
| ID   | Angle              | Variable tested | Hook (first 3 words…) | Headline | Body | CTA |
|------|--------------------|-----------------|-----------------------|----------|------|-----|
| A1   | <angle 1>          | hook pattern    | …                     | …        | …    | …   |
| A2   | <angle 1>          | hook pattern    | …                     | …        | …    | …   |
| B1   | <angle 2>          | hook pattern    | …                     | …        | …    | …   |
```

- **Change one variable at a time** across an angle's variants, so a result attributes to a cause (hook pattern, claim strength, CTA).
- Every variant has a unique **ID** — test results read back to a line by ID.
- Note the proposed **split** (even split unless the brief says otherwise) and the **primary metric** the test should judge (CTR, CVR — whatever the brief names; if none, flag it for growth-hacker).

---

## Step 6 — Fit channel specs

Before handoff, run every variant through the channel-constraints checklist
(below). Anything that overflows a limit gets rewritten to fit — the limit is
the constraint, not the line.

<!-- STACK: channel-specific specs (character limits per field, aspect ratios, placement rules, ad-policy restricted claims) injected here -->

---

## Step 7 — Hand off (async)

Per the Signal Protocol — handoff is file-based / PR, never a live spawn.

Open a PR (or append to `signals/→<agent>.md`) with:

```markdown
## Ad Copy — <Campaign / Offer Name>

### Brief
Brief: <path> | Offer: <one line> | Audience: <one line> | Channel: <channel + placement>

### Angles tested
- <angle 1 — one sentence>
- <angle 2 — one sentence>

### Variant matrix
<the matrix from Step 5>

### Proposed test
- Split: <even / weighted> | Primary metric: <CTR / CVR / …>

### Claims flagged for sign-off
- <claim> — needs <source / approval> before it ships (or: none)

### Definition of done
- [ ] Every variant fits the channel spec (char limits / format)
- [ ] One variable changes at a time within each angle
- [ ] No unprovable claim ships unflagged
```

Then flag growth-hacker to wire the test (split, audience, metric) and
data-analyst to read the result. Do not call the winner yourself — the data
does, read by data-analyst.

---

## Variation matrix template

Use this skeleton whenever you generate variants — it forces one-variable-at-a-time:

```
Angle:        <the single argument>
Hold constant: <offer, audience, channel — fixed across the row>
Vary:         <ONE of: hook pattern | claim strength | CTA | tone>
Variants:     A1 … An  (one per value of the varied dimension)
```

---

## Channel-constraints checklist

Every variant clears all of these before handoff:

- [ ] Within the channel's **character limit** for each field (headline / primary text / description)
- [ ] Fits the **format / placement** named in the brief (feed, story, search, etc.)
- [ ] Honours **must-include** elements (brand name, legal line, disclaimer)
- [ ] No **prohibited claim** for the channel's ad policy (escalate if unsure)
- [ ] Tone matches the channel's native register (not a desktop banner on a vertical feed)

<!-- STACK: channel-specific limit values + policy list injected here -->

---

## Hook checklist

Every hook clears all of these before it enters the matrix:

- [ ] The idea lands in the **first three words**
- [ ] Carries **one idea** — not two stitched together
- [ ] Aimed at the **audience's** want or blocker, not the product's feature list
- [ ] Any claim in it is **defensible** by the brief (or flagged for sign-off)
- [ ] **Distinct** from its siblings — it tests a different pattern, not a synonym swap
