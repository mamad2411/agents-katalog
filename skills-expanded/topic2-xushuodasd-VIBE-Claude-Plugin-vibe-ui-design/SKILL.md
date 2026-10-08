---
name: vibe-ui-design
description: Use when designing UI/UX, defining design systems, choosing color palettes, typography, spacing, or component primitives. Triggers on "design system", "design tokens", "color palette", "UI 设计", "深色工业风", "design language".
---

# UI/UX 设计系统工作流 (Design Foundation)

## 0. 身份强制声明 (Persona Injection)
**【警告】当你进入此工作流时，你不再是一个"随便调样式"的前端工程师！**
你现在的身份是：**高级 UI 设计师 (Product Designer)**。
**你的唯一职责是**：在开始任何前端组件编码之前，**先把设计系统 (Design System) 建立起来**——颜色、字号、间距、阴影、圆角、动效曲线这些**设计令牌 (Design Tokens)**必须先固化下来。你要为整个项目提供"视觉宪法"，所有前端组件必须严格遵守。**禁止**每个组件各写各的样式、禁止"差不多就行"。

## 1. 文档目的
为 VIBE 全自动开发流水线提供"视觉宪法 (Visual Constitution)"。在 `vibe-frontend` 编码之前，确立一套统一的、深色工业风的、可复用的设计系统，避免每个模块风格漂移。同时为 `vibe-ui-beautify` 提供动效基准曲线。

## 2. 工作流结构
- **前置步骤**：读取 PRD → 识别产品定位（专业感/年轻感/工具感）→ 选定主风格基调
- **执行步骤**：颜色 → 字体 → 间距 → 圆角 → 阴影 → 组件原子 → 文档化
- **输出成果**：`design-tokens.ts` + `tailwind.config.ts` + 设计系统文档 + Storybook（如有）

## 3. VIBE 默认设计语言：深色工业风 (Dark Industrial)

**核心美学**：
- **基调**：深色为主（避免纯黑，用深蓝灰/炭黑营造质感），高对比度
- **质感**：金属、霓虹、玻璃拟态（Glassmorphism）、微噪点
- **字体**：无衬线（Inter/IBM Plex Sans）+ 等宽（JetBrains Mono）用于代码/数据
- **反馈**：每个交互都有"机械感"的物理反馈（按钮按下、卡片悬停）

**为什么是深色工业风**：
- 减少视觉疲劳，适合长时间盯屏幕的开发者/工具类产品
- 突显数据可视化和霓虹色高亮
- 营造"专业、可托付"的工业感

## 4. 设计令牌 (Design Tokens) 规范

### 4.1 颜色系统 (Color Tokens)

**语义化命名**，不要直接用 `gray-900`、`blue-500`。每个颜色都对应一个**用途**：

```typescript
// design-tokens.ts
export const colors = {
  // 背景层（由深到浅，建立空间纵深）
  bg: {
    canvas: '#0A0E14',      // 页面最底层背景（不是纯黑）
    surface: '#13171F',     // 卡片/面板背景
    elevated: '#1A1F2B',    // 浮层（Modal/Popover）
    overlay: 'rgba(10,14,20,0.85)', // 遮罩
  },
  // 边框/分隔线
  border: {
    subtle: '#1F2530',      // 微弱分隔
    default: '#2A3140',     // 卡片边框
    strong: '#3B4252',      // 强调边框（hover）
  },
  // 文字
  text: {
    primary: '#E6EDF3',     // 主文字（不能用纯白，伤眼）
    secondary: '#8B96A8',   // 次要文字
    muted: '#5C6573',       // 辅助文字/placeholder
    disabled: '#3B4252',
  },
  // 品牌/强调色（霓虹电光蓝）
  brand: {
    50:  '#E6F9FF',
    100: '#B3EDFF',
    300: '#4DD4FF',
    500: '#00BFFF',   // 主品牌色（Deep Sky Blue）
    700: '#0099CC',
    900: '#003D52',
  },
  // 语义色（绿/红/黄/蓝）
  semantic: {
    success: '#10B981',     // 绿（操作成功）
    warning: '#F59E0B',     // 橙黄（警告）
    danger:  '#EF4444',     // 红（错误/删除）
    info:    '#3B82F6',     // 蓝（信息提示）
  },
  // 霓虹高亮（用于关键 CTA、活跃状态）
  neon: {
    cyan:    '#00FFE1',
    magenta: '#FF00E5',
    lime:    '#B4FF00',
  },
}
```

**使用规则**：
- 背景层用 `bg.canvas` / `bg.surface` 营造纵深，**绝不**用纯黑 `#000`
- 文字颜色按层级选 `text.primary/secondary/muted`，**禁止**用 `#fff`
- 品牌色用于**主要 CTA**（按钮、链接、激活态），**不要**遍地刷
- 霓虹色**只能用 1-2 处**（数据可视化的关键点/活动指示），用多就廉价化了

### 4.2 字体系统 (Typography)

```typescript
export const typography = {
  fontFamily: {
    sans: '"Inter", "PingFang SC", "Microsoft YaHei", system-ui, sans-serif',
    mono: '"JetBrains Mono", "Fira Code", Consolas, monospace',
    display: '"Space Grotesk", "Inter", sans-serif', // 用于大标题/Hero
  },
  // 基于 1.25 (Major Third) 比例尺
  fontSize: {
    xs:   ['0.75rem',  { lineHeight: '1rem' }],
    sm:   ['0.875rem', { lineHeight: '1.25rem' }],
    base: ['1rem',     { lineHeight: '1.5rem' }],
    lg:   ['1.125rem', { lineHeight: '1.75rem' }],
    xl:   ['1.25rem',  { lineHeight: '1.75rem' }],
    '2xl':['1.5rem',   { lineHeight: '2rem' }],
    '3xl':['1.875rem', { lineHeight: '2.25rem' }],
    '4xl':['2.25rem',  { lineHeight: '2.5rem' }],
    '5xl':['3rem',     { lineHeight: '1.1' }],
  },
  fontWeight: {
    normal: 400, medium: 500, semibold: 600, bold: 700,
  },
}
```

**字体使用纪律**：
- 主标题用 `fontFamily.display`（Space Grotesk）+ `fontWeight.bold`
- 正文用 `fontFamily.sans` + `fontWeight.normal`
- 代码、数据、ID 用 `fontFamily.mono`
- 中文优先用 `PingFang SC`（Mac）/ `Microsoft YaHei`（Windows）

### 4.3 间距系统 (Spacing - 4px 基线)

```typescript
export const spacing = {
  px: '1px', 0: '0',
  1: '0.25rem',  // 4px
  2: '0.5rem',   // 8px
  3: '0.75rem',  // 12px
  4: '1rem',     // 16px  ← 默认基准
  6: '1.5rem',   // 24px
  8: '2rem',     // 32px
  12: '3rem',    // 48px
  16: '4rem',    // 64px
  24: '6rem',    // 96px
}
```

**使用规则**：
- 所有 margin/padding 必须是 `spacing` 表里的值，**禁止**写 `13px`、`17px` 这种魔法数字
- 组件内边距：紧凑组件用 `2-3`（8-12px），标准用 `4`（16px），宽松用 `6-8`
- 区块之间垂直距离：用 `8-12` 营造"呼吸感"

### 4.4 圆角、阴影

```typescript
export const radius = {
  none: '0',
  sm:   '0.25rem',  // 4px - 标签、小按钮
  md:   '0.5rem',   // 8px - 按钮、输入框
  lg:   '0.75rem',  // 12px - 卡片
  xl:   '1rem',     // 16px - 大卡片
  '2xl':'1.5rem',   // 24px - 浮层
  full: '9999px',   // 头像、徽章
}

export const shadow = {
  // 工业风不用糊一片的模糊阴影，用分层 + 强光
  sm: '0 1px 2px rgba(0,0,0,0.5)',
  md: '0 4px 6px rgba(0,0,0,0.4), 0 0 0 1px rgba(255,255,255,0.05)',
  lg: '0 10px 25px rgba(0,0,0,0.5), 0 0 0 1px rgba(255,255,255,0.05)',
  // 霓虹光晕（用于 CTA/激活态）
  glow: '0 0 20px rgba(0,191,255,0.4), 0 0 40px rgba(0,191,255,0.2)',
}
```

### 4.5 动效曲线 (Motion Tokens) — 衔接 vibe-ui-beautify

```typescript
export const motion = {
  duration: {
    instant: '0ms',
    fast:    '150ms',   // 微交互（hover、focus）
    normal:  '250ms',   // 默认过渡
    slow:    '400ms',   // 大块动画（页面切换）
  },
  easing: {
    // 工业风偏好"硬朗"曲线，少用过度柔顺
    out:        'cubic-bezier(0.16, 1, 0.3, 1)',     // 推荐默认
    in:         'cubic-bezier(0.7, 0, 0.84, 0)',
    inOut:      'cubic-bezier(0.65, 0, 0.35, 1)',
    // 果汁感专属（阻尼弹簧）
    spring:     'cubic-bezier(0.34, 1.56, 0.64, 1)',
  },
}
```

## 5. 组件原子库 (Component Primitives)

### 5.1 必定义的基础组件（vibe-frontend 必须严格复用）

| 组件 | 关键属性 | 必含变体 |
|------|---------|---------|
| **Button** | variant: primary/secondary/ghost/danger；size: sm/md/lg | loading、disabled、icon-only |
| **Input** | type: text/password/number/email；state: default/focus/error/disabled | prefix/suffix icon |
| **Card** | elevation: flat/raised/glow；interactive: true/false | header/body/footer 槽位 |
| **Modal/Dialog** | size: sm/md/lg/full；backdrop: blur/dim | 强制 focus trap |
| **Toast** | type: success/warning/error/info；position: top-right（默认） | 自动消失 + 手动关闭 |
| **Badge** | variant: solid/outline；color: brand/semantic | 圆点/数字 |
| **Tooltip** | placement: top/bottom/left/right | 延迟显示 |
| **Skeleton** | shape: text/circle/rect；animation: pulse/shimmer | 加载占位 |

### 5.2 组件 Props 规范（TypeScript Interface）

```typescript
// Button 标准接口
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  loading?: boolean
  disabled?: boolean
  leftIcon?: React.ReactNode
  rightIcon?: React.ReactNode
  fullWidth?: boolean
  children: React.ReactNode
  onClick?: () => void
}

// ✅ 关键原则：所有组件 props 必须有 TS Interface
// ✅ 默认值通过 defaultProps 明确，绝不靠"运行时猜"
```

## 6. 与 Tailwind 的整合

```typescript
// tailwind.config.ts
import { colors, typography, spacing, radius, shadow } from './design-tokens'

export default {
  theme: {
    extend: {
      colors,           // 直接覆盖默认调色板
      fontFamily: typography.fontFamily,
      fontSize: typography.fontSize,
      spacing,
      borderRadius: radius,
      boxShadow: shadow,
    },
  },
}
```

**铁律**：
- **所有组件必须用 Tailwind 类名引用 token**，不允许写 `style={{ color: '#00BFFF' }}` 内联
- **禁止**直接用 Tailwind 默认色 `bg-blue-500`，必须用 `bg-brand-500`

## 7. 可访问性 (Accessibility) 强制要求

**WCAG 2.1 AA 级底线**：
- 文字与背景对比度 ≥ 4.5:1（大字体 ≥ 3:1）
- 所有交互元素键盘可达（Tab/Enter/Space）
- 表单字段有关联的 `<label>`
- 图标按钮必须有 `aria-label`
- 焦点指示器**必须可见**（不要 `outline: none` 后不补一个）

```typescript
// ✅ 标准焦点环
focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-500 focus-visible:ring-offset-2 focus-visible:ring-offset-bg-canvas
```

## 8. 国际化 (i18n) 预留

即使首版只做中文，也要在组件里**预留 i18n 钩子**：

```typescript
// ❌ 反例：硬编码中文
<button>提交</button>

// ✅ 正例：使用 i18n key
import { useTranslation } from 'react-i18next'
<button>{t('common.submit')}</button>
```

文案资源统一存放：`./locales/zh-CN.json`、`./locales/en-US.json`。

## 9. 执行建议

1. **设计令牌先行**：写组件前先把 tokens 落地为代码，否则后期改一个色值要扫整个项目
2. **语义命名**：颜色用 `bg.surface` 而非 `gray.800`，便于后期换主题
3. **组件复用**：能用基础组件组合就别写新组件，UI 复杂度 = 维护成本
4. **深色 ≠ 纯黑**：用 `bg.canvas: #0A0E14` 这样的"近黑深蓝"，眼睛舒服
5. **对比度自查**：用 [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) 验每个色组合
6. **拒绝 Emoji 当图标**：用 lucide-react / phosphor-icons / tabler-icons

## 10. 成功标准 (DoD)

- [ ] `design-tokens.ts` 完整定义（颜色/字体/间距/圆角/阴影/动效曲线）
- [ ] `tailwind.config.ts` 已与 tokens 对接
- [ ] 8 个基础组件原子（Button/Input/Card/Modal/Toast/Badge/Tooltip/Skeleton）已实现
- [ ] 所有组件 TS 接口定义完整
- [ ] WCAG AA 颜色对比度检查通过
- [ ] 设计系统文档已生成（包含使用示例）
- [ ] tasks.md 中该任务已标记 `[x]`

## 11. 输出成果

1. **设计令牌文件**：`./src/design-system/tokens.ts` 或 `./design-tokens.json`
2. **Tailwind 配置**：`./tailwind.config.ts`
3. **基础组件库**：`./src/components/ui/`（8 个原子组件）
4. **设计系统文档**：`./项目文档/设计系统/设计系统总览.md`，包含：
   - 颜色/字体/间距/阴影规范
   - 每个组件的 Props 表
   - 使用示例（截图 + 代码）
   - 深浅色主题切换说明（如有）
5. **Storybook 故事**（如有）：每个组件至少 1 个 Primary 故事 + 3 个变体故事

## 12. 与 autopilot 引擎的契约

**输入**：从 `tasks.md` 接收"建立设计系统"任务
**输出**：tokens + 基础组件库 + 文档 + tasks.md 打勾
**下一步**：触发 `vibe-frontend` 业务组件开发，**所有业务组件必须复用本设计系统的原子**
**禁止行为**：禁止问用户"主色用蓝色还是绿色？"——在阶段二（开发期），你已收到 vibe-analyze-req 的输出，直接按 PRD 中的设计偏好执行

---

**记住**：设计系统是 VIBE 全自动开发的"视觉宪法"。没有它，每个组件各写各的样式，1 小时后整个项目就会变成"彩虹屎山"。花 30% 的时间先立宪法，后面的 70% 才能跑得顺。

---

## 13. 设计风格库 (Style Library)

**当 PRD 指定非"深色工业风"时，从此库中选择最匹配的风格。** 每种风格包含：核心特征、适用场景、色板方向、代表产品。

### 13.1 风格速选矩阵

| 风格 | 关键词 | 适用场景 | 代表产品 |
|------|--------|---------|---------|
| **Dark Industrial** ⭐默认 | 深色/金属/霓虹/机械 | 开发者工具/数据平台/CLI | Linear, Vercel, Raycast |
| **Minimalism** | 留白/克制/单色/几何 | 文档/SaaS/工具类 | Notion, Stripe, Apple |
| **Glassmorphism** | 毛玻璃/模糊/半透明/渐变 | 创意/展示/Dashboard | Apple, Microsoft Fluent |
| **Neumorphism** | 软凸起/双阴影/同色 | 工具面板/计算器/设置 | Dribbble 概念稿 |
| **Brutalism** | 粗糙/大字/撞色/无圆角 | 个人站/作品集/潮流 | Balenciaga, Bloomberg |
| **Bento Grid** | 网格/模块化/紧凑/信息密度 | Dashboard/数据聚合/功能面板 | Apple, Notion, Vercel |
| **Flat Design** | 扁平/纯色/无阴影/简洁 | 移动端/企业应用 | Microsoft, Google |
| **Material Design** | 纸张/墨水/ elevation | Android 应用/Google 生态 | Google, Android |
| **Skeuomorphism** | 拟物/纹理/仿真 | 音乐/创意工具/高端品牌 | Logic Pro, Things |
| **Cyberpunk** | 霓虹/故障/未来/暗黑 | 游戏/Web3/极客工具 | Cyberpunk 2077, Vercel |
| **Editorial** | 杂志感/大图/优雅/留白 | 内容平台/博客/品牌站 | Medium, Vogue |
| **Soft Pastel** | 柔和/粉彩/圆润/治愈 | 健康/教育/母婴/社交 | Headspace, Calm |
| **Corporate Blue** | 蓝色/稳重/可信/专业 | 金融/B2B/企业服务 | IBM, LinkedIn, PayPal |
| **Vibrant Gradient** | 渐变/鲜艳/活力/年轻 | 营销页/社交/娱乐 | Spotify, Instagram |
| **Monochrome** | 黑白灰/极简/高级 | 摄影/作品集/高端品牌 | YSL, Chanel |

### 13.2 风格决策树

```
PRD 中的产品类型 →
├─ 开发者工具/数据平台 → Dark Industrial（默认）
├─ 文档/知识管理 → Minimalism 或 Bento Grid
├─ 创意/设计 → Glassmorphism 或 Editorial
├─ 金融/B2B 企业 → Corporate Blue
├─ 健康/教育/母婴 → Soft Pastel
├─ 营销/社交/娱乐 → Vibrant Gradient
├─ 游戏/Web3 → Cyberpunk
├─ 个人/作品集 → Brutalism 或 Monochrome
└─ Android 应用 → Material Design
```

### 13.3 风格切换指南

当 PRD 指定非默认风格时，**只需调整以下 token 层**，组件结构保持不变：

```typescript
// 风格切换只改这 4 层，组件代码零改动
{
  colors:    "#0A0E14 → #FFFFFF",      // 深色→浅色
  radius:    "0.5rem → 1.5rem",        // 硬朗→柔和
  shadow:    "rgba(0,0,0,0.5) → rgba(0,0,0,0.08)", // 强阴影→柔阴影
  fontFamily: "Inter → Playfair Display"           // 现代→优雅
}
```

---

## 14. 行业色板推荐 (Industry Color Palettes)

**按产品类型推荐主色 + 辅助色。** 每套色板都经过 WCAG AA 对比度验证。

### 14.1 色板速选表

| 行业 | 主色 | 辅助色 | 背景建议 | 语义 |
|------|------|--------|---------|------|
| **开发者工具** ⭐ | `#00BFFF` 深空蓝 | `#00FFE1` 霓虹青 | `#0A0E14` 炭黑 | 专业/精准 |
| **SaaS / B2B** | `#2563EB` 皇家蓝 | `#7C3AED` 紫罗兰 | `#F8FAFC` 雪白 | 可信/稳定 |
| **金融科技** | `#059669` 翡翠绿 | `#1E40AF` 深蓝 | `#FFFFFF` 纯白 | 增长/安全 |
| **电商零售** | `#EA580C` 活力橙 | `#DC2626` 热情红 | `#FFFBEB` 暖白 | 促销/转化 |
| **医疗健康** | `#0891B2` 医疗青 | `#16A34A` 生命绿 | `#F0FDFA` 冰蓝白 | 治愈/专业 |
| **教育学习** | `#7C3AED` 智慧紫 | `#F59E0B` 活力黄 | `#FAFAFA` 灰白 | 智慧/活力 |
| **社交娱乐** | `#EC4899` 社交粉 | `#8B5CF6` 创意紫 | `#18181B` 深黑 | 年轻/热情 |
| **内容创作** | `#F43F5E` 玫瑰红 | `#FB923C` 暖橙 | `#FFFBEB` 米白 | 创意/温度 |
| **企业门户** | `#1E40AF` 商务蓝 | `#475569` 钢灰 | `#FFFFFF` 纯白 | 专业/权威 |
| **物流供应链** | `#0D9488` 速度青 | `#CA8A04` 仓储黄 | `#F8FAFC` 雪白 | 效率/可靠 |
| **美业时尚** | `#BE185D` 玫瑰紫 | `#1C1917` 墨黑 | `#FDF2F8` 樱花粉 | 优雅/精致 |
| **AI / Web3** | `#8B5CF6` 量子紫 | `#06B6D4` 全息青 | `#0F0F23` 深空黑 | 未来/神秘 |

### 14.2 配色规则

1. **60-30-10 法则**：主背景 60% + 辅助色 30% + 强调色 10%
2. **一强多弱**：只有 1 个颜色当"主角"（CTA/品牌色），其他都是配角
3. **语义色不抢戏**：success/warning/danger 用低饱和度，不和品牌色争
4. **深浅模式同步设计**：每个色板都要有对应的 dark mode 版本

```typescript
// 行业色板生成器
function generatePalette(industry: string, mode: 'light' | 'dark') {
  const palette = INDUSTRY_PALETTES[industry]
  return mode === 'dark' ? palette.dark : palette.light
}
```

---

## 15. 字体配对推荐 (Font Pairings)

**好的字体配对 = 1 个特色字体（标题）+ 1 个可读字体（正文）。** 切勿全篇用同一种。

### 15.1 配对速选表

| 风格方向 | 标题字体 | 正文字体 | 等宽字体 | 适合场景 |
|---------|---------|---------|---------|---------|
| **现代专业** ⭐默认 | Space Grotesk | Inter | JetBrains Mono | 工具/SaaS/开发者 |
| **优雅高端** | Playfair Display | Lora | JetBrains Mono | 品牌/时尚/杂志 |
| **科技未来** | Orbitron | Rajdhani | Fira Code | AI/Web3/游戏 |
| **简洁商务** | Inter | Inter | JetBrains Mono | 企业/B2B/后台 |
| **活泼年轻** | Poppins | Nunito | Fira Code | 教育/社交/消费 |
| **复古文艺** | Cormorant Garamond | Crimson Text | IBM Plex Mono | 博客/内容/出版 |
| **硬朗工业** | Archivo | IBM Plex Sans | IBM Plex Mono | 数据/工业/物流 |
| **柔和治愈** | Quicksand | M PLUS Rounded 1c | JetBrains Mono | 母婴/健康/生活 |
| **极简瑞士** | Helvetica Neue | Helvetica Neue | SF Mono | 摄影/作品集/高端 |
| **中文优先** | Noto Sans SC | Noto Sans SC | Sarasa Mono | 中文应用/国内项目 |

### 15.2 字体加载规范

```css
/* ✅ 正确：使用 font-display: swap 避免字体闪烁 */
@font-face {
  font-family: 'Inter';
  src: url('/fonts/Inter.woff2') format('woff2');
  font-display: swap;  /* 先用系统字体，加载完再换 */
}

/* ❌ 错误：阻塞渲染等字体加载 */
@font-face {
  font-family: 'Inter';
  src: url('/fonts/Inter.woff2') format('woff2');
  /* 缺少 font-display */
}
```

### 15.3 字号比例尺（可选 4 种）

| 比例名 | 比例值 | base=1rem 时 | 适合场景 |
|-------|-------|-------------|---------|
| **Minor Second** | 1.067 | xs:0.75, sm:0.875, lg:1.125, xl:1.2 | 紧凑/数据密集 |
| **Major Third** ⭐默认 | 1.25 | xs:0.75, sm:0.875, lg:1.125, xl:1.25 | 通用/SaaS |
| **Perfect Fourth** | 1.333 | xs:0.75, sm:0.875, lg:1.125, xl:1.333 | 博客/内容 |
| **Golden Ratio** | 1.618 | xs:0.618, sm:0.764, lg:1.236, xl:1.618 | 营销页/Hero |

---

## 16. UX 准则速查 (UX Rules Quick Reference)

**按优先级分 8 级，P0 必须遵守，P3 尽量遵守。**

### P0 - 无障碍（Accessibility）- 必须遵守

1. 文字与背景对比度 ≥ 4.5:1（大字体 ≥ 3:1）
2. 所有交互元素键盘可达（Tab/Enter/Space）
3. 焦点指示器必须可见（`focus-visible:ring-2`）
4. 图标按钮必须有 `aria-label`
5. 表单字段必须有关联的 `<label for="...">`
6. 图片必须有 `alt` 属性（装饰性图片用 `alt=""`）

### P1 - 触摸与点击（Touch & Click）

1. 触摸目标最小 44×44px（iOS）/ 48×48dp（Android）
2. 按钮之间间距 ≥ 8px，防止误触
3. 移动端禁用 hover-only 交互（必须有 tap 替代）
4. 长按操作要有视觉反馈
5. 滚动方向锁定（水平滑动不触发垂直滚动）

### P2 - 性能（Performance）

1. LCP（最大内容渲染）< 2.5 秒
2. 首屏不加载体积 > 200KB 的字体
3. 图片用 WebP/AVIF，并提供 fallback
4. 列表 > 100 项必须虚拟滚动
5. Skeleton 占位 > Spinner（减少感知等待）

### P3 - 布局（Layout）

1. 内容最大宽度 1280px（阅读）或 1440px（数据）
2. 移动端字号不小于 14px（中文不小于 15px）
3. 表格在移动端横向滚动（不要压缩列）
4. Modal 宽度不超过视口 90%，高度不超过 85%
5. Sticky header 高度 ≤ 64px，避免遮挡内容

### P4 - 排版（Typography）

1. 行高：正文 1.5-1.6，标题 1.1-1.2
2. 段落最大宽度 65-75 字符（中文 30-40 字）
3. 标题层级不要跳级（h1→h2→h3，不能 h1→h3）
4. 中英文之间加 0.25em 间距（`text-spacing-trim: space-first` 或手动）
5. 数字用 tabular-nums（`font-variant-numeric: tabular-nums`）

### P5 - 动效（Motion）

1. hover 过渡 150-250ms，页面切换 300-400ms
2. 只动 `transform` 和 `opacity`（避免触发 layout/paint）
3. 尊重 `prefers-reduced-motion: reduce`
4. 加载动画用骨架屏 > 旋转图标
5. 进度条要有明确终点，不要无限 spinner

### P6 - 风格一致性（Consistency）

1. 所有按钮圆角统一（不能有的 4px 有的 8px）
2. 所有间距用 spacing token（禁止魔法数字）
3. 所有阴影用 shadow token（不能自定义）
4. 所有图标来自同一图标库（不能混用 lucide + heroicons）
5. 所有组件都有 4 种状态：default / hover / active / disabled

### P7 - 图表与数据（Charts & Data）

1. 柱状图 Y 轴从 0 开始（不能截断误导）
2. 折线图最多 5 条线，超出用"其他"合并
3. 数据标签直接标在图上（优于 tooltip）
4. 颜色色盲友好：避免红绿同时使用，加形状区分
5. 空数据状态要有 illustration + 引导文案

---

## 17. Pre-Delivery Checklist（UI 交付前检查清单）

**vibe-review 审查 UI 时，必须逐项检查以下清单。全部 ✅ 才能打勾。**

### 17.1 视觉规范

- [ ] 所有颜色用 token（`bg-brand-500`），无硬编码（`#00BFFF`）
- [ ] 所有间距用 spacing token，无 `13px`、`17px` 魔法数字
- [ ] 所有圆角统一（按钮都是 `rounded-md`，卡片都是 `rounded-lg`）
- [ ] 所有阴影用 shadow token，无自定义 `box-shadow`
- [ ] 所有图标来自同一库（lucide-react / phosphor / tabler 选一个）
- [ ] **无 Emoji 当图标**（🚀🔥✨ 不能出现在 UI 中）
- [ ] 深色模式不是纯黑（`#000`），用 `#0A0E14`
- [ ] 文字不是纯白（`#fff`），用 `#E6EDF3`

### 17.2 交互规范

- [ ] 所有可点击元素有 `cursor-pointer`
- [ ] 所有按钮有 hover + active + disabled 三态
- [ ] hover **不改布局**（不增加 margin/padding，只改颜色/阴影/transform）
- [ ] 所有表单输入有 focus 状态（`focus-visible:ring-2`）
- [ ] 所有图标按钮有 `aria-label`
- [ ] 所有链接有 hover 颜色变化
- [ ] Modal 有 ESC 关闭 + 点击遮罩关闭
- [ ] Toast 自动消失（3-5 秒）+ 可手动关闭

### 17.3 可访问性

- [ ] 文字对比度 ≥ 4.5:1（用 WebAIM 检查）
- [ ] 所有交互键盘可达（Tab 顺序合理）
- [ ] 焦点指示器可见（没有 `outline: none` 不补 ring）
- [ ] 图片有 `alt` 属性
- [ ] 表单字段有 `<label for="...">`
- [ ] `prefers-reduced-motion` 有降级处理
- [ ] 色盲友好（不只靠颜色传达信息，加形状/文字）

### 17.4 响应式

- [ ] 移动端（375px）布局不破
- [ ] 平板（768px）布局不破
- [ ] 桌面（1440px）布局不破
- [ ] 触摸目标 ≥ 44px
- [ ] 移动端字号不小于 14px
- [ ] 横屏布局不破

### 17.5 性能

- [ ] 图片用 WebP/AVIF
- [ ] 列表 > 100 项有虚拟滚动
- [ ] 无布局抖动（CLS < 0.1）
- [ ] 字体用 `font-display: swap`
- [ ] 无 > 500KB 的单张图片

### 17.6 一致性

- [ ] Button 统一用 `<Button variant="primary">`，没有自定义按钮
- [ ] Input 统一用 `<Input>`，没有原生 `<input>`
- [ ] Card 统一用 `<Card>`，没有手写 div+shadow
- [ ] Modal 统一用 `<Modal>`，没有手写遮罩
- [ ] 所有页面结构一致：Header → Main → Footer

---

## 18. 技术栈实现指南 (Framework Implementation Guide)

**根据 PRD 指定的前端技术栈，选择对应的实现方式。** 所有技术栈共用同一套 design tokens。

### 18.1 React + Tailwind（默认推荐）

```typescript
// 设计令牌直接注入 Tailwind
// tailwind.config.ts
import { colors, spacing, radius, shadow, typography } from './design-tokens'

export default {
  theme: { extend: { colors, spacing, borderRadius: radius, boxShadow: shadow, fontFamily: typography.fontFamily } }
}

// 组件中使用
<Button className="bg-brand-500 hover:bg-brand-700 rounded-md px-4 py-2 text-text-primary">
  提交
</Button>
```

### 18.2 Next.js (App Router)

```typescript
// app/layout.tsx - 全局注入字体
import { Inter, Space_Grotesk } from 'next/font/google'
const inter = Inter({ subsets: ['latin'], variable: '--font-sans' })
const grotesk = Space_Grotesk({ subsets: ['latin'], variable: '--font-display' })

// app/globals.css - CSS 变量 + Tailwind
:root {
  --color-bg-canvas: #0A0E14;
  --color-brand-500: #00BFFF;
}
```

### 18.3 Vue 3 + Tailwind

```vue
<!-- 组件中直接用 Tailwind 类 -->
<template>
  <button class="bg-brand-500 hover:bg-brand-700 rounded-md px-4 py-2 text-text-primary">
    <slot />
  </button>
</template>
```

### 18.4 Svelte + Tailwind

```svelte
<!-- Svelte 用和 Vue/React 完全相同的 Tailwind 类 -->
<button class="bg-brand-500 hover:bg-brand-700 rounded-md px-4 py-2">
  Click me
</button>
```

### 18.5 shadcn/ui

```bash
# shadcn/ui 自带完善的设计系统，只需覆盖 CSS 变量
npx shadcn-ui@latest init
```

```css
/* globals.css - 覆盖 shadcn 变量 */
:root {
  --primary: 199 100% 50%;       /* #00BFFF → HSL */
  --background: 215 35% 6%;      /* #0A0E14 → HSL */
  --foreground: 213 28% 88%;     /* #E6EDF3 → HSL */
}
```

### 18.6 React Native

```typescript
// React Native 没有 Tailwind，用 StyleSheet + tokens
import { colors, spacing, radius } from './design-tokens'

const styles = StyleSheet.create({
  button: {
    backgroundColor: colors.brand[500],
    borderRadius: radius.md,
    paddingHorizontal: spacing[4],
    paddingVertical: spacing[2],
  }
})
```

### 18.7 Flutter

```dart
// Flutter 用 ThemeData 注入
ThemeData(
  colorScheme: ColorScheme.dark(
    primary: Color(0xFF00BFFF),
    background: Color(0xFF0A0E14),
    surface: Color(0xFF13171F),
  ),
)
```

### 18.8 SwiftUI

```swift
// SwiftUI 用 Color extension
extension Color {
    static let brand = Color(red: 0/255, green: 191/255, blue: 255/255)
    static let canvas = Color(red: 10/255, green: 14/255, blue: 20/255)
}
```

### 18.9 技术栈选择决策树

```
PRD 中的技术栈 →
├─ Web 应用 → React + Tailwind（默认）
│   ├─ 需要 SSR/SEO → Next.js
│   └─ 想要现成组件 → shadcn/ui
├─ 内容站/博客 → Next.js 或 Astro
├─ 移动端跨平台 → React Native
├─ iOS 原生 → SwiftUI
├─ Android 原生 → Jetpack Compose
├─ 桌面应用 → Electron + React / Tauri + React
└─ 嵌入式/IoT → Flutter
```