# mushanghai-retrospective/AGENTS.md

> Single-mode post-Demo Day retrospective. Hands off into next seed hypothesis. See `../AGENTS.md` for family-level conventions.

## Modes

| Letter | Name | Trigger | Primary Output Path |
|---|---|---|---|
| Single | Post-experiment retrospective | retrospective, post-experiment reflection, reproduction notes, next experiment seed | `experiments/<track>/<seed-name>-retro.md` |

## Local Layout

- `SKILL.md` - single-mode retro flow and five-step protocol.
- `assets/retro-template.md` - retrospective output template.
- No local `references/` directory exists; safety, Four Musts, and handoff context come from linked skills and canon refs in `SKILL.md`.

## Where to Look

| Task | Location | Notes |
|---|---|---|
| Build the retro | `assets/retro-template.md` | Fill after collecting track, seed, dates, signals, artifacts. |
| Check HARK warning | `SKILL.md` | Step 2, possible explanations. |
| Preserve reproduction details | `SKILL.md` | Step 3 lists required repeatability fields. |
| Route next seed | `SKILL.md` | Step 5 hands to EL proposal bootstrap. |
| Add participant language | `mushanghai-participant-log` | Use for group retros only. |

## Local Conventions

- HARK warning stays visible: never rewrite the original hypothesis after seeing data.
- Null results, missed days, and device failures remain in the retro.
- Solo and group retros use different prompts.

## Anti-Patterns (this skill)

- Editing the original hypothesis post-hoc.
- Turning the retro into a new proposal before Step 5.
- Hiding null results, missed days, or device failures.
- Writing identifiable health data or participant names into the retro.

## Hand-Offs

- Step 5 hands to `mushanghai-experiment-leader` Mode A for the next seed.
