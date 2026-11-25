---
name: laohu-arrangement-underscore
description: 当用户明确要求影视、游戏或视听场景的 underscore/cue 编曲时，根据叙事节点、时码、对白与音效安排音乐进入、留白和退出。
---

本子级仅在用户明确要求为画面/场景/剧情段落写 underscore、scene cue 或同步配乐时由 [laohu-arrangement 主 Skill](../../SKILL.md) 加载。仅提电影、剧集、游戏或某位配乐家不触发；若只要画面之外可独立聆听的主题歌曲，由宿主判断 screen-theme 或通用歌曲路径。用户没有画面时仍可先形成音乐叙事草案；只暂停依赖真实镜头和剪辑的同步层。

# Screen underscore：按叙事与声画时间安排音乐
## 独立 cue 的可执行计划默认
有画面时，以画面版本、FPS、实际时间码和用户标出的剧情/对白为准，必须输出 cue-in/out 与各关键点，不套以下时长。无画面且未给 cue 长度时，按叙述事件顺序交一份“未同步”60 秒文本计划：0–8 秒 establish；8–24 秒呈示主题/关系；24–40 秒在用户描述的关键行动/证据后改变一项和声、音区或织体；40–52 秒对白/决定前减层或静默；52–60 秒收束并留真实尾音窗口。按用户事件先后把节点放入对应窗口，不得自编情节或声画 hit point；事件少于五个时空窗保留，不增造节点。若交付需量化谱/MIDI 但任务仍是自由时间，继续用秒数/tempo map；仅在用户要均匀拍网格时选择 4/4、72 BPM、18 小节恰为 60 秒的可编辑网格，并标“工作网格，未同步”。制作互锁参考为 Britell/Gilroy 对《Andor》Maarva 葬礼段的共创：音乐在拍摄前开发并成为城镇仪式、反过来启发独白；迁移为音乐职务与场景社区行动共定，不伪造源 cue 的时码和时长。

## 输入与同步边界

先问本轮要的是音乐概念、可同步 cue，还是可交付音频。描述角色/关系、场景意图、情绪转折、必须突出/避开的叙事点；若要求对画面同步，再取得可读视频/时间线或明确时码的镜头表，以及关键对白、音效和目标时长。没有这些素材时可先给无时码的叙事音乐蓝图，不能声称 hit point、对白避让或剪辑同步已成立。

为真实画面建立 cue 表：标 cue in/out、入点前后叙事状态、关键视觉动作/对白/音效、允许的音乐峰值和退出方式。时间码要与素材版本、帧率、起点一致；锁画/剪辑版本变化后重核 cue。按导演/用户指出的情节点安排同步，而不是让每个动作都有打击乐击中。

## 音乐进入、留白和退出

每个 cue 先确定主要职务：提示角色或关系、维持悬念、提供连续感、塑造空间/时间，或把观众注意力推向一个变化。进入可以先于切镜建立预期，也可以在动作/对白后出现；退出可在新对白、音效或叙事重点前让位。确定留白是否比持续音乐更清晰，再配主题、脉冲、织体或不稳定和声。

| 画面/叙事情况 | 默认 cue 决定 | 何时切换 |
|---|---|---|
| 新场景/关系尚未揭示，观众需要预感 | 可在画面切入前短暂预入，用持续音/节奏身份建立连续性 | 若要让环境声或首句制造惊讶，则延后到事件之后进入 |
| 关键台词或角色做出选择 | 降低旋律起音与对白相近频段；保留低密度持续层，或在关键词前退出 | 若沉默会削弱该选择的重量，保留不抢前景的单一声部并在句后回响 |
| 发现、反转或情绪状态改变 | 在信息被观众接收后改变和声、音区或动机形态；把峰值放在叙事确认点 | 画面需要先展示发现过程时，延迟峰值，不跟每个动作同步 |
| 动作段或快速剪辑 | 锚定长句、整体拍轴或少数关键 hit point，让节奏带过剪辑 | 只有导演指定/情节确有重击时才对单个动作精确落点 |
| 场景离开或下一 cue 接入 | 选择收束、尾音延续、可编辑延音或提前让位，明确 out 点 | 若下一场要无缝衔接，保持调式/音色/脉冲连续并按版本试听 |

表中的每项都是默认建议，不取代导演/用户的叙事要求；cue 表要标明选了哪一项及理由，方便修订。

检查对白的语义重音与音效瞬态。主角关键台词处控制旋律前景、起音密度和相近频段；必要时让持续音跨过对白、在句尾回响或完全停音乐。避免只靠混响把拥挤声部“藏起来”。动作/剪辑较密时，音乐可锁定更大节奏组或低频脉冲，不需给每个剪辑点写独立重音。作曲草案至少写 cue-in、cue-out、主要叙事点、最需要留白的对白/音效和一个可听的高潮/转折；同步交付再换算成素材版本对应的精确时间码。

## 材料与方案分支

用户给已有主题时先保留动机身份，再改变配器、节奏、和声张力或音区以匹配场景状态；没有主题时可写情绪/音色草案，待叙事线索足够再决定是否需要角色动机。画面与剧情未定时给可调参数，如 cue 长度/终点、音色密度和高潮时刻，不填假时码。

固定时长广告/游戏提示可按循环或事件触发设计，但标明真实触发长度和尾音处理；开放时长场景可准备可延展段、可移除层或可接续终止。分支用于不同叙事意图，不同时输出无差别情绪版本。

## 提示词、cue 事件与谱面编译

需要 AI 草案时读取宿主[生成控制 Reference](../../references/ai-generation.md)。器乐 cue 的前台身份先由一项材料承担：连续动机、低频脉冲、和声/音色织体或明确静默；`Instrumental Form` 将每个 cue 的叙事职务、材料进入、变化和退出写成可读蓝图。有人声仅在本次确需有词/人声时写 `Vocal Details`：优先保持对白理解的短句、无词长音或对白间回答；歌词主题曲/角色歌另走主题歌曲职责，不能把对白下的 cue 偷换成长段主唱。

器乐提示词起句：

```text
Global Metadata: underscore for <specific scene and dramatic objective>, <BPM or free-time>, <pulse/meter if established>, <dynamic and spatial range>; leave <identified dialogue/effect range> perceptually clear.
Motif / Front Identity: <one confirmed theme, pulse, harmonic field, timbral texture, or intentional silence; state its register and role>.
Arrangement: enter at <story/cue point>, establish <initial state>, change <one musical dimension> after <confirmed narrative turn>, yield space at <dialogue/effect>, and leave by <cue-out/next scene handoff>; use <actual continuity or stop ending>.
Instrumental Form: <cue-in and cue-out; cue-by-cue dramatic function; motif state; pulse/texture progression; key dialogue/effects; tail or loop handoff>.
```

有人声时另给 `Vocal Details`（音区、字词/无词、句长、动态、具体入退位置），并将可唱句放在对白空位；若不需要人声，不生成多余歌词。段落标签和起止依据剧本/镜头表，不从画面主题推断没给出的精确时间码。

按 cue 职务从四条中选一条可复制到 `Vocal Details`，写明真实入退位置：
- 对白下空间："Use a soft wordless hum only beneath dialogue without key semantic information, and keep it out of the speech register."
- 揭示后的余波："Hold one wordless vowel after the reveal and release it before the next dialogue entrance."
- 有词 cue："Use one short lyric line only in the confirmed dialogue gap, then leave the next spoken line clear."
- 声音身份碎片："Place a low spoken fragment after the character turn and exit before intelligible dialogue resumes."
没有人声要求时用乐器 motif 或静默做前台，不用“人声纹理”占位。

将 cue 计划转成符号/事件底稿时，每个声部事件用绝对 `onset_qn` 与 `offset_qn`，以及可选的独立 `midi_gate_qn`、力度和 cue/section 标识。已给真实时码和素材 fps 时，按同一版本的时间轴与速度图换算；自由速度/时码无拍轴时，先保持绝对时间点或 tempo map，不制造等间隔小节。没有画面仅有叙事草案时，用 `cue_start_qn + <相对拍位>` 表达探索性位置并标“未同步”，不可声称 hit point 对齐。MIDI 力度起点按声部职责定：主题/显著 hit 高于持续床层，低层留动态余量；Note Off 后仍有释放的声源须核实际尾音长度与 cue-out，不能将 MIDI gate 当成音响静音时刻。

通用谱编译时，ABC/MusicXML 只能精确写出已确定拍轴和音乐事件：主题音符用实际音高/时值，持续音 tie，真正静默写休止，节奏打击按目标软件支持的 percussion mapping。cue-in/out、timecode、帧率、同步音效等作为伴随 cue 表元数据，不伪造为 ABC 音符或 MusicXML 的通用时间码字段。对话/画面锁定后复核谱面速度图及事件位置；独立草案只保留相对小节/拍位。声音自动化另用已核实的目标 DAW 控制格式，详见[生成控制 Reference](../../references/ai-generation.md)与[输出契约 Reference](../../references/output-contracts.md)。 YuE2 外部 ABC 的事件选择与投影由主 Skill 统一处理，见[YuE2 外部谱编译](../../references/yue2.md)。

## 返回宿主与验收

与 screen-theme 或 genre 专项组合时，本配置只负责场景 cue 的叙事/时码职责；主题专项决定可识别材料如何与剧情相关，其他音乐专项决定其声部语法。若同一时点要求“音乐击中动作”和“完全留白/对白优先”冲突，回宿主按锁定叙事目标裁决。

返回宿主：cue 表或无时码草案、每段叙事职务、入点/退出/留白策略、主题材料处理、对白/音效冲突、缺少的同步输入。宿主继续音乐创作、生成/谱面/音频输出及验收。检查素材版本、时码、帧率、cue长度、对话和音效空间；仅在画面与最终混音中验证同步和遮蔽。

## 方法依据与适用边界

Michael Rabiger《Directing the Documentary》“Using Music and Working with a Composer”章节建议明确 cue 职能与真实时码入出点；这是 cue 工作方法来源。具体音乐/场景单元取 Tony Gilroy 与 Nicholas Britell 对《Andor》终集 Maarva 葬礼 procession 的[创作访谈](https://www.starwars.com/news/tony-gilroy-andor-season-1-interview)：约七分钟的场景音乐在拍摄前两年协作完成，演员现场演奏真实乐器，音乐身份与 Ferrix 群体仪式及 Maarva 独白互相影响。迁移到新 cue 时先列用户给出的行动/对白顺序，再给每段声部标职责和出入；无画面只写相对时间计划，不移植七分钟时长、乐器或伪造 hit point。
