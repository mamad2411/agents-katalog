---
name: frontend-code-generator-vue3
description: 页面重构 Skill，用于基于设计稿（Figma 设计稿 / 页面截图）输出高度还原的 Vue3 规范页面代码。输入设计稿或截图，输出符合数据/DOM分离、目录规范、响应式适配的完整页面文件。当用户提供设计稿/截图并要求开发前端页面时触发。
version: 1.0.0
icon: "🛠️"
---

# 页面重构规范

**核心目标：输入一个设计稿（Figma / 截图） → AI 输出高度还原、规范合规的重构页面代码。**

## 输入与输出

### 用户需提供
- **设计稿**（以下任一形式均可）：
  - Figma 设计稿（截图 / 链接 / 描述）
  - **页面截图**（任何来源的 UI 截图均可作为还原依据）
- （可选）补充需求说明（交互逻辑、特殊效果等）

### AI 输出产物
按以下顺序交付：
1. **图片资源清单** — 设计稿中涉及的图片列表及存放路径建议
2. **数据源文件** — `public/data/{module}/index.json`
3. **页面文件** — `src/views/{module}/index.vue` + `index.scss`
4. **页面级组件** — `src/views/{module}/components/**`（如有拆分）
5. **全局组件** — `components/`（如提取了跨页面复用组件）

## 触发条件

当用户请求以下任务时，使用此 Skill：
- 根据 Figma 设计稿 / 页面截图开发页面
- 基于设计稿/截图生成前端页面或组件代码
- 创建 Vue3 + TS + SCSS 项目并还原设计稿
- 根据截图还原前端页面布局和样式

## 技术栈规范

### 默认技术栈
- **框架**: Vue 3 (Composition API)
- **语言**: TypeScript
- **样式**: SCSS
- **UI 组件库**: Element Plus（**页面开发中优先使用 Element Plus 组件**，包括但不限于表格/表单/按钮/空状态/弹窗/分页等）
- **开发模式**: 组件化开发

### 命名规范
- 变量名、class 名遵循**简单易读**原则
- 使用语义化命名，避免缩写（除非是通用缩写如 `btn`、`img`）
- 组件名使用 PascalCase（如 `UserProfile.vue`）
- 变量/函数名使用 camelCase
- CSS class 使用 kebab-case

### 可配置性原则（核心）
- **数据与 DOM 结构分离**：页面数据必须抽离为独立的 JSON 配置文件
- **配置驱动渲染**：页面组件通过 props 接收数据，不硬编码业务数据
- **便于维护和扩展**：修改数据只需改 JSON，无需动页面代码

## 文件组织规范

### 目录结构

```
project/
├── public/                    # 公共资源
│   ├── images/               # 图片资源（按功能模块分文件夹）
│   │   └── {module}/         # 与 views/{module} 命名保持一致
│   └── data/                 # ★ 页面数据源 ★
│       └── {module}/         # 与 views/{module} 命名保持一致
│           └── index.json
├── components/                # ★ 全局公共组件（与 src 同级）★
│   └── {ComponentName}/
│       ├── index.vue
│       └── index.scss
├── src/
│   ├── views/               # 页面视图
│   │   └── {module}/        # 按功能模块创建文件夹
│   │       ├── index.vue    # 页面主文件（纯 DOM 结构 + 数据绑定）
│   │       ├── components/  # 页面级组件
│   │       └── index.scss   # 页面样式
│   └── styles/              # 全局样式
│       └── global.scss
```

### 文件存放规则
1. **图片资源**: 统一放在 `public/images/` 下，按功能模块分子文件夹，**`{module}` 命名与 `views/{module}` 保持一致**
2. **页面数据**: 每个页面对应一个 JSON 文件，统一放在 `public/data/{module}/index.json`
3. **组件样式**: 所有组件样式必须单独抽出，分散到各组件文件中管理
4. **页面级组件**: 放在 `views/{module}/components/`
5. **全局公共组件**: 放在 **`components/`（与 `src` 同级）**，不在 `src/components/`

### 数据与 DOM 分离规范（重要）

每个页面必须实现**数据与 DOM 结构分离**：

```
public/data/{module}/            # ★ 数据层：统一放 public 下 ★
└── index.json                   # 页面数据源（标题、列表内容、文案等）

src/views/{module}/              # 视图层 + 样式层
├── index.vue                    # 纯结构：只负责 DOM 渲染和数据绑定
├── index.scss                   # 样式层
└── components/                  # 子组件
```

**index.vue 写法示例：**
```vue
<template>
  <div class="{module}-page">
    <HeroSection :config="pageData.hero" />
    <FeatureList :items="pageData.features" />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import HeroSection from './components/HeroSection/index.vue'
import FeatureList from './components/FeatureList/index.vue'
// ★ 数据从 public/data 的 JSON 导入，不硬编码 ★
import pageDataJson from '../../../public/data/{module}/index.json'

const pageData = ref(pageDataJson)
</script>

<style scoped lang="scss">
@import './index.scss';
</style>
```

**public/data/{module}/index.json 示例：**
```json
{
  "hero": {
    "title": "欢迎使用",
    "subtitle": "这是副标题"
  },
  "features": [
    { "id": 1, "title": "特性一", "desc": "描述文字" }
  ]
}
```

## 设计稿还原规范（核心）

### 开发流程

```
用户输入设计稿 → AI 内部解析 → 提取设计 Token → 生成数据源 JSON → 编写页面代码 → 交付完整文件
```

**详细步骤：**

1. **内部解析设计稿** — 识别布局结构、组件拆分边界、交互区域
2. **提取设计 Token** — 颜色、字体、间距、圆角、阴影等视觉参数，写入对应 SCSS
3. **生成数据源文件** — 将文案、列表数据等业务信息抽离到 `public/data/{module}/index.json`
4. **编写页面代码** — 按规范目录结构输出 Vue + SCSS 文件
5. **响应式适配** — 根据设计稿类型完成适配

### 设计 Token 还原规范

AI 必须从设计稿中提取以下视觉参数并还原：

| Token 类型 | Figma 精确还原 | 截图估算策略 |
|-----------|---------------|-------------|
| **颜色** | 精确取色，主色/辅助色/中性色分层 | 近似取色，按视觉归类（主色/成功/警告/危险/信息/文字/边框/背景），优先使用 Element Plus 色值变量 |
| **字号/行高** | 按设计稿数值还原 | 按 Element Plus 字号梯度推断（12/14/16/18/20/24/30/36px） |
| **间距 (padding/margin)** | 按设计稿测量值还原 | **按 4 倍数网格估算**：常用 8/12/16/20/24/32/40/48px |
| **圆角 (border-radius)** | 精确还原 | 常见值推断：小元素 2-4px、卡片 8-12px、大区块 16px+ |
| **阴影 (box-shadow)** | 还原模糊半径、扩散半径、透明度 | 优先使用 Element Plus 阴影变量：`--el-box-shadow` / `--el-box-shadow-light` / `--el-box-shadow-lighter` / `--el-box-shadow-dark` |
| **字体字重** | 按设计稿还原 (400/500/600/700) | 正常 400 / 中等 500 / 半粗 600 / 粗体 700，按视觉判断 |
| **图标** | 使用 SVG 或图片资源，保持尺寸一致 | `public/images/` 或内联 SVG 或使用 Element Plus Icon |
| **渐变背景** | 用 CSS gradient 还原角度和色值 | 视觉近似还原角度和色值 |

**截图还原核心原则：**
- 优先使用 **Element Plus 内置的设计变量**（如 `--el-color-primary`、`--el-border-radius-base`、`--el-spacing-*`），保持与组件库风格统一
- 间距遵循 **4px 基准网格**，避免出现奇数值（如 13px、17px）
- 无法精确判断时，取**最接近的常见值**，不随意创造不规范数值
- 整体视觉效果以"**看起来与截图一致**"为验收标准，允许合理误差

### 布局还原则
- **Flex / Grid**：优先使用现代布局方式，避免 float
- **定位方式**：static > relative > absolute > fixed，按需选择
- **居中方案**：flex 居中优先，margin auto 次之
- **溢出处理**：ellipsis 文本截断、overflow hidden/scroll

### 组件拆分规则

何时拆分子组件：
- **同一 UI 区块在页面内重复出现** → 抽为组件循环渲染
- **功能独立且内部逻辑复杂（如表单、弹窗）** → 拆为独立组件
- **该区块未来可能被其他页面复用** → 提升至全局 `components/`
- **单文件代码超过 150 行** → 考虑按区域拆分

命名约定：根据区块功能语义命名，如 `HeroSection`、`FeatureCard`、`DataTable`

### 背景实现规范
- **优先使用 `background` 属性**实现设计稿背景
- **避免使用 `<img>` 标签**进行背景定位
- 背景图片放在 `public/images/` 对应模块目录下

### 交互状态还原

除静态样式外，还需还原以下交互态（设计稿中有体现时）：
- **hover 态**：按钮/卡片/链接的悬停效果（颜色变化、阴影加深、微缩放等）
- **active 态**：点击时的反馈效果
- **focus 态**：表单输入框的聚焦边框高亮
- **disabled 态**：禁置状态的视觉表现（透明度/灰色）
- **加载态**：骨架屏 / loading 占位（如有）

### 空状态规范（必选）

所有包含列表数据展示的页面**必须实现空状态**：

- **使用 Element Plus 的 `el-empty` 组件**
- **触发条件**：数据数组为空或加载完成无结果时展示
- **默认行为**：自动判断数据是否为空并切换显示

```vue
<template>
  <div class="list-area">
    <template v-if="dataList.length > 0">
      <div v-for="item in dataList" :key="item.id" class="list-item">
        <!-- 正常内容 -->
      </div>
    </template>
    <el-empty v-else description="暂无数据" />
  </div>
</template>
```

- **自定义场景**：根据页面语义选择合适的空状态描述文案和图标类型
- **搜索无结果**：可使用 `"search"` 类型的 el-empty
- **列表为空**：默认类型即可，文案建议用 JSON 数据驱动

### 响应式布局规则

根据**设计稿类型**决定是否采用响应式布局：

| 设计稿类型 | 响应式要求 | 说明 |
|-----------|-----------|------|
| **PC 设计稿** | **必须响应式** | 适配移动端，采用 CSS Media Query |
| **移动端设计稿** | **可选** | 默认不强制适配 PC，如需适配需明确说明 |

**断点建议：**
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

**开发前确认：**
- [ ] 确认设计稿类型（PC / 移动端 / 双端）
- [ ] PC 设计稿：默认响应式适配移动端
- [ ] 移动端设计稿：询问是否需要适配 PC

## 质量验收标准

输出代码需满足以下标准才算"高度还原"：

| 维度 | 验收标准 |
|------|---------|
| **视觉还原度** | Figma: 误差 ≤ 2px；截图: 视觉一致性为主 |
| **布局一致性** | 区域排列、对齐方式、比例关系与设计稿/截图一致 |
| **交互完整性** | hover/focus/disabled 等状态效果已实现 |
| **响应式** | PC 设计稿完成移动端适配（如适用） |
| **规范合规性** | 目录结构、数据分离、命名规范均符合本 Skill 要求 |
| **无硬编码** | 业务数据全部抽离至 JSON，Vue 文件不含硬编码文案 |

## 开发检查清单

生成代码前，确认以下事项：
- [ ] 是否使用 Vue3 + TypeScript + SCSS
- [ ] 是否引入 Element Plus 作为 UI 组件库
- [ ] 文件目录是否符合规范
- [ ] **数据与 DOM 是否分离**（数据在 `public/data/{module}/index.json`，页面不硬编码业务数据）
- [ ] **`public/data/` 和 `public/images/` 的 `{module}` 命名是否与 `views/{module}` 一致**
- [ ] **全局公共组件是否放在 `components/`（与 `src` 同级）**
- [ ] 设计稿（Figma / 截图）：是否已内部解析布局结构
- [ ] 设计 Token 是否提取完整（颜色/字号/间距/圆角/阴影）
- [ ] 若为截图输入：是否采用 4px 网格估算 + Element Plus 变量对齐策略
- [ ] 背景是否优先使用 background 实现
- [ ] 交互状态（hover/focus 等）是否按需实现
- [ ] **列表页面是否使用 el-empty 实现空状态**
- [ ] 是否确认设计稿类型（PC / 移动端）
- [ ] PC 设计稿是否实现响应式适配移动端
- [ ] 移动端设计稿是否需要适配 PC（如需要）

## 参考文档

详细编码风格规范请参考 `references/coding-standards.md`
