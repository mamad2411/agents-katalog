---
name: slow-api
description: 接口变慢、P95 增长、下游调用超时或用户响应延迟时使用。
---
# 接口变慢排查 v1.0.0

适用：files 系统 1.0.0、demo 环境。需要相同窗口的延迟指标、调用链样本、超时日志和变更记录。

query_metrics 区分基线与当前 P95，保留 ms 单位；get_trace_summary 指出样本覆盖范围。不能把少量调用链当完整请求分布。
用 search_logs 核对超时错误码和 request_id；用 get_recent_changes 列出时间上相近的变更。get_dependencies 核对依赖边，read_evidence 按 ID 取回上下文。

结束：得到有支持与反对证据的服务级候选，或缺失调用链/指标时保留待核实。建议补查仅针对当前资产许可范围。

示例：请求总耗时 4380 ms、下游跨度 4170 ms 只支持优先核查下游，不证明宿主 CPU 或网络是根因。
