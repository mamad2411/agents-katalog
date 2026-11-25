---
name: experiment-results-reporting
description: Organize RPent or LIBERO evaluation runs into reproducible validation-set and experiment-results tables, with evidence-based failure attribution and explicit token, timing, cost, and extrapolation rules. Use when adding a validation set, summarizing a new run, or comparing evaluation outputs; do not use for running evaluations or changing benchmark code.
metadata:
  short-description: Reproducible evaluation tables and metric rules
---

# 实验结果汇总

将已有的评测清单、运行配置和结果产物整理成两张可复现的中文表格。只读取用户指定的产物；不要因汇总请求补跑、重试、修复数据集或修改评测代码。

开始前确认统计范围：验证集名称、run/output 目录、模型与版本、是否包含重试，以及目标全集的定义。若结果来自多个 run，逐条记录来源并避免重复计数。缺少字段时写 null 或“未知”，不要把缺失当作零。

## 固定输出

先用一句话说明范围和数据完整性，然后输出以下两张表：

1. **验证集组成与设置**：按 suite 或任务条目列出 suite、task ID、rollout 数、seed、任务类型/实际目标、swap 或扰动关系。表格下列出共同运行设置：planner、model、reasoning effort、每条最大模型响应数、planner timeout、最大环境步数、watchdog、策略权重、memory、硬件/渲染模式等。明确这些是本次运行设置还是官方配置。
2. **实验结果汇总**：按 suite 和最后一行 overall 汇总成功/失败/未知/未运行、有效统计条数、总/平均 token、平均 rollout 时间、平均环境服务时间、平均扣除环境时间、官方 API 等价费用。若用户要求完整全集估算，在表末增加一行“完整全集外推”，并在表下说明外推方法与假设。

不同验证集或不同 run 应分组展示，不能静默合并。需要横向比较时保持相同列和相同统计口径。

## 先归因，再统计

先串联 episode → attempt/thread → request/response 的时间线，核对模型错误、工具返回、finish/finalizer、预算记录与累计 usage。顶层 `timeout`、进程退出码或缺少终结 usage 不能单独决定失败原因和统计范围。

- **服务端/网络失败**：有证据的断网、代理错误、服务容量不足等失败请求不计入方法 token 与费用。若同一任务随后有完整的有效响应/成功尝试，取该有效部分计算，前面的服务失败不使该任务失去统计资格。记录排除的请求/尝试及原因。
- **harness/模型能力失败**：最大模型请求次数、工具决策次数或环境步数耗尽，以及有效执行中的规划、代码、控制失败，均如实计为任务失败；失败前的有效 usage 与费用全部纳入。API 连接重试上限与任务决策上限是两种预算，必须区分。
- **混合原因**：任务已用尽决策预算并报告失败，随后服务断开或外层超时，仍保留该任务失败及此前有效执行用量。只有服务故障、尚无可判定结果的任务单列为基础设施中断；wall-clock 超时或 watchdog 触发必须沿时间线确认是服务等待还是有效执行耗尽，不能直接归因。
- **请求成功不等于任务成功**：有效响应包括导致任务失败的响应；多轮任务要累计全部有效响应，不能只取最终一次响应或只挑成功任务。独立完整重跑是否替换旧 episode，仍按已确认的 run 合并规则；不得借此删除有有效执行的能力失败。
- **取消笼统的 partial 判定**：不得因某次服务失败无 usage、缺少 turn.completed 或请求数不一致，将整个任务标为 partial 并剔除均值。先恢复 session 最新累计值与逐请求 usage，核对其覆盖的有效执行范围。仅失败请求缺 usage 时不预留“未知费用”或宣称总量是下界。确实缺少有效响应的 usage 时，写明具体请求、缺失字段和证据，保留已有用量及任务结果；不能把缺失编成零，也不能无说明地改变分母。

## 统计口径

- 结果状态分开记录：任务成功、任务失败、启动失败/未知、超时、未运行。成功率分母必须标明；不要把“有效样本成功率”写成完整验证集成功率。
- token 使用选定有效请求对应的 Codex thread/tokenUsage/updated 或 session thread_token_usage / total_token_usage 的最新去重累计值。累计值已覆盖的请求不能再相加；跨线程按 thread ID、跨响应按 response ID 去重。若累计值混有明确服务失败的已记录用量，按对应请求证据排除，不能为“对齐”请求数或终结记录任意扣减。总 token 为 input + output；缓存输入和 reasoning output 已包含在这两个字段中，不重复相加。保留原始整数，展示时可用 M = 1,000,000。
- token 和费用采用相同的有效请求范围，任务均值包含成功与 harness/模型能力失败。分母按有可统计有效用量的任务计算，不按有没有历史服务失败计算；若有效响应用量确实缺失，分别披露已记录量、缺失原因和对应指标分母。不要用“完整 usage n”制造未经归因的筛选。
- rollout 时间是有效执行区间的 wall-clock；环境时间是同一区间内环境服务 handler 的活动区间；扣除后时间为 rollout - simulator。初始场景准备、服务启动、结果持久化和导出不计入 rollout。若计时不可取得或差值为负，写 null 并记录原因。用量归因不自动改变完整 rollout 时间：wall-clock 中的服务等待如需扣除，必须有可定位的时间区间并另标“扣除服务等待后的时间”，不得按失败次数估算扣时。
- 官方费用必须注明模型、价格版本/日期、计费档位和输入缓存处理。标准档位的通用公式为：(uncached_input / 1e6) × input_price + (cached_input / 1e6) × cached_price + (output / 1e6) × output_price。若单请求超过模型价格页规定的长上下文阈值、使用 Batch/Flex/Fast、代理重试或自定义 API，应单独说明；API 等价费用不是实际账单。
- 估算优先按 suite 分层：对每个 suite 用有效样本均值乘以目标全集中该 suite 的条目数，再求和。样本不足、任务选择有偏或数据版本不一致时必须标为粗略预算，不得给出虚假的置信区间。可同时给出整体均值外推作为敏感性参考，但不能替代分层估算。
- 报告实际有效条数、缺失条数、是否包含失败和超预算条目、是否包含重试。历史 run、失败重试和修复后的新 run 默认不合并，除非用户明确要求并提供合并规则。

## 复现信息

记录清单版本/哈希、代码版本与工作区状态、run manifest、模型/effort、策略与 memory 标识、依赖或数据版本、统计时间范围。不要输出 API key 或整份环境变量。需要字段定义、CSV/JSON 映射和归因示例时，读取 [references/report-schema.md](references/report-schema.md)。
