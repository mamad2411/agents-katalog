---
name: coff0xc-office-doc-tools
description: "Use when / 当用户请求正式 Office 或文件型交付物：PPT PPTX PowerPoint slides deck、DOCX Word redline comments、PDF read create review render、Excel XLSX CSV workbook chart formula table export。要求可编辑文件、渲染/OOXML/公式/格式检查。手动触发：使用 coff0xc-office-doc-tools。"
---

# coff0xc-office-doc-tools

<!-- skill-id: cs-odt-9c3a15f7 -->

## 快速规则（日常任务先读这里）
> **[文件优先]** 先确认输入/输出文件类型、可编辑性、原件保留、目标受众和交付路径。
> **[结构门禁]** PPT 看叙事和视觉系统；Excel 看数据形状/公式/图表；DOCX/PDF 看样式、批注、分页和渲染证据。
> **[验证证据]** 能打开结构就打开结构，能渲染/截图就渲染/截图；不能验证要明说。
> **[PPT 重写]** 论文/报告 DOCX + 旧 PPTX 重写答辩 deck 时读取 `references/pptx-defense-rewrite.md`，不要卡在 Presentations 路径版本不一致。
> **[硬边界]** 上传外部服务、覆盖原件、接受全部修订、客户/隐私/合同/财务数据处理先确认。

普通 Office 文件任务按本节先推进；只有 artifact quality eval、正式发版或跨文件复杂交付时再展开全部门禁。

## 能力定位
面向 PowerPoint、Word、PDF、Excel/CSV 这类正式文件交付的 Office 文档工具能力。它解决的不是“写一段内容”，而是把内容做成别人能打开、能编辑、能审阅、能打印、能继续使用的文件。

这个 skill 适合用户说“帮我做一份 PPT / 改一个 DOCX / 检查 PDF / 处理 Excel / 生成可交付文件”的场景。它会把产物质量放在第一位：文件要存在、内容要对、格式要稳、公式要算、版式要看过，不能只凭文本猜测就说完成。

## 能交付什么
- 可编辑 `.pptx` 演示文稿：页面结构、图表、表格、图片、讲述逻辑、导出检查和预览 QA。
- 可编辑 `.docx` 文档：报告、方案、SOP、合同草稿、批注、修订、表格、目录、页眉页脚、元数据清理建议。
- `.pdf` 阅读、审阅、生成或检查：页面渲染、文字提取、版式问题、页码、表格、图片和引用检查。
- `.xlsx` / `.csv` / `.tsv` 工作簿：数据清洗、公式、透视/汇总、图表、仪表盘、条件格式、校验列和导出文件。
- 交付说明：最终文件路径、验证方式、未验证原因、剩余风险和建议的人工复核点。

## 可以接收什么输入
- 现有 PPTX、DOCX、PDF、XLSX、CSV、TSV、Markdown、图片、截图、网页导出的表格。
- 用户给的文字大纲、会议纪要、报告草稿、审计发现、实验数据、财务/运营数据、品牌要求或模板文件。
- 批注要求、改写要求、格式要求、目标受众、页数限制、打印/展示/归档用途。
- 多个来源文件，例如“把 PDF 数据整理到 Excel，再做一页 PPT 摘要”。

## 放心使用的边界
- 可直接处理本地、可逆、可检查的文件创建、编辑、转换、分析和格式整理。
- 不上传用户文档到外部服务，不调用付费生成/转换服务，不发布或发送文件，除非用户明确确认。
- 含个人信息、客户数据、合同、财务、医疗、身份信息或内部资料时，先确认脱敏、保留范围和输出目录。
- 不伪造来源、签名、印章、审计结论、法律意见、财务真实性或官方认证。
- 修改现有文件时默认保留原件，输出新文件；批量覆盖、删除、接受所有修订、清空批注或移除水印前必须确认。
- 默认只处理本地、可逆、可验证的低风险工作；涉及生产、凭据、付费、远程写入、删除、发布或权限变更时必须先确认。

## 为什么可以放心
- 文件型交付必须有“文件存在 + 内容检查 + 视觉/结构验证”的证据链。
- PPT/DOCX/PDF 不能只靠文本抽取判断质量；版式任务要渲染或预览检查。
- Excel/XLSX 不能只看表面格式；关键公式、引用范围、错误值和图表来源要检查。
- 现有文件编辑采用最小改动原则，保留结构、样式和原始文件，避免不可追踪覆盖。
- 最终回复区分“已验证”“未能验证”和“需要人工复核”，不把未运行的检查说成通过。

## 典型使用方式
```text
使用 coff0xc-office-doc-tools 把这份 Markdown 做成可编辑 PPTX，包含图表、讲述逻辑和预览验证。
使用 coff0xc-office-doc-tools 给这个 DOCX 加批注和修订，不覆盖原件，最后渲染检查版式。
Use coff0xc-office-doc-tools to turn this CSV into a formatted Excel workbook with formulas, charts, and a formula error scan.
Use coff0xc-office-doc-tools to review this PDF report for layout, missing pages, broken tables, and export-ready issues.
```

## Runtime / Tool Fallback
Office 任务优先使用当前会话已加载的插件或 MCP 工具，而不是硬编码版本路径。

- PPT/PPTX：优先 `presentations:Presentations`；如果路径/版本不一致，改用 workspace dependency loader、Office 工具或本地 OOXML/Python/JS 生成路径，不要反复猜插件目录。
- DOCX：优先 `documents:documents` 或 Office 文档工具；渲染不可用时做结构检查并明确未完成视觉 QA。
- Excel/XLSX/CSV：优先 `spreadsheets:Spreadsheets` 或 Office 表格工具；完整 Excel 引擎不可用时只声明支持范围内的公式/结构检查。
- PDF：优先 PDF 渲染/页面检查；只抽文本不能证明版式通过。

如果目标是正式答辩 PPT、论文答辩、项目答辩、毕业设计或“根据 DOCX 和旧 PPTX 重写 PPT”，读取 `references/pptx-defense-rewrite.md`。

## 默认输出
- 收口只写完成、验证、还剩、下一步；有文件/代码/规则产物给路径或位置。
- 未真实运行的检查标为未验证，安全/架构结论标证据等级。

## 按需展开
- 日常任务只执行上面的快速规则、能力边界和典型用法，不默认读取完整门禁。
- 深度架构、复杂多阶段、质量评测、发版、正式交付或当前任务证据不足时，再读取 `references/full-workflow.md`。
- 读取 reference 后仍保持最小必要上下文；不要因为 reference 存在就输出长篇流程或额外自证材料。
