---
name: onboarding-automator
description: "Automated developer onboarding — environment setup, first PR walkthrough, and codebase familiarization. Use when ramping up a new engineer on a project."
version: 1.0.0
platforms: [linux, macos]
---

# Onboarding Automator

## What It Does
Automates the developer onboarding journey from zero to first merged PR. Handles environment setup (dependencies, tools, configs), provides an interactive codebase tour (architecture, key modules, conventions), assigns a curated "good first issue," and guides the developer through the PR process with real-time feedback. Reduces time-to-first-PR from days to hours.

## Iron Laws (NEVER violate)
1. **Single command to start** — Onboarding must be reducible to one command: `onboard` or `make setup`. More than that is friction.
2. **Real task, not tutorial** — The first task must be a real, useful contribution. Tutorial projects don't create belonging.
3. **Environment is reproducible** — Setup must be deterministic. "Works on my machine" is the enemy of onboarding.
4. **Feedback in minutes** — New developer's first PR must get review feedback within hours, not days. Delayed feedback = lost momentum.

## Red Flags (STOP immediately)
- **Setup failure** — Environment setup fails on a supported platform → onboarding is broken; fix immediately
- **Outdated setup docs** — Setup instructions reference deprecated tools or versions → onboarding silently broken
- **First issue impossible** — "Good first issue" requires deep codebase knowledge → issue not actually "good first"
- **Zero feedback** — First PR sits unreviewed for 48+ hours → team doesn't prioritize onboarding

## Common Rationalizations (self-deception)
- "New devs should figure it out themselves" → Self-serve onboarding wastes weeks. Structured onboarding pays for itself in days.
- "The README is enough" → READMEs go stale. Automated setup scripts can't go stale because they fail fast.
- "We'll pair program the first week" → Pair programming is great but doesn't scale. Automation scales to infinite new devs.

## When To Use
- Onboarding new developers to an existing codebase
- Setting up onboarding infrastructure for a growing team
- Reducing time-to-productivity for contractors or interns
- Creating self-serve onboarding for open source contributors
- Auditing and fixing broken onboarding workflows

## Human Partner Signals (escalate to human)
- **Unique setup issue** — Environment fails in a way the automation can't fix → human mentor needed
- **Permission needed** — New dev needs access to systems (CI, cloud, DB) that require manual approval
- **First PR scope creep** — "Good first issue" turns out to be complex → reassign or scope down
- **Team assignment** — New dev needs a human mentor/ buddy assigned → team lead decision

## Pipeline
1. Prepare: define supported platforms, required tools, and environment configuration
2. Automate: create setup script that installs deps, configures tools, clones repos, runs verification
3. Document: generate interactive codebase tour — architecture diagram, key modules, conventions, testing
4. Curate: select "good first issue" from backlog — well-defined, scoped, with clear acceptance criteria
5. Guide: walk through PR workflow — branch, commit conventions, test requirements, review process
6. Support: provide real-time troubleshooting for setup issues and first PR blockers
7. Measure: track time-to-first-PR, setup success rate, and new dev satisfaction

## Verification Checklist
- [ ] Single command (`onboard` or `make setup`) works on all supported platforms
- [ ] Setup verification step confirms all tools and dependencies are correctly installed
- [ ] "Good first issue" is scoped to ≤4 hours for a new developer
- [ ] Codebase tour covers architecture, conventions, testing, and common workflows
- [ ] First PR review SLA defined and met (<24 hours from submission)
- [ ] Onboarding tested with someone unfamiliar with the codebase (fresh-eyes test)

## Related Skills
- `dev-environment-manager` — Reproducible environments are the foundation of onboarding
- `documentation-generator` — Generated docs provide the codebase tour content
- `code-reviewer` — First PR review uses the same review standards
- `github-pr-workflow` — PR workflow that new developers learn through onboarding
