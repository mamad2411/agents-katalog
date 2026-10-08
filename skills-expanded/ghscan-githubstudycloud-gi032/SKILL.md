---
name: new-vue-component
description: |
  Scaffold a new Vue 3 component (SFC) following project conventions:
  shadcn-vue primitives, Tailwind v4, Pinia if state needed, Vitest spec, Storybook story.
  Use when the user asks to "create a new component", "make a Xxx component",
  "scaffold a Button/Form/Card", or to add interactive UI to a Vue page.
argument-hint: "<ComponentName> [feature-folder]"
arguments: [name, folder]
disable-model-invocation: false
allowed-tools: Read Write Edit Bash(npx *) Bash(pnpm *)
---

# 创建新 Vue 组件

为组件 `$name` 在 `app/components/$folder/` 目录下创建以下文件（若 `$folder` 为空，默认放 `feature/`）：

## 1. SFC 文件 `$name/$name.vue`

```vue
<script setup lang="ts">
// 1) imports
// 2) defineProps / defineEmits / defineSlots
// 3) composable
// 4) state
// 5) computed
// 6) watch / lifecycle
// 7) methods
</script>

<template>
  <!-- 用 shadcn-vue 原语优先 -->
</template>
```

要求：
- `<script setup lang="ts">`
- props / emits 类型化（TS-only 写法）
- 不要写 `<style>`，用 Tailwind v4 类
- 复用 `app/components/ui/` 下的 shadcn-vue 组件
- 用户可见文本走 `useI18n().t(...)`
- 复杂状态用 Pinia store 而不是 props drilling

## 2. 单元测试 `$name/$name.test.ts`

```ts
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import $name from './$name.vue'

describe('$name', () => {
  it('renders props correctly', () => {
    const wrapper = mount($name, { props: { /* ... */ } })
    expect(wrapper.text()).toContain('…')
  })

  it('emits on click', async () => {
    const wrapper = mount($name)
    await wrapper.find('button').trigger('click')
    expect(wrapper.emitted('submit')).toBeTruthy()
  })
})
```

## 3. Storybook 故事 `$name/$name.stories.ts`

```ts
import type { Meta, StoryObj } from '@storybook/vue3'
import $name from './$name.vue'

const meta: Meta<typeof $name> = {
  title: 'Feature/$name',
  component: $name,
  tags: ['autodocs'],
}
export default meta

export const Default: StoryObj<typeof $name> = { args: { /* ... */ } }
export const Loading: StoryObj<typeof $name> = { args: { /* ... */ } }
export const Error: StoryObj<typeof $name> = { args: { /* ... */ } }
```

## 4. 在 `app/components/index.ts` 追加导出

```ts
export { default as $name } from './$folder/$name/$name.vue'
```

## 输出顺序（必须按此顺序）

第一步：**输出组件规约表**

```
| 字段 | 类型 | 必填 | 说明 |
|------|------|-----|------|
| props.xxx | string | ✓ | ... |
| emits.submit | (FormData) => void | ✓ | ... |
| slots.default | - | - | ... |
| 状态 | ref<...> | - | ... |
| 依赖 | useAuthStore | - | ... |
```

第二步：等用户确认规约 OK，再生成上面 4 个文件。

第三步：完成后告诉用户：
- 跑 `pnpm test $name`
- 跑 `pnpm storybook` 看看视觉
- 跑 `/a11y-vue $name/$name.vue` 做无障碍检查
