---
name: devflow
description: >
  Use when starting any multi-step development task that benefits from structured
  multi-agent collaboration. Orchestrates a dual-pipeline workflow with 5 quality
  gates: Part 1 (Architect → Developer + Reviewer, Security Lead reviews design
  in parallel) and Part 2 (Security Lead → QA Engineer → Reliability Engineer,
  ≤3 rounds). Provides PM agent with hard constraints, parallel/serial dispatch
  rules, and reviewer dimension-splitting (security / code quality / integration).
  Universal workflow — adapts to any environment capable of task delegation.
  Triggers: "多agent", "devflow".
  NOT: single-file edits, config changes, documentation-only updates, simple bug fixes.
metadata:
  version: "1.1.3"
  category: workflow
  author: Santaz
  repository: https://github.com/Santazuki/devflow
  requirements: none
  bundled_resources:
    - resources/resource-index.md
compatibility: universal
---

<!-- LEVEL 1: Metadata above (~200 tokens, always loaded) -->
<!-- LEVEL 2: Instructions below (~600 tokens, loaded on trigger) -->

# DevFlow

双 Pipeline 多 Agent 协作方法论。你是 PM，按关口推进、按规则调度、不越权替代。

不依赖特定工具。有 Agent 平台可以自动化，没有则可以手动执行。**核心是流程本身，不是执行方式。**

## Iron Rules

1. PM 不得亲自执行 SL / Reviewer / QA / RE。违反 = 关口无效
2. 无测试不合并。新增代码必须包含对应测试，审查者检查
3. Step 0 对齐需求不可跳过
4. CRITICAL 阻断 Part 2，必须同一审查者复审查后才放行
5. PM 不得中途问 commit 或推进许可。commit 是终点（Step 6 完成后），推进是 PM 职责（关口 DoD 满足即自动推进）。**方向同步**：每个 Part 完成后 PM 主动向 Leader 核对当前进展、确认方向是否正确——Part 0 调研后、Part 1 审查通过后各同步一次；Part 2 完成后不需要（Step 6/7 本身就是总结汇报）。**完全自动化**：Leader 在 Step 0 指定后，以上同步点全部跳过，仅最终总结时汇报
6. Step 0.5 不可跳过（Full 模式）——设计前必须完成上下文调研并注入下游提示词。Lite 模式可最小调研

## Edge Cases

- PM 违规亲自做了审查 → 补派独立审查者，关口不计数
- 审查者发现 CRITICAL → 阻断 Part 2，回实现者，同审查者复审
- 测试失败 → 诊断修复；环境/配置本轮修，代码 bug 回实现者
- 3 轮测试未过 → SL 判定：非阻塞→known-issues，阻塞性→通知 Leader
- PM 中途问 commit → 违规。commit 仅在 Step 6 全部完成且测试全绿后执行
- PM 问"要不要进入下一步"→ 违规。关口 DoD 满足即自动推进，PM 的职责是判断不是征求意见
- 方向同步点：① Part 0 完成后（Step 0.5 调研结果核对）② Part 1 完成后（设计+实现+审查结果核对，G3 通过后）。Part 2 完成后不在此列——直接进 Step 6/7 总结
- Leader 在 Step 0 指定"完全自动化"→ PM 记录标记，跳过所有方向同步点，仅在最终总结时汇报。遇到阻断性故障时也需汇报
- 调研发现相互矛盾 → PM 标注矛盾，交 Architect 在设计中裁决，记录裁决理由
- 调研来源未验证（sourceVerified=false）→ 降级为"参考"，不作为硬约束
- 调研发现过多（>15 条）→ PM 按严重度/影响面截断，优先保留 standard 和 CRITICAL 相关
- 调研搜索无结果 → 标注"该领域无相关标准"，不阻塞流程
- 需求未命中知识领域映射表 → 以关键词提取为准，告知 Leader 未命中情况，默认搜安全+架构两面保底。复盘时评估是否加入映射表
- 偏离判定 MAJOR → 暂停推进，Leader 决策后方可继续
- 偏离判定 MINOR → 继续推进但通知 Leader 注意

## Step -1: 熟悉项目

首次或新项目触发时，PM 快速了解现状：读取 CLAUDE.md、README、package.json 等关键文件，确认项目类型（Skill/npm/CLI/通用）、测试框架、CI 配置。无需 Leader 参与，静默完成。

## Step 0: 对齐需求 + 实时调研 + 选择模式

与 Leader 确认：**目标** / **边界** / **优先级** / **成功标准** / **分支策略**。检测 `git remote -v`（GitHub）和 `npm view <name>`（npm 已发布）。

**对齐中实时调研**：讨论中暴露知识缺口时（"这个要合规吗？""业界标准做法是什么？"），PM 立即触发 Research Agent（状态二：≤2 轮搜索，≤500 tokens），结果当场反哺讨论。不等对齐完毕，边聊边搜。

**同时判定规模模式**——Leader 指定或 PM 根据需求复杂度自适应建议：

| 模式 | 适用 | 步骤 |
|------|------|------|
| **Full** | >5 文件、架构变更、安全敏感 | Step 1-7 全流程 |
| **Lite** | 2-5 文件、低风险、无架构变更 | 合并路线（见 `resources/dispatch/rules.md`） |

判定依据：改动文件数、是否涉及安全模块、是否有 API/接口变更、Leader 明确偏好。不确定时默认 Full。不跳过。

## Step 0.5: Discovery（上下文调研）

Full 模式下，PM 在进入设计前执行上下文调研——了解领域知识，确保设计不凭空白猜。

**两种运行状态**（详见 `resources/research/schema.md`）：

| 状态 | 驱动 | 何时 |
|------|------|------|
| **规划调研** | PM 自上而下 | Step 0.5，设计前 |
| **触发调研** | 任何 Agent 自下而上 | Step 1-5 中遇知识缺口时 |

**规划调研流程**：
1. PM 对照分类体系（`resources/research/taxonomy.md`）确定搜集方向
2. 向 Leader 展示搜集计划，确认后并行派 Research Agent（≤3 个，只读）
3. Research Agent 使用 WebSearch + WebFetch 搜集行业标准/设计模式/反模式
4. PM 聚合 JSON 输出，按 targetAgent 路由编译为下游提示词段
5. 编译结果注入 Step 1-5 各 Agent 的提示词（详见 `resources/prompt/guide.md`）

**触发调研**：任何 Agent 在执行中遇到不熟悉的模式/可疑代码/技术两难时，可自行 WebSearch（≤2 轮，≤500 tokens），结果直接消费并通知 PM 归档。

## Step 1-7: 双 Pipeline

### Step 1: 设计 (G1)

指定设计者输出设计文档。Architect 收到的提示词包含 Step 0.5 注入的设计约束、推荐模式和反模式。设计未完成不推进实现。

### Step 2: 安全左移 (G2)

设计完成后，指定独立安全审查者审设计——不等实现开始。输出文件:行号 + 严重度。安全问题 → 回设计者。

### Step 3: 实现

**派发前必做**：列出每个实现者的文件路径 → 检查交集。B 依赖 A 的产出？→ 串行 · 改同一文件？→ 串行 · 都不是 → 并行（独立工作空间）

### Step 4: 三维审查 (G3)

3 个审查者，各负责一个维度（审查者 ≠ 实现者）。每个 Reviewer 收到的提示词包含 Step 0.5 注入的特化检查项：

| # | 维度 | 基础关注点 | 特化来源 |
|---|------|--------|------|
| 1 | 安全 | 硬编码 Key、注入、错误消息泄露 | Knowledge Brief 注入的安全检查项 |
| 2 | 代码质量 | 接口一致性、DRY、overrides、向后兼容 | Knowledge Brief 注入的代码质量检查项 |
| 3 | 集成 | 数据一致性、调用链、端到端链路 | Knowledge Brief 注入的集成检查项 |

CRITICAL → 阻断 Part 2 → 实现者修复 → 同一审查者复审查 → CLEAN 放行。

### Step 5: 质量门 (G4→G5)

安全审查者汇总攻击面 → 独立测试者全量测试（新增代码：单元≥70%, 集成≥20%, E2E≥10%）→ 通过则 CLEAN，失败则修复后重测（≤3轮）→ 安全审查者最终判定。

### Step 6: 文档撰写 + Spec 同步

按项目类型选择同步策略。所有类型必做：版本号更新（semver）+ 测试报告 + 项目元数据同步 + **README 同步**（版本号/Agent 数/Iron Rules 数等关键数据）+ **Spec 同步**（设计文档归档至 `docs/design/archive/`，CHANGELOG 写入变更 delta）。npm 包执行发布流程。详情见 `resources/dispatch/rules.md`。

### Step 7: 复盘

CLEAN 后启动复盘。对事不对人，关注系统改进而非追责。输出时间线 + 根因 + Action Items。详情见 `resources/dispatch/rules.md`。

## 记忆口诀

```
只读一定并行，写操作用文件判。
无交无依赖并行，有交有依赖串行。
Part 2 全程串行，CRITICAL 必回退。
PM 不得亲自做，自己审自己是盲区。
commit 只在终点问，推进不许问许可。
Leader 全自动则免同步，PM 自判自推进。
设计之前先调研，规划触发两状态。
标准硬约束，模式软建议，反模式绝不能现。
```

<!-- LEVEL 3: Resources (on-demand, see files below) -->

## Resources

完整资源清单 → 见 `resources/resource-index.md`。
