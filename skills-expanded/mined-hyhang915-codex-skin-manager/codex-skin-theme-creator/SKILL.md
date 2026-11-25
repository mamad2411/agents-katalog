---
name: codex-skin-theme-creator
description: Create, regenerate, or import a Codex skin theme from an image or visual idea and automatically add it to Codex 皮肤管理器. Use when the user asks to 创建 Codex 主题、生成皮肤主题、把图片做成 Codex 皮肤、重做某套主题背景, or create/import a Codex skin theme on macOS or Windows.
---

# Codex 主题创建器

把主题直接写入管理器的用户主题库。使用项目当前的 schema 2、裁切、校验和原子替换流程，不修改内置主题目录。

## 工作流

1. 明确主题名称、角色/场景、浅色或暗色倾向。缺少 ID 时生成 3–64 位小写 kebab-case ID。
2. 用户需要生图或重做背景时，先使用 `imagegen` 生成横向高质量场景图。画面不得预叠 UI、文字、白雾或黑色遮罩；主体视觉中心优先放在横向 55%–62%，左侧保留清晰环境。
3. 从画面选择强调色、辅助色和点缀色，均使用 `#RRGGBB`。横向焦点默认 `58`，多人合影按人物完整度调整。
4. 调用本 Skill 的创建脚本。脚本输出 `2400x800` 的 `background.png`、`1200x400` 的 `preview.png` 和 `theme.json`，完成后直接进入用户主题库。
5. 检查脚本返回的 JSON。`status` 必须为 `installed`；管理器打开时会自动刷新主题库。

## 创建命令

将包含本文件的 Skill 绝对目录记为 `SKILL_DIR`，然后运行：

```bash
node "$SKILL_DIR/scripts/create-theme.mjs" \
  --image "/absolute/path/source.png" \
  --id "theme-id" \
  --name "主题名称" \
  --author "作者" \
  --description "主题描述" \
  --category "角色" \
  --appearance "light" \
  --accent "#4F9FE8" \
  --secondary "#70C7B3" \
  --highlight "#E8995C" \
  --focus "58"
```

只有用户明确要求更新同一自定义主题时才添加 `--replace`。不得使用内置主题 ID。

## 验收

- 返回的 `themePath` 中只有 `theme.json`、`background.png`、`preview.png`。
- 两张图均为真实 PNG 和精确 3:1；背景人物完整，左侧不过度虚化。
- `avatarOverlay` 为 `show`，确保宠物不会随主题切换隐藏。
- 首页、聊天、设置、插件和技能页面共用同一主背景，并由管理器主题变量适配文字与面板。

需要手工打包、诊断导入错误或检查全部字段时，读取 [references/theme-format.md](references/theme-format.md)。
