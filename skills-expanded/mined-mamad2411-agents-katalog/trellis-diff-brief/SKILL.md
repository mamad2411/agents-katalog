---
name: trellis-diff-brief
description: "按需读取当前 Trellis 任务与实际 git diff，生成对话内简短改动说明。用于用户想知道“这轮改了啥”、push 前看改动、check 前快速理解实现范围、sub-agent 实现后主对话需要复盘实际变更时。"
---

# Trellis Diff Brief

按需解释当前任务的实际改动。只读 task artifacts 和 git diff，在对话里输出摘要；不写文件、不修改代码、不做 check、不提交。

## 核心规则

- 以真实 git 状态和 diff 为准，不凭记忆总结。
- 优先关联当前 Trellis 任务；没有当前任务时，也可以只基于 git diff 汇总。
- 区分任务相关改动、生成/快照/任务文档改动、未识别 dirty 文件。
- 不替代 `trellis-check` / `trellis-check-all`；只解释改动，不判断质量是否通过。
- 默认不输出大段 patch。必要时只读取关键文件的局部 diff。
- 不执行 `git add`、`git commit`、`git push`、`git merge`、格式化、测试或任何写操作。

## 执行步骤

1. 解析任务：
   - 运行 `python3 ./.trellis/scripts/task.py current --source`。
   - 若有当前任务，读取 `prd.md`、`design.md if present`、`implement.md if present`、`brief.md if present` 和 `task.json`。
2. 收集父仓状态：
   - `git status --short`
   - `git diff --stat`
   - `git diff --name-only`
   - `git diff --cached --stat`
   - `git diff --cached --name-only`
   - `git log --oneline -5`
3. 如 `task.json.base_branch` 存在，补充：
   - `git log <base_branch>..HEAD --oneline`
   - `git diff --stat <base_branch>...HEAD`
4. 如父仓状态显示 submodule dirty，或 `.trellis/config.yaml` 中有独立 Git package，按同样方式读取对应 Git root 的状态。
5. 只在需要解释行为时读取关键 patch：
   - `git diff -- <file>`
   - `git diff --cached -- <file>`
   - 对大文件或大 diff 只抽取相关片段，不整段粘贴。

## 输出格式

```markdown
## Diff Brief

### 任务目标
- <来自 brief / prd 的一句话；没有任务时写“未绑定当前任务”>

### 实际改动
- <按行为或模块归纳，不按文件机械罗列>

### 关键文件
- `<path>`：<改了什么，为什么重要>

### 生成 / 文档 / 快照
- <如无则写“无明显生成或快照改动”>

### 未识别 dirty
- <不属于本轮任务或无法判断的 dirty 文件；如无则写“无”>

### 验证状态
- **已看到**：<从对话、任务文档或命令输出能确认的验证>
- **未确认**：<没有证据的检查，不要假装已跑>

### 注意点
- <风险、需要人工重点看的点；如无则写“无明显风险”>
```

## 分类口径

- “实际改动”写用户或 workflow 能感知的行为变化。
- “关键文件”只列会帮助用户理解改动的文件；不要把 `git diff --name-only` 原样全贴。
- “生成 / 文档 / 快照”用于区分 `enhancements/`、任务文档、manifest、锁文件、生成物等辅助改动。
- “未识别 dirty”必须如实列出，避免用户以为它们也属于本轮实现。
- “验证状态”只能写有证据的命令或检查；没跑就写未确认。

## 不要做

- 不要创建 `changes.md` 或其它持久文件，除非用户明确要求。
- 不要修改 `brief.md`、三件套或 `task.json`。
- 不要把 diff brief 写成 check 报告。
- 不要为了简短省略会改变用户判断的范围、风险或未识别 dirty。
