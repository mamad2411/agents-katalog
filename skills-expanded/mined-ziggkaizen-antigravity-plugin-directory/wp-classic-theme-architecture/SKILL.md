---
name: wp-classic-theme-architecture
description: Plans WordPress classic and hybrid theme architecture, classifies theme type, separates presentation from plugin responsibilities, and defines a maintainable file structure. Use when starting or restructuring a PHP-template theme.
license: MIT
compatibility: "General classic/hybrid theme guidance; checked against WordPress 7.0.1 documentation."
---

# WordPress Classic Theme Architecture

Use this skill to make architecture decisions before writing theme code.

## Use this skill when

- Starting a standalone classic theme.
- Converting an unstructured theme into a maintainable architecture.
- Deciding whether selected block-era features belong in a classic theme.
- Deciding whether functionality belongs in the theme or a plugin.
- Planning a child theme, before loading the child-theme skill for implementation detail.

## Approach

1. Confirm exact WordPress, PHP, distribution, and browser requirements.
2. Classify the theme using the decision matrix.
3. Define presentation responsibilities and plugin boundaries.
4. Map required template hierarchy coverage.
5. Choose a minimal, navigable directory structure.
6. Decide whether `theme.json`, block styles, patterns, or editor assets add clear value.
7. Define quality gates before implementation.

## Workflow

Use [classic-theme-planning-workflow.md](workflows/classic-theme-planning-workflow.md).

## Resources

- [classic-hybrid-decision-matrix.md](resources/classic-hybrid-decision-matrix.md)
- [theme-vs-plugin-boundary.md](resources/theme-vs-plugin-boundary.md)
- [theme-structure-reference.md](resources/theme-structure-reference.md)

## Output

Return:

- Theme classification and rationale.
- Compatibility baseline.
- Responsibility boundary.
- Proposed file tree.
- Required templates and features.
- Testing and release gates.
- Explicit out-of-scope items.
