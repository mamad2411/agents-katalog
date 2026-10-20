# AGENTS.md

> **muShanghai Longevity Month 2026**: program documentation and AI-agent navigation for the May 2026 self-experimentation cycle. AI-agent navigation; humans read README.md.

## Project Identity

This repo is the muShanghai Longevity Month 2026 program documentation and AI-agent skill family.
It covers two parallel cohorts: Longevity Month Experiment (May 19 - June 5) and BioBloom Hackathon (May 17 - 22).
It uses three unified tracks: Decoding TCM (Frank + Buddy), Lifestyle (Xiao He + Rebecca), and Proof of Living — the Longevity Month edition of muShanghai Build in Public — Track Leaders: Natalia + Mariam; program-wide Build in Public leads: Sunny + Tang Ming.
Pure documentation repo, zero source code. No build, no tests, no CI.

## Structure

```text
.
|-- LICENSE                     # Mozilla Public License 2.0
|-- README.md                   # Human-facing program guide and public catalog
|-- AGENTS.md                   # This root AI-agent navigation file
|-- experiment-leader/          # EL role definition; deeper detail in sub-AGENTS.md when present
|-- participants/               # Participant role definition; deeper detail in sub-AGENTS.md when present
|-- track-leader/               # TL service catalog; deeper detail in sub-AGENTS.md when present
|-- skills/                     # Seven muShanghai AI-agent skills; see skills/AGENTS.md
|-- .sisyphus/                  # Plans, notepads, and workflow scratch; see .sisyphus/AGENTS.md
`-- FYI/                        # Practical Shanghai references; see FYI/AGENTS.md
```

For deeper detail, read the nearest sub-AGENTS.md before editing inside that subtree.

## Where to Look

| Task | Location | Notes |
|---|---|---|
| Understand a role | `experiment-leader/ROLE.md`, `track-leader/ROLE.md`, `participants/ROLE.md` | Role docs are canonical for behavior. |
| Add or edit a skill | `skills/AGENTS.md` | Skill family conventions live there. |
| Find program conventions | `AGENTS.md` `## Conventions` | Root-level hard rules for the repo. |
| Check active implementation plan | `.sisyphus/plans/` | Start with the skill-family plan. |
| Find a Hongqiao clinic | `FYI/hongqiao-medical-resources.md` | Reference-only practical orientation. |
| Trace what was decided | `.sisyphus/notepads/*/decisions.md` | Pair with issues and learnings files. |
| Verify Four Musts spec | `skills/mushanghai-canon/references/four-musts.md` | Problem, Monitoring-or-Observation, Intervention-or-Interaction, Deliverables. |
| Find the canonical safety banner | `skills/mushanghai-canon/references/safety.md` | Use before health-adjacent outputs. |
| Check installed skills | `~/.claude/skills/mushanghai-*` | Symlinked to this repo when installed live. |
| Update README catalog | `README.md` | Must include all 7 skills, but don't duplicate it here. |
| Check calendar canon | `skills/mushanghai-canon/references/may-2026-calendar.md` | Use for May 12, 17, 19, 22, and June 5 dates. |
| Review track definitions | `skills/mushanghai-canon/references/three-tracks.md` | Same three tracks for both cohorts. |

## Conventions

- English-only document bodies. No Chinese characters anywhere in body text.
- 14-day protocol max. No 4-week, month-long, or approximately 17-day durations.
- Three unified tracks only: Decoding TCM, Lifestyle, Proof of Living.
- Four Musts, not Three: Problem, Monitoring-or-Observation, Intervention-or-Interaction, Deliverables. Proof of Living uses Interaction.
- Traffic-light markers: canonical emoji `🟢 / 🟡 / 🔴` plus the canon em dash separator. Never `[green / yellow / red]` or other variants.
- TOC required on docs with more than 3 H2 headings.
- Track Leader doc is a service catalog, not recruitment. `track-leader/ROLE.md` is not "we are hiring TLs".

## Anti-Patterns (this repo)

- Scripts inside `skills/*/` directories are forbidden in MVP per skill-creator constraint.
- `README.md`, `CHANGELOG.md`, or `INSTALL.md` inside `skills/*/` are forbidden.
- Frontmatter `description + when_to_use` combined over 1,536 chars is forbidden.
- `SKILL.md` over 500 lines, references over 120 lines, and assets over 100 lines are forbidden.
- Adding Chinese characters anywhere in body text is forbidden.
- Auto-publishing draft public posts is forbidden by the Phase 4 hard rule.
- Committing without explicit user instruction is forbidden.

## No-Code Reality

No `npm install`, no `pip install`, no test runner, no build step, no CI.
This is a markdown-only repo, so don't invent code commands or package workflows.
The only "install" is copying or symlinking `skills/*` directories into `~/.claude/skills/` and `~/.agents/skills/`.
LSP diagnostics on markdown remain useful for link checks and frontmatter sanity.

## Skill Family (7 skills)

- `mushanghai-canon` - read-only hub (non-invocable)
- `mushanghai-onboarding` - May 12 bootstrap
- `mushanghai-experiment-leader` - proposal / TL review / SOP / consent / mid-experiment status
- `mushanghai-track-leader` - scope / tech / pitch triage / daily traffic-light / synthesis
- `mushanghai-participant-log` - daily log + Recruitment Night
- `mushanghai-demo-prep` - 5-minute Demo Day prep (May 22 / June 5)
- `mushanghai-retrospective` - post-Demo Day retro + next seed
- Full catalog and conventions in `skills/AGENTS.md`.

## Roles

- `experiment-leader/ROLE.md` - proposes and runs a single experiment
- `track-leader/ROLE.md` - service catalog for what TLs offer
- `participants/ROLE.md` - subject + practitioner + recorder
- Role docs win over skills when they conflict.

## Active Workflow Artifacts

Active plan: `.sisyphus/plans/2026-05-11-mushanghai-skill-family.md` (Phases 0-3 complete, Phase 4 conditional).
Superseded plan: `.sisyphus/plans/2026-05-11-mushanghai-experiment-leader-skill.md` (1,307 lines, fully shipped).
Notepads: `.sisyphus/notepads/2026-05-11-mushanghai-skill-family/{decisions,issues,learnings}.md`.
Workflow conventions: `.sisyphus/AGENTS.md`.

## Hard Operational Rules

- Commit only on explicit user instruction.
- Outside-`.sisyphus/` file writes must be delegated per OH-MY-OPENCODE directive.
- Direct edits to `.sisyphus/*` are allowed.
- When a skill changes, the README catalog row and install loop must be updated.

## Top-of-Mind Gotchas

Symlink path: skills are symlinked from `~/.claude/skills/mushanghai-*` to the repo. Editing the file in either path edits the same content.
`search-mcp-install.md` (Tavily/Firecrawl) lives under `mushanghai-onboarding/references/`; not a rogue file.
`experiments/<track>/<seed-name>-*.md` is a runtime artifact path produced by skills, not committed to this repo.
