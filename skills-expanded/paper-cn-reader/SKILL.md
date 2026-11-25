---
name: paper-cn-reader
description: 学术论文精读翻译与批注，生成 HTML+PDF 中文精读文档。读取英文论文 PDF，逐段忠实翻译为中文，保留原文图片/表格/公式/章节结构，在关键位置添加 8 类 AI 辅助批注（概念解释/关键结论/方法理解/公式解读/图表解读/实验分析/阅读提醒/批判性思考），最终输出带打印样式的 HTML 和 PDF。触发场景：论文精读、论文翻译、论文批注、读论文生成中文版、精读论文并批注、把英文论文转成中文 HTML、论文深度阅读、paper deep reading、annotated paper translation。当用户提供论文 PDF 并要求逐段翻译、添加批注、生成精读文档时使用此 skill。区别于 paper-quick-reader（速读抓核心），此 skill 强调忠实完整翻译+辅助理解批注。
---

# Paper CN Reader — 学术论文精读翻译与批注

将英文论文 PDF 转换为带 AI 批注的中文精读 HTML + PDF 文档。核心：**忠实逐句翻译**（非概括）+ **保留原文图表公式** + **辅助理解批注**。

## 核心原则

1. **忠实完整**：逐段逐句翻译，不压缩为摘要，不省略限定条件和实验细节
2. **三视觉分离**：中文译文 / 原文内容 / AI 批注必须在视觉上明确区分
3. **不编造**：无法识别标记 `【原文此处识别不清】`，AI 分析只在批注区

## 工作流程

### 第 1 步：解析论文

读取 PDF，识别：
- 总页数、章节结构、单栏/双栏排版
- 图片数量、表格数量、公式数量
- 附录和参考文献位置

**双栏 PDF 注意**：必须正确识别阅读顺序（先左栏后右栏），避免错误拼接。

### 第 2 步：提取资源

使用 bundled 脚本提取图片到 `assets/` 目录：

```bash
python scripts/extract_pdf_assets.py <论文.pdf> assets --min-width 100 --min-height 100
```

- 图片按 `figure_1.png`, `figure_2.png` ... 命名
- 同页多图追加 a/b/c 后缀
- 矢量图无法提取时，用脚本内 `screenshot_region()` 按区域截图（3 倍缩放）
- **不得因提取困难省略图片**，失败必须在对应位置说明

依赖：`pip install pymupdf`

### 第 3 步：翻译正文

按论文顺序逐段翻译，保存页码映射。**详细规则见 [references/translation_rules.md](references/translation_rules.md)**，要点：

- 逐段逐句翻译，术语首次出现用 `中文术语（English Term）`
- 模型名/数据集名/变量名/缩写保留英文
- 默认只呈现中文译文，不重复完整英文正文
- 长难句可调语序但不改原意

### 第 4 步：添加批注

仅在真正需要辅助理解处添加。**8 种批注类型及示例见 [references/annotation_guide.md](references/annotation_guide.md)**。

密度：平均每 1-2 页 1-3 个有价值批注。重点位置：摘要贡献、引言动机、框架图、核心结构、重要公式、损失函数、关键表格、消融实验、局限性。

**禁止无效批注**：「很重要」「结果很好」、正文简单重复、泛泛评价。

### 第 5 步：生成 HTML

基于 [assets/template.html](assets/template.html) 骨架和 [assets/styles.css](assets/styles.css) 样式生成。模板已包含：

- 语义化结构（`<article>` / `<section>` / `<aside class="annotation">`）
- MathJax CDN（行内 `$...$`，独立 `$$...$$`）
- 8 类批注 CSS（不同低饱和边框色）
- 目录导航 + 页码定位（`data-source-page` / `[P5-C2]`）
- 打印 CSS（`@page` A4 + `@media print`）

生成时：
1. 复制 `template.html` 和 `styles.css` 到输出目录
2. 替换占位符为实际翻译内容
3. 图片用相对路径 `assets/figure_N.png`
4. 表格重建为 HTML `<table>`（保留数值、加粗、最优值标记）
5. 公式用 LaTeX，保留 `\tag{N}` 编号

### 第 6 步：生成 PDF

使用 bundled 脚本将最终 HTML 转为 PDF：

```bash
python scripts/html_to_pdf.py 论文精读中文版.html 论文精读中文版.pdf
```

脚本会等待图片、字体、MathJax 渲染完成后再导出。A4 页面，边距 18mm/16mm。

依赖：`pip install playwright && playwright install chromium`

**替代方案**（若 Playwright 不可用）：Puppeteer / Chromium Headless / WeasyPrint。

### 第 7 步：质量检查

逐项检查 **[references/quality_checklist.md](references/quality_checklist.md)**，涵盖：内容完整性、翻译质量、图片表格、公式、批注、排版、PDF 输出。

## 交付物

```
输出目录/
├── 论文精读中文版.html   # 主文档（可独立打开）
├── 论文精读中文版.pdf    # 由 HTML 渲染生成
├── styles.css           # 样式表
└── assets/
    ├── figure_1.png
    ├── figure_2.png
    └── ...
```

完成后简要报告：论文总页数、已翻译章节、提取图片数、重建表格数、批注数、无法识别内容、各文件路径。

## 关键约束

- **不得编造**论文内容、实验结果、表格数值
- **不得省略**图片/表格/公式——提取失败必须说明
- **AI 分析只在批注区**，译文区只呈现忠实翻译
- **批判性批注**必须注明"分析或推测"，不可伪装成论文结论
- **HTML 可独立打开**：CSS 和图片用相对路径，文件夹移动后仍可显示
