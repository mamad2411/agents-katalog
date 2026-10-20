---
description: CodeSpirit CSS 样式规范 - 命名约定、主题系统、动画效果、AMIS样式覆盖
globs: *.css
alwaysApply: false
---

# CSS 样式规范

## AMIS 主题集成

- 样式编写结合 AMIS 官方样式指南：https://aisuda.bce.baidu.com/amis/zh-CN/style/index
- 项目使用 **antd** 主题，覆盖样式使用 `.antd-*` 前缀
- cxd 主题样式使用 `.cxd-*` 前缀

## CSS 变量系统

使用 `:root` 统一定义设计令牌，便于主题切换和一致性维护：

```css
:root {
    /* 颜色系统 */
    --primary-color: #007bff;
    --success-color: #28a745;
    --warning-color: #ffc107;
    --danger-color: #dc3545;
    --info-color: #17a2b8;
    
    /* 灰色色阶 */
    --gray-100: #f8f9fa;
    --gray-200: #e9ecef;
    --gray-300: #dee2e6;
    --gray-600: #6c757d;
    --gray-800: #343a40;
    
    /* 间距系统 */
    --spacing-xs: 0.25rem;   /* 4px */
    --spacing-sm: 0.5rem;    /* 8px */
    --spacing-md: 1rem;      /* 16px */
    --spacing-lg: 1.5rem;    /* 24px */
    
    /* 字体系统 */
    --font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    --font-size-sm: 0.875rem;
    --font-size-md: 1rem;
    --font-size-lg: 1.125rem;
    
    /* 阴影系统 */
    --shadow-sm: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
    --shadow-md: 0 0.25rem 0.5rem rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
    
    /* 边框系统 */
    --border-radius: 0.375rem;
    --border-radius-sm: 0.25rem;
    --border-radius-lg: 0.5rem;
    
    /* 过渡动画 */
    --transition: all 0.3s ease;
    --transition-fast: all 0.15s ease;
}
```

## 命名约定

### 模块前缀命名

使用模块/功能前缀避免样式冲突：

| 模块 | 前缀 | 示例 |
|-----|-----|------|
| 考试系统 | `exam-` | `.exam-container`, `.exam-timer` |
| 问卷系统 | `survey-` | `.survey-participate-page` |
| 租户管理 | `tenant-` | `.tenant-admin-wrapper` |
| 聊天功能 | `chat-` | `.chat-container`, `.chat-message` |
| AMIS 卡片 | `amis-cards-` | `.amis-cards-page`, `.amis-cards-card` |

### BEM-like 命名

```css
/* 块 */
.exam-container { }

/* 元素 */
.exam-container .exam-header { }
.exam-container .exam-body { }

/* 修饰符 */
.exam-container--compact { }
.exam-timer--urgent { }
```

### 状态类命名

```css
.is-active { }
.is-checked { }
.is-loading { }
.is-error { }
.is-focused { }
.has-error { }
```

## 动画效果

### 过渡动画

动效要自然、高效，推荐使用 `cubic-bezier` 缓动函数：

```css
/* 标准过渡 */
transition: all 0.3s ease;

/* 弹性过渡 */
transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);

/* 回弹效果 */
transition: all 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
```

### 关键帧动画

```css
/* 渐入动画 */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* 脉冲动画 */
@keyframes pulse {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.05); opacity: 0.8; }
}

/* 旋转加载 */
@keyframes spin {
    to { transform: rotate(360deg); }
}

/* 光晕效果 */
@keyframes shimmer {
    0% { left: -100%; }
    100% { left: 100%; }
}
```

### 悬停交互

```css
.card:hover {
    transform: translateY(-3px) scale(1.01);
    box-shadow: var(--shadow-lg);
}

.button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,123,255,0.3);
}

.button:active {
    transform: translateY(0);
}
```

## 主题系统

### 亮色/暗色主题

```css
/* 系统偏好检测 */
@media (prefers-color-scheme: dark) {
    :root {
        --bg-color: #1f2937;
        --text-color: #e5e7eb;
        --border-color: #374151;
    }
}

/* 强制暗色主题类 */
.theme-dark {
    --bg-color: #1f2937;
    --text-color: #e5e7eb;
}
```

### 主题变体类

```css
.theme-primary { --theme-color: var(--primary-color); }
.theme-success { --theme-color: var(--success-color); }
.theme-warning { --theme-color: var(--warning-color); }
.theme-danger { --theme-color: var(--danger-color); }
```

## 响应式设计

### 标准断点

```css
/* 超小屏幕 (手机) */
@media (max-width: 480px) { }

/* 小屏幕 (大手机/小平板) */
@media (max-width: 768px) { }

/* 中等屏幕 (平板) */
@media (max-width: 992px) { }

/* 大屏幕 (笔记本) */
@media (max-width: 1200px) { }

/* 超大屏幕 (桌面) */
@media (max-width: 1400px) { }
```

### 移动优先示例

```css
.container {
    padding: 1rem;
}

@media (min-width: 768px) {
    .container {
        padding: 1.5rem;
    }
}

@media (min-width: 1200px) {
    .container {
        padding: 2rem;
    }
}
```

## AMIS 样式覆盖

### antd 主题覆盖

```css
/* 表单项 */
.antd-Form-item {
    margin-bottom: 24px;
    padding: 20px;
    background: #fafbfc;
    border-radius: 8px;
}

/* 按钮 */
.antd-Button--primary {
    background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
    border: none;
    border-radius: 8px;
}

/* 表格 */
.antd-Table-table thead th {
    background: var(--gray-100) !important;
    font-weight: 600 !important;
}
```

### cxd 主题覆盖

```css
.cxd-Panel {
    background: var(--card-bg);
    border-radius: var(--border-radius-lg);
    box-shadow: var(--shadow-md);
}

.cxd-Panel-header {
    padding: 16px 24px;
    border-bottom: 1px solid var(--border-color);
}
```

## 性能优化

### GPU 加速

```css
/* 开启硬件加速 */
.animated-element {
    will-change: transform, opacity;
    backface-visibility: hidden;
    transform: translateZ(0);
}
```

### 减少重绘

```css
/* 避免使用 */
.avoid {
    box-shadow: /* 复杂阴影 */;
    filter: blur(10px);
}

/* 推荐使用 transform 代替 */
.recommended {
    transform: translateY(-2px);
}
```

### 减少动画（无障碍）

```css
@media (prefers-reduced-motion: reduce) {
    * {
        animation: none !important;
        transition: opacity 0.3s ease !important;
    }
}
```

## 渐变和装饰效果

### 常用渐变

```css
/* 主色渐变 */
background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);

/* 柔和背景渐变 */
background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);

/* 卡片头部渐变 */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### 装饰伪元素

```css
.card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
    transform: scaleX(0);
    transition: transform 0.3s ease;
}

.card:hover::before {
    transform: scaleX(1);
}
```

## 工具类

### 常用工具类

```css
/* 文本对齐 */
.text-left { text-align: left !important; }
.text-center { text-align: center !important; }
.text-right { text-align: right !important; }

/* 显示控制 */
.d-none { display: none !important; }
.d-block { display: block !important; }
.d-flex { display: flex !important; }

/* 间距 */
.m-0 { margin: 0 !important; }
.mt-1 { margin-top: 0.25rem !important; }
.mb-2 { margin-bottom: 0.5rem !important; }
.p-2 { padding: 0.5rem !important; }
```

## 滚动条样式

```css
/* Webkit 浏览器滚动条 */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}

::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.03);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: rgba(0, 0, 0, 0.1);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(0, 0, 0, 0.2);
}

/* Firefox 滚动条 */
* {
    scrollbar-width: thin;
    scrollbar-color: rgba(0, 0, 0, 0.1) transparent;
}
```

## 禁止事项

- ❌ 不要使用 `!important` 覆盖 AMIS 核心功能样式（除非必要）
- ❌ 不要使用内联样式代替 CSS 类
- ❌ 不要使用绝对单位 `px` 定义字体大小（使用 `rem`）
- ❌ 不要创建过于复杂的选择器（超过 3 层嵌套）
- ❌ 不要在动画中使用会触发重排的属性（`width`, `height`, `top`, `left`）
- ❌ 不要忽略暗色主题适配
