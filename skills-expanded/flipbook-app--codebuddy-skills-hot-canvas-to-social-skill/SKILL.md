---
name: hot-canvas-to-social
description: 端到端把网络热点做成画册并发布成社交图文。先调用 hot-canvas-batch 产出 N 个热点画册（canvas），再基于产出的画册进入 canvas-to-social 完成导出+文案润色+多 tab 填充，最后停在「发布」交给用户。触发词：热点做成抖音、批量发抖音图文、热点画册发抖音、canvas 转抖音批量、热搜一键图文、end-to-end social。
---

# 热点画册 → 社交图文 端到端编排 (hot-canvas-to-social)

## 这是什么
一个**编排 skill**，把两个已有 skill 串起来跑完整链路：

```
WebSearch 热点 → [hot-canvas-batch] 产出 N 个画册 → [canvas-to-social] 导出+润色+多tab填充 → 停在发布
```

它自己不重复实现建册或发布逻辑——而是**按顺序调用**：
1. **`hot-canvas-batch`**（建册，服务自启自关）。
2. **`canvas-to-social`**（导出 + 浏览器自动化填充）。

> 目前发布目标仅支持**抖音**（`canvas-to-social/references/publishing-douyin.md`）。
> 未来新增平台时，导出阶段不变，只需在阶段 3 增加对应平台的填充流程。

## 何时使用
- "收集热点做成画册并发到抖音" / "批量把热搜做成抖音图文" / "一键热点图文"。
- 用户想要从「找选题」到「待发布的抖音草稿」全程自动化，最后人工点发布。

## 唯一铁律（三条，最高优先级）
1. **选题阶段必须过滤政治敏感话题**——只选娱乐/科技/体育/游戏/生活/文化等安全热点。
2. **永远不点最终「发布」按钮**——发布不可逆、对外公开。所有 tab 填好内容、校验、
   停在发布按钮前，把最后一步交给用户。仅当用户明确要求才点「存草稿」。
3. **不要读图**——不用 Read 工具去查看/识别导出的 `.png`。文案一律基于 `文案.md` 的文字
   图说改写，图片只按阅读顺序原样上传；核对上传结果用 `js()` 读 DOM/计数，而非看图。

## 页面易变，每次自更新
抖音创作者中心 DOM/class/文案变化快。阶段 3 的所有浏览器选择器都是**实测快照、可能失效**。
执行时遵循「**先探测 → 失效就按可见文字兜底 → 把新规则用 Edit 回写
`canvas-to-social/references/publishing-douyin.md`（及本文件摘要）**」的闭环，保证下次拿到最新规则。
详见 publishing-douyin.md 顶部「自更新约定」。

## 参数
开工前先和用户确认（用 AskUserQuestion）：
- **N**：做几个画册 / 发几条图文（默认 3，每画册 ≈10-15 张图）。
- **方向**：竖版 portrait（抖音图文推荐）/ 横版。
- 合集：默认全部归入抖音「图解世界」合集（存在就选，不存在则跳过、不新建）。

---

## 阶段 0 —— 选题（你来做，需联网）
用 WebSearch 搜当日热点，挑 N 个流量高且**非政治敏感**的选题。为每个选题抓具体事实
（数字、事件、名称）作为下钻 label。把选题写成 `<root>/themes.json`（结构见
`../hot-canvas-batch/SKILL.md` 中的 `themes.example.json`）。

## 阶段 1 —— 建册（调用 hot-canvas-batch）
跑一条命令，脚本自启服务、建册、自关服务、写历史：
```bash
node ../hot-canvas-batch/scripts/build_canvases.mjs --themes <root>/themes.json
```
（`ORIENTATION`/`DRILL_PER`/`RECENT_DAYS` 等 env 见该 skill。近 90 天同主题会被自动去重。）

建完后取本次产出的 canvasId：
```bash
node ./scripts/latest_canvases.mjs --json
```
它读 `topics-history/` 里**最新一次** run.json，并核对每个 canvas 的 images/ 是否真有图
（`present:true`）。只对 `present` 的 canvas 继续发布。

> 注意：hot-canvas-batch 跑完会**关掉服务**，且历史**不存 url**。发布阶段**不需要**服务在跑
> ——导出脚本直接读 `server/data/canvases/<id>/` 磁盘文件，与服务无关。

## 阶段 2 —— 导出 + 文案润色（可用 subagent 并行）
每个 canvas 互相独立、且都是**纯磁盘操作**（读画册、写导出包、改文案），所以这一阶段
**可以并行**。对每个 canvasId 派一个 subagent（`general-purpose`，在单条消息里并行发起）：

每个 subagent 的任务：
1. 跑导出脚本（仅标准库）：
   ```bash
   # cwd in canvas-to-social skill root
   python3 ./scripts/export_canvas.py <canvasId> \
     --data-root /abs/path/to/app/server/data --limit 35
   ```
   脚本末尾打印 `OUT_DIR=...`（导出目录，含 `images/01-..NN.png` 和 `文案.md`）。
2. **文案润色（口语化）**：读 `文案.md` 的原始百科图说，改写为：
   - **标题 ≤ 20 字**，要有钩子/悬念/数字。
   - **正文 ≤ 1000 字**，口语化、有节奏、能引发互动；末尾用纯文本 `#话题 #话题` 带 3-6 个
     相关话题标签。
   - 把改好的标题+正文写回导出目录下一个 `发布文案.md`（或回报给主流程）。
3. subagent 用 SendMessage 把 `{canvasId, OUT_DIR, 标题, 正文, 图片数}` 回报给 main。

> 字数铁律来自 `canvas-to-social/references/publishing-douyin.md`：标题≤20、正文≤1000、图片≤35。

## 阶段 3 —— 多 tab 填充（串行，共享一个 Chrome）
发布要操作用户**已登录**的 Chrome，所有 tab 共享同一个 CDP 会话，**无法真正并行**——
但可以把 N 条都填好、各占一个 tab，作为「图解世界」待发布分组，最后让用户逐个点发布。

前置：用户已在自己 Chrome 登录抖音；`browser-harness` CLI 可用（用法见
`browser` skill）。

对每个 canvas 的导出包，**依次**执行（细节严格按 canvas-to-social skill 中的 `references/publishing-douyin.md` 的第 1-7 步）：
1. `new_tab("https://creator.douyin.com/creator-micro/content/upload?default-tab=3")`
   —— 直接进发布图文页（比从首页找入口更稳）。`wait_for_load()` 后确认是上传页。
2. `upload_file("input[type=file]", sorted(images/*.png))` 上传（顺序 01..NN）。
3. 标题（≤20）：用 prototype value setter + 派发 input/change。
4. 正文（≤1000）：contenteditable 用 `execCommand('insertText')`；话题写成纯文本 `#词`。
5. **背景音乐（必做）**：音乐入口卡片的真正可点元素是 `.container-right-uW7Pj1`/
   `.action-Q1y01k`，用**原生 `.click()`** 打开抽屉（`click_at_xy` 常无效）。**点之前先确保
   上一步合集下拉已收起**（否则 `.semi-portal` 浮层会盖住音乐入口，命中测试会返回
   `semi-select-option`）。   抽屉打开后扫 `([\d.]+)万人使用`，**按播放量取前 10 首热门候选，
   再 `random.choice` 随机选一首**（不要固定取第一名），hover 后点「使用」，读到「修改音乐」
   即成功。批量发布时维护 `used_songs` 集合跳过已用歌，保证多条 BGM 各不相同。详见
   canvas-to-social skill 中的 `references/publishing-douyin.md` 第 5 步。
6. 合集：先选合集**再**选音乐（避免下拉浮层挡住音乐入口）。用「不选择合集」文字定位
   `.semi-select` 点开，存在「图解世界」就选，否则跳过（**绝不自动新建**）。
7. 校验（读回标题字数/正文字数/图片数/合集名/音乐），定位「发布」按钮但**不点**。

> **步骤顺序建议**：上传图 → 标题 → 正文 →（先）合集 →（后）音乐 → 校验。把音乐放在
> 合集之后，能规避「合集下拉残留浮层挡住音乐入口」这个高频坑。

每个 tab 填完后**保留打开**，进入下一个 canvas 的新 tab。N 个全部填好后，向用户报告每个
tab 的状态清单，并提示：请逐个检查后自行点「发布」。

## 阶段 4 —— 收尾汇报
给用户一张总表：每条 = canvasId / 主题 / 图片数 / 标题 / 正文字数 / 合集 / tab 状态
（已就绪待发布）。明确说明：**没有任何一条被自动发布**，发布权在用户手里。

---

## subagent 用法要点
- **并行**：仅阶段 2（导出+润色）派多个 subagent，单条消息多个 Agent 调用并发。
  每个 subagent 拿到 `canvasId` + `--data-root` 绝对路径 + 字数限制 + 润色要求，自洽完成。
- **串行**：阶段 3（浏览器填充）**不要**派并行 subagent——多个 agent 抢同一个 Chrome CDP
  会互相踩踏。由 main（或单个发布 subagent）顺序操作多个 tab。
- subagent 是无状态的：prompt 里给全绝对路径、canvasId、字数上限、润色风格，别让它去
  猜上下文。

## 常见坑
- **canvas 缺图**：建册阶段 codebuddy planner 偶发 JSON 解析失败会让个别节点没图。
  `latest_canvases.mjs` 的 `imageCount`/`present` 能帮你筛掉空画册；导出 `--limit 35`
  本就只取有图节点的 BFS 顺序。
- **历史无 url、服务已关**：发布不依赖服务，导出脚本读磁盘即可。要预览画册再另起服务。
- **坐标漂移**：浏览器步骤每次按文字/placeholder 重新查询元素，绝不跨步骤复用坐标
  （见 canvas-to-social skill 中的 `references/publishing-douyin.md` 健壮性要点）。
- **别让 subagent 碰发布**：导出/润色可委托，浏览器填充和发布留在主线程顺序做，且永不
  自动发布。
