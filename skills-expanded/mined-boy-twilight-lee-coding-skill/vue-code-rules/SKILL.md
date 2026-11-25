---
name: vue-code-rules
description: "Apply mandatory Vue 3 SFC and component-architecture rules when editing or reviewing Vue components, composables, pages, or layouts."
---

# Vue Code Rules

These rules are mandatory for changed or reviewed Vue code; existing code does not waive them. Fix directly affected violations without migrating unrelated components. Higher-priority instructions prevail; project overrides apply only where a rule permits them. Report unavoidable conflicts and keep deviations minimal.

## Core Rules

1. Keep present SFC blocks in `<template>`, `<script>`, `<style>` order and omit empty blocks. Use kebab-case custom tags, and self-close components without content.
2. Use the minimum necessary DOM and nesting; add wrappers only when existing elements cannot meet the required behavior or layout. Prefer common tags such as `div`, `span`, `i`, `button`, and `input`; keep native controls for their behavior. Prohibit uncommon tags, landmark/sectioning containers, and invented tags. Do not add unrelated accessibility attributes unless the user explicitly requests accessibility compatibility.
3. Order each tag's attributes as directives, bindings, literal text, plain booleans, then events. `v-if` and `v-show` share highest priority; alternative-branch directives share that leading group. Bound booleans and dynamic class/style stay with bindings. Preserve meaningful within-group order, spread overrides, event behavior, and conditional sibling adjacency; do not reorder child nodes.
4. Combine multiple class sources in one `:class` array. Do not split the same element across `class` and `:class` or build long concatenated class strings.
5. Own blank-line decisions only inside `<template>`: separate genuinely independent regions with at most one blank line and keep tightly coupled nodes contiguous. Read `ts-code-rules`' Blank Lines reference for all script blocks, TypeScript/TSX, and top-level SFC separators; `css-code-rules` owns style blocks and stylesheets.
6. Verify active Vite auto-import configuration before adding Vue or Vue Router imports. Omit explicit imports for covered runtime APIs; import uncovered APIs or APIs whose coverage cannot be verified.
7. Keep compiler macros at `<script setup>` scope, immediately after imports and before runtime logic; place `defineModel` after `defineSlots` when both are used. Receive `defineProps`, `defineEmits`, and `defineSlots` as `props`, `emits`, and `slots`, respectively. `defineExpose` goes last, except that top-level `await` requires initialized public bindings to be exposed before the first await.
8. For both JavaScript and TypeScript scripts, read and apply `ts-code-rules`' Business Comments reference for generic comment rules. Vue owns only these special rules: put watcher/lifecycle responsibility comments above registrations; keep compiler-macro interiors comment-free and omit generic macro labels; document existing standalone contracts outside macros. Do not add comments in templates.
9. Use kebab-case component files, directories, and tags. Follow the fixed owner structure: `index.vue`, `index.ts`, and only needed `component/`, `constants/`, `hooks/`, `type/`, plus `index.less` (or its existing-language equivalent) or a multi-file `style/`, never both. First-level units require directories; only simple private children may stay single files. Extracted child styles require directory form. Prohibit unrelated directories and loose helper files. Keep private functional helpers in hooks and shared stateless utilities in project utils. `index.ts` only forwards the default component and externally needed components, methods, modules, or types, including named instance types when needed.
10. Keep each `.vue` at or below 1000 lines. Consider cohesive children for complex templates and responsibility-focused hooks for large scripts; extract styles under `css-code-rules`. Avoid arbitrary line slicing. Preserve state/lifecycle ownership, component contracts, and style scope, and update public entries, consumers, and component discovery.
11. Every `provide`/`inject` scenario must follow the complete fixed context pattern, regardless of depth or value count. The owner-scoped `use**Context` facade returns only `provide()` and `inject()`. Keep business initialization in a private `create**Context` function called only by `provide()`, provide and return the same complete context object, and inject without a default value; throw when no provider exists. Infer TypeScript context types from the factory with `ReturnType`. Each owner provides once; descendants inject.
12. In templates, access declared props by their bare names. Prohibit `props.xxx` unless that specific prop name conflicts with a variable defined in the script; use `props.xxx` only for the conflicting prop. Keep script-side prop access and the required `props` macro receiver unchanged.

## Required Reference Loading

After repository inspection and before implementation or review decisions, open and fully read every matching reference, including uncertain matches. Every task must read at least one; if none matches, read the closest. Each rule owns one reference. References are mandatory; mentioning or summarizing them does not replace reading them.

- Rule 1: Read [Template Examples](references/template-examples.md) when deciding SFC block order, component tags, or slots.
- Rule 2: Read [DOM Structure Examples](references/dom-structure-examples.md) for DOM depth, tag restrictions, wrappers, or accessibility-attribute scope.
- Rule 3: Read [Template Attribute Order Examples](references/template-attribute-order-examples.md) for directive/attribute/event ordering or spread overrides.
- Rule 4: Read [Class Binding Examples](references/class-binding-examples.md) when combining class sources.
- Rule 5: Read [Template Blank Lines](references/blank-line-examples.md) for whitespace inside templates; for scripts, top-level SFC separators, or styles, fully read the canonical reference linked there instead.
- Rule 6: Read [Auto-Import Examples](references/auto-import-examples.md) for Vue/Router imports and active Vite coverage.
- Rule 7: Read [Compiler Macro Examples](references/compiler-macro-examples.md) for macro placement or exposure around top-level await.
- Rule 8: Read [Vue-Specific Comment Rules](references/script-comment-examples.md) and its linked shared Business Comments reference for script comments, watcher/lifecycle placement, macro exceptions, or the prohibition on adding template comments.
- Rule 9: Read [Component Structure Examples](references/component-structure-examples.md) for names, allowed directories, helper/style placement, public entries, or instance types.
- Rule 10: Read [Component Decomposition Examples](references/component-decomposition-examples.md) for file-size limits, split decisions, or post-split checks.
- Rule 11: Read [Provide/Inject Context Pattern](references/complex-component-context-examples.md) for every provide/inject implementation or review; follow its complete fixed example.
- Rule 12: Read [Template Prop Access Examples](references/template-prop-access-examples.md) for template prop access, bare prop names, or script-variable name conflicts.

## Working Process

1. Inspect repository instructions, affected and related components, and active build, auto-import, lint, formatter, and TypeScript configuration.

2. Apply `ts-code-rules` to TypeScript scripts and `css-code-rules` to styles. All JavaScript and TypeScript script blank lines and top-level SFC separators follow the shared TS Blank Lines reference; JavaScript also reuses its Business Comments reference without activating unrelated TypeScript rules. Vue's own blank-line rule applies only inside templates.

3. Check changed lines against applicable rules and reference checklists. Run targeted formatter, lint, Vue type-check, or tests without rewriting unrelated files. Report unmet rules and unavailable or failed checks; formatting or visual inspection alone does not prove correctness.
