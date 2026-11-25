---
name: media-chrome-skills
description: |
  Media Chrome 组件库使用指南和最佳实践。用于开发视频/音频播放器、集成媒体控件、定制播放器主题。
  当需要创建、配置或定制媒体播放器时，使用此 skill。包含快速上手、组件详解、样式定制、多源媒体支持、最佳实践、踩坑指南和高级功能。
---

# Media Chrome Skills

## 概述

Media Chrome 是一个基于 Web Components 的媒体播放器控制组件库，提供完全可定制的音频和视频播放器控制界面。具有框架无关性、支持多种媒体元素、简单 HTML/CSS 控制的特点。

**核心特性：**
- 兼容任何 JavaScript 框架（React、Angular、Svelte 等）
- 支持 `<video>`、`<audio>` 及多种媒体源（YouTube、HLS、DASH 等）
- 简单的 HTML 标签添加/移除控件
- CSS 变量轻松定制样式

## 何时使用此 Skill

- 搭建视频/音频播放器
- 定制播放器控件和样式
- 接入第三方媒体源（YouTube、HLS 等）
- 解决播放器开发中的常见问题
- 实现高级功能（键盘快捷键、主题系统等）

---

## 快速开始

### 安装方式

**CDN 引入（推荐快速原型开发）：**
```html
<script type="module" src="https://cdn.jsdelivr.net/npm/media-chrome@4/+esm"></script>
```

**NPM 安装：**
```bash
npm install media-chrome
```

**React 项目：**
```bash
npm install media-chrome
# 或使用 React 包装器
npm install media-chrome/react
```

### 最小视频播放器

```html
<script type="module" src="https://cdn.jsdelivr.net/npm/media-chrome@4/+esm"></script>

<media-controller>
  <video slot="media" src="video.mp4"></video>
  <media-control-bar>
    <media-play-button></media-play-button>
    <media-mute-button></media-mute-button>
    <media-time-range></media-time-range>
    <media-fullscreen-button></media-fullscreen-button>
  </media-control-bar>
</media-controller>
```

### 最小音频播放器

```html
<script type="module" src="https://cdn.jsdelivr.net/npm/media-chrome@4/+esm"></script>

<media-controller audio>
  <audio slot="media" src="audio.mp3"></audio>
  <media-control-bar>
    <media-play-button></media-play-button>
    <media-time-range></media-time-range>
    <media-mute-button></media-mute-button>
    <media-volume-range></media-volume-range>
  </media-control-bar>
</media-controller>
```

**核心概念：**
- `<media-controller>` 是核心容器，管理所有媒体状态
- `slot="media"` 指定媒体元素（video/audio/其他）
- `audio` 属性标记为音频播放器
- 控制组件（按钮、滑块等）嵌套在控制器内

**参考完整示例：** `examples/basic-video.html` 和 `examples/basic-audio.html`

---

## 核心组件详解

### 容器组件

**media-controller（核心控制器）**
- 管理所有媒体状态和事件分发
- 提供键盘快捷键支持
- 支持热键配置

```html
<media-controller 
  defaultsubtitles
  hotkeys="nospace"
  keyboardforwardseekoffset="15"
  keyboardbackwardseekoffset="5">
  <!-- 媒体和控件 -->
</media-controller>
```

**media-control-bar（控制条容器）**
- 水平排列控制组件
- 自动处理布局和间距

### 按钮类组件

| 组件 | 功能 | 关键属性 |
|------|------|----------|
| `<media-play-button>` | 播放/暂停 | `mediapaused`（只读状态） |
| `<media-mute-button>` | 静音/取消静音 | `mediavolumechange` |
| `<media-fullscreen-button>` | 全屏切换 | `mediaisfullscreen` |
| `<media-pip-button>` | 画中画 | `mediapipunavailable` |
| `<media-airplay-button>` | AirPlay 投屏 | `mediaairplayunavailable` |
| `<media-cast-button>` | Chromecast 投屏 | `mediacastunavailable` |
| `<media-captions-button>` | 字幕开关 | `mediasubtitleslist` |
| `<media-loop-button>` | 循环播放 | `medialooped` |
| `<media-playback-rate-button>` | 播放速率 | `mediaplaybackrate` |
| `<media-seek-forward-button>` | 快进 | `seekoffset="15"` |
| `<media-seek-backward-button>` | 快退 | `seekoffset="5"` |

### 显示类组件

| 组件 | 功能 | 关键属性 |
|------|------|----------|
| `<media-time-display>` | 当前时间显示 | `showduration`（显示总时长） |
| `<media-duration-display>` | 总时长显示 | - |
| `<media-poster-image>` | 封面图片 | `src`, `slot="poster"` |
| `<media-loading-indicator>` | 加载指示器 | - |
| `<media-preview-thumbnail>` | 预览缩略图 | 配合 time-range 使用 |

### 滑块类组件

**media-time-range（时间轴进度条）**
- 显示播放进度和缓冲进度
- 支持预览缩略图
- 支持章节标记

```html
<media-time-range>
  <!-- 可选：预览缩略图 -->
  <media-preview-thumbnail slot="preview"></media-preview-thumbnail>
  <media-preview-time-display slot="preview"></media-preview-time-display>
</media-time-range>
```

**media-volume-range（音量滑块）**
```html
<media-volume-range></media-volume-range>
```

### 菜单类组件

```html
<!-- 设置菜单 -->
<media-settings-menu anchor="auto">
  <media-settings-menu-item>
    Speed
    <media-playback-rate-menu slot="submenu" hidden></media-playback-rate-menu>
  </media-settings-menu-item>
  <media-settings-menu-item>
    Quality
    <media-rendition-menu slot="submenu" hidden></media-rendition-menu>
  </media-settings-menu-item>
</media-settings-menu>
```

**菜单类型：**
- `<media-captions-menu>` - 字幕选择
- `<media-rendition-menu>` - 画质选择
- `<media-audio-track-menu>` - 音轨选择
- `<media-playback-rate-menu>` - 播放速率选择

**详细组件文档：**
- `references/components/media-controller.md` - 核心控制器
- `references/components/buttons.md` - 按钮组件
- `references/components/ranges.md` - 滑块组件
- `references/components/displays.md` - 显示组件
- `references/components/menus.md` - 菜单组件

---

## 样式定制

### CSS 变量

**核心颜色变量：**
```css
media-controller {
  --media-primary-color: #0078ff;
  --media-secondary-color: #ffffff;
  --media-text-color: #ffffff;
  --media-icon-color: #ffffff;
}
```

**控件样式变量：**
```css
media-controller {
  --media-control-background: rgba(20, 20, 30, 0.7);
  --media-control-hover-background: rgba(50, 50, 60, 0.9);
  --media-control-height: 48px;
  --media-control-padding: 10px;
  --media-button-icon-width: 24px;
  --media-button-icon-height: 24px;
}
```

**时间轴特定变量：**
```css
media-time-range {
  --media-time-range-buffered-color: rgba(255, 255, 255, 0.4);
  --media-time-range-progress-color: var(--media-primary-color);
  --media-preview-thumbnail-background: #000;
}
```

**字体变量：**
```css
media-controller {
  --media-font-family: -apple-system, BlinkMacSystemFont, sans-serif;
  --media-font-size: 14px;
  --media-font-weight: 500;
}
```

### 响应式设计

```css
/* 防止布局偏移（CLS） */
media-controller:not([audio]) {
  display: block;
  max-width: 960px;
  aspect-ratio: 16 / 9;
}

video {
  width: 100%;
  height: fit-content; /* 修复 Safari 溢出 */
}

/* 响应式控件隐藏 */
@media (max-width: 640px) {
  media-volume-range {
    display: none;
  }
}
```

**完整 CSS 变量列表：** `references/css-variables.md`

---

## 多源媒体支持

### 支持的媒体元素

| 媒体源 | 需要引入 | 示例 |
|--------|----------|------|
| HTML5 Video/Audio | 无 | `<video src="video.mp4">` |
| HLS | `hls-video-element` | `<hls-video src="playlist.m3u8">` |
| DASH | `dash-video-element` | `<dash-video src="manifest.mpd">` |
| YouTube | `youtube-video-element` | `<youtube-video src="https://youtube.com/watch?v=...">` |
| Vimeo | `vimeo-video-element` | `<vimeo-video src="https://vimeo.com/...">` |
| Mux | `@mux/mux-video` | `<mux-video playback-id="...">` |
| Cloudflare | `cloudflare-video-element` | `<cloudflare-video src="...">` |

### HLS 流媒体示例

```html
<script type="module" src="https://cdn.jsdelivr.net/npm/hls-video-element@1.1/+esm"></script>

<media-controller>
  <hls-video
    slot="media"
    src="playlist.m3u8"
    stream-type="on-demand"
    crossorigin>
    <!-- 预览缩略图 -->
    <track kind="metadata" label="thumbnails" src="storyboard.vtt">
    <!-- 章节 -->
    <track kind="chapters" src="chapters.vtt">
  </hls-video>
  <!-- 控件 -->
</media-controller>
```

### YouTube 示例

```html
<script type="module" src="https://cdn.jsdelivr.net/npm/youtube-video-element@1.0/+esm"></script>

<media-controller>
  <youtube-video
    slot="media"
    src="https://www.youtube.com/watch?v=dQw4w9WgXcQ">
  </youtube-video>
  <!-- 控件 -->
</media-controller>
```

**完整媒体源配置：** `references/supported-media-elements.md`

---

## 最佳实践

### 性能优化

1. **防止布局偏移（CLS）**
   - 始终设置 `aspect-ratio` 或固定高度
   - 使用 CSS 预留空间

2. **按需加载控件**
   - 使用 `unavailable` 属性自动隐藏不可用控件
   ```css
   media-airplay-button[mediaairplayunavailable],
   media-cast-button[mediacastunavailable],
   media-pip-button[mediapipunavailable] {
     display: none;
   }
   ```

3. **延迟加载媒体**
   ```html
  <video slot="media" preload="metadata" poster="poster.jpg">
   ```

### 可访问性（a11y）

- 所有按钮内置 ARIA 标签
- 支持完整的键盘导航
- 屏幕阅读器友好

**键盘快捷键：**
- `Space/K` - 播放/暂停
- `M` - 静音
- `F` - 全屏
- `←/→` - 快退/快进
- `↑/↓` - 音量增/减

### 框架集成

**React 使用注意事项：**
- 使用 `class=` 而非 `className=`
- 推荐使用官方 React 包装器：`media-chrome/react`

```jsx
import { MediaController, MediaPlayButton } from 'media-chrome/react';

<MediaController>
  <video slot="media" src="video.mp4" />
  <MediaPlayButton />
</MediaController>
```

**详细最佳实践：** `references/best-practices.md`

---

## 常见问题与踩坑

### 问题 1: 组件未定义

**症状：** 控件不显示或显示为普通 HTML 元素

**原因：** Web Components 未加载完成

**解决方案：**
```css
/* 隐藏未定义元素 */
:not(:defined) {
  display: none;
}

/* 等待定义 */
media-controller:defined {
  display: block;
}
```

### 问题 2: 布局偏移/闪烁

**症状：** 页面加载时控件位置跳动

**解决方案：**
```css
media-controller:not([audio]) {
  display: block;
  max-width: 960px;
  aspect-ratio: 16 / 9;
  background: #000;
}
```

### 问题 3: React 中使用报错

**症状：** React 项目中属性不生效

**原因：** Web Components 与 React 属性系统差异

**解决方案：**
- 使用 `class=` 替代 `className=`
- 使用 `mediaplaybackrate=` 替代 `mediaPlaybackRate=`
- 推荐使用 React 包装器

### 问题 4: 控件无法控制媒体

**症状：** 点击按钮无反应

**原因：** 媒体元素未正确关联控制器

**解决方案：**
```html
<!-- 嵌套方式（推荐） -->
<media-controller>
  <video slot="media" src="video.mp4"></video>
  <media-play-button></media-play-button>
</media-controller>

<!-- 外部关联方式 -->
<media-controller id="my-controller"></media-controller>
<video src="video.mp4"></video>
<media-play-button mediacontroller="my-controller"></media-play-button>
```

### 问题 5: 内存泄漏

**症状：** 频繁创建/销毁播放器后内存占用过高

**解决方案：**
- 确保组件正确清理
- 监听 `disconnectedCallback`
- 参考 `examples/memory-leak-test.html`

**完整踩坑指南：** `references/troubleshooting.md`

---

## 高级功能

### 状态事件系统

**监听播放状态：**
```javascript
const controller = document.querySelector('media-controller');

// 请求事件（用户操作）
controller.addEventListener('mediaplayrequest', (e) => {
  console.log('Play requested');
});

// 状态变更事件
controller.addEventListener('mediapausedchange', (e) => {
  console.log('Paused state:', e.detail);
});
```

**常用事件：**
- `mediaplayrequest` / `mediapauserequest` - 播放/暂停请求
- `mediamuterequest` / `mediaunmuterequest` - 静音请求
- `mediaseekrequest` - 跳转请求
- `mediavolumechange` - 音量变更
- `mediatimeupdate` - 时间更新

**完整事件列表：** `references/media-events.md`

### 键盘快捷键定制

**禁用特定快捷键：**
```html
<media-controller hotkeys="nospace noarrowleft noarrowright">
  <!-- 禁用空格键和左右箭头 -->
</media-controller>
```

**自定义跳转偏移：**
```html
<media-controller
  keyboardforwardseekoffset="15"
  keyboardbackwardseekoffset="5">
</media-controller>
```

### MediaStore 集成

React 项目可使用 MediaStore hooks：

```jsx
import { useMediaState } from 'media-chrome/react';

function CustomPlayButton() {
  const paused = useMediaState('paused');
  return <button>{paused ? 'Play' : 'Pause'}</button>;
}
```

**MediaStore 详解：** `references/media-store.md`

### 主题系统

```html
<media-theme>
  <media-controller>
    <!-- 播放器内容 -->
  </media-controller>
</media-theme>
```

**主题开发：** `references/themes.md`

---

## 示例文件

本 skill 包含多个示例文件，位于 `examples/` 目录：

| 文件 | 说明 |
|------|------|
| `basic-video.html` | 最小视频播放器 |
| `basic-audio.html` | 最小音频播放器 |
| `advanced-controls.html` | 完整控件演示 |
| `hls-streaming.html` | HLS 流媒体播放 |
| `youtube-embed.html` | YouTube 嵌入 |
| `dark-theme.html` | 暗色主题定制 |
| `responsive.html` | 响应式布局 |
| `state-events.html` | 状态事件监听 |

---

## 参考资源

### 官方资源
- 官方文档: https://media-chrome.org/docs
- GitHub 仓库: https://github.com/muxinc/media-chrome
- 在线示例: https://media-chrome.mux.dev/examples/vanilla/

### 参考文档

本 skill 包含以下参考文档（位于 `references/` 目录）：

| 文档 | 说明 |
|------|------|
| `components-catalog.md` | 完整组件清单、API、图标 Slot、React 命名映射 |
| `css-variables.md` | 所有 CSS 变量列表 |
| `styling.md` | 自定义图标、条件样式、::part()、调色板 |
| `themes.md` | CSS 变量主题 + `<media-theme>` 模板系统（变量/条件/片段/响应式/自定义 Slot/NPM 分发） |
| `responsive-design.md` | 断点系统、Container Queries、响应式布局 |
| `supported-media-elements.md` | 支持的媒体源详解 |
| `best-practices.md` | 详细最佳实践 |
| `troubleshooting.md` | 完整踩坑指南 |
| `media-events.md` | 所有事件类型 |
| `media-store.md` | React MediaStore Hooks（MediaProvider、useMediaRef/Selector/Dispatch 等） |
| `stream-type.md` | 流类型（live/on-demand）、UI 适配、DVR |
| `prevent-layout-shift.md` | CLS 防止（aspect-ratio、预加载策略） |
| `slots-positioning.md` | Slots 定位和控件布局 |
| `keyboard-shortcuts.md` | 键盘快捷键 |
| `internationalization.md` | 国际化 |
| `architecture.md` | 架构设计 |

---

## 快速决策树

```
需要搭建播放器？
├─ 第一次使用？
│  └─ 查看"快速开始" + examples/basic-video.html
│
├─ 需要定制控件？
│  └─ 查看"核心组件详解" + references/components-catalog.md
│
├─ 需要定制样式？
│  └─ 查看"样式定制" + references/css-variables.md + references/styling.md
│
├─ 需要自定义图标？
│  └─ 查看 references/styling.md（自定义图标章节）
│
├─ 需要接入第三方媒体？
│  └─ 查看"多源媒体支持" + references/supported-media-elements.md
│
├─ 需要创建可分享的主题？
│  └─ 查看 references/themes.md（<media-theme> 模板主题）
│
├─ 需要响应式布局？
│  └─ 查看 references/responsive-design.md
│
├─ React 项目？
│  └─ 查看 references/media-store.md
│
├─ 直播流场景？
│  └─ 查看 references/stream-type.md
│
├─ 遇到布局跳动问题？
│  └─ 查看 references/prevent-layout-shift.md
│
├─ 遇到问题？
│  └─ 查看"常见问题与踩坑" + references/troubleshooting.md
│
└─ 需要高级功能？
   └─ 查看"高级功能" + 对应 reference 文档
```

---

## 技术信息

**版本：** Media Chrome v4.x  
**技术栈：** Web Components (Custom Elements), Shadow DOM, TypeScript  
**浏览器支持：** 所有现代浏览器（Chrome、Firefox、Safari、Edge）  
**框架兼容性：** React, Vue, Angular, Svelte, 原生 HTML/JS
