---
name: "vue"
description: "Vue 3 patterns: Composition API, composables, Pinia state, Vue Router, async components, performance, TypeScript with Vue"
---

# Vue Skill

## When to activate
- Building Vue 3 components with the Composition API
- Writing composables to share reactive logic
- Setting up Pinia for state management
- Configuring Vue Router with navigation guards
- Using `<script setup>` syntax
- Optimising Vue component performance
- Using TypeScript with Vue 3

## When NOT to use
- Vue 2 / Options API projects — some patterns differ significantly
- React projects — use the React skill
- Nuxt.js-specific patterns (SSR, file-based routing) — note the differences where they apply

## Instructions

### Composition API with `<script setup>`

```vue
<!-- UserProfile.vue -->
<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'

// Props with TypeScript
const props = defineProps<{
  userId: string
  showActions?: boolean
}>()

// Emits
const emit = defineEmits<{
  (e: 'updated', user: User): void
  (e: 'deleted', userId: string): void
}>()

// Reactive state
const loading = ref(false)
const user = ref<User | null>(null)
const errorMessage = ref('')

// Computed
const fullName = computed(() =>
  user.value ? `${user.value.firstName} ${user.value.lastName}` : ''
)

// Watchers
watch(() => props.userId, async (newId) => {
  await loadUser(newId)
}, { immediate: true })

// Lifecycle
onMounted(() => {
  document.title = `User: ${props.userId}`
})

// Methods
async function loadUser(id: string) {
  loading.value = true
  try {
    user.value = await api.getUser(id)
  } catch (err) {
    errorMessage.value = 'Failed to load user'
  } finally {
    loading.value = false
  }
}

async function handleUpdate(data: Partial<User>) {
  const updated = await api.updateUser(props.userId, data)
  user.value = updated
  emit('updated', updated)
}
</script>

<template>
  <div v-if="loading" class="skeleton" />
  <div v-else-if="errorMessage" class="error">{{ errorMessage }}</div>
  <div v-else-if="user" class="profile">
    <h1>{{ fullName }}</h1>
    <button v-if="showActions" @click="handleUpdate({ active: !user.active })">
      {{ user.active ? 'Deactivate' : 'Activate' }}
    </button>
  </div>
</template>
```

### Composables — reusable reactive logic

```typescript
// composables/useAsync.ts
import { ref, type Ref } from 'vue'

export function useAsync<T>(fn: () => Promise<T>) {
  const data: Ref<T | null> = ref(null)
  const error = ref<Error | null>(null)
  const loading = ref(false)

  async function execute() {
    loading.value = true
    error.value = null
    try {
      data.value = await fn()
    } catch (err) {
      error.value = err instanceof Error ? err : new Error(String(err))
    } finally {
      loading.value = false
    }
  }

  return { data, error, loading, execute }
}

// composables/usePagination.ts
export function usePagination(fetchFn: (page: number) => Promise<PaginatedResult>) {
  const items = ref([])
  const page = ref(1)
  const hasMore = ref(true)
  const loading = ref(false)

  async function loadMore() {
    if (!hasMore.value || loading.value) return
    loading.value = true
    const result = await fetchFn(page.value)
    items.value.push(...result.data)
    hasMore.value = result.hasMore
    page.value++
    loading.value = false
  }

  return { items, hasMore, loading, loadMore }
}

// Usage
const { data: users, loading, execute: fetchUsers } = useAsync(() => api.getUsers())
onMounted(fetchUsers)
```

### Pinia — state management

```typescript
// stores/user.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

// Setup store (Composition API style — recommended)
export const useUserStore = defineStore('user', () => {
  // State
  const currentUser = ref<User | null>(null)
  const isLoading = ref(false)

  // Getters (computed)
  const isAuthenticated = computed(() => currentUser.value !== null)
  const displayName = computed(() =>
    currentUser.value?.name ?? currentUser.value?.email ?? 'Guest'
  )

  // Actions
  async function login(email: string, password: string) {
    isLoading.value = true
    try {
      currentUser.value = await api.login(email, password)
    } finally {
      isLoading.value = false
    }
  }

  async function logout() {
    await api.logout()
    currentUser.value = null
  }

  return { currentUser, isLoading, isAuthenticated, displayName, login, logout }
}, {
  persist: true,  // pinia-plugin-persistedstate: persist to localStorage
})

// Usage in component
const userStore = useUserStore()
const { isAuthenticated, displayName } = storeToRefs(userStore)  // reactive refs
await userStore.login(email, password)
```

### Vue Router — navigation and guards

```typescript
// router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: () => import('@/views/HomeView.vue'),  // lazy load
    },
    {
      path: '/dashboard',
      component: () => import('@/views/DashboardView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/admin',
      component: () => import('@/views/AdminView.vue'),
      meta: { requiresAuth: true, roles: ['admin'] },
    },
  ],
})

// Global navigation guard
router.beforeEach((to, from) => {
  const store = useUserStore()

  if (to.meta.requiresAuth && !store.isAuthenticated) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  if (to.meta.roles && !to.meta.roles.includes(store.currentUser?.role)) {
    return { name: 'forbidden' }
  }
})

export default router
```

### Async components and Suspense

```vue
<!-- Load heavy components lazily -->
<script setup>
import { defineAsyncComponent } from 'vue'

const HeavyChart = defineAsyncComponent({
  loader: () => import('./HeavyChart.vue'),
  loadingComponent: ChartSkeleton,
  errorComponent: ErrorDisplay,
  delay: 200,      // show loading only if takes > 200ms
  timeout: 10000,  // error if takes > 10s
})
</script>

<template>
  <Suspense>
    <template #default>
      <HeavyChart :data="chartData" />
    </template>
    <template #fallback>
      <div class="skeleton" />
    </template>
  </Suspense>
</template>
```

### Performance patterns

```vue
<script setup>
import { shallowRef, markRaw } from 'vue'

// shallowRef — don't deeply track large objects
const bigDataset = shallowRef<Row[]>([])

// markRaw — opt out of reactivity for non-reactive objects (class instances, etc.)
const chartInstance = markRaw(new ChartLibrary())

// v-memo — skip re-render if value hasn't changed
// Useful in long lists where some items don't change
</script>

<template>
  <!-- v-once: render once, never update -->
  <StaticHeader v-once />

  <!-- v-memo: re-render only when selected changes -->
  <div v-for="item in list" :key="item.id" v-memo="[item.selected]">
    {{ item.name }} {{ item.selected ? '✓' : '' }}
  </div>
</template>
```

### TypeScript integration

```typescript
// types/index.ts — declare component prop types globally
export interface User {
  id: string
  email: string
  name: string
  role: 'user' | 'admin'
}

// Component with generic props
// UserList.vue
<script setup lang="ts" generic="T extends { id: string }">
const props = defineProps<{
  items: T[]
  selected?: T
}>()
const emit = defineEmits<{ select: [item: T] }>()
</script>

// Provide/Inject with types
// Parent
const key = Symbol() as InjectionKey<UserService>
provide(key, userService)

// Child
const userService = inject(key)  // typed as UserService | undefined
```

### Common template patterns

```vue
<template>
  <!-- v-model shorthand -->
  <input v-model="searchQuery" />
  <!-- equivalent to: :value="searchQuery" @input="searchQuery = $event.target.value" -->

  <!-- v-model modifiers -->
  <input v-model.trim="name" />       <!-- auto-trim whitespace -->
  <input v-model.number="age" />      <!-- auto-convert to number -->
  <input v-model.lazy="email" />      <!-- update on blur, not every keystroke -->

  <!-- Dynamic component -->
  <component :is="currentView" v-bind="viewProps" />

  <!-- Slots with scoped data -->
  <DataTable :rows="users">
    <template #cell-name="{ row }">
      <a :href="`/users/${row.id}`">{{ row.name }}</a>
    </template>
  </DataTable>
</template>
```

## Example

**User:** Build a paginated product list page with search, category filter, and a cart stored in Pinia — selected products survive a page refresh.

**Expected output:**
- `stores/cart.ts` — Pinia setup store with `persist: true`, `addItem`, `removeItem`, `total` getter
- `composables/useProducts.ts` — `useAsync` + `usePagination` composable
- `views/ProductsView.vue` — `<script setup>`, search/filter state, product grid, load-more
- `components/ProductCard.vue` — emits `add-to-cart`, receives product prop with type
- Vue Router route with `meta: { title: 'Products' }` and a navigation guard setting `document.title`

---
