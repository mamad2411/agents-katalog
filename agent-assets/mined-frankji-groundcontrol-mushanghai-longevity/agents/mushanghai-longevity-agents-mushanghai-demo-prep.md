# mushanghai-demo-prep/AGENTS.md

> Single-mode 5-minute Demo Day walkthrough builder. Used for both May 22 BioBloom and June 5 Longevity Month. See `../AGENTS.md` for family-level conventions.

## Modes

| Letter | Name | Trigger | Primary Output Path |
|---|---|---|---|
| Single | Demo Day preparation | prep my demo, 5-minute demo, demo day prep, rehearse my demo | `experiments/<track>/<seed-name>-demo.md` |

## Local Layout

- `SKILL.md` - single-mode walkthrough and output rules.
- `assets/demo-outline.md` - demo output template.
- `assets/rehearsal-checklist.md` - readiness checklist for step 5.
- No local `references/` directory exists; date and Four Musts context comes from canon references listed in `SKILL.md`.

## Where to Look

| Task | Location | Notes |
|---|---|---|
| Draft the demo | `assets/demo-outline.md` | Main output template. |
| Check rehearsal readiness | `assets/rehearsal-checklist.md` | Walk every item, require confirmation. |
| Confirm Demo Day dates | `../mushanghai-canon/references/may-2026-calendar.md` | May 22 and June 5. |
| Restate Four Musts | `../mushanghai-canon/references/four-musts.md` | Use Interaction for Proof of Living. |
| Add Proof of Living public details | `../mushanghai-canon/references/proof-of-living.md` | Hashtags and handles must appear. |

## Local Conventions

- Proof of Living demos restate four required hashtags and platform handles.
- Plan B is mandatory for live demo, data import, or participant failure.
- Minute budget totals no more than 5 minutes.

## Anti-Patterns (this skill)

- Live-demo-only output with no Plan B.
- Demoing Proof of Living without surfacing the four hashtags.
- Inventing outcomes, counts, source files, or observations.
- Using more than one anchor visual or artifact.

## Hand-Offs

- After Demo Day, hand to `mushanghai-retrospective`.
