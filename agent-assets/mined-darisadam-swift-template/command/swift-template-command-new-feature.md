---
description: Scaffold a new feature module following the project's architecture conventions.
argument-hint: <FeatureName>
---

Scaffold a new feature module named `$ARGUMENTS` following the architecture defined in `CLAUDE.md`.

Steps:
1. Read `CLAUDE.md` to confirm the architecture style (Simple MVVM, Modular MVVM, Clean+MVVM+Repository, or TCA).
2. Look at an existing feature module in this repo as a template. Copy its layout exactly — don't invent a new shape.
3. Create the new module's directory, sources, tests, and (if Tuist) `Project.swift` / (if XcodeGen) entry in `project.yml`.
4. Wire it into the app target's dependency list.
5. Regenerate the Xcode project (`tuist generate` or `xcodegen generate`).
6. Run `/verify` to confirm lint + tests pass.

Stop and ask if any of these steps are ambiguous — don't guess at module naming or routing conventions.
