---
name: animation-explainer
description: 把一个技术概念/流程/系统转化为"剧场式"动画 HTML — 多场景 + 自动播放 + 章节导航 + 旁白与真实代码。适用于网络协议、底层原理、算法、架构原理等"看不见但需要看见"的主题。单文件 HTML，无构建步骤。
triggers:
  - "做一个 X 的动画演示"
  - "把 X 讲清楚，用动画的形式"
  - "X 的底层是怎么发生的"
  - "用动画解释 X 的工作原理"
---

# Animation Explainer · 知识动画化技能

## 这个技能是什么

输入一个主题（"打开浏览器到屏幕上像素的全过程"、"一个 SQL 查询是怎么被执行的"、"TLS 1.3 握手"、"V8 是怎么编译 JS 的"），输出一份**单文件 HTML 动画演示**，能在任意浏览器打开播放。

参考实现：`examples/browser-request/index.html`。**任何新主题都从复制这个文件开始**，而不是从零写。

## 它不是什么

- ❌ 不是幻灯片：每节有 SVG 动画，元素会移动、闪烁、依次出现
- ❌ 不是单页长滚动信息图：内容被切成离散场景，自动按节奏播放
- ❌ 不是 PPT 截图导出工具：纯 HTML+SVG+CSS+原生 JS，没有打包步骤
- ❌ 不是通用 explainer 框架：只解决一类问题 — **多场景剧场式技术解说**

---

## 核心结构（必须遵守）

### 文件
- **单一 `index.html`**，所有 CSS/JS/SVG 内联。零外部依赖（除了 Google Fonts，可选）。
- 复制 `examples/browser-request/index.html` 改，**不要从空文件开始**。

### 页面骨架（grid）
```
┌─────────────────────────────────────────────┐
│ 顶栏: brand + chips + 进度条 + N/总数        │  ← 章节导航
├─────────────────────────────────────────────┤
│  舞台 (SVG 全屏)        │  旁白面板          │
│  ─ 当前场景的动画区     │  - 节号 + 大标题   │  ← 主体（1.55 : 1）
│  ─ 角落计时             │  - 正文（带高亮）  │
│                         │  - 代码块（真实）  │
├─────────────────────────────────────────────┤
│ 控件: ◀ 上一节  ⏸/▶  下一节 ▶  ↻  + 章节名 │  ← 控件
└─────────────────────────────────────────────┘
```

### DOM 约定
- 每个场景一个 `<svg class="scene" id="scene-N">`，**只有 `.active` 那个显示**
- 每个旁白一个 `<div class="pane" data-pane="N">`，配对切换
- JS 用 `CHAPTERS` 数组驱动一切，每项必须有 `{ id, title, duration, narration }`
  - `narration` = 中文口播稿（**必填**，详见"口播旁白系统"那节）
  - `duration` = TTS 开时是进度条参考；TTS 关时是切换间隔
- 切换 = 切 `.active` + 调用 `runScene(N)` + 触发口播

### 必备控件
- 上一节 / 下一节 / 播放暂停 / 重播本节 / 🔊 旁白开关
- 键盘: ← → / Space / R / **M（静音切换）**
- 章节 chip 可点击直接跳转
- 顶部进度条 + N/总数标签
- 角落 SCENE 编号 + `mm:ss / mm:ss` 计时
- **自动推进由口播结束驱动**，不是固定 setTimeout（详见"口播旁白系统"那节）

---

## 工作流（每次接到任务执行这 6 步，可选第 7 步导出 MP4）

### 步骤 1 · 拆主题为场景

**约束：3–8 个场景**。少于 3 节没必要做动画；多于 8 节注意力分散。

每个场景 = "一个核心概念 + 一个能动的视觉隐喻"。先在脑子里过一遍，写出来：

```
场景 1 · [标题]
  核心概念: [一句话能讲完的那个点]
  视觉隐喻: [打字机 / 飞行的包 / 流水线 / 树 / 时序图 / ...]
  真实数据: [命令输出 / 报文 / 日志 / 耗时数字]
  时长: [6000~9000ms]
```

**好的隐喻是排他的**。"DNS 是电话簿" ✅ 一眼就懂；"DNS 是分布式服务" ❌ 太泛。

### 步骤 2 · 选择视觉模式（按场景类型）

复用 demo 里已有的 5 种基础模式，不要每节都发明新的：

| 类型               | 用途                          | demo 里在哪          |
| ------------------ | ----------------------------- | -------------------- |
| **实物 mockup**    | 起点/终点、用户看得见的东西   | scene 1（浏览器壳）  |
| **节点 + 飞包**    | 多方协调、网络拓扑、消息流转  | scene 2（DNS 递归）  |
| **时序图**         | 两端协议、握手、状态转移      | scene 3/4/5/7（TCP/TLS/HTTP） |
| **流水线 + 日志**  | 内部处理、阶段流转、副作用    | scene 6（服务器内部）|
| **结构树 / 合并**  | 数据结构、编译、解析          | scene 8（DOM/CSSOM） |

需要新隐喻时，先问"能不能用以上 5 种里的 1 种讲清楚"。

### 步骤 3 · 写真实数据，不要编

旁白里的代码块是教学价值最高的部分。**所有命令、报文、日志、时间都要真实**：

- 命令: 真的运行 `dig`、`curl -v`、`tcpdump` 输出
- 报文: 用 HTTP/1.1 真实格式（动词 路径 协议\r\n + Header\r\n + ...）
- 时间: 用合理的 RTT/TTFB 范围（不要写 0ms 或 999ms）
- 日志: 抄真实框架的输出格式（Rails / Nginx / Postgres 各有特征）

虚构的报文/日志读者一眼就知道是 AI 编的，整个 demo 的可信度崩塌。

### 步骤 4 · 写动画函数（每场景一个）

每个 `scene N()` 函数干两件事：
1. **重置元素**到初始状态（`resetEl('id1','id2')`）
2. **按时间序列**调用 `showEl(id, delayMs)` 或自己写 RAF 动画

复杂运动（飞行）用 RAF + cosine easing：

```js
const start = performance.now(); const dur = 2400;
function step(ts){
  const p = Math.min(1, (ts - start) / dur);
  const ease = 0.5 - Math.cos(p * Math.PI) / 2;  // ease-in-out
  el.setAttribute('transform', `translate(${x0 + dx * ease}, ${y0})`);
  if (p < 1) requestAnimationFrame(step);
}
requestAnimationFrame(step);
```

简单显隐用 `showEl(id, delay)`（CSS transition 已挂好）。

**动画总时长**应 ≤ 口播时长（10–20s）。动画演完后画面应"稳"住等口播读完，给观众回看代码的时间 —— 实际推进时机由口播结束驱动，详见下一步和"口播旁白系统"那节。

### 步骤 5 · 写口播稿 + 生成 MP3

给 `CHAPTERS` 每项补 `narration` 字段（口播稿写法见"口播旁白系统"那节）。然后跑一次：

```bash
node scripts/generate-audio.mjs examples/<your-demo>
```

脚本会自动从 HTML 抠出 narration 字段，生成 `audio/scene-N.mp3`（默认云希男声）。重新打开 demo，HTML 会自动检测并使用 mp3 旁白；没生成 mp3 会回退到浏览器原生 Web Speech API。

第一次跑前要装依赖：`npm install`。

### 步骤 6 · 自检（反 AI Slop 清单）

提交前逐项核对：

- [ ] 没有"作为一个 AI 助手" / "希望对你有帮助"这类废话
- [ ] 没有 emoji 泛滥（一节最多 1 个，且作为视觉锚点而不是装饰）
- [ ] 代码块的命令是真的能跑的
- [ ] 时间数字是合理范围（不是占位的 100ms / 1000ms）
- [ ] 没有用 `<div>` 堆出"动画"（必须是真的会动）
- [ ] 每个场景结束时画面"稳"，给读者读完代码的时间
- [ ] 暗色背景不刺眼（不要纯黑 #000，用 #060912 这种）
- [ ] 字体用 Inter + JetBrains Mono，不要 system-ui 凑合
- [ ] 浏览器打开后能键盘 ← → / Space / M 操作
- [ ] 主题专业术语都准确（"三次握手"不写成"三次连接"）
- [ ] `.codeblk` 的 CSS 有 `white-space: pre; tab-size: 2;`（否则代码挤一行）
- [ ] `CHAPTERS` 每项都有 `narration` 字段，没漏节
- [ ] 口播稿是真口语（不会读出"等" "之" "乃"这种书面字）
- [ ] `audio/scene-N.mp3` 已生成
- [ ] 切换章节是按口播结束驱动，不是 `setTimeout(duration)` 硬切
- [ ] 控件区有 🔊 按钮 + M 键绑定

### 步骤 7 · 人工审核 + 导出 MP4（可选）

前 6 步走完、在浏览器里看过完整 demo、觉得满意后，再导出 MP4。这一步是**人工 in-the-loop**：不审核就导出会浪费几分钟跑 Playwright，最终发现某节口播错字或动画卡顿，还得重跑。

```bash
node scripts/export-video.mjs examples/<your-demo>
# 或：npm run video:<demo-name>
```

输出 `<your-demo>/video.mp4`（1280×800 30fps，5MB / 2 分钟左右）。可以直接发微信、抖音、B 站、知乎。

第一次跑前要装浏览器：`npx playwright install chromium`（约 200MB，只装一次）。

实现细节见下方"视频导出"那节。

---

## 设计系统（颜色 / 字体 / 间距）

### 颜色（5 个语义槽，按需选）

| Token       | 值       | 语义                         |
| ----------- | -------- | ---------------------------- |
| `--cyan`    | #22d3ee  | 客户端 / 主线 / "去"的方向   |
| `--violet`  | #a78bfa  | 服务端 / 系统 / "回"的方向   |
| `--lime`    | #a3e635  | 代码字符串 / 成功            |
| `--amber`   | #fbbf24  | 状态码数字 / 中间步骤        |
| `--rose`    | #fb7185  | Paint / 警告 / 危险          |
| `--emerald` | #34d399  | 最终成功 / 200 OK            |

一个场景里**最多用 3 种**主色，其他降到 `--text-dim` / `--muted`。

### 字体（已在 demo `<head>` 引入）

- **Inter** — UI 正文
- **Inter Tight** — 大标题（h2）
- **JetBrains Mono** — 所有代码、日志、抓包、技术标签

### 间距 / 圆角

- 控件按钮: `padding: 7px 13px`, `border-radius: 8px`
- 大卡片: `border-radius: 16px`（var(--radius-lg)）
- 中卡片: `border-radius: 10px`
- 网格背景: 48×48px 极淡，营造"工程感"

### 代码块（重要）

旁白里的 `.codeblk` **必须**有 `white-space: pre; tab-size: 2;` —— 否则 HTML 默认把所有空白（含换行）折叠成单个空格，整段代码会挤成一行。模板已带上，从模板出发就 OK；从老 demo 复制要确认这条 CSS 在。

```css
.codeblk{
  /* ...其它... */
  white-space: pre;        /* ← 必须 */
  tab-size: 2;             /* ← 缩进对齐 */
  -moz-tab-size: 2;
  overflow: auto;          /* 长行水平滚动 */
  max-height: 240px;       /* 限高度，超出垂直滚动 */
}
```

SVG `<text>` 元素由 y 坐标硬定位，行间距建议 **font-size × 1.45**（如 11px 字号配 16px 行距、12px 字号配 18px 行距）。

---

## 口播旁白系统（每个 demo 默认带上）

**为什么**：动画 + 真人口播 = 真正的科普视频体验。只看不听，单场景的注意力撑不住 20 秒。

### CHAPTERS 数据结构

```js
const CHAPTERS = [
  { id:1, title:"...", duration:11000,
    narration:"一切从一行字开始。打开一个 vue 文件……" },
  // ...
];
```

### 口播稿写法（决定听感，比语音引擎本身更重要）

| 要求                       | ✅ 好                                              | ❌ 差                                                  |
| -------------------------- | ------------------------------------------------- | ----------------------------------------------------- |
| 3–5 句，每句 ≤ 25 字       | "TCP 是可靠的传输协议。在发数据前要先建立连接。"   | "TCP（Transmission Control Protocol）是一种面向连接的、可靠的、基于字节流的传输层通信协议。" |
| 口语化，不照搬旁白         | "reactive 不复制对象，而是用 Proxy 把它包起来"     | "reactive 函数返回的并非原对象的副本，乃是一个 Proxy 实例" |
| 避免符号污染朗读节奏       | "把模板、脚本、样式三段塞在一起"                   | "把模板（template）、脚本（script）、样式（style）塞在一起" |
| 专业术语**不翻译**         | "Proxy 拦截器"、"render 函数"                      | "代理拦截器"、"渲染函数"（TTS 读中文易出错）           |
| 时长 10–20s（云希默认语速）| —                                                 | —                                                     |

### 双轨实现：MP3 优先 → Web Speech 兜底

```
打开 demo
  ├─ 探测 audio/scene-1.mp3 能否加载（1.5s 超时）
  ├─ 能加载 → 用 mp3（edge-tts 预生成的云希等 Neural voice，质量好）
  └─ 不能加载 → 回退 Web Speech API（系统自带 voice，质量一般但零依赖）
```

带来的好处：
- 删掉 `audio/` 目录，demo 仍可用（用系统 voice）
- 改了 narration 文案，重跑生成脚本即可
- 本地 `file://` 双击也能工作（Audio 元素支持同目录文件）

### MP3 生成（edge-tts，免费）

```bash
# 一次性安装
npm install

# 给某个 demo 生成 mp3（默认 voice：云希男声，rate +5%）
node scripts/generate-audio.mjs examples/<demo-name>

# 换 voice
node scripts/generate-audio.mjs examples/<demo-name> --voice=zh-CN-XiaoxiaoNeural

# 调语速
node scripts/generate-audio.mjs examples/<demo-name> --rate=+10%
```

中文 Neural voice 推荐：

| voice                  | 性别 | 风格     | 用途                |
| ---------------------- | ---- | -------- | ------------------- |
| **YunxiNeural**（云希）| 男   | 年轻清爽 | **技术解说默认**    |
| YunyangNeural（云扬）  | 男   | 新闻播报 | 历史 / 综述         |
| YunjianNeural（云健）  | 男   | 浑厚     | 长篇教学            |
| XiaoxiaoNeural（晓晓） | 女   | 温柔标准 | 通用                |
| XiaoyiNeural（晓伊）   | 女   | 活泼年轻 | 趣味科普            |

脚本逻辑：用正则从 demo 的 `index.html` 抠出 `CHAPTERS` 数组里的 `narration: "..."` 字符串，逐节生成 `audio/scene-N.mp3`。

### 自动推进：必须按口播结束驱动

**错误做法**（早期 demo 的 bug）：

```js
// ❌ 用固定 duration 切下一节 — 口播没说完就被打断
setTimeout(() => goTo(i+1), CHAPTERS[i].duration);
```

**正确做法**：

```js
const ADVANCE_BUFFER_MS = 1200;   // 口播结束后停留多久再切下一节
const SAFETY_MAX_MS     = 60000;  // 兜底：若口播 onEnd 没触发，最长 60s 强制推进

function startCurrentScene(){
  state.sceneStart = performance.now();
  const text = CHAPTERS[state.index].narration;
  if (state.ttsEnabled && text) {
    scheduleAdvance(SAFETY_MAX_MS);                // 兜底
    speak(text, state.index, () => {               // ← 真正的推进信号
      if (state.playing) scheduleAdvance(ADVANCE_BUFFER_MS);
    });
  } else {
    scheduleAdvance(CHAPTERS[state.index].duration); // 静音回退到 duration
  }
}
```

`speak()` 接收 `onEnd` 回调，挂在 `audio.onended` / `utterance.onend` / `onerror` 上 —— **失败也触发推进**，不会卡死。

### 三个关键防坑细节

**1. `stopSpeak()` 主动停止时，要先卸掉 `onended` 监听器**

```js
function stopSpeak(){
  if (currentAudio) {
    currentAudio.onended = null;   // ← 关键
    currentAudio.onerror = null;
    currentAudio.pause();
    currentAudio.currentTime = 0;
    currentAudio = null;
  }
  if ('speechSynthesis' in window) speechSynthesis.cancel();
}
```

否则 `pause()` 之后浏览器仍可能触发 `ended`，被误判为"自然结束"导致莫名切页。

**2. 初始化用 `state.playing = true; goTo(0)`，不是 `goTo(0); play()`**

```js
// ✅
state.playing = true;
updatePlayBtn();
goTo(0);
```

后者会在 goTo 里 speak 一次（无 onEnd），play 里再 speak 一次（带 onEnd）—— 第一个 mp3 刚开播就被第二次调用打断。

**3. Audio 引用要锁住，回调里判等**

```js
const a = new Audio(`audio/scene-${idx+1}.mp3`);
currentAudio = a;
a.onended = () => {
  if (currentAudio === a) currentAudio = null;  // ← 防旧实例污染
  onEnd && onEnd();
};
```

防止用户连按下一节时，上一个 audio 的延迟 ended 事件污染新场景的状态。

### Web Speech 兜底实现

```js
function webSpeak(text, onEnd){
  if (!('speechSynthesis' in window)) { onEnd && onEnd(); return; }
  speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(text);
  u.lang = 'zh-CN'; u.rate = 1.05;
  if (cnVoice) u.voice = cnVoice;
  u.onend   = () => { onEnd && onEnd(); };
  u.onerror = () => { onEnd && onEnd(); };  // 失败也推进
  speechSynthesis.speak(u);
}
```

`cnVoice` 在页面初始化时挑选，优先级：Premium/Enhanced/Neural 中文 > 任意中文 > null。

---

## 视频导出（MP4）

**适用**：human-in-the-loop 工作流 —— 浏览器里审核通过后，一键导出可分发的视频文件。

### 命令

```bash
# 一次性安装（第一次跑前）
npm install
npx playwright install chromium

# 导出某个 demo
node scripts/export-video.mjs examples/<demo-name>
# 或：npm run video:<demo-name>

# 自定义分辨率 / 帧率
node scripts/export-video.mjs examples/<demo-name> --width=1920 --height=1080 --fps=60
```

默认输出 `<demo-name>/video.mp4`：1280×800 30fps，H.264 + AAC，约 5MB / 2 分钟。

### 实现原理

```
Playwright headless Chromium 加载 HTML
   ↓
recordVideo 录制 WebM（无音轨 — Playwright 的限制）
   ↓
ffmpeg 把每节 mp3 串起来 + 节间 1.2s 静音（对齐 ADVANCE_BUFFER_MS）
                            + 头部 1s pre-roll（对齐 autoplay 启动延迟）
   ↓
ffmpeg mux WebM + 音轨 → MP4（H.264 + AAC + pix_fmt yuv420p + faststart）
```

`pix_fmt yuv420p` 是 QuickTime / 微信 / 抖音兼容性的必备；`faststart` 让 mp4 头部前置，浏览器边下边播。

### 同步约束（必须理解）

画面切换由 HTML 内的 `audio.onended` 驱动；音轨是脚本按 mp3 真实时长 + ADVANCE_BUFFER 预先拼好的。两者用同样的时间常数（1.2s），所以**大体同步**。

**轻微漂移可能出现**（一般 < 0.5s，整段不超过 1s），来源：
- 每次 `new Audio().play()` 有 100–300ms 加载延迟，在录制中累积；脚本预拼的音轨没这延迟
- 浏览器渲染抖动

如果漂移肉眼可见到影响阅读：
- 重跑一次（Chromium 缓存预热后第二次通常更准）
- 调大 `PRE_ROLL_S`（脚本顶部）让首句晚一点开始
- 若仍不准，把脚本改成"按 console.log 时间戳对齐"的高级模式（暂未实现）

### 提交策略

**不要把 mp4 提交进 git**：
- 体积大（5MB+/demo），每改一次都要重新生成
- 已在 `.gitignore` 排除（`examples/*/video.mp4`）
- 视频是"派生产物" —— 需要的人本地跑 `npm run video:<demo>` 即可

要分发的 mp4 单独上传（飞书 / 微信文件 / B 站 / 抖音）。

---

## 输出位置约定

```
examples/
  <kebab-case-topic>/
    index.html             # 主文件（单文件 HTML，含所有 CSS/JS/SVG）
    audio/                 # TTS 旁白（edge-tts 生成，跟 demo 一起提交）
      scene-1.mp3
      scene-2.mp3
      ...
      scene-N.mp3
    video.mp4              # 可选 · 导出的视频（不入 git，本地按需生成）
```

例如：`examples/sql-query-execution/index.html`、`examples/git-merge/index.html`。

- `audio/` 可选 —— 删掉后 HTML 会自动回退到浏览器原生 Web Speech API，质量差但能听
- `video.mp4` 可选 —— 是导出产物，只在要分发时本地生成

---

## 常见任务的拆解参考

收到主题时，可以先比对一下是否属于以下类型：

| 主题类型           | 场景拆解模式                                         |
| ------------------ | ---------------------------------------------------- |
| **网络协议**       | 起因 → 寻址 → 连接 → 加密 → 请求 → 响应 → 解析       |
| **编译/解释器**    | 源码 → 词法 → 语法 → AST → 优化 → 字节码 → 执行      |
| **前端框架原理**   | SFC → 编译 → 响应式（reactive/track/trigger）→ VNode → Diff → Patch |
| **数据库查询**     | SQL → 解析 → 优化器 → 执行计划 → 索引扫描 → 聚合     |
| **构建工具**       | 入口 → 依赖图 → 编译 → 打包 → Tree shaking → 输出    |
| **操作系统**       | 用户态调用 → 系统调用 → 内核处理 → 硬件 → 返回       |
| **加密算法**       | 明文 → 分组 → 轮函数 → 密钥扩展 → 密文 → 解密验证    |
| **分布式协议**     | 提议 → 投票 → 多数派 → 提交 → 通知 → 状态同步        |

---

## 与花叔 Design / 前端设计技能的关系

- 这个 skill **专注于教学性技术动画**，更窄、更程式化
- 视觉品味遵循 `frontend-design` / `huashu-design` 的反 AI slop 原则
- 不要为每个 demo 重新设计颜色/字体；用本 skill 的 design token

---

## 维护规范

- 每完成一个新主题的 demo，把它的章节拆解写进上面的"常见任务"表
- 发现新的视觉模式（不在已有 5 种里）且复用过 2 次以上，**沉淀到 templates/**
- demo 文件之间**不共享代码**（保持单文件可分发的属性），但**共享模式**
- **提交前必跑** `node scripts/generate-audio.mjs examples/<demo>` 生成 mp3，让 demo 默认带高质量口播
- 改了某节 narration 后重跑生成脚本（脚本会整体覆盖 audio/ 目录，单节增量没必要）
- `audio/` 目录建议跟着 demo 一起提交 — 约 100KB/节，8 节 < 1MB，比让用户自己装 npm + 跑脚本省事
- `video.mp4` **不进 git**（已在 .gitignore 排除），需要分发时本地 `npm run video:<demo>`
- 输出位置约定下增加 `audio/scene-N.mp3` 子结构
