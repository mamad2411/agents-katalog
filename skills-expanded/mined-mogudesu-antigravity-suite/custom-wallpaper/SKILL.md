---
name: custom-wallpaper
description: >-
  Manage Antigravity workspace background wallpapers, theme transparency, frosted glass blur,
  auto palette, star-rail conversation navigation, and the unified plugin / skill deck.
  Use when user wants to change, adjust, or restore the Antigravity visual theme.
---

# Antigravity Wallpaper & Background Manager

Manage workspace visual styles and custom anime/aesthetic wallpapers.

## Quick Actions
- Apply wallpaper: `node ~/.gemini/config/plugins/Antigravity 星夜美化-mogu/scripts/apply.js [path] [opacity]`
- Restore default: `node ~/.gemini/config/plugins/Antigravity 星夜美化-mogu/scripts/restore.js`
- Live controls: `POST http://127.0.0.1:39290/api/live` with `opacity` / `blur` / `darkTint` / `focusX` / `focusY` / `palette`
- Persist config: `POST http://127.0.0.1:39290/api/config`
- Open panel: `[星夜换肤控制台](sidecar://antigravity-custom-wallpaper/wallpaper_panel/ui.html)`

## In-app UI
- Sidebar: conversation list first, compact quota dock at the bottom (click to expand).
- Right-edge star rail: jump between conversation turns.
- Composer deck: 插件 / 技能库 / 收藏，支持搜索与 `<SKILL>` 标签插入。
- Effort slider: 连续拖动、GPU 弹簧回弹；模型下拉里也有连续滑杆；`Alt+1/2/3` 快捷键。
- 3D cartoon star cosmos: composer orbit ring, corner charms, meteor showers, send burst; modes / intensity / meteor frequency in the console.
- Font presets: 星刊雅宋 / 现代几何 / 人文书卷 / 星夜萌圆, live switching +正文 scale.
- Prompt pin: 默认不吸顶；控制台可开启「提问吸顶（吸顶时压缩成一行）」。
- Memory manager: 侧栏「自定义配置」下方的「记忆管理」打开 Mnemon 工作台（PERSONA/USER/MEMORY 编辑、备份、记忆空间条目），实现位于 `scripts/memory-page.js`。
- `Alt+Z`: immersive wallpaper mode.

## Console tabs
- 视觉: wallpaper, glass, palette, fonts, star cosmos, prompt pin, apply/restore.
- 记忆: edit PERSONA.md / USER.md / MEMORY.md, mirror status, immediate backup, read-only memory entries (mnemon).
- 控制: computer-use policy/status and browser-bridge port/extension/Edge status (computer-use + antigravity-browser-bridge; bridge port 8767).
