---
name: vue-frontend-patterns
description: Write Vue.js code following best practices, component patterns, composables, and Vue 3 patterns. Use when writing Vue components, creating composables, setting up Pinia stores, or when the user asks about Vue, components, composables, or frontend patterns.
---

# Vue.js Frontend Patterns & Best Practices

Write maintainable, performant Vue.js applications following best practices and modern patterns.

## Component Patterns

### Component Structure

```vue
<template>
  <div class="user-card">
    <h3>{{ user.name }}</h3>
    <p>{{ user.email }}</p>
    <button @click="handleEdit">Edit</button>
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from "vue";

interface User {
  id: number;
  name: string;
  email: string;
}

interface Props {
  user: User;
}

const props = defineProps<Props>();

const emit = defineEmits<{
  edit: [id: number];
}>();

function handleEdit() {
  emit("edit", props.user.id);
}
</script>

<style scoped>
.user-card {
  padding: 1rem;
  border: 1px solid #ccc;
}
</style>
```

### Composition API Best Practices

```vue
<script setup lang="ts">
import { ref, computed, watch, onMounted } from "vue";
import { useUserStore } from "@/stores/user";

// Props and emits
const props = defineProps<{
  userId: number;
}>();

const emit = defineEmits<{
  updated: [user: User];
}>();

// Reactive state
const loading = ref(false);
const error = ref<string | null>(null);

// Stores
const userStore = useUserStore();

// Computed properties
const user = computed(() => userStore.getUserById(props.userId));
const isAdmin = computed(() => user.value?.role === "admin");

// Methods
async function fetchUser() {
  loading.value = true;
  error.value = null;
  try {
    await userStore.fetchUser(props.userId);
  } catch (err) {
    error.value = err instanceof Error ? err.message : "Failed to fetch user";
  } finally {
    loading.value = false;
  }
}

// Watchers
watch(
  () => props.userId,
  (newId) => {
    if (newId) {
      fetchUser();
    }
  },
  { immediate: true },
);

// Lifecycle
onMounted(() => {
  fetchUser();
});
</script>
```

## Composables Pattern

### Creating Reusable Composables

```typescript
// composables/useApi.ts
import { ref, Ref } from "vue";

interface UseApiOptions<T> {
  immediate?: boolean;
  onSuccess?: (data: T) => void;
  onError?: (error: Error) => void;
}

export function useApi<T>(
  apiCall: () => Promise<T>,
  options: UseApiOptions<T> = {},
) {
  const data: Ref<T | null> = ref(null);
  const loading = ref(false);
  const error: Ref<Error | null> = ref(null);

  async function execute() {
    loading.value = true;
    error.value = null;
    try {
      const result = await apiCall();
      data.value = result;
      options.onSuccess?.(result);
      return result;
    } catch (err) {
      const errorObj = err instanceof Error ? err : new Error("Unknown error");
      error.value = errorObj;
      options.onError?.(errorObj);
      throw errorObj;
    } finally {
      loading.value = false;
    }
  }

  if (options.immediate) {
    execute();
  }

  return {
    data,
    loading,
    error,
    execute,
  };
}

// Usage
const {
  data: users,
  loading,
  error,
  execute: fetchUsers,
} = useApi(() => api.getUsers(), { immediate: true });
```

### Common Composables

```typescript
// composables/useDebounce.ts
import { ref, Ref } from "vue";

export function useDebounce<T>(value: Ref<T>, delay = 300) {
  const debouncedValue = ref(value.value) as Ref<T>;

  let timeoutId: ReturnType<typeof setTimeout>;

  watch(value, (newValue) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => {
      debouncedValue.value = newValue;
    }, delay);
  });

  return debouncedValue;
}

// composables/useLocalStorage.ts
import { ref, watch } from "vue";

export function useLocalStorage<T>(key: string, defaultValue: T) {
  const storedValue = localStorage.getItem(key);
  const value = ref<T>(storedValue ? JSON.parse(storedValue) : defaultValue);

  watch(
    value,
    (newValue) => {
      localStorage.setItem(key, JSON.stringify(newValue));
    },
    { deep: true },
  );

  return value;
}
```

## Pinia Store Patterns

### Store Structure

```typescript
// stores/user.ts
import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { User } from "@/types/user";
import { userApi } from "@/api/user";

export const useUserStore = defineStore("user", () => {
  // State
  const users = ref<User[]>([]);
  const currentUser = ref<User | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);

  // Getters
  const activeUsers = computed(() =>
    users.value.filter((user) => user.status === "active"),
  );

  const getUserById = computed(
    () => (id: number) => users.value.find((user) => user.id === id),
  );

  // Actions
  async function fetchUsers() {
    loading.value = true;
    error.value = null;
    try {
      users.value = await userApi.getUsers();
    } catch (err) {
      error.value =
        err instanceof Error ? err.message : "Failed to fetch users";
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function createUser(userData: CreateUserData) {
    loading.value = true;
    try {
      const newUser = await userApi.createUser(userData);
      users.value.push(newUser);
      return newUser;
    } catch (err) {
      error.value =
        err instanceof Error ? err.message : "Failed to create user";
      throw err;
    } finally {
      loading.value = false;
    }
  }

  function setCurrentUser(user: User | null) {
    currentUser.value = user;
  }

  return {
    // State
    users,
    currentUser,
    loading,
    error,
    // Getters
    activeUsers,
    getUserById,
    // Actions
    fetchUsers,
    createUser,
    setCurrentUser,
  };
});
```

### Store Persistence

```typescript
// stores/user.ts with persistence
import { defineStore } from "pinia";
import { piniaPersistedState } from "pinia-plugin-persistedstate";

export const useUserStore = defineStore(
  "user",
  () => {
    const currentUser = ref<User | null>(null);
    const preferences = ref<UserPreferences>({});

    return {
      currentUser,
      preferences,
    };
  },
  {
    persist: {
      key: "user-store",
      storage: localStorage,
      paths: ["currentUser", "preferences"], // Only persist specific paths
    },
  },
);
```

## Vue Router Patterns

### Route Guards

```typescript
// router/guards.ts
import { RouteLocationNormalized, NavigationGuardNext } from "vue-router";
import { useAuthStore } from "@/stores/auth";

export function requireAuth(
  to: RouteLocationNormalized,
  from: RouteLocationNormalized,
  next: NavigationGuardNext,
) {
  const authStore = useAuthStore();

  if (!authStore.isAuthenticated) {
    next({ name: "login", query: { redirect: to.fullPath } });
  } else {
    next();
  }
}

export function requireRole(role: string) {
  return (
    to: RouteLocationNormalized,
    from: RouteLocationNormalized,
    next: NavigationGuardNext,
  ) => {
    const authStore = useAuthStore();

    if (!authStore.hasRole(role)) {
      next({ name: "forbidden" });
    } else {
      next();
    }
  };
}

// router/index.ts
router.beforeEach(requireAuth);
router.beforeEach((to, from, next) => {
  if (to.meta.requiresRole) {
    requireRole(to.meta.requiresRole)(to, from, next);
  } else {
    next();
  }
});
```

### Lazy Loading Routes

```typescript
// router/index.ts
const routes = [
  {
    path: "/users",
    name: "users",
    component: () => import("@/views/Users/index.vue"),
  },
  {
    path: "/orders",
    name: "orders",
    component: () => import("@/views/Orders/index.vue"),
  },
];
```

## Component Communication

### Props Down, Events Up

```vue
<!-- Parent Component -->
<template>
  <UserList
    :users="users"
    @user-selected="handleUserSelected"
    @user-deleted="handleUserDeleted"
  />
</template>

<script setup lang="ts">
function handleUserSelected(user: User) {
  selectedUser.value = user;
}

function handleUserDeleted(userId: number) {
  users.value = users.value.filter((u) => u.id !== userId);
}
</script>

<!-- Child Component -->
<script setup lang="ts">
const props = defineProps<{
  users: User[];
}>();

const emit = defineEmits<{
  "user-selected": [user: User];
  "user-deleted": [userId: number];
}>();

function selectUser(user: User) {
  emit("user-selected", user);
}

function deleteUser(userId: number) {
  emit("user-deleted", userId);
}
</script>
```

### Provide/Inject

```vue
<!-- Parent -->
<script setup lang="ts">
import { provide } from "vue";

const theme = ref("dark");
const locale = ref("en");

provide("theme", theme);
provide("locale", locale);
</script>

<!-- Child (any level deep) -->
<script setup lang="ts">
import { inject } from "vue";

const theme = inject<Ref<string>>("theme", ref("light"));
const locale = inject<Ref<string>>("locale", ref("en"));
</script>
```

## Performance Optimization

### v-show vs v-if

```vue
<!-- Use v-show for frequent toggles -->
<div v-show="isVisible">Content</div>

<!-- Use v-if for conditional rendering -->
<div v-if="shouldRender">Content</div>
```

### Computed vs Methods

```vue
<script setup lang="ts">
// ✅ Good - Computed (cached)
const filteredUsers = computed(() => users.value.filter((user) => user.active));

// ❌ Bad - Method (recalculated on every render)
function getFilteredUsers() {
  return users.value.filter((user) => user.active);
}
</script>
```

### Key Management

```vue
<!-- ✅ Good - Use unique keys -->
<div v-for="user in users" :key="user.id">
  {{ user.name }}
</div>

<!-- ❌ Bad - Using index as key when items can change -->
<div v-for="(user, index) in users" :key="index">
  {{ user.name }}
</div>
```

## Best Practices

1. **Use Composition API** - Prefer `<script setup>` syntax
2. **Extract composables** - Reuse logic across components
3. **Use Pinia for state** - Centralized state management
4. **Lazy load routes** - Code splitting for better performance
5. **Use computed for derived state** - Automatic caching
6. **Proper key usage** - Unique keys for v-for
7. **Props validation** - Use TypeScript interfaces
8. **Event naming** - Use kebab-case for events
9. **Scoped styles** - Prevent style leakage
10. **Type safety** - Use TypeScript throughout

## When Writing Vue Components

1. **Use Composition API** - Modern Vue 3 approach
2. **Extract to composables** - Reusable logic
3. **Use Pinia stores** - For shared state
4. **Lazy load routes** - Better performance
5. **Validate props** - TypeScript interfaces
6. **Handle loading/error states** - Better UX
7. **Use computed properties** - For derived data
8. **Optimize re-renders** - Use v-show, keys, etc.
9. **Follow naming conventions** - Components PascalCase, composables camelCase
10. **Keep components focused** - Single responsibility
