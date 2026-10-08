---
name: flutter-forge
description: Generate production-ready Flutter screens with Riverpod, Freezed, GoRouter, and enterprise standards
category: software-development
triggers:
  - "create flutter screen"
  - "build flutter widget"
  - "generate dart"
---

# Flutter Screen Generation

Generate complete Flutter features following enterprise patterns.

## Instructions

1. Read `agents/flutter-forge.md` for the full Flutter code generation workflow
2. Riverpod for all server state — no setState for API data
3. Freezed for all data models. GoRouter for typed routing. Dio for HTTP
4. Data fetching at the leaf level — each widget watches its own provider
5. Reuse existing widgets — search codebase first, refactor god widgets
6. Always include: Model + Repository + Provider + Screen + Widgets + Tests
7. const constructors wherever possible. SafeArea wrapping screens
8. Handle loading (shimmer), error (retry), empty states on every screen
