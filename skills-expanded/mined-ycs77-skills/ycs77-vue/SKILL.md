---
name: ycs77-vue
description: Lucas Yang's opinionated Vue 3 conventions for SFC block order, inline props/emits types, reactive form state, complex ref type assertions, same-name bindings, and template props access.
metadata:
  author: Lucas Yang
  version: "2026.10.08"
---

# Lucas Yang's Vue Conventions

Opinionated Vue 3 and TypeScript patterns emphasizing minimal boilerplate, readability, and practical simplicity for real-world projects.

## TypeScript Formatting

**Standard**: 2 spaces, single quotes, no semicolons, trailing commas.

## Vue SFC Patterns

### 1. SFC Block Order

Always place `<template>` before `<script setup lang="ts">` in Single File Components. This follows the natural reading flow from structure (what to render) to behavior (how it works).

**Good:**
```vue
<template>
  <div class="container">
    <h1>{{ title }}</h1>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const title = ref('Hello World')
</script>
```

### 2. Inline Props/Emits Types

Prefer inline types in `defineProps` and `defineEmits` so the component API is visible at the call site.

**Good:**
```vue
<script setup lang="ts">
const props = defineProps<{
  title: string
  count?: number
  items: {
    id: string
    name: string
  }[]
}>()

const emit = defineEmits<{
  update: [value: string]
  delete: [id: string]
}>()
</script>
```

**Exception**: Only extract to a separate interface when the type is reused across multiple components or needs to be exported.

### 3. Use reactive() for Form State

When managing form state, prefer using `reactive()` to create a single reactive object that holds all form fields. This approach simplifies state management and reduces boilerplate code compared to using multiple `ref()` calls for each field.

**Good:**
```vue
<template>
  <form @submit.prevent="handleSubmit">
    <input v-model="form.email" type="email">
    <input v-model="form.password" type="password">
    <input v-model="form.rememberMe" type="checkbox">
  </form>
</template>

<script setup lang="ts">
import { reactive } from 'vue'

const form = reactive({
  email: '',
  password: '',
  rememberMe: false,
})

function handleSubmit() {
  console.log(form) // Clean object or reactive object, easy to submit
}

function resetForm() {
  form.email = ''
  form.password = ''
  form.rememberMe = false
}
</script>
```

**Rationale**: Grouping related state reduces `.value` boilerplate and makes form submission cleaner. Use individual `ref()` only for truly independent state.

### 4. Use Type Assertion for ref() with Complex Types

For interface or complex object types, prefer `ref(value) as Ref<Type>` over `ref<Type>(value)` to avoid type conflicts from Vue's deep unwrapping. Make sure the value satisfies the asserted type. For primitive and enum types, use `ref<Type>()`.

Prefer `null` over `undefined` for an absent object.

**Good:**
```vue
<script setup lang="ts">
import type { Ref } from 'vue'
import { ref } from 'vue'

interface User {
  id: number
  name: string
}

enum Status {
  Pending = 'pending',
}

// Complex type - use type assertion
const user = ref({ id: 1, name: 'Lucas' }) as Ref<User>
const users = ref([]) as Ref<User[]>
const isSelectedUser = ref(null) as Ref<User | null>

// Primitive types - generic parameter is fine
const count = ref<number>(0)
const isActive = ref<boolean>(false)
const status = ref<Status>(Status.Pending)
</script>
```

**Avoid:**
```vue
<script setup lang="ts">
import type { User } from '@/types'
import { ref } from 'vue'

// May cause: Type '...' is not assignable to type 'Ref<User>'
const user = ref<User>()
</script>
```

### 5. Use Same-name Shorthand for Bindings

Use same-name shorthand for matching bindings in Vue 3.4+.

**Good:**
```vue
<template>
  <div :id :title>
    <MyComponent :user-name :count :is-active />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const id = ref('app')
const title = ref('Dashboard')
const userName = ref('Lucas')
const count = ref(42)
const isActive = ref(true)
</script>
```

**Rationale**: `:user-name` matches `userName` (kebab-case to camelCase). If a binding needs explicit `props.` access (Section 6), use its full form.

### 6. Access Props Directly in Templates

Props declared with `defineProps` are available by name in `<template>`. Prefer `{{ title }}` to `{{ props.title }}` when unambiguous. Use `props.name` when a local binding shadows a prop. For syntax-sensitive names such as `class` (a JavaScript reserved word) and `as` (used in TypeScript type assertions), access the props explicitly: `props.class` and `props.as`. Bare `class` cannot be used as an expression for `:class` shorthand; `:is="as"` leaves the source of `as` implicit.

**Good:**
```vue
<template>
  <div :class="props.class">
    <h1>{{ title }}</h1>
    <component :is="props.as">content</component>
  </div>
</template>

<script setup lang="ts">
import type { HTMLAttributes } from 'vue'

const props = defineProps<{
  title: string
  as: string
  class?: HTMLAttributes['class']
}>()
</script>
```

**Avoid:**
```vue
<div :class>
  <component :is="as">content</component>
</div>
```

