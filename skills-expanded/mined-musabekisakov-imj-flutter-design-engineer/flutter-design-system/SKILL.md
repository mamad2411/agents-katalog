---
name: flutter-design-system
description: Create, extend, or repair semantic Flutter design systems covering tokens, themes, typography, color, spacing, geometry, motion, and component contracts. Use for ThemeData work, design-token extraction, dark mode, component standardization, UI consistency, or migration away from scattered visual constants.
---

# Flutter Design System

Build a semantic system that serves the product; do not impose a generic component library.

## Process

1. Inventory existing `ThemeData`, extensions, constants, text styles, colors, radii, spacing, shared widgets, and package dependencies.
2. Identify visual language and product constraints. Read `references/visual-direction.md`, `references/typography-and-color.md`, and `references/layout-and-density.md`.
3. Define semantic roles before values:
   - surfaces, content, borders, accents, status, and interaction states;
   - display, title, body, label, and numeric typography roles;
   - spacing, radius, elevation, icon size, control height, and motion roles.
   For products spanning multiple domains, read `references/connected-product-workflows.md`; give domains semantic accents without fragmenting the shared system.
4. Map roles into `ColorScheme`, `TextTheme`, component themes, and narrowly scoped `ThemeExtension`s.
5. Support light/dark contrast and platform behavior without duplicating raw values throughout widgets.
6. Define component contracts for behavior and states, not only appearance.
7. Migrate incrementally. Avoid replacing mature project primitives unless the new system resolves a documented issue.

## Rules

- Prefer semantic names such as `surfaceRaised` over color names such as `gray100` in widget code.
- Keep domain meaning out of universal primitives when a local component is clearer.
- Avoid excessive token granularity that makes ordinary UI changes require system archaeology.
- Test text scaling, RTL, disabled/error states, and theme transitions.
- Keep package APIs stable when modifying a library.

Use starter assets in `assets/starter/` as adaptation examples, not mandatory architecture.

## Deliver

Document token decisions, migration boundaries, component contracts, theme coverage, and verification performed. State intentional exceptions.
