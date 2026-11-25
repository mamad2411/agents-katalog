# 微信小程序 / uni-app 开发规范

## 概述

本 Skill 覆盖微信原生小程序和 uni-app（Taro）的开发规范，帮助 Claude Code 生成符合国内主流标准的小程序代码。

适用场景：
- 微信原生小程序页面开发
- uni-app 跨端组件编写
- 小程序状态管理（Pinia / Vuex）
- 小程序 API 封装（request、storage、login）

---

## 目录结构规范

### uni-app（推荐）

```
src/
├── pages/                  # 页面
│   ├── index/
│   │   ├── index.vue
│   │   └── components/     # 页面级私有组件
│   └── order/
│       ├── list.vue
│       └── detail.vue
├── components/             # 全局公共组件
│   ├── base/               # 基础组件（Button、Icon 等）
│   └── business/           # 业务组件
├── stores/                 # Pinia 状态管理
│   ├── user.ts
│   └── cart.ts
├── api/                    # 接口封装
│   ├── request.ts          # 统一请求封装
│   ├── user.ts
│   └── order.ts
├── utils/                  # 工具函数
├── hooks/                  # 组合式函数
└── types/                  # TypeScript 类型
```

---

## 请求封装

```typescript
// api/request.ts — 统一请求封装，处理 token、错误码、loading
import { useUserStore } from '@/stores/user'

interface RequestOptions {
  url: string
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
  data?: Record<string, unknown>
  showLoading?: boolean
}

interface ApiResponse<T = unknown> {
  code: number
  message: string
  data: T
}

const BASE_URL = import.meta.env.VITE_API_BASE_URL

export async function request<T = unknown>(options: RequestOptions): Promise<T> {
  const { url, method = 'GET', data, showLoading = false } = options
  const userStore = useUserStore()

  if (showLoading) uni.showLoading({ title: '加载中' })

  return new Promise((resolve, reject) => {
    uni.request({
      url: BASE_URL + url,
      method,
      data,
      header: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${userStore.token}`,
      },
      success: (res) => {
        const result = res.data as ApiResponse<T>
        if (result.code === 200) {
          resolve(result.data)
        } else if (result.code === 401) {
          // token 过期，跳转登录
          userStore.logout()
          uni.navigateTo({ url: '/pages/login/index' })
          reject(new Error('登录已过期'))
        } else {
          uni.showToast({ title: result.message, icon: 'error' })
          reject(new Error(result.message))
        }
      },
      fail: (err) => {
        uni.showToast({ title: '网络请求失败', icon: 'error' })
        reject(err)
      },
      complete: () => {
        if (showLoading) uni.hideLoading()
      },
    })
  })
}

// 语法糖
export const get = <T>(url: string, data?: Record<string, unknown>) =>
  request<T>({ url, method: 'GET', data })

export const post = <T>(url: string, data?: Record<string, unknown>) =>
  request<T>({ url, method: 'POST', data })
```

---

## 微信登录封装

```typescript
// hooks/useWxLogin.ts
import { ref } from 'vue'
import { post } from '@/api/request'
import { useUserStore } from '@/stores/user'

export function useWxLogin() {
  const loading = ref(false)
  const userStore = useUserStore()

  async function login(): Promise<void> {
    loading.value = true
    try {
      // Step 1: 获取微信 code
      const { code } = await new Promise<WechatMiniprogram.LoginSuccessCallbackResult>(
        (resolve, reject) => uni.login({ success: resolve, fail: reject })
      )
      // Step 2: 换取业务 token
      const { token, userInfo } = await post<{ token: string; userInfo: UserVO }>(
        '/auth/wx-login', { code }
      )
      userStore.setToken(token)
      userStore.setUser(userInfo)
    } finally {
      loading.value = false
    }
  }

  return { login, loading }
}
```

---

## 分页列表 Hook

```typescript
// hooks/usePagination.ts — 通用上拉加载更多
import { ref, reactive } from 'vue'

export function usePagination<T>(
  fetchFn: (page: number, pageSize: number) => Promise<{ list: T[]; total: number }>
) {
  const list = ref<T[]>([])
  const loading = ref(false)
  const refreshing = ref(false)
  const finished = ref(false)
  const pagination = reactive({ page: 1, pageSize: 20, total: 0 })

  async function loadMore() {
    if (loading.value || finished.value) return
    loading.value = true
    try {
      const { list: newItems, total } = await fetchFn(pagination.page, pagination.pageSize)
      list.value.push(...newItems)
      pagination.total = total
      pagination.page++
      finished.value = list.value.length >= total
    } finally {
      loading.value = false
    }
  }

  async function refresh() {
    refreshing.value = true
    list.value = []
    pagination.page = 1
    finished.value = false
    try {
      await loadMore()
    } finally {
      refreshing.value = false
    }
  }

  // 初始加载
  loadMore()

  return { list, loading, refreshing, finished, loadMore, refresh }
}
```

---

## 页面规范

```vue
<!-- pages/order/list.vue -->
<script setup lang="ts">
import { usePagination } from '@/hooks/usePagination'
import { orderApi } from '@/api/order'

// 页面标题用 definePageMeta（uni-app Vite 模式）
defineOptions({ name: 'OrderList' })

const { list, loading, finished, loadMore, refresh } = usePagination(
  (page, pageSize) => orderApi.getList({ page, pageSize })
)

// 下拉刷新
onPullDownRefresh(async () => {
  await refresh()
  uni.stopPullDownRefresh()
})

// 上拉加载更多
onReachBottom(() => loadMore())
</script>

<template>
  <view class="order-list">
    <order-item
      v-for="order in list"
      :key="order.id"
      :order="order"
    />
    <view v-if="loading" class="loading-tip">加载中...</view>
    <view v-if="finished && !loading" class="finished-tip">没有更多了</view>
  </view>
</template>
```

---

## 常见错误

### ❌ 直接调用 wx API，不封装

```javascript
// 错误：到处写原生调用，难以维护
wx.request({ url: 'https://api.example.com/...' })
```

### ✅ 统一通过封装层调用

```typescript
// 正确：统一的 request 封装处理 token、错误
import { get } from '@/api/request'
const orders = await get<Order[]>('/orders')
```

### ❌ 在页面中写 API 调用逻辑

```javascript
// 错误：API 逻辑写在页面里
onLoad(async () => {
  const res = await uni.request({ url: '...' })
  list.value = res.data.data
})
```

### ✅ 封装到 api 层

```typescript
// api/order.ts
export const orderApi = {
  getList: (params: OrderQuery) => get<PageResult<OrderVO>>('/orders', params),
}
// 页面中
const orders = await orderApi.getList({ page: 1, pageSize: 20 })
```
