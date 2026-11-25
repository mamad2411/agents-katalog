---
name: opendesign-scripts
description: OpenDesign 构建脚本工具使用指南。当需要使用 @opensig/open-scripts CLI 工具进行图标生成、SVG 清理、组件构建、样式编译、设计令牌生成时使用此 skill。支持 5 个命令：gen:icon（SVG 转 Vue 图标组件）、clean:svg（SVG 清理优化）、build:component（Vue 组件库构建）、build:style（SCSS 样式编译）、gen:token（设计令牌 CSS 变量生成）。使用场景：(1) 配置和执行构建脚本，(2) 编写图标/令牌配置文件，(3) 了解构建流程和命令用法
---

# OpenDesign Scripts 使用指南

`@opensig/open-scripts` 是 OpenDesign 生态的 CLI 构建工具包，提供从 SVG 图标生成到组件库打包的全流程构建能力。

## 安装

```bash
pnpm add -D @opensig/open-scripts
# 或
npm install -D @opensig/open-scripts
```

安装后即可在 `package.json` 的 `scripts` 中使用 `open-scripts` 命令。

---

## 谁需要哪些命令？

open-scripts 的 5 个命令分为两类使用场景。请根据你的项目类型选择：

### 组件库开发（如 @opensig/opendesign 本身）

构建和发布组件库 npm 包时，需要使用**全部 5 个命令**：

| 命令 | 何时使用 |
|------|---------|
| `gen:icon` | 新增/修改 SVG 图标后，重新生成图标 Vue 组件 |
| `clean:svg` | 收到设计师交付的原始 SVG 后，先清理再交给 `gen:icon` |
| `build:component` | 发布前构建组件库产物（ES/CJS/UMD） |
| `build:style` | 发布前编译 SCSS 样式为 CSS 产物 |
| `gen:token` | 设计令牌 JSON 更新后，重新生成主题 CSS 变量文件（用于 `@opensig/opendesign-token` 包的构建） |

标准构建流程：`gen:icon → build:component → build:style`

### 业务项目开发（使用 OpenDesign 组件库的网站/应用）

业务项目**不需要** `build:component`、`build:style` 和 `gen:token`：
- `build:component` / `build:style` 专门用于构建组件库 npm 包，业务项目直接安装 `@opensig/opendesign` 即可
- `gen:token` 专门用于构建 `@opensig/opendesign-token` 包，业务项目直接安装该包并引入对应主题的 CSS 文件即可（参见 opendesign-components skill 的安装章节）

业务项目可能用到的命令：

| 命令 | 何时使用 |
|------|---------|
| `gen:icon` | 项目有自己的自定义图标（非组件库内置图标）时，将 SVG 转为 Vue 组件以便统一使用 |
| `clean:svg` | 清理设计师交付的原始 SVG（可选，视 SVG 质量而定） |

---

## 命令索引

- [gen:icon](#genicon) — 从 SVG 文件生成 Vue 图标组件（组件库 + 业务项目） · [参考文档](references/gen-icon.md)
- [clean:svg](#cleansvg) — 清理和优化 SVG 文件（组件库 + 业务项目） · [参考文档](references/clean-svg.md)
- [build:component](#buildcomponent) — 构建 Vue 组件库（仅组件库开发） · [参考文档](references/build-component.md)
- [build:style](#buildstyle) — 编译 SCSS 样式为 CSS（仅组件库开发） · [参考文档](references/build-style.md)
- [gen:token](#gentoken) — 从 JSON 生成设计令牌 CSS 变量（仅令牌包构建） · [参考文档](references/gen-token.md)

---

## gen:icon

把设计师提供的 SVG 图标文件，按 fill/stroke/color 三种类型分类，通过 SVGO 优化后自动转成可直接导入使用的 Vue 单文件组件。

**适用场景**：组件库开发和业务项目均可使用。业务项目中当设计稿包含非组件库内置的自定义图标时，使用此命令统一管理。

### SVG 资源从设计稿到代码的工作流

当设计稿（Pixso/Figma 等）中包含可以转化为 SVG 图标的切图时，应按以下流程操作：

1. **优先通过 MCP 获取**：如果设计工具提供了 MCP（Model Context Protocol）能力，应优先调用其 MCP 接口批量导出 SVG 资源，而非手动逐个导出
2. **手动导出 SVG**：若无 MCP 能力，则将设计稿中的图标切图逐个导出为 `.svg` 格式
3. **按类型分类存放**：根据图标内容判断类型，将 SVG 放入对应子目录（见下方「SVG 导出规范与分类规则」）
4. **可选清理**：如果导出的 SVG 包含冗余属性，先运行 `clean:svg` 清理
5. **全部导出完成后**，运行 `gen:icon` 命令一次性生成所有图标的 Vue 组件
6. 在业务代码中导入使用（见下方「图标组件的导入方式」）

> **注意**：应在所有 SVG 切图都导出完毕后再统一运行 `gen:icon`，因为该命令每次执行会清空输出目录并重新生成全部组件。

### 图标新增与修改的最佳实践

当任务涉及图标的**新增**或**修改**时，必须遵循以下原则：

1. **优先复用已有图标**：在新增图标前，先检查 SVG 源文件目录（`input` 配置指向的 `fill/`、`stroke/`、`color/` 子目录）以及已生成的图标组件，确认是否已存在相同或语义相近的图标。若已有可用图标，直接导入使用，不重复添加
2. **采用增量策略**：需要新增图标时，仅将新的 SVG 文件**追加**到对应的 `fill/`、`stroke/`、`color/` 子目录中，**不要删除或覆盖**已有的 SVG 文件。`gen:icon` 会从 `input` 目录读取全部 SVG 并重新生成组件，因此只需确保新文件正确放入即可
3. **修改图标时就地替换**：若需修改已有图标的视觉样式，直接用新版 SVG **替换同名文件**，保持文件名不变，这样生成的组件名和所有引用代码都无需改动

**检查已有图标的方法**：
- 查看 SVG 源文件目录下各子目录中的文件名，按命名规范判断语义是否匹配
- 搜索已生成的图标组件目录（`output` 配置指向的目录），按组件名查找
- 若项目使用组件库内置图标（`@opensig/opendesign`），还应检查组件库中是否已内置所需图标

> **反模式**：不要为了"干净"而清空 SVG 源文件目录后重新放入所有文件——这会导致 Git 历史中出现大量无意义的删除+新增记录，且容易遗漏已有图标。

### SVG 导出规范与分类规则

**导出规范**：
- 图标应导出为**留有适当白边的正方形**画布，优先使用 **24×24px** 尺寸
- 若图标有特殊尺寸需求，仍按标准尺寸导出 SVG，在调用处通过 CSS `font-size` 或 `width`/`height` 调整显示大小
- 导出时移除不必要的图层、蒙版和裁切路径
- **需要动态样式的路径**：若某个 `<path>` 需要在交互时单独变色或改变样式，应在设计工具中为该路径设置有意义的 **ID**（如 `highlight`、`badge`），`gen:icon` 的 SVGO 流程会自动将 `id` 转为 `class`，调用方即可通过 CSS 类选择器控制该路径的样式

```vue
<!-- 示例：通过类名控制 SVG 内部路径的颜色 -->
<OIcon :icon="OIconNotification" class="my-icon" />

<style scoped>
/* 设计师在 SVG 中为小红点路径设置了 id="badge"，生成后变为 class="badge" */
.my-icon :deep(.badge) {
  fill: red;
}
</style>
```

**分类规则**——根据图标的视觉内容判断放入哪个子目录：

| 目录 | 判断依据 | 生成后颜色控制方式 | 典型场景 |
|------|---------|------------------|---------|
| `fill/` | 图标以**实心填充**为主，颜色由 `fill` 属性控制 | 通过 CSS `color` 统一变色 | 实心箭头、实心勾选、实心收藏星 |
| `stroke/` | 图标以**线条描边**为主，颜色由 `stroke` 属性控制 | 通过 CSS `color` 统一变色 | 线框关闭、线框搜索、线框设置 |
| `color/` | 图标包含**多种固定颜色**，不应被 CSS 统一变色 | 保留 SVG 原始颜色 | 品牌 Logo、彩色插图、多色状态图标 |

> **判断技巧**：用文本编辑器打开 SVG，如果 `<path>` 等元素主要使用 `fill` 属性着色 → `fill/`；主要使用 `stroke` 属性着色 → `stroke/`；同时使用多种不同颜色值 → `color/`。

### SVG 文件命名规范

SVG 文件名直接决定生成的 Vue 组件名（如 `arrow-right.svg` → `OIconArrowRight`），应遵循统一的命名规则：

**命名格式**：`{语义名}[-{形态变体}].svg`

- **语义名**：描述图标含义，使用 kebab-case（小写 + 连字符），由「对象」或「动作」构成
- **形态变体**（可选）：同一语义的不同视觉形态后缀

**语义名选取规则**：

| 优先级 | 构成方式 | 示例 |
|--------|---------|------|
| 1 | 单个动作或对象（含义明确时） | `search.svg`、`home.svg`、`close.svg` |
| 2 | 动作 + 对象 | `file-download.svg`、`user-add.svg`、`link-copy.svg` |
| 3 | 对象 + 限定词 | `arrow-right.svg`、`chevron-down.svg`、`caret-up.svg` |

**常见形态变体后缀**：

| 后缀 | 含义 | 示例 |
|------|------|------|
| `-circle` | 带圆形背景 | `check-circle.svg`、`info-circle.svg` |
| `-square` | 带方形背景 | `plus-square.svg` |
| `-line` | 线性描边版本 | `heart-line.svg` |
| `-solid` | 实心填充版本 | `heart-solid.svg` |

**常用语义词参考**：

| 类别 | 推荐词汇 |
|------|---------|
| 导航 | `arrow-{up/down/left/right}`、`chevron-{方向}`、`caret-{方向}`、`expand`、`collapse`、`menu`、`more` |
| 操作 | `add`、`delete`、`edit`、`search`、`download`、`upload`、`save`、`copy`、`share`、`refresh`、`close`、`filter`、`sort` |
| 对象 | `file`、`folder`、`user`、`home`、`calendar`、`mail`、`image`、`link`、`bell`、`lock`、`key`、`settings` |
| 状态 | `check`、`warning`、`error`、`info`、`loading`、`success`、`question` |
| 媒体 | `play`、`pause`、`stop`、`mute`、`volume` |

**命名原则**：
- 以图标的**视觉含义/用途**命名，不以业务功能命名（`close.svg` 而非 `dialog-dismiss.svg`）
- 同一组相关图标保持前缀一致（`arrow-up`、`arrow-down`、`arrow-left`、`arrow-right`）
- 避免冗余前缀——文件已在 `fill/`、`stroke/`、`color/` 子目录中，无需在文件名中重复类型信息

### 图标组件的导入方式

生成的图标组件支持多种导入方式，根据项目结构选择合适的方式：

```vue
<script setup>
// 方式 1：从组件库包导入（使用组件库内置图标）
import { OIconArrowRight, OIconClose } from '@opensig/opendesign';

// 方式 2：通过路径别名导入（业务项目自定义图标，需在 vite.config / tsconfig 中配置别名）
import { OIconCustom } from '@/icon-components';

// 方式 3：相对路径导入
import { OIconCustom } from '../icon-components';

// 方式 4：从 monorepo 的其他子包导入（通过包名引用）
import { DocIconLogo } from '@my-org/docs-icons';
</script>
```

**最佳实践**：
- **组件库内置图标**直接从 `@opensig/opendesign` 导入，无需自己运行 `gen:icon`
- **业务项目自定义图标**建议配置路径别名（如 `@/icon-components`），避免深层相对路径
- **monorepo 中跨包共享图标**建议将图标生成到独立子包并发布，其他包通过包名导入

```bash
open-scripts gen:icon --config ./icons/icon.config.ts
```

**配置文件核心字段**：

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `input` | `string` | 否 | `'./svgs'` | SVG 源文件目录，需包含 `fill/`、`stroke/`、`color/` 子目录 |
| `output` | `string` | 否 | `'./components/'` | 生成的 Vue 组件输出目录 |
| `prefix` | `string` | 否 | `''` | 组件名前缀（如 `'o-'` 生成 `OIconXxx`） |
| `componentClass` | `string` | 否 | `'svg-icon'` | SVG 根元素的 CSS 类名 |
| `renderOnServer` | `boolean` | 否 | `false` | 是否支持 SSR（false 时图标仅客户端渲染） |

### 配置示例

```typescript
// icon.config.ts
export default {
  input: './svgs',
  output: '../src/icon-components/',
  componentClass: 'o-svg-icon',
  prefix: 'o-',
};
```

**SVG 目录结构要求**：
```
svgs/
├── fill/       ← 填充型图标（移除 fill 属性，通过 CSS color 控制颜色）
│   ├── arrow-right.svg
│   └── check.svg
├── stroke/     ← 描边型图标（移除 stroke 属性，通过 CSS color 控制颜色）
│   └── close.svg
└── color/      ← 多色图标（保留原始颜色）
    └── logo.svg
```

> 详细配置说明，请查看 [references/gen-icon.md](references/gen-icon.md)

---

## clean:svg

使用 SVGO 批量清理和优化 SVG 文件，移除冗余属性、样式元素和脚本，输出精简后的 SVG 文件。通常在 `gen:icon` 之前使用，用于预处理设计师交付的原始 SVG。

**适用场景**：组件库开发和业务项目均可使用。当设计师导出的 SVG 包含多余的 `<style>`、`<script>`、内联样式等冗余信息时，先用此命令批量清理。

```bash
open-scripts clean:svg --config ./icons/cleansvg.config.ts
```

**配置文件核心字段**：

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `input` | `string` | 否 | `'./src/icons/svgs'` | SVG 源文件目录 |
| `output` | `string` | 否 | `'./src/icons/output/'` | 清理后的输出目录 |
| `svgo` | `Config` | 否 | 内置默认配置 | SVGO 优化配置 |

### 配置示例

```typescript
// cleansvg.config.ts
export default {
  input: './svgs',
  output: './_svgs',
};
```

> 详细配置说明，请查看 [references/clean-svg.md](references/clean-svg.md)

---

## build:component

使用 Vite 构建 Vue 组件库，输出三种模块格式：ES Module（`es/`）、CommonJS（`lib/`）和 UMD（`dist/`）。同时生成 TypeScript 类型声明文件。此命令不接受配置文件，直接在组件库包根目录执行。

**适用场景**：仅组件库开发使用。业务项目直接安装 `@opensig/opendesign` npm 包即可，不需要自己构建组件库。

```bash
open-scripts build:component
```

**构建产物**：

| 目录 | 格式 | 说明 |
|------|------|------|
| `es/` | ESM（`.mjs`） | 保留模块结构，支持 tree-shaking |
| `lib/` | CJS（`.js`） | CommonJS 格式，兼容 Node.js |
| `dist/opendesign.js` | UMD | 浏览器直接引入 |
| `dist/opendesign.min.js` | UMD（压缩） | 生产环境使用 |
| `dist/opendesign-icon.js` | UMD | 图标单独打包 |
| `dist/opendesign-icon.min.js` | UMD（压缩） | 图标生产包 |

> 详细说明，请查看 [references/build-component.md](references/build-component.md)

---

## build:style

编译组件库的 SCSS 样式文件为 CSS，生成多种引入方式的样式产物。此命令不接受配置文件，读取硬编码的 `./src` 目录作为输入。

**适用场景**：仅组件库开发使用。业务项目通过 `import '@opensig/opendesign/es/index.css'` 引入已编译好的样式，不需要自己编译 SCSS。

```bash
open-scripts build:style
```

**构建产物**：

| 产物 | 说明 |
|------|------|
| `es/**/*.scss` + `lib/**/*.scss` | 原始 SCSS 文件拷贝 |
| `es/**/*.css` + `lib/**/*.css` | 编译后的 CSS |
| `es/**/css.js` + `lib/**/css.js` | CSS 引入入口（替代 SCSS 入口） |
| `dist/index.css` | 全量样式 |
| `dist/index.min.css` | 全量样式（压缩） |
| `dist/theme/*/index.css` | 各主题样式 |

> 详细说明，请查看 [references/build-style.md](references/build-style.md)

---

## gen:token

从 JSON 格式的设计令牌定义文件，生成多主题的 CSS 变量文件和 VS Code 代码片段文件。用于将设计师在 Pixso/Figma 等工具中导出的令牌转换为前端可用的 CSS 自定义属性。

**适用场景**：仅用于 `@opensig/opendesign-token` 令牌包的构建。业务项目**不需要**运行此命令——直接安装 `@opensig/opendesign-token` 并引入对应主题的 CSS 文件即可：

```bash
pnpm add @opensig/opendesign-token
```

```typescript
// main.ts — 以 openEuler 社区为例
import '@opensig/opendesign-token/themes/e.light.token.css'
import '@opensig/opendesign-token/themes/e.dark.token.css'
```

```bash
open-scripts gen:token --config ./tokens/token.config.ts
```

**配置文件核心字段**：

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `prefix` | `string` | 是 | — | CSS 变量前缀（如 `'--o-'`） |
| `output` | `string` | 否 | `'./'` | 输出目录 |
| `tokenFile` | `string[]` | 是 | — | 令牌 JSON 文件路径数组 |
| `themeMap` | `Array<{valueKey, name, root?}>` | 是 | — | 主题映射（定义各主题的 CSS 选择器） |
| `codeSnippetsFile` | `string` | 否 | — | VS Code 代码片段输出路径 |

### 配置示例

```typescript
// token.config.ts
export default {
  prefix: '--o-',
  output: './dist',
  themeMap: [
    { valueKey: 'light', name: ['o.light', 'default'] },
    { valueKey: 'dark', name: 'o.dark' },
    { valueKey: 'light', name: 'o', root: true },
  ],
  tokenFile: ['./opendesign-token.json'],
  codeSnippetsFile: './dist/opendesign.token.code-snippets',
};
```

> 详细配置说明，请查看 [references/gen-token.md](references/gen-token.md)

---

## 典型构建流程

### 组件库发布构建

在 OpenDesign 组件库中，发布前的标准执行顺序为：

```
gen:icon → build:component → build:style
```

对应 `package.json` 配置：

```json
{
  "scripts": {
    "gen:icon": "open-scripts gen:icon --config ./icons/icon.config.ts",
    "clean:svg": "open-scripts clean:svg --config ./icons/cleansvg.config.ts",
    "build:component": "open-scripts build:component",
    "build:style": "open-scripts build:style",
    "gen:token": "open-scripts gen:token --config ./tokens/token.config.ts",
    "build": "pnpm gen:icon && pnpm build:component && pnpm build:style"
  }
}
```

### 业务项目使用

业务项目只需配置自己用到的命令：

```json
{
  "scripts": {
    "gen:icon": "open-scripts gen:icon --config ./icons/icon.config.ts"
  }
}
```

### 命令依赖关系

| 命令 | 前置依赖 | 说明 |
|------|---------|------|
| `clean:svg` | 无 | 可独立执行，用于预处理 SVG |
| `gen:icon` | `clean:svg`（可选） | 建议先清理 SVG，但非强制 |
| `build:component` | `gen:icon` | 需要先生成图标组件，才能一起打包 |
| `build:style` | 无 | 与 `build:component` 独立，但通常在其后执行 |
| `gen:token` | 无 | 独立执行，不依赖其他命令 |

---

## 构建产物的 Git 忽略规则

**所有命令的输出目录都是自动生成的产物，不应纳入版本控制。** 请在项目 `.gitignore` 中添加对应规则。执行任何命令前，应先检查 `.gitignore` 是否已覆盖该命令的输出目录，若未覆盖则立即添加。

推荐的 `.gitignore` 配置：

```gitignore
# open-scripts 构建产物（自动生成，勿提交）

# gen:icon 生成的图标组件
icon-components

# clean:svg 清理后的 SVG 输出
_svgs

# build:component 构建产物
es
lib
dist

# gen:token 生成的令牌 CSS（若 output 为 dist 则已被上方覆盖）
```

> **注意**：如果某个命令的 `output` 配置为自定义路径，请确保该路径也被 `.gitignore` 覆盖。

---

## 首次使用：自动创建缺失的文件和目录

当命令需要配置文件或输入目录但对应文件/目录不存在时，应按以下最佳实践自动创建：

### gen:icon

若配置文件和输入目录缺失，创建以下结构：

```
icons/
├── icon.config.ts          ← 配置文件
└── svgs/                   ← input 目录
    ├── fill/               ← 存放单色填充图标
    ├── stroke/             ← 存放单色描边图标
    └── color/              ← 存放多色图标
```

配置文件模板：
```typescript
// icons/icon.config.ts
export default {
  input: './svgs',
  output: '../src/icon-components/',
  componentClass: 'o-svg-icon',
  prefix: 'o-',
};
```

同时在 `package.json` 中添加：
```json
{
  "scripts": {
    "gen:icon": "open-scripts gen:icon --config ./icons/icon.config.ts"
  }
}
```

并确保 `.gitignore` 中包含 `icon-components`。

### clean:svg

若配置文件和输入目录缺失，创建以下结构：

```
icons/
├── cleansvg.config.ts      ← 配置文件
└── svgs/                   ← input 目录（可与 gen:icon 共用）
```

配置文件模板：
```typescript
// icons/cleansvg.config.ts
export default {
  input: './svgs',
  output: './_svgs',
};
```

同时在 `package.json` 中添加：
```json
{
  "scripts": {
    "clean:svg": "open-scripts clean:svg --config ./icons/cleansvg.config.ts"
  }
}
```

并确保 `.gitignore` 中包含 `_svgs`。

### gen:token

若配置文件和令牌 JSON 文件缺失，创建以下结构：

```
tokens/
├── token.config.ts          ← 配置文件
└── opendesign-token.json    ← 令牌 JSON 数据（从设计工具导出）
```

配置文件模板：
```typescript
// tokens/token.config.ts
export default {
  prefix: '--o-',
  output: './dist',
  themeMap: [
    { valueKey: 'light', name: ['o.light', 'default'] },
    { valueKey: 'dark', name: 'o.dark' },
  ],
  tokenFile: ['./opendesign-token.json'],
};
```

同时在 `package.json` 中添加：
```json
{
  "scripts": {
    "gen:token": "open-scripts gen:token --config ./tokens/token.config.ts"
  }
}
```

### build:component / build:style

这两个命令不需要配置文件，但要求项目具备特定的源码目录结构。若结构缺失，说明项目尚未完成组件库源码搭建，不应直接创建空目录——应先完成组件开发再使用这两个命令。

---

## Monorepo 项目中的路径规划

在 monorepo 项目中，各命令的配置文件、输入目录和输出目录应放在**对应子包内**，路径相对于配置文件所在目录解析。以下是推荐的目录结构（以 opendesign-components 为参考）：

### 组件库包（如 `packages/opendesign/`）

```
packages/opendesign/
├── package.json                          ← scripts 定义在此
├── icons/
│   ├── icon.config.ts                    ← gen:icon 配置
│   ├── cleansvg.config.ts                ← clean:svg 配置
│   └── svgs/                             ← SVG 源文件（提交到 git）
│       ├── fill/
│       ├── stroke/
│       └── color/
├── src/
│   ├── index.ts                          ← 组件主入口
│   ├── icon/
│   │   └── index.ts                      ← 图标入口
│   ├── icon-components/                  ← gen:icon 输出（git 忽略）
│   └── {component}/
│       └── style/
│           └── index.scss
├── es/                                   ← build:component 输出（git 忽略）
├── lib/                                  ← build:component 输出（git 忽略）
└── dist/                                 ← build:component UMD 输出（git 忽略）
```

对应 `package.json` scripts：
```json
{
  "scripts": {
    "gen:icon": "open-scripts gen:icon --config ./icons/icon.config.ts",
    "clean:svg": "open-scripts clean:svg --config ./icons/cleansvg.config.ts",
    "build:component": "open-scripts build:component",
    "build:style": "open-scripts build:style",
    "build": "pnpm gen:icon && pnpm build:component && pnpm build:style"
  }
}
```

icon.config.ts 中 `output: '../src/icon-components/'` 表示相对于 `icons/` 目录向上一级到包根目录再进入 `src/icon-components/`。

### 业务应用包（如 `packages/docs/`）

```
packages/docs/
├── package.json
├── icons/
│   ├── icon.config.ts                    ← gen:icon 配置
│   └── svgs/
│       ├── fill/
│       ├── stroke/
│       └── color/
└── src/
    └── icon-components/                  ← gen:icon 输出（git 忽略）
```

业务应用包通常只使用 `gen:icon`，`prefix` 应使用区别于组件库的前缀（如 `'doc-'`）以避免命名冲突：

```typescript
// packages/docs/icons/icon.config.ts
export default {
  input: './svgs',
  output: '../src/icon-components/',
  componentClass: 'o-svg-icon',
  prefix: 'doc-',                        // 使用不同前缀，避免与组件库图标冲突
};
```

### 关键原则

- **配置文件放在子包内**：每个子包有自己的配置，通过 `--config` 参数指向
- **input 路径相对于配置文件**：`input: './svgs'` 表示与配置文件同级的 `svgs/` 目录
- **output 路径相对于配置文件**：`output: '../src/icon-components/'` 表示从配置文件位置出发的相对路径
- **SVG 源文件提交到 git**：`input` 目录（`svgs/`）包含设计师交付的 SVG 原始资源，应纳入版本控制
- **生成产物不提交**：`output` 目录和构建产物目录应全部被 `.gitignore` 覆盖
- **各子包使用不同 prefix**：monorepo 中多个包使用 `gen:icon` 时，应设置不同的 `prefix`（如 `'o-'`、`'doc-'`）以防止组件名冲突
