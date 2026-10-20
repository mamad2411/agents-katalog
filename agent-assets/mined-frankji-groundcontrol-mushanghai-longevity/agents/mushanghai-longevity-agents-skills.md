# skills/AGENTS.md

> Hub-and-spoke AI-agent skill family for muShanghai Longevity Month 2026. AI-agent navigation; humans read the parent README.md install section.

## Hub-and-Spoke Architecture

One hub: `mushanghai-canon`, a non-invocable read-only skill with `disable-model-invocation: true`.
Six spokes load canon as a mandatory prerequisite through relative paths like `../mushanghai-canon/references/...`.
The pattern source is `larksuite/cli`'s `lark-shared` skill, adapted here for program canon rather than API auth.
Every spoke opens with the canon safety banner from `references/safety.md` before any other user-facing content.
This file covers only skill-family navigation; root `AGENTS.md` holds program-wide conventions.

## Spoke Catalog

| Skill | Audience | Modes | Trigger Window | Output Path |
|---|---|---|---|---|
| `mushanghai-canon` | (other skills) | n/a | always loaded | n/a (read-only refs) |
| `mushanghai-onboarding` | new attendees | A: full install · B: skills only · C: hypothesis only | May 12 | n/a |
| `mushanghai-experiment-leader` | EL + TL | A: Proposal · B: TL Review · C: SOP · D: Consent · E: Mid-experiment Status | May 15 - June 5 | `experiments/<track>/<seed-name>-*.md` |
| `mushanghai-track-leader` | TL | A: Scope · B: Tech · C: BioBloom Pitch Triage · D: Daily Traffic-Light · E: Synthesis | May 15 - June 5 | varies by mode |
| `mushanghai-participant-log` | participants | A: Daily Log · B: Recruitment Night | May 17 - June 5 | `experiments/<track>/<seed-name>/logs/...` |
| `mushanghai-demo-prep` | EL | single mode | post May 19 -> May 22 / June 5 | `experiments/<track>/<seed-name>-demo.md` |
| `mushanghai-retrospective` | EL (solo or group) | single mode | after Demo Day | `experiments/<track>/<seed-name>-retro.md` |

## Canon Layout

- `references/safety.md` - never-paste list plus canonical safety banner block.
- `references/four-musts.md` - Problem, Monitoring, Intervention or Interaction, Deliverables spec.
- `references/two-cohorts.md` - Longevity Month vs BioBloom dates and relationship.
- `references/three-tracks.md` - Decoding TCM, Lifestyle, and Proof of Living.
- `references/proof-of-living.md` - Proof of Living track spec and Build in Public parent framework.
- `references/may-2026-calendar.md` - date-by-date timeline.
- `references/canonical-sources.md` - when in doubt, which `ROLE.md` wins.

## Spoke Directory Pattern

```text
skills/mushanghai-{name}/
├── SKILL.md                  # frontmatter + walkthrough
├── references/               # supporting docs (link to canon refs)
│   └── *.md
└── assets/                   # templates the skill fills in
    └── *.md
```

## Hard Conventions (skill-authoring)

- `description + when_to_use` combined <= 1,536 chars (frontmatter cap).
- `SKILL.md` <= 500 lines, target 60-250 for current spokes.
- `references/*.md` <= 120 lines; `assets/*.md` <= 100 lines.
- Frontmatter `allowed-tools: Read Write` for all spokes; canon hub has no allowed-tools.
- First non-frontmatter line: `Valid for May 2026 cycle` admonition.
- Second admonition: prerequisite read of `../mushanghai-canon/references/safety.md` plus `../mushanghai-canon/references/four-musts.md`.
- Third section: `Always: show the canon safety banner first`; point to `references/safety.md` here instead of duplicating the banner.
- All asset cross-references use relative paths from the `SKILL.md`.
- No `scripts/`, `README.md`, `CHANGELOG.md`, or `INSTALL.md` inside any skill dir.

## Adding a New Skill

1. Create `skills/mushanghai-{name}/SKILL.md` mirroring `mushanghai-retrospective`, the smallest single-mode skill.
2. Add the canon prereq admonition plus safety banner pointer.
3. Add assets and references as needed, respecting line caps.
4. Symlink with `ln -sfn "$(pwd)/skills/mushanghai-{name}" ~/.claude/skills/mushanghai-{name}` and the matching `~/.agents/skills/mushanghai-{name}` path.
5. Add a row to the README catalog table.
6. Add the skill name to BOTH `for s in` loops in the README install commands.
7. Validate with `lsp_diagnostics` on the new files plus the canon-prereq grep test.

## Cross-Skill Handoffs

- `mushanghai-onboarding` -> `mushanghai-experiment-leader` Mode A, after seed hypothesis.
- `mushanghai-experiment-leader` Mode A -> Mode B, after TL review.
- `mushanghai-experiment-leader` Mode B -> Mode C (SOP) -> Mode D (Consent) after green approval.
- `mushanghai-track-leader` Mode C -> `mushanghai-experiment-leader` Mode B, post Recruitment Night.
- `mushanghai-participant-log` Mode B -> enrollment at Recruitment Night.
- `mushanghai-experiment-leader` Mode E -> `mushanghai-track-leader` Mode D, traffic light coordination.
- `mushanghai-demo-prep` -> Demo Day.
- `mushanghai-retrospective` Step 5 -> `mushanghai-experiment-leader` Mode A, next seed.
