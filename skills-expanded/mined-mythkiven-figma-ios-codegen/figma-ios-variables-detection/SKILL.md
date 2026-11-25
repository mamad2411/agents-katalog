---
name: figma-ios-variables-detection
description: >-
  Translate Figma Variables multi-mode warnings (already detected by figma-ios-preload-data)
  into top-of-file Swift comments so dark mode is not silently dropped.
  Use when generating Swift code from a data package whose summary.has_dark_mode is true.
---

# Figma Variables 多 Mode 警告处理（消费数据包）

## 数据来源

- `{data_dir}/manifest.json`：`summary.has_dark_mode` (bool) 与 `warnings[]`
- `{data_dir}/variables.json`：原始 Variables 数据，含每个 Mode 的 token 值（按需查阅）

## 处置规则

### 1. `has_dark_mode == true`

在生成的 Swift 文件**顶部**追加 banner 注释：

```swift
// ============================================================
// ⚠️  WARNING: Dark Mode 未生成
// ============================================================
// 设计稿在 Figma Variables 中定义了多个 Mode（含暗色模式），
// 当前生成的代码只覆盖了 Light Mode 的颜色 token。
//
// 暗色处理建议：
//   1. 用 UIColor(dynamicProvider:) 包裹关键颜色
//   2. 或基于 traitCollection.userInterfaceStyle 在 traitCollectionDidChange 切换
//   3. 详细 Mode 列表与 token 值见 {data_dir}/variables.json
// ============================================================
```

### 2. `has_dark_mode == false`

不输出任何 dark mode 注释。

### 3. 其他 warning（如 `Token referenced but not resolved`）

转为代码顶部 `// WARNING: <msg>` 单行注释。

## 自检清单

- [ ] 已读 `manifest.json`
- [ ] `has_dark_mode==true` 时已加 banner 注释
- [ ] 其他 warnings 已逐条转为代码注释
- [ ] 没有调用 `detect_figma_variables.py` 或 MCP `get_variable_defs`
