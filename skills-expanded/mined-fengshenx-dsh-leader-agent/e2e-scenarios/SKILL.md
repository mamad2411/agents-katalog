---
name: e2e-scenarios
description: 写浏览器 e2e 场景与排查失败：断言锚、等待预算、失败读数、双向验证、把目标会话放进项目树。要新增/修改 tests/e2e 场景、或 e2e 红了要定位时使用。
whenToUse: 新增或修改 tests/e2e/*.e2e.js、给 UI 行为留可复现证据、或排查一条 e2e 失败时。
---

# 浏览器 e2e 场景

e2e 的判据是「真实宿主 + 真实 chromium 里，可观察行为是否成立」。车道命令、文件职责、场景模板、mock 约定与截图落点见 [docs/e2e-testing.md](https://github.com/fengshenx/dsh-leader-agent/blob/main/docs/e2e-testing.md)；宿主方案的由来与从宿主搬来的确定性规则见[笔记](https://github.com/fengshenx/dsh-leader-agent/blob/main/.agents/notes/implemented/testing/2026-11-04-e2e-host-approach-and-determinism.md)。本技能只讲写场景与排查时的方法。

## 适用场景

- 新增一条场景，要证明某个界面行为在真实宿主里成立。
- 给一个 bug 修完补回归，先让场景在修复前变红。
- 一条 e2e 红了，要区分「数据没到」「渲染错了」「清理挂了」。

## 断言纪律

- **断言外部世界**：DOM 的 class、`getComputedStyle` 的具体属性、磁盘上的 JSON。不读 agent 的自述文本，不拿页面里的推理文字当证据。
- **等状态，不睡时间**。`waitFor()` 轮询到条件成立；locator 用 `contenteditable="true"`、`data-*`、可见文本这类状态条件，让 playwright 自己等。
- **等待预算按正常耗时给**。实测单场景 3–8 秒、元素 1–2 秒到位：首次启动 20 秒、元素状态 15 秒。写 60 秒/90 秒只会让失败多等一整分钟，还把「机器慢」与「等错了元素」混成同一个症状。慢机与 2 核 CI 用 `E2E_BUDGET_SCALE=1.5` 整体放大（测试级上限走 `scenarioTimeout()`，取同一个倍率）。
- **失败要带读数**。元素等待走 `waitForLocator()`：失败时报 locator、目标元素读数（计数、`visible`、边界盒、`display` / `visibility` / `checkVisibility`、宽高）与页面读数（会话行、工作区行、插件元素计数）。目标读数用来分开「不在 DOM」「在 DOM 但 `display:none`」「在 DOM 但零尺寸」——只数 count 时这三种是同一句超时。读数自身限 2 秒，页面主线程卡死时退化成 `{ unavailable }`；自定义读数用 `describePage()`。细节见[e2e 失败预算](https://github.com/fengshenx/dsh-leader-agent/blob/main/.agents/notes/implemented/testing/2026-11-04-e2e-failure-budget.md)。
- **造状态用 seed**：目标状态直接写进数据文件（`<home>/dsh-leader-agent/cards.json`、`projects.json`），让界面去读。靠反复重启、反复点 UI 去凑瞬时态，永远对不齐。
- **标识符必须来自本次运行**：端口、token、会话 id、数据根都从本次实例取，不硬编码上一轮残留的值。

## 双向验证

撤掉修复 → 断言必须变红 → 还原 → 变绿。绿了但撤掉修复也绿，说明断言没守住任何东西。

- 验证的是断言，不是实现：先怀疑断言有没有落在真实可观测量上，再怀疑修复。
- 一次只改一个变量：两个变量同时变，失败原因就分不开。
- 把「撤掉什么、红了哪条、报什么读数」写进 PR；没有读数的「已双向验证」不算证据。

## 失败诊断

操作面（单场景入口、`e2e:report`、负载卫生、已知 flake、超时口径与取证路径）见 [docs/e2e-testing.md 的跑法与失败处理](https://github.com/fengshenx/dsh-leader-agent/blob/main/docs/e2e-testing.md#跑法与失败处理)；本节只讲判据，不重复命令。

1. **先看耗时**：单场景约 10–15 秒，全量按场景数累加。跑了一分钟还没结束，先怀疑某个等待在等不会出现的元素（典型：`lib/client.js` 没构建、会话行没渲染），不是机器慢。别用 `grep` / `head` 过滤输出，`TimeoutError` 里的 locator 就是线索。报错头是「等待失败：…」而不是「等待超时」时，先看页面或浏览器是不是已经关掉、崩了——那不是选择器的问题。测试级上限 90 秒（`scenarioTimeout()`，随 `E2E_BUDGET_SCALE` 放大）；清理链上实例与 mock 卡住会变成带名字的失败，浏览器关闭超时只告警并继续。
2. 先看 `problems`（pageerror / console.error）。本仓出过「圆点不亮」查不出原因的情况，根因是三处空 `catch`：保留会话失败、订阅就绪失败，全都吞掉，界面上只剩一个空心圈。失败必须报告，且同一目标只报一次。
3. **构建过了也可能坏**：改过 `src/client/` 里的 CSS 就先跑 `plugin.e2e.js` 冒烟。`STYLE_TEXT` 这类模板字符串里混进反引号会当场截断模板，剩余正文被当成 JS 表达式，产物里留下未定义标识符——插件在 import 期抛错、整页白屏，症状与「没构建」一模一样（每个等待都超时），而 `node --check`、单测与覆盖率门禁全绿，它们都不做模块求值。冒烟只验「插件能不能挂载」，3–6 秒，红了不必等全套跑完；`problems` 里的原文形如 `dsh-leader-agent: import failed: <标识符> is not defined`。
4. 看 `instance.logs`（子进程 stdout/stderr 全量）与 `mock.requests`：模型请求到底有没有发出来、打到哪个端点、带没带标记。
5. **区分「数据没到」与「渲染错了」**：落盘文件里有没有、DOM 里有没有，分开查；字段不在就是数据层的问题，不在渲染层。
6. **一次性日志优于每帧日志**：首次读数打一条就够，高频刷新会把控制台淹掉。
7. 起不来先看源 profile：`dsh` 不在 PATH、profile 缺 web app bundle、node_modules 没装，报错都会直接说明。

## 搭场景：让目标会话出现在射击位

要点的按钮长在某个会话行上（归档、打开、续聊），而这行出现在左栏需要同时满足三个条件。少一条，界面上什么都不会出现，症状还都一样「等不到」。

1. **只有登记过的 worker 会话进项目树**。`groupSessionsByProject()` 按调用方传入的 `isWorkerSession` 判身份，其余会话一律跳过（`src/host/projects/session-index.js`）——手工 New Session 造的普通会话永远不在项目树下，别指望在它上面点项目内的动作。要在项目树下取证，先让 worker 派工出来（worker 是普通根会话，会话头不带 `origin` 标记，只能按登记判定）。
2. **派工只认项目 leader**。身份来自 `projects.json` 的 `leaderSessionId`，判定读的是进程内镜像（`src/host/projects/service.js` 的 `isLeaderSession()`，镜像由 `loadIndex()` 从注册表填充）。要换 leader：停机 → 改 `projects.json` → 重启，热改文件不会被读到。
3. **mock 用首条用户消息判角色**。`firstUserText()` 含 `MOCK-WORKER-TASK` 就把该会话当 worker 首轮，直接吐文本、永不派工。所以 leader 会话的第一条消息只能带场景标记（如 `MOCK-LONG-REPORT`），worker 标记由 mock 拼进派工 task 里。

路径形式不是坑：项目目录与会话 cwd 都过 `realpath`（`src/host/projects/service.js:23`），`/tmp/...` 与 `/private/tmp/...` 判成同一个目录，不要在这上面找原因。

会话 id 从 `$DSH_HOME/sessions/--<编码后的 cwd>--/<id>` 里按 mtime 取最新，不要硬编码。左栏刷新靠窗口 focus 或整页 reload；`sessionsByProject` 每次调用都现查宿主会话注册表，不缓存，所以 reload 后仍看不到，问题在上面三条里，不在刷新时机。

**一次只改一个变量**。上面三条里任意两条同时变动，失败原因就分不开——本轮踩过：换会话与改项目目录一起做，成功之后把功劳记在了目录上，而真实原因是新会话的首条消息不再带 worker 标记。改一样、验一次、再改下一样。

## 为宣传素材截真实 UI

宣传片要真实感，但不能把断言场景直接当素材：截图是给人看的，不是回归证据。

1. **沿用同一套夹具**：用 `launchE2E()` 起真实宿主 + mock，只在场景末尾额外 `page.screenshot()`；不要为宣传另写一套假 UI。
2. **先 seed 再截图**：把任务标题、状态、槽位直接写进 `cards.json` / `projects.json`，目标画面一次到位。不要靠反复点 UI 凑 20 张卡。
3. **数据要多样**：标题有长有短，状态有进行中/待验收/报错，卡片有 2–3 个槽位；全是一样的卡在成片里会露馅。
4. **视口就是夹具的 `1440×900@1x`**：`launchE2E()` 的 context 固定 `1440×900`、`deviceScaleFactor: 1`，签名不暴露 viewport/scale；`page.setViewportSize()` 只改 viewport，改不了 context 级缩放。截图清晰度上限就是这个分辨率。需要更大画幅时，把截图当素材放进 `promo-stills` 的封面 HTML，按 `--scale 2` 导出构图（放大的是版式，不是截图细节）；关键卡片裁切后在 HTML 里用大字重排。竖屏宣传不把宿主强行改窄，桌面窗口只当上下文。
5. **等状态再截**：等目标卡片/看板可见，不用固定 sleep；截图前可关掉光标 hover，避免高亮入镜。
6. **脱敏**：token、真实用户目录、内部 URL、个人信息不能入镜；用 mock 数据与临时数据根。
7. **输出只进 `.dev/`**：截图与裁切放 `.dev/promo/assets/`，不提交；成片与封面另存交付目录。
8. **图文分工**：整张桌面截图只提供“真实运行”的上下文；手机上要读的标题、槽位、状态用裁切卡片或 HTML 大字重排。

画面怎么组织、旁白怎么对齐，见 [`promo-video`](../promo-video/SKILL.md)。

## 边界

- 不为了 e2e 改生产代码：场景用现有 class 与 role；需要新选择器时那是一次产品决定，不夹带。
- 不把截图当断言：截图只解释「当时界面上是什么样」，回归靠断言。
- 不覆盖原生控件、浮层像素位置、WebKit / Firefox：这些走人工取证，PR 里如实标注。
- 不加 `--test-force-exit`：它会把漏清理从「挂住/超时变红」变成「绿着通过 + 孤儿进程」；有界清理见[e2e 清理笔记](https://github.com/fengshenx/dsh-leader-agent/blob/main/.agents/notes/implemented/testing/2026-11-04-e2e-shutdown-bounded.md)。
