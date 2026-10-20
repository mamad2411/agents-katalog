# /super-dev-seeai (claude-code)

在当前项目触发 Super Dev SEEAI 赛事极速版。

## 输入
- 需求描述: `$ARGUMENTS`
- 如果未提供参数，先要求用户补全需求后再执行。

## SEEAI 定位
- 面向比赛或超短时间盒交付，例如精美官网、小游戏、展示型工具或单功能 demo。
- 保留 research / 三文档 / docs confirm / spec，但全部压缩成比赛快版。
- Spec 确认后直接进入前后端一体化快速开发，不再拆 preview confirm。
- 若宿主会更新 `.super-dev/workflow-state.json`，必须显式写入 `flow_variant = seeai`，确保恢复和继续提示仍然回到 SEEAI 模式。

## 半小时时间盒
- 0-4 分钟：fast research，锁定评审场景、竞品风格和作品 wow 点。
- 4-8 分钟：输出 compact research / PRD / architecture / UIUX。
- 8-10 分钟：等用户确认文档和方向，不展开长讨论。
- 10-12 分钟：生成 compact Spec / tasks，只保留最小可交付路径。
- 12-27 分钟：一体化 full-stack sprint，先把主展示面做成，再补最小必要后端/数据层。
- 27-30 分钟：polish、demo 路径检查、讲解词和亮点总结。

## 首轮输出模板
- `作品类型`：官网类 / 小游戏类 / 工具类，三选一。
- `评委 wow 点`：本次作品最值得被记住的一个亮点。
- `P0 主路径`：半小时内必须真实跑通的一条演示路径。
- `主动放弃项`：本轮明确不做的部分，避免范围失控。
- `关键假设`：只有在用户没说清时才写，最多 1 到 2 条。
- 如果需求不缺关键输入，不要长时间澄清，直接进入 fast research。

## 范围裁剪规则
- P0：必须完成一个可演示主路径，首页/主玩法/主工具流程必须能跑。
- P1：补一个明显 wow 点，例如强主视觉、动画、排行榜、分享页、彩蛋交互。
- P2：只有在剩余时间充足时才加扩展能力，例如真数据库、登录、复杂后台。

## 比赛短文档模板
- `research.md`：题目理解、评委 wow 点、参考风格、主动放弃项。
- `prd.md`：P0 主路径、P1 wow 点、P2 可选项、非目标。
- `architecture.md`：页面/玩法主循环、技术栈、最小后端、降级方案。
- `uiux.md`：视觉关键词、主 KV、页面骨架、关键动效。
- `spec`：只保留一个 sprint 清单，按 `P0 -> P1 -> polish` 排序。

### 推荐标题骨架
- `research.md`：`# 题目理解` `# 参考风格` `# Wow 点` `# 主动放弃项`
- `prd.md`：`# 作品目标` `# P0 主路径` `# P1 Wow 点` `# P2 可选项` `# 非目标`
- `architecture.md`：`# 主循环` `# 技术栈` `# 数据流` `# 最小后端` `# 降级方案`
- `uiux.md`：`# 视觉方向` `# 首屏/主界面` `# 关键交互` `# 动效重点` `# 设计 Token`
- `spec`：`# Sprint Checklist` 下只列 `P0`、`P1`、`Polish`

## 作品类型决策
- 官网类题：优先主视觉、品牌叙事、首屏信息密度和滚动节奏。
  默认技术栈：React/Vite 或 Next.js + Tailwind + Framer Motion。
  默认 sprint：Hero/首屏 -> 亮点区/叙事 -> CTA/滚动动效 -> 最终 polish。
- 小游戏类题：优先核心玩法循环、反馈感、积分/胜负和再次游玩闭环。
  默认技术栈：HTML Canvas + Vanilla JS；复杂玩法再上 Phaser。
  默认 sprint：主循环可玩 -> 积分/胜负反馈 -> 特效/音效 -> 复玩和 polish。
- 工具类题：优先一个高价值主流程、输入输出清晰、结果页直观。

  默认技术栈：React + Vite + Tailwind；必要时补最小 Express/Fastify 后端。
  默认 sprint：输入页/主流程 -> 结果页 -> 分享/导出等演示加分项 -> 最终 polish。

## 题型识别提示
- 提到品牌、官网、落地页、活动宣传、首屏，默认按官网类处理。
- 提到玩法、得分、胜负、闯关、点击反馈，默认按小游戏类处理。
- 提到生成、分析、查询、输入输出、结果页、效率提升，默认按工具类处理。
- 如果需求跨多类，先选最容易让评委记住的那一类做主轴。

## 降级策略
- 如果真实后端会拖慢交付，优先用本地 mock、JSON、内存态或静态数据把演示路径跑通。
- 如果鉴权、支付、上传等不是评审主轴，优先做高保真演示流，不强行接完整生产链路。
- 如果时间吃紧，砍掉次要页面和长尾功能，保住视觉完成度、主流程和讲解效果。

## 必须执行的顺序
1. 先做 fast research，快速吸收竞品、参考作品与评审导向，并写入 `output/*-research.md`
2. 再生成 compact `output/*-prd.md`、`output/*-architecture.md`、`output/*-uiux.md`
3. 三份 compact 文档完成后，必须先等待用户明确确认
4. 用户确认后，再创建 compact Spec / tasks
5. Spec 之后直接进入 full-stack sprint：先做主展示前端，再补最小必要后端/数据层，然后统一 polish
6. 最后输出 demo 路径、亮点总结与如何讲解这个作品

## 设计与质量要求
- 速度优先，但不能做成未抛光的半成品。
- 默认追求高展示性、强主视觉、明确 wow 点，但保持题型适配，不强制所有作品都是营销页。
- 文案、按钮、交互、主流程必须可演示，禁止明显占位和 AI slop。
- 功能图标只能来自 Lucide / Heroicons / Tabler，禁止 emoji。
- 时间不够时优先删功能，不要删完成度；至少保住一个 wow 点和一条主演示路径。

## 禁止事项
- 不要跳过 research / 三文档 / docs confirm / spec。
- 不要把 SEEAI 模式扩回标准 Super Dev 的 preview gate / 长质量闭环。
- 不要在文档确认前直接开工。

## Super Dev SEEAI Flow Contract
- SUPER_DEV_SEEAI_FLOW_CONTRACT_V1
- PHASE_CHAIN: research>docs>docs_confirm>spec>build_fullstack>polish>handoff
- DOC_CONFIRM_GATE: required
- PREVIEW_CONFIRM_GATE: omitted
- QUALITY_STYLE: speed_with_showcase_quality
