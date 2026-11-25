---
name: petdex
description: Install and select animated petdex mascots for Hermes.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [petdex, mascot, display, cli, tui, desktop]
    category: productivity
    homepage: https://petdex.dev
---

# Petdex 技能

可从公共 [petdex](https://github.com/crafter-station/petdex) 图库中浏览、安装并选择动画形式的“宠物”吉祥物。安装后的宠物会针对 Hermes CLI、TUI 以及桌面应用中的各种状态（空闲、运行工具、正在查看、出错、已完成）做出相应反应。该技能负责驱动 `hermes pets` CLI 命令以及 `display.pet` 配置——它并不负责生成精灵图。

## 适用场景

- 用户希望使用桌面端/终端端的吉祥物，或询问有关“宠物”/petdex 的信息。
- 用户想要更改、预览或禁用当前激活的宠物。
- 排查为何某个宠物未显示的问题（与终端图形支持及配置相关）。

## 先决条件

- 能够访问 `petdex.dev` 以获取图库和清单内容（仅读权限，无需认证）。
- 需要 Pillow（Hermes 的核心依赖项）用于精灵图解码——该工具通常已预装。
- 如需在终端中实现高保真渲染，需使用具备图形处理功能的终端（如 kitty、Ghostty、WezTerm、iTerm2 或 sixel）。否则系统会自动切换为真彩色 Unicode 半块字符作为替代方案。

## 运行方法

使用 `terminal` 工具来执行 `hermes pets <subcommand>` 命令。

## 快速参考表

| 目标 | 命令 |
| --- | --- |
| 浏览图库 | `hermes pets list`（可添加子字符串进行筛选：`hermes pets list cat`） |
| 列出已安装的宠物 | `hermes pets list --installed` |
| 安装宠物 | `hermes pets install <slug>`（添加 `--select` 可使其立即激活） |
| 设置激活的宠物 | `hermes pets select <slug>`（省略 slug 参数则会出现选择器） |
| 调整所有界面中宠物的大小 | `hermes pets scale <factor>`（例如 `0.5`，范围限制在 0.1–3.0 之间） |
| 在终端中预览/播放动画 | `hermes pets show [slug] [--cycle] [--state run]` |
| 禁用宠物 | `hermes pets off` |
| 移除宠物 | `hermes pets remove <slug>` |
| 检查配置是否正常 | `hermes pets doctor` |

## 操作步骤

1. 查找合适的宠物：执行 `hermes pets list <query>`，记下其 `slug` 值。
2. 安装并激活：执行 `hermes pets install <slug> --select`。
3. 进行预览：执行 `hermes pets show`（按 Ctrl+C 可停止预览）。
4. 确认配置状态：执行 `hermes pets doctor`——该命令会显示最终选定的宠物、配置的渲染模式、检测到的终端图形协议以及当前实际生效的模式。

宠物会被安装到 `<HERMES_HOME>/pets/<slug>/` 目录下（支持根据用户配置文件进行区分）。选定某个宠物后，系统会将 `display.pet.slug` 和 `display.pet.enabled` 的值写入 `config.yaml` 文件中。

## 配置选项

在 `config.yaml` 文件的 `display.pet` 部分可设置以下参数：

- `enabled`（布尔值）——整体开关控制。
- `slug`（字符串）——当前激活的宠物；留空则表示使用第一个已安装的宠物。
- `render_mode`——可选值为 `auto`（自动检测）、`kitty`、`iterm`、`sixel`、`unicode` 或 `off`。
- `scale`（浮点数）——原生 192×208 像素图帧在屏幕上的显示尺寸（默认值为 0.33，范围限制在 0.1–3.0 之间）。调整此值可同时改变所有界面中的宠物大小；可通过 `hermes pets scale <factor>` 命令、`/pet scale` 分隔符命令或桌面端的“外观”滑块来进行设置。
- `unicode_cols`（整数）——Unicode 替代方案下的字符宽度。

## 常见问题与注意事项

- 宠物只有在既已安装又处于激活状态（即 `enabled: true`）时才会显示。
- 在管道或重定向操作中（即没有 TTY 的情况下），系统会按设计要求禁用终端渲染功能。
- petdex 的 npm CLI 会将宠物安装到 `~/.codex/pets` 目录下；而 Hermes 则使用自己基于用户配置文件的 `<HERMES_HOME>/pets/` 目录——请通过 `hermes pets` 命令进行安装。

## 验证方法

如果宠物已正确安装、处于激活状态、开关已开启且 Pillow 可正常导入，执行 `hermes pets doctor` 后会显示 `✓ ready` 的提示。
