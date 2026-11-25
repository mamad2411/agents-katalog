---
name: status
description: Circle status dashboard for the current project.
---

# Circle — Status Dashboard

Show the status of the Circle framework for the current project.

## Soul

Read and apply `../../resources/soul.md` before continuing.

## Process

1. **Detect project name**: `basename "$PWD" | tr '[:upper:]' '[:lower:]'`

2. **Detect domain** by analyzing files in the current directory:
   - **software**: if common project markers exist (e.g., `package.json`, `requirements.txt`, `go.mod`, `Cargo.toml`, `pom.xml`, `*.xcodeproj`, `Makefile`, `CMakeLists.txt`, `Gemfile`, `build.gradle`)
   - **business**: if `business-plan.md`, `market-analysis.md`, or `strategy.md` exists
   - **personal**: if `goals.md`, `journal.md`, or `habits/` folder exists
   - **general**: default if no domain indicator found

3. **Check workflow status**: Read `~/.circle/projects/<project-name>/output/session-state.json` if it exists.
   - If it exists: show current phase, active workflow, completed steps
   - If it doesn't exist: indicate Circle is not yet initialized for this project

4. **Check existing artifacts**: List files in `~/.circle/projects/<project-name>/output/` if the directory exists. Show each role's output files.

5. **Show simple view** (default):

```
Circle — <project-name>
================================
Domain:  <detected>
Status:  <initialized/not initialized>
Phase:   <current phase from session-state or "Not started">

What's done:
  <List completed steps, e.g. "Requirements (Scope Clarifier)", "Architecture (Architecture Owner)">
  <Or "Nothing yet — run circle:init to get started">

What's next:
  <Next suggested step based on phase>
  <Or "Run circle:greenfield for the full workflow">

Your circle:
  circle:scope       — Scope Clarifier (requirements, work items)
  circle:arch        — Architecture Owner (design, trade-offs)
  circle:impl        — Implementer (implementation, code review)
  circle:qa          — Quality Guardian (testing, quality)
  circle:e2e         — E2E Author (end-to-end tests in the E2E suite)
  circle:ux          — Experience Designer (UI/UX design)
  circle:refine      — Refiner (prioritization, roadmap)
  circle:facilitate  — Facilitator (cycle planning)
  circle:security    — Security Guardian (audits, threat modeling)
  circle:docs        — Documentation Steward

Workflows:
  circle:greenfield — Full workflow start to finish
  circle:cycle      — Cycle planning session (Shape Up)

Review:
  circle:pr-review — PR code review
  circle:triage      — Handle review feedback

Utilities:
  circle:validate-prd — PRD quality validation (8 checks)
  circle:tdd          — TDD red-green-refactor enforcer
  circle:init         — Set up Circle for this project
  circle:skills-discovery — Discover and install external skills (security-gated)
  circle:shard        — Split large docs for faster processing
  circle:council      — Pressure-test a hard decision with 5 analytical lenses

Tip: Invoke `circle:status detailed` for version and integration status.
```

6. **If the user requests "detailed" or "full" view**, also show:

Generated artifacts:
```
Generated artifacts:
  scope/       <list of files or empty>
  arch/        <list of files or empty>
  impl/        <list of files or empty>
  qa/          <list of files or empty>
  e2e/         <list of files or empty>
  security/    <list of files or empty>
  ux/          <list of files or empty>
  refine/      <list of files or empty>
  facilitate/  <list of files or empty>
  pr-review/  <list of files or empty>
  triage/      <list of files or empty>
  docs/        <list of files or empty>

Output directory: ~/.circle/projects/<project-name>/output/
```

Active workflow details:
```
Active workflow: <greenfield/cycle/none>
Completed steps: <list or N/A>
```

TDD configuration:
```
TDD:
  Enabled:     <true/false from config.yaml, default: true>
  Enforcement: <hard/soft from config.yaml, default: hard>
```

Inspect integrations exposed by the current host and check local binaries to show their availability.

```
Integrations:
  Linear:      <connected/available/unavailable>
  Notion:      <connected/available/unavailable>
  no-mistakes: <version/unavailable>

  Local:
    circle  <version from plugin.json>

Connect or install integrations only after user confirmation.
