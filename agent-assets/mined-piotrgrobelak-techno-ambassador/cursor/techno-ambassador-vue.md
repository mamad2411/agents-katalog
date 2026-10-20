---
description: 
globs: *.vue
alwaysApply: false
---

## FRONTEND

### Guidelines for VUE

#### VUE_CODING_STANDARDS

- Use the Composition API instead of the Options API for better type inference and code reuse
- Implement <script setup lang="ts"> for more concise component definitions
- Use `Suspense` and async components for handling loading states during code-splitting
- Use `defineModel` in child components to simplify two-way binding with parent state.
- Leverage the `defineProps` and defineEmits macros for type-safe props and events
- Use the new `defineOptions` for additional component options
- Implement `provide`/`inject` for dependency injection instead of prop drilling in deeply nested components
- Use the Teleport component for portal-like functionality to render UI elsewhere in the DOM
- Leverage ref over reactive for primitive values to avoid unintended unwrapping
- Use `v-memo` for performance optimization in render-heavy list rendering scenarios
- Implement shallow refs for large objects that don't need deep reactivity
- Use `useTemplateRef` instead of the default `ref` to get a component reference.
- Always use `computed` properties instead of method calls in <template></template> for data transformations and filtering
- Add comments only in template sections to divide the code into logical sections if necessary.

#### PRIMEVUE_STYLING_RULES

- Choose a styling mode and apply it consistently across the project:
  - **Styled mode:** Use PrimeVue's built-in themes (e.g., Aura, Lara, Nora).
  - **Unstyled mode:** Apply your own styles using CSS frameworks like Tailwind CSS or Bootstrap, leveraging PrimeVue's unstyled components.
- Use the `p-` prefix for CSS classes to maintain consistency with PrimeVue conventions.
- Utilize PrimeVue's PassThrough API to add attributes, event listeners, and ARIA properties to internal DOM elements without modifying component source code.
- Use PassThrough for adding test IDs, accessibility attributes, or custom event handlers.
- Ensure all components comply with WCAG 2.1 AA standards.
- Add appropriate ARIA attributes and roles, especially for dynamic components.
- Leverage PrimeVue's built-in keyboard navigation and screen reader support.
- Use PrimeVue components as documented, e.g., `<p-button>`, `<p-inputText>`, `<Tag>`, with proper props like `severity`, `rounded`, and `icon`.
- Avoid direct DOM manipulation of PrimeVue components; always use their API or PassThrough.
- Organize PrimeVue components in dedicated folders such as `src/components/primevue/`.
- Use TypeScript for type safety and better integration with PrimeVue's typings.
- If using Tailwind CSS, incorporate PrimeVue's Tailwind presets to streamline styling with utility classes.
- Ensure consistent styling approach across all components.
