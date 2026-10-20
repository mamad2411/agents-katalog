---
applyTo: "**/*.vue,**/*.tsx,**/*.jsx"
---
# Vue 3 + Tailwind Frontend Conventions

ALWAYS use Vue 3 Composition API with `<script setup>`.
NEVER use Options API in new components.
ALWAYS use Tailwind CSS utility classes — no custom CSS unless absolutely necessary.
ALWAYS extract reusable UI into composables (`use*.ts`) or components.
NEVER put business logic in components — extract to composables or services.
ALWAYS use TypeScript with strict mode.
NEVER use `any` types — use `unknown` with Zod validation at boundaries.
ALWAYS co-locate component tests alongside components.
CRITICAL: Components MUST be < 100 lines. Extract when larger.
