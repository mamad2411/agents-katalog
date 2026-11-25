---
name: "research-report-review"
description: "通用的研报表格与图表底稿抽取、数据核验和预测复盘工作流。当用户需要完整提取研报表格或图表指标、截取原文图表、生成可刷新的 Choice Excel 底稿、校验历史数值口径或复盘预测时使用。"
license: proprietary
version: "1.6.31"
metadata:
  category: investment-finance
  author: 东方财富
  agent_created: true
---

# 研报底稿抽取与预测复盘

本 Skill 适用于任意公司、行业、地区、语言和排版的研报。不得把单篇研报的公司名、页码、表名、行名、指标或数值当成通用规则。

## 路由

- 只有上传文件、选择 Skill 或没有明确文字任务时，不得默认启动最重的“生成完整研报底稿”流程；先请用户选择下列模式。用户明确要求继续既有底稿任务时可从检查点恢复，无需重复确认。
- “生成研报底稿”：摄取、全表与全图普查、数据映射、Excel 和用户报告。
- 用户说“提取这篇研报底稿”“做这篇研报的底稿”或同义表达时，直接路由到“生成研报底稿”，不得再因“提取”一词与“底稿”一词并存而询问模式。
- “提取研报表格/图表”：摄取、全量抽取、原文截图与元数据交付。
- “核验研报数据”：全表抽取通过后，外部数据比对与口径归因。
- “复盘预测”：预测对实际、根因和框架评价。

## 金标准案例与快速演示

任务开始后先运行 `scripts/golden_case_manager.py match --pdf <输入PDF>`。该检查只计算本地指纹，不调用外部服务。

- 若 PDF 与金标准案例精确匹配，且用户要现场演示、快速复现或明确接受已验收样例，可用 `export` 直接复制该案例的 `expected.xlsx`。必须说明这是已验收样例的复现，不是本次重新执行的实时取数；不得伪造新的执行时间或查询记录。
- 若用户明确要求重新跑、验证当前服务或刷新数据，即使精确命中也必须执行完整流程；案例只作为回归判据，用于比较对象覆盖、截图配对、MQL、方向和版式。
- 若只与案例同类，不得复制样例 Excel 或旧数值。按需读取案例的 `mql_scripts.md`、`feedback_lessons.md` 和 [金标准案例与反馈沉淀](reference/golden_case_workflow.md)，复用查询路径和判断规则后重新解析、查询与验证。
- 案例索引、完整性校验、导出和反馈模板均由 `scripts/golden_case_manager.py` 管理。案例文件受清单哈希约束；校验失败时不得走快速演示路径。

## 执行稳定性

完整底稿任务开始时必须读取并遵守 [分阶段执行、检查点与防循环](reference/execution_stability.md)。不得假设存在固定时限、工具调用次数、积分限制或“必须尽快交卷”；除非用户或运行环境明确给出预算，不得以时间、上下文或效率为理由跳过指标、提前切换数据源、降低验收标准或生成简化交付物。

流程按 `01_census.json → 02_source_evidence.json → 03_mapping_plan.json → 04_query_results.json → 05_workbook_input.json` 单调推进。已 `PASS` 的对象不得重复执行相同操作；续跑从磁盘检查点恢复，不从自然语言进度或曾出现重复的回复恢复。相同工具及参数成功后禁止再调用；失败重试必须产生参数、候选路径或方法变化。相同下一步说明连续出现两次且中间没有新工具结果或工件变化时立即停止叙述，读取检查点并执行唯一尚未完成的动作。

可能阻塞的外部服务按“服务批次”使用 `scripts/service_guard.py` 保护，例如一次 PDF 解析、一页或一组截图的 Vision 验收、一次 MQL 候选检索批次或一个指标族的执行批次。不得为批次内每个正常请求各追加一对本地 `start/finish` 调用。批次开始前原子记录 `PENDING`，结束后结算；同一批次最多 3 次实质不同的尝试。单一服务连续 2 次 `TIMEOUT/PARSE_FAILED/RATE_LIMIT/ERROR/ABANDONED` 时只熔断该服务，不影响其他服务；禁止 sleep、空请求或换对象探活。保存阶段进度；MQL实际调用已返回明确故障终态时，按数据执行协议自动兜底受影响项；未完成调用及其他服务依赖保留阻塞，继续独立步骤。

同一任务的初始MQL工具发现、语法知识及调用规范只加载一次，将工具链标识、知识定位及完成状态保存到已有run_manifest的mql_session。后续所有查询复用，续跑读取已有完成状态；只有工具链实际变化或原有知识被真实语法错误证明失效时才刷新受影响部分。指标元数据、市场路径、实体和期间按需要补查，不是重复加载通用语法。

## MQL 底稿的三项目标

以下目标按顺序约束查询生成和校验，审计字段不得反过来阻止已经正确执行且结果完整的数据块：

1. 原文对象是连续时间序列时，优先使用 MQL 原生时序能力（通常为 `TimeSeriesBlock + SetWindow`）取得完整序列；禁止用区间涨跌幅、单个期末值或多个截面点拼接冒充时序。
2. 对所有可结构化映射的表格和图表逐一尝试 MQL，并以最大化 `20_研报底稿` 的可刷新覆盖率为目标。单个对象失败只隔离该对象，继续生成其他成功对象；不得因一个对象失败清空或阻断整张底稿 Sheet。
3. 财务取数按场景分流：整篇财报表格优先使用报表路径整表直取（`REPORT_FULL_TABLE`，参考 `reference/mql_templates/` 对应科目模板）；个别财务指标或科目优先检索标准指标路径，只有指标无候选、经有效参数真实执行无数据或指标覆盖不完整且留有结构化证据时，才对缺失项使用报表兜底。完整优先级链见 [底稿生成契约](reference/generation_contract.md) G2 的权威 `financial_query_mode` 顺序。

## 不可跳过的顺序

个股研报先读取 [个股研报底稿标准范式](reference/equity_report_standard.md)。

layoutV2 返回后先运行 `scripts/prepare_workbook_phases.py from-layout` 生成 `01_census.json` 与 `02_source_evidence.json` 骨架；该脚本原生兼容 `data.textBlocks`、`textBlocks`、`layoutAnalysis.blocksByPage` 以及 HTML/Markdown 表格。视觉审阅完成后再运行 `normalize-evidence`。行标签、矩形、数值令牌、轴枚举、报告期、图表时间形态和可查询字段等机械字段由脚本生成；模型只补充语义分类、视觉结论和疑难映射。若脚本无法识别输入结构，必须以 `LAYOUT_SCHEMA_BLOCKED` 停止摄取并保存原始响应，不得临时手写完整 census/evidence JSON。

1. 按 [PDF 图表解析与截图接口](reference/pdf_layout_api.md) 调用 `layoutV2`，再按 [PDF 摄取、表格与图表保真](reference/ingestion_rules.md) 建立页面清单、排除区域、全表与全图普查。接口文本只作候选信号；页面渲染图和裁剪图分别是表格结构、图表边界与视觉完整性的最终根据。
   `layoutV2` 地址固定写成构建占位符 `{em_base_url}/proxy/pdf/layoutV2`，由发布/打包过程自动替换为当前正式线或测试线网关，不得硬编码任一环境域名。凭据只允许从当前进程的 `EM_API_KEY` 环境变量或构建占位符 `{em_api_key}` 注入并执行 `.strip()`；不得新增专用 Key 变量或通过命令行传入。空值和未替换的字面量 `{em_api_key}` 均视为未注入。HTTP 或业务码 401/403 记为不可重试的 `AUTH_INVALID`，立即熔断 `pdf_layout`，保存进度后等待有效 Key，禁止重复请求。
2. 每张纳入表格完成“结构→行标签→数值→全量回读”四遍处理；每个 `classType=image` 图表块完成“坐标截图→标题/footer/图形完整性视觉校验→元数据抽取→指标抽取”。同页并排对象必须独立裁切，不得使用跨栏全局阅读顺序。
3. 排除免责声明、分析师/机构利益披露、评级定义、联系信息及“相关研究”推荐目录中的表格。排除对象仍需登记页码、空间范围和理由；财务附表、估值表和正文表格不得因位于附录而排除。
4. 审计清单通过后，先按 [底稿生成契约](reference/generation_contract.md) 固定视觉对象截图配对、表格语义、全量可查字段、全部历史实际期间、原文行列轴和技术键到可读名称的映射；契约完成前不得生成 MQL。财务表语义由原文表名、行标签、期间表头和轴结构共同确定，进入查询阶段后不得降级为普通截面表。再按 [指标清单规范](reference/indicator_inventory_template.md) 区分历史实际、分析师预测、一致预期比较、研报衍生值和主观判断。图表指标必须标记 `source_type=IMAGE`、图表 ID、序列/坐标语义、频率、抽取方法和置信状态；带 `~`、仅来自坐标轴刻度或只能估读的数值不得伪装成精确值。
5. 需要 Choice 映射或数据核验时，按 [数据执行协议](reference/mql_execution_protocol.md) 处理。是否使用 MQL 取决于数据能否结构化查询，不取决于数据领域或本地是否已有缓存。任何可结构化数据都先完成 MQL 指标检索与真实执行；财务、行情、收益率、走势图、宏观、行业、利率、债券、基金、指数、外汇、商品、估值和股本只是常见例子，不构成白名单。现有核心缓存只是财务高频易错路径的加速器。财务来源先用 `scripts/source_coverage_compiler.py` 和 `scripts/financial_workpaper_factory.py` 处理复杂期间、公式和单位；其他结构化来源统一使用 `scripts/structured_mql_factory.py`，按截面、时序或本次 MQL 参考确认的其他组织形态生成脚本。缓存未命中和未列举领域必须进入 `通过MQL工具链获取结构化数据`，不能直接降级到其他接口。各来源分别生成独立脚本，不同 `source_id` 禁止使用相同脚本哈希。所有结构化数据先通过MQL工具链获取结构化数据。实际检索确认无支持候选或有效查询无所需结果，或实际MQL调用返回明确服务故障且按有限预算停止重试，才允许自动对受影响缺失项使用妙想兜底。服务故障登记SERVICE_FAILURE_CONFIRMED及原始请求/响应证据，不冒充指标无数据。未调用、PENDING、IN_PROGRESS、ABANDONED、中断或仅因等待/耗时停止不能换源；语法、参数、证券代码、日期或缓存路径错误先修正，修正耗尽本身不允许换源。正常结果继续复用，替代来源标明故障或缺指标原因，不能伪装成MQL可刷新数据。明确超时必须是工具返回的超时终态，不以等待时长推断故障。
6. 按 [Excel 工作簿规范](reference/workbook_spec.md) 准备执行后 JSON。表格和图表回读数据都必须逐指标检索并实际通过MQL工具链获取结构化数据；表格以 `source_type=TABLE`、图表以 `source_type=CHART` 进入 `workpapers`。一张图表可按实体类型或查询口径拆成多个 MQL 映射块。每个成功块必须保存 `raw_result`，先定义目标行轴和列轴，再分别检查保持原矩阵与行列转置后的形状、表头及行标签。`mql_orientation` 缺省时按 Choice 加载项语义解释为 `1`；若转置结果不符合目标布局，必须显式设置为 `0`。财务多期表的目标通常是纵向财务科目、横向报告期；指数区间涨跌幅的目标通常是纵向指数、横向指标列，但最终有效方向仍由本次 `raw_result` 与目标布局的比较决定。应用有效方向后生成 `last_result`，再由该矩阵建立 `cached_table`，三者机械复核。`expected_rows/expected_columns` 按应用方向后的矩阵填写，溢出区也按该形状预留。能够查询的指标必须进入 MQL；仅未匹配、明确不支持或执行失败的指标才省略。部分指标缺失时以 `PARTIAL/SUCCESS` 生成其余成功 MQL，不得用 PDF 静态值填充失败项。不得在对话中反复手工拼装完整 JSON；使用阶段工件和 `scripts/merge_workbook_phases.py` 唯一合并。合并后先运行 `scripts/preflight_workbook_input.py`，它一次列出全部机械错误；修正拥有字段的阶段工件后最多再预检一次。预检仍失败则保存错误清单并交付阻塞状态，不得通过改写命令绕过去。最终只运行 `scripts/research_report_pipeline.py input.json --output result.xlsx`；该入口依次执行来源覆盖审计、预检和构建，禁止绕过覆盖审计直接反复调用构建器。
7. Excel 是默认第一交付物。固定 Sheet 为 `00_导读`、`10_研报快照`、`20_研报底稿`、`30_预测框架`、`90_执行日志`。
8. `10_研报快照` 对每张图表都执行双通道验收：`layoutV2` 的文本/表格识别结果只作候选信号，PDF 页面渲染图和按坐标裁剪图是最终视觉判据。展示形态按接口返回结构二选一，而不是按“接口是否返回结果”二选一：接口将同一对象另行识别为独立表格块时，通过 `parsed_table_ids` 展示“截图→独立解析表格”；接口只在图片块 `content` 中给出 Markdown/文本候选表格时，将候选结果与截图逐项核验后生成 `chart_data`，展示“截图→双通道验收表”。同一候选数据不重复展示两份表格。若接口候选与截图不一致，以截图为准并记录修正项。快照不展示 `MQL映射状态`、`MQL映射说明`，这些字段仅保留在 JSON 和执行日志用于审计。所有快照内容都是 PDF 来源证据，不是 Choice 查询结果。
9. `20_研报底稿` 只写通过真实执行验证的 MQL 公式、纯脚本批注和空白溢出区，来源可为普通表格或图表回读表。禁止把 `chart_data`、PDF 值、旧缓存、人工补值或 `mx-ds-mcp` 静态结果直接写入本 Sheet；无法映射 MQL 的图表指标只在快照、JSON 和执行日志保留，并记录原因。每个锚点以最终 `mql_script` 为唯一查询来源：该字符串先真实执行，再原样写入 Excel 批注；`script_sha256` 必须同时记录在 workpaper 和对应执行日志中。不得执行综合脚本后裁切结果，再给锚点写入未经执行的“等价子脚本”，也不得给已执行脚本追加未经验证的名称、单位或指标路径。
10. 最终报告面向投研用户，重点是表格/图表完整性、历史数据准确度、口径差异和分析师的盈利、目标价、市盈率预测框架。报告不展示查询脚本、工具评测、技术路径或内部标签；只在用户明确选择后另行导出脚本。

## 完成门禁

只有同时满足以下条件才能宣称“完整抽取底稿”：

- 页面清单覆盖全部页码，纳入+排除表格数等于普查表格数。
- 图表普查覆盖全部 `image` 块及标题命中的表格类图表；纳入、排除与未决数合计等于图表普查数。每张纳入图表的截图和元数据一一对应，标题/footer/图形完整性视觉校验通过。
- 所有纳入表格的表头数、物理数据行数、每行单元格数、数值令牌数和顺序均通过。
- 每个抽取单元格都能定位到唯一表格空间区域；并排表无跨区引用。
- 每张纳入表格逐行逐值回读通过，不得以抽样代替最终验收。
- 查询生成前已产生 `queryable_fields`、来源行列轴契约和 `display_label_map`。任何证券、股票、指数、行业、利率、债券、基金、商品、期货、外汇、宏观或其他序列都必须同时保留技术键与可读名称；代码/ID 不得作为唯一展示标签。期间列同样纳入 `display_label_map`：当真实执行返回的期间表头（如 `2025-12-31`）与研报期间标签（如 `2025A`）逐列不同时，逐列补 `kind=REPORTING_PERIOD` 条目（`key`=取数标签、`display_name`=研报标签）；权威定义见 [底稿规范](reference/workbook_spec.md)。
- 财务报表、财务摘要、主要财务比率和每股指标表已在来源快照中固定为财务语义，目标轴为 `FINANCIAL_METRIC × REPORTING_PERIOD`。全部 `ACTUAL` 报告期必须进入 `source_periods`，并由成功结果或带执行证据的省略记录完整分割；不得只取一期后把表改标为 `CROSS_SECTION_TABLE`。
- 每个财务工作底稿必须记录 `financial_query_mode`，其允许值与优先级链以 [底稿生成契约](reference/generation_contract.md) G2 为唯一权威（整表报表直取优先、个别科目报表兜底，本文件不重列顺序）。选择 `REPORT_FULL_TABLE` 时每张财务表用报表路径整表直取；选择财务时序指标时，每张财务表必须分别用一个 `TimeSeriesBlock(#1) + SetWindow` 覆盖全部目标期间；三张表是三个独立底稿区块，但每张表内部不得按期间拆成多个锚点。成功块必须真实返回全部目标期间；候选路径、窗口和周期等可从脚本与执行结果取得的审计字段由生成器自动补全。报表口径不可用时再尝试时序指标候选；时序指标无候选时继续指标原生多期或按期合并。
- 每张图表必须同时具有接口候选信号和截图视觉验收记录。展示层在“截图+独立表格块”和“截图+图片块 content 双通道验收表”之间二选一；这只是避免重复展示，不是省略任一验收通道。任何 `parsed_table_ids` 引用都必须同页、唯一且不重复展示。存在 `parsed_table_ids` 时不得再为同一候选数据生成 `chart_data`；图片块 content 候选形成 `chart_data` 时必须记录 `candidate_source=LAYOUT_IMAGE_CONTENT`、`visual_validation=PASS` 及修正说明。快照中不得出现 `MQL映射状态` 或 `MQL映射说明` 标签。
- `build_workbook.py --validate-only` 通过，Excel 中五个核心 Sheet 齐全；`10_研报快照` 保留表格原文、图表截图和对应回读表且无覆盖；`20_研报底稿` 对普通表格与图表来源只含通过执行验证的 MQL 公式与空白溢出区，不含任何 PDF 静态数据表、图片或 Excel 图表。若非财务来源只能成功映射为 `EdbBlock` 的 `DATE × SERIES` 时序而不能重构原截面，则以 `PARTIAL/SUCCESS` 保留覆盖与省略说明，并将每个 EDB 锚点放入独立 `21_EDB_NNN` Sheet；主底稿只保留跳转入口。真实 `mx-ds-mcp` 来源和静态核验值保留在执行日志。
- `00_导读` 的标题、标签、值和说明统一左对齐。`20_研报底稿` 不得出现部分 MQL 行与部分静态行混排，也不得以“缓存结果”名义预填任何数据。
- 生成 `20_研报底稿` 的唯一数据契约是本次执行后新 JSON。对 `SUCCESS` 表，`last_result` 必须是实际执行成功的完整返回矩阵，`cached_table` 必须与其逐单元格一致；`PARTIAL/SUCCESS` 不要求与 PDF 原表同形，只要求覆盖所有本次已匹配且执行成功的指标，并明确记录省略项及原因。仅当整表没有成功指标时才降为 `TABLE_BLOCKED`。
- 任一图表查询在 `execution_log` 中记录 `data_source=MQL` 且状态成功时，必须存在引用同一 `source_data_block_id` 的成功 `workpapers` 项和 `20_研报底稿` 公式锚点；不得仅把执行结果写进日志后仍输出静态图表数据。
- 每个成功 MQL 工作底稿都必须填写 `orientation_reason`，记录目标行轴、目标列轴及保持/转置的比较结果。`mql_orientation` 可省略；省略时有效值为 `1`。`raw_result` 应用有效方向后必须与 `last_result`、`cached_table` 逐单元格一致，公式第二参数使用同一有效值，预留溢出区使用方向处理后的行列数。保持/转置均无法匹配目标布局时必须阻塞，不得猜测。
- 每个成功 MQL 工作底稿还必须填写 `target_row_axis`、`target_column_axis`、`row_axis_labels` 和 `column_axis_labels`；应用方向后的第一列与第一行必须分别匹配声明标签。财务多期表固定以 `FINANCIAL_METRIC` 为行轴、`REPORTING_PERIOD` 为列轴；当结果期间表头与研报期间标签逐列不同时，第一行改为等于 `display_label_map` 期间条目的 `key` 序列（`column_axis_labels`/`covered_periods` 仍保留研报标签，权威定义见 [底稿规范](reference/workbook_spec.md)），不得改写 `last_result`。不得在装配阶段统一覆盖逐表方向决策。连续时间图固定以 `DATE` 为行轴、`SERIES` 为列轴，并通过日期范围、频率和有效点数校验。
- 预检必须解析选中 Block 的输出别名，并要求它们依次等于 `script_output_fields` 和 `raw_result` 的非技术表头。每个输出字段必须有 `unit_contracts`：文本/标识符注明类型，数值注明原始单位、展示单位、比例语义和缩放因子。单位或比例语义变化时，转换必须真实出现在该字段的 MQL 表达式中。
- 锚点溢出范围只按最终脚本真实执行后、应用 orientation 的 `last_result` 形状规划。标题、元数据、后续锚点、合并单元格和其他来源区块不得与该矩形相交；不得使用人工声明的估计高度覆盖真实矩阵形状。
- 每段成功 MQL 脚本的数据 Block 必须从 `#1` 开始连续递增，公式选择器必须引用该脚本真实存在的 Block。跨市场、跨指标族或异构结果不能安全合成时，同一来源区域允许追加第二、第三个锚点并分别预留溢出区；不得把只含 `#2/#3` 的脚本批注写入锚点。此多锚点能力用于扩大可刷新覆盖，不能替代财务多期的单一时序查询。
- 图表完整性不是只比较序列名称。连续时间图必须同时满足序列覆盖、起止日期覆盖、频率匹配和每条序列至少两个有效时间点；单个区间涨跌幅只能作为端点核验，不能生成走势图工作底稿，也不能标记 `FULL/PARTIAL`。
- 连续时间图的 `axis_tick_frequency` 与 `observation_frequency` 必须分开。观测频率以曲线点密度、数据语义和候选元数据判定，不得因横轴只标月份就降为月频。必须保存 `frequency_evidence` 和按期间/频率计算的 `expected_min_points`，实际返回点数不足时阻断底稿。
- 走势展示类时序锚点可把 `SetWindow` 结束时间写为不带引号的动态记号：普通时序用 `N()`，`_s` 报告期时序用 `MRQ()`；EDB 不支持。启用时填写 `query_end_date_dynamic`，`query_end_date` 保存生成时快照日期并仍与来源结束日期一致；此类锚点独占 `22_TS_NNN` Sheet（下方留空容纳刷新增长），重放验证以生成时首次执行快照为基线。精确复现类底稿（财务多期整表、核验对照）保持固定窗口。
- 财务个别科目使用 `REPORT_FALLBACK` 兜底时，必须通过 `indicator_attempt_ids` 引用 `90_执行日志` 中同来源的真实指标检索/执行失败记录；自由文本的“无候选”不是证据。整表 `REPORT_FULL_TABLE` 只需 `report_selection_reason`，不要求失败证据。写入 `20_研报底稿` 的唯一门禁是 MQL 真实执行通过；含服务端妙想专用路径的脚本执行成功后允许写入，不再作为禁止项。
- 财务附表与可比公司表必须建立来源覆盖矩阵。财务表的可查科目/期间，可比公司表的公司、报告期和指标，都必须被成功覆盖或带理由省略二者之一完整分割。跨市场或币种不同不是直接省略理由；必须先解析实体并真实尝试。
- 跨市场可比公司按市场生成独立成功锚点；同一来源的所有市场段必须使用相同且有序的 `market_schema`，每段记录 `market_segment` 的市场、币种、实体和代码，代码与选中 Block 的 `SetCodes` 完全一致。所有市场段合并后覆盖来源实体一次且仅一次，并用 `market_output_order` 恢复研报原始顺序。
- `90_执行日志` 的每个成功 MQL 块必须保存指标/对象、原始 Block、完整指标或报表路径、执行编号、取数时间、返回形状/摘要、单位和状态；空壳成功记录视为校验失败。
- 宏观、行业经济、利率、债券、基金、指数、外汇和商品等数值型指标若直接路由到 `mx-ds-mcp`，必须能在执行日志中找到同指标的 MQL 不支持、无候选或无数据证据；缺少该证据视为路由失败，不得宣称底稿完整。
- MQL 失败必须记录标准类别。`SYNTAX_ERROR`、`PARAMETER_ERROR`、`DATE_ERROR`、`ENTITY_CODE_ERROR`、`SECTOR_UNIVERSE_ERROR`、`PATH_ERROR` 是可纠正错误，不得作为 `mx-ds-mcp` 兜底、`NO_MATCH` 或完整交付的依据；允许兜底的类别以 [数据执行协议](reference/mql_execution_protocol.md) Step 2.5 为唯一权威（含 `SERVICE_FAILURE_CONFIRMED`，本文件不重列）。海外代码部分为空而境内代码有值，应先判定实体代码解析问题；行业涨跌幅不得用股票筛选结果替代行业板块/行业指数查询。

单个指标或数据块重试最多 3 次。仍失败时省略该指标并记录原因；只有整张表最终没有任何成功指标时才标记 `TABLE_BLOCKED`。不得把部分结果标记为 `FULL`。

## 按需读取

- 完整底稿任务稳定执行：[reference/execution_stability.md](reference/execution_stability.md)；不要在开始时一次性读取所有其他参考文件。
- 全表抽取：[reference/ingestion_rules.md](reference/ingestion_rules.md)
- PDF 接口、图表截图与元数据：[reference/pdf_layout_api.md](reference/pdf_layout_api.md) 和 [scripts/extract_pdf_charts.py](scripts/extract_pdf_charts.py)
- A股个股三大报表时序取数：[reference/mql_templates/a_share_financial_timeseries.md](reference/mql_templates/a_share_financial_timeseries.md)；核心缓存：[reference/a_share_financial_timeseries_core.json](reference/a_share_financial_timeseries_core.json)
- MQL 脚本模板库（A股三表科目/比率/估值/派生/时序、A股/港股/美股主营构成、港美股、跨品种共 12 个）：生成报表或指标脚本前先查 [reference/mql_templates/index.md](reference/mql_templates/index.md)，按市场×标的×数据形态命中模板，探测确认本次字段元数据后替换【可替换参数】并真实执行通过后才可写入底稿
- Excel 交付：[reference/workbook_spec.md](reference/workbook_spec.md) 和 [scripts/build_workbook.py](scripts/build_workbook.py)
- 阶段证据规范化：[scripts/prepare_workbook_phases.py](scripts/prepare_workbook_phases.py)；在 MQL 规划前生成行标签、数值令牌、轴与期间等机械字段。
- MQL 上下文压缩：[scripts/mql_context_index.py](scripts/mql_context_index.py)；`通过MQL工具链获取结构化数据` 的完整返回按 [数据执行协议](reference/mql_execution_protocol.md) ① 层**原样**先落盘（不做格式改写，不得改写为 HTML/Excel 交付物），再一次建立候选路径索引，禁止通过多次 shell 搜索逐字段翻找同一原始响应。
- 工作簿机械预检：[scripts/preflight_workbook_input.py](scripts/preflight_workbook_input.py)；在唯一一次完整校验前集中报告 census、bbox、期间、图表时间形态和 MQL 矩阵方向错误。
- 个股财务指标候选缓存：按 [reference/mql_execution_protocol.md](reference/mql_execution_protocol.md) 的 Step 2.3，用 [reference/financial_indicator_seed.json](reference/financial_indicator_seed.json) 和 [scripts/financial_indicator_cache.py](scripts/financial_indicator_cache.py) 先生成批量检索计划；缓存仅存指标元数据，不存数值。
- 查询与 Excel 生成前必读：[reference/generation_contract.md](reference/generation_contract.md)。
- 数据核验：[reference/tolerance_rules.md](reference/tolerance_rules.md)
- 预测与估值：[reference/forecast_framework.md](reference/forecast_framework.md)
- 未匹配项：[reference/unmatched_attribution.md](reference/unmatched_attribution.md)
- 报告：[reference/report_template.md](reference/report_template.md) 或 [reference/retrospective_report_template.md](reference/retrospective_report_template.md)
- 仅当对中际旭创对应研报做底稿抽取或回归测试时，读取 [案例锚点.md](examples/中际旭创对应研报/案例锚点.md)。其中数字不得作为其他研报的默认值或必查项。
- 精确命中金标准 PDF、用户要求现场演示，或需要把已确认的人为反馈沉淀为回归规则时，读取 [reference/golden_case_workflow.md](reference/golden_case_workflow.md)。相似周报只读取匹配案例的 `mql_scripts.md` 与 `feedback_lessons.md`，不得加载或复制 `expected.xlsx` 中的旧数值。
