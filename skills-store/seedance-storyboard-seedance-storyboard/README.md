<div align="center">

# 🎬 seedance-storyboard

**把剧本文字一键转成 Seedance / 即梦 文生视频分镜脚本**
**A Claude Skill that turns screenplay text into Seedance (即梦 / Doubao) video-generation storyboards**

[English](#english) · [中文](#中文)

</div>

---

## 中文

### 这是什么

`seedance-storyboard` 是一个 [Claude Code Agent Skill](https://docs.claude.com/en/docs/claude-code/skills)。
你给一段剧情文字（剧本、小说桥段、动作描述、广告创意，甚至一句话），它会自动转写成
**Seedance / 即梦（豆包 Doubao Seedance）文生视频可直接喂入的分镜脚本**：

- 先定**全局影像风格**：`视觉基调（镜头器材）`+`色彩与调影`+`情绪基调`+`一致性约束`
- 再按秒拆成**逐镜时间轴**：`分镜1 …（0–1.5s）景别·运镜：主体+动作+细节`

输出风格对标专业影视化分镜文案——精确到秒、运镜明确、动作连贯、画面可拍。

### 输出长这样

````
【视觉基调】
变形宽银幕电影质感，仿 IMAX 胶片摄影机 + Panavision C 系列镜头；全程手持拍摄，
动态模糊，轻微手持抖动，保持临场感与紧迫感。

【色彩与调影】
60 年代复古科幻原子朋克美学；复古暖橙 + 海盐蓝高对比色调，胶片颗粒质感……

【情绪基调】
画面血腥暴力，战斗节奏紧凑激烈，凸显末日逃亡，强调速度感与力量感。

【一致性约束】
始终为同一机器人主角，金属机身与配色一致；面部 LED 屏表情清晰稳定不扭曲。

【画面内容】
分镜1 开场入画（0–1.5s） 广角低角度固定镜头：机器人重重摔向地面，向前侧滚翻卸力……
分镜2 备战起势（1.5–3s） 中景·环绕半圈无缝衔接：右手闪电般快拔左轮，拇指扳倒击锤……
分镜3 双枪击杀（3–5s） 过肩跟拍·随身体平移：贴脸扣扳机，两枪间隔不足 0.3 秒……
````

### 设计依据（为什么这么拆）

规则全部来自 Seedance 的实测提示词规律：

- **骨架** = `主体 + 动作 + 场景 + 光影 + 镜头语言 + 风格`，模型擅长在清晰输入上扩展
- **单条视频 5s 或 10s @ 24fps**，时间轴按此排布
- **多镜头要显式衔接**（无缝切至 / 镜头切换），切镜后**重新交代新场景**
- **不响应负向提示词** → 把「不要崩」改写成「人体结构正常、比例自然」等正向描述
- 写**一致性约束**（角色/服装/面部稳定）显著减少崩坏
- **长剧本自动按场景切分**，每个场景输出一条独立的 ≤10s 脚本

### 安装

把整个文件夹放进你的 Claude Code skills 目录：

```bash
# 个人级（全局可用）
git clone https://github.com/zcx960/seedance-storyboard.git \
  ~/.claude/skills/seedance-storyboard

# 或项目级
git clone https://github.com/zcx960/seedance-storyboard.git \
  .claude/skills/seedance-storyboard
```

重启 / 刷新 Claude Code 后即可。

### 用法

直接说人话即可触发，例如：

- 「把这段剧情转成 Seedance 分镜」
- 「帮我拆成分镜 / 写成 AI 视频提示词」
- 「这段小说桥段做成即梦视频脚本」

也可指定参数：默认时长（5s/10s）、单场景还是整段长剧本。
触发关键词包括：剧本、视频脚本、分镜、运镜、storyboard、Seedance、即梦、文生视频等。

### 仓库结构

```
seedance-storyboard/
├── SKILL.md                      # 技能主体：工作流 + 输出模板 + 写作要点 + 触发描述
└── references/
    └── seedance-vocab.md         # 景别/运镜/机位/器材/色彩/光线/衔接/一致性 词表 + 进阶范例
```

---

## English

### What it is

`seedance-storyboard` is a [Claude Code Agent Skill](https://docs.claude.com/en/docs/claude-code/skills).
Give it any piece of narrative text — a screenplay, a novel passage, an action description,
an ad concept, even a single sentence — and it rewrites it into a **storyboard prompt ready to
feed into Seedance / 即梦 (Doubao Seedance) text-to-video**:

- A **global look** header: `visual base (camera/lens)` + `color & grading` + `mood` + `consistency constraints`
- A **second-by-second shot timeline**: `Shot 1 …(0–1.5s) framing · camera move: subject + action + detail`

Output reads like a professional shot list — timed to the second, explicit camera language,
continuous action, shootable frames. (Output is in Chinese to match the Seedance/即梦 ecosystem.)

### Why this structure

Every rule is grounded in how Seedance actually responds to prompts:

- **Backbone** = `subject + action + scene + lighting + camera language + style`; the model
  excels at expanding clear input
- A single clip is **5s or 10s @ 24fps** — the timeline is laid out to fit
- **Multi-shot needs explicit transitions** (cut to / camera switch), and you must
  **re-describe the new scene** after a cut
- **Negative prompts don't work** → "don't distort" is rewritten as positive constraints like
  "natural human/mechanical proportions"
- **Consistency constraints** (same character, wardrobe, stable face) sharply reduce artifacts
- **Long scripts are auto-split by scene**, each scene producing its own ≤10s script

### Install

Drop the folder into your Claude Code skills directory:

```bash
# Personal (global)
git clone https://github.com/zcx960/seedance-storyboard.git \
  ~/.claude/skills/seedance-storyboard

# Or per-project
git clone https://github.com/zcx960/seedance-storyboard.git \
  .claude/skills/seedance-storyboard
```

Restart / refresh Claude Code and you're set.

### Usage

Just ask in plain language — it triggers on intent, e.g.:

- "Turn this scene into a Seedance storyboard"
- "Break this into shots / write it as an AI-video prompt"
- "Make this novel passage into a 即梦 video script"

You can also specify: target duration (5s/10s), single scene vs. full multi-scene script.
Trigger keywords include: screenplay, video script, storyboard, shot list, camera movement,
Seedance, 即梦, text-to-video, and more.

### Repo layout

```
seedance-storyboard/
├── SKILL.md                      # The skill: workflow + output template + writing rules + trigger description
└── references/
    └── seedance-vocab.md         # Framing / camera-move / angle / gear / color / light / transition / consistency vocab + advanced examples
```

---

## License

[MIT](LICENSE) © 2026 zcx960

> Built with the Claude Code `skill-creator` workflow. Seedance / 即梦 / Doubao are trademarks of
> their respective owners; this skill is an independent, unofficial prompt-authoring helper.
