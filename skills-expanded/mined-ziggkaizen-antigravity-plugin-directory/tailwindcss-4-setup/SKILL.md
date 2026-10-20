---
name: tailwindcss-4-setup
description: Helps agents install, configure, verify, and migrate Tailwind CSS 4 projects. Use when adding Tailwind CSS, choosing Vite/PostCSS/CLI integration, or migrating from Tailwind CSS 3 to 4.
license: MIT
---

# Tailwind CSS 4 Setup Skill

Use this skill for Tailwind CSS 4 installation, integration selection, initial configuration, and v3-to-v4 migration work.

## When to Use

- The user asks to add Tailwind CSS 4.
- A project needs Vite, PostCSS, framework, or CLI integration guidance.
- A Tailwind CSS 3 project is being upgraded to Tailwind CSS 4.
- Tailwind CSS 4 installation appears broken or incomplete.

## Decision Tree

1. Inspect the project.
   - Read `package.json`.
   - Identify Vite, PostCSS, framework, or no bundler.
   - Locate CSS entrypoints and imported stylesheets.
   - Check for `tailwind.config.*`, `postcss.config.*`, `vite.config.*`, and lockfiles.
2. Choose one integration path.
   - Vite project: prefer `@tailwindcss/vite`.
   - PostCSS-driven project: prefer `@tailwindcss/postcss`.
   - No bundler or static HTML: prefer `@tailwindcss/cli`.
3. Add only the dependencies required for that path.
4. Add or update the CSS entrypoint with `@import "tailwindcss";`.
5. Verify the build and inspect rendered UI behavior.
6. For migration tasks, use the migration checklist before deleting legacy files.

## Workflows

- `workflows/install-tailwindcss-4-workflow.md`: use when adding Tailwind CSS 4 to a project.
- `workflows/migrate-from-tailwindcss-3-workflow.md`: use when moving an existing Tailwind CSS 3 project to Tailwind CSS 4.

## Resources

- `resources/integration-decision-matrix.md`: choose Vite, PostCSS, or CLI.
- `resources/migration-checklist.md`: migration safety checklist.

## Examples

- `examples/vite-app-css.example.md`: CSS entrypoint example for Vite-style projects.
- `examples/postcss-config.example.md`: PostCSS plugin configuration example.

## Operating Guidance

- Do not add `tailwind.config.js` as a default setup step.
- Do not use Tailwind CSS 3 instructions for a Tailwind CSS 4 project.
- Do not remove legacy config until its purpose has been understood.
- Prefer minimal, reversible changes.
- After editing, run the project’s existing format, lint, build, or test command when available.
