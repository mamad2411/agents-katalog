---
name: YunxiaoQA
description: >-
  测试人员云效（Projex）自动化：拉取待处理/处理中【测试】任务，诊断查重后一键发起缺陷
  （本期交付绑定开发负责人 / 非本期自指定负责人），拉取已修复|暂不修复待验清单，
  批量关闭已修复、再次打开复现缺陷、已关闭并入当期迭代，缺陷闭环后将【测试】标已完成。
  用户说 YunxiaoQA、测试任务、拉取测试任务、发起缺陷、再次打开、批量关闭、并入迭代、
  闭环测试任务 时使用。仅测试角色；不建【开发】/不创建迭代/不代开发改已修复。
  凡写云效先 Plan 确认再一口气 apply；禁止对齐 yunxiao-requirement-lifecycle。
---

# 测试任务（YunxiaoQA）

> **安装**：`npx skills add 15810879921-coder/YunxiaoQA -a cursor -g -y` · 详见 [README.md](README.md)

测试人员云效自动化。斜杠调起 **`/YunxiaoQA`**；对外中文名 **测试任务**。本 Skill **自洽成篇**；**禁止** fork / include / 「对齐」`yunxiao-requirement-lifecycle`。

与 **YunxiaoPM（需求任务）**、开发交付 Skill 分工：本 Skill **只做测试侧**读写。

## Plan 模式门禁（强制 · 凡写云效）

凡会改云效的操作（建缺陷、改状态、闭环任务、挂迭代、改负责人/验证者等），Agent **第一步**必须：

1. `SwitchMode` → **plan**（说明：先对齐参数与执行清单，确认后再一口气 apply）。
2. **切换项目**时：口令带 `项目=` 或 Plan 点选；有 YunxiaoPM 时可复用其 PJ。禁止静默用错误 `spaceIdentifier`；确认后写入 `assets/runtime-ids.json` → `project.last_selected`。
3. Plan 写清：项目名 + spaceId、口令类型、涉及编号、目标状态、负责人/验证者、关联对象、**不会做的事**。
4. **用户确认 / 「执行」之前**：禁止 apply。
5. 确认后切回 Agent，**同一轮按清单一口气执行到底**，再一次性校验回报。

**例外（可读可不进 Plan）：** 仅 `拉取测试任务` / `拉取待验缺陷` 且不改状态。

**禁止：** 以「参数已齐」「速度路径」跳过 Plan。

细则见 [references/plan-gate.md](references/plan-gate.md)。

## 真相源模型

```text
【测试】= 交付子项（TASK_SUB→【交付】）；由开发 Skill 在提测时创建（本 Skill 不建）
缺陷     = Bug 工作项；验证者=workitem.verifier；本期负责人=同交付【开发】负责人
缺陷打开态 = 待确认（禁止再用「待处理」指缺陷）
查重/复用 = 优先编号；禁止只按模糊标题瞎改他人单
测试可改状态 = 已修复→已关闭 | 已修复→再次打开 |（闭环）【测试】→已完成
测试不改     = 待确认/再次打开/处理中 → 已修复|暂不修复|处理中（开发侧）
【测试】任务打开态 = 待处理 / 处理中（任务状态名，与缺陷待确认不同）
产品不建迭代 = 本 Skill 只把已关闭缺陷挂到已有当期迭代
常量       = assets/runtime-ids.json（2026-07-27 01_ONEOS 已实网补齐）
```

## 外置调用（禁止本 Skill 内嵌对方全文）

| 时机 | 调用 |
|---|---|
| 人员 / 项目 catalog / 通用状态 | 优先读本目录 [assets/runtime-ids.json](assets/runtime-ids.json)；缺项再读 `~/.cursor/skills/YunxiaoPM/assets/runtime-ids.json` |
| PJ 云效项目点选 | YunxiaoPM `references/project-selection.md` + `scripts/list_projects.py` |
| 缺陷描述模板 / 定位矩阵 | 本 Skill [references/bug-template.md](references/bug-template.md) · [references/diagnosis.md](references/diagnosis.md) |
| 实写 API | [references/live-api.md](references/live-api.md)（01_ONEOS 已验证） |
| 列表/建缺/流转脚本 | [scripts/README.md](scripts/README.md) · `check_auth.py` / `refresh_cookies.py` / `list_test_tasks.py` / `list_bugs.py` / `create_bug.py` / `transit_bug.py` |

日常测试**优先本 Skill**；不必再挂载英文 `yunxiao-bug-triage`（诊断要点已收入本 Skill）。

## 路由（按需完整阅读）

| 场景 | 模块 |
|---|---|
| 口令面 | [references/commands.md](references/commands.md) |
| 条线 1/2 · 状态机 · 再次打开 | [references/defect-flow.md](references/defect-flow.md) |
| 诊断 · 查重 · 分层初判 | [references/diagnosis.md](references/diagnosis.md) |
| 缺陷描述模板 | [references/bug-template.md](references/bug-template.md) |
| Plan 确认清单 | [references/plan-gate.md](references/plan-gate.md) |
| 实写 API | [references/live-api.md](references/live-api.md) |

## 口令速查

```text
拉取测试任务：状态=待处理|处理中；[项目=…]
发起缺陷：标题=…；描述=…；[测试任务=ONEOS-xx | 交付=ONEOS-xx]；[负责人=…]；[证据=…]
发起缺陷(非本期)：标题=…；描述=…；负责人=…；[验证者=…]；[项目=…]
拉取待验缺陷：状态=已修复|暂不修复；[测试任务=…]；[负责人=…]
批量关闭已修复：[测试任务=…] 或 缺陷=ONEOS-a,ONEOS-b,…
再次打开：缺陷=ONEOS-xx；[原因=复现说明]；[证据=…]
并入当期迭代：缺陷=… 或 范围=已关闭且未挂迭代；迭代=（当期/指定名）
闭环测试任务：测试任务=ONEOS-xx
```

**编号优先**：口令显式 `ONEOS-xx` > 当前上下文 > 询问；**禁止按标题猜编号后静默写云效**。

## 发起缺陷流水线（强制 · 方案 B）

每次 `发起缺陷` / `发起缺陷(非本期)`：

1. **规范化证据**（环境、路径、角色、时间、步骤、实际/期望、截图；无秘密）
2. **查重**（活跃 + 近期关闭；同因则更新旧单并回报，不问则新建）
3. **分层初判**（前端/后端/数据/配置/环境；标「推断」）
4. **填模板** → 见 [bug-template.md](references/bug-template.md)
5. **字段**：验证者=当前测试人；本期负责人=同交付【开发】负责人（多人 Plan 点选）；非本期负责人=口令必填
6. **关联**：本期必须在 **create 时**挂 `ASSOCIATED→【测试】或【交付】`（用 `scripts/create_bug.py`）；创建后强制回读校验；**禁止**依赖事后 `relation/record`（常失败「不能关联相同的工作项」）
7. Plan 回显 → 确认 → apply（`create_bug.py` 去掉 `--dry-run`）→ 回读校验 → 回报编号与链接；关联校验失败（退出码 3）须停并回报

## 本 Skill 终点与明确不做

- **终点**：测试同学完成拉单、提缺陷、回归关闭/再次打开、并入迭代、闭环【测试】。
- **明确不做：** 创建【开发】/【测试】任务、代开发标「已修复/暂不修复」、创建迭代、改需求阶段看板、挂仓库/开分支/提 MR。

可一句交接：「开发侧请用开发 Skill 拉待确认/再次打开缺陷并标已修复|暂不修复。」

## 验收清单（回报自检）

- [ ] 拉【测试】：仅待处理/处理中（或口令指定）
- [ ] 发起缺陷：验证者/负责人/关联正确；走过查重+模板
- [ ] 再次打开：仅自「已修复」且有复现说明；负责人未误改
- [ ] 批量关闭：仅「已修复」→「已关闭」；复现单已跳过或已再次打开
- [ ] 并入迭代：仅「已关闭」；迭代已存在（未新建）
- [ ] 闭环【测试】：关联缺陷全部 ∈ {暂不修复, 已关闭}
- [ ] 本轮无建【开发】、无创建迭代、无代开发改状态
