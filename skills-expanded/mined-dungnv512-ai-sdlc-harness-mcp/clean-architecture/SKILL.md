---
name: clean-architecture
description: Layer boundaries and import rules for Flutter features (presentation -> domain <- data). MANDATORY TRIGGERS - "clean architecture", "layer", "boundary", "import rule", "domain layer", "use case", "repository pattern".
allowed-tools: Read, Grep, Glob, Edit
---

# Skill: clean-architecture

> **Layout note (2026-07-30).** This repo uses a Flutter local-package
> layout under `modules/`. Read `lib/features/<f>/` in the rules
> below as `modules/<name>/lib/src/<f>/` — the layer contract
> (`presentation → domain ← data`) is identical. Cross-feature
> imports go through the module barrel (`package:<name>/<name>.dart`)
> or `modules/core` — never reach into another package's `lib/src/`.
> See `CLAUDE.md` "Module boundary rules" for the current authority
> statement.

## When to use

Any time code crosses a layer boundary or a new file is created
under `modules/*/lib/src/<f>/` (or `lib/features/<f>/` on any legacy
subtree that still exists).

## Inputs

- feature slug
- proposed file path
- proposed imports

## Steps (decision flow)

1. Identify layer of the file:
   - path contains `/domain/`   -> Domain
   - path contains `/data/`     -> Data
   - path contains `/presentation/` -> Presentation
2. Allowed imports per layer:

   | layer        | may import                                       | must NOT import                  |
   | ------------ | ------------------------------------------------ | -------------------------------- |
   | domain       | `dartz`, `equatable`, project domain types       | flutter, dio, freezed UI, get_it |
   | data         | domain of same feature, dio, retrofit, freezed   | presentation, flutter            |
   | presentation | domain of same feature, flutter, flutter_bloc    | data of any feature              |

3. Cross-feature imports:
   - Same module → import via relative path within the module's
     `lib/src/`, or via the module's barrel
     (`package:<name>/<name>.dart`) when consumed from outside.
   - Cross-module → go through the target module's barrel only
     (`package:auth/auth.dart`, `package:stockbook_ui_component/…`);
     never reach into another package's `lib/src/`.
   - Shared code between two modules → move it into `modules/core`
     (never a direct feature-to-feature dependency) and open an ADR
     if the extraction is non-trivial.
4. Generated files (`*.g.dart`, `*.freezed.dart`) follow the same
   rules as their source.

## Output template

```
File:       <path>
Layer:      <domain|data|presentation>
Imports:    OK | violations:
              - <import> -> reason
Verdict:    ALLOW | BLOCK
```

## Examples

- `lib/features/feed/domain/usecase/get_feed.dart` importing
  `package:flutter/material.dart` -> **BLOCK** (domain has no Flutter).
- `lib/features/post/presentation/...` importing
  `lib/features/user/data/...` -> **BLOCK** (cross-feature + wrong layer).

## See also

- `bloc-pattern`, `flutter-feature-scaffold`
