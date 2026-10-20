---
name: pitch-templates
description: >
  Artifact templates for the Investor Deck Coach. Provides markdown and YAML
  skeletons for every artifact the agent and skills produce in `.pitch/{project}/`.
  Preloaded into the investor-deck-coach agent — not user-invocable.
user_invocable: false
---

# Pitch Templates

This skill is a template library. It is not invoked by slash command. The
`investor-deck-coach` agent and other skills load templates from
`templates/` when generating artifacts.

## Templates Provided

| Template | Produces (v0.4 paths) |
|---|---|
| `templates/PITCH.yaml.template` | `.pitch/{project}/PITCH.yaml` — metadata, stage, ask |
| `templates/DISCOVERY.md.template` | `.pitch/{project}/DISCOVERY.md` |
| `templates/MARKET_RESEARCH.md.template` | `.pitch/{project}/02-research/MARKET_RESEARCH.md` |
| `templates/source.md.template` | `.pitch/{project}/sources/src-NNN-*.md` |
| `templates/proof-point.md.template` | `.pitch/{project}/proof-points/pp-NNN-*.md` |
| `templates/financial-model.yaml.template` | `.pitch/{project}/03-financials/MODEL.yaml` |
| `templates/NARRATIVE.md.template` | `.pitch/{project}/04-narrative/NARRATIVE.md` |
| `templates/slide.md.template` | `.pitch/{project}/04-narrative/slides/NN-*.md` |
| `templates/ADVERSARIAL_REPORT.md.template` | `.pitch/{project}/05-adversarial/ADVERSARIAL_REVIEW.md` |
| `templates/REHEARSAL_NOTES.md.template` | `.pitch/{project}/06-verification/REHEARSAL_NOTES.md` |
| `templates/COMPLETENESS_REPORT.md.template` | `.pitch/{project}/06-verification/VERIFICATION_REPORT.md` |
| `templates/EXPLORATION_JOURNAL.md.template` | `.pitch/{project}/journal/{YYYY-MM-DDTHHMMSSZ}-{topic}.md` — one file per session/topic, not a single rolling file |
| `templates/GLOSSARY.md.template` | `.pitch/{project}/GLOSSARY.md` |

## How Skills Use Templates

When a skill needs to create an artifact, it:

1. Reads the relevant template from `templates/`
2. Substitutes placeholders (`{{COMPANY_NAME}}`, `{{STAGE}}`, etc.) from
   `PITCH.yaml` and conversation state
3. Writes the populated artifact to `.pitch/{project}/`

Templates use `{{PLACEHOLDER}}` syntax. Placeholders unfilled at write
time MUST be left as `[TODO: description]` markers and flagged by
`/investor-coach:validate`.

## Updating Templates

Templates are versioned with the plugin. Changes require a minor version
bump in `.claude-plugin/plugin.json`. Backward compatibility for existing
`.pitch/` folders is not required at v0.1.0 — projects re-render on demand.
