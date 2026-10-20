# mushanghai-canon/AGENTS.md

> Non-invocable canon hub. Other muShanghai skills load these references as prerequisites. See `../AGENTS.md` for family-level conventions.

## Local Layout

- `SKILL.md` - read-only loader notes, `disable-model-invocation: true`.
- `references/canonical-sources.md` - repo source-of-truth order when docs conflict.
- `references/four-musts.md` - Problem, Monitoring or Observation, Intervention or Interaction, Deliverables.
- `references/may-2026-calendar.md` - May 12, 17, 19, 22, June 5 timing.
- `references/proof-of-living.md` - canonical Proof of Living track spec, hashtags, handles, cadence.
- `references/safety.md` - never-paste list, consent policy, high-risk escalation.
- `references/three-tracks.md` - Decoding TCM, Lifestyle, Proof of Living track definitions.
- `references/two-cohorts.md` - Longevity Month Experiment and BioBloom relationship.

## Where to Look

| Task | Location | Notes |
|---|---|---|
| Check invocation status | `SKILL.md` | Canon is not user-callable. |
| Find safety banner | `references/safety.md` | Spokes show this before user-facing work. |
| Verify Four Musts labels | `references/four-musts.md` | Use Interaction for Proof of Living. |
| Confirm dates | `references/may-2026-calendar.md` | Key May 2026 cycle dates only. |
| Resolve doc conflict | `references/canonical-sources.md` | Root role docs win over compact refs. |

## Local Conventions

- Read-only hub.
- Frontmatter has `disable-model-invocation: true`.
- Spokes load references by relative path, `../mushanghai-canon/references/...`.

## Anti-Patterns (this skill)

- Invoking canon directly from user input.
- Duplicating canon text inside a spoke skill.
- Editing references without updating affected `ROLE.md` or `README.md` content alongside.

## Hand-Offs

- Loaded by `mushanghai-onboarding`, `mushanghai-experiment-leader`, `mushanghai-track-leader`, `mushanghai-participant-log`, `mushanghai-demo-prep`, and `mushanghai-retrospective`.
