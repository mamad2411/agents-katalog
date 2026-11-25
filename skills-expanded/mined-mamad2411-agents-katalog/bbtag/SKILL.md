---
name: bbtag
description: 'Push content to BluETag (蓝签) e-ink display via Bluetooth. Use this skill whenever the user wants to send text, images, reminders, menus, schedules, or any content to their bbtag/蓝签 device. Also trigger when the user wants to preview content, scan for nearby devices, or check device status. Key phrases: 推送到蓝签, 发给老婆, 更新蓝签显示, push to bbtag, send to display.'
version: 1.0.0
user-invocable: true
argument-hint: "[内容描述]"
---

# bbtag — 蓝签推送工具

## 安装

首先检查 `bluetag` 是否已全局安装：

```bash
bluetag --version
```

如果命令不存在，切换到项目根目录（含 `pyproject.toml` 的目录）执行安装：

```bash
cd /path/to/bbtag && uv tool install .
```

安装后 `bluetag` 即为全局命令，可在任意目录使用。

---

## 基本用法

### 推送文字
```bash
bluetag text "正文内容" --title "标题"
```

正文支持 `\n` 换行：
```bash
bluetag text "家烧黄鱼\n凉拌猪耳朵\n炒青菜" --title "晚餐菜单"
```

仅预览，不推送：
```bash
bluetag text "正文" --title "标题" --preview-only
```

### 推送图片
```bash
bluetag push /path/to/image.png
```

### 扫描设备
```bash
bluetag scan
```

---

## 样式选项

| 参数 | 可选值 | 默认 |
|------|--------|------|
| `--title-color` | black / red / yellow | red |
| `--body-color` | black / red / yellow | black |
| `--separator-color` | black / red / yellow | yellow |
| `--align` | left / center | left |
| `--screen` | 3.7inch / 2.13inch | 3.7inch |

默认配色（红标题 + 黄分隔线 + 黑正文）在 3.7inch 屏幕上效果很好。

---

## 屏幕规格

| 型号 | 分辨率 | 支持颜色 |
|------|--------|---------|
| 3.7inch | 240×416 | 黑 / 白 / 红 / 黄 |
| 2.13inch | 250×122 | 黑 / 白 / 红 |

---

## 工作流

1. 理解用户想推送的内容（标题、正文、样式需求）
2. 先用 `--preview-only` 生成预览让用户确认
3. 用户确认后执行推送

---

## 常见场景示例

**菜单**：
```bash
bluetag text "家烧黄鱼\n凉拌猪耳朵\n炒青菜" --title "晚餐菜单"
```

**提醒**：
```bash
bluetag text "下午3点开会\n记得带资料" --title "今日提醒" --title-color black --separator-color red
```

**居中对齐**：
```bash
bluetag text "内容" --title "标题" --align center
```
