---
name: code-cleanup
description: 代码清理与性能优化 skill —— 识别并清理冗余文件、过时函数、无用逻辑（CL-xx 规则集），并定位高耗时/高内存的文件、函数、逻辑做性能优化（PF-xx 规则集）。以「行为保全优先、先测量后优化」为红线，走「盘点 → 静态扫描 → 分级与确认 → 分批清理/优化 → 验证与沉淀」五阶段；配套可直接运行的 `scripts/cleanup.py`（复用 quality_gate 的 AST 工具、Finding 模型、SQLite 基线与评分）与可注册进 pre-commit 的检测器。当用户要求清理冗余文件、删除死代码、移除过时函数、清理无用逻辑/注释掉的代码/临时文件、精简无用依赖、做全库清理，或要求性能优化、降低内存占用、定位热点函数、分析复杂度、优化慢查询/慢接口/慢列表渲染、减少打包体积时使用。
---

# 代码清理与性能优化（Code Cleanup & Perf Hotspot）

两件事、一套流程：**删掉不该存在的代码**（清理），**让留下来的代码更快更省**（优化）。
两者共用同一套定位基础设施（AST 扫描 + 基线演进 + 报告），因为它们的输入完全相同——
「哪些代码/逻辑值得动」。

## 任务目标

| 目标 | 规则集 | 产出 |
|---|---|---|
| 识别并清理冗余文件、过时函数、无用逻辑 | `CL-01` ~ `CL-10` | 清理行动清单（可删除/可收敛，逐条带位置、理由、指纹） |
| 定位高耗时/高内存的文件、函数、逻辑并优化 | `PF-01` ~ `PF-08` | 性能优化清单（需 profiler 复核的候选 + 具体手段） |

**默认模式 = 全库**；变更集（diff/PR）与定点（指定目录/文件）为轻量分支，复用同一清单与分级。

## 两条不可让渡的红线

1. **行为保全优先**（对齐 [`refactoring-methodology.md`](../../../docs/spec/refactoring-methodology.md)）：没有测试保护网或人工确认，**不得删除任何生产代码**。静态工具只能产出「候选」，删除决策必须由人做出。
2. **先测量后优化**（对齐性能工程通识）：`PF-xx` 命中项全部是**静态候选**，不等于缺陷。未用 `py-spy` / `cProfile` / `tracemalloc` / `EXPLAIN QUERY PLAN` 实测前，不得声称「优化了性能」。

与之配套的第三条约束：**数据零受损**（[`plan-design-principles.md`](../../../docs/spec/plan-design-principles.md) P1/G0）——
清理只作用于代码树；数据落外置数据根，任何脚本不得顺手 `DROP`/`DELETE`/`VACUUM`。

## 评审输入（开始前必须明确）

| 输入要素 | 说明 | 缺省处理 |
|---|---|---|
| 模式 | 全库 / 变更集（base..head）/ 定点（目录、文件） | 用户说「全库清理/整体清理」→ 全库；指定路径 → 定点；给出 diff → 变更集 |
| 范围 | 模块/目录清单 | 全库模式以 `scripts/cleanup/config.py::PYTHON_SCAN_ROOTS` + `frontend/src` 为范围 |
| 清理强度 | 只报告 / 报告+豁免存量 / 报告+执行删除 | 默认**只报告**；用户明确要求「直接清理」时才进入执行分支 |
| 性能目标 | 延迟 / 内存 / 包体积 / 查询耗时 | 未指定时按「先定位后定目标」处理，报告中列候选项供用户挑选 |
| 保护网 | 测试套件与基线是否可用 | 无测试时强制走「特征测试 + 人工确认」路径，禁止直接删改 |

## 工作流总览（五阶段）

| 阶段 | 动作 | 退出条件（门禁） |
|---|---|---|
| 1 盘点 | 确认模式/范围/强度；跑一次全量基线扫描 | 产出基线（`scripts/reports/cleanup/cleanup.db`）+ 首份报告 |
| 2 扫描 | 静态检测（`CL-xx` + `PF-xx`），必要时叠加外部工具 | 候选清单落盘，规则分布与 Top 热点可见 |
| 3 分级与确认 | 按严重度分流；逐条做「动态引用核查」与「实测确认」 | 每条候选被标记为 确认可删 / 需实测 / 误报豁免 |
| 4 分批执行 | 清理按批提交；优化按「测量 → 改 → 复测」闭环 | 每批可独立回退，测试全绿 |
| 5 验证与沉淀 | 回归 + 复扫对比基线 + 复盘写 `references/iteration-log.md` | 存量清偿率提升、无误报残留 |

### 阶段 1：盘点与基线

```bash
# 全量基线扫描 + Markdown 报告（首次必跑，作为后续环比基准）
python scripts/cleanup.py --report

# 只看清理侧 / 只看性能侧
python scripts/cleanup.py --ruleset cl --json
python scripts/cleanup.py --ruleset pf --report
```

基线语义（与 `quality_gate` 同构）：首次全量扫描把所有 finding 记为 `open`；
下一轮全量扫描中未复现的自动标记 `fixed`；人工判定为误报的用 `--suppress` 落 `suppressed`。
**默认不阻断**（清理决策需人工介入）；只有 CI 强门禁场景才加 `--strict`。

### 阶段 2：扫描

内置检测器（零第三方依赖，纯标准库 `ast`）：

| 检测器 | 覆盖规则 |
|---|---|
| `detectors/dead_files.py` | CL-01 冗余文件（包装 OE-01 import 图）、CL-07 临时遗留、CL-08 空壳模块 |
| `detectors/dead_symbols.py` | CL-02 过时函数/类/常量（全库词元零引用） |
| `detectors/dead_logic.py` | CL-03 不可达、CL-04 恒定条件/等价分支、CL-05 空存根、CL-06 未使用局部变量、CL-09 注释代码块 |
| `detectors/perf.py` | PF-01 循环内 IO、PF-02 嵌套循环/线性扫描、PF-03 全量加载、PF-04 无界累积、PF-05 循环内字符串拼接、PF-06 热点候选、PF-09 WHERE 列函数包裹致索引失效 |
| `detectors/frontend.py` | CL-10 前端不可达文件、PF-07 渲染热点、PF-08 Context 未 memo |

可选增强工具见 `references/tool-matrix.md`（knip / vulture / ts-prune / radon / py-spy …）。
**降级原则**：外部工具缺失不阻塞流程，内置检测器保证能力下限；外部工具结果一律与内置结果交叉核对。

已由 `quality_gate` 覆盖、本 skill **不重复实现**的规则：`OE-01` 冗余模块、`OE-02` 过度抽象、
`OE-04` 重复代码块、`OE-06` 前端未使用导出、`OE-05` 复杂度超标、`OE-07` 超长组件。
清理任务应同时跑一次 `python scripts/quality_gate.py --ruleset oe` 取并集。

### 阶段 3：分级与确认

严重度以「造成实际风险 + 删除代价」为准：

| 级别 | 含义 | 处置 |
|---|---|---|
| `high` | 明确无消费者的整文件/整模块；命名即临时的遗留件 | 优先处理，仍需人工确认后删 |
| `medium` | 零引用符号、嵌套 ≥3 层循环、无 LIMIT 全量查询、空存根 | 进入本批次清单 |
| `low` | 未使用局部变量、2 层嵌套循环、注释代码块、索引 key | 批量清扫或直接豁免 |

**每一条候选在动它之前必须过三轮质询**（详见 `references/safety-protocol.md`）：

1. **动态引用核查**：`getattr`/`import_module`/`__import__`/注册表字典/装饰器/字符串类名/子进程调用/CLI 入口/桌面快捷方式/Runbook 是否引用它？
2. **框架反射核查**：是否被 FastAPI/Click/pytest/Pydantic 等按名字或装饰器调用？
3. **外部消费者核查**：`EMSXDataPipeline` 等仓库外消费者、Docker/Nginx 配置、前端 HTML 是否引用？

任一命中 → 转为 `--suppress` 豁免并写明理由，或加入 `scripts/cleanup/config.py` 对应豁免清单。

`PF-xx` 候选额外要求**实测证据**，否则降级为「待实测」不得进入优化批次。

### 阶段 4：分批执行

**清理批次顺序**（对齐 [ADR-0014](../../../docs/spec/adr/0014-dead-code-cleanup.md) 的分批经验，收益/风险比由高到低）：

```
B1 临时/调试遗留（CL-07）       → 零风险，先做
B2 空壳模块与不可达文件（CL-08/CL-01）→ 逐文件确认后删
B3 过时符号（CL-02）            → 按模块分批，每批跑测试
B4 无用逻辑（CL-03~CL-06/CL-09）→ 与功能改动同 commit，避免大 diff
B5 前端不可达文件（CL-10）      → 每批跑 `npm run build:all-modules` 验证
```

每批纪律：**批间跑测试**（`pytest` 三套 + `vitest` + 前端 build）；**删除与文档修订同 commit**；
**禁止跨批顺手改无关代码**（[`anti-patterns.md`](../../../docs/spec/anti-patterns.md) 的"超范围加料"）。

**优化闭环**（每一处都必须走完）：

```
测量基线 → 定位（profiler/EXPLAIN） → 单一改动 → 复测对比 → 固化基线
```

- 后端：`py-spy record` / `cProfile` 定 CPU，`tracemalloc` / `memory_profiler` 定内存，
  `EXPLAIN QUERY PLAN` 定查询，`pytest-benchmark` 定回归；
- 前端：React DevTools Profiler 定重渲染，`vite build --mode analyze` 或 bundle 可视化定体积；
- 优化后必须给出**前后对比数字**，否则视为未完成。

### 阶段 5：验证与沉淀

1. 复跑 `python scripts/cleanup.py --report`，对比基线与存量清偿率；误报项 `--suppress` 收口。
2. 全量回归：后端 `pytest`、前端 `vitest run`、`npm run build:all-modules`、`python scripts/quality_gate.py`。
3. 更新文档：被删脚本/接口在 `AGENTS.md`、`docs/spec/project-structure.md`、相关 README 中改注
   「已随 YYYY-MM-DD 清理移除，git 历史可恢复」；**历史记录豁免**（`specs/`、`plans/`、ADR、SQL 迁移注释中的历史提及不改）。
4. 复盘写 `references/iteration-log.md`（误报 / 遗漏 / 分级偏差 / 新增豁免清单），并滚动更新本 skill 的规则与阈值。

## 规则集索引

- 清理规则全表与逐条判定：`references/ruleset-cl.md`
- 性能规则全表与逐条判定：`references/ruleset-pf.md`
- 删除前安全协议（必读）：`references/safety-protocol.md`
- 外部工具矩阵与降级策略：`references/tool-matrix.md`
- 与 quality_gate / pre-commit / CI 集成：`references/integration-guide.md`
- 报告模板：`references/report-template.md`
- 自迭代复盘日志：`references/iteration-log.md`

## 命令速查

```bash
python scripts/cleanup.py                      # 全量扫描（清理 + 性能）
python scripts/cleanup.py --report             # + Markdown 报告
python scripts/cleanup.py --ruleset cl|pf      # 单规则集
python scripts/cleanup.py --json               # 机器可读（CI / 仪表盘）
python scripts/cleanup.py --strict             # 新增项即退出码 1（CI 强门禁）
python scripts/cleanup.py --suppress <fp> --note "理由"
git diff --cached --name-only | grep -E '\.(py|ts|tsx)$' | python scripts/cleanup.py --staged --quiet
python -m pytest scripts/cleanup/tests/ -q     # 检测器自测
```

## 约束

- **只报告不擅自删除**：除非用户明确授权执行清理，否则本 skill 的产出是清单与报告。
- **不臆测**：`PF-xx` 不声称性能问题，只声称「值得实测的候选」；`CL-xx` 不声称死代码，只声称「静态零引用候选」。
- **可复现**：每条 finding 带文件、行号、符号与 `fingerprint`，作者可直接跳转、可跨扫描追踪生命周期。
- **零新增依赖**：检测器保持纯标准库；外部工具为可选增强，缺失时自动降级。
- **遵守项目文件放置规范**：临时产物落 `_tmp/`，运行产物落 `scripts/reports/cleanup/`（已 gitignore）。
