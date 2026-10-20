---
description: Validate a brief — completeness, contradictions, claim boundary. Writes nothing
argument-hint: [a campaign brief path, and/or overrides to validate alongside it]
---

Validate a brief. **Do not build anything.**

Arguments — a brief path, overrides, or both (may be empty): **$ARGUMENTS**

## Which brief

If the arguments name a file under `campaigns/*/briefs/`, that is the brief,
**merged over its campaign's `campaign.md`** — the brief supplies only what
differs, and inherited fields count as present. Validate the merged result.

Otherwise the brief is whatever this conversation has established: the request,
plus anything settled since. If nothing has been, say so and ask for the
required fields below rather than validating an empty brief.

## 1. Required

Report each as present or missing. Missing ones must be asked for, not invented:

- Format (`image` | `carousel` | `video` | `ugc`)
- Angle
- Pain point
- Hook
- Script

## 2. Inferable

For each absent field, say what you *would* assume:

- Name → slug from the hook or product
- Ratios → the type's default (`image` 1x1+4x5, `carousel` 1x1, `video`/`ugc` 9x16)
- Duration → 15s video, 24s UGC
- Brand → the only file in `brands/`, or ask if there are several
- Placement, Audience, CTA → from the brand and the offer

## 3. Contradictions

Name them; don't resolve them silently. The ones that actually occur:

- A `Duration` on an `image` (images have no timeline)
- Ratios that fight the stated placement
- A `Brand` with no matching file in `brands/`
- A 6s `ugc`, or a duration the angle can't fill
- Fields carried over from a different ad — a slug, proof line or CTA that
  describes another product
- A campaign brief that restates an inherited field with a *different* value
  than `campaign.md` — the override wins, but say it happened; it's usually a
  stale copy rather than an intentional exception

## 4. Claim boundary

List every fact **Proof / claims allowed** actually authorises — for a campaign
brief that list lives in `campaign.md` and covers the whole campaign. That list
plus the product and offer as stated is the complete set of what may appear on
screen. Flag anything in the Script or Hook that asserts more — a number, a
price, a rating, a guarantee, a testimonial — and say it will need a visible
placeholder or a source.

Check the Hook and Script against **Do not say** and the brand's `voice.avoid`.

## 5. Verdict

One of:

- **Ready** — what you'd assume, then build with `/generate`
- **Ready with gaps** — buildable, but list what a placeholder will stand in for
- **Blocked** — which required field is missing, and the question to answer

Nothing is written to disk by this command.
