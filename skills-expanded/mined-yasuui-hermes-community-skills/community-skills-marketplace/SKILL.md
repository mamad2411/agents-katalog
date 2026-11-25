---
name: community-skills-marketplace
description: Design, curate, secure, and ship a Hermes community skills marketplace with a polished skills.sh-style UX.
version: 1.0.0
author: Yasuui
category: productivity
tags:
  - hermes
  - skills
  - marketplace
  - curation
  - security
license: MIT
platforms:
  - macos
  - linux
  - windows
requires:
  - Hermes Agent v0.13.0+
---

# Community Skills Marketplace

Use this skill when building or reviewing a Hermes skills directory, marketplace, registry, or curation workflow.

## Goals

- Make the site feel like a real product, not a dump of files.
- Keep browsing and installation dead simple.
- Surface proven skills first.
- Preserve creator attribution with GitHub handles.
- Remove persona leakage and internal chat artifacts from public content.
- Treat skill content as untrusted input until validated.

## Canonical structure

Prefer a single source of truth for the public catalog:

- `skills/skills.json` for registry metadata
- `docs/data/community.json` for the public community payload when the static site needs a mirrored copy
- `docs/skills/built-in/catalog.json` for Hermes-managed / packaged content
- `SKILL.md` for each skill, with consistent frontmatter and a stable schema

Keep community-authored and Hermes-managed catalogs separated in both data and UI. The front page should be community-only; managed content gets its own page or surface.

Avoid fragmented one-off lists that drift apart.

## Curation model

Use explicit tiers and labels:

- `Hermes-managed` — maintained by the core Hermes project or shipped via updates
- `Community` — contributed by users
- `Proven` — actively used or repeatedly validated
- `Tested` — validated with the repo's schema/docs checks; use this only for community-added skills
- `Secure-reviewed` — passed the repo's validation/security checks

Surface the best few community skills in a featured area, then let search and filters do the rest.

If the public UI needs a trust signal, show it only where it is actually meaningful. Do not stamp `tested` onto Hermes-managed skills just because they are packaged.

## Attribution rules

- Attribute skill creators by GitHub handle when public.
- Use the contributor's actual handle, not a persona label.
- If the skill is a shared community contribution, keep attribution visible in the card and the detail view.
- For internal or private-only skills, mark them clearly and do not surface them in the public catalog.

## Security rules

Treat skill submissions as content, not code you can trust.

Validate for:

- required frontmatter fields
- malformed YAML
- unknown or unexpected fields
- secret/token patterns
- shell injection patterns
- dangerous binaries or executables in skill folders

Reject or quarantine anything that looks like malware, credential leakage, or a prompt-injection trap.

## UX rules

Aim for a skills.sh-like feel:

- strong hierarchy
- fast search
- clear categories
- featured skills up top
- visible install path
- compact card summaries
- trust badges that mean something

Avoid clutter, novelty chrome, and personality leakage.

## Workflow

1. Inspect the current registry and determine the canonical data source.
2. Identify proven skills from the repo and the user's existing Hermes skills.
3. Remove or hide internal-only skills from the public surface.
4. Standardize metadata and creator attribution.
5. Add security validation before any deployment.
6. Verify the live site renders and the public payloads stay in sync.

## Mobile-responsive table-to-card pattern

The site uses a table-first layout on desktop that must convert to stacked cards on mobile. Key rules:

1. **Remove `min-width` from `.skills-table` globally** — put it inside `@media (min-width: 760px)` so mobile cards never force horizontal scroll.
2. **At ≤760px**: hide `thead`, make `tbody` + `tr` `display: block`/`display: grid`, and label each `<td>` via `data-label` attribute + `content: attr(data-label)` on `::before`. Do **not** hardcode `nth-child::before { content: 'Label' }` — use `data-label` on each cell so JS-driven rows get the right label automatically.
3. **Action buttons** (Install/Remove, Copy prompt/Copy inspect) go side-by-side on mobile via `display: inline-flex` on their `<td>` containers, then stack full-width at ≤480px.
4. **Category chips** get `overflow-x: auto; flex-wrap: nowrap` on mobile so they scroll horizontally instead of wrapping.
5. **`.table-wrap`** gets `margin-left: -14px; margin-right: -14px; border-left: none; border-right: none` on mobile for full-bleed cards.
6. **Stat cards** collapse to single column at ≤760px, back to 3-column (tighter) at ≤480px.
7. **Hero grid** (`1.7fr / 0.9fr`) collapses to `1fr` at ≤1080px so aside drops below copy.
8. **Topbar tabs** wrap on mobile with `flex-wrap: wrap; width: 100%`.

Always add `data-label` attributes in the JS row-creation functions (`createCommunityRow`, `createManagedRow`), not just in the CSS. The CSS reads `attr(data-label)` for the mobile label; if JS doesn't set the attribute, mobile users see blank labels.

## Pitfalls

- Do not let public docs inherit internal agent persona language.
- Do not mix session notes into public catalog records.
- Do not let the featured list become a random grab bag.
- Do not rely on presentation alone; validate the underlying files.
- Do not hardcode `nth-child::before { content: 'Label' }` for mobile table labels — use `data-label` attributes on `<td>` elements and `content: attr(data-label)` in CSS. Hardcoded nth-child rules break when columns differ between community (6 cols) and managed (6 different cols) pages, and they conflict with the `attr()` approach.
- Do not put `min-width` on `.skills-table` unconditionally — it forces horizontal scroll on mobile. Wrap it in `@media (min-width: 760px)`.
- Vercel deployments can diverge from git HEAD. When the live CSS/HTML differs from what is in the repo, download the live files first (`curl`) and use them as the source of truth before making edits.

## References

- `references/marketplace-patterns.md` for the curation and security checklist used in this repo.
- `references/community-vs-managed-split.md` for the community-vs-managed catalog split, tested metadata rule, and removal UX pattern.
- `references/mobile-responsive-table-card.md` for the table-to-card breakpoint strategy, data-label approach, and source-of-truth divergence pattern.