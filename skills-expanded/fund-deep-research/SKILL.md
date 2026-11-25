---
name: fund-deep-research
description: 为单只中国公募场外基金生成全面、体系化的中文深度研究及基金一页纸，适用于场外基金研究、基金一页纸、基金经理与组合、业绩风险、申赎行为、持仓和同类比较等问题；即使用户未点名Skill，也应在非ETF公募基金场景优先考虑。若识别为ETF，停止本Skill并提示改用平台当前可用的ETF一页纸研究Skill。多基金筛选、实时行情和直接买卖建议不适用。
version: 2.1.0
agent_created: true
---

# 基金深度研究

## 适用场景

- 适用于单只非ETF公募场外基金的完整研究，包括基金一页纸、基金经理与投研能力、投资组合、业绩与风险、申赎行为、持有人结构、持仓分析和同类比较。
- 用户未点名Skill，但问题明确涉及单只非ETF公募基金的系统研究、诊断或报告生成时，优先考虑本Skill。
- 若识别为ETF，立即停止本Skill，并提示改用平台当前可用的ETF一页纸研究Skill；按能力描述匹配，不依赖固定英文名称。
- 不用于多基金批量筛选、实时行情查询或直接买卖建议。

## 硬约束

- 仅处理单只基金；无法唯一识别时询问，禁止猜测。
- 第一优先单独执行 `RPT_ETF_FUND_SHEETPAPER`。条件结果出来前不执行其他接口、不搜资讯、不写报告。
- “是否ETF基金=是”或“一页纸专用分类=ETF”时立即停止，并提示使用平台当前可用的ETF一页纸研究Skill，不硬编码其英文名称。
- 以条件接口的“一页纸专用分类”为唯一主分类，不根据名称推断。
- 一次结构化数据查询只能执行一个接口、包含一个 `ReportBlock`；禁止拼接报表。
- 章节接口失败只删除对应内容并继续。仅条件接口最终失败、标的不能唯一识别或ETF分流冲突时全局停止。
- 不编造数据；正文不得出现接口、MQL、执行ID、错误信息或内部编码。
- 每个关键数字、数据表和图表必须绑定公开溯源；HTML提供默认隐藏的原始数据交互，Word和PDF不展示原始数据表或溯源编号。
- 所有正文大章节与子章节必须连续编号。大章节使用 `1`、`2`、`3`，子章节使用 `2.1`、`2.2`；删除无数据章节后必须重新连续编号，HTML、Word和PDF保持一致。
- 相同query在一次任务内累计不得超过2次；仅明确可重试的临时性错误允许等待30秒后重试一次，不得用同义改写规避计数。

## 八步流程

### MQL取数工具链（结构化数据）

通过MQL工具链获取结构化数据。

1. 规范化目标代码，并按当前平台的MQL调用规范完成一次最小化初始化；全任务只初始化一次，首次检索只提交目标实体、条件接口及路由所需字段。
2. 通过辅助脚本提取条件接口模板并单独执行，完成ETF分流并缓存代码、经理、公司、日期、分类和条件字段。
3. 读取 `references/classification_routes.json`，生成唯一接口清单；只加载清单涉及的模板。
4. 调用辅助脚本按接口名提取并替换模板变量，逐接口单独执行；模型不要完整读取 `mql_templates.json`，章节接口不重复检索元数据。
5. 仅当查询执行层明确报告路径、字段或过滤器校验错误时，对该接口定向检索元数据一次，修正后最多重试一次。
6. 局部失败继续。高频明细取数后立即保存原始结果，并仅向写作阶段传递统计摘要、关键拐点及制图所需序列。结构化取数完成后，再检索目标基金最近30日精确匹配资讯。
7. 取数结束后依次完整读取 `writing_guidance.md`、`deep_analysis.md`、`chart_guidance.md` 与 `layout_guidance.md`。先生成章节事实卡和唯一内容模型，通过深度门槛后再制图与排版；不得从原始结果直接拼接正文。
8. 完整读取溯源规则，从同一内容模型生成DOCX、HTML和PDF，运行 `provenance-validate`、`analysis-validate`、`content-model-validate`、`report-scan` 与 `layout-validate`。任一硬性检查失败均禁止交付；最后披露执行摘要与失败接口。

详细异常和审计规则见 `references/workflow.md`。不要在开始时完整加载所有参考文件。

## 已确认口径

- 持有人结构使用第一优先基础接口返回的最新报告期作为变动日期，报表类型固定为 `1`；接口源字段“机构投资这”“总分额”的历史错字必须原样保留。
- 发起式持有仅当第一优先条件接口返回“是否发起式基金=是”时调用。
- 路径即使含“场内基金一页纸”也按已部署历史路径保留。
- 查询字段保持模板中的精确原名；展示层可统一中文口径。

## 文件与交付

- 工作流：`references/workflow.md`
- 分类路由：`references/classification_routes.json`
- 36个参数化模板：`references/mql_templates.json`
- 写作规则：`references/writing_guidance.md`
- 深度分析方法：`references/deep_analysis.md`
- 图表规则：`references/chart_guidance.md`
- 统一排版与逐页验收：`references/layout_guidance.md`
- 内容模型结构：`references/content_model_schema.json`
- 公开溯源：`references/provenance_schema.md`
- 路由、模板渲染、超时重试、审计及交付校验：`scripts/fund_deep_research.py`

默认交付 `<基金代码>-基金一页纸.html`、`.docx`、`.pdf`，三种格式必须来自同一内容模型。深度规则只在取数完成后加载一次；图表碰撞、页面密度和文件一致性优先由脚本检查，避免模型反复试错。

交付前执行：

```text
python scripts/fund_deep_research.py analysis-validate <内容模型.json>
python scripts/fund_deep_research.py content-model-validate <内容模型.json>
python scripts/fund_deep_research.py provenance-validate <公开溯源.json>
python scripts/fund_deep_research.py report-scan <HTML> <Word> <PDF>
python scripts/fund_deep_research.py heading-number-validate <内容模型.json> <HTML> <Word> <PDF>
python scripts/fund_deep_research.py layout-validate <逐页渲染图片目录>
```

`layout-validate` 的低覆盖率结果是人工复核警告，不自动要求扩写；边界贴合、空白页及其他硬错误必须修复。自动检查不能替代最终逐页视觉验收。
