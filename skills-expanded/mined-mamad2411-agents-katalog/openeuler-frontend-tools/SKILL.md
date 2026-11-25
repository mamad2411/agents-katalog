---
name: openeuler-frontend-tools
description: openEuler Portal 前端开发工具和规范集合。当需要使用项目中的通用 composables、SCSS mixins 或工具函数时使用此 skill。使用场景：(1) 需要使用响应式屏幕适配功能时查找 useScreen composable，(2) 需要使用响应式字体 mixin 时查找 font.scss，(3) 需要使用 URL 参数、Cookie 等工具函数时查找 utils/common.ts，(4) 需要使用国际化、剪贴板、防抖搜索等 composables 时查找对应的工具
---

# openEuler Portal 前端开发工具

本 skill 提供了 openEuler Portal 项目中所有通用开发工具的完整指南，包括 Vue Composables、SCSS Mixins 和工具函数。

## 工具分类

### 1. Composables（组合式函数）

位于 `openEuler-portal/app/.vitepress/src-new/composables/` 目录，提供可复用的 Vue 3 Composition API 功能：

- **useScreen** - 响应式屏幕尺寸检测和适配
- **useLocale** - 国际化语言切换
- **useClipboard** - 剪贴板操作
- **useDebounceSearch** - 防抖搜索
- **useCheckbox** - 复选框状态管理
- **useScrollBottom** - 滚动到底部检测
- **useInViewDuration** - 元素可见时长统计

详细使用方法请参考 [Composables 参考文档](references/composables.md)

### 2. SCSS Mixins（样式混入）

位于 `openEuler-portal/app/.vitepress/src-new/assets/style/mixin/` 目录，提供响应式样式和通用样式混入：

- **screen.scss** - 响应式断点 mixin
- **font.scss** - 响应式字体大小 mixin（display1-3, h1-h4, text1-2, tip1-2）
- **common.scss** - 通用样式 mixin（暗色模式、文本截断、滚动条、悬停效果等）

详细使用方法请参考 [Mixins 参考文档](references/mixins.md)

### 3. Utils（工具函数）

位于 `openEuler-portal/app/.vitepress/src-new/utils/` 目录，提供通用工具函数：

- **common.ts** - URL 参数、Cookie、时间格式化、Git 平台检测等
- **locale.ts** - 语言环境获取

详细使用方法请参考 [Utils 参考文档](references/utils.md)

## 快速开始

### 使用 Composable

```vue
<script setup lang="ts">
import { useScreen } from '~@/composables/useScreen';
import { useLocale } from '~@/composables/useLocale';

const { isPhone, isPad, isLaptop, current } = useScreen();
const { t, locale, isZh, changeLocale } = useLocale();
</script>
```

### 使用 SCSS Mixin

```vue
<style lang="scss" scoped>
@use '~@/assets/style/mixin/font.scss' as *;
@use '~@/assets/style/mixin/screen.scss' as *;

.title {
  @include h1; // 使用响应式标题样式
}

.content {
  @include text1; // 使用响应式正文样式
  
  @include respond-to('phone') {
    padding: 16px;
  }
}
</style>
```

### 使用工具函数

```typescript
import { getUrlParam, setCookie, changeTimeStamp } from '~@/utils/common';
import { getCurrentLocale } from '~@/utils/locale';

// 获取 URL 参数
const id = getUrlParam('id');

// 设置 Cookie
setCookie('theme', 'dark', 7);

// 时间戳格式化
const date = changeTimeStamp(Date.now());

// 获取当前语言
const lang = getCurrentLocale();
```

## 使用场景

### 场景 1：响应式页面开发

需要根据屏幕尺寸调整布局或样式时：

1. 使用 `useScreen` composable 获取屏幕尺寸状态
2. 使用 `@include respond-to()` mixin 编写响应式样式
3. 使用 `font.scss` 中的 mixin 确保字体响应式适配

### 场景 2：国际化功能

需要实现多语言切换时：

1. 使用 `useLocale` composable 进行语言切换
2. 使用 `getCurrentLocale` 获取当前语言环境
3. 在模板中使用 `t()` 函数进行文本翻译

### 场景 3：表单和交互功能

需要实现表单、搜索、剪贴板等功能时：

1. 使用 `useCheckbox` 管理复选框状态
2. 使用 `useDebounceSearch` 实现防抖搜索
3. 使用 `useClipboard` 实现复制功能

### 场景 4：样式开发

需要应用项目标准样式时：

1. 使用 `font.scss` 中的字体 mixin 确保字体大小符合规范
2. 使用 `common.scss` 中的通用 mixin（文本截断、滚动条样式等）
3. 使用 `screen.scss` 中的响应式断点

## 参考资源

- [Composables 完整参考](references/composables.md) - 所有 composables 的详细使用方法
- [Mixins 完整参考](references/mixins.md) - 所有 SCSS mixins 的详细使用方法
- [Utils 完整参考](references/utils.md) - 所有工具函数的详细使用方法

## 注意事项

1. **路径别名**：项目使用 `~@/` 作为 `src-new` 目录的别名；新项目通常用 `@/`，导入路径相应调整
2. **响应式断点**：屏幕断点定义在 `screen.scss` 中，与 `useScreen` composable 保持一致
3. **字体规范**：使用 `font.scss` 中的 mixin 确保字体大小符合设计规范
4. **类型安全**：所有 composables 和 utils 都提供完整的 TypeScript 类型定义

## 在新项目中配置 SCSS Mixin 文件

SCSS mixin 文件不随 npm 包分发，需要在项目中手动创建。参考 [Mixins 参考文档](references/mixins.md) 在以下路径创建同名文件：

```
src/assets/style/mixin/
├── screen.scss   ← 响应式断点（respond-to mixin）
├── font.scss     ← 响应式字体（h1~h4, text1-2, tip1-2, display1-3 mixin）
└── common.scss   ← 通用样式（in-dark, text-truncate, scrollbar, hover mixin）
```

**断点值**（与 opendesign token 体系保持一致）：

| 断点名 | 范围 |
|--------|------|
| `phone` | 0–600px |
| `pad_v` | 601–840px |
| `pad_h` | 841–1200px |
| `laptop` | 1201–1440px |
| 桌面（无 mixin） | >1440px（默认样式） |

**vite.config.ts 配置**（全局自动注入，所有 SCSS 文件无需手动 `@use`）：

```typescript
css: {
  preprocessorOptions: {
    scss: {
      additionalData: `
@use "@/assets/style/mixin/screen.scss" as *;
@use "@/assets/style/mixin/font.scss" as *;
@use "@/assets/style/mixin/common.scss" as *;
`,
    },
  },
},
```

⚠️ **配置后禁止在各 `.vue` 文件或 `.scss` 文件中手动 `@use` 上述 mixin 文件**，否则会报"cannot use module twice"错误。

⚠️ **`screen.scss` map 值必须用引号包裹**（字符串），否则 SCSS 把括号解析为 list 导致编译错误：

```scss
// ✅ 正确
$breakpoints: (
  '<=pad_v': '(max-width: 840px)',
  'laptop':  '(min-width: 1201px) and (max-width: 1440px)',
);

// ❌ 错误（括号被解析为 SCSS list）
$breakpoints: (
  '<=pad_v': (max-width: 840px),
);
```











