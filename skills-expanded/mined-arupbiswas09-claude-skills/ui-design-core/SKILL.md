---
name: ui-design-core
description: |
  核心设计能力 - 提供配色、布局、组件样式生成及反模式检查。
  当用户说"设计UI"、"生成样式"、"页面布局"、"CSS样式"、"组件设计"、"配色方案"、"设计系统"、"前端样式"、"响应式设计"、"动画效果"时使用此技能。
  支持多种设计风格：Neo-Brutalism、Glassmorphism、Editorial、Cyberpunk。
  提供配色方案、布局生成、组件样式、微交互动效、响应式网格。拒绝"AI廉价感"，追求大胆、独特、细节丰富的设计。
  重要特性：提供反模式检查，避免泛滥的渐变、无聊的阴影、默认圆角等平庸设计。
disable-model-invocation: false
---

# Core Design Skills

## 🌟 技能核心：拒绝平庸
本技能旨在生成**具有独特审美、生产级质量**的前端界面。
**核心原则**：拒绝千篇一律的 "AI 廉价感" (AI Slop)。我们追求**大胆**、**独特**且**细节丰富**的设计。

## 🧠 Design Thinking (设计思维)
在编写任何代码之前，必须先确立设计方向：

### 1. 确立审美基调 (Bold Direction)
不要做"干净但无聊"的设计。选择一个明确的风格方向：
- **Brutalism (野兽派)**: 粗边框、高对比度、单色底、巨大字体。
- **Glassmorphism (玻璃拟态)**: 深度模糊、半透明层、微妙的光影。
- **Neo-Brutalism**: 鲜艳高饱和色、复古黑边、几何图形。
- **Editorial (杂志风)**: 精致的衬线体、大留白、不对称布局。
- **Cyberpunk (赛博朋克)**: 霓虹光晕、深色背景、Glitch 效果。

### 2. 细节至上 (Refined Details)
- **Typography**: 拒绝 Arial/Roboto。混合搭配 Display 字体（标题）和高可读性 Sans 字体（正文）。
- **Motion**: 每一个交互都应有物理反馈。使用 `cubic-bezier` 而不是线性的 `ease`。
- **Depth**: 避免扁平化。使用阴影、纹理、噪点 (Noise) 来增加质感。

## 🚫 反模式 (Anti-Patterns)
**绝对禁止**以下 "AI 默认审美"：
- ❌ 泛滥的紫色/蓝色线性渐变背景。
- ❌ 毫无个性的 `box-shadow: 0 4px 6px rgba(0,0,0,0.1)`。
- ❌ 默认的圆角 (如 `border-radius: 4px`) —— 要么完全直角，要么夸张的大圆角。
- ❌ 枯燥的 "Header-Hero-Features" 三段式布局。

## 📝 代码示例

### 1. Neo-Brutalism 风格卡片

```css
/* 独特的 Neo-Brutalism 风格 */
.neo-card {
  background: #fff;
  border: 4px solid #000;
  border-radius: 0; /* 直角 */
  box-shadow: 8px 8px 0 #000; /* 硬阴影 */
  padding: 2rem;
  transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.neo-card:hover {
  transform: translate(-4px, -4px);
  box-shadow: 12px 12px 0 #000;
}
```

```tsx
// React + Tailwind 实现
function NeoCard({ children }: { children: React.ReactNode }) {
  return (
    <div className="bg-white border-4 border-black p-8 shadow-[8px_8px_0_#000]
                    transition-all duration-200 hover:translate-x-[-4px] hover:translate-y-[-4px]
                    hover:shadow-[12px_12px_0_#000]">
      {children}
    </div>
  );
}
```

### 2. Glassmorphism 玻璃拟态

```css
/* 玻璃效果 */
.glass-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 24px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}
```

```tsx
// Tailwind CSS 实现
function GlassCard({ children }: { children: React.ReactNode }) {
  return (
    <div className="bg-white/10 backdrop-blur-xl border border-white/20
                    rounded-3xl shadow-lg p-6">
      {children}
    </div>
  );
}
```

### 3. Editorial 杂志风格排版

```css
/* 杂志风格排版 */
.editorial-header {
  font-family: 'Playfair Display', serif;
  font-size: clamp(3rem, 8vw, 8rem);
  font-weight: 700;
  line-height: 0.9;
  letter-spacing: -0.03em;
  color: #1a1a1a;
}

.editorial-body {
  font-family: 'Inter', sans-serif;
  font-size: 1.125rem;
  line-height: 1.8;
  color: #444;
  max-width: 65ch; /* 最佳阅读宽度 */
}
```

### 4. 微交互动效

```css
/* 精心设计的按钮动效 */
.btn-premium {
  position: relative;
  overflow: hidden;
  background: #000;
  color: #fff;
  padding: 1rem 2rem;
  border-radius: 0;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.btn-premium::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(120deg, transparent, rgba(255,255,255,0.3), transparent);
  transform: translateX(-100%);
  transition: transform 0.6s;
}

.btn-premium:hover::before {
  transform: translateX(100%);
}

.btn-premium:active {
  transform: scale(0.98);
}
```

### 5. 响应式网格布局

```css
/* 现代 CSS Grid 布局 */
.bento-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: minmax(200px, auto);
  gap: 1.5rem;
}

.bento-item--large {
  grid-column: span 2;
  grid-row: span 2;
}

.bento-item--wide {
  grid-column: span 3;
}

@media (max-width: 768px) {
  .bento-grid {
    grid-template-columns: 1fr;
  }
  .bento-item--large,
  .bento-item--wide {
    grid-column: span 1;
    grid-row: span 1;
  }
}
```

## 🎨 常用指令与 Prompt 策略

### 1. 布局生成 (Layout)
不要只说 "生成一个着陆页"，尝试更具体的风格描述：
```bash
# ❌ 错误示范
/ui-design 生成一个科技感着陆页

# ✅ 正确示范
/ui-design 生成一个 Neo-Brutalism 风格的着陆页。使用高饱和度的橙色和黑色，厚重的边框，巨大的无衬线标题，并且布局要打破常规网格。
```

### 2. 组件样式 (Component)
```bash
# 生成具有杂志质感的卡片
/ui-design 设计一个 Article Card。使用衬线字体 (Playfair Display)，大留白，图片带有视差滚动效果，鼠标悬停时卡片轻微上浮并投射长阴影。
```

### 3. 即时重构 (Refactor)
```bash
# 拯救平庸设计
/ui-design 重新设计这个 Hero Section。现在的太普通了。把它改成极简主义风格，使用巨大的文字排版作为主视觉，去掉所有多余的装饰，只保留黑白两色和极细的分割线。
```

## �️ 技术栈推荐
- **CSS Framework**: Tailwind CSS (推荐), CSS Modules.
- **Animation**: Framer Motion (React), GSAP, 或原生 CSS Transitions.
- **Icons**: Lucide React, Remix Icon (避免 FontAwesome).
