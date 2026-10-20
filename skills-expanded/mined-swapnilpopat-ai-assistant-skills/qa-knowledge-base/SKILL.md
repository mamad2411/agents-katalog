---
name: qa-knowledge-base
description: Build a living QA knowledge base — patterns, runbooks, test data, env access, defect taxonomy, AT/perf cookbooks — that scales onboarding and reduces recurring questions. Use when QA tribal knowledge is bottlenecked or scattered.
source: self
date_added: 2026-05-01
---

# QA Knowledge Base

A QA KB exists to make recurring knowledge **self-serve**: how to run a test, where data lives, how to repro a tricky bug class, what's owned by whom. The bar: "a new engineer answers their question in < 5 minutes."

## Stack Baseline (2026)

| Concern | Default |
| --- | --- |
| Storage | Repo-as-source-of-truth (`/docs/qa/**`) rendered via Backstage TechDocs / MkDocs / Docusaurus |
| Search | Backstage search, Algolia DocSearch, Glean |
| Diagrams | Mermaid + PlantUML embedded in MD |
| Templates | Reusable templates per artifact (test plan, charter, perf report, bug template) |
| Ownership | CODEOWNERS per page; "last reviewed" date enforced via lint |
| Lint | Vale, markdownlint, link-check, "stale > 90 days" CI check |

## When to Use

- Scaling the QA team beyond 3–5 people.
- Recurring questions in chat ("how do I get a test card?").
- Onboarding a new engineer / contractor.
- Tribal knowledge concentrated in 1–2 people.
- Pre-audit (SOC 2, ISO 9001, ISO 25010) evidence gathering.

## Suggested Structure

```
docs/qa/
├─ index.md                       # entry point + map
├─ getting-started/
│  ├─ onboarding.md
│  ├─ tools-access.md             # Jira, BrowserStack, Sentry, Tempo
│  └─ environments.md             # local, ephemeral, staging, prod
├─ patterns/
│  ├─ test-pyramid.md
│  ├─ flaky-test-quarantine.md
│  ├─ data-builders.md
│  └─ trace-correlation.md
├─ playbooks/
│  ├─ release-readiness.md
│  ├─ pre-launch-bug-bash.md
│  ├─ on-call-during-release.md
│  └─ post-incident-test-gap-review.md
├─ cookbooks/
│  ├─ a11y/                       # axe, NVDA, VoiceOver recipes
│  ├─ perf/                       # k6 templates, k6+OTel
│  ├─ api/                        # Bruno collections, contract tests
│  └─ ui/                         # Playwright fixtures, POM samples
├─ taxonomies/
│  ├─ severity-priority.md
│  └─ defect-categories.md        # IEEE 1044
├─ test-data/
│  ├─ accounts.md                 # bot users, roles, permissions
│  ├─ payment-cards.md            # Stripe/Adyen test cards
│  └─ fixtures.md                 # how to generate
├─ runbooks/
│  ├─ recover-staging.md
│  ├─ rebase-test-database.md
│  └─ rotate-bot-credentials.md
└─ metrics/
   ├─ slos.md
   └─ flake-budget.md
```

## Page Anatomy

Every page must include:

```yaml
---
title: <topic>
owners: ["@qa-guild", "@payments"]
last_reviewed: 2026-05-01
review_cadence_days: 90
applies_to: ["all", "checkout"]
---
```

Body sections: **Purpose** → **When to Use** → **Steps / Recipe** → **Worked example** → **Pitfalls** → **References**.

## Lifecycle Discipline

- **Authoring**: pull request with template. Reviewer = page owner.
- **Review cadence**: CI flags pages where `last_reviewed > now - review_cadence_days`.
- **Deprecation**: archive in `docs/qa/_archive/`; never delete (history matters).
- **Telemetry**: Backstage page-views → identify dead pages and high-traffic gaps.

## Lint Snippet

```yaml
# .github/workflows/docs.yml
- name: markdownlint
  run: npx markdownlint-cli2 "docs/**/*.md"
- name: link-check
  run: npx markdown-link-check $(git ls-files 'docs/**/*.md')
- name: stale-pages
  run: node scripts/stale-docs.mjs --max-days 120
```

## Recommended Seed Pages (do these first)

1. Onboarding (Day 1 / Week 1 / Month 1)
2. Environments + access matrix
3. Test data (accounts, cards, seeded orders)
4. How to run the test suites locally + in CI
5. Bug report template + severity/priority guidance
6. Flake quarantine policy
7. On-call during release
8. Trace-correlation cookbook (k6 + OTel)
9. Accessibility quick start (axe, NVDA, VoiceOver)
10. Performance baselines + SLOs

## Common Pitfalls

| Pitfall | Fix |
| --- | --- |
| Confluence sprawl, no single source | Repo-as-truth; render to Backstage; Confluence read-only |
| Pages without owners | Owner mandatory in front-matter; CI enforces |
| Pages never re-reviewed | Stale lint with cadence; PR to update |
| Nobody can find anything | Add search; flat enough hierarchy; index page with map |
| Process docs but no recipes | Cookbooks > policy; runnable examples |
| Doc rot from copy-paste | Single source per topic; transclude / link |
| Knowledge in screenshots only | Capture text; screenshots only as supplement |

## Output Format

A "KB health" report per quarter:

```
QA KB — Q2 2026 health
Pages:        118
Stale > 120d: 7 (assigned to owners; ETA 2 weeks)
Top traffic:  test-data/payment-cards (4,210 views), envs (3,780)
Zero traffic: 12 candidates for archive
Search hit ratio: 81% (good)
```

## References

- Backstage TechDocs: <https://backstage.io/docs/features/techdocs/>
- *Docs Like Code* — A. Gentle
- ISO/IEC/IEEE 26515 (developing user docs)
- Vale linter: <https://vale.sh/>
- Diátaxis framework: <https://diataxis.fr/>
