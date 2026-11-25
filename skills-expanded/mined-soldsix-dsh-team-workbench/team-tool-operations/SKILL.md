---
name: team-tool-operations
description: 团队任务工具的准确调用、版本冲突、自动派工、提交验收、重复检测和无副作用恢复；用于队长、组长与执行成员。
user-invocable: true
disable-model-invocation: false
metadata:
  language: zh-CN
  version: '1.1'
---

# 团队任务操作

## 首轮调用

先读 `team_goal`、`list_agents` 和当前任务；已分配到任务的成员读该任务即可，不重复全队盘点。用 `team_help({"topic":"tasks","action":"所需操作"})` 看操作的必填项，或查询本主题真实工具参数。会话里说“做完了”不能代替提交。

## 任务与并发

同一目标版本、输入版本、环境和验收对应一个任务及有效执行。创建前查可复用结果与 `input_key`；有意的交叉验证另立“独立复核”任务。计划的 input_version、environment_version、acceptance_criteria 一起传；输入路径只列现有输入。聊天请求先登记再派工。新方案使用 project_plan；input_key 使用已确认任务 id，输入、输出、依赖和验收须一致。前置文件验收并发布后，再创建消费它的下一阶段任务，不把未来文件当现有输入。

独立问题可并行，依赖通过已验收任务建立。执行者、写入范围、输出和复核员要明确。默认复用闲置且技能适合的成员；待命不调用模型。auto_dispatch、auto_assign 和 required_skill 以工具当前参数为准，不靠反复发送同一消息催办。

## 更新顺序

1. `team_task_get` 取得最新 revision、execution_id、状态、目标版本和阻碍。
2. 更新只传当前 action 的字段。改计划用 plan；修改文本用 edit；配复核用 configure_review。不能把 complete 的 evidence 填给 review_evidence。
3. 执行者优先 `team_task_submit`，兼容入口为 complete；提交 result、evidence、实际 artifact_paths；有计划的任务附当前 execution_id。提交不等于通过验收。
4. 指定独立复核人优先 `team_task_review`，兼容入口为 review；提供非空 review_summary、review_evidence 和逐项 review_checks；没有验证就不能 accepted。
   私有成果通过 team_workspace 的 read_artifact 按提交回执读取，不直接读取执行成员目录。复核拒绝不会自动重跑；队长先判断是成果缺陷还是复核工具故障，再明确重分配剩余工作。需要停止自动调度时，执行或复核期间可以 configure_dispatch 设置 auto_assign:false，不 release 当前执行。
5. 有旧外部影响时由另一成员先核对，再 `team_task_reconcile`。重分配、release 或 reopen 不清除副作用历史。

## 错误恢复与验收

团队目标只用 `team_goal({"action":"read"})` 核对。模式同时提供的 `get_goal` 是个人目标工具，返回 null 不代表已确认的团队目标完成、消失或撤销。确认状态、任务验收和模型最终汇报分别核对，不能用其中一个代替另外两个。

CAS 冲突只先重读，再判断更新是否已成功；不能机械地换 revision 重试。重复投递先查消息/执行，避免另建 run。退休前移交执行任务、待复核项、消息与下级。验收以有效任务版本和真实产物为准，旧目标成果保留后按差异重新核查。

按需读 [操作表与恢复案例](references.md)。
