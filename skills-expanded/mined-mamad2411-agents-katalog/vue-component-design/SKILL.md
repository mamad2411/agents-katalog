---
name: vue-component-design
description: 在规划或设计新 Vue 组件、组件拆分、组件重构、Props/Emits、composable 抽取时使用；TRS 开发计划涉及组件任务时必须使用。
---

# Vue 组件设计规范

## 概述

指导如何设计可维护、可复用、职责清晰的 Vue 3 组件。涵盖组件拆分策略、Props/Emits 设计、组合式函数抽取、以及常见组件模式。

**核心原则**：单一职责 + 最小化 Props + 组合优于继承。

默认使用 Vue 3、`<script setup lang="ts">` 和组合式 API；自研组件在模板中使用 PascalCase，第三方组件按项目约定前缀使用。

## writing-plans 阶段要求

当本技能用于实施计划阶段时，计划必须写清：

- 本技能约束适用于哪些任务。
- 计划的 `Required TRS skills` 中必须列出 `vue-component-design`；若同时涉及样式、接口、表单或 Store，也必须列出对应 TRS skill。
- 需要创建或修改的文件。
- 关键组件职责、Props/Emits、Slots、expose 或 composable 抽取方案。
- 验证步骤必须分层：开发中优先 `pnpm lint:eslint` / `pnpm lint`，涉及页面交互必须浏览器运行时验证；不得默认安排 `pnpm build`，只有用户明确确认后才执行。
- 若任务涉及页面、组件、样式、交互或接口联调，计划中必须增加 `Browser Runtime Verification` 小节，声明使用 `chrome-devtools-mcp`，并列出页面路径、核心操作、Console、Network、布局检查点。

## 何时激活

- 设计新的 Vue 组件
- 重构臃肿的组件
- 讨论组件拆分策略
- 创建可复用的组合式函数

## 参考文档

- 规划或设计组件前，按需读取 `references/vue.md` 和 `references/typescript.md`。
- 如果只是纯组件职责、Props/Emits 或 composable 抽取判断，以本技能正文为主；涉及团队 Vue/TS 约定时再读取 references。

## 组件拆分决策树

```
组件代码 > 200 行？
├── 是 → 优先拆分（强烈建议）
└── 否 → 检查是否有多个职责
         ├── 是 → 按职责拆分
         └── 否 → 保持现状

逻辑是否在多处重复？
├── 是 → 提取为 composable
└── 否 → 保持在组件内

模板片段是否独立可复用？
├── 是 → 提取为子组件
└── 否 → 保持在模板内
```

## 组件层次设计

### 三层组件架构

```
pages/          → 页面组件（路由级别，组装 + 数据获取）
├── components/ → 业务组件（领域特定，如 OrderTable）
└── @/components/ → 通用组件（纯 UI，如 SearchInput）
```

| 层级 | 职责 | 示例 |
|------|------|------|
| **页面组件** | 路由入口、数据获取、组装子组件 | `UserList.vue` |
| **业务组件** | 特定业务逻辑、可在同域复用 | `UserFilterPanel.vue` |
| **通用组件** | 纯 UI、无业务逻辑、跨项目复用 | `SearchInput.vue` |

## Props 设计原则

### 1. 最小化必需 Props

```typescript
// ✅ 好的设计 - 只要求必需的
interface Props {
  items: ListItem[]           // 必需
  loading?: boolean           // 可选，默认 false
  pageSize?: number           // 可选，默认 10
  showPagination?: boolean    // 可选，默认 true
}

// ❌ 差的设计 - 太多必需参数
interface Props {
  items: ListItem[]
  loading: boolean
  pageSize: number
  showPagination: boolean
  emptyText: string
  bordered: boolean
}
```

### 2. 避免 Boolean 陷阱

```typescript
// ❌ 多个 Boolean 让调用方困惑
<MyTable :bordered :striped :compact :hoverable></MyTable>

// ✅ 使用具名对象或联合类型
interface Props {
  variant?: 'default' | 'compact' | 'bordered'
  size?: 'sm' | 'md' | 'lg'
}
```

### 3. 使用 v-model 简化双向绑定

```vue
<!-- 父组件 -->
<SearchPanel v-model:keyword="keyword" v-model:filters="filters"></SearchPanel>

<!-- 子组件 SearchPanel.vue -->
<script setup lang="ts">
const keyword = defineModel<string>('keyword', { default: '' })
const filters = defineModel<FilterState>('filters', { required: true })
</script>
```

## Emits 设计

```typescript
// ✅ 语义化事件命名 —— 动词 + 名词
const emit = defineEmits<{
  select: [item: ListItem]        // 选中某项
  delete: [id: string]            // 删除某项
  'update:filters': [val: Filter] // 更新筛选
  confirm: []                     // 确认操作
}>()

// ❌ 模糊的事件名
const emit = defineEmits<{
  change: [val: any]    // 什么变了？
  click: []             // 点了什么？
  callback: [data: any] // 什么回调？
}>()
```

## 组合式函数（Composables）

### 何时提取 Composable

1. **逻辑复用**：≥2 个组件使用相同逻辑
2. **关注点分离**：独立的业务逻辑块（如表格分页、表单校验）
3. **可测试性**：纯逻辑便于单测

### 命名与结构

```typescript
// composables/useTablePagination.ts

interface UseTablePaginationOptions<T> {
  fetchFn: (params: PaginationParams) => Promise<PageResult<T>>
  defaultPageSize?: number
}

export function useTablePagination<T>(options: UseTablePaginationOptions<T>) {
  const { fetchFn, defaultPageSize = 10 } = options

  const data = ref<T[]>([])
  const loading = ref(false)
  const pagination = reactive({
    current: 1,
    pageSize: defaultPageSize,
    total: 0,
  })

  async function fetchData() {
    loading.value = true
    try {
      const result = await fetchFn({
        page: pagination.current,
        size: pagination.pageSize,
      })
      data.value = result.list
      pagination.total = result.total
    } finally {
      loading.value = false
    }
  }

  function handlePageChange(page: number) {
    pagination.current = page
    fetchData()
  }

  onMounted(fetchData)

  return {
    data: readonly(data),
    loading: readonly(loading),
    pagination,
    refresh: fetchData,
    handlePageChange,
  }
}
```

### Composable 规范

```typescript
// ✅ 正确的返回值 - 使用 readonly 保护内部状态
return {
  data: readonly(data),     // 只读
  loading: readonly(loading),
  refresh: fetchData,       // 暴露方法
}

// ❌ 错误 - 直接暴露可变状态
return {
  data,      // 外部可以随意修改
  loading,
}
```

## 常见组件模式

### 1. 列表页三件套

```vue
<!-- UserList.vue（页面组件） -->
<script setup lang="ts">
const { data, loading, pagination, refresh, handlePageChange } =
  useTablePagination({ fetchFn: fetchUserList })

const { keyword, filters, handleSearch, handleReset } =
  useListFilter({ onFilter: refresh })
</script>

<template>
  <div class="p-4">
    <!-- 筛选区 -->
    <UserFilterPanel
      v-model:keyword="keyword"
      v-model:filters="filters"
      @search="handleSearch"
      @reset="handleReset"
    />

    <!-- 表格区 -->
    <a-table
      :data-source="data"
      :loading="loading"
      :pagination="pagination"
      @change="handlePageChange"
    />
  </div>
</template>
```

### 2. 弹窗表单模式

这里重点展示组件拆分和状态传递边界；表单校验、提交 loading、`code === 200` 判断和错误处理细节，必须继续遵循 `form-validation` 与 `api-integration`。

```vue
<!-- EditUserModal.vue -->
<script setup lang="ts">
import type { FormInstance } from 'ant-design-vue'

const visible = defineModel<boolean>('open', { default: false })

interface Props {
  userId?: string   // 有值=编辑，无值=新增
}
const props = defineProps<Props>()

const emit = defineEmits<{
  success: []
}>()

const isEdit = computed(() => !!props.userId)
const title = computed(() => isEdit.value ? '编辑用户' : '新增用户')

const formState = reactive({
  name: '',
  email: '',
})
const formRef = ref<FormInstance | null>(null)
const submitting = ref(false)
const rules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  email: [{ required: true, message: '请输入邮箱', trigger: 'blur' }],
}

// 编辑时加载数据
watch(() => props.userId, async (id) => {
  if (id) {
    const { data } = await fetchUser(id)
    if (data?.code !== 200) return
    Object.assign(formState, data.data)
  }
}, { immediate: true })

async function handleSubmit() {
  await formRef.value?.validate()
  if (submitting.value) return
  submitting.value = true
  try {
    const { data } = isEdit.value
      ? await updateUser(props.userId!, formState)
      : await createUser(formState)
    if (data?.code !== 200) return
    visible.value = false
    emit('success')
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <a-modal
    v-model:open="visible"
    :title="title"
    :confirm-loading="submitting"
    @ok="handleSubmit"
  >
    <a-form ref="formRef" :model="formState" :rules="rules">
      <a-form-item label="姓名" name="name">
        <a-input v-model:value="formState.name" />
      </a-form-item>
      <a-form-item label="邮箱" name="email">
        <a-input v-model:value="formState.email" />
      </a-form-item>
    </a-form>
  </a-modal>
</template>
```

## 反模式检查清单

- [ ] ❌ 组件超过 200 行 → 优先拆分（行数只是信号，仍需结合职责与复杂度判断）
- [ ] ❌ Props 超过 8 个 → 考虑用对象 / 插槽替代
- [ ] ❌ 组件内直接调用 API → 提取到 composable
- [ ] ❌ 在子组件中修改 props → 使用 emit 或 v-model
- [ ] ❌ 组件名不体现用途 → 重命名为 "领域+行为" 格式
- [ ] ❌ 模板中复杂表达式 → 提取为 computed
