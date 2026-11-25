---
name: salin-ui-director
description: 产品 UI 总控与多 skill 路由。用于用户明确要求 UI 总控、完整界面项目、从需求到实现再验收，或任务同时涉及普通产品界面、Dashboard、shadcn 组件工程、动效和质量审查。负责确定目标、项目类型、职责边界、执行顺序与统一验收，不替代 salin-product-ui-builder、salin-dashboard-builder、salin-shadcn-ui 或 salin-ui-quality-audit。单一明确任务应直接使用对应专项 skill。
---

# Salin UI Director

这个 skill 是轻量总控，不重复保存各专项的详细知识。它负责先判型、再分工、最后把设计目标、组件工程和质量验收合成一个可落地流程。

## 四个主能力包

| 能力包 | 负责 | 不负责 |
|---|---|---|
| `salin-product-ui-builder` | 普通 Web/App/小程序、SaaS 功能页、AI 工具、表单、登录、设置、官网与营销页的设计和实现 | Dashboard 图表专项、纯审查 |
| `salin-dashboard-builder` | Dashboard 页面架构、侧边栏、指标、交互图表、筛选联动和数据状态 | 普通营销页和无数据界面 |
| `salin-shadcn-ui` | shadcn 初始化、组件源码、主题 tokens、变体、表单/表格/应用壳组合 | 自定义 registry 发布、技术栈未定的纯设计 |
| `salin-ui-quality-audit` | UI 审查、批评、反模板化、打磨、加固、无障碍与上线验收 | 未经授权修改代码 |

`shadcn-ui-registry`、Figma/Product Design、GSAP 等保留为专项能力，仅在用户需求明确时加入，不合并进四个主包。

## 路由规则

- 普通产品页面的新建、改造或实现：`salin-product-ui-builder`。
- Dashboard、数据看板、运营后台图表/侧栏：`salin-dashboard-builder`。
- 已确定使用 shadcn 的组件和主题工程：`salin-shadcn-ui`。
- 整体流程、视觉层级、反模板化、跨页面一致性、通用无障碍或上线质量审查：`salin-ui-quality-audit`，默认不修改。
- 图表选型、数据口径、坐标轴、Dashboard 导航和筛选联动审查：`salin-dashboard-builder`。
- shadcn CLI、component base、组件源码、tokens、主题和底层组件行为审查：`salin-shadcn-ui`。
- “设计并用 shadcn 实现”：产品 builder 负责用户任务和页面结构，shadcn skill 负责组件与主题工程。
- “重构 Dashboard 并验收”：dashboard builder 负责方案和实现，quality audit 负责独立复核。
- “完整 UI 项目”：按目标 → 专项设计 → 组件实现 → 真实验收顺序组合，避免四个 skill 同时重复分析。
- 动效仅在信息状态变化、空间关系或品牌表达需要时加入；项目已有 GSAP 或用户明确要求时再使用 GSAP 专项。

## 总控流程

1. **目标和验收**：明确用户、设备、主任务、业务约束、实现范围与可观察结果。
2. **项目检查**：已有项目先读 README、AGENTS/CLAUDE、依赖、路由、组件、样式、tokens、环境变量示例和 Git 状态。
3. **选择并加载主 skill**：只能有一个主负责人。选定后必须完整加载并遵守主 skill 的 `SKILL.md`；协作 skill 只加载分工对应的参考。专项 skill 不可用时明确报告并使用已知的最小安全流程，不得假装已调用或已遵守其规则。
4. **统一设计读法**：一句话固定页面类型、用户、视觉语言和主操作，避免各模块各自选风格。
5. **确定交接契约**：统一 tokens、状态所有权、路由/权限、响应式和验收标准。
6. **按顺序执行**：先产品流程与信息架构，再组件工程，再必要动效，最后质量审查。
7. **真实验证**：运行项目已有检查，并在浏览器走关键流程；质量审查只记录复核确认的问题。

## 何时读取总控参考

| 情况 | 参考 |
|---|---|
| 不确定项目属于哪类产品 | [references/project-types.md](references/project-types.md) |
| 需要跨模块统一视觉方向 | [references/visual-direction.md](references/visual-direction.md) |
| 用户明确要求 Apple-like | [references/apple-style.md](references/apple-style.md) |
| 页面模式跨多个普通产品表面 | [references/surface-patterns.md](references/surface-patterns.md) |
| 跨模块已有界面需要结构性重设计诊断 | [references/redesign-audit.md](references/redesign-audit.md) |
| 项目包含组件落地协调 | [references/implementation-playbook.md](references/implementation-playbook.md) |
| 明确需要 GSAP 或复杂动效 | [references/motion-gsap.md](references/motion-gsap.md) |
| 总体完成前检查 | [references/qa-checklist.md](references/qa-checklist.md) |

专项 skill 已包含更详细规则时，以专项规则为准；总控参考只用于跨模块一致性。

## 输出契约

```markdown
## UI 总控方案
- 目标：用户 / 主任务 / 设备 / 验收标准
- 主负责人：一个主 skill 及理由
- 协作模块：需要的专项 skill 与明确边界
- 执行顺序：设计 → 实现 → 动效（如需）→ 验收
- 统一契约：视觉方向 / tokens / 状态 / 响应式 / 权限路由
- 保持不动：不在本次范围的模块
- 风险：项目事实缺失 / 未验证环境 / 依赖变化
```

用户要求执行时，输出短方案后继续实现，不停留在调度建议；用户只要求方案、评审或计划时保持只读，不擅自执行。完成后汇报关键文件、检查结果、未验证项和残余风险。

## 总控自检

- 是否只有一个主负责人，避免多 skill 重复产出相互冲突的方案。
- 是否把 Dashboard、普通产品、shadcn 工程和质量审查放到正确边界。
- 是否统一视觉方向、tokens、状态与验收，而非拼接四套风格。
- 是否保留项目现有技术栈、组件和未提交修改。
- 是否在真实页面验证，而不是只宣布代码能编译。
