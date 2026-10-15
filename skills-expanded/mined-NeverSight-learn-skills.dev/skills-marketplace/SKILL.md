---
name: skills-marketplace-skill
description: Discovers, evaluates, installs, audits, and integrates external skills from the skills.sh ecosystem into the local workflow.
---

# Skills Marketplace Skill

You act as the external skill integration role.
Use this when the task is better served by a mature reusable skill than by rebuilding everything manually.

## Use Cases

- the user explicitly asks to search or install skills from skills.sh
- the task belongs to a mature high-frequency domain where external skills likely exist
- there is a clear knowledge gap and a specialized skill is likely faster and safer than manual research alone

## Default Workflow

1. Identify the domain: frontend, testing, deployment, database, mobile, and so on.
2. Search skills.sh for relevant candidates and anchor the answer to the current marketplace state, not cached assumptions.
3. Start with the current skills.sh page evidence: purpose, install count, audit badges, and obvious scope boundaries.
4. Review repository source only after the shortlist is already tight or before installation.
5. Compare maintenance burden, vendor lock-in, and repo conventions before recommending installation.
6. Install only the most relevant repo or individual skill, not a grab bag of loosely related ones.
7. Integrate the skill back into the current project context instead of treating it as a black box.
8. Check updates and treat external skills as dependencies that may need review.

## Time-Sensitive Output Rules

- date every marketplace recommendation when install counts or rankings matter
- if the shortlist changed materially since the last recorded example, prefer refreshing the recommendation over preserving old wording
- for ranking-heavy searches, prefer a small current shortlist over a broad survey
- treat marketplace snapshots as time-sensitive assets that need periodic refresh, not one-time captures

## Common Commands

- search: `npx skills find [query]`
- install repo: `npx skills add <owner/repo>`
- install one skill from a GitHub repo: `npx skills add https://github.com/<owner>/<repo> --skill <skill-name>`
- shorthand install when supported: `npx skills add <owner/repo@skill>`
- global install one skill: `npx skills add https://github.com/<owner>/<repo> --skill <skill-name> -g -y`
- check updates: `npx skills check`
- update installed skills: `npx skills update`

## Recommended Starting Point

If the environment needs a discovery entry point first, start with:

- `find-skills` by `vercel-labs/skills`

If `find-skills` is already installed locally, use it as the first entry point for discovery before manual browsing.

Typical search areas:

- React / Next.js
- Playwright / testing
- Expo / React Native
- API design / backend patterns
- dbt / analytics engineering / warehouse modeling
- security / code review
- Docker / deploy / observability
- incident response / SRE / on-call workflows

## Security And Quality Rules

- review the skill page and repository source before installation
- prefer reputable organizations and clearly scoped skills
- do not install many unrelated skills at once
- make it explicit when the answer is based only on current skills.sh page evidence versus a deeper repo review
- make vendor, cloud, or repo-layout lock-in explicit when it matters
- validate important conclusions even after installation

## Output Focus

- candidate skills found
- why each one is recommended or rejected
- install commands
- expected usage boundary
- obvious trust, maintenance, and vendor-lock-in tradeoffs
- whether later updates or audits are needed
