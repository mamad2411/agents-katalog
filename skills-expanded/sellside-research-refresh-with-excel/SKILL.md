---
name: "sellside-research-refresh-with-excel"
version: "3.0.6"
description: "自包含单体研报复现：内置「研报底稿抽取」与「研报仿写」完整流水线，基于原始研报框架，为新标的/新时间生成新研报、新可刷新 Excel 底稿，及原始研报底稿与评测报告。"
---

# 研报复现（自包含单体）

> 本 skill 是**编译生成的自包含单体**：`bundle/review`（研报底稿抽取）与 `bundle/drafting`（研报仿写）的完整逻辑已 vendor 内置，运行时**不再用 Skill 工具加载任何子 skill**，也不依赖外部子 skill 目录。所有子流程脚本路径均指向 `bundle/review/scripts/*`、`bundle/drafting/scripts/*`。

---

## 0. 运行时门禁（硬约束，AI 必须遵守）

**职责分层**：
- **衔接缝合层**（可改）：宿主自有 `scripts/*`、`reference/*`——框架提取、适配、B 底稿生成、交付编排。
- **子 skill 内部实现层**（只读）：`bundle/review/scripts/*`、`bundle/review/reference/*`、`bundle/drafting/scripts/*`、`bundle/drafting/references/*`。

**门禁**：
- ✅ 允许按本文指示**调用/读取**子 skill 脚本（运行所需）。
- 🚫 **禁止修改** `bundle/review/scripts/*`、`bundle/drafting/scripts/*` 及其 reference 的任何源码。
- 🚫 **禁止写绕过子 skill 内部脚本的平行脚本**（如 build_evidence.py、attach_bbox.py 类）。
- ✅ **首跑自检**：任何任务段开始前必须运行 `scripts/check_bundle.py`；`BLOCKED` 即停止，bundle 缺失/指纹不符走"改上游源 → 重跑 build_bundle.py 编译"路径，**禁止运行时现场重建 bundle**。
- 子流程遇故障 → 写 `BLOCKED` 并停下，不越界自行修复内部脚本；确需修复的，走"改上游源 → 重跑 build_bundle.py 重新编译"路径，不在运行时手改。
- 阶段完成必须经 **handoff 文件 + SHA-256 校验**，禁止仅用任务状态标记冒充完成。
- 🚫 **stage-4 handoff 只能由 `scripts/prepare_drafting_handoff.py finalize` 生成**（携带 generator + engine_receipt）；宿主手写 stage-4 handoff 或绕过引擎手写交付，在交付门禁一律判 `STAGE4_BYPASSED`/`FAIL`，退出码 1。
- 子 skill 确需修复 → 改上游源目录后重跑 `scripts/build_bundle.py` 重新编译产物，不在运行时改 `bundle/`。

---

## 1. 输入 / 输出 / 总流程

**输入**：① 原始研报 PDF；② 新标的（可同标的）；③ 新时间（可同时间）。
**输出（4 份，缺一不可）**：
1. 新研报 MD + HTML（由内置 drafting 生成）
2. 新 B 底稿 xlsx（5-Sheet，`20_研报底稿` 仅 `=mql()` 公式）
3. 原始 A 底稿 xlsx（由内置 review 生成）
4. 原始评测报告 md（由内置 review 生成）

**总流程**：阶段 0（review 生成 A 底稿+评测报告）→ 阶段 1/2/3（宿主框架提取/适配/B 底稿）→ 阶段 4（drafting 生成新研报 MD/HTML）→ 交付。阶段间通过落盘 handoff + SHA-256 交接。

编排契约、检查点续跑、依赖清单见宿主 `reference/`（orchestration_contract.md、checkpoint_resume_protocol.md、dependency_inventory.json）。

---

## 2. 阶段 0：生成原始研报底稿（内置 review 流程）

> 路径前缀：脚本 `bundle/review/scripts/`，规范 `bundle/review/reference/`。本阶段产物为 A 底稿 xlsx + 评测报告 md。

### 2.1 路由与前置
- 用户要求"提取这篇研报底稿/做底稿" → 直接进入"生成研报底稿"，不询问模式。
- 先运行 `bundle/review/scripts/golden_case_manager.py match --pdf <PDF>`（仅本地指纹，不调外部服务）。精确命中且用户接受演示样例可用 `export` 复制 `expected.xlsx`，须声明为已验收样例复现；用户要求重跑/刷新则必须完整执行。
- 完整底稿任务开始时读取并遵守 `bundle/review/reference/execution_stability.md`。流程按 `01_census.json → 02_source_evidence.json → 03_mapping_plan.json → 04_query_results.json → 05_workbook_input.json` 单调推进；已 PASS 对象不重复执行，续跑从磁盘检查点恢复。

### 2.2 不可跳过顺序（摘要，详见 `bundle/review/SKILL.md`）
1. 个股研报先读 `bundle/review/reference/equity_report_standard.md`。
2. 调用 layoutV2 后先跑 `bundle/review/scripts/prepare_workbook_phases.py from-layout` 生成 census/evidence 骨架（兼容 `data.textBlocks`/`layoutAnalysis.blocksByPage`）；视觉审阅后再 `normalize-evidence`。无法识别结构须以 `LAYOUT_SCHEMA_BLOCKED` 停止并保存原始响应，**不得手写 census/evidence JSON**。
3. 按 `bundle/review/reference/pdf_layout_api.md` 调 layoutV2（地址写占位符 `{em_base_url}/proxy/pdf/layoutV2`，凭据仅从 `EM_API_KEY`/`{em_api_key}` 注入），按 `ingestion_rules.md` 建页面清单、全表全图普查。页面渲染图与裁剪图是最终判据。
4. 审计通过后按 `generation_contract.md` 固定视觉对象、表格语义、字段、期间与映射；再按 `indicator_inventory_template.md` 区分历史实际/预测/衍生/主观。
5. 按 `mql_execution_protocol.md` 用 MQL 工具链取数：**任何可结构化数据先 MQL**，缓存未命中/未列举领域必须进 MQL，不得直接降级其他接口。明确服务故障才允许妙想兜底并登记 `SERVICE_FAILURE_CONFIRMED`。
6. 按 `workbook_spec.md` 准备 JSON，逐指标真实执行 MQL；用 `merge_workbook_phases.py` 唯一合并 → `preflight_workbook_input.py` 预检 → 最终只运行 `research_report_pipeline.py input.json --output result.xlsx`。
7. Excel 固定 5-Sheet：`00_导读`/`10_研报快照`/`20_研报底稿`/`30_预测框架`/`90_执行日志`。
8. `20_研报底稿` 只写经真实执行验证的 `=mql()` 公式 + 脚本批注 + 空白溢出区；禁止 PDF 静态值、旧缓存、人工补值。

### 2.3 阶段 0 完成门禁（同时满足才算完成）
- 页面清单覆盖全部页码，纳入+排除表=普查表数；图表普查全覆盖、纳入图表截图与元数据一一对应、视觉校验通过。
- 所有纳入表格逐行逐值回读通过，不得以抽样代替。
- `build_workbook.py --validate-only` 通过，5 个核心 Sheet 齐全；`20_研报底稿` 仅含 `=mql()` 公式与空白溢出区，无 PDF 静态数据表/图片/Excel 图表。
- 每个成功 MQL 块在 `90_执行日志` 有完整记录；`20_研报底稿` 公式与日志、workpapers 一致。
- 产物命名：`*_研报底稿抽取.xlsx` + `*_底稿评测报告.md`。
- 宿主用 `scripts/run_stage0.py --final` 校验产物存在性与 SHA-256；**严禁宿主自行拼装底稿 xlsx**。

---

## 3. 阶段 1/2/3：框架提取、适配、B 底稿生成（宿主自有）

> 路径：宿主 `scripts/`、`reference/`。属衔接缝合层，可改。

- **阶段 1 框架提取**：入口 `scripts/extract_metric_framework.py`，规范 `reference/metric_framework_extraction.md` + `metric_framework.schema.json`。从原始研报抽取指标框架。
- **阶段 2 适配**：入口 `scripts/adapt_target_framework.py`，规范 `reference/entity_period_mapping.md` + `target_adaptation.schema.json`。将框架适配到新标的/新时间。
- **阶段 3 生成 B 底稿**：入口 `scripts/build_target_workbook.py`，规范 `reference/target_workbook_generation.md`。

**硬约束（数据来源）**：B 底稿数据**只能来自 mx MCP 与 MQL MCP，MQL 优先**，不得引入其他数据源。来自 MQL 的数据落 Excel 必须是 `=mql()` 公式（MQL 脚本写入单元格**批注**，不得写入值或公式参数）。
- B 底稿 conform review 的权威 5-Sheet schema：`bundle/review/reference/workbook_spec.md`。
- `=mql()` 单元格契约以 `Local/Plan/MQL与Excel插件集成.md` 为权威：公式在单元格、脚本在批注（明文）、溢出区留白、`orientation` 第二参数控制行列转置、未装加载项显示 `#NAME?`。
- **MQL server_name 动态取当次会话 `mcp_file_system` 里真实注册名（形如 `mcp_*mql*`），禁止硬编码 `mcp-mql-tools`**。

---

## 4. 阶段 4：仿写新研报（内置 drafting 流程）

> 路径前缀：脚本 `bundle/drafting/scripts/`，规范 `bundle/drafting/references/`。输入：参考研报 PDF + B 底稿 xlsx。产出：新研报 MD + HTML。
> 本阶段为**自动衔接**：阶段 3 handoff 一经 `CONFIRMED`，立即启动，不得询问用户或停等。

**强制独立续跑（硬规则，见 `reference/checkpoint_resume_protocol.md`）**：阶段 4 必须在**新上下文/新任务段**执行，注入内容仅限 stage-3 handoff、参考 PDF、B 底稿路径与本节指针。禁止在承载阶段 0–3 的长上下文尾部以"预算将尽/上下文过长"为由降级为宿主手写 MD/HTML——此类偏差被交付门禁判 `STAGE4_BYPASSED`/`FAIL`，无任何合法手写路径。无浏览器只影响最后一步渲染审计（`--finalize-unrendered`），不构成绕过理由。

`SKILL_DIR` = `bundle/drafting`，`RUN` = 独立任务目录。复用宿主 Python、Node、pdfplumber、pdftoppm 与浏览器，不下载字体/浏览器、不装插件、不执行宏、不改原工作簿。

### 4.1 批量索引与参考确认
```bash
python "$SKILL_DIR/scripts/environment_probe.py"
python "$SKILL_DIR/scripts/workbook_probe.py" scan "底稿.xlsx" --output "$RUN/work/excel-index.json"
python "$SKILL_DIR/scripts/local_pdf_ingest.py" --pdf "参考.pdf" --out-dir "$RUN/work/local" --dpi 150
```
先读 reference-hints.json 确认主标题/对象/期别，写 reference-outline.json：
```bash
python "$SKILL_DIR/scripts/prepare_reference.py" --outline "$RUN/work/reference-outline.json" --index "$RUN/work/local/local-reference-index.json" --output "$RUN/work/reference-contract.json"
python "$SKILL_DIR/scripts/reference_profile.py" --pdf "参考.pdf" --contract "$RUN/work/reference-contract.json" --output "$RUN/work/reference-profile.json" --cache-dir "$RUN/../样式缓存" --apply
python "$SKILL_DIR/scripts/freeze_reference.py" --contract "$RUN/work/reference-contract.json" --baseline "$RUN/work/reference-baseline.json" --pdf "参考.pdf"
```
详见 `bundle/drafting/references/`（generation.md、excel.md、pdf.md、style-profile.md）。

### 4.2 一次事实映射与正文生成
```bash
python "$SKILL_DIR/scripts/build_draft.py" --init --contract "$RUN/work/reference-contract.json" --work "$RUN/work" --basename "对象-研究主标题" --workbook "底稿.xlsx"
```
填 plan 定位/表矩阵/派生公式、填 prose；`plan.scope_review` 设 PASS 后：
```bash
python "$SKILL_DIR/scripts/build_draft.py" "$RUN/work/workflow.json"
```
缺项才走补充素材与引用（`bundle/drafting/references/supplement-citations.md`、`mql-recovery.md`）。

### 4.3 编译与集中验收
```bash
node "$SKILL_DIR/scripts/report_workflow.mjs" "$RUN/work/workflow.json"
node "$SKILL_DIR/scripts/layout_audit.mjs" "$RUN/交付/对象-研究主标题.html" "$RUN/work/layout-audit.json" --workflow "$RUN/work/workflow.json"
node "$SKILL_DIR/scripts/report_workflow.mjs" "$RUN/work/workflow.json" --finalize "$RUN/work/layout-audit.json.receipt.json"
```
无可用浏览器时降级：
```bash
node "$SKILL_DIR/scripts/report_workflow.mjs" "$RUN/work/workflow.json" --finalize-unrendered "当前平台没有可用浏览器工具"
```
状态 `COMPLETE_WITH_UNVERIFIED_LAYOUT`，不伪造视觉 PASS。

### 4.4 阶段 4 完成门禁
- 产出同名 `对象-研究主标题.md` 与 `.html`（由内部稿编译，非宿主手写）。
- MD 无内部标记；HTML 单文件离线可用、与 MD 共用正文及 ECharts 配置。
- finalize 核对产物、浏览器检查与证据指纹；仅提交结论不复算。
- 必须经 `scripts/prepare_drafting_handoff.py finalize` 生成 stage-4 handoff：handoff 携带 `generator` 与 `engine_receipt`，HTML 内 `meta source-md-sha256` 指纹与 MD 哈希一致（缺失/不一致 finalize 直接拒绝）。

---

## 5. 端到端交付门禁

最终必须 4 份齐全：新研报 MD/HTML、新 B 底稿 xlsx、原始 A 底稿 xlsx、原始评测报告 md。入口 `scripts/assemble_delivery.py`，规范 `reference/end_to_end_delivery.md`。受控夹具不得冒充真实端到端执行。

交付门禁除自洽校验外，还执行 **stage-4 来源校验**（generator 绑定、engine_receipt、工作流状态三态 `COMPLETE`/`COMPLETE_WITH_OMISSIONS`/`COMPLETE_WITH_UNVERIFIED_LAYOUT`、MD/HTML 哈希与 meta 指纹、首行"非原机构正式报告"声明与残留标记文本断言）。任一失败 → `delivery-manifest.status=FAIL`（`STAGE4_BYPASSED`）、stage-5 handoff `FAILED`、**退出码 1**，失败产物不得写入 limitations 放行。`COMPLETE_WITH_UNVERIFIED_LAYOUT` 通过时自动标注「版式未渲染审计」，不假填视觉 PASS。

参考文档：阶段 0 全量规则见 `bundle/review/SKILL.md` 与 `bundle/review/reference/*`；阶段 4 全量规则见 `bundle/drafting/SKILL.md` 与 `bundle/drafting/references/*`。两份子 SKILL.md 作为**参考文档**保留在 `bundle/*/SKILL.md`，但不作为可加载 skill。
