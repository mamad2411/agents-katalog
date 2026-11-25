---
name: x-article-auto-publisher
description: End-to-end X Articles publishing workflow from markdown with remote images. Downloads images locally, converts with pandoc, pastes HTML body into X editor, replaces camera placeholders with local images in order, then saves draft or publishes.
allowed-tools: Bash(python:*), Bash(pandoc:*), Bash(playwright-cli:*), Bash(powershell:*)
---

# X Article Auto Publisher

## 适用场景
- 你给我一个本地 Markdown 文件。
- 文件里图片是远程 CDN 链接。
- 目标是自动发布到 X Articles（可选仅保存草稿）。

## 路径约定（.codex / .claude）
- 不同代理环境里，skill 根目录可能是 `.codex/skills/...` 或 `.claude/skills/...`。
- 本 skill 文档与命令统一使用“skill 目录内相对路径”（如 `.\scripts\...`），避免绑定某个宿主目录名。
- 如果你在仓库根目录执行命令，需要先 `cd` 到当前 skill 目录再运行。

## 固定流程
1. 运行 `scripts/cdn_to_local_img.py`：
   - 生成 `<stem>_local.md`
   - 生成 `<stem>_local_assets/001.* ...`
2. 用 pandoc 生成：
   - `<stem>_local.html`
   - `<stem>_local_base64.html`
3. 提取 `<stem>_local.body.html`：
   - 如果 html 有 `<body>`，提取 body inner HTML
   - 如果没有（片段 html），直接复制全文件
4. 打开 `https://x.com/compose/articles`，进入编辑器。
5. 用 `scripts/copy_to_clipboard.py html -f <body-fragment>` 设置 HTML 剪贴板。
6. 编辑器中 `Ctrl+A` -> `Backspace` -> `Ctrl+V` 粘贴正文。
   - 直接跑 `scripts/paste_from_clipboard_into_x_editor.js`
7. 用 `scripts/check_x_counts.js` 校验：
   - `emojiCount`（`1f4f7.svg` 占位）应大于 0（若文章有图）
   - `bodyImgs` 初始应为 0
8. 按 `assets` 文件名排序，从 `001` 开始逐个替换：
   - `scripts/copy_to_clipboard.py image <image-path>`
   - `scripts/replace_one_x_placeholder.js`
   - 成功条件：`emojiCount -1` 且 `bodyImgs +1`
9. 全部替换后：
   - 默认：保存为草稿（不发布）
   - 用户明确要求发布：点击 Publish 完成发布

## 强约束
- 不手工重写 markdown 内容。
- 不将整份 standalone html（含 head/style）直接贴入编辑器。
- 必须使用 HTML 剪贴板，不能用纯文本剪贴板替代。
- 占位替换失败时立即停止，不继续错位替换。

## 推荐命令模板
在 `x-article-auto-publisher` 目录内执行：
```powershell
python ".\scripts\cdn_to_local_img.py" "<input.md>"
pandoc -f markdown -t html5 -s -o "<stem>_local.html" "<stem>_local.md"
pandoc -f markdown -t html5 --embed-resources --standalone -o "<stem>_local_base64.html" "<stem>_local.md"
python ".\scripts\copy_to_clipboard.py" html -f "<stem>_local.body.html"
playwright-cli open "https://x.com/compose/articles" --headed --persistent
playwright-cli run-code --filename=".\scripts\paste_from_clipboard_into_x_editor.js"
playwright-cli --raw run-code --filename=".\scripts\check_x_counts.js"
```

## 易踩坑与处理
- 文章入口页不是编辑器：
  - `https://x.com/compose/articles` 可能先到 Drafts 列表，需要点击 `create` 才进入 `/compose/articles/edit/...`。
  - 只有编辑页里 `check_x_counts.js` 才会返回 `hasEditor=true`。
- Playwright 会话不一致：
  - `open` 和后续 `run-code / click / snapshot` 必须在同一会话上下文执行。
  - 如果出现 `Browser 'default' is not open`，通常是会话或权限上下文不一致，需在同一上下文重开并继续。
- 占位替换顺序：
  - 每次调用 `replace_one_x_placeholder.js` 前，必须先执行一次 `copy_to_clipboard.py image <image-path>`。
  - 若先替换后设图，会导致占位统计异常。
