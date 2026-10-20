---
description: Vue 3 前端开发规范，适用于 Vue 3 + TypeScript + Tailwind CSS + Vite 项目
globs: ["**/*.vue", "**/*.ts", "**/*.tsx", "**/*.css", "**/vite.config.*", "**/tailwind.config.*"]
alwaysApply: false
---

# Vue 3 开发规范

## 技术栈

- **框架**: Vue 3 (Composition API)
- **语言**: TypeScript（严格模式）
- **构建工具**: Vite
- **样式**: Tailwind CSS
- **状态管理**: Pinia
- **路由**: Vue Router 4
- **UI 组件**: shadcn/ui（Vue 版本）或其他基于 Tailwind 的组件库
- **HTTP 客户端**: Axios
- **代码规范**: ESLint + Prettier

## 组件规范

### 文件命名

- 组件文件使用 PascalCase：`UserProfile.vue`、`AppHeader.vue`
- 页面组件放在 `views/` 目录，通用组件放在 `components/` 目录
- 组件名与文件名保持一致

### 组件结构顺序

```vue
<script setup lang="ts">
// 1. 导入
// 2. Props / Emits 定义
// 3. 响应式状态
// 4. 计算属性
// 5. 方法
// 6. 生命周期钩子
// 7. Watch
</script>

<template>
  <!-- 模板内容 -->
</template>

<style scoped>
/* 样式 */
</style>
```

### Props 定义

- 始终使用 TypeScript 类型定义 Props，使用 `withDefaults` 设置默认值
- Props 使用 camelCase 命名，模板中使用 kebab-case

```vue
<script setup lang="ts">
interface Props {
  userId: string
  userName?: string
  isActive?: boolean
  items: UserItem[]
}

const props = withDefaults(defineProps<Props>(), {
  userName: '',
  isActive: false,
  items: () => [],
})
</script>
```

### Emits 定义

```vue
<script setup lang="ts">
const emit = defineEmits<{
  change: [value: string]
  submit: [data: FormData]
  'update:modelValue': [value: number]
}>()
```

### 响应式状态

- 对象/数组使用 `reactive()`，基本类型使用 `ref()`
- 优先使用 `ref()` 保持一致性（Vue 官方推荐）
- 避免解构响应式对象（会失去响应性），使用 `toRefs()`

```vue
<script setup lang="ts">
import { ref, reactive, computed, toRefs } from 'vue'

const count = ref(0)
const userForm = reactive({
  name: '',
  email: '',
  age: 0,
})

const isFormValid = computed(() => {
  return userForm.name.length > 0 && userForm.email.includes('@')
})
</script>
```

## Composition API 最佳实践

### Composable 封装

- 将可复用逻辑封装为 Composable 函数（`use` 前缀）
- 放在 `composables/` 目录下
- Composable 应返回响应式状态和方法

```typescript
// composables/useUserList.ts
import { ref, onMounted } from 'vue'
import type { User } from '@/types'

export function useUserList() {
  const users = ref<User[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchUsers() {
    loading.value = true
    error.value = null
    try {
      users.value = await userApi.getList()
    } catch (err) {
      error.value = err instanceof Error ? err.message : '获取用户列表失败'
    } finally {
      loading.value = false
    }
  }

  onMounted(fetchUsers)

  return {
    users,
    loading,
    error,
    fetchUsers,
  }
}
```

### 生命周期钩子

- 使用 `onMounted`、`onUnmounted` 等 Composition API 钩子
- 在 `onUnmounted` 中清理定时器、事件监听等副作用

```vue
<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'

let timer: ReturnType<typeof setInterval>

onMounted(() => {
  timer = setInterval(refresh, 5000)
})

onUnmounted(() => {
  clearInterval(timer)
})
</script>
```

## Pinia 状态管理

### Store 定义

- 使用 Setup Store 风格（更接近 Composition API）
- 每个 Store 放在 `stores/` 目录下，文件名与 store ID 一致
- Store ID 使用 camelCase

```typescript
// stores/useUserStore.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/types'

export const useUserStore = defineStore('user', () => {
  const currentUser = ref<User | null>(null)
  const isLoggedIn = computed(() => currentUser.value !== null)

  async function login(credentials: LoginCredentials) {
    const user = await authApi.login(credentials)
    currentUser.value = user
  }

  function logout() {
    currentUser.value = null
  }

  return {
    currentUser,
    isLoggedIn,
    login,
    logout,
  }
})
```

## Vue Router 规范

### 路由定义

- 路由配置使用懒加载（`() => import(...)`）
- 路由名称使用 PascalCase
- 路由路径使用 kebab-case

```typescript
// router/index.ts
const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('@/layouts/DefaultLayout.vue'),
    children: [
      {
        path: '',
        name: 'Home',
        component: () => import('@/views/HomePage.vue'),
        meta: { title: '首页', requiresAuth: false },
      },
      {
        path: 'user-profile',
        name: 'UserProfile',
        component: () => import('@/views/UserProfilePage.vue'),
        meta: { title: '用户资料', requiresAuth: true },
      },
    ],
  },
]
```

### 路由守卫

```typescript
router.beforeEach((to, from) => {
  const userStore = useUserStore()
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    return { name: 'Login', query: { redirect: to.fullPath } }
  }
})
```

## TypeScript 规范

- 开启严格模式：`"strict": true`
- 为所有函数参数和返回值添加类型注解
- 使用 `interface` 定义对象类型，`type` 定义联合/交叉类型
- API 响应类型放在 `types/` 或 `api/` 目录

```typescript
// types/user.ts
export interface User {
  id: string
  name: string
  email: string
  role: 'admin' | 'user' | 'guest'
  createdAt: string
}

export type CreateUserInput = Omit<User, 'id' | 'createdAt'>
export type UpdateUserInput = Partial<CreateUserInput>
```

## API 请求封装

```typescript
// api/request.ts
import axios from 'axios'
import type { AxiosRequestConfig } from 'axios'

const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 10000,
})

// 请求拦截器
request.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 响应拦截器
request.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response?.status === 401) {
      // 处理未授权
    }
    return Promise.reject(error)
  }
)

export default request
```

## 模板规范

- 使用 `v-for` 时必须提供 `:key`，优先使用唯一 ID 而非 index
- `v-if` 和 `v-for` 不在同一元素上使用（`v-if` 优先级更高）
- 使用 `<template>` 包裹多个元素避免不必要的 DOM 节点
- 事件处理函数在模板中不加括号（除非需要传参）

```vue
<template>
  <!-- 推荐 -->
  <ul>
    <li v-for="user in users" :key="user.id">
      {{ user.name }}
    </li>
  </ul>

  <!-- 使用 template 避免不必要节点 -->
  <template v-if="isLoaded">
    <UserHeader :user="currentUser" />
    <UserContent :user="currentUser" />
  </template>
</template>
```

## 样式规范

- **默认使用 Tailwind CSS** 工具类，避免编写自定义 CSS
- 响应式设计采用移动优先（`sm:` `md:` `lg:` `xl:`）
- 使用 `@apply` 将常用工具类组合为组件级样式
- 组件样式使用 `scoped` 避免全局污染
- 深色模式使用 `dark:` 变体

```vue
<template>
  <div class="flex items-center gap-4 rounded-lg bg-white p-4 shadow-sm dark:bg-gray-800">
    <img class="h-12 w-12 rounded-full object-cover" :src="user.avatar" :alt="user.name" />
    <div class="flex-1">
      <h3 class="text-base font-semibold text-gray-900 dark:text-white">{{ user.name }}</h3>
      <p class="text-sm text-gray-500 dark:text-gray-400">{{ user.email }}</p>
    </div>
    <button
      class="rounded-md bg-blue-500 px-3 py-1.5 text-sm font-medium text-white hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
      @click="handleAction"
    >
      操作
    </button>
  </div>
</template>

<style scoped>
/* 仅在 Tailwind 无法满足需求时才编写自定义 CSS */
.user-card {
  @apply flex items-center gap-4 rounded-lg bg-white p-4 shadow-sm;
}
</style>
```

## 项目目录结构

```
src/
├── api/          # API 请求封装
├── assets/       # 静态资源
│   ├── images/
│   └── styles/
├── components/   # 通用组件
│   └── common/
├── composables/  # 组合式函数
├── layouts/      # 布局组件
├── router/       # 路由配置
├── stores/       # Pinia 状态管理
├── types/        # TypeScript 类型定义
├── utils/        # 工具函数
└── views/        # 页面组件
```

## 性能优化

- 使用 `defineAsyncComponent` 懒加载大型组件
- 使用 `v-memo` 缓存静态列表项
- 使用 `shallowRef` / `shallowReactive` 优化大型不可变数据
- 合理使用 `computed` 缓存计算结果，避免模板中的复杂表达式
