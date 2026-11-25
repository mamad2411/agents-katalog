---
name: spec-debate
description: 让 Claude 与 Codex 对一份 spec 文档做匿名对抗辩论，由独立第三方裁判合成终稿。当用户想"辩论这份 spec"、"对抗评审 spec"、"让 Claude 和 Codex 辩论文档"、或输入 /spec-debate [路径.md] 时触发。产出 debate-log.md + spec.final.md，原文件零改动。
---

# spec-debate

> 四阶段对抗辩论：独立评审 → 交叉评审 → 反驳（≤3 轮自适应停机）→ 独立裁判合成。Claude 与 Codex 是异构辩手，互相匿名；主循环只编排，绝不下场辩论。

**触发**：`/spec-debate <spec路径.md>` 或自然语言「辩论这份 spec / 对抗评审这份文档」。

本 SKILL.md 是**编排剧本**——你（Claude Code 主循环）作为**中立编排器**逐步执行。长提示词在 `references/`，按需读取并注入。**你自己绝不评审或反驳 spec**，只调度子 agent / Codex、做匿名化转译、判定收敛、写日志、调度裁判。

---

## 角色

| 角色 | 实体 | 说明 |
|------|------|------|
| 编排器 | 你（主循环） | 中立调度，不辩论 |
| 辩手甲 | fresh Claude 子 agent（Agent 工具，general-purpose） | 异构视角之一 |
| 辩手乙 | Codex（`codex-companion.mjs task`） | GPT 侧视角 |
| 裁判 | fresh Claude 子 agent | 零辩论记忆，独立合成 |

向任一辩手 / 裁判传递信息时，**统一用「评审甲 / 评审乙」中性标签，绝不泄漏对方是 Claude/Codex/GPT**。

---

## 步骤 0：前置检查

1. 入参须是存在的 `.md` 文件。否则打印用法 `/spec-debate <spec路径.md>` 并停止。
2. **定位 Codex companion**（最硬的外部依赖）：

```bash
COMPANION=$(ls -t ~/.claude/plugins/cache/openai-codex/codex/*/scripts/codex-companion.mjs 2>/dev/null | head -1)
[ -z "$COMPANION" ] && COMPANION=$(ls -t ~/.claude/plugins/marketplaces/openai-codex/*/scripts/codex-companion.mjs 2>/dev/null | head -1)
echo "${COMPANION:-NOT_FOUND}"
```

若为 `NOT_FOUND`：告诉用户 Codex 未就绪（建议 `/codex:setup`），并询问是否**降级为「仅 Claude 双 agent」**模式（见步骤 5）。本会话用户已授权自主完成时，直接走降级并在日志标注。

3. **建产物目录**：设 spec 路径为 `$SPEC`，目录为 `${SPEC%.md}.debate/`：

```bash
DEBATE_DIR="${SPEC%.md}.debate"; mkdir -p "$DEBATE_DIR"
```

---

## 步骤 1：独立评审（1 次，并行，互不可见）

1. 读 `references/reviewer-prompt.md` 与 `references/json-contract.md`，把 `{{SPEC_CONTENT}}` 替换为 spec 全文，得到评审提示 `P`。
2. **并行**发起两侧：
   - **辩手甲**：用 Agent 工具起 general-purpose 子 agent，prompt = `P` + 附上 json-contract 正文。要求返回 envelope JSON。
   - **辩手乙**：起 Codex 后台任务，轮询完成后取回结果：
     ```bash
     # 起任务：输出形如 "Codex Task started ... as task-xxxx"
     JOB=$(node "$COMPANION" task --background "$P_ESCAPED" | grep -oE 'task-[A-Za-z0-9-]+' | head -1)
     # 轮询直到 status=completed（每 6s 一次，Codex 通常数十秒～数分钟）
     until node "$COMPANION" status "$JOB" --json | grep -q '"status": *"completed"'; do sleep 6; done
     # 取回：辩手乙的最终输出在 result JSON 的 .job.summary 字段
     node "$COMPANION" result "$JOB" --json | python3 -c 'import json,sys;print(json.load(sys.stdin)["job"]["summary"])'
     ```
     （`P_ESCAPED` 为转义后的提示文本。`.job.summary` 即 Codex 的完整回答，对它做 JSON 抽取。）
3. 对两侧返回各做 **JSON 抽取**（见下「JSON 抽取兜底」），得到 `甲_r1`、`乙_r1` 两个 envelope。
4. **立即增量写日志**：把第 1 轮两侧 envelope 追加到 `$DEBATE_DIR/debate-log.md`（带轮次标题 + 可读转录）。

---

## 步骤 2-3：交叉评审 + 反驳（循环，≤3 轮）

从 round=2 开始，最多到 round=3。每轮：

1. 读 `references/cross-review-prompt.md`。为**每一方**构造提示，替换：
   - `{{SELF_LABEL}}` / `{{OTHER_LABEL}}`：甲↔乙
   - `{{SPEC_CONTENT}}`：spec 全文
   - `{{SELF_PREV}}`：该方上一轮 envelope
   - `{{OTHER_PREV}}`：**对方**上一轮 envelope（此处即天然匿名——只传 JSON，不带身份）
2. **并行**让两侧产出本轮 envelope（甲走 Agent 子 agent，乙走 Codex task）。抽取 JSON。
3. **立即增量写**本轮两侧 envelope 到 `debate-log.md`。
4. **收敛判定**：

   ```
   stop = 甲.converged AND 乙.converged
          AND 甲.remaining_disputes == []
          AND 乙.remaining_disputes == []
   ```
   - `stop == true` → 跳出循环，进步骤 4。
   - 否则 round<3 继续下一轮；round==3 强制停。
5. **空轮保护**：若本轮**双方都**是空 / 非法 findings，**不得**据此判收敛 —— 记为失败轮，向用户报告（自主模式下：重试该轮一次，再失败则带现有日志进裁判并标注）。

---

## 步骤 4：合成（裁判，1 次）

1. 读 `references/judge-prompt.md`，替换 `{{SPEC_CONTENT}}`（原 spec）与 `{{DEBATE_LOG}}`（完整 `debate-log.md` 内容，已匿名）。
2. 用 Agent 工具起一个**全新** general-purpose 子 agent 当裁判（不复用任何辩论上下文）。
3. 把裁判输出写入 `$DEBATE_DIR/spec.final.md`（含正文 + 末尾采纳/驳回理由表）。

---

## 步骤 5：降级路径（Codex 不可用）

辩手乙改用**另一个 Claude 子 agent**扮演，system 提示强调"你是挑刺型评审乙，立场要与评审甲尽量不同、专找对方忽略的角度"。其余流程（匿名、循环、收敛、裁判）完全不变。在 `debate-log.md` 顶部标注 `模式：降级（双 Claude，无异构）`。

---

## 步骤 6：收尾

打印：
- `debate-log.md` 与 `spec.final.md` 的绝对路径
- 跑了几轮、是否收敛 / 触顶、是否降级
- 一句话：**原 spec 未改动；终稿在 spec.final.md，由你决定是否替换原文。**

---

## JSON 抽取兜底

从模型 / Codex 返回文本中提取 envelope：
1. 优先匹配 ```json ...``` 围栏内内容；否则取第一个 `{` 到最后一个 `}`。
2. `JSON.parse` / `python3 -c "import json,sys;json.load(sys.stdin)"` 校验。
3. 失败 → 对该方**重请求一次**（提示里追加"上次输出非合法 JSON，请只输出 envelope JSON"）。
4. 再失败 → `debate-log.md` 记 `WARNING: <方> round<N> JSON 无效，按空 findings 处理`，该方该轮 `findings:[]`、`converged:false`。

---

## 硬约束

- 主循环**不评审、不反驳、不补充 finding** —— 只搬运、匿名、判定、记录。
- 任何传给辩手 / 裁判的内容**不得**出现 Claude / Codex / GPT / 模型名等身份线索。
- **绝不覆盖**原 spec 文件；所有产物只落在 `*.debate/` 目录。
- 硬上限 3 轮，杜绝死循环。
