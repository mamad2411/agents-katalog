---
name: vms
description: 使用 VMS (Vue Mini SFC) 工具开发微信小程序的完整指南。涵盖 Vue 3 Composition API、TypeScript、事件绑定、v-for、v-show、响应式数据、组件通信、插槽等核心用法，以及常见问题和最佳实践。Use when developing WeChat Mini Program with VMS, writing Vue SFC with @unmagic/vue-mini, or debugging template compilation issues.
license: MIT
metadata:
  author: github.com/unmagic
  version: '0.0.2'
---

# Vue Mini SFC 微信小程序开发指南

## 工具简介

**Vue Mini SFC**（简称 **VMS**）允许你使用 Vue 3 `<script setup lang="ts">` 语法开发微信小程序，自动编译为小程序原生代码。

**版本：** 0.0.2 | **仓库：** github.com/unmagic/vms

**要求：**

- **必须使用 TypeScript** - SFC 文件必须以 `<script setup lang="ts">` 编写
- Vue 3 Composition API + `<script setup>`
- 运行时：`@unmagic/vue-mini >= 1.0.0`
- Node.js >= 22.17.1

**输出：** 微信小程序原生代码（WXML + JS + WXSS + JSON）

## 项目结构

```
src/
├── pages/           # 页面
├── components/      # 组件
├── subXXX/          # 分包
├── api/             # API 接口
├── stores/          # Pinia 状态管理
├── utils/           # 工具函数
├── composition/     # 组合式函数
├── app.ts           # 应用入口（编译为 app.js）
├── app.json         # 小程序全局配置
└── app.wxss         # 全局样式
```

## CLI 命令

```bash
# 安装
pnpm add -D @unmagic/vms

# 开发模式（文件监听 + 增量编译）
vms dev

# 生产构建
vms build

# 生产构建 + 上传小程序
vms build --upload
```

## 配置文件

在项目根目录创建 `vms.config.js`，支持 `export default` 或 `export const config = ...` 两种写法：

```js
// vms.config.js
export default {
  wx: {
    appid: 'your-appid',
    privateKeyPath: '/path/to/private.key',
    name: 'your-name',
    email: 'your@email.com',
    version: '1.0.0',
    description: '项目描述',
  },
  sourceDir: 'src',      // 源码目录（默认 src）
  outputDir: 'dist',     // 输出目录（默认 dist）
  alias: { '@': './src' }, // 路径别名（默认 @ → ./src）
  component: {           // 第三方组件匹配（可选）
    prefix: 'td-',
    pathPrefix: 'tdesign-miniprogram/',
  },
  cacheStats: false,      // 缓存统计开关（默认 false）
  copyOnly: [],           // 跳过 Babel 直接复制的文件（如 ['big.js', 'ec-canvas/']）
}
```

## 推荐开发流程

1. 使用 `vms dev` 启动开发模式
2. 微信开发者工具打开 `dist/dev` 目录
3. 修改 `.vue` 文件，保存后自动编译
4. 在微信开发者工具中查看效果
5. 使用 `vms build` 生产构建，输出到 `dist/prod`

## 基础语法

### 1. 页面/组件定义

**注意：** 所有 Vue API 必须从 `@unmagic/vue-mini` 导入，不要从 `vue` 导入。

```vue
<script setup lang="ts">
import { ref, computed, onLoad } from '@unmagic/vue-mini'

// 响应式数据
const count = ref(0)
const double = computed(() => count.value * 2)

// 方法
function increment() {
  count.value++
}

// 生命周期
onLoad(() => {
  console.log('页面加载')
})
</script>

<template>
  <div class="container">
    <text>{{ count }}</text>
    <text>{{ double }}</text>
    <button @tap="increment">+1</button>
  </div>
</template>
```

### 2. 事件绑定

**推荐使用 `@tap`** - 小程序原生点击事件，无需转换，性能更好。

#### 简单事件（推荐）

```vue
<!-- 无参函数直接绑定 -->
<button @tap="onSubmit">提交</button>

<!-- 有参函数 -->
<button @tap="onSubmit(formData)">提交</button>
```

#### 箭头函数（用于简单逻辑）

```vue
<!-- 访问事件参数 -->
<input @input="(e) => onInput(e.value)" />

<!-- 多个参数 -->
<button @tap="(e) => onClick(item, e)">点击</button>
```

#### 事件修饰符

| 修饰符          | 编译结果         | 说明              |
| --------------- | ---------------- | ----------------- |
| `.stop`         | `catch:`         | 阻止事件冒泡      |
| `.mut`          | `mut-bind:`      | 互斥事件绑定      |
| `.capture`      | `capture-bind:`  | 捕获阶段监听      |
| `.capture-stop` | `capture-catch:` | 捕获阶段+阻止冒泡 |

```vue
<button @tap.stop="onTap">阻止冒泡</button>
<button @tap.mut="onTap">互斥点击</button>
<button @tap.capture="onTap">捕获阶段</button>
<button @tap.capture-stop="onTap">捕获并阻止</button>
```

#### 事件参数处理规则

| 绑定方式                           | 参数处理             | 使用场景               |
| ---------------------------------- | -------------------- | ---------------------- |
| `@tap="onTap"`                     | 原样传递完整事件对象 | 需要访问事件完整信息时 |
| `@tap="(value) => onTap(value)"`   | 自动加 `.detail`     | 只需要事件值时         |
| `@tap="($event) => onTap($event)"` | 原样传递             | 需要完整事件对象时     |

**注意：** 箭头函数中非 `$event` 的参数会自动从 `event.detail` 取值，不要手动写 `.detail`。

#### 复杂表达式（已支持）

```vue
<!-- 箭头函数执行多条语句 -->
<button @tap="() => { doA(); doB() }">点击</button>

<!-- 条件表达式 -->
<button @tap="() => (isEdit ? update() : create())">保存</button>

<!-- 对象方法调用 -->
<button @tap="() => form.validate().then(submit)">提交</button>
```

**注意：** 虽然支持复杂表达式，但为了代码可读性，复杂逻辑仍建议提取为方法。

#### v-for 中的事件

```vue
<!-- 访问当前项 -->
<div v-for="item of list" :key="item.id" @click="onSelect(item)">
  {{ item.name }}
</div>

<!-- 访问当前项和索引 -->
<div v-for="(item, index) of list" :key="item.id" @click="onSelect(item, index)">
  {{ item.name }}
</div>
```

**注意：** v-for 中使用内联箭头函数时，编译器会智能判断是否需要创建局部引用，只传递 index 优化性能。

### 3. v-for 循环

```vue
<!-- 基础用法 -->
<div v-for="item of items" :key="item.id">{{ item.name }}</div>

<!-- 嵌套循环 -->
<div v-for="group of groups" :key="group.id">
  <div v-for="item of group.items" :key="item.id" @click="item.onClick">
    {{ item.name }}
  </div>
</div>

<!-- 带方法的循环项 -->
<script setup>
const items = ref([{ name: 'Item 1', onClick: () => console.log('clicked') }])
</script>
<template>
  <div v-for="item of items" :key="item.name" @click="item.onClick">
    {{ item.name }}
  </div>
</template>
```

#### :key 规则

- 简单属性路径（如 `item.id`）→ 提取属性名作为 key
- 纯标识符（如 `index`）→ 保留原名
- 嵌套路径（如 `item.data.id`）→ 回退到 `*this` 并发出警告

### 4. 条件渲染

```vue
<!-- v-if / v-else -->
<div v-if="isLoading">加载中...</div>
<div v-else>内容</div>

<!-- v-show -->
<div v-show="isVisible">显示/隐藏</div>

<!-- template + v-if（编译为 block） -->
<template v-if="showContent">
  <div>内容1</div>
  <div>内容2</div>
</template>
<!-- 编译后：<block wx:if="{{showContent}}">...</block> -->
```

### 5. 响应式数据

```vue
<script setup>
import { ref, computed, watch } from '@unmagic/vue-mini'

const count = ref(0)                           // ref
const double = computed(() => count.value * 2)  // computed

watch(count, (newVal, oldVal) => {              // watch
  console.log('count changed:', oldVal, '->', newVal)
})
</script>
```

### 6. :class 绑定

VMS 支持完整的 Vue `:class` 语法，通过 WXS 辅助函数实现。

```vue
<!-- 对象语法 -->
<div :class="{ active: isActive, disabled: isDisabled }"></div>

<!-- 数组语法 -->
<div :class="[baseClass, extraClass]"></div>

<!-- 数组 + 对象混合 -->
<div :class="[baseClass, { active: isActive }]"></div>

<!-- 模板字符串 -->
<div :class="`item-${index}`"></div>

<!-- 三元表达式 -->
<div :class="isActive ? 'active' : 'inactive'"></div>

<!-- 静态 + 动态 -->
<div class="static-class" :class="dynamicClass"></div>
```

**编译原理：** 动态 class 通过自动生成的 WXS 函数处理，该函数会合并所有 class 源并返回最终的 class 字符串。父组件传入的 class 也会被自动注入。

### 7. :style 绑定

VMS 支持完整的 Vue `:style` 语法。

```vue
<!-- 对象语法（camelCase 自动转 kebab-case） -->
<div :style="{ color: 'red', fontSize: '14px' }"></div>

<!-- 数组语法 -->
<div :style="[baseStyles, overridingStyles]"></div>

<!-- 字符串语法 -->
<div :style="'color:red;font-size:14px'"></div>

<!-- 模板字符串 -->
<div :style="`color:${color}`"></div>
```

**注意：** `camelCase` 属性名会自动转换为 `kebab-case`（如 `fontSize` → `font-size`）。WXS 兼容性由编译器自动处理。

## 插槽

### 已支持

- **默认插槽**
- **具名插槽**
- **多子节点插槽**
- 自动添加 `multipleSlots: true` 配置

```vue
<!-- 子组件定义插槽 -->
<template>
  <div>
    <slot></slot>                   <!-- 默认插槽 -->
    <slot name="header"></slot>     <!-- 具名插槽 -->
  </div>
</template>

<!-- 父组件使用 -->
<template>
  <ChildComponent>
    <div>默认插槽内容</div>          <!-- 默认插槽 -->
    <template #header>              <!-- 具名插槽 -->
      <div>头部内容</div>
    </template>
    <template #content>             <!-- 多子节点 -->
      <span>内容1</span>
      <span>内容2</span>
    </template>
  </ChildComponent>
</template>
```

### 插槽限制

- **不支持作用域插槽**（`<template #item="{ data }">`）
- **插槽内容必须使用标签包裹**，不能直接写文本
- 空插槽会被替换为注释节点

### template 节点转 block 规则

- 带 `v-if`/`v-for` 的 `<template>` → `<block>`
- 不带指令的 `<template>` → 直接展开子节点，不生成 `<block>`

## 微信小程序 API

### 导航

```vue
<script setup>
function navigateToPage() {
  wx.navigateTo({ url: '/pages/detail/DetailIndex' })
}
function redirectToPage() {
  wx.redirectTo({ url: '/pages/home/HomeIndex' })
}
function navigateBack() {
  wx.navigateBack()
}
</script>
```

### 数据请求

```vue
<script setup>
import { ref, onLoad } from '@unmagic/vue-mini'

const data = ref(null)

onLoad(async () => {
  const res = await wx.request({ url: 'https://api.example.com/data' })
  data.value = res.data
})
</script>
```

### 存储

```vue
<script setup>
wx.setStorageSync('key', value)
const value = wx.getStorageSync('key')
wx.removeStorageSync('key')
</script>
```

## 组件通信

### 函数传递（需包裹在 fun 对象中）

由于小程序限制，传递给子组件的函数必须包裹在 `fun` 对象中：

```vue
<!-- 父组件 -->
<script setup>
import { ref } from '@unmagic/vue-mini'
const title = ref('标题')
const events = ref({
  fun: {
    onConfirm: () => console.log('确认'),
    onCancel: () => console.log('取消'),
  },
})
</script>

<template>
  <ChildComponent :title="title" :request="events" />
</template>

<!-- 子组件 -->
<script setup>
const { title, request } = defineProps<{
  title: string
  request: { fun: { onConfirm: () => void; onCancel: () => void } }
}>()

function handleConfirm() {
  request.fun.onConfirm()
}
</script>
```

### 页面跳转传参

**方式 1：defineProps（推荐）**

```vue
<script setup lang="ts">
const { id } = defineProps<{ id: string }>()
console.log(id)
</script>
```

**方式 2：onLoad**

```vue
<script setup>
import { onLoad } from '@unmagic/vue-mini'

function goToDetail(item) {
  wx.navigateTo({ url: `/pages/detail/DetailIndex?id=${item.id}` })
}

onLoad((options) => {
  console.log(options.id)
})
</script>
```

## 生命周期

**重要：** 所有生命周期都从 `@unmagic/vue-mini` 导入。`<script setup>` 在 `lifetimes.attached` 阶段执行。

### 页面组件生命周期

| VMS 生命周期        | 小程序原生方法              | 执行时机                |
| ------------------- | --------------------------- | ----------------------- |
| `setup`             | `lifetimes.attached`        | 页面实例创建            |
| `onLoad`            | `methods.onLoad`            | 页面加载，可获取参数    |
| `onShow`            | `methods.onShow`            | 页面显示                |
| `onReady`           | `methods.onReady`           | 页面初次渲染完成        |
| `onHide`            | `methods.onHide`            | 页面隐藏                |
| `onUnload`          | `methods.onUnload`          | 页面卸载                |
| `onPullDownRefresh` | `methods.onPullDownRefresh` | 下拉刷新                |
| `onReachBottom`     | `methods.onReachBottom`     | 上拉触底                |
| `onPageScroll`      | `methods.onPageScroll`      | 页面滚动                |
| `onShareAppMessage` | `methods.onShareAppMessage` | 转发分享                |
| `onShareTimeline`   | `methods.onShareTimeline`   | 分享到朋友圈            |

### 自定义组件生命周期

| VMS 生命周期 | 小程序原生           | 执行时机                |
| ------------ | -------------------- | ----------------------- |
| `setup`      | `lifetimes.attached` | 组件实例创建            |
| `onReady`    | `lifetimes.ready`    | 组件布局完成            |
| `onMove`     | `lifetimes.moved`    | 组件位置变化            |
| `onDetach`   | `lifetimes.detached` | 组件从页面移除          |

**限制：** 自定义组件（非页面）中不能使用 `onLoad`/`onUnload`，请改用 `onReady`/`onDetach`。

### 组件中监听所在页面生命周期

| VMS 生命周期  | 小程序原生                | 执行时机         |
| ------------- | ------------------------- | ---------------- |
| `onShow`      | `pageLifetimes.show`      | 所在页面显示     |
| `onHide`      | `pageLifetimes.hide`      | 所在页面隐藏     |
| `onResize`    | `pageLifetimes.resize`    | 所在页面尺寸变化 |

## 限制说明

### 不支持的 Vue 特性

| 特性                | 说明                                   |
| -------------------- | -------------------------------------- |
| `v-model`            | 不支持双向绑定                         |
| `defineModel`        | 编译宏不支持                           |
| `defineSlots`        | 编译宏不支持                           |
| `v-bind="obj"`       | 需要逐个绑定属性                       |
| 组合式函数           | `useTemplateRef`, `useSlots` 等不支持  |
| Vue 内置组件         | `<transition>`, `<keep-alive>` 等     |
| 作用域插槽           | 不支持数据传递给插槽                   |
| `.prevent` 修饰符    | 需手动处理阻止默认行为                 |

### 命名注意事项

**props 属性名建议不要以 `data` 开头**（`data-` 是小程序 `dataset` 的保留前缀，VMS 编译器会自动生成 `data-a`、`data-b` 等属性用于传递 v-for 索引等数据，可能产生冲突）：

| 不推荐       | 推荐                       |
| ------------ | -------------------------- |
| `dataList`   | `list`, `items`, `records` |
| `dataType`   | `type`, `category`, `kind` |
| `dataSource` | `source`, `origin`, `from` |

### WXS 环境限制（编译器已自动处理）

模板中的动态表达式会被编译为 WXS（WeiXin Script），WXS 不支持以下语法，VMS 编译器会自动降级：

- 可选链 `?.` → 降级为条件判断
- `void 0` → 替换为 `undefined`
- `Array.isArray()` → 替换为类型检查
- 箭头函数 → 转换为普通函数
- 模板字符串 → 转换为字符串拼接
- `$` 变量名 → 替换为 `_`（避免与 WXS 内置冲突）

## 常见问题

### Q1: 模板中直接使用 wx 报错

在模板中直接使用 `wx` 会出现 TypeScript 错误。请在 script 中声明函数：

```vue
<script setup>
function navigateToDetail() {
  wx.navigateTo({ url: '/pages/detail' })
}
</script>

<template>
  <button @tap="navigateToDetail">跳转</button>
</template>
```

### Q2: 内联箭头函数的 .detail 处理

```vue
<!-- 正确：自动从 event.detail 取值 -->
<input @input="(value) => onInput(value)" />

<!-- 错误：会变成 e.detail.detail -->
<input @input="(e) => onInput(e.detail.value)" />

<!-- 需要完整事件对象时用 $event -->
<button @tap="($event) => onTap($event.currentTarget.dataset)">点击</button>
```

### Q3: v-for 中访问父级变量

```vue
<template>
  <div v-for="group of groups" :key="group.name">
    <div v-for="item of group.items" :key="item.name" @tap="onSelect(group, item)">
      {{ group.name }} - {{ item.name }}
    </div>
  </div>
</template>
```

### Q4: 首次渲染前 undefined 导致 TypeError

`@unmagic/vue-mini` 数据初始化时 undefined 值可能导致首次渲染前 WXS 抛出 TypeError。确保响应式数据在使用前有合理的初始值。

## 调试技巧

1. **查看编译输出** - 检查 `dist/dev/` 目录下的生成文件
2. **使用微信开发者工具** - 查看控制台输出和页面结构
3. **检查响应式数据** - 在开发者工具 AppData 面板查看
4. **查看 WXML** - 确认模板正确编译
5. **查看 WXS** - 动态 class/style 会生成 `<wxs>` 标签，检查生成逻辑

## 编译器架构（简要）

```
CLI 层 (cli.ts)        → 构建流程控制、文件监听、依赖扫描
    ↓
转换层 (transformer.ts) → 协调三路转换，输出 .wxml/.js/.wxss/.json
    ↓
模板层 (template/)      → Vue 模板 → WXML，管道式转换器
    ├── nodeProps/clazz.ts   → :class 处理（WXS 生成）
    ├── nodeProps/style.ts   → :style 处理
    ├── nodeProps/event.ts   → 事件处理器
    ├── nodeProps/slot.ts    → 插槽转译
    ├── expression.ts        → 表达式降级（babel）
    └── wxsPolyfill.ts       → WXS polyfill
    ↓
脚本层 (script/)        → script setup → defineComponent
    ├── macro/              → defineProps/defineEmits/defineExpose
    └── collectImports.ts   → 依赖收集
```

**核心技术：** `@vue/compiler-sfc` 解析 + `@babel/core` 转换 + `rollup` 打包
