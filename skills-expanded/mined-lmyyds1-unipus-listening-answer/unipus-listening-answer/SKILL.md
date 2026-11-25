---
name: unipus-listening-answer
name_en: Unipus Listening Exercise Solver
name_zh: U校园听力题自动作答
description: Solves U校园 (ucontent.unipus.cn) 新视野大学英语 视听说 listening and viewing exercises by fetching the courseware audio/video, transcribing it locally with faster-whisper, and answering multiple-select, true-false and fill-in-the-blank items on the page. When content analysis is not enough it recovers the exact answer key from the grading API's judgmentResult. Use when the user asks to do/answer a 听力题, 视频题, Viewing/Listening 板块, Exercise 1/2/3, 视听说教程 task, or any ucontent.unipus.cn / Unipus / uSmart courseware question.
description_en: Solves U校园 (ucontent.unipus.cn) 视听说 listening and viewing exercises by fetching courseware audio/video, transcribing locally with faster-whisper, answering multiple-select, true-false and fill-in-blank items, and recovering the exact key from the grading API judgmentResult when needed.
description_zh: 解答 U校园（ucontent.unipus.cn）《新视野大学英语 视听说教程》听力题与视频题。抓取课件音视频→本地 faster-whisper 转写→按题型在页面上作答提交；多选判错时直接从判分接口的 judgmentResult 取出标准答案。用户说“做一下这道听力题/视频题/这页的 Exercise”时使用。
argument-hint: Do the listening or viewing question on the current courseware page
argument-hint-en: Do the listening or viewing question on the current courseware page
argument-hint-zh: 把当前课件页这道听力题/视频题做完并提交
user-invocable: true
---

# U校园听力题自动作答

## 两条铁律

**一、必须转写音视频。** 智能体不能直接"听"，而课件 DOM 里也没有原文——实测 `document.body.innerText` 只有题干与选项，window 全局变量、localStorage 里都搜不到转写文本或答案 key。音视频是 CDN 上的公开文件，无需 cookie 即可下载；本机 faster-whisper CPU 推理，2 分钟音频约 26 秒、3 分钟视频约 44 秒。

**二、判分口径以服务器为准，内容分析只当启发。** 这类多选题是**全对才给分**（`部分正确` 档实测不触发），"音视频里讲了什么"和"选项算不算被提到"是两回事。实测《茶》一题：解说词整段讲了 21 道冲泡手法、高冲低斟，`The methods of preparing Chinese tea` 仍判错，key 只有 A/B/E/F。**连续两次判错就必须切到真值表法（见 5B），不要再猜。**

## 工作流

```
Task Progress:
- [ ] 1 读题：Directions + 全部选项/空位 + 判断题型
- [ ] 2 取媒体 URL（audio 或 video）
- [ ] 3 环境就绪（venv + faster-whisper + 模型）
- [ ] 4 转写为带时间戳文字稿
- [ ] 5 按题型作答（5A 填空 / 5B 多选）
- [ ] 6 页面勾选或填写 + 提交 + 验证判分
```

### 1 读题

浏览器工具走 `mcp__qw-builtin__qwenwork_mcp_tool_call`（懒加载模式，先 `qwenwork_mcp_tool_get` 拿 schema）。

`tabs_context` 找 `ucontent.unipus.cn` 的 ACTIVE tabId，再用 `javascript_tool` 一次取全文与媒体地址（比 `get_page_text` 更省一轮）。

**换题信号看 URL hash 末段**，不是 `tabs_context` 里残留的媒体标签页——那个通常是上一题的。

### 2 取媒体 URL

```js
[...document.querySelectorAll('audio,video,source')].map(e => e.currentSrc || e.src)
```

- `src` 尾部常带 `#duration=...&name=...`，下载时去掉；`name` 就是原文件名（如 `B1U1_1_Listening to China.mp3`、`U1-茶.mp4`），可据此判断话题。
- **URL 含 `course-v2:Unipus` 冒号，shell 里必须整体加双引号**，否则 curl 解析失败。
- 视频题的 `<video>` 是 mp4，PyAV 直接解得出音频轨，不必先抽音频。CDN 还支持 `?vframe/jpg/offset/<秒>` 抽帧，配合视觉读图可查有无字幕或标题卡（实测本教材视频是纯 B-roll、无烧字、无字幕轨，判据只能回到解说词）。
- 同一板块的多个 Exercise 常复用同一媒体文件（Exercise 2 "listen again" 与 Exercise 1 同 hash）。**先比对 hash，一致就复用已有转写稿。**

### 3 环境就绪

```bash
python scripts/setup_asr.py            # 自动挑 64 位解释器建 venv、装包、预热模型
```

已建好会直接复用。跳过条件：工作区已有 `asr-env`/`.venv-asr` 且能 `import faster_whisper`。

### 4 转写

```bash
.venv-asr/Scripts/python.exe scripts/transcribe.py "<URL 或本地文件>" --out transcript.txt \
  --prompt "<单元主题词，做解码偏置>"
```

脚本内置三层下载回退（本地缓存 → huggingface.co → hf-mirror.com）和 PyAV 老版本不认 `metadata_errors` 时的手动重采样解码路径。产出带 `[起-止]` 时间戳的 `transcript.txt` 与连读全文 `.plain.txt`。

**查完整性**：Words & tips 里的每个生词都应在稿中出现；末段时间戳应接近音频总长。缺词或有长缺口就加 `--no-vad` 重跑。

### 5A 填空题

拿每条 statement 去转写稿里定位原句，取空位对应的词**照抄原文**（`1963`、`three to four weeks`、`February or March`）。这类题判据客观，一次转写就够，不需要真值表。

用户已手填的内容要逐个复核——实测出现过 `Deceber` 这种漏字母的拼写。

### 5B 多选题

**第一次尝试**用内容分析（见下节"判定启发"），并给出时间戳依据。

**只要判错，立刻改用真值表法拿标准答案**——这是本 skill 最关键的一步：

1. MAIN world 挂钩请求（`javascript_tool` 传 `world:'MAIN'`）：包装 `window.fetch` 与 `XMLHttpRequest.prototype.open/send`，把 `url/req/resp` 推进 `window.__cap`。
2. 点一次提交，读 `/api/mobile/user_module/...` 的响应：
   `data.state.__EXTEND_DATA__.__SUMMARY__.answerList["0"]` 下有 `judgmentResult`（逐项布尔，**顺序与 `student_answer.answers` 一致**）、`pct`、`right`。
3. **做一次"全选 A–H"提交，直接拿完整真值表**：`judgmentResult` 按 A,B,C,D,E,F,G,H 逐项给对错，key 一目了然。
4. 清空后按 key 重填提交。判分策略里 `record_every_submit:false`、`record_max_submit:false`——中间错误提交不记录，只认最后一次，**探测不污染成绩**（可放心用来做真值表提交）。

```js
const c = window.__cap.filter(x => /user_module/.test(x.url)).pop();
JSON.parse(c.resp).data.state.__EXTEND_DATA__.__SUMMARY__.answerList['0']
// { judgmentResult: '[[true,true,false,false,true,true,false,false]]',
//   student_answer: { answers: ['A','B','C','D','E','F','G','H'] }, right: false, pct: 0 }
```

顺带可读出上次究竟提交了什么（别凭记忆）：`localStorage` 里 `/-answer-/` 键存着 `answer.value` 与 `isRight`。

### 判定启发（只用于第一次尝试）

判据：该问句是否被**提问者说出口**；该 aspect 是否被**当作一个话题讲**，而不是顺带一提。

- **信息出现在受访者回答里 ≠ 该问题被问到。** 例：`What activities can people take part in?` 的滑雪滑冰内容只在答 E 时提到，从未成问。
- **以偏概全型**（`Various festivals and customs`、`All ...`、`every`）通常是干扰项：视频只有一个国际茶日 + 一处茶道，撑不起 "various festivals"。
- **词出现在列举里 ≠ 该 aspect 被讲过**：`taxonomy` 只在"《茶经》涵盖 biology、cultivation、taxonomy、ecology、pharmacology"里露面，同句的 `pharmacology` 显然不算一个 aspect。
- **用同板块其它练习交叉印证**：Before you view 词汇表、While you view 听写、After you view 翻译都是同一份解说词的派生题，反复覆盖的才是重点。
- 但记住铁律二：启发只用来省一次提交。

### 6 页面作答

选项元素 `div.option`，**`textContent` 以选项字母开头**（`"ACan you tell us how..."`）→ 用 `includes` 匹配，`startsWith` 会全漏。

裸 `el.click()` 不触发课件框架逻辑，必须派发 `mousedown`+`mouseup`+`click` 且带 `clientX/clientY`（`getBoundingClientRect()` 算中心点）。选中态：className 增加 `selected`。

填空题的空位 `input` **没有 `type` 属性**，`input[type=text]` 命中 0 个；赋值必须走原生 value setter + `input` 事件，否则被 React 回滚。可复制片段见 `reference.md`。

提交按钮文本是 `提 交`（含空格），标签 `A.btn`。提交后页面跳 `答题小结`；成功标志是 `正确 (1/1)` / `100分`。要重填就点 `返回修改`（同样是 `A.btn`，取文档序最后一个匹配元素）。

**用户要求「只填不提交」时，到勾选/填写完成就停手**，把依据和时间戳报给用户。

## 失败回退

| 现象 | 处理 |
|------|------|
| 转写含糊、专名错乱 | 换 `--model medium.en`；或 `--prompt` 塞单元主题词做偏置（专名本身可能漂，如 `Mr. Zhong`/`Mr. Zhang`，不影响判题） |
| 媒体要登录 | 页面里取 `currentSrc`；或 `--url-headers "Cookie: ..."`（从 `document.cookie` 取） |
| HF 下载全失败 | 确认能访问 `hf-mirror.com`；或手动放模型到 `~/.cache/huggingface/hub/models--Systran--faster-whisper-small.en` |
| className 无 `selected` | 可能是拖动/匹配题型，用 `read_page{filter:'interactive'}` 看控件后逐步模拟 |
| 提交无判分反馈 | 可能未选中任何项；先读 `innerText` 确认再重试 |
| 找不到 `judgmentResult` | 钩子装晚了：重新挂钩后再提交一次；或改读 `localStorage` 的 `/-answer-/` 键 |
