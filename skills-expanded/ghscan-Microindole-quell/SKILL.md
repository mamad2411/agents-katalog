---
name: tui_development
description: 基于 Bubble Tea 和 Lipgloss 的终端界面开发规范
---

# TUI 开发技能 (TUI Development)

## 核心框架
- **Bubble Tea (Elm Architecture)**: 遵循 Model-Update-View 模式。
- **Lipgloss**: 用于样式定义、布局控制和自适应。

## 开发要点
1. **状态管理**: 确保 Model 尽可能扁平，状态变更仅在 Update 中处理。
2. **样式复用**: 在 `internal/ui/styles.go` (如存在) 或特定组件中定义预设样式。
3. **性能**: 复杂列表或大型渲染应注意优化渲染频率，合理使用 `bubbles` 库中的组件。
4. **自适应**: 在 View 中捕获 `tea.WindowSizeMsg` 并动态调整 Lipgloss 的宽度和高度。

## 视觉原则
- 使用 HSL 调色板而非基础颜色。
- 增加微小的交互反馈（如 Hover 或 Focus 状态的边框加亮）。
