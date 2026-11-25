---
name: event-review
description: 周审/记忆提炼。用干净的上下文读取事件日志与任务残留，提炼候选条目进 inbox，按阈值提议 memory/knowledge/skill 升级，并陪同用户逐条分流。当用户说"review events"、"整理记忆"、"周审"、"提炼事件"或距离上次审阅超过一周时使用。
---

# Event Review —— 事件提炼与记忆升级

你是一个**干净 agent**：不带任何正在进行的任务上下文，只做提炼。
方法论依据：hook 只记事件不做判断；由干净 agent 定期读事件、跨时间去重归类；
人每周批量审，分流到 CLAUDE.md / L2 索引 / memory / 丢掉。

## 输入

- 事件日志：`.agents/events/events-*.jsonl`（按月，不可变）
- 水位线：`.agents/events/.last-reviewed`（上次审到的行号/文件名）
- 检查点：`.agents/events/checkpoints/`（compact 时抢救的任务状态）
- 现有条目：`CLAUDE.md`、`AGENTS.md`、`.agents/INDEX.md`、`.agents/knowledge/`、`.agents/pitfalls/`、`.agents/runbooks/`
  （用来**去重**：已经沉淀过的不要再提）

**不要读 `.agents/inbox/` 之外的待审内容当成结论引用**；不要读 `.agents/current/`（那是活跃任务，与本次提炼无关，除非它在 checkpoints 里）。

## 步骤

### 1. 读事件，归类
从水位线之后开始读。关注的事件类型：
- `tool_error`：同一类错误（同文件/同报错特征）出现 **≥2 次** → 候选 knowledge（坑）
- `compact` + `checkpoint_saved`：对比 checkpoint 里的 plan/notes 与最终结果，找"被压缩掉但仍有价值"的结论
- `gate_block`：反复被门禁拦截的同类修改 → 可能是流程问题
- `stop`/`session_start`/`session_end`：用于判断任务边界，本身通常无价值

### 2. 写候选进 inbox（只写 inbox，不直接改任何受保护文件）
每个候选一个文件：`.agents/inbox/YYYY-MM-DD-<slug>.md`，头部包含：
```
类型: pitfall | knowledge | memory | skill-draft | discard
来源: 事件日志行 / checkpoint 路径
建议去向: CLAUDE.md 第X节 | .agents/INDEX.md 坑目录 | .agents/knowledge/xxx.md | memory(feedback) | 丢掉
```

### 3. 应用三个升级阈值
| 信号 | 阈值 | 产出 |
|---|---|---|
| 同类失败重复 | ≥2 次 | 候选 knowledge（写 inbox） |
| 用户重复说同样的话 | 第 2 次 | memory（feedback 类型，写入项目 memory） |
| 同一流程成功 | 3 次 | skill 草稿提议（只提议，**绝不自动安装**） |

- memory 写入：项目 memory（Claude Code 项目级 memory，feedback 类型；路径可用 `/memory` 查看）。memory 的写入不需要门禁（它是 agent 自己的笔记），但内容必须只关于"这个 agent 怎么干活"。
- knowledge / pitfall / runbook / skill：**一律先进 inbox**，等用户审。

### 4. 陪同用户周审（逐条过）
对每个 inbox 条目，向用户说明：内容、来源证据、建议去向，请用户三选一：
1. **收**：按去向落盘 ——
   - 写 `CLAUDE.md` / `.agents/INDEX.md` / `.agents/gate.conf` / skills / settings 会触发门禁：先征得用户同意，`touch <项目根>/.claude/.gate-token`，再写入（令牌一次性）。
   - 落盘后从 inbox 删除该条目，并在来源知识文件的"升级记录"打勾。
2. **改**：按用户意见修改后再落盘。
3. **丢**：删除条目（大多数候选应该被丢掉，这是正常的）。

### 5. 收尾
- 更新 `.agents/events/.last-reviewed`（记录已审到的事件文件与行号）。
- 向用户汇报：收了 N 条 / 丢了 M 条 / 待跟进事项。

## 纪律
- 跨时间去重优先于收录：同一个坑第二次出现时合并进已有条目，不新建。
- 拿不准就标"存疑"留待下次，不要强行下结论。
- 一次只审一周的量；事件太多时分批，不要一口气吞完撑爆上下文。
