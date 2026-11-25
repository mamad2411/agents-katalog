---
name: caw-eval
metadata:
  version: "2026.04.22.1"
description: |
  在本地 Mac 编排 CAW (Cobo Agentic Wallet) Agent 评测，并把 headless claude / openclaw agent
  dispatch 到远端服务器执行，最终产出评分数据和分析报告。
  Use when: 用户想运行 CAW 评测、跑评测、测试 Skill、评估 Agent 质量、
  生成评测报告，或说 "跑评测", "测评 CAW", "eval", "评分",
  "recipe 评测", "弱模型评测", "openclaw 评测", "模型兼容性测试"。
---

# CAW Eval

端到端评测 CAW Agent 质量：本地 Mac 作为调度器，dispatch 到远端服务器跑 headless claude
（标准 / recipe 评测）或 openclaw agent（弱模型兼容性评测），评分和报告都在本地完成。

## Step 0: 环境识别（必做）

```bash
[[ "$(hostname)" == *openclaw* ]] && echo "env=openclaw" || echo "env=local"
```

- `env=local`：继续。确保 `gcloud auth login` 已完成、IAP 通道可用。
- `env=openclaw`：停止。本 SKILL 是**本地调度器**，不能在 openclaw 服务器直接跑。
  请回到本地 Mac 终端后重新触发。

## 流程路由

评测三个正交维度：

| 维度 | flag | 取值 |
|------|------|------|
| 评测模式 | `--eval-mode` | `e2e`（默认，全 E2E 含 task_completion）/ `pact`（仅评 pact 构造）/ `onboard`（onboarding 评估） |
| Recipe 来源 | `--recipe-source` | `real`（默认/调真实 backend）/ `seed`（注入 dataset 的 recipe）/ `empty`（注入空，对照组） |
| Agent 类型 | 脚本分文件 | `run_eval_cc.py`（Claude Code headless）/ `run_eval_openclaw.py`（弱模型如 doubao/minimax/gpt） |

> 老 cli 仍兼容：`--eval-mode standard ↔ e2e`、`--eval-mode recipe ↔ pact`；`--recipe-mode cc_with_recipe/openclaw → seed`、`cc_no_recipe → empty`、`cc_real_recipe/oc_real_recipe → real`。

### 速查表（用户意图 → 命令模板）

| 用户说 | eval-mode | recipe-source | 脚本 | 服务器池 | run_name 模板 | 详细步骤 |
|--------|-----------|---------------|------|----------|---------------|----------|
| "跑评测" / "全流程评估" / 默认 | `e2e` | `real` | `run_eval_cc.py` | `SERVERS_CC_MAIN` | `eval-cc-{model}-e2e-real-recipe-{TS}` | [run-eval-cc.md](./references/run-eval-cc.md) |
| "真实 recipe" / "live recipe" + CC | `e2e` 或 `pact` | `real` | `run_eval_cc.py` | `SERVERS_CC_MAIN` | `eval-cc-{model}-{mode}-real-recipe-{TS}` | [run-eval-recipe.md](./references/run-eval-recipe.md) |
| "recipe 评测" / "pact 模式" + dataset recipe 注入 | `pact` | `seed` | `run_eval_cc.py` | `SERVERS_CC_MAIN` | `eval-cc-{model}-pact-seed-recipe-{TS}` | [run-eval-recipe.md](./references/run-eval-recipe.md) |
| "recipe 对照组" / "无 recipe" | `pact` | `empty` | `run_eval_cc.py` | `SERVERS_CC_CTRL` | `eval-cc-{model}-pact-no-recipe-{TS}` | [run-eval-recipe.md](./references/run-eval-recipe.md) |
| "recipe 对比评测" | 三跑：`pact`+`seed`、`pact`+`empty`、`pact`+`real` | — | 两个脚本都用 | MAIN（seed/real）+ CTRL（empty）| 三 run | [run-eval-recipe.md](./references/run-eval-recipe.md) |
| "弱模型评测" / "doubao/minimax/gpt 评测" / "openclaw 评测" | `e2e` 或 `pact` | `real` 或 `seed` | `run_eval_openclaw.py` | `SERVERS_{MODEL}` | `eval-oc-{model}-{mode}-{source-alias}-{TS}` | [run-eval-openclaw.md](./references/run-eval-openclaw.md) |

**run_name 别名约定**：`real → real-recipe`、`seed → seed-recipe`、`empty → no-recipe`。模板：`eval-{cc|oc}-{model}-{eval-mode}-{source-alias}-{YYYYMMDD-HHMM}`。

**默认**：`run_eval_cc.py --eval-mode e2e --recipe-source real`（即 sonnet headless 全 E2E + agent 调真实 backend recipe）。

执行前的公共前置（SSH / gcloud / 服务器同步）：[common-execution.md](./references/common-execution.md)

---

## 概览

### e2e / pact 评测（CC headless）

本地 Mac 用 `run_eval_cc.py dispatch` 并行调度 N 台服务器，每台跑 headless `claude -p`。

```
本地 dispatch → 动态队列（空闲服务器自动取下一个 item）
               → 远端 claude headless 跑任务
               → scp 拉回 session → 上传 Langfuse → 评分 → 报告
```

- 时间：17 case / 3 台 ≈ 30-50 分钟（取决于难度）
- **服务器池**（详见 [run-eval-cc.md Step 2](./references/run-eval-cc.md)）：
  - `SERVERS_CC_MAIN`：3 台（test09-11），跑 e2e / pact + `recipe-source=real|seed`
  - `SERVERS_CC_CTRL`：3 台（test12-14），仅跑 pact + `recipe-source=empty` 对照组
  - 两池互不干扰，Recipe 对比可并行
- 详细步骤：[run-eval-cc.md](./references/run-eval-cc.md)
- Recipe 五种组合对比：[run-eval-recipe.md](./references/run-eval-recipe.md)

### Openclaw 弱模型评测

本地 Mac 用 `run_eval_openclaw.py dispatch` 并行调度多台 openclaw 服务器，每台串行跑
`openclaw agent`，session 直接上传 Langfuse，本地评分出报告。

```
本地 dispatch → 多台服务器 openclaw agent 跑任务 → 上传 Langfuse
             → 本地读 Langfuse trace 评分（LLM Judge subagent 并行）→ 报告
```

- 时间：14 case / 3 台弱模型 ≈ 1-3 小时（取决于模型）
- 详细步骤：[run-eval-openclaw.md](./references/run-eval-openclaw.md)

---

## 评分体系

### e2e 模式（全流程）

```
综合分 = task_completion × 0.3 + process_quality × 0.7
process_quality = S1(意图) × 0.15 + S2(Pact) × 0.45 + S3(执行) × 0.4
```

### pact 模式（仅评 pact 构造）

```
综合分 = S1(意图) × 0.20 + S2(Pact) × 0.45 + S3(交易构建) × 0.35
S3 = tx_construction_correctness × 0.5 + recipe_adherence × 0.3 + tx_submission_success × 0.2
```

无 task_completion。仅评估交易是否被正确构建/提交，不评估链上执行结果。

所有分数 0-1。详见 [scoring.md](./references/scoring.md)。

## 问题归因（写报告时使用）

对每个 finding 按 7 层归类：🔵 被测 SKILL / 🟢 评分体系 / 🟡 数据集 / 🟤 Recipe / 🟠 评测工具链 / 🔴 产品代码 / 🟣 运行环境。细则见 [issue-attribution.md](./references/issue-attribution.md)。

## 数据集

| 数据集 | Case 数 | 场景 | 说明 |
|--------|:-------:|-----|------|
| `recipe-test-v3` | 7 | uniswap-swap / aave-lend / weth-wrap | Recipe 评测（推荐），统一 schema v2 |
| `standard-test-v3` | 7 | 同 recipe-test-v3 | 标准评测（推荐），同一份测试集 + 不同 eval_mode 做 A/B |
| `caw-agent-eval-seth-v2` | 14 | transfer / swap / lend / dca / ... | 旧 schema（pact_hints/stage_criteria），仅历史回放 |
| `caw-recipe-eval-seth-v1` | - | recipe 多步骤 | Sepolia 多步骤场景，部分 item 已部分新 schema |

- 默认 `recipe-test-v3`（pact 模式）/ `standard-test-v3`（e2e 模式）
- `recipe-test-v3` 和 `standard-test-v3` 内容**完全一致**（只是 metadata.eval_type 不同），区别仅在运行时：
  - `--eval-mode pact --recipe-source seed`：dispatch 注入 `CAW_RECIPE_FILE`，judge 评 tx 构建（不评链上）
  - `--eval-mode e2e --recipe-source real`：dispatch **不**注入 `CAW_RECIPE_FILE`（agent 自主 `caw recipe search`），judge 评全流程（含 task_completion）
- `--dataset-name` 可指定其他数据集
- 数据集管理：[dataset-management.md](./references/dataset-management.md)
- 数据集审查（11 条机械规则）：[dataset-review.md](./references/dataset-review.md)

## 服务器环境搭建

新建 openclaw 评测服务器（GCP 实例 / openclaw / caw / onboarding / 充值 / 验证）：
→ [server-setup.md](./references/server-setup.md)

## Scripts

| 脚本 | 用途 |
|------|------|
| `run_eval_cc.py` | CC 评测编排（dispatch / run / upload / score / metrics） |
| `run_eval_openclaw.py` | Openclaw 评测编排（dispatch / run / upload / pack） |
| `score_traces.py` | 评分管线（断言 + judge → 综合分 → Langfuse） |
| `judge_cc.py` | LLM-as-Judge（prompt 构建） |
| `assertions.py` | 结构化提取 + 门槛断言 |
| `eval_utils.py` | 公共工具（Langfuse 客户端 / 数据集 / 批量上传） |
| `upload_session.py` | session → Langfuse trace |
| `generate_dataset.py` | 数据集生成 |
| `validate_dataset.py` | 数据集 schema 校验 |
| `runtime_compliance.py` | 评测运行时合规自检 |
| `sync_to_servers.sh` | 服务器同步 + hash 校验 |
