---
name: framework-expertise
description: Framework- and architecture-specific implementation guidance. Use when building or reviewing code in a known stack (Laravel, Filament, Vue, React, Next, Electron, Ionic, shadcn, Tailwind) or when choosing between microservice and monolithic architectures. A router — load only the reference file(s) matching the detected stack.
---

# Framework Expertise (router)

Use stack-detection first, then load only the matching reference(s). Wave 1 ships an initial set; more references are added in later waves.

- Laravel / Filament → `references/laravel.md`
- Vue / shadcn-vue / Tailwind → `references/vue.md`
- Microservice vs monolithic → `references/architecture-styles.md`

If no reference matches the detected stack, apply general best practices from solid-principles + clean-code-standards and follow the repo's existing conventions.
