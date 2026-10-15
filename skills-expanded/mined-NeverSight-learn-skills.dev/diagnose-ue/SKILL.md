---
name: diagnose-ue
description: Diagnose UE issues when a concrete Unreal Engine symptom needs a reproducible feedback loop, including crash, assert, PIE/Packaged drift, Blueprint, asset/load/cook, network, rendering, memory, performance, or platform-only failure. Produce runtime mode, falsifiable hypotheses, probes, evidence, regression seam, and one repair handoff.
version: 0.1.0
---

# Diagnose UE

面向 UE 开发问题的定位纪律。核心不是先猜代码，而是先构造一个可重复、可观察、agent 可运行或可指导用户运行的反馈循环；再用可证伪假设、定向仪表和回归验证收敛问题。

UE 问题通常横跨 C++、Blueprint、Asset、Editor state、Cooked content、平台配置和异步线程。不要只按 Web 应用思路找 request/response；要先确定问题发生在哪个运行形态：Editor、PIE、Standalone、Dedicated Server、Listen Server、Client、Cooked、Packaged、Shipping、目标平台。

## 进入边界

使用本 skill 的前提是存在具体 UE 症状，需要定位原因、验证修复，或从运行时 artifact 建立诊断路径。可以由用户显式调用，也可以由 `workflow-router` 或上一轮 `Natural Handoff` 推荐后进入。本 skill 产出运行形态、root cause、证据、修复选项和回归验证建议；不要提交持久业务代码修改。

适用：

- crash、assert、ensure、Editor hang、PIE/Standalone/Cooked/Packaged/Shipping 差异。
- Blueprint、asset/load/cook、network、rendering、memory、performance、platform-only failure。

不适用：

- UE API 教学、概念解释、一般架构设计。
- 新功能设计、普通实现任务、纯代码 review。
- 纯 RenderDoc `.rdc` 捕获分析，除非目标是回到 UE 工程里建立 repro 和修复验证循环。

如果需要落地修复，用 `Natural Handoff` 推荐 `$quick-change`、`$implement` 或 `none` 中的一个。

## Language Contract

语言契约：生成的文档和聊天输出默认以中文优先；代码、命令、API 名称、契约字段、ID、专有名词以及必要的技术术语保留英文。用户或目标项目明确要求英文时可以例外，但必须记录原因。

## Pressure Scenarios（压力场景）

- 用户要求“直接修”时，仍必须先确认运行形态、精确症状和最短反馈循环；未复现或未定界前不要改代码。
- 只有 log、callstack、截图或 trace、没有工程访问时，不要声称已复现；标记为 artifact-based diagnosis，并列出需要用户补充的最小材料。
- 只在 Cooked、Packaged、Shipping、network、platform 或特定 RHI 出现的问题，不能用 PIE 或不对应的运行形态通过作为完成验证。
- 性能问题必须先固定 baseline、地图、视角、scalability、RHI、分辨率和采样窗口，再改代码。
- 临时 instrumentation 必须能对应某个 hypothesis 的 prediction；结束前清理或明确保留位置。

## References

- 运行形态依赖 Editor、PIE、Standalone、Cooked、Packaged、Shipping、server/client、platform 或 RHI 时，必须读取 `references/runtime-modes.md`。
- 选择 log、callstack、CrashContext、minidump、Unreal Insights、Network Profiler、Cook log 或 `[DEBUG-UE-...]` probe 时，必须读取 `references/probes-and-artifacts.md`。
- 将 repro 转成 Automation、Functional Test、Gauntlet、command-line、cook/package、network 或 performance validation 时，必须读取 `references/regression-seams.md`。

## Phase 1 — 建立 UE 反馈循环

先得到一个能稳定暴露症状的 pass/fail 信号。优先选择能被命令行、自动化测试或固定操作脚本重复执行的循环。

优先尝试最小 map/Actor/Asset、Automation/Functional Test、固定命令行启动、PIE/Standalone 操作脚本、Cook/Package 循环、网络多实例循环、性能 profiling 循环、崩溃捕获循环，最后才使用 HITL 循环。运行形态和 artifact 细节见 `references/runtime-modes.md` 和 `references/probes-and-artifacts.md`。

让循环更快、更尖锐、更确定：跳过无关启动，缩小 map 和 asset，固定随机种子、GameMode、启动参数和运行形态；用可断言的 crash function、ensure 文本、错误 asset、错误 replicated value 或帧时间阈值定义 pass/fail。

没有可信反馈循环时，停下来说明已尝试内容，并向用户请求缺失的最小材料。

## Phase 2 — 复现并定界

运行反馈循环并确认看到的是用户描述的问题，不是附近的另一个错误。

必须记录：

- 运行形态：Editor、PIE、Standalone、Cooked、Packaged、Shipping、Server/Client、平台、RHI、build configuration。
- 精确症状：crash/ensure/assert 文本、callstack 顶部有效帧、错误 log category、错误画面、错误状态值、耗时指标。
- 触发条件：map、actor/component、asset path、输入步骤、网络角色、关卡切换、存档/加载、GC、异步加载或 shader/cook 时机。
- 复现率：稳定复现、N 次中 M 次复现，或性能指标的 baseline。

复现前不要进入修复。

## Phase 3 — 提出 3-5 个可证伪假设

先列出排序后的 hypotheses，再测试。每个 hypothesis 必须写出 prediction。

格式：

> 如果 `<X>` 是原因，那么 `<改变 Y / 添加 probe Z / 切换运行形态>` 会让症状消失、移动或变得更严重。

UE 常见假设维度：

- 生命周期：constructor、PostInitProperties、BeginPlay、OnRegister、Tick、EndPlay、GC、async loading、level streaming 顺序错误。
- Reflection/Blueprint：UPROPERTY 缺失、Blueprint stale class、hot reload 产物、CDO/default value、nativization/cook 差异。
- Asset/Cook：引用丢失、soft reference 未 cook、redirector、AssetManager rule、platform-specific asset 或 shader permutation。
- Threading：GameThread/RenderThread/RHIThread/AsyncTask 边界错误，非线程安全 UObject 访问。
- Network：authority/ownership、RPC 条件、replication order、prediction、dormancy、seamless travel。
- Performance：CPU/GPU/render thread bottleneck、GC spike、asset streaming、shader compilation、tick fan-out、allocation churn。

把排序列表展示给用户；用户不在时，按当前排序继续。

## Phase 4 — 定向仪表

每个 probe 都要对应 Phase 3 的一个 prediction。一次只改变一个变量。

优先使用 Debugger/breakpoint/watch、已有 UE 工具、定向 log、Blueprint probe。probe 和 artifact 选择见 `references/probes-and-artifacts.md`。

不要 “log everything and grep”。性能问题先测 baseline，再改代码；渲染问题先判断 CPU/GPU/render thread/RHI thread；网络问题先分清 server truth、client prediction 和 replicated presentation。

## Phase 5 — 修复方案与回归验证入口

有正确 seam 时，先把最小 repro 转成 regression test 或自动化验证建议，再进入修复。

可接受 seam 包括 Automation/Functional/Gauntlet test、小型 repro map + command line + 断言 log/exit code、C++ unit/automation test、性能 baseline 测试，以及 cook/package 验证。选择细节见 `references/regression-seams.md`。

如果没有正确 seam，记录这是架构或测试性缺口；不要用过浅的 unit test 制造虚假信心。

修复入口必须说明：

1. regression test 或等价验证应该如何先失败、后通过。
2. 最小修复方向、影响范围和风险。
3. 最终推荐 `$quick-change`、`$implement` 或 `none` 中的一个；不要同时给两个修复入口。
4. 修复后必须重新运行原始未最小化场景。
5. 对 cooked/packaged-only、network-only、platform-only 问题，修复后必须在对应运行形态再验证一次。

## Natural Handoff

诊断 loop 完成后，只能给出一个 next skill：

- 小、清楚、低风险且可快速验证的修复，推荐 `$quick-change`。
- 跨模块、测试/实现步骤较多、影响 contract 或风险不清的修复，推荐 `$implement`。
- 证据不足、暂无正确修复入口，或用户只需要诊断报告，推荐 `none`。

Natural Handoff 必须带上 root cause 状态、regression seam、最小修复方向、风险和仍缺材料；用户自然确认只进入这一个 next skill，不能绕过目标 skill 的 branch、scope、verification 或修改确认。

## Phase 6 — 清理与复盘

完成前检查：

- [ ] 已确认 root cause，或明确说明仍缺少什么 UE 运行形态证据。
- [ ] 已给出 regression seam、等价验证循环，或已记录没有正确 seam。
- [ ] 已给出唯一修复入口：`$quick-change`、`$implement` 或 `none`。
- [ ] 所有 `[DEBUG-UE-...]` log、Blueprint Print String、临时 console command、测试 map 中的 debug-only 对象已清理或移动到明确 debug 位置。
- [ ] 临时 asset、repro map、trace、minidump 的去留明确；保留时放在项目约定的 debug/artifact 位置。
- [ ] 诊断报告或后续修复 handoff 中说明最终正确的 hypothesis、验证方式和覆盖的运行形态。

## 输出检查

最终诊断输出包含：

- 运行形态和复现条件。
- 精确症状和关键证据。
- 已测试 hypotheses、prediction 和结果。
- root cause 状态：confirmed、likely、blocked。
- regression seam 或等价验证循环。
- 清理状态和残留 artifacts。
- 唯一修复入口：`$quick-change`、`$implement` 或 `none`。

最后追问：什么原本可以防止这个问题？如果答案是缺少测试 seam、生命周期耦合、资产引用规则不清、网络 ownership 模型混乱或 profiling 基线缺失，把具体结论交给架构改进或测试基础设施建设，而不是在修复前泛泛重构。
