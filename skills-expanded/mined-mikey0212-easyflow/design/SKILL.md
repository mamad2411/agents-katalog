---
name: design
description: "用户触发 /ezfl:design 或要求进入设计阶段时必须使用本 skill。仅负责设计讨论、Reframe、Premise Challenge，并产出 pre_design.md。"
---

# design

<HARD-GATE>
本 skill **仅**负责把用户需求经过强制结构化讨论后落地为 `pre_design.md`。

- **禁止**跳过 brainstorming 强制交互（≥3 个探索性问题 + 等待用户回答 + 覆盖 ≥3 类）
- **禁止**跳过 Reframe Check（./policies/reframe-check.md）
- **禁止**跳过 Premise Challenge（./policies/premise-challenge.md）
- **禁止**未拿到用户对**完整设计方案**的整体确认就标记本阶段完成
- **禁止**未 `read_file templates/pre-design-template.md` 就生成 `pre_design.md`（Step 4.1 强制前置）
- **禁止**使用未基于 brainstorming 摘要生成的随机 slug——`change_id` 的 slug 部分必须由 AI 从用户回答的探索性问题摘要中提炼（取核心 2-3 个名词关键词），保证可解释性
</HARD-GATE>

**启动时必须先输出**：`[easy-flow] 进入阶段: design — 使用 easy-flow:design skill。`

## 状态布局

- 起草期间：`.harness/changes/draft-<session_suffix>-<unix_ts>/state.yaml`
- Step 4.4 敲定后：`mv` 到 `.harness/changes/<change_id>/state.yaml`
- 同步维护 `.harness/workflow.yaml: active_changes` 游标 entry（写入一律走 `hooks/workflow-entry.sh`，见 `./policies/workflow-lock.md`，HARD STOP H12）。

---

## 流程（按顺序执行，每一步未完成不得进入下一步）

### Step 1：准备 draft 目录 + workflow entry

**单次 Bash 调用**（封装了 draft 创建 / state.yaml 写入 / workflow entry 追加）：

```bash
PLUGIN_ROOT="$(cat <repo_root>/.harness/.cache/.plugin_root)"
INIT_RESULT=$(bash "$PLUGIN_ROOT/hooks/design-init.sh" "<repo_root>")
INIT_EXIT=$?
echo "INIT_EXIT=$INIT_EXIT INIT_RESULT=$INIT_RESULT"
```

**输出解读**（读 `INIT_RESULT` JSON）：

| `INIT_EXIT` | `status` 字段 | 含义 | 后续动作 |
|------------|--------------|------|---------|
| 0 | `"ok"` | 成功 | 从 `draft_name` 取值，进入 Step 1.5 |
| 1 | `"existing"` | 已有未完成 draft | 用 `ask_followup_question` 询问 A/B/C（见下） |
| 2 | —（stderr） | 参数/环境错误 | 按 H12 阻断 |
| 3 | —（stderr） | workflow 写入失败 | 按 H12 阻断 |

`status="existing"` 时 `existing` 字段含已有 draft 目录列表，**必须**用 `ask_followup_question` 询问：
- **A. 续写最新一个**：`draft_name` 为列表最后一项，跳到 Step 2
- **B. 丢弃所有**：对每个 dir 执行以下操作后重新调用 `design-init.sh`：
  ```bash
  for d in <existing 列表>; do
    rm -rf "<repo_root>/.harness/changes/$d"
    bash "$PLUGIN_ROOT/hooks/workflow-entry.sh" delete-active --skill design \
      --repo-root "<repo_root>" --where-change-id "$d"
  done
  ```
- **C. 取消退出**：退出

#### 1.5 状态行输出（H8）

输出 `[easy-flow] design draft: .harness/changes/<draft_name>/ ; workflow: appended entry phase=design`。

### Step 2：加载宪法（注入点 A）

读取 `openspec/memory/constitution.md`（若存在且无占位符）。

### Step 3：brainstorming 强制交互（核心步骤）

#### 3.1 设计讨论（强制硬门）

| 维度 | 下限 |
|------|------|
| 提问数量 | **≥ 3 个**探索性问题 |
| 覆盖类型数 | **≥ 3 类**（不能连提同类问题刷数） |
| 提问范式来源 | `./policies/response-posture.md` 第四节 **Exploratory Question Patterns**（E1-E5） |
| 等待行为 | 必须等待用户回答**全部** ≥3 个问题后才能进入 3.2 |
| 模糊回答处理 | 按 response-posture.md 第二节 **Pushback Patterns** 推回，**不**计入提问数量达成 |

整个子流程必须先 `read_file ./policies/response-posture.md` 并按照其行为对照表、Pushback Patterns、6 条回复前自检执行。

**3.1 自检**（呈现方案前必须通过）：是否已向用户提出 ≥3 个问题、覆盖 ≥3 类、且收到具体回答？未达成 → 继续提问。

#### 3.2 Reframe Check

`read_file ./policies/reframe-check.md` 并按其 **第 1 节**执行：满足 3 个跳过条件则跳过；否则输出 1 个 Reframe 候选，等用户在 ✅ / ✏️ / ❌ 间选择（✅ 进入 3.3；✏️ 最多 2 轮迭代；❌ 保留原始 framing）。

#### 3.3 设计决策方案 Options

`read_file ./policies/reframe-check.md` 并按其 **第 2 节**执行：每个实现层决策点给出 2-3 个方案 + 优劣权衡，等用户在 A/B/C 中选；未选方案 + 拒绝理由记录待写入 `## Alternatives` 节。

#### 3.4 Premise Challenge

`read_file ./policies/premise-challenge.md` 并按其执行：基于 3.1~3.3 提炼 3-5 条前提（覆盖 ≥3 类）→ 输出清单等用户对每条 agree / disagree / unsure（disagree 重生成清单最多 3 轮；unsure 具体追问）→ 全部 agree 进入 Step 4。

### Step 4：产出 `pre_design.md` + 敲定 change_id + 用户整体确认

#### 4.1 写入 `pre_design.md` 到 draft 目录

落盘路径：`<repo_root>/<draft_dir>/pre_design.md`（即 `.harness/changes/<draft_name>/pre_design.md`）。

**强制前置**：写入前必须 `read_file templates/pre-design-template.md`，并输出 `[easy-flow design] 已 read_file templates/pre-design-template.md`。**禁止**未读模板就生成内容。

内容严格按模板的 9 个固定节生成（Reframe 历程 / Constitution Alignment / Premises / Premise History / Decisions / Alternatives / 任务范围 / Open Questions / 下游约束）。各节内容来源（3.2 / Step 2 / 3.4 / 3.3）由本阶段对应步骤的产物填充；首行 `# Pre-Design: <change_id>` 暂用占位 `<TBD>`，4.4 敲定后回填。

#### 4.2 用户整体确认 pre_design.md

向用户输出预览并询问：

> 以上是完整的设计方案（包括架构、技术选型、任务范围），请 review 并确认是否可以进入下一阶段？
>
> （请回复"确认 / ok / 同意"等明确的整体确认；若仅对某个条目有意见，请直接指出该条目以便修改）

判定规则：

| 用户回复 | 判定 | 后续动作 |
|---------|------|---------|
| 明确整体确认（"确认/ok/同意"等） | 完成 | 进入 4.3 |
| 仅对某条/某节给出反馈 | **不算确认** | 修改对应内容后**重新执行 4.2** |
| 模糊回复（"差不多"、"可以吧"） | **不算确认** | **必须明确再问一次**："以上是完整的设计方案，请确认是否可以进入下一阶段？" |
| 沉默 / 无回复 | **不算确认** | 同上 |

**禁止**把 3.1~3.4 中任何一处用户的局部"同意"当作整体确认。

#### 4.3 生成 change_id（AI 自动）

整体确认后，AI 自动从 brainstorming 的"核心问题陈述"（用户答完 ≥3 个问题后浮出的核心动作 + 对象，**不**是字面摘录）提炼 2-3 个核心名词/动词关键词，kebab-case 拼接得 slug（正则 `^[a-z][a-z0-9-]+$`，10-25 字符），再拼 `change_id = "<slug>-<session_suffix>"`（终态正则 `^[a-z][a-z0-9-]+-[0-9a-f]{6}$`）。校验失败重试，3 次后阻断要求人工介入。

可审计输出：

```
[easy-flow] AI 已生成 change_id：<change_id>
  slug 来源：<提炼时引用的 brainstorming 关键词，如 "refactor / sdk / api">
  session 后缀：<session_suffix>
该标识将作为 worktree 目录 / git 分支 / OpenSpec change 目录 / 本 change state.yaml 的统一名字。
如需覆盖，请在 /ezfl:propose 触发前回复："改为 <新 slug>"，否则进入下一阶段后无法修改。
```

不阻塞流程，直接进入 4.4。若 4.5 后用户回复"改为 X" → 用 X 替换 slug 重做 4.4。

#### 4.4 重命名 draft → 正式目录 + 同步 workflow.yaml

**单次 Bash 调用**（封装了目录 mv / state.yaml 更新 / pre_design.md 首行回填 / workflow rename）：

```bash
PLUGIN_ROOT="$(cat <repo_root>/.harness/.cache/.plugin_root)"
FINAL_RESULT=$(bash "$PLUGIN_ROOT/hooks/design-finalize.sh" "<repo_root>" "<draft_name>" "<change_id>")
FINAL_EXIT=$?
echo "FINAL_EXIT=$FINAL_EXIT FINAL_RESULT=$FINAL_RESULT"
```

| `FINAL_EXIT` | 含义 | 后续动作 |
|---|---|---|
| 0 | 成功 | 进入 4.5 |
| 1 | 目标目录已存在 | 按 H12 阻断 |
| 2 | 参数/环境错误 | 按 H12 阻断 |
| 3 | workflow rename 失败 | 按 H12 阻断 |

#### 4.5 输出完成状态行

输出 `[easy-flow] design 阶段完成：.harness/changes/<change_id>/pre_design.md 已锁定；workflow entry change_id 由 <draft_name> 改为 <change_id>。` 并提示下一步 `/ezfl:propose`。
