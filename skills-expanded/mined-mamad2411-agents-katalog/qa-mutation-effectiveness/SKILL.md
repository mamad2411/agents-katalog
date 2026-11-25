---
name: qa-mutation-effectiveness
version: 1.0.0
status: stable
created_date: 2026-06-15
allowed-tools: Read, Bash, Grep, Glob
parent: enterprise-qa-testing
references_agents: [qa-mutation-runner]
description: >-
  QA child skill - mutation testing for TEST-SUITE effectiveness: whether the existing suite catches injected bugs (mutation score), not whether the code works. StrykerJS (`thresholds.break`) / cargo-mutants (`--in-diff`) / mutmut / PIT, scoped to the diff of HIGH and CRITICAL modules for cost. Owns parent Mutation/Test-Effectiveness layer.
---

# qa-mutation-effectiveness

## 1. Position

测**测试套件够不够严**的 skill，不是测代码对不对。心智区别（关键）：

- **Code coverage** 回答："这行代码被某个测试**执行**过吗？" —— 但执行 ≠ 验证。一个没有断言的测试能跑满 100% 覆盖率却抓不到任何 bug。
- **Mutation score** 回答："如果我往代码里**注入一个 bug**（mutant），现有测试**会不会失败**？" —— 这是测试**有效性**的直接度量。注入的 bug 被测试杀掉（killed）= 好；存活（survived）= 测试有洞。

`qa-test-design-tdd-bridge` §3 只把 mutation 列为"可选项一句话"；本 skill 把它落成**真能跑、带阈值 gate、带成本控制**的能力。

**成本控制是第一性约束**：mutation testing 会对每个 mutant 重跑测试套件，朴素全量跑极慢（O(mutants × test-suite-time)）。因此本 skill **只测 High/Critical 风险模块的 diff**——`cargo-mutants --in-diff` / Stryker 的 `mutate` glob 限定 + `--since` / `--incremental` / mutmut 的 `paths_to_mutate` 收窄。绝不无脑全仓跑。

## 2. Triggers

- Parent §6 Step 5（risk = High/Critical 且涉及**逻辑密集 / 高危**模块 —— 权限判定、计费计算、状态机、加解密、风控规则、数据一致性逻辑）
- "我的测试到底够不够好 / 能不能信"（测试质量怀疑）
- 关键模块新增 / 重写后，想验证新写的测试不是摆设
- CI 想加一道 mutation-score gate（高危模块测试有效性回归）
- 独立触发：test-suite 质量审计 / 季度测试健康度 review

## 3. Responsibilities

- **按语言选工具**（auto-discover stack）：
  | 语言 | 工具 | PR-scoped / 增量手段 | gate 机制 |
  |---|---|---|---|
  | JS / TS | **StrykerJS** (`@stryker-mutator/core`) | `mutate: [globs]` 限高危文件 + `--since <ref>` + `incremental: true`（`.stryker-tmp/incremental.json`） | `thresholds.break: <N>` → score < break ⇒ **exit 1**（build fail） |
  | Rust | **cargo-mutants** | `--in-diff <diff-file>`（只测 PR diff 的 mutant）+ `--file <glob>` | exit non-zero on surviving/`--minimum-test-timeout`; CI fails on missed mutants |
  | Python | **mutmut** | `paths_to_mutate` 收窄 + `--since`(via VCS) | `mutmut results` → surviving 数 → gate |
  | Java/JVM | **PIT / pitest** | `targetClasses` + `targetTests` + `--changedClasses`/`scmMutationCoverage` | `mutationThreshold` → build fail |
- **Mutation score 阈值 gate**：`score = killed / (killed + survived)`（通常排除 `no-coverage` / `timeout` / `equivalent` 视工具语义）。score < 阈值 → FAIL。阈值按模块风险设（High ≥ 70%、Critical ≥ 80% 为建议起点，项目可调严，**不允许为 pass 调松** — Hard Rule §2.7）。
  > **分母口径 — 务必对齐（防误读）**：本 skill 的 gate 公式 `killed / (killed + survived)` **排除 `no-coverage`**，而 StrykerJS clear-text 报的 **"Mutation score total" 把 `no-coverage` 计入分母**，两数会不同（E2E 实测：skill 公式 73.91% vs Stryker total 68.00%，差额来自 2 个 no-coverage mutant）。报告与 gate 一律以 **skill 公式（排 no-coverage）为准**；若直接用 Stryker `thresholds.break` 把关，须知道它默认对哪个分母（Stryker 另有 `mutationScore` vs `mutationScoreBasedOnCoveredCode` 两个口径），并在配置里显式选定 covered-code 口径，避免 no-coverage 把 gate 拖低或拖高。**no-coverage 高 = 该补 coverage（见 §反模式），不是把它混进有效性分母。**
- **Surviving mutant 分析**：列出存活 mutant（哪个文件、哪行、什么变异：条件取反 / 边界 ± / 返回值替换 / 算术符替换 / 移除语句），每个存活 mutant = 一条"测试该补但没补"的线索。
- **区分 survived vs equivalent**：equivalent mutant（语义等价、无法被任何测试杀死，如 `a*1` → `a`）不算测试缺陷，应标注排除；不能把 equivalent 误判为测试洞而强行加测试。
- **成本预算**：报告 mutant 总数 / 已测 / 跳过 + wall-clock；超预算时收窄 scope（仅 diff、仅最高危文件）而不是降阈值。

### 3.1 为什么 `--in-diff` / 增量是刚需

朴素 mutation 全跑：1000 个 mutant × 套件 30s = 8+ 小时，CI 不可接受。PR 实务做法：

- **cargo-mutants `--in-diff <patch>`**：只对本次 diff 触碰的代码行生成 mutant —— 把成本从"全仓"压到"本次改动"，最适合 PR gate（官方推荐用法）。
- **StrykerJS `--since <branch>`** + `incremental`：只 mutate 自 baseline 以来变化的文件，并复用上次结果缓存未变部分。
- **PIT `scmMutationCoverage` / `--changedClasses`**：基于 SCM 只测改动类。

本 skill 默认走增量/diff 模式；全量 mutation 仅在显式"全模块审计"任务且预算允许时跑。

## 4. Non-responsibilities

- 不测代码功能正确性（那是 unit/integration/E2E 层的事 —— mutation 假设"测试已存在"，它测的是这些测试好不好）
- 不写新测试（发现 surviving mutant 后，补测试由 `qa-test-design-tdd-bridge` → `tdd-guide` 做；本 skill 只产"该补哪些"的清单）
- 不替代 coverage（coverage 是 mutation 的前置过滤 —— 0 覆盖的代码连 mutant 都跑不起来；两者互补不替代）
- 不做性能 / 负载（→ `qa-performance-reliability` / `qa-load-stress-reliability`）
- 不对全仓无差别跑（成本失控；见 §3.1）

## 5. Workflow

1. Auto-discover stack（package.json / Cargo.toml / pyproject / pom.xml|build.gradle）→ 选工具
2. 从 parent 拿 risk_level + changed_files → 圈定**仅 High/Critical 模块**为 mutation target
3. 算 diff（`git diff <base>...HEAD`）→ 准备 `--in-diff` / `--since` / `mutate` glob
4. 设 mutation-score 阈值（按模块风险，来源：现有配置 / 风险档默认；不允许临时调松）
5. dispatch `qa-mutation-runner`（它跑工具、抓 score / surviving mutants / mutant 计数 / wall-clock + exit_code）
6. 验收 `MUTATION_SCHEMA`：score 是否真实算出、阈值 gate 是否真触发、surviving 是否列清、equivalent 是否区分、是否走了增量（没爆预算）
7. Output `mutation_effectiveness` YAML

## 6. Output Contract

```yaml
mutation_effectiveness:
  language: js | ts | rust | python | java | mixed
  tool: stryker | cargo-mutants | mutmut | pit
  scope:
    mode: in-diff | since-ref | full-module   # 默认非 full
    diff_base: <git ref>
    mutated_paths: [src/lib/billing.ts, src/lib/permissions.ts]  # 仅高危
    risk_level_gate: high | critical
  mutants:
    total_generated: <N>
    killed: <N>
    survived: <N>
    timeout: <N>
    no_coverage: <N>
    equivalent_excluded: <N>          # 标注为等价、排除出分母
  mutation_score:
    score_pct: <N>                    # killed / (killed + survived) per tool semantics
    threshold_pct: 80
    threshold_met: true | false
  surviving_mutants:                  # 每个 = 一条"测试该补"的线索
    - file: src/lib/billing.ts
      line: 42
      mutation: "conditional boundary: >= → >"
      hint: "no test covers the exact boundary; add boundary-value case"
  cost:
    wall_clock_sec: <N>
    incremental_used: true | false
    over_budget: false
  artifacts:
    report: <path mutation report — stryker html/json | cargo-mutants outdir | mutmut results | pit html>
    stdout_log: <path>
  decision: PASS | FAIL | BLOCKED
  blockers: []
```

## 7. Parent Integration

- Triggered by: parent §6 Step 5（reference agent 模式 — 本 skill prepare input → `qa-mutation-runner` execute → 本 skill validate）
- Returns: `mutation_effectiveness` YAML
- Consumed by: `qa-evidence-bundle` → `child_skill_results.mutation` (evidence layer key: `mutation`)
- Runner emits `MUTATION_SCHEMA.v1`（workflow-spec mode）
- 落盘：`bash "$HOME/.claude/scripts/qa-sdk.sh" evidence.append <tag> mutation <result>` → `.qa/evidence/<tag>/mutation.yaml`
- **下游接力**：surviving_mutants 清单 → `qa-test-design-tdd-bridge`（补测试），不在本 skill 内闭环

## 8. Forbidden patterns

- **无脑全仓跑 mutation**（成本爆炸；必须 `--in-diff` / `--since` / glob 收窄到高危模块）
- 为 pass 调低 mutation-score 阈值或删 mutant 类型（违反 Hard Rule §2.7）
- 把 **code coverage 当 mutation score** 报（两者不是一回事；coverage 高不代表测试有效）
- 把 **equivalent mutant 误判为测试洞** 强加无意义测试（应标注排除）
- 声称 mutation 通过但无 report artifact + stdout（违反 Hard Rule §2.1）
- 对没有测试覆盖的代码跑 mutation 当"测试有效性"结论（全 survived 是因为没测试，不是测试"无效"——应先要求补 coverage）
- superseded：用 mutation score 替代功能测试（它衡量测试质量，不衡量功能正确）

## 9. References

- [StrykerJS — mutation testing for JS/TS](https://stryker-mutator.io/docs/stryker-js/introduction/) · [thresholds.break (build fail)](https://stryker-mutator.io/docs/stryker-js/configuration/#thresholds-object) · [incremental mode](https://stryker-mutator.io/docs/stryker-js/incremental/)
- [cargo-mutants (Rust)](https://mutants.rs/) · [`--in-diff` for PR-scoped mutation](https://mutants.rs/in-diff.html)
- [mutmut — Python mutation testing](https://mutmut.readthedocs.io/)
- [PIT / pitest — JVM mutation testing](https://pitest.org/) · [incremental analysis / SCM](https://pitest.org/quickstart/incremental_analysis/)
- [What is mutation testing (killed vs survived vs equivalent)](https://stryker-mutator.io/docs/) 
- Parent §3 Risk Model (High/Critical gating) · §2.7 No threshold weakening · `qa-test-design-tdd-bridge` §3 (mutation sampling)
