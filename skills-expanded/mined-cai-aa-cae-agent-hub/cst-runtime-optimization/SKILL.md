---
name: cst-runtime-optimization
description: 当用户要求使用 CLI/runtime 执行 CST 参数优化循环、S11 指标迭代、多轮仿真对比时调用此 Skill。本 Skill 依赖 cst-runtime-cli 提供基础设施，不携带 runtime scripts，所有 CLI 调用走 base skill 的 uv run python -m cst_runtime 入口。
---

# CST Runtime 优化 Skill

## 优化流程速查

```text
Phase 0: 准备
  task 确认(工程/目标/参数/约束) → inspect-project(含category)
  [agent: 选几何参数 → 用户确认 → 翻译为objective spec]

Phase 1: 探针(参数≥4强制)
  run-probe-phase --objective <spec>
  [agent: 看top_params/edge_hit → 选参数/调范围/定算法]

Phase 2: 优化循环
  loop:
    run-optimization-step --objective <spec>
    [agent: objective达标? → break / ask_study_failed? → 换优化器]

Phase 3: 收尾
  generate-report → 灵敏度验证 → 经验→docs/
  [agent: 收敛质量判断 + 结论沉淀]
```

**关键决策点：**
| 阶段 | 节点 | agent 行动 |
|------|------|-----------|
| 0 | inspect-project | 筛选 `category=geometry` 的参数作为候选 |
| 0 | task确认 | 向用户确认5项：工程类型、objective函数、目标阈值、参数列表、几何约束 |
| 1 | run-probe-phase 返回 | `main_effects_normalized > 0.1` 保留，`edge_hit=true` 扩范围 |
| 1 | 算法选择 | 参数少+线性=TPE，多+交互复杂=CMA-ES，默认 `suggested_algorithm` |
| 2 | 每轮返回 | `objective_value` vs 目标阈值 → 达标break |
| 2 | ask_study_failed | 未达标且 study 认为收敛 → 换优化器(最多一次) |
| 3 | 收尾 | 灵敏度验证 + 经验入库 |

## 定位

本 Skill 专注 CST 参数优化闭环，依赖 `cst-runtime-cli` 提供底层基础设施。

- 不携带 `scripts/` 或 `cst_runtime/` 源码；所有 CLI 调用走 base skill。
- 负责定义优化迭代流程、早停判断、参数策略、数据导出和报告生成。
- 所有生产任务使用标准 `tasks/task_xxx_slug/runs/run_xxx/{projects,exports,logs,stages,analysis}` 结构。

## 依赖声明

本 Skill 不实现 CST 操作，以下工具全部由 `cst-runtime-cli` 提供。所有 CLI 调用通过工作区的 `-m cst_runtime` 入口执行。

| 职责 | CLI 工具 |
|------|---------|
| run 创建 | `prepare-run`、`get-run-context` |
| 审计 | `record-stage`、`update-status` |
| 进程/session | `cst-session-open`、`cst-session-close`、`cst-session-quit` |
| 参数 | `list-parameters`、`change-parameter` |
| 仿真 | `start-simulation-async`、`wait-simulation` |
| 结果导出 | **`export-run-results`**（统一导出 S11+2D+远场） |
| 结果显示 | **`generate-report`**（生成综合报告） |
| **探针阶段** | **`run-probe-phase`**（一键探针：设计→仿真→分析→注入 study） |
| **优化迭代** | **`run-optimization-step`**（一步迭代：ask→改参→仿真→tell，agent 判断早停） |
| Objective 函数 | 内置在管道中 — `s11_min_db`, `s11_at_freq`, `gain_max`, `bandwidth`, `expression` |

## Objective 函数系统

优化目标不再硬编码为 S11 min dB。通过在管道工具中传入 `--objective <spec>` 指定目标函数：

| 类型 | 格式 | 示例场景 |
|------|------|----------|
| S11 全局最小值 | `{"type": "s11_min_db"}` | 默认，最小化反射 |
| 指定频率 S11 | `{"type": "s11_at_freq", "freq": 2.4}` | 2.4GHz 阻抗匹配 |
| 最大增益 | `{"type": "gain_max", "port": 1}` | 优化天线增益 |
| 带宽 | `{"type": "bandwidth", "below_db": -10}` | S11<-10dB 带宽最大化 |
| 自定义表达式 | `{"type": "expression", "expr": "min(s11_db)"}` | 灵活组合 |

objective 默认方向：s11 类为最小化，gain/bandwidth 类为最大化。可通过 `direction` 覆盖。

两个管道（`run-probe-phase`、`run-optimization-step`）均接受 `objective` 参数。省略时默认 `{"type": "s11_min_db"}`，与旧行为完全一致。

## 触发条件

使用本 Skill：
- 参数优化循环、S11 指标迭代、多轮仿真对比
- 需要实现"仿真 → 读结果 → 解析指标 → 判断是否达目标"的自动化循环
- 需要定义早停条件（target S11 阈值、轮数上限）

不使用本 Skill：
- 单次仿真或结果读取（用 `cst-runtime-cli`）
- 纯几何建模、材料、边界定义

## 文件名约定

导出文件统一放到 `exports/`，固定命名：

```text
exports/
  s11_run{N}.json              ← {N}=CST run_id，无时间戳
  farfield/{freq}_port{port}_run{N}_{quantity}.json ← 每轮独立
  result_2d_*.json
  report.html                  ← generate-report 输出
```

## 优化迭代模式

所有优化迭代走统一模式：

```text
┌─ agent 循环 ──────────────────────────────────────────────┐
│ run-optimization-step --objective <spec>                   │
│   → objective_value, study_best, steps_since_improvement   │
│   → 达标? → break / ask_study_failed? → switch sampler    │
│   → 未达标 → 继续循环                                       │
└───────────────────────────────────────────────────────────┘
```

> `run-probe-phase` 和 `run-optimization-step` 是**自包含管道**，各自管理完整的 session 生命周期。详见 `describe-pipeline`。
>
> 如需在标准流程中插入自定义步骤（如改参后验证实体），可回退到原子工具（`prepare-experiment` + `run-experiment` + `ask-study` + `tell-study` 等）。

### 降级模式（无需 Optuna 时）

适合仅需简单改参仿真对比、不建 study 的场景：

```text
┌─ 每轮迭代 ──────────────────────────────────────────────────────┐
│ prepare-experiment  ← 修改参数（支持 names+values 批量改参）      │
│   → run-experiment  ← 仿真 + 自动导出 S11 + 远场                     │
│   → agent 看 objective_value → 早停判断                           │
│   → 达标 break / 未达标继续下一轮                                  │
└─────────────────────────────────────────────────────────────────┘
```

> `prepare-experiment` 和 `run-experiment` 是**自包含管道**，各自管理完整的 session 生命周期。

### 原子工具模式（需要自定义步骤时）

```text
┌─ 每轮迭代 ─────────────────────────────────────────┐
│ cst-session-open                                    │
│   → change-parameter → save-project                 │
│   → start-simulation-async → wait-simulation        │
│   → cst-session-close --save false                  │
│   → export-run-results                              │
│   → 早停判断 → 达标 break / 未达标继续下一轮              │
└────────────────────────────────────────────────────┘
```

### 每次新建项目

适合改变几何实体或需要完全独立数据。每轮独立 `run_00N` 目录。

```text
prepare-run(run_00N) → prepare-experiment
  → run-experiment
```

### 结果显示

```powershell
# 先用 args-template 生成参数，再调用
uv run python -m cst_runtime args-template --tool generate-report
# 编辑模板中的 data_dir、output_html、modules 字段
uv run python -m cst_runtime generate-report --args-file <模板.json>
```

`modules` 默认 `s11,farfield3d,timeline`，可选 `metrics,optimization`。

`generate-report` 自动读取 `exports/` 下的全部 `s11_run*.json` 和 `farfield/*.json`，渲染 S11 曲线、3D 远场、参数变更记录和操作审计。

**3D 远场仪表板**：使用 WebGL Canvas 渲染，支持鼠标拖拽旋转、滚轮缩放、自动旋转。页面自包含（无 CDN 依赖），可作为独立 HTML 文件离线查看。

## 自动化优化循环红线

> **早停判断** 是本 Skill 区别于照单执行的关键红线。其他通用红线（session 分离、S11 复数处理、远场增益证据约束等）见 `cst-runtime-cli` SKILL.md。

- 每轮执行流程必须包含早停判断：`仿真 → 读结果 → 计算 objective → 判断是否达目标 → 达则 break，不达则继续`
- "执行"和"评估"不得拆分为两个独立阶段；目标指标必须在每轮循环体内部实时解析和判断
- 若未实现早停导致超过目标后继续执行额外轮次，任务输出必须明确标记为 `overrun`
- 参数发现：使用 `inspect-project`（而非 `list-parameters`）一次性获取全部参数名、值、中文描述。避免逐一 `describe-tool` 查每个参数。
- **探针强制**：待优化参数 ≥ 4 个时，**必须先执行探针阶段**（`run-probe-phase`），筛选关键参数后再进入正式优化循环。跳过探针直接进入正式优化的，任务输出必须标记为 `probes_skipped`，由此产生的浪费轮次计入 agent 成本。

### 禁止自编优化脚本

agent **不得**为优化循环编写独立 Python 脚本（如 `optimize_loop.py`、`run_optimization.py` 等）。

所有优化迭代必须使用现有管道工具（`run-probe-phase` + `run-optimization-step`，或降级到 `prepare-experiment` + `run-experiment`）或原子工具的 CLI 原生编排。脚本层无法正确处理：
- CST 缓存命中后的状态恢复
- DE 进程锁死后的自动重启
- 多 run_id 的数值排序读取
- 远场导出的时序依赖
- 探针阶段的多轮循环状态管理

任何偏离管道工具的自定义脚本均视为违规，由此产生的浪费（仿真轮次、时间、结果丢失）由 agent 承担。

### 禁止销毁已有 run 数据

run 目录（`runs/run_xxx/`）是**不可逆数据容器**。禁止：

- 删除或覆写 `exports/` 下的历史导出文件
- 从源工程重新拷贝 `.cst` 替换 `projects/working.cst`——这会丢失所有历史 run_id 和结果

当需要干净工程状态（如清除 CST 内部缓存、重置仿真历史）时，必须：

```text
prepare-run → 创建新 run_00N 目录
             → 从源工程拷贝到新 run 的 projects/
             → 新旧 run 各自保留完整数据
```

这样旧 `run_00N-1/` 的 `exports/` 和 project 历史保持完整，新 `run_00N/` 从零开始，互不干扰。

### 已知问题与恢复

| 问题 | 原因 | 恢复方式 |
|------|------|---------|
| 端口非均匀填充 | 修改 `g`(脊间距) 导致端口区域出现多种材料 | `cst-session-close --save false` 丢弃改参，恢复原值 |
| 部分仿真未重跑 | CST 检测到网格未改变时可能返回缓存结果 | `run-experiment` 内置 run_id 预检对比，输出 `warning` 字段 |
| 远场导后保存 | 远场导出使 CST 进入错误状态 | `close(save=False)` 自动处理；**不要额外调用 save** |

## 优化闭环流程

### Phase 0：准备

**目的：** 确保 agent 和用户对优化目标一致理解。

1. `prepare-run` → `get-run-context`
2. `inspect-project` → 返回全参数（含 `category`）
3. agent 筛选 `category=geometry` 的参数作为候选，列出给用户
4. 向用户确认 5 项：
   - 工程类型
   - 优化目标函数（S11 min / 指定频率 S11 / 增益 / 带宽 / 自定义表达式）
   - 目标阈值
   - 候选参数列表（含初始范围）
   - 几何约束（如 L ≥ g）
5. agent 将用户确认的优化目标翻译为 `objective` 参数格式

**引导规则：**
> 优化目标必须向用户确认后才能进入探针阶段。参数选择以 `category=geometry` 为主。
> 用户描述的目标由 agent 翻译为 objective spec。无明确目标时默认最小化 objective。

### Phase 1：探针（参数≥4 强制）

```powershell
uv run python -m cst_runtime run-probe-phase \
  --project-path <run>\projects\working.cst \
  --parameters '{"R":{"min":0.1,"max":0.5},"g":{"min":20,"max":30}}' \
  --study-storage <run>\studies\optimization.db \
  --study-name horn_matching \
  --objective '{"type":"s11_min_db"}'
```

`run-probe-phase` 自动完成：
1. 复制 `working.cst` → `working_probe.cst`（基线隔离）
2. 设计 Plackett-Burman 折因实验
3. 逐点仿真，按 `objective` 函数计算值
4. 导出移入 `exports/probe/`
5. 分析主效应 + 交互效应
6. 注入 Optuna study

**返回：** `main_effects`、`interactions`、`top_params`、`edge_hit`、`suggested_algorithm`

**agent 决策：**

| 决策 | 信号 | 规则 |
|------|------|------|
| 选参数 | `main_effects_normalized` | > 0.1 保留，< 0.05 固定为中心值 |
| 调范围 | `edge_hit` | true → 扩范围或提示用户 |
| 选算法 | `suggested_algorithm` | TPE（默认）/ CMA-ES（多参数+强交互） |

### Phase 2：优化循环

```powershell
uv run python -m cst_runtime run-optimization-step \
  --project-path <run>\projects\working.cst \
  --study-storage <run>\studies\optimization.db \
  --study-name horn_matching \
  --objective '{"type":"s11_min_db"}'
```

`run-optimization-step` 自动完成：
1. 切换优化器（如指定 `--sampler`）
2. `ask-study` — Optuna 采样
3. `prepare-experiment` — 改参 + 保存
4. `run-experiment` — 仿真 + 导出
5. 按 `objective` 函数计算值
6. `tell-study` — 回报结果

**返回：** `objective_value`、`study_best`、`steps_since_improvement`

**agent 早停判断：**

```
每轮返回后:
  1. objective_value < target? → break ✓
  2. ask_study_failed 且未达标且未换过优化器? → --sampler cma-es 切换
  3. 否则继续循环
```

**切换优化器：** 加 `--sampler cma-es` 或 `--sampler random`。pipe 内部重建 study + 迁移历史 trial。

### Phase 3：收尾

1. `generate-report`
2. 收敛质量评估：`study_best` 在边界？相比 probe `mean_value` 有改善？
3. 灵敏度验证：最优 ±1%、±5% 跑 check-point，用同一 `objective` 函数评估
4. 经验写入 `docs/opt-exp-*.md`

**引导规则：**
> 灵敏度验证使用与优化阶段相同的 `objective` 函数。经验入库是验收项，缺少 docs/ 记录的任务标记为 `incomplete_docs`。

## 泛用经验总结

每次优化任务完成后，必须提炼**可复用的泛用经验**，写入工作区根目录的 `docs/` 目录。

### 触发条件

满足以下任一条件即需总结：
- 遇到新的 CST 行为陷阱（缓存、覆盖、状态异常等）
- 发现参数间的交互效应或非线性关系
- 探针阶段筛选出意外的关键参数
- 优化策略（TPE、网格搜索等）在特定场景下表现异常
- 管道工具组合使用中发现的新模式或限制

### 输出格式

文件命名：`docs/opt-exp-{YYYY-MM-DD}-{简短主题}.md`

内容结构：
```markdown
# 经验：{标题}

## 场景
- 工程类型：
- 参数集：
- 优化目标：

## 发现
{具体现象、数据、对比结果}

## 根因
{分析结论，区分 CST 行为 vs 物理规律 vs 工具限制}

## 泛用规则
{可迁移到其他工程的经验，1-3 条}

## 验证状态
- [ ] 单次验证 / [ ] 多次验证 / [ ] 跨工程验证
```

### 存放位置

工作区根目录 `docs/` 下，按主题分类：
- `docs/opt-exp-*.md` — 优化经验
- `docs/cst-traps-*.md` — CST 陷阱
- `docs/pipeline-patterns-*.md` — 管道编排模式

### 质量要求

- **泛用性**：经验必须能迁移到至少 2 个不同工程场景，否则不写
- **证据驱动**：每条结论必须有对应的 `exports/` 数据或 `stages/` 记录支撑
- **不重复**：写入前检查 `docs/` 是否已有同类经验，有则追加而非新建
- **不写过程**：只写结论和规则，不记录"我做了什么"的流水账

## 引用

以下通用规则详见 `cst-runtime-cli` SKILL.md：
- **CLI 调用原则** — 入口模式、JSON 契约、args-template 优先（默认写到 `.cst_runtime/tmp/`）、project_path 约束
- **管道工具自包含性** — `prepare-experiment`/`run-experiment`/`inspect-project` 各自管理 session，无需前置 `cst-session-open`
- **错误处理** — `workspace_not_initialized`、`source_project_missing`、`ambiguous_open_projects`、`lock_not_released`、`Access is denied`
- **进程管理前置 gate** — `cst-session-management-gate` 管道、硬性停止条件
- **结果与远场红线** — S11 复数处理、modeler/results session 分离、仿真后关闭顺序、`close(save=False)` 规则

## 最终验收清单

- [ ] 优化循环每轮均实现早停判断
- [ ] `exports/` 下有导出文件（s11_run{N}.json 等）
- [ ] `status.json` 状态正确
- [ ] 工程已关闭且无 `.lok` 锁文件
- [ ] 清理 CST 进程结果已记录
- [ ] `logs/tool_calls.jsonl` 和 `stages/` 可追溯
- [ ] 只使用了 Skill + CLI，没有调用旧脚本
- [ ] 使用了 objective 函数（非默认需确认）
- [ ] 参数数 ≥ 4 的优化已执行探针阶段（`run-probe-phase` 或 `design-probes` + `analyze-probes` + `study-add-trials`）
- [ ] 探针结果（主效应、交互效应、`top_params`）已记录到 `stages/`
