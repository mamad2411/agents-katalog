---
name: lanshu-html-ppt-templates
description: 基于 30 套岚叔 HTML 演示模板创建、改写和定制演示文稿，支持商务汇报、政企汇报、路演、发布会、学术答辩、教学课件、数据叙事与交互演示。用户需要 HTML 幻灯片、网页 PPT 或使用这些模板制作演示时使用。
metadata:
  author: Lanshu
  version: "1.3.0"
---

# 岚叔 HTML 演示模板

使用 `assets/templates/` 的完整单文件模板制作可直接放映的 HTML 演示。在线目录：<https://ppt.lanshuagent.com/>；作者：<https://x.com/LufzzLiz>。

## 选择模板

先读 [references/template-catalog.md](references/template-catalog.md)，按内容、受众和交付格式选型。用户已指定风格时沿用；未指定时根据材料选择，并简短说明。无需为常规样式选择额外确认。

- 商务汇报、战略和信息密集内容：`07-consulting`、`01-swiss`。
- 融资路演、产品和技术发布：`04-brutalism`、`03-aurora`、`17-terminal`。
- 品牌、文化、策展和生活方式：`02-editorial`、`08-oriental`、`09-organic`、`18-riso`、`19-collage`。
- 数据分布和连续叙事：`11-morph`；可调业务假设：`14-live-model`；地域和全球网络：`20-globe`。
- 学术答辩和课题汇报：`21-academic`；教学课件和培训：`23-chalkboard`。
- 产品功能介绍和年度总结：`22-bento`；AI 产品与客户故事：`24-chat`；年会和团队复盘：`25-pixel`。
- 政企、国企和机关的工作汇报：`28-official`；年度大事记、企业内刊：`26-newspaper`。
- 工程评审与硬件方案：`27-blueprint`；产品路线图和战略规划：`29-metro`；用户故事和品牌故事：`30-comic`。
- 用户需要多页 PDF 时，优先选择目录中标注有多页打印样式的模板；打印效果仍需实际检查。

## 创建与修改

命令中的路径相对于本 skill 目录；先定位 skill 的实际安装位置。

```bash
python3 scripts/deck.py list
python3 scripts/deck.py new 07-consulting --output /path/to/outputs/presentation.html --title "演示标题"
python3 scripts/deck.py source 07-consulting
python3 scripts/deck.py inspect /path/to/outputs/presentation.html
```

`new` 复制完整模板，保留字体和脚本，拒绝覆盖已有文件。`--title` 只修改浏览器标题，页面正文需要继续改写。`source` 仅在终端隐藏字体 Base64，保留原始行号；不要把它的输出保存成演示文件。

执行前阅读 [references/authoring.md](references/authoring.md)。对选中的 HTML 做定点修改：

1. 根据用户材料建立逐页叙事，再替换标题、正文、图表数据、页眉页脚与品牌。优先复用现有版式，按内容增删页。
2. 保留播放内核依赖的 ID、class、`data-*`、事件绑定与图表接口，以及 TOOLKIT（放映工具包）和 PRESENTER（演讲者窗口）代码块；改变页面数量时同步页码、生成数组和备注数量。
3. 更新 `script#deck-notes` 中的 JSON 数组，让备注顺序与实际放映顺序一致。模板样例中的公司、数字、来源文字和联系方式需要替换或删除。
4. 输出独立 HTML。静态图形优先使用 SVG/CSS，实时图形沿用现有 Canvas；新增资源需内嵌或随演示一同交付。

模板的中文字体按原文字符裁剪，新增文字会先用系统字体回退。改完文字后，联网运行 `python3 scripts/embed_fonts.py <演示文件>`，按页面实际用到的字重新裁剪内嵌字体；离线时优先沿用现有字体栈，并检查版面。保留原有字体许可说明。

## 交互与导出边界

- 普通模板使用 `.slide`；无限画布、电影、空间界面、终端、拼贴各有独立数据结构，具体见作者指南。
- `14-live-model` 的模型参数、现金流和绑定元素需要一起修改；演讲者预览是独立实例，默认不会同步主屏临时调整的模型参数。
- 30 套都内置放映工具包：`?` 快捷键面板、`O` 总览、页码加 `Enter` 跳页、`B`/`W` 黑白屏、`L` 激光笔、`D` 画笔批注，`E` 在浏览器里改字、改讲稿、全套替换和调主题色并另存为新文件。用 `python3 scripts/present.py <演示文件>` 打开后按 `M`，可用同一 Wi‑Fi 下的手机扫码遥控。
- `17-terminal` 是终端外观的网页演示，显示的命令属于页面内容。
- `12-generative` 每次运行可能得到不同画面；需要可复现结果时固定种子。
- 当前提供 HTML 与部分模板的浏览器打印 PDF；交互和动画由浏览器播放。需要可编辑 `.pptx` 时明确说明格式差异，再按用户选择另行转换。
- 公网部署仅在用户要求时执行。修改配置中的域名不会自动取得新域名或发布权限。

## 校验和交付

```bash
python3 scripts/deck.py validate /path/to/outputs/presentation.html
```

该命令检查备注 JSON 和内联 JavaScript 语法；需要本机 Node.js 才能完成 JavaScript 检查。它不执行页面脚本。

在可用的浏览器里检查首尾页、关键图表、最长正文、翻页、全屏、演讲者备注和交互；有 PDF 要求时检查实际打印结果。无法运行浏览器时说明已做的静态检查和未验证部分。

交付 HTML 的可用路径、页数和必要的播放说明；可提示按 `?` 查看全部快捷键，需要手机遥控时用 `scripts/present.py` 打开。用户要求 PDF 时一并交付验证过的 PDF；说明交互状态和动画在导出中的实际表现。
