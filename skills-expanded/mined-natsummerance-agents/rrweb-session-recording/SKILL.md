---
name: rrweb-session-recording
description: |
  基于 rrweb 的网页会话 DOM 级录制与回放集成方案：首帧全量快照 + DOM mutation/用户交互增量事件流，多页面加载串联为单一录制，沙箱化回放与播放器 GUI，rrweb-snapshot 还可独立输出禁用 JS 的静态页面快照。触发场景：用户说"在应用里嵌入用户操作录制"、"做会话回放/session replay"、"复现用户报错时的页面现场"、"把网页状态存成可回放快照"。不适用于：产出供人观看的产品演示视频（走 screen-demo-recorder）、PV/UV 聚合统计类埋点分析。
source_project: rrweb-io/rrweb
tags: [session-replay, dom-recording, rrweb, debugging, user-behavior]
---

# RRWeb Session Recording（DOM 级会话录制回放集成法）

## R (Reading) — 源项目核心设计

> "rrweb refers to 'record and replay the web', which is a tool for recording and replaying users' interactions on the web." —— 四包分工：rrweb-snapshot 将 DOM 及状态序列化为带唯一标识的结构并可单独充当"all Javascript deactivated"的静态 HTML 截图；record 在首帧快照上增量记录 mutations 与交互；replay 重建快照并回放事件列表/流；rrweb-player 提供 GUI（pause/fast-forward/drag-and-drop to play at any time）。"Multiple page loads can be chained together into a single recording."

（来源：https://raw.githubusercontent.com/rrweb-io/rrweb/main/README.md ）

## I (Interpretation) — 方法论骨架

核心洞察：**不录像素录语义**——把页面状态编码为结构化事件流，体积小、可检索、可在沙箱中精确重建。

1. **四包按需组合**：rrweb-snapshot（序列化+重建）/ record（增量事件采集）/ replay（事件驱动重建）/ rrweb-player（播放器 GUI），不必全家桶。
2. **首帧全量 + 后续增量**：先做可序列化 DOM 快照并分配唯一 ID，此后仅记录 mutation observer 捕获的差异与鼠标/输入等交互事件。
3. **跨页面串联**：多次页面加载的事件链成一条完整会话，SPA 跳转不丢上下文。
4. **沙箱回放**：回放在受控环境中重建 DOM（见上游 docs/sandbox.md），录制页脚本不会在回放时执行。
5. **网络层扩展点**：roadmap 的 plugin API 覆盖 XHR/fetch/GraphQL 录制，另有 rrweb cloud 存储引擎做海量会话去重、"token 高效 AI 回放格式"在建。
6. **生态位认知**：Sentry/PostHog/Datadog/Mixpanel/New Relic 等均基于它做 session replay——它是嵌入应用的基础设施库，不是独立桌面软件。

## A1 (Past Application) — 源项目的典型应用

### 案例: 错误监控产品的"报错现场回放"
- **输入**: 在 Web 应用注入 record 侧 SDK，事件流持续上报至自家后端。
- **做法**: 出错时刻向前取固定时间窗的事件列表，replay 侧重建首帧快照后逐事件推进，player UI 让支持人员暂停/拖拽定位问题操作。
- **结果**: Sentry、Highlight.io、Gleap 等产品据此实现"用户是怎么点到报错页"的可视化复现；官方另提供托管后端（rrweb cloud）解决大规模会话的去重存储。

## A2 (Future Trigger) ★ 触发场景

### 用户会在什么情境下需要
1. 问题复现："用户说页面坏了但讲不清点了什么，要在应用里录下他的操作并完整回放"。
2. 行为观察：客服/UX 团队想看真实用户在关键流程（注册/结账/表单）里的逐步操作。
3. 页面状态存档：把某刻网页状态存成可回放快照，或仅需静态快照（禁用 JS 的"DOM 截图"）。

### 语言信号
- "嵌入网页/应用里录制用户操作"
- "会话回放 / session replay"
- "复现用户的报错现场"
- "DOM 快照 / 录制 DOM 变更"

### 与相邻 skill 的区分
- 与 screen-demo-recorder 的区别：本 skill 输出**结构化事件流**，嵌在产品内部，面向开发者与支持人员的精确重建；screen-demo-recorder 输出**剪辑好的 MP4/GIF 视频**，面向外部观众的市场/教学素材。要"程序能回放的数据"来这里，要"人能观看的视频"去那里。

## E (Execution) — 可执行步骤

1. **场景定档** — 明确目的（问题复现/行为观察/状态存档）、目标站点结构与采样策略。完成标准: 写出"在 X 应用的 Y 流程上，以 Z 采样率录制，用于 W"。
2. **依赖引入** — 安装 @rrweb/record 与 @rrweb/replay（或仅用 rrweb-snapshot 做静态快照），核对浏览器兼容。完成标准: 构建通过，bundle 体积对照 README 徽章在预算内。
3. **录制接入** — 初始化 record：首帧全量快照 + 增量监听；配置输入掩码/元素忽略等脱敏项；多页面场景启用会话串联。完成标准: 本地操作一轮产出完整事件序列，敏感字段在事件流中不可读。
4. **传输与存储** — 批量上报自有后端或 rrweb cloud；大流量做去重压缩。完成标准: 断网重连后会话可恢复拼接，存储成本符合预估。
5. **回放与播放器** — 接入 replay + rrweb-player，验证沙箱隔离生效。完成标准: 任一会话可暂停/快进/拖拽定点还原，控制台无回放侧报错。
6. **合规自检** — 确认告知同意机制、脱敏规则覆盖率、留存周期三项。完成标准: 发布清单中同意文案、脱敏配置、保留期限齐备并留档。

## B (Boundary) — 边界

### 不适用场景（≥2条）
- 制作**对外发布的产品演示/教学视频**（缩放动效、光标美化、MP4/GIF 成片）→ 走 screen-demo-recorder。
- 纯**流量统计**（PV/UV、转化漏斗等聚合指标）→ 常规 analytics 即可，无需逐事件回放。
- 自动化测试执行录像 → E2E 框架自带 video/trace 更合适。

### 已知局限 / 失败模式（≥1条）
- 回放保真度受限于事件流：canvas/WebGL 重交互、跨域 iframe、浏览器差异可能导致还原偏差，接入前需对目标页面类型做试点验证；
- 长会话/复杂页面的事件体量可观，需存储层去重兜底；roadmap 中"token 高效 AI 回放格式"尚未落地，不得当作现成能力向用户承诺。

### 隐私红线
- 录制**真实用户会话属于个人信息处理**：必须在隐私政策披露并提供同意/退出机制；"偷偷上线录制、不做任何告知"的请求一律拒绝，可提供低打扰替代（一次性首访告知、抽样录制、匿名化）。
- 默认脱敏不可省略：密码、支付卡号、证件号等输入必须掩码（maskAllInputs 类配置或元素级忽略），回放数据按最小必要设定留存期并严格限权。

## 相关 skills
- contrasts-with: screen-demo-recorder（事件流回放 vs 成品视频）

---

## 审计信息
- **验证**: V1 ✓ / V2 ✓ / V3 ✓
- **蒸馏时间**: 2026-08-25；**来源**: webfetch `https://raw.githubusercontent.com/rrweb-io/rrweb/main/README.md`（本地 upstream 无该仓库，HEAD 直连失败后经 PowerShell 直取 main 分支成功）
