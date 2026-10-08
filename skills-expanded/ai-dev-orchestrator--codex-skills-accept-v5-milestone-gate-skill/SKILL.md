---
name: accept-v5-milestone-gate
description: 将 AI-Dev-Orchestrator V5 母本中的工作包 / 阶段裁定、Pass / Partial / Blocked 分级、无法裁定判定、缺证识别与遗留项收口规则收敛成中文验收型 skill。用于在实现、review、verify 之后，对某个 V5 切片、工作包或阶段给出正式 gate 结论，并明确可放行边界、不可放行边界、阻塞原因、缺失证据与下一线程接力方向。
---

# accept-v5-milestone-gate

## 使命与 owner

把 V5 线程里的“现在差不多可以宣布完成了吧”收敛成 **诚实、分级、可追责、可继承** 的正式裁定。

这个 skill 的 owner 职责只有一个：

> **负责判断当前最多能宣布到哪一步，并把 gate 结论写成后续线程可直接继承的正式交接物。**

它重点负责：

- 对工作包、单轮切片或阶段给出 `Pass / Partial / Blocked / 无法裁定` 结论
- 明确能确认完成的范围、不能确认完成的范围、阻塞原因与遗留项
- 识别“缺证”和“真阻塞”的区别，避免把信息不足误写成放行或阻塞
- 判断当前是否具备进入下一线程 / 下一阶段 / 下一层裁定的条件
- 给 `build / write / govern / drive / verify` 等兄弟 skill 明确回退或接棒方向

它不应该把线程带偏成：

- 继续补实现、补验证、补 review 或补 freeze 文档
- 没有足够材料就乐观放行
- 把“结构治理完成一部分”写成“前端控制面可宣发”
- 把“局部切片完成”夸大成“整个 Phase 完成”
- 不写缺证项、遗留项与下一棒 owner

## 强绑定的权威输入

优先级从高到低如下：

1. `C:\Users\Administrator\Desktop\AI-Dev-Orchestrator-V5-Plan.md`
2. `docs/README.md`
3. `C:\Users\Administrator\Desktop\ai-skills草案\00-V5-skill-suite-map.md`
4. `C:\Users\Administrator\Desktop\ai-skills草案\accept-v5-milestone-gate-skill-草案.md`
5. `references/milestone-gate-map.md`
6. `references/pass-partial-blocked-rules.md`
7. `references/evidence-requirements-and-rollup-checklist.md`
8. `references/milestone-gate-thread-checklist.md`
9. 当前工作包的计划 / freeze / 实现说明 / review 结论 / verify 结论 / 文档回填
10. 仅在必要时抽查的相关代码、页面、构建输出、接口响应、日志或脚本输出

如果这些输入之间冲突，**以 V5 母本 + 已验证事实 + 已审查风险结论 + 仓库现实为准**，不要让乐观叙述覆盖现实。

## V5 母本绑定原则

这个 skill 必须明确绑定到 V5 母本，不允许退化成“泛化项目验收”。

默认优先对照母本里的三类验收口径：

### 产品能力验收

关注：

- 老板是否真的能配置团队与控制角色
- provider / prompt / token / memory / multi-agent 能力是否形成真实闭环
- 控制面是否只是展示，还是已经能操作、回显并留下事实证据

### 工程验收

关注：

- 数据结构、迁移、合同与主链是否闭合
- 关键路径是否有最小 smoke / integration / build / page / API 证据
- 结构治理后入口页、锚点、脚本和联调路径是否仍稳定

### 成本验收

关注：

- token / cost 是否有真实统计口径或至少有可追踪基础
- 成本优化是否只是口号，还是已有量化或可复核证据

如果用户没有指定验收对象，默认先收敛为：

1. 一个工作包或单轮切片
2. 不默认上升为整个 Phase
3. 只有证据闭合时，才允许提升到阶段级裁定

## 技能边界

### 什么时候使用

在下列场景使用本 skill：

- 某个工作包已经过一轮实现、review、verify，想做正式裁定
- 你想知道当前能否把状态改成“通过 / 部分通过 / 阻塞”
- 你需要一个正式 gate 结论，给后续线程继承
- 你需要识别“只是缺证”还是“确实被阻塞”
- 你要判断“前端结构治理后是否具备放行条件”这类场景

### 什么时候不要继续停留在本 skill

- 主任务是修 skill 包本身、修乱码、补 references / templates → `build-v5-skill-pack`
- 主任务是写前端控制面、补 hooks / types / api / 页面交互 → `write-v5-web-control-surface`
- 主任务是治理 `App.tsx` / `ProjectOverviewPage.tsx`、拆分结构、稳定锚点 → `govern-v5-web-structure`
- 主任务是跨 backend / web / docs / verify 协调整链交付 → `drive-v5-orchestrator-delivery`
- 主任务是查运行事实、build、页面、API、回归 → `verify-v5-runtime-and-regression`
- 主任务是做结构风险、合同风险、主链风险审查 → `review-v5-code-and-risk`
- 主任务是补 freeze 状态、回填进度与完成定义 → `manage-v5-plan-and-freeze-docs`

一句话：**本 skill 管裁定，不代替实现、治理、验证、总控、文档治理或 skill 维护。**

## 四类正式结论

### 1. Pass

适用于：

- 验收对象明确
- 范围基本闭合
- 关键实现已完成
- 必要 review 与 verify 足够支撑当前层级
- 高风险已消化、已接受或已明确隔离
- 文档、代码、验证口径一致

### 2. Partial

适用于：

- 核心部分完成，但仍有明确缺口
- 当前可算“切片完成”，不能算“更大范围完成”
- 可以继续推进，但必须保留遗留项、前置条件与下一棒 owner

### 3. Blocked

适用于：

- 验收对象明确，但关键实现、关键依赖或关键风险阻断了放行
- 存在明确阻塞源：例如 build 失败、入口断裂、接口不通、主链未接通、高风险未解
- 即使继续讨论，也不能把当前状态写成可放行

### 4. 无法裁定

适用于：

- 验收对象不清，甚至不知道在验工作包、切片还是 Phase
- 缺少必要输入，导致连 `Pass / Partial / Blocked` 都无法负责任地分级
- 只有实现自述，没有最小 review / verify / 完成定义支撑
- 证据之间明显冲突，但还没查清以哪份事实为准

**注意：**

- `Blocked` = 对象明确，但当前真被事实阻断。
- `无法裁定` = 连可靠分级基础都不够，先补材料再回来判。

## 正式落盘边界

### 本 skill 的主要输出形式

- `Pass / Partial / Blocked / 无法裁定` 结论
- 验收对象与裁定层级
- 依据材料与证据等级
- 能确认完成与不能确认完成的范围
- 缺证项、阻塞项、遗留项与前置条件
- 下一线程建议 skill 与理由

### 默认会触达的材料

- 母本 / plan / freeze / 回填文档
- 当前工作包的实现说明
- 最近一轮 `review-v5-code-and-risk` 结论
- 最近一轮 `verify-v5-runtime-and-regression` 结论
- 必要时的代码、页面、build、日志、API、脚本现实核对

### 默认不越权的面

- 不替实现 skill 修功能
- 不替 `verify` 补运行事实
- 不替 `review` 做结构 / 合同 / 主链风险识别
- 不替 `manage` 直接改冻结状态
- 不替 `build-v5-skill-pack` 维护其他 skill 本体

## 开始入口

每次接手 V5 裁定任务时，先按下面顺序读取，且只读最小集合：

1. 打开 V5 母本：`C:\Users\Administrator\Desktop\AI-Dev-Orchestrator-V5-Plan.md`
2. 打开 skill map：`C:\Users\Administrator\Desktop\ai-skills草案\00-V5-skill-suite-map.md`
3. 打开本 skill 自带参考：
   - `references/milestone-gate-map.md`
   - `references/pass-partial-blocked-rules.md`
   - `references/evidence-requirements-and-rollup-checklist.md`
   - `references/milestone-gate-thread-checklist.md`
4. 打开当前工作包的计划 / freeze / 回填文档
5. 打开最近一轮 `review-v5-code-and-risk` 结论
6. 打开最近一轮 `verify-v5-runtime-and-regression` 结论
7. 只在必要时抽查最相关的代码、页面或输出事实

### 最小必读材料

- 当前工作包或阶段的完成定义
- 最近一轮实现说明
- 最近一轮 review 结论
- 最近一轮 verify 结论
- 若已有 freeze 回填，则同步查看其状态口径

### 按验收对象补读

#### 工作包 / 切片级验收

- 该切片直接改动的代码或页面入口
- 与当前切片直接相关的 verify 证据
- 相关 review 风险分级

#### 阶段级验收

- 该 Phase 下多个工作包的回填
- build / smoke / page / API 证据汇总
- 关键遗留项与前置条件清单

## 如何处理模糊请求

遇到“现在能不能算完成”“能不能过这阶段”“给个正式结论”这类模糊请求时：

1. 先翻译成 **一个验收对象 + 一个裁定层级**。
2. 默认先验收工作包或切片，不默认直接验收整个 Phase。
3. 明确这次结论影响哪个状态口径。
4. 如果材料不足，也要把“当前只能给无法裁定 / Partial / Blocked”写成结论的一部分。

例如：

- “Phase 1 现在能过吗” → 先拆成 provider / prompt / token / role policy / memory recall 各自是否闭合
- “这轮 runtime 改动能不能算完成” → 先按单轮后端切片做裁定，不直接上升到整个模块
- “这个团队控制中心能不能宣发” → 先看前端控制面、后端合同、verify 证据与遗留风险是否闭合
- “前端结构治理后能不能放行” → 先看治理范围、入口 / build / 锚点 / 脚本 / 回归证据与遗留结构债是否闭合

## 核心工作流

### 1. 先判 owner 是否正确

先回答：

- 当前主任务真的是“裁定”，还是其实还在补实现 / 补验证 / 修 skill？
- 当前对象是一个切片、一个工作包，还是整个 Phase？
- 如果现在继续做 accept，会不会越权替别人补事实？

判错 owner，就会把整个结论写偏。

### 2. 锁定验收对象与裁定层级

至少写清：

- Phase
- 工作包 / 切片
- 本轮只裁定什么
- 本轮明确不裁定什么

### 3. 收齐三类材料

尽量同时看三类材料：

1. 完成定义与计划口径
2. 实现与 review 风险材料
3. verify 与运行证据

少任意一类，结论都容易失真；必要时直接进入“无法裁定”。

### 4. 区分“缺证”与“真阻塞”

优先判断：

- 是不是材料不够，所以还不能分级？→ `无法裁定`
- 还是对象明确，但已被 build / 入口 / 合同 / 主链 / 高风险事实卡住？→ `Blocked`

### 5. 判断“最多能说到哪里”

验收不是追求积极，而是追求准确。

如果当前最多只能说：

- “结构治理切片已完成，入口与 build 最小回归通过”

就不要写成：

- “整个前端控制面可宣发”

### 6. 套用分级规则

- 满足闭合条件 → `Pass`
- 仅切片闭合、仍有明确缺口 → `Partial`
- 有明确事实阻塞 → `Blocked`
- 缺材料或材料冲突到无法负责任分级 → `无法裁定`

### 7. 写正式遗留项

每次裁定至少留下：

- 风险
- 缺证项
- 必补项
- 下一阶段前置条件
- 下一线程建议 owner

### 8. 明确交接路线

线程结束时必须明确下一棒是谁：

- 若完成定义不清 → `manage-v5-plan-and-freeze-docs`
- 若实现不够 → `write-v5-runtime-backend` / `write-v5-web-control-surface`
- 若结构治理未闭合 → `govern-v5-web-structure`
- 若缺运行事实 / build / 页面 / 回归证据 → `verify-v5-runtime-and-regression`
- 若高风险没澄清 → `review-v5-code-and-risk`
- 若本质是跨层整链收口 → `drive-v5-orchestrator-delivery`
- 若要修 accept skill 包本身 → `build-v5-skill-pack`

## 特别场景：前端结构治理后是否具备放行条件

这是本 skill 的高频 gate 场景之一，但要和 `govern-v5-web-structure`、`verify-v5-runtime-and-regression` 分工清楚。

### `govern-v5-web-structure` 负责什么

- 做结构治理方案与落地
- 控制入口页瘦身、拆分边界、测试锚点规范
- 说明联调影响与最小验证建议

### `verify-v5-runtime-and-regression` 负责什么

- 证明 build、入口、页面、脚本、锚点或回归事实是否成立
- 记录失败事实、环境阻塞与证据等级

### `accept-v5-milestone-gate` 在这个场景只负责什么

- 判断“是否具备放行条件”
- 判断是 `Pass / Partial / Blocked / 无法裁定`
- 判断这次最多能宣称到“结构治理切片通过”还是“控制面整体可继续推进”

### 结构治理场景的推荐分级

#### 可给 Pass

- 结构治理对象明确
- 治理目标已落地
- verify 已证明 build / 入口 / 关键受影响链路最小回归通过
- review 没有剩余高风险阻断
- 结论只覆盖本次结构治理切片，不夸大到整个业务能力

#### 应给 Partial

- 结构治理主体完成，但仍有待同步锚点、脚本、次级页面或文档
- verify 仅覆盖最小回归，还不足以支撑更大范围放行
- 只够宣布“本切片结构治理基本闭合”，不够宣布“前端整体稳定”

#### 应给 Blocked

- build / 入口 / 关键页面 / 关键脚本存在明确失败
- 结构治理打断旧链路或暴露高风险未解
- 页面 owner 边界、合同或联调依赖仍未闭合，导致无法放行

#### 应给 无法裁定

- 只有重构 diff，没有治理目标说明
- 没有 verify 证据，不知道入口和回归有没有受影响
- review / verify / 完成定义缺失到无法负责任判断

## 与兄弟 skill 的协作契约

- 本 skill 负责：**阶段裁定、工作包裁定、分级结论、缺证识别、遗留项收口、下一棒指定**
- `build-v5-skill-pack` 负责：**skill 包体检、修复、补强、路由收口；不负责业务裁定**
- `write-v5-web-control-surface` 负责：**前端控制面实现落地；不负责最终 gate**
- `govern-v5-web-structure` 负责：**前端结构治理与稳定锚点；不负责最终放行**
- `drive-v5-orchestrator-delivery` 负责：**跨 backend / web / docs / verify 的整链推进；不代替 accept 下最终裁定**
- `verify-v5-runtime-and-regression` 负责：**运行事实、构建 / API / 页面 / 回归证据；不代替 accept 下 milestone 结论**
- `review-v5-code-and-risk` 负责：**结构、兼容性、主链、合同与风险把关**
- `manage-v5-plan-and-freeze-docs` 负责：**完成口径、freeze 文档、状态回填与交接治理**

不要替兄弟 skill 越权补实现、补验证或补审查；本 skill 只对裁定负责。

## 推荐输出骨架

优先使用 `templates/milestone-gate-decision-template.md`，至少覆盖：

- 验收归属
- 依据材料
- 证据等级与缺证项
- 裁定结论
- 能确认完成与不能确认完成的范围
- 遗留项 / 阻塞项 / 前置条件
- 下一线程建议 skill

## 非完成定义

出现以下情况时，不能算本 skill 工作合格完成：

- 验收对象不明确，就直接给笼统结论
- 明明缺证，却硬给 `Pass` 或 `Blocked`
- 明明是 `Partial`，却夸大成 `Pass`
- 只复述上游自述，不写证据来源与证据等级
- 不写遗留项、缺证项和前置条件
- 把结构治理切片完成写成前端整体可宣发
- 验收结论让后续线程不知道该先补什么、由谁补

## 红线

1. 不要跳过 review / verify 就做乐观验收。
2. 不要把 `Partial` 硬写成 `Pass`。
3. 不要把“缺证”误写成“已经阻塞”或“已经通过”。
4. 不要不给遗留项、缺证项和下一棒 owner。
5. 不要在结论里夸大当前可用程度。
6. 不要把切片完成误写成阶段完成。
7. 不要越权修改或接管其他兄弟 skill 本体。

## Done checklist

- 已明确当前验收对应哪个 V5 Phase / 工作包 / 切片。
- 已明确这次裁定的层级，以及明确不裁定的更大范围。
- 已引用 V5 母本，而不是脱离母本自由发挥。
- 已同时查看完成口径、实现材料、review 结论、verify 证据。
- 已区分当前是 `Pass / Partial / Blocked / 无法裁定` 的哪一种。
- 已明确证据等级、缺证项与冲突证据处理方式。
- 已清楚写出能确认完成与不能确认完成的范围。
- 已把遗留项、风险、前置条件写成正式交接物。
- 已明确下一线程应接的 owner skill。
- 已避免把局部完成夸大为整阶段完成。
- 已让后续新线程可以直接调用本 skill 接手同类里程碑裁定任务。

## References

- `references/milestone-gate-map.md`
- `references/pass-partial-blocked-rules.md`
- `references/evidence-requirements-and-rollup-checklist.md`
- `references/milestone-gate-thread-checklist.md`
- `playbooks/milestone-gate-playbook.md`
- `templates/milestone-gate-decision-template.md`
