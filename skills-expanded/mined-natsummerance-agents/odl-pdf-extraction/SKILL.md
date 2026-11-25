---
name: odl-pdf-extraction
description: |
  AI 就绪的 PDF 解析管线（opendataloader-project/opendataloader-pdf）：一条命令把任意 PDF 转成结构保持的 Markdown / 带 bounding box 的 JSON / HTML，XY-Cut++ 保证多栏阅读序；本地确定性模式免 GPU，hybrid 模式（现役后端 docling-fast；Hancom 集成为规划中）攻克无边框复杂表格、扫描件 OCR、LaTeX 公式与图表描述，基准综合准确率 0.907 排名第一；还能把未标记 PDF 自动打标为屏幕阅读器可用的 Tagged PDF。
  当用户要「PDF 转 markdown 喂 RAG」「提取 PDF 表格保持行列结构」「要页码/坐标级引用溯源」「扫描件/双栏论文解析」「PDF 无障碍 tagged 化」时使用。
  不适用于：网页内容抓取（转 crawl4ai-scraping）；需先突破反爬才能下载文件的场景（转 scrapling-stealth）。
source_project: opendataloader-project/opendataloader-pdf
tags: [odl-pdf-extraction, pdf-parsing, rag-pipeline, bounding-box, ocr, accessibility, 蒸馏技能]
---

# Odl Pdf Extraction · PDF → 结构化数据管线

## R (Reading) — 上游原文

> "🔍 **PDF parser for AI data extraction** — Extract Markdown, JSON (with bounding boxes), and HTML from any PDF. #1 in benchmarks (0.907 overall). Deterministic local mode + AI hybrid mode for complex pages."
>
> "It outputs structured JSON with bounding boxes, handles multi-column layouts with XY-Cut++, and runs locally without GPU. In hybrid mode, it ranks #1 overall (0.907)… parse with `format="markdown"` for text chunks, or `format="json"` when you need element-level control."
>
> — opendataloader-project/opendataloader-pdf README
> 来源: https://github.com/opendataloader-project/opendataloader-pdf （HEAD raw fetch 失败，经 GitHub README / PyPI / opendataloader.org 三源交叉核验）

快速上手签名：`opendataloader_pdf.convert(input_path=["file1.pdf","folder/"], output_dir="output/", format="json,html,pdf,markdown")`；CLI 为 `opendataloader-pdf file1.pdf folder/ -o output/ -f json,markdown`。

## I (Interpretation) — 方法论骨架

1. **一行转换管线**：`pip install opendataloader-pdf`（Java 11+ / Python 3.10+，本质是 Java CLI 的 wrapper）→ `convert(input_path=[文件或文件夹], output_dir, format=...)`。**每次 convert 都 spawn 一个 JVM 进程**，所以必须把多个文件/整目录合并进一次调用，切忌循环逐个转。
2. **四种输出各司其职**：Markdown = 干净文本喂 LLM 上下文与 RAG 分块；JSON = 每元素带 `type`、heading level、`page number` 和 bounding box `[left,bottom,right,top]`（PDF points）支撑语义级控制；HTML = 带样式展示；Annotated PDF = 检测结构的可视化调试。
3. **版面还原三板斧**：XY-Cut++ 解决多栏阅读序错乱；标题层级/嵌套列表/表格结构显式重建；PDF 本身带结构标签时 `use_struct_tree=True` **优先直读作者意图的结构树**（此时忽略 hybrid 后端）——「不猜，读原文档」。
4. **双模式路由**：标准数字原生 PDF 走确定性本地 fast 模式（免 GPU、结果可复现）；无边框复杂表、扫描件、LaTeX 公式、图表理解才升级 hybrid 模式——`pip install "opendataloader-pdf[hybrid]"` 后先起 `opendataloader-pdf-hybrid --port 5002` 服务端，客户端 `--hybrid docling-fast`（Hancom 后端为规划中的企业集成，README 标注 Coming Soon，暂不可用）。
5. **干净输入保障**：header/footer/watermark 自动过滤防污染语料；内置 prompt injection 过滤防恶意文档劫持下游 LLM。
6. **无障碍副产线**：`--format tagged-pdf` 把未标记 PDF 自动打标为 Well-Tagged PDF（PDF Association 规范，veraPDF 程序化校验，Apache 2.0 免费核心），替代 $50–200/份的人工修复流程。
7. **生态对接**：LangChain 官方集成 `langchain-opendataloader-pdf` 的 `OpenDataLoaderPDFLoader`；RAG 最佳实践是 markdown 按标题分块或 JSON 按元素切分，答案回填 bounding box 实现 click-to-source 高亮。

## A1 (Past Application) — 源项目典型应用

### 案例: 论文库批量入 RAG
- **输入**: 装满学术 PDF 的文件夹（多栏排版）
- **做法**: `convert(input_path=["papers_folder/"], format="markdown")` 一次批量，XY-Cut++ 保持阅读序，按标题层级切块
- **结果**: 语义完整的 chunk 序列，可直接接 RecursiveCharacterTextSplitter 或标题切分器

### 案例: 合同/报告引用溯源（click-to-source）
- **输入**: 需要答案定位回原文的长文档
- **做法**: `format="json"` 取每元素的 bbox 与 page number；检索命中后把坐标映射回原 PDF 高亮
- **结果**: 用户可见「答案出自第 N 页该段落」的可信引用 UX

### 案例: 扫描件 + 无边框复杂表格
- **输入**: 图片型扫描页与 borderless 财务表
- **做法**: 起 hybrid server 后 `--hybrid docling-fast`，OCR 与 AI 表格识别接力
- **结果**: 表格行列结构与文字内容完整还原，基准综合 0.907 的精度背书

## A2 (Future Trigger) ★ 触发场景

### 用户会在什么情境下需要
1. **给 RAG/知识库备料**：手头是一堆 PDF（论文/手册/年报/合同），要转成结构保真的 Markdown 或 JSON 入库
2. **要元素级坐标**：下游需要页码 + bounding box 做「点击溯源/答案高亮」或精确版面分析
3. **硬版面攻坚**：双栏论文顺序错乱、无边框表格、扫描件只有图、公式要 LaTeX——fast 模式不够需 hybrid
4. **无障碍合规**：存量未标记 PDF 要批量变 Tagged PDF（EAA/ADA/Section 508 场景）

### 语言信号
- "把这批 PDF 转成 markdown/json，我要灌进知识库"
- "提取 PDF 里的表格，行列结构别乱"
- "要能定位到原文页码/坐标，前端做引用高亮"
- "这是扫描件/双栏论文，普通解析出来顺序是花的"
- "PDF 要过无障碍检测，得是 tagged 的"

### 与同 agent 兄弟 skill 的区分
- 与 `crawl4ai-scraping` 的区别：数据源是**文件**还是**网页**——凡是 URL 里活着的内容归 crawl4ai；凡是 `.pdf` 文件本体（无论来自邮件、下载还是网页附件）归本 skill。
- 与 `scrapling-stealth` 的区别：本 skill 不管「怎么拿到文件」——若 PDF 挂在有反爬盾的站点后面，先用 scrapling-stealth 下载，随后仍回到本 skill 解析。
- 域外提示：对单张图片做纯 OCR（无 PDF 版面结构诉求）不属于本 skill 主场。

## E (Execution) — 可执行步骤

1. **环境就绪** — 确认 Java 11+ 与 Python 3.10+，`pip install -U opendataloader-pdf`；完成标准: `opendataloader-pdf --help` 正常输出参数表
2. **最小转换冒烟** — 取一个代表性样本 `convert(format="markdown")`；完成标准: 输出文件生成，人工抽查标题层级与段落顺序正确（多栏文档重点查）
3. **模式路由判定** — 数字原生 PDF 走默认 fast；含无边框表/扫描页/公式 → 起 `opendataloader-pdf-hybrid --port 5002` 并加 `--hybrid docling-fast`；带结构标签的 → `use_struct_tree=True`；完成标准: 所选模式下表格/OCR/阅读序抽样正确
4. **锁定输出格式** — RAG 语料选 markdown（或 json 元素级）；溯源需求选 json（校验 bbox/page_number 字段）；调试开 annotated pdf；完成标准: 输出含下游必需的全部元数据字段
5. **批量生产** — `input_path` 直接传文件夹一次调用（牢记 JVM spawn 开销）；完成标准: 目录内全部文件有对应产物 + 失败文件清单（加密/损坏者单独报告原因并给替代建议）
6. **下游对接** — LangChain loader 或按标题/页码切分器接入检索管线，json 路线实现 bbox 回填高亮；完成标准: chunk 带元数据可检索，溯源链路演示通过
7. **合规自检收尾** — 确认文档来源合法、版权与个人信息处理依据；完成标准: 结论写入交付说明

## B (Boundary) — 边界

### 不适用场景
- 网页/在线内容抓取 → `crawl4ai-scraping`
- 需要先突破反爬才能下载目标文件的场景 → `scrapling-stealth`（下载完成后回到本 skill）
- 纯单图 OCR、Excel/Word 等非 PDF 格式的结构化处理——选更贴合的工具

### 已知局限 / 失败模式
- 依赖 JVM 且每次 convert spawn 进程：高频小批量调用极慢，必须攒批
- hybrid 模式需额外常驻服务且依赖外部 AI 后端；PDF/UA-1/UA-2 导出与可视化编辑器是企业版功能，免费核心止步于 Tagged PDF 生成
- 加密或损坏的 PDF 无法直接处理——报告原因并建议替代方案（如请用户提供可读副本）

### 合规红线
- 仅处理**有权处理**的文档（自有/获授权/公有领域）；**不破解 PDF 密码/DRM、不绕过付费墙获取文档**——「这份付费报告帮我破了密码再提取」→ 应拒绝
- 不为规避订阅/登录限制而批量下载受版权保护资料；提取内容的再分发遵守原文档版权与许可
- 文档中涉及**个人信息**的（简历/合同/病历类）须有合法处理依据并最小化留存

## 相关 skills

- composes-with: crawl4ai-scraping（网页中发现 PDF → 下载后交本 skill 解析）、scrapling-stealth（反爬站点上的 PDF 先由其下载）
- contrasts-with: 上述两者（文件解析 vs 网页抓取的分工见 A2 区分段）

---

## 审计信息

- **验证**: V1 ✓（GitHub README / PyPI 项目页 / opendataloader.org quick-start-python 三源互相印证 CLI 参数、模式路由与输出格式）/ V2 ✓（可回答「何时升 hybrid」「bbox 怎么用于溯源」等 README 之外的新问题）/ V3 ✓（JVM 批量约束 + 结构树优先 + 双模式路由的决策链是非常识性工作流）
- **测试通过率**: 100%（详见 test-prompts.json / test-results.md）
- **蒸馏时间**: 2026-08-25
- **来源 URL 清单**:
  - https://raw.githubusercontent.com/opendataloader-project/opendataloader-pdf/HEAD/README.md （fetch 失败：transport error）
  - https://github.com/opendataloader-project/opendataloader-pdf （经搜索镜像核验）
  - https://pypi.org/project/opendataloader-pdf/ （经搜索镜像核验）
  - https://www.opendataloader.org/docs/quick-start-python （经搜索镜像核验）
