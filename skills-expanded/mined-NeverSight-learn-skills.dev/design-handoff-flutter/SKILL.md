---
name: design-handoff-flutter
description: Implements Flutter screens from designer screenshots and handoff notes using Material 3. Two-pass workflow — mockup-brief with Implementation spec, then AppShell + route screens. Use when approved mockups exist for a HeyEddi Flutter app.
disable-model-invocation: true
paths:
  - "lib/**"
  - ".heyeddi/designs/**"
  - "pubspec.yaml"
---

# Design Handoff — Flutter

**Designer then implementer** — Material 3 + go_router (not PrimeVue).

## When to use

- Flutter project (`@flutter-engineering` scaffolded)
- `.heyeddi/designs/<feature>/` has reference images
- Implementing settings/dashboard from PNG or wireframe

## Instructions

### Pass 1 — Designer

1. `python scripts/load_handoff.py --route <route> --project-root <root>`
2. Write `mockup-brief.md` with **Implementation spec** (widgets: `Card`, `NavigationDrawer`, `FilledButton`, spacing in dp).
3. `python scripts/describe_handoff.py --route <route> --sync-design`

### Pass 2 — Implementer

4. Read `reference/material-handoff.md` + Implementation spec.
5. Update `lib/theme/app_theme.dart` from spec.
6. Build `lib/widgets/app_shell.dart` (drawer + scaffold).
7. `python scripts/verify_handoff.py --route <route> --phase shell --check`
8. `python scripts/verify_tokens.py --check` + `python scripts/verify_theme.py --check`
9. Build `lib/screens/<feature>_screen.dart`.
10. `python scripts/verify_handoff.py --route <route> --phase full --check`
11. Chain `@visual-auditor` with `FLUTTER_WEB_URL=http://127.0.0.1:8085`

## References

- `reference/material-handoff.md` — Card padding, theme, navigation patterns
