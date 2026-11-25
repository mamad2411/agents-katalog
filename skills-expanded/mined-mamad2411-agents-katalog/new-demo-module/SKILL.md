---
name: new-demo-module
description: Scaffold a compact module-style demo boundary aligned with this repo's modular layout
argument-hint: <ModuleName>
---

# New Demo Module

Create a compact module-style boundary for **$0**.

## Workflow Gate

Before editing files:

1. inspect the existing shared-layer and module structure
2. present a concise implementation plan
3. ask one combined approval question, for example: `If you approve the plan, I'll create a local safety commit first and proceed with the implementation.`
4. treat `go` or `do it` as approval plus a local safety commit
5. if the user explicitly says to continue without the commit, skip the commit
6. if the reply is unclear, ask again before editing files

If the user later asks to push to Git:

1. prepare one compact final commit text
2. show that text to the user and ask for approval
3. after approval, squash local commits into one commit and use the approved text

If a helper script is useful for analysis or structure checks, place it under `.artifacts/codex-scripts/` so it stays out of Git and can be reused later.

## Target Layout

```text
src/Modules/$0/
  $0/
    Domain/
    Application/
    DependencyInjection.cs
    $0.csproj
  $0.Infrastructure/
    Persistence/
    DependencyInjection.cs
    $0.Infrastructure.csproj

src/Web.App/Pages/Modules/$0/
```

## Rules

- follow the compact module layout from `.codex/rules/modules.md`
- keep layer dependencies inward
- if the module is still too small to justify dedicated projects, stop and keep the feature in the shared layers instead
- if you add dedicated projects, register them from `Web.App`

## Minimum Checks

1. Build the solution.
2. Run architecture tests.
3. Confirm the new module folder does not bypass the shared-layer dependency flow.
