# Vue3 最佳实践

## 概述

本 Skill 涵盖 Vue3 组合式 API（Composition API）的最佳实践，适用于使用 Vue3 + TypeScript + Pinia 的项目。

适用场景：
- 新建 Vue3 组件时确定代码结构
- 状态管理设计（Pinia）
- 组合式函数（Composables）封装
- 性能优化

---

## 组件结构规范

### 标准 `<script setup>` 组件

```vue
<!-- 推荐顺序: defineProps → defineEmits → 响应式状态 → computed → watch → 方法 → 生命周期 -->
<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import type { UserVO } from '@/types'

// 1. Props & Emits
const props = defineProps<{
  userId: string
  readonly?: boolean
}>()

const emit = defineEmits<{
  saved: [user: UserVO]
  cancelled: []
}>()

// 2. Store
const userStore = useUserStore()

// 3. 响应式状态
const loading = ref(false)
const form = ref({ name: '', email: '' })

// 4. Computed
const isValid = computed(() =>
  form.value.name.trim().length > 0 && form.value.email.includes('@')
)

// 5. Watch
watch(() => props.userId, async (id) => {
  if (id) await loadUser(id)
}, { immediate: true })

// 6. 方法
async function loadUser(id: string) {
  loading.value = true
  try {
    const user = await userStore.fetchUser(id)
    form.value = { name: user.name, email: user.email }
  } finally {
    loading.value = false
  }
}

async function handleSave() {
  if (!isValid.value) return
  loading.value = true
  try {
    const saved = await userStore.updateUser(props.userId, form.value)
    emit('saved', saved)
  } finally {
    loading.value = false
  }
}

// 7. 生命周期（通常用 watch + immediate 替代 onMounted）
onMounted(() => {
  // 只放真正需要 DOM 的逻辑
})
</script>

<template>
  <div class="user-form">
    <input v-model="form.name" :disabled="props.readonly || loading" />
    <input v-model="form.email" :disabled="props.readonly || loading" />
    <button :disabled="!isValid || loading" @click="handleSave">
      {{ loading ? '保存中...' : '保存' }}
    </button>
  </div>
</template>
```

---

## Composables（组合式函数）

### 封装规范

```typescript
// composables/useUserForm.ts
// 命名：use + 功能描述（驼峰）
// 文件：composables/ 目录，一个功能一个文件

import { ref, computed } from 'vue'
import type { UserVO, UpdateUserDTO } from '@/types'

export function useUserForm(initialData?: Partial<UserVO>) {
  // 状态定义在内部，通过返回值暴露
  const form = ref<UpdateUserDTO>({
    name: initialData?.name ?? '',
    email: initialData?.email ?? '',
  })
  const dirty = ref(false)

  const isValid = computed(() =>
    form.value.name.trim().length > 0 &&
    /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email)
  )

  function reset() {
    form.value = { name: initialData?.name ?? '', email: initialData?.email ?? '' }
    dirty.value = false
  }

  // ✅ 返回响应式引用和方法，不要返回解构后的值
  return { form, dirty, isValid, reset }
}
```

### 异步数据获取

```typescript
// composables/useAsync.ts — 通用异步状态管理
import { ref, type Ref } from 'vue'

export function useAsync<T>(fn: () => Promise<T>) {
  const data: Ref<T | null> = ref(null)
  const loading = ref(false)
  const error = ref<Error | null>(null)

  async function execute() {
    loading.value = true
    error.value = null
    try {
      data.value = await fn()
    } catch (e) {
      error.value = e instanceof Error ? e : new Error(String(e))
    } finally {
      loading.value = false
    }
  }

  return { data, loading, error, execute }
}

// 使用示例
const { data: user, loading, execute: loadUser } = useAsync(() => api.getUser(id))
```

---

## Pinia 状态管理

### Store 结构

```typescript
// stores/user.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { userApi } from '@/api/user'
import type { UserVO } from '@/types'

// 使用组合式写法（更灵活，与 Composition API 一致）
export const useUserStore = defineStore('user', () => {
  // State
  const currentUser = ref<UserVO | null>(null)
  const userCache = ref<Map<string, UserVO>>(new Map())

  // Getters
  const isLoggedIn = computed(() => currentUser.value !== null)
  const userName = computed(() => currentUser.value?.name ?? '未登录')

  // Actions
  async function fetchUser(id: string): Promise<UserVO> {
    // 先查缓存
    if (userCache.value.has(id)) {
      return userCache.value.get(id)!
    }
    const user = await userApi.getById(id)
    userCache.value.set(id, user)
    return user
  }

  async function updateUser(id: string, data: Partial<UserVO>): Promise<UserVO> {
    const updated = await userApi.update(id, data)
    userCache.value.set(id, updated)
    if (currentUser.value?.id === id) {
      currentUser.value = updated
    }
    return updated
  }

  function logout() {
    currentUser.value = null
    userCache.value.clear()
  }

  return { currentUser, isLoggedIn, userName, fetchUser, updateUser, logout }
})
```

---

## TypeScript 类型规范

```typescript
// types/index.ts — 集中定义，按业务模块分文件

// VO：接口返回给前端的视图对象
export interface UserVO {
  id: string
  name: string
  email: string
  avatar?: string
  createdAt: string  // ISO8601 字符串
}

// DTO：前端发给接口的数据
export interface CreateUserDTO {
  name: string
  email: string
  password: string
}

export interface UpdateUserDTO {
  name?: string
  email?: string
}

// 分页通用类型
export interface PageResult<T> {
  list: T[]
  total: number
  page: number
  pageSize: number
}

// API 统一响应格式
export interface ApiResponse<T = void> {
  code: number
  message: string
  data: T
}
```

---

## 性能优化

```typescript
// 1. v-memo 缓存列表项（大列表场景）
// <li v-for="item in list" :key="item.id" v-memo="[item.id, item.selected]">

// 2. defineAsyncComponent 懒加载
import { defineAsyncComponent } from 'vue'
const HeavyChart = defineAsyncComponent(() => import('./HeavyChart.vue'))

// 3. shallowRef 用于大对象
import { shallowRef } from 'vue'
const bigData = shallowRef<BigObject | null>(null)  // 只监听引用变化

// 4. 避免在模板中使用复杂表达式，改用 computed
// ❌ <div>{{ list.filter(x => x.active).length }}</div>
// ✅ const activeCount = computed(() => list.value.filter(x => x.active).length)
```

---

## 常见错误

### ❌ 解构响应式对象导致失去响应性

```typescript
// 错误：解构后 name 不再是响应式的
const { name } = useUserForm()

// 正确：保持响应式引用
const { form } = useUserForm()
// 然后用 form.value.name 访问
```

### ❌ watch 监听整个对象但不用 deep

```typescript
// 错误：监听对象属性变化需要 deep 或监听具体属性
watch(form, handler)  // 替换整个对象才会触发

// 正确方式一：监听具体属性
watch(() => form.value.name, handler)

// 正确方式二：需要监听所有属性变化时用 deep
watch(form, handler, { deep: true })
```
