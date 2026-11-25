---
name: design-md
description: 定義與產生現代前端 UI/UX 設計系統規格書（DESIGN.md）。包含色票系統（HSL/HEX/語意色）、響應式佈局規格（Mobile 手機 390px、Tablet 平板、Desktop 桌面 1280px+）、間距網格、字體層級、深淺色主題與元件互動狀態。當需要規劃網站/App 視覺規範、UI Layout 或設計 Tokens 時使用。
version: 2.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [ui, ux, design-system, design-tokens, responsive, mobile, desktop, layout, color-palette, typography, tailwind, dark-mode]
---

# UI/UX Design System & Layout Specification (`DESIGN.md`)

專門用於為前端 Web、Mobile Web 與桌面端應用制定**結構化、跨裝置的 UI/UX 設計規範（`DESIGN.md`）**。

---

## 📐 一、標準 DESIGN.md 模板結構

```markdown
---
version: 1.0.0
name: "Modern Minimalist System"
description: "跨裝置深淺色自適應設計系統"

# 1. 色票系統 (Color Palette Tokens)
colors:
  primary: { light: "#0F172A", dark: "#F8FAFC" }
  brand: { default: "#3B82F6", hover: "#2563EB", active: "#1D4ED8" }
  background: { light: "#FFFFFF", dark: "#0B0F19", subtle: "#F1F5F9" }
  surface: { light: "#F8FAFC", dark: "#111827", elevated: "#1E293B" }
  text: { primary: "#0F172A", secondary: "#64748B", muted: "#94A3B8" }
  semantic:
    success: "#10B981"
    warning: "#F59E0B"
    error: "#EF4444"
    info: "#06B6D4"

# 2. 跨裝置響應式斷點與佈局 (Responsive Layouts)
breakpoints:
  mobile: "390px"    # iPhone / 窄螢幕直向 (單欄流式佈局、底欄導航、安全區適配)
  tablet: "768px"    # 平板 / 摺疊螢幕 (2 欄網格、可折疊側邊欄)
  desktop: "1280px"  # 標準桌面 (12 欄 Grid、固定雙欄側導航、Max-W 1200px)
  wide: "1536px"     # 超寬螢幕 (Max-W 1440px 居中置中)

# 3. 間距與圓角尺度 (Spacing & Radii)
spacing:
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "24px"
  xl: "32px"
  2xl: "48px"
radii:
  sm: "6px"
  md: "10px"
  lg: "16px"
  full: "9999px"

# 4. 字體排印 (Typography Hierarchy)
typography:
  fontFamily: "Inter, 'Noto Sans TC', system-ui, sans-serif"
  h1: { mobile: "24px / 1.2", desktop: "36px / 1.15", weight: 700 }
  h2: { mobile: "20px / 1.25", desktop: "28px / 1.2", weight: 600 }
  body: { size: "15px", lineHeight: "1.6", weight: 400 }
  caption: { size: "12px", lineHeight: "1.4", weight: 500 }
---

# UI/UX Design System Specification

## 📱 1. 跨裝置佈局原則 (Responsive Strategy)
* **Mobile First (手機端 390px)**：
  * 單欄垂直佈局，操作熱區集中於拇指易觸及的底部 1/3。
  * 點擊目標（Touch Target）高度不小於 44px。
* **Desktop (桌面端 1280px+)**：
  * 左側固定側邊欄導航（寬 240px~280px），右側為 12 欄彈性內容區域。
  * 支援懸停微動效（Hover Micro-interactions）與鍵盤快捷鍵。

## 🎨 2. 視覺與層次 (Visual Elevation & Effects)
* **毛玻璃 (Glassmorphism)**：`backdrop-blur-md bg-white/70 dark:bg-slate-900/70 border border-white/20`.
* **陰影層次 (Shadows)**：
  * `elevation-1` (卡片): `0 1px 3px rgba(0,0,0,0.05)`
  * `elevation-2` (彈窗/選單): `0 10px 25px -5px rgba(0,0,0,0.1)`

## ♿ 3. 無障礙與對比度 (Accessibility)
* 文字與背景對比度嚴格遵循 WCAG AA 規範（文字對比度 ≥ 4.5:1，標題 ≥ 3:1）。
* 所有互動按鈕均具備 `:focus-visible` 外框焦點環。
