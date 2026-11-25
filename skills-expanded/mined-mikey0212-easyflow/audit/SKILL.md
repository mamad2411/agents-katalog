---
name: audit
description: "用户触发 /ezfl:audit 或要求审计实施产出时必须使用本 skill。执行 Constitution 合规检查（注入点 D）+ 5 项 scorer 脚本，结果写入 .harness/metrics/<timestamp>-metrics.json。"
---

# audit

<HARD-GATE>
禁止跳过任何 5 个 scorer 脚本。在 team 模式下，scorer 检出 blocking 违规时禁止把 audit 标记为通过。在审计结果写入 `.harness/metrics/<timestamp>-metrics.json`（目录形式，每次 audit 一个新文件）之前禁止进入 ship。
</HARD-GATE>

**启动时必须先输出**：`[easy-flow] 进入阶段: audit — 使用 easy-flow:audit skill。`

## Overview

审计 skill。两步审计流程：Constitution Compliance Audit + Scorer 评分。


**Metrics 存储约定**（贯穿 audit / reflect / scorer）：
- 目录：`.harness/metrics/`（**当前工作目录的** `.harness/`——若在 worktree 内即 worktree 的 metrics，ship 阶段会合回主仓）
- 文件名：`<timestamp>-metrics.json`，每次 audit 写一个新文件，**不覆盖**历史
- `<timestamp>` 推荐格式：`YYYYMMDD-HHMMSS`（UTC，例如 `20260525-074800`）
- **JSON 顶层必含 `change_id` 字段**（v0.3.7 起）：用于 reflect 按 change 维度归因；同一 worktree 内若先后跑过 A→B 两个 change 的 audit，可按 change_id 区分
- **稳定契约**：`.harness/metrics/` 是**唯一存储位置**（不再拷贝到 archive）。reflect 通过 glob 聚合全局趋势；单 change 追溯通过 JSON 内的 `change_id` 字段从顶层过滤。**禁止把顶层 metrics 视为冗余而清理**——会破坏 reflect 全局视图
- reflect skill 通过主仓 `.harness/metrics/*-metrics.json` glob 聚合所有历史（worktree 的 metrics 在 ship 阶段合回主仓后才进入 reflect 视野）
- 单个 scorer 也通过 `ls -t .harness/metrics/*-metrics.json | head -1` 取最近一次结果

**State 写入约定**：
- 单 change 档案：`.harness/changes/<change_id>/state.yaml`（worktree 路径下即 worktree 内的同名目录）
- audit 完成后写入 `audit.*` 段（`constitution_valid` / `overall_score` / `scorer_results` / `blocked`）
读取 `.harness/workflow.yaml: active_changes`，筛选 `phase=audit` 的 entry：
- **唯一匹配**：取其 `change_id`
- **多个匹配**：用 `ask_followup_question` 让用户选择
- **零匹配**：阻断，提示"未找到 design 阶段的 active change，请先执行 /ezfl:design"

## Step 1: Constitution Compliance Audit（注入点 D）

脚本驻留 plugin 内部，由 `.harness/.cache/.plugin_root`（SessionStart 写入）定位；若缺失或脚本不可执行，提示用户重启会话以触发重新写入。

```bash
PLUGIN_ROOT="$(cat .harness/.cache/.plugin_root)"
bash "$PLUGIN_ROOT/hooks/constitution-validity.sh"   # 0=有效 / 1=无效 / 2=不存在
```

判定后续：
- 有效：逐条核对 Core Principle —— NON-NEGOTIABLE 违规为 Critical，其余为 Important，有违规则停等用户三选项
- 无效：按 `constitution_required` 配置决定告警或阻断


## Step 2: Scorer 评分

5 个 scorer 脚本同样驻留 plugin 内（`$PLUGIN_ROOT/scorers/`），每个输出 0-100 分 + 理由：

```bash
PLUGIN_ROOT="$(cat .harness/.cache/.plugin_root)"
for s in audit-violation-rate constitution-violation-count test-coverage-scorer complexity-scorer doc-sync-scorer; do
  bash "$PLUGIN_ROOT/scorers/$s.sh"
done
```

每个脚本 stdout 输出一行 JSON：`{"scorer":"<name>","score":<0-100>,"reason":"<text>"}`。

**聚合写入约定**：
- 目录：`mkdir -p .harness/metrics`
- 文件：`.harness/metrics/<timestamp>-metrics.json`（`<timestamp>` 用 `date -u +%Y%m%d-%H%M%S`）
- `change_id` 取自 `hooks/change-locate.sh` 单匹配结果(与 SKILL.md "State 写入约定"节共享解析逻辑);若解析失败(如 trivial 路径无 entry)则填 `""`,reflect 按"未归因"分桶
- `overall_score` **加权聚合**(见下方"Overall Score 加权聚合")
- 单文件结构（数组形式，便于 reflect 直接遍历；同时保留 `audit` 嵌套段供 `audit-violation-rate.sh` 下次复用）：

```json
{
  "timestamp": "20260525-074800",
  "change_id": "refactor-sdk-api-0701c0",
  "mode": "solo",
  "audit": {
    "violations": 0,
    "total_checks": 12
  },
  "overall_score": 90,
  "scorers": [
    {"scorer":"audit-violation-rate","score":100,"reason":"无已知违规"},
    {"scorer":"constitution-violation-count","score":100,"reason":"..."},
    {"scorer":"test-coverage","score":85,"reason":"行覆盖 85% (source=istanbul:coverage/coverage-summary.json)"},
    {"scorer":"complexity","score":78,"reason":"..."},
    {"scorer":"doc-sync","score":92,"reason":"..."}
  ]
}
```

> `audit.violations` = Step 1 中累计的 Critical+Important 违规条数；`audit.total_checks` = 该次 audit 共核对的 Core Principle + 子检查项总数（无明确分母时填 1）。`audit-violation-rate.sh` 读取最新一次 metrics 计算违规率。

> **不要写到** `.harness/metrics.json`（单文件形式）—— 那会破坏 scorer/reflect 的"按时间戳叠加历史"语义。

## Overall Score 加权聚合

5 个 scorer 的 score 通过加权平均聚合为 `overall_score`,用于 `thresholds.solo.warn_below` / `thresholds.team.block_below` 的阈值判定,同时写入 `metrics JSON` 顶层与 `state.yaml: audit.overall_score`。

**公式**:

```
overall_score = round( Σ(score_i × w_i) / Σ(w_i) )
```

其中 `w_i` 取自 `.harness/harness.toml: [scorer.weights]` 中对应 scorer 名的值;**未配置 / 缺失 / 整个 [scorer.weights] 段不存在** → 全部默认 `1.0`(等权平均,与本特性引入前的行为完全一致)。

**特殊语义**:
- `w_i = 0` → 该 scorer 完全排除出 overall_score(其 score 仍写入 `scorers[]` 供溯源,但不参与计算)
- `Σ(w_i) = 0`(理论极端:所有权重为 0)→ overall_score 取 0,reason 提示"所有 scorer 权重为 0"
- 权重为负数 → 视为配置错误,该项按 1.0 处理并 stderr 警告

**降权常见用法**:`test-coverage` 在未接入标准覆盖率报告(lcov/cobertura/Istanbul JSON)时启发式估算不准,可降到 `0.3` 减少其对 overall_score 的影响。详见 `scorers/README.md`。

## Mode 分发

- solo：低分（< `thresholds.solo.warn_below`）仅告警
- team：低分（< `thresholds.team.block_below`）阻塞，需 override

## Policy

| Policy | 文件 | 作用 |
|--------|------|------|
| Constitution Audit | `./policies/constitution-audit.md` | 详细审计规则 |
