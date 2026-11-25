---
name: wps-office
description: Operate WPS Office desktop suite (WPS 文字 / 表格 / 演示) via simulated keyboard and mouse through clawtouch-mcp — exact menu paths, shortcut differences from MS Office, and cloud-save dialog handling. Tested against WPS Office 2024 on Windows. Load when the user wants to edit, read, or automate WPS document / spreadsheet / presentation files.
---

# Skill: WPS Office (文字 / 表格 / 演示)

For LLM agents driving **WPS Office** through `clawtouch-mcp`. WPS is
the dominant office suite in mainland China; the UI is similar to
Microsoft Office but with non-trivial shortcut and menu-path
differences that bite agents trained mostly on MS Office documentation.

> **Tested against**: WPS Office **2024** (个人版 / 教育版) on
> Windows 10/11 (zh-CN). Last verified 2026-05-26.
>
> ⚠️ WPS releases new major versions roughly yearly with ribbon and
> shortcut adjustments. WPS 2019 / 2021 have noticeably different
> menu paths in places. If a step doesn't match what you see, please
> open an issue at
> [tinqiao-oss/clawtouch-skills](https://github.com/tinqiao-oss/clawtouch-skills/issues).

## When to use this skill

The user wants to operate WPS 文字 (Writer), WPS 表格 (Spreadsheets),
or WPS 演示 (Presentation). If the user has both WPS and MS Office
installed and isn't explicit, **default to WPS in China-locale
environments** (where WPS is usually the system default for `.docx`).

## Common across all three apps

- **Top menu**: `Alt` triggers the menu bar (Alt+F = File, Alt+H = Home, …)
- **File operations**: `Ctrl+N` new, `Ctrl+O` open, `Ctrl+S` save,
  `Ctrl+P` print — same as MS Office
- **Cloud save dialog on Ctrl+S**: WPS may prompt to save to WPS Cloud.
  Press `Escape` then re-issue local save via `Alt+F` → arrow to
  "另存为" (Save As) → Enter
- **Tab switching between open docs**: `Ctrl+Tab`

## WPS 文字 (Writer) — document editing

| Task | Step sequence |
|------|---------------|
| Insert table | Press `Alt` to show ribbon KeyTips, then the letter over **插入 (Insert)** — it varies by WPS version/locale, so read it on screen rather than assuming, or click the 插入 ribbon tab → "表格" → set rows/cols |
| Bold selected text | Select first (e.g. `hid.key("ctrl+shift+right")` repeatedly), then `hid.key("ctrl+b")` |
| Find / replace | `hid.key("ctrl+h")` |
| Go to page | `hid.key("ctrl+g")` opens "定位" dialog → type page number → Enter |
| Track changes on / off | `hid.key("ctrl+shift+e")` toggles 修订模式 |

### WPS vs Word differences

- **选择性粘贴** (paste special): `Ctrl+Alt+V` — same as Word, but dialog options ordered differently
- **Comment shortcut**: `Ctrl+Alt+M`, same as Word
- **格式刷** (format painter): toolbar button only — no stable keyboard shortcut

## WPS 表格 (Spreadsheets)

| Task | Step sequence |
|------|---------------|
| Go to specific cell | `hid.key("ctrl+g")` → type `B5` → Enter |
| Enter formula | `hid.type("=SUM(A1:A4)")` → `hid.key("enter")` |
| Select column of active cell | `hid.key("ctrl+space")` |
| Select row of active cell | `hid.key("shift+space")` |
| Insert row above active row | `hid.key("ctrl+shift+=")` opens dialog → arrow to "整行" → Enter (also accepts `ctrl+shift+plus` / `ctrl+shift+equal` aliases) |
| Next / previous sheet | `hid.key("ctrl+pagedown")` / `hid.key("ctrl+pageup")` |
| Filter toggle | `hid.key("ctrl+shift+l")` |

### WPS 表格 vs Excel differences

- Cell formatting dialog: both open with `Ctrl+1`, but tab order differs
- Some Excel-only functions don't exist in older WPS (e.g. `XLOOKUP`); fall back to `VLOOKUP`
- WPS's "数据透视表" (pivot table) wizard differs visually from Excel's

## WPS 演示 (Presentation)

| Task | Step sequence |
|------|---------------|
| New slide after current | `hid.key("ctrl+m")` |
| Start slideshow from current slide | `hid.key("shift+f5")` |
| Start slideshow from beginning | `hid.key("f5")` |
| Exit slideshow | `hid.key("escape")` |
| Insert text box | Toolbar only — no keyboard shortcut |

## Known gotchas

- **WPS Cloud upsell**: first launch (and occasionally afterwards)
  WPS shows a cloud-save banner / popup. Dismiss with `hid.key("escape")`
  before the actual task.
- **Auto-save dialogs**: enabled by default in some installs — a
  surprise dialog can swallow a typed character.
- **Floating selection toolbar**: selecting text triggers a floating
  contextual toolbar that intercepts mouse clicks. Move cursor away
  (`hid.move` to a safe area) before clicking elsewhere.
- **Mixed Chinese / English typing**: WPS doesn't switch IME for you, and
  `hid.type` can't produce Chinese at all through an active IME. For any
  literal Chinese / non-ASCII text, paste it from the clipboard instead —
  see the [paste-text skill](../paste-text/SKILL.md). For shortcuts
  (`Ctrl+X` etc.) the IME doesn't matter.

## When this skill doesn't help

- Cross-document operations (open A, copy, switch to B, paste): the
  OS / shell handles those, not WPS internals
- WPS Cloud sharing dialogs: highly dynamic, fall back to screenshot
  + LLM reasoning
- Macros / VBA: use the macro editor directly, not HID
