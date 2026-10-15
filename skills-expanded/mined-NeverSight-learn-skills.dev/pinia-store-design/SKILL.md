---
name: pinia-store-design
description: 在规划是否使用 Pinia、设计 store、跨组件/跨路由共享状态、未读数等全局状态时使用；TRS 开发计划涉及 Store 任务时必须使用。
---

# Pinia 状态管理设计规范

## 概述

规范 Pinia store 的设计决策与代码结构。核心问题是"什么状态该放 store"，而不是"怎么写 store 语法"。

**核心原则**：Store 是全局共享状态的最后手段，不是默认选择。

## writing-plans 阶段要求

当本技能用于实施计划阶段时，计划必须写清：

- 本技能约束适用于哪些任务。
- 计划的 `Required TRS skills` 中必须列出 `pinia-store-design`；Store action 涉及接口时必须同时列出 `api-integration`。
- 需要创建或修改的文件。
- 状态归属、共享范围、生命周期、持久化需求、actions/getters 和接口依赖。
- 验证方式：开发中优先 `pnpm lint:eslint` / `pnpm lint`，涉及页面交互必须做页面运行时、跨组件或跨路由状态检查；不得默认安排 `pnpm build`，只有用户明确确认后才执行。
- 若任务涉及页面、组件、样式、交互或接口联调，计划中必须增加 `Browser Runtime Verification` 小节，声明使用 `chrome-devtools-mcp`，并列出页面路径、核心操作、Console、Network、布局检查点。

## 何时激活

- 判断某个状态是放 store 还是组件本地
- 设计新的 Pinia store 结构
- 在 store 中处理异步请求
- 多个组件需要共享同一份数据

---

## 一、状态放哪里：决策树

```
这个状态需要在多个不相关的组件中共享？
├── 否 → 放组件本地（ref / reactive）
│
└── 是 → 这些组件是父子关系？
         ├── 是 → 用 Props / Emits 或 provide/inject
         │
         └── 否（跨层级、跨路由）→ 放 Pinia Store
```

当共享范围、组件关系、生命周期不明确时，不要猜，先补齐信息：

- 需要共享到哪些组件/页面？是否跨路由？
- 这些组件是否父子关系，是否能用 Props/Emits 或 provide/inject 传递？
- 刷新后是否需要保留（持久化）？

### 适合放 Store 的状态

| 场景 | 示例 |
|------|------|
| 用户身份信息 | 登录用户、权限列表、token |
| 全局 UI 状态 | 侧边栏折叠状态、主题、语言 |
| 跨路由共享数据 | 购物车、消息未读数 |
| 需要持久化的配置 | 用户偏好设置 |

### 不适合放 Store 的状态

| 场景 | 推荐方式 |
|------|---------|
| 单个页面的列表数据 | 组件本地 ref + composable |
| 弹窗的 visible 状态 | 组件本地 ref |
| 表单的输入状态 | 组件本地 reactive |
| 某个组件的 loading | 组件本地 ref |

---

## 二、Store 目录结构

```
src/
└── stores/
    ├── user.ts          # 用户身份、权限
    ├── app.ts           # 全局 UI 状态（菜单、主题）
    ├── dict.ts          # 数据字典（全局枚举缓存）
    └── index.ts         # 统一导出（可选）
```

**命名规范**：
- 文件名：camelCase，例如 `user.ts`、`userInfo.ts`
- Store ID：与文件名一致的 kebab-case 字符串，例如 `'user-info'`
- 导出函数：`use` + PascalCase，例如 `useUserStore`

---

## 三、Store 标准结构

### 标准写法（Setup Store 风格，与 `<script setup>` 一致）

```typescript
// stores/user.ts
import type { UserInfo, Permission } from '@/types/user'

export const useUserStore = defineStore('user', () => {
  // ① State —— 响应式数据
  const userInfo = ref<UserInfo | null>(null)
  const permissions = ref<string[]>([])
  const token = useStorage('token', '')

  // ② Getters —— 派生数据
  const isLoggedIn = computed(() => !!token.value)
  const hasPermission = computed(
    () => (code: string) => permissions.value.includes(code)
  )

  // ③ Actions —— 方法（含异步）
  async function fetchUserInfo() {
    const { data } = await axios.get('/api/user/info')
    if (data?.code !== 200) return
    userInfo.value = data.data
    permissions.value = data.data.permissions ?? []
  }

  function logout() {
    userInfo.value = null
    permissions.value = []
    token.value = ''
  }

  return {
    // 暴露 state（用 readonly 保护不应被外部直接修改的）
    userInfo: readonly(userInfo),
    permissions: readonly(permissions),
    token,
    // 暴露 getters
    isLoggedIn,
    hasPermission,
    // 暴露 actions
    fetchUserInfo,
    logout,
  }
})
```

### Options Store 风格（不推荐新代码使用，仅兼容旧代码）

```typescript
// 仅用于迁移旧代码，新 store 统一用 Setup 风格
export const useAppStore = defineStore('app', {
  state: () => ({ collapsed: false }),
  getters: {
    menuWidth: (state) => state.collapsed ? 64 : 240,
  },
  actions: {
    toggleMenu() { this.collapsed = !this.collapsed },
  },
})
```

---

## 四、异步 Action 规范

Store 中的异步 action 与组件中的请求写法保持一致，遵循 `api-integration`：

```typescript
// ✅ 标准异步 action
async function fetchDictList() {
  dictLoading.value = true
  try {
    const { data } = await axios.get('/api/dict/list')
    if (data?.code !== 200) return
    dictMap.value = Object.fromEntries(
      data.data.map((item: DictItem) => [item.code, item])
    )
  } finally {
    dictLoading.value = false
  }
}

// ❌ 禁止 —— 没有 finally，loading 漏关
async function badFetch() {
  loading.value = true
  const { data } = await axios.get('/api/xxx')
  loading.value = false  // 出错时不执行
}
```

---

## 五、在组件中使用 Store

### 正确解构方式

```typescript
// ✅ 用 storeToRefs 解构响应式数据，方法直接解构
const userStore = useUserStore()
const { userInfo, isLoggedIn } = storeToRefs(userStore)  // 保持响应式
const { fetchUserInfo, logout } = userStore               // 方法直接取

// ❌ 直接解构会丢失响应式
const { userInfo } = useUserStore()  // userInfo 变成普通值，不响应更新
```

### 只在需要的组件中调用 store

```typescript
// ✅ 在需要的组件内调用
const userStore = useUserStore()

// ❌ 在 composable 外部（模块顶层）调用（Pinia 实例未挂载）
const userStore = useUserStore()  // 模块顶层调用会报错

export function useXxx() {
  const userStore = useUserStore()  // ✅ 在函数内部调用
}
```

---

## 六、Store 持久化

需要刷新后保留的状态（如 token、主题），用 `useStorage`（VueUse，项目已自动导入）替代普通 ref：

```typescript
export const useAppStore = defineStore('app', () => {
  // ✅ 自动同步到 localStorage，刷新后恢复
  const theme = useStorage<'light' | 'dark'>('app-theme', 'light')
  const collapsed = useStorage('sidebar-collapsed', false)

  return { theme, collapsed }
})
```

---

## 七、跨 Store 通信

Store 可以直接调用其他 store，不需要任何特殊处理：

```typescript
// stores/order.ts
export const useOrderStore = defineStore('order', () => {
  async function submitOrder(form: OrderForm) {
    // 直接在 action 内调用其他 store
    const userStore = useUserStore()
    if (!userStore.isLoggedIn) {
      message.warning('请先登录')
      return
    }
    await axios.post('/api/order/create', {
      ...form,
      userId: userStore.userInfo?.id,
    })
  }

  return { submitOrder }
})
```

---

## 反模式检查清单

- [ ] ❌ 把单页面的列表数据放进了 store → 移到组件本地
- [ ] ❌ 在 store 中直接操作 DOM 或调用路由跳转 → 在组件中处理，store 只管数据
- [ ] ❌ Store 中有超过 10 个以上的 state 字段 → 考虑拆分成多个 store
- [ ] ❌ 直接解构 store 的 state 而不用 storeToRefs → 响应式丢失
- [ ] ❌ 在模块顶层调用 useXxxStore() → 移到函数内部
- [ ] ❌ 用 store 传递父子组件数据 → 改用 Props / Emits
