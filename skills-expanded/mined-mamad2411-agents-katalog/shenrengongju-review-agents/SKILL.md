# AGENTS.md（review 作用域）

## 审查证据链
- 风险状态变化必须同步 `review/03-问题台账.csv` 与 `review/06-收口执行记录.md`；必要时同步 `review/02-审查总报告.md`。
- freeze 证据必须明确区分“历史 dirty 证据”和“正式 clean freeze”，不能混写成同一口径。
- `review/runtime/**` 属于证据产物；除非任务明确要求，不手工篡改历史快照内容。

## 脚本与记录
- `review/scripts/*` 的正式 gate 应优先复用现有 quality snapshot / docs consistency 能力，不重复造轮子。
- 新增 freeze/gate 脚本时，要在执行记录中写清执行顺序、输出目录、是否要求 clean workspace。
