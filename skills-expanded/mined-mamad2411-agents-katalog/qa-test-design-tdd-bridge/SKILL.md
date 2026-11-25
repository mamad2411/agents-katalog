---
name: qa-test-design-tdd-bridge
version: 1.0.0
status: stable
created_date: 2026-05-24
allowed-tools: Read, Bash, Grep, Glob
parent: enterprise-qa-testing
references_agents: [tdd-guide]
description: >-
  QA bridge skill - translates QA risk analysis into TDD inputs (scenario matrix from equivalence partitioning, boundary, decision table, state transition, error guessing, property-based) and validates returned evidence. Red-green-refactor belongs to the `tdd-guide` agent; mutation scoring to `qa-mutation-effectiveness`.
---

# qa-test-design-tdd-bridge

## 1. Position

Unit/TDD layer reference adapter。本 skill **不**替代 `tdd-guide` agent；它的工作：
- 把 parent 风险 + module 信息**翻译成**对 `tdd-guide` 的输入（scenario matrix + edge cases + forbidden patterns）
- **验收** `tdd-guide` 返回的测试文件 + stdout + scenario 覆盖
- 防止 implementation-detail tests / fake-mock tests / snapshot-only assertions 等假测试

## 2. Triggers

- Parent `enterprise-qa-testing` §6 Step 5/6（默认 dispatch）
- Risk score ≥ Medium + 逻辑变更
- 新增 utility / Server Action / Zod schema / repository / domain logic
- Bug fix（regression test 先写）

## 3. Responsibilities

- **Scenario matrix design**（基于 8 类测试设计技术）：
  - **Equivalence partitioning**：等价类划分
  - **Boundary value analysis**：边界 ± 1
  - **Decision table**：条件组合
  - **State transition**：状态机
  - **Error guessing**：经验性边角
  - **Regression case extraction**：从 bug 中提
  - **Property-based testing**：fast-check（输入域随机采样）
  - **Mutation testing sampling**：Stryker（验证测试是否足够严）
- **Forbidden patterns enumeration**：implementation-detail / snapshot-only / fake-mock / 测试没断言
- **Input package** for `tdd-guide`：target_module / changed_behavior / public_api / risk_level / scenario_matrix / edge_cases / forbidden_patterns
- **Evidence validation**：是否真有测试文件改动 / 是否有 stdout / 是否覆盖 scenario matrix / 是否没有假测试

### 3.1 ISTQB 黑盒测试设计技术 checklist（每条 = 一种 scenario 生成法）

> ADDITIVE 文档增强。把 §3 的技术名展开成"对每个待测 module 怎么落 scenario"的可勾选 checklist。按 risk_level 选 4-8 类（Low/Medium 选前 4 类即可；High/Critical 应覆盖 5 类以上含状态转换 + pairwise）。这些是 **scenario 设计输入**，真正的 red-green-refactor 仍由 `tdd-guide` 跑。

- [ ] **等价类划分 Equivalence Partitioning**：把输入域切成"行为等价"的分区，每区**至少取 1 个代表值**——valid 分区 + 每个 invalid 分区各一。例：年龄字段 `[<0 非法] [0-17 未成年] [18-120 成年] [>120 非法]` → 4 个代表值，而非穷举。目的：用最少用例覆盖最多行为类。
- [ ] **边界值分析 Boundary Value Analysis**：在每个等价类**边界 ± 1**取值——经典 2-value（boundary, boundary±1）或 3-value（boundary-1, boundary, boundary+1）。例：分区边界 18 → 测 17 / 18 / 19。补 off-by-one / 闭开区间错误。**通常与等价类配对使用**（先分区，再在每区边界加测）。
- [ ] **判定表 Decision Table**：当输出由**多个条件组合**决定时，列条件 × 动作矩阵，每条规则（条件组合）一个用例。例：`isLoggedIn × hasSubscription × isTrial → canAccess` 共 2³=8 条规则（可用规则合并裁掉不可达组合）。目的：防"条件交互"漏测（单测每个条件 true/false 不等于测了组合）。
- [ ] **状态转换 State Transition**：当对象有状态机时，画 state → event → next-state 表，覆盖**每个合法转换** + **关键非法转换**（在错误状态触发事件应被拒）。例：订单 `created → paid → shipped → delivered`，测合法链 + "未支付直接 ship 应失败"。覆盖准则可标 0-switch（每转换至少一次）/ 1-switch（每对连续转换）。
- [ ] **Pairwise / 组合测试 Pairwise (all-pairs)**：当多个独立参数各有多取值、全组合爆炸时，用 pairwise 只保证**任意两参数的每对取值组合至少出现一次**（基于"多数缺陷由 ≤2 参数交互触发"的经验）。例：3 参数各 3 值 = 27 全组合 → pairwise 约 9-11 例。工具：`allpairspy` / `PICT` / `fast-check` 的组合采样。**仅在参数维度高时用**，低维直接判定表全覆盖。
- [ ] **错误猜测 Error Guessing**：基于经验补常见易错点——null / empty / 超长 / 0 / 负数 / Unicode / 前后空格 / 重复提交 / 并发 / locale / timezone / 大小写。无系统性，是前 5 类的补充网。
- [ ] **回归用例提取 Regression**：从历史 bug / 本次 fix 反推——每个修过的缺陷应有一条"会复现它"的测试（与 parent §9 Goal-Driven：先写失败测试再修）。
- [ ] **Property-based / Mutation（可选，工具就绪时）**：`fast-check` 做属性测试（输入域随机采样验证不变量）；`Stryker` 做变异采样（验证测试是否足够严，mutation score 反映"测试能不能抓到被注入的 bug"）。属高阶补强，非每个 module 必做。

**落 scenario_matrix 时**：每条 scenario 标注它来自哪类技术（便于 §"Evidence validation" 反查覆盖完整性），并确保**negative / boundary 占比不为 0**（纯 happy-path 违反 §8 Forbidden patterns）。

### 3.2 Property-based / generative testing 实务要点（fast-check / Hypothesis — Q5 扩展）

> ADDITIVE 能力扩展（CAPABILITY-UPGRADE Wave A, Q5）。§3.1 是 **example-based**（你想出代表值、边界、组合 —— 受限于你想得到什么）。Property-based 反过来：**你声明一条对所有输入都该成立的不变量（property），框架自动生成成百上千随机输入去试图证伪它**，专抓"你没想到的输入"。两者互补，不替代：example 测已知关键场景，property 探输入域。

**核心心智 — 从"举例"到"声明不变量"**：

- example-based：`expect(reverse([1,2,3])).toEqual([3,2,1])`（一个例子）。
- property-based：`∀ arr: reverse(reverse(arr)) === arr`（一条对所有数组成立的性质）。框架随机生成 `arr`（空、单元素、超长、含重复、含特殊值）来反驳它。
- 失败时**自动 shrink**：框架把触发失败的随机输入**收缩到最小反例**（如 1000 元素数组 → 报"`[0, 0]` 就挂了"），直接定位根因。

**常见 property 套路（适用核心逻辑 / 算法 / 序列化 / 状态机）**：

- **Round-trip / 往返**：`decode(encode(x)) === x`（序列化、parse/format、压缩、编解码）。最高价值套路之一。
- **Invariant / 不变量**：操作前后某性质恒定（排序后长度不变且元素是原集合的排列；账户转账前后总额守恒）。
- **Idempotence / 幂等**：`f(f(x)) === f(x)`（normalize、dedupe、saturating 操作）。
- **Oracle / 对照**：新实现 vs 已知正确的慢实现（或旧实现）结果一致（重构 / 优化的护栏）。
- **Metamorphic / 蜕变**：输入变换 → 输出可预测变换（`f(x) ≤ f(x ∪ y)` 单调性；加价后总额不减）。
- **Commutative / 顺序无关**：`merge(a,b) === merge(b,a)`。

**工具与落法**：

| 语言 | 工具 | 关键用法 |
|---|---|---|
| JS / TS | **fast-check**（`fc.assert(fc.property(arbitraries, predicate))`） | 用 `fc.integer/string/array/record/oneof` 等 arbitrary 描述输入域；失败自动 shrink；`fc.assert(..., { numRuns: 1000 })` 控样本量；可 `fc.pre()` 过滤前置条件；与 Vitest/Jest 直接组合 |
| Python | **Hypothesis**（`@given(strategies)`） | `@given(st.lists(st.integers()))` 声明输入策略；`@example(...)` 钉住已知关键 case；`assume(...)` 过滤；shrink 内置；与 pytest 直接组合 |

> **Caveat（来自 research 4-qa.md）**：Hypothesis（Python）/ proptest（Rust）在本轮 deep-research 中是 **推荐但未逐一核验**。落地 Python 项目时按官方 quick-start 复查 API（strategies 名、`@settings` 参数）；Rust 核心逻辑可用 `proptest` 或 `quickcheck`，用前确认 crate 当前 API。fast-check（JS/TS）+ Schemathesis（API，见 `qa-contract-api` §3.3）是本轮已核验的主路径。

**与 §3.1 的关系（按 risk_level 叠加，不是二选一）**：

- Low / Medium：example-based（§3.1 前 4 类）通常足够；property 可选。
- **High / Critical 且逻辑密集**（算法 / 计费 / 风控 / 编解码 / 状态机 / 并发安全的纯逻辑）：**应叠加 ≥1 条 property**，尤其 round-trip / invariant / oracle —— 这是 example-based 难以穷举的地方。
- property test 的**断言仍是行为断言**，不是 implementation-detail（仍受 §8 Forbidden patterns 约束 —— 不许断言私有调用次数）。

**落 scenario_matrix / tdd_reference_input 时**：property 作为一类 technique（`property_based`）写进 `techniques_applied`，每条 property 记 `{property_name, invariant, arbitraries, tool}`；执行仍由 `tdd-guide` 跑（red-green-refactor），本 skill 验收返回证据里 property 是否真跑（有 `numRuns` / 样本数 stdout）、是否 shrink 出反例、不变量是否真被检验。

## 4. Non-responsibilities

- 不实施 TDD red-green-refactor（由 `tdd-guide`）
- 不写实现代码（由 `tdd-guide` 或开发者）
- 不替代 code review（由 `code-reviewer`）
- 不做 E2E / Component / Integration（其他 child skill）

## 5. Workflow

1. **Pull from parent**：target module / public API / changed behavior / risk_level
2. **Apply test design techniques**：按 risk_level 选 4-8 类技术
3. **Build scenario_matrix**：每条 scenario {input / expected / risk_reason}
4. **List edge_cases**：边界、null、empty、very-large、locale、timezone
5. **Specify forbidden_patterns**：列出本次必须避免的反模式
6. **Property-based**（§3.2，High/Critical 逻辑密集时应叠加 ≥1 条不变量 via fast-check / Hypothesis）/ **mutation effectiveness**（高危模块测试有效性 → 独立 skill `qa-mutation-effectiveness`，不在本 skill 内跑全量）
7. **Output input package**（见 §6）
8. **Receive evidence** from `tdd-guide`
9. **Validate**：测试文件存在? stdout 真实? scenario 全覆盖? 无假测试?
10. **Output `test_design_tdd_bridge` YAML**

## 6. Output Contract

```yaml
test_design_tdd_bridge:
  reference_agent: tdd-guide
  tdd_reference_input:
    target_module: <e.g. src/lib/permissions.ts>
    changed_behavior: <e.g. canPurchase predicate flipped from allowlist to negative>
    public_api: <e.g. getTenantPermissions(userId, tenantId)>
    risk_level: medium | high | critical
    techniques_applied:
      - equivalence_partitioning
      - boundary_value
      - decision_table
      - state_transition
      - pairwise            # all-pairs combinatorial; if high param dimensionality (§3.1)
      - error_guessing
      - regression
      - property_based  # if fast-check (JS/TS) / Hypothesis (Py) available — §3.2
      - mutation_sampling  # NOTE: full mutation effectiveness is its own skill `qa-mutation-effectiveness`
    property_specs:           # §3.2 — populated when property_based applied
      - property_name: reverse_round_trip
        invariant: "reverse(reverse(arr)) === arr"
        arbitraries: "fc.array(fc.integer())"
        tool: fast-check | hypothesis | proptest
        kind: round_trip | invariant | idempotence | oracle | metamorphic | commutative
    scenario_matrix:
      - scenario: <name>
        input: { ... }
        expected: ...
        risk_reason: <why this matters>
    edge_cases:
      - null_input
      - empty_string
      - very_large_input
      - locale_variation
      - timezone_variation
    forbidden_patterns:
      - implementation_detail_assertion
      - snapshot_only_assertion
      - fake_test_without_assertion
      - mock_internal_module_under_test
      - test_that_never_fails
  validation_of_returned_evidence:
    test_files_changed: [paths]
    commands_actually_ran: true | false
    stdout_present: true | false
    scenario_coverage:
      total: <N>
      covered: <M>
      uncovered: [scenarios]
    forbidden_pattern_violations: []
    mutation_score: <optional — see qa-mutation-effectiveness for the real measurement>
    property_testing_evidence:        # §3.2 — validate property tests actually ran
      properties_run: <N>
      num_runs_per_property: <e.g. 1000>     # fast-check numRuns / Hypothesis samples
      counterexamples_found: []              # each shrunk minimal repro, if any
      shrinking_observed: true | false
  decision: PASS | FAIL | BLOCKED
  blockers: []
```

## 7. Parent Integration

- **Triggered by**：parent §6 Step 5/6
- **Returns**：`test_design_tdd_bridge` YAML
- **Consumed by**：`qa-evidence-bundle` → `child_skill_results.test_design`

## 8. Forbidden patterns

- 接受 `tdd-guide` 输出"测试已加"但无 stdout 证明
- scenario matrix 仅覆盖 happy path（必须含 negative / boundary）
- 接受 implementation-detail tests（如 spy on private function call count）
- 接受 mock 内部模块测自己（违反 Hard Rule §2.4）
- 接受 snapshot-only assertion（snapshot 必须配合行为 assertion）
- 声称跑了 property test 但无样本量证据（`numRuns` / Hypothesis samples stdout）—— property test 不跑足够样本等于没测（违反 parent §2.1 no-evidence）
- property 的不变量写成 tautology（如 `expect(x).toBe(x)` 或永真断言）—— 假 property，永不失败（与 "test_that_never_fails" 同源）
- 用 property test 断言 implementation detail（私有调用次数等）—— property 仍受行为断言约束

## 9. References

- [fast-check — property-based testing for JS/TS](https://fast-check.dev/) · [arbitraries](https://fast-check.dev/docs/core-blocks/arbitraries/) · [shrinking & numRuns](https://fast-check.dev/docs/configuration/)
- [Hypothesis — property-based testing for Python](https://hypothesis.readthedocs.io/) · [strategies](https://hypothesis.readthedocs.io/en/latest/data.html) · [`@given`/`@example`](https://hypothesis.readthedocs.io/en/latest/details.html) (推荐但本轮未逐一核验 — 用前复查 API)
- [proptest (Rust)](https://docs.rs/proptest/) / [quickcheck (Rust)](https://docs.rs/quickcheck/) (核心逻辑 property；用前确认 crate API)
- [StrykerJS — mutation testing](https://stryker-mutator.io/) (full mutation effectiveness → skill `qa-mutation-effectiveness`)
- [ISTQB CTFL — test design techniques](https://glossary.istqb.org/en_US/term/test-design-technique/2)
- [Black-box techniques: equivalence partitioning / boundary value / decision table / state transition](https://glossary.istqb.org/en_US/term/black-box-test-technique)
- [Microsoft PICT — pairwise/combinatorial test generation](https://github.com/microsoft/pict) · [allpairspy](https://pypi.org/project/allpairspy/)
- [Testing Library — guiding principles](https://testing-library.com/docs/guiding-principles/)
