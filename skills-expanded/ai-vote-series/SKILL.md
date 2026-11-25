---
name: ai-vote-series
description: AI 观众投票动画连载：一个原创卡通主角，N 天后有件大事（第一次相亲、同学聚会、面试……），每天一集，每集结尾让观众在评论区二选一，票多的下一集改掉、改了不变回去，第二天观众回来看结果。画面全部用代码画（Canvas 2D，逐帧渲染），角色靠状态文件固定、每集不变脸；旁白用用户自己的克隆声音（火山引擎，可先用 edge-tts 占位），逐词对齐出大字幕和嘴型；配乐音效也是代码合成。用户说「做一个像 30daystofix 那样的号」「观众投票的动画连载」「每天一集让评论区决定」「出第 N 集，上集赢了 XX」「做 Day N」，或者要改某一集的台词、画面、投票选项时使用，哪怕没提 Skill 名字。Make a daily audience-vote cartoon series (30 days to X), code-animated with a persistent character state, in your own cloned voice.
---

# AI 观众投票动画连载

一个原创卡通主角，30 天后有件大事。每天一集（40–50 秒，竖屏 9:16），结尾二选一，评论区票多的下一集改掉，改了就不变回去。演示：`demo/30DaysToTheDate_Day1.mp4`（Leo，30 天后第一次相亲，英文，作者本人的克隆声音）。

## 0. 先说清楚

- 用用户的语言和他说话；视频语言按 `series.json` 的 `lang`（演示是英文）。
- **原创**：格式来自外网 @30daystofix 那类号（The Glow Up Project），只学格式。不做它的主角、「同学聚会」设定、面板文字和封面字。
- **只拿生活习惯开涮**：卫生、房间、作息、穿着、社交；不拿长相、身材、种族、疾病开玩笑。
- **声音**：默认用户自己的克隆声音；密钥只放 `.env`，不打印、不提交。发布时提醒标注 AI 合成。
- **自己看**：每次渲染完都用 Read 看抽帧，不要只看日志就交付；声音你听不到，交付时说清楚只用识别核过发音。
- 路径：`SK/` = 本 Skill 目录，`S/` = `SK/scripts/`；`SERIES` = 用户的系列文件夹；`EP` = `SERIES/epNN`。

## 1. 第一次：建系列

1. `python S/new_series.py SERIES --from-example`（直接拿 30 Days to the Date 改）或不带参数（空模板）。它会检查 ffmpeg、playwright + Chrome、numpy/scipy/pillow、faster-whisper、edge-tts。
2. 和用户定设定（`docs/01-format.md`）：主角是谁、N 天后的大事、面板名（DATE-READY / REUNION-READY…）、视频语言、配音用不用他的克隆声音。写进 `series.json`。
3. 换主角就改引擎 `leo()` 和配色 `C`，`render.py EP stills` 看几帧，用户点头再往下。
4. 列一张能投的清单 `fixes.json`（10–20 项），每一项都要在引擎里有改前、改后两个样子（`docs/02-character-state.md`）。

## 2. 每一集

1. **定这一集**：第 1 集照 `examples/30-days-to-the-date/ep01` 的结构（介绍主角 → 大事 → 3–4 个笑点 → 规则 → 投票）；改造集照 `ep02`（剪头发：理发师、飞出一只鸟、FIX_AT 换发型、进度条涨、妈妈短信推剧情、新投票）；之后每集：`python S/new_episode.py SERIES N --winner XXX`，它会算好 `state.json`（含 `before`）、复制上一集的引擎、写台词骨架。
2. **写台词**（`script.json`）：结果 → 改的过程一个笑点 → 新问题 → 二选一 → Comment one word → N days left。一句一行，短句，口语；每句 `gap` 是后面的停顿。给用户看，改到他点头。
3. **配音**：`python S/voice.py EP`（第一次先 `--test` 一句让他听）。输出 `vo.wav`、`timeline.json`（每个词的时间）、`mouth.json`。看一眼识别出的词和台词对不对得上。
4. **画面**（`docs/03-engine.md`）：在 `EP/index.html` 的 `draw(t)` 里按台词编排场景，关键词上弹出道具；改造那一刻设 `FIX_AT = W_('L03', '词')`。
5. **看帧**：`python S/render.py EP stills 1,4,8,...`（每句中间一帧），Read `EP/stills/sheet.png`：字幕挡脸、卡片压脸、出画、面板被盖、改前改后对不对。修到满意。
6. **音效配乐**：改 `EP/audio.py` 的音效时间点（`W(line, word)`），`python S/render.py EP audio`。
7. **出片**：`python S/render.py EP all`（约 3–5 分钟）→ `EP/<标题>_DayN.mp4` + 封面。再抽 6–10 帧看一遍，SendUserFile 发给用户。
8. **发布和读票**（`docs/05-publish.md`）：文案模板、读票、写 `log.md`，第二天回到第 1 步。

## 3. 改一点

- 改台词：改 `script.json` → `voice.py`（只重合成改过的句子）→ 画面里用到那句时间的地方会自动跟着走 → `render.py EP all`
- 改画面：改 `draw(t)` → `stills` 看 → `render.py EP frames --from 帧号`（只重渲后半段）→ `encode`
- 改投票选项：改最后两句台词和 `vote()` 里的两张卡

## 4. 坑

- 字幕一组超过 15 个字母会被拆得很怪：`buildChunks` 里调长度；重点词在 `HL` 正则里加
- 卡片和主角抢位置：卡片出现时把主角缩到 0.62–0.8、往下挪
- 结尾大字盖住脸：大字放 400–600 高度，主角放低
- 一个人一直站着不动会显得死：说话时身体轻摆（已内置），每 2–3 秒画面要有新东西
- 克隆音色读数字：写成单词（thirty、forty-seven）更自然；识别成阿拉伯数字没关系
