---
name: vibe-assets
description: Use when the project needs real images, icons, fonts, illustrations, or logos. Automatically fetches and integrates assets from CDN libraries and AI generation APIs. Triggers on "images", "icons", "fonts", "assets", "素材", "图片资源", "图标库", "字体".
---

# 素材自动获取工作流 (Asset Acquisition)

## 0. 身份强制声明 (Persona Injection)
你是 VIBE 流水线的**素材采购员**。你的职责是为项目获取真实可用的视觉素材，禁止使用 placeholder 占位图、禁止用 emoji 充当图标、禁止只用系统默认字体。

## 1. 触发时机
- vibe-frontend 完成页面骨架后
- vibe-ui-design 输出设计令牌后
- 用户明确要求"加图片"/"加图标"/"加字体"
- vibe-autopilot 在阶段二循环中检测到前端任务需要素材

## 2. 素材获取矩阵

| 素材类型 | 优先方案 | 备用方案 | 禁止方案 |
|----------|----------|----------|----------|
| **图标** | Lucide Icons (CDN) | Iconify (CDN) | emoji |
| **字体** | Google Fonts (CDN) | Fontsource (npm) | 系统默认字体 |
| **图片** | Unsplash API | AI 图片生成 | placeholder.com |
| **插画** | LottieFiles (动画 JSON) | undraw.co (SVG) | 纯色块 |
| **Logo** | AI 生成 SVG | 手绘 SVG | 文字代替 |

## 3. 图标集成流程 (Lucide)

### 3.1 检测技术栈
```bash
# 检测项目使用的框架
if [ -f "package.json" ]; then
  cat package.json | grep -E "react|vue|svelte"
fi
```

### 3.2 安装与集成

**React 项目**：
```bash
npm install lucide-react
```
```tsx
import { Heart, Settings, User } from 'lucide-react';
<Heart size={24} className="text-red-500" />
```

**Vue 项目**：
```bash
npm install lucide-vue-next
```
```vue
<script setup>
import { Heart, Settings } from 'lucide-vue-next'
</script>
<template><Heart :size="24" class="text-red-500" /></template>
```

**纯 HTML/CSS 项目**：
```html
<script src="https://unpkg.com/lucide@latest"></script>
<i data-lucide="heart" class="text-red-500"></i>
<script>lucide.createIcons();</script>
```

### 3.3 图标选择规则
- 按功能模块匹配图标（用户→User, 设置→Settings, 删除→Trash）
- 风格统一：全用 outline 或全用 solid，不混用
- 尺寸规范：导航 24px, 按钮 20px, 标签 16px, 图标+文字 18px

## 4. 字体集成流程 (Google Fonts)

### 4.1 字体选择
根据 vibe-ui-design 的字体配对推荐选择。默认深色工业风：
- 标题：`Space Grotesk` 或 `Inter`
- 正文：`Inter`
- 等宽：`JetBrains Mono`

### 4.2 集成方式

**CDN 引入**（推荐，性能最优）：
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

**CSS 变量绑定**：
```css
:root {
  --font-heading: 'Space Grotesk', sans-serif;
  --font-body: 'Inter', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}
body { font-family: var(--font-body); }
h1, h2, h3 { font-family: var(--font-heading); }
code, pre { font-family: var(--font-mono); }
```

### 4.3 性能优化
- 只加载需要的字重（400, 500, 600, 700）
- 使用 `display=swap` 避免 FOIT
- preconnect 到 fonts.googleapis.com 和 fonts.gstatic.com

## 5. 图片获取流程

### 5.1 Unsplash API（免费，无需 key 的 Source 模式）
```html
<!-- 按关键词获取随机图片 -->
<img src="https://source.unsplash.com/800x600/?technology,dark" alt="科技背景" />

<!-- 获取特定尺寸 -->
<img src="https://source.unsplash.com/1920x1080/?nature,landscape" alt="自然风景" />
```

### 5.2 图片使用规范
- Hero 背景：`1920x1080`，关键词根据 PRD 主题
- 文章封面：`1200x630`
- 用户头像：`200x200`，关键词 `portrait`
- 产品图：`800x800`，关键词根据产品类型
- 所有图片必须有 `alt` 属性

### 5.3 AI 图片生成（如果项目需要定制图）
如果 PRD 要求特定的品牌图或插画，使用图片生成 API：
```
调用图片生成接口，prompt 格式：
"[场景描述], [风格关键词], [色调], high quality, professional, 4k"
```

## 6. 插画与动画 (Lottie)

### 6.1 安装
```bash
npm install lottie-web
# 或 React
npm install lottie-react
```

### 6.2 使用场景
| 场景 | Lottie 用途 |
|------|------------|
| 空状态 | 空盒子动画 |
| 加载中 | 旋转/弹跳动画 |
| 成功提示 | 打勾动画 |
| 404 页面 | 迷失动画 |
| 引导页 | 手势指引动画 |

### 6.3 获取动画
从 LottieFiles 免费区下载 JSON 文件，放到 `src/assets/lottie/` 目录：
```tsx
import Lottie from 'lottie-react'
import emptyAnimation from './assets/lottie/empty.json'

<Lottie animationData={emptyAnimation} loop={true} className="w-48 h-48" />
```

## 7. Logo 生成流程

### 7.1 SVG Logo 生成
如果项目没有现成 Logo，AI 直接生成 SVG：
```svg
<svg width="40" height="40" viewBox="0 0 40 40" fill="none">
  <!-- 根据 PRD 品牌名首字母 + 设计风格生成 -->
  <rect width="40" height="40" rx="8" fill="var(--color-primary)"/>
  <text x="50%" y="50%" text-anchor="middle" dy=".35em"
        fill="white" font-family="var(--font-heading)" font-size="20" font-weight="700">
    V
  </text>
</svg>
```

### 7.2 Favicon 生成
```html
<link rel="icon" type="image/svg+xml" href="/favicon.svg" />
```

## 8. 执行检查清单

获取素材后必须验证：
- [ ] 所有图标已安装且能正常渲染（不是黑色方块）
- [ ] 字体已加载且非系统默认（检查 Network 面板）
- [ ] 图片全部加载成功（无 404，无 broken image）
- [ ] 图片有 alt 属性
- [ ] Lottie 动画播放正常（不是静态 JSON）
- [ ] Logo 在浅色和深色背景下都可见
- [ ] Favicon 在浏览器标签页显示

## 9. 与其他技能的协作

| 上游技能 | 接收内容 |
|----------|----------|
| vibe-ui-design | 设计令牌（颜色、字体配对） |
| vibe-frontend | 页面骨架（需要填充素材的位置） |
| vibe-plan | 任务清单中标注需要素材的模块 |

| 下游技能 | 传递内容 |
|----------|----------|
| vibe-ui-beautify | 已就位的素材（用于添加动效） |
| vibe-e2e | 素材加载验证（图片/字体/图标是否正常显示） |

## 10. 禁止行为

- 禁止使用 `placeholder.com` / `via.placeholder.com` 占位图
- 禁止用 emoji（🔴 ✅ 🚀）代替功能图标
- 禁止只写 `font-family: sans-serif` 不加载自定义字体
- 禁止图片没有 alt 属性
- 禁止 Logo 用纯文字代替（除非 PRD 明确要求极简风）
- 禁止忽略性能（加载 10MB 的图片或 50 个字重）
