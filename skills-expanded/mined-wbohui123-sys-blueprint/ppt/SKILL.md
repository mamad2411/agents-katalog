---
name: ppt
description: 制作可编辑 PPTX、网页放映与 JSON 演示工程，并继续修改已有工程。
disable-model-invocation: true
---

# 演示文稿

把当前材料组织成适合听众的演示，交付可编辑 PPTX、独立 HTML 放映和可继续修改的 JSON 工程。构建器取自 dsh-ppt 0.9.0，图片与原生图表依赖已随技能提供；使用 App 的 Node，不需要 Office 或另一个工作台。

先想清听众要理解什么、哪些内容和证据需要成页，再写 Markdown 或结构化页面。缺少的事实保留为草稿，页面数量与结构由材料和用途决定。

```bash
node "<本技能目录>/scripts/制作演示.mjs" --title "项目汇报" --content 汇报材料.md --theme swiss --out 演示 --file 项目汇报
node "<本技能目录>/scripts/制作演示.mjs" --check 演示/项目汇报.json
```

需要表格、图表、图片、备注、主题或继续编辑时，读 [用法](references/用法.md)。图片从当前项目的 PNG/JPEG 取得，图表保留原始数值；构建器不下载外链素材。

HTML 可用 `render_page` 检查放映画面；它不能证明最终 PPTX 的实际排版。最终 PPTX 可用可选的 LibreOffice Kit 0.1.5 渲染，命令见用法，逐页用 `read_image` 看缺字、裁切和内容关系。引擎不可用时仍能交付可编辑文件，说明实际 PPTX 排版尚未验证。交给用户的是三个可点击入口；后续修改使用同一 JSON 工程。
