---
name: laohu-arrangement-salsa
description: 用户要 Salsa/萨尔萨合奏时，以两小节 Son clave 朝向组织 montuno、tumbao、打击声部与人声问答。
---

# Salsa：用 2–3 Son clave 组织 montuno、tumbao 与声部呼应
## 独立完整新作的项目蓝图
无指定录音/速度/曲式的完整 Son-based Salsa 新作使用 4/4、96 BPM，BPM 明确按四分音符宏拍计；照数 `1 2 3 4`，八分切分另数 `&`。这不是 48 BPM 半速读法；若演奏者以双倍 subdivided 口数，仍保留 96 的 tempo-map，并标记 double-time 细分，不把 BPM 改写成 192 后又沿用相同小节/clave 长度。两小节 2–3 Son clave 为一个方向周期。项目曲式 80 小节：Intro 8 → Verse 16 → Coro/Pregón 16 → Montuno/器乐 16 → Final Coro/Pregón 16 → Outro 8；各组 clave 同向，只有用户指定 3–2 朝向或来源曲确实翻转时才换向。每段起止小节以四分拍网格计算。Berklee/Mauleón/Poole 支持 clave、montuno/tumbao 角色与跨线 anticipations；96 BPM 和这套整曲长度是本项目选择，不是这些来源规定。

## 触发与默认路线

- 用户明确指定 Salsa/萨尔萨，或要求将作品编成 Salsa 时使用；“Latin”大类、巴西 Bossa、探戈或一件拉丁打击乐器不能单独触发。
- 无更细分支或参考锁定时，采用 son-based Salsa 路线：4/4 两小节为一个 clave 周期，默认 2–3 Son clave；第 1 小节 clave 两击落在 2、3 拍，第 2 小节三击落在 1、2&、4 拍。钢琴 montuno 以重复切分和弦型顺着这个方向，bass tumbao 在和弦支点与弱拍提前之间推进，打击组各自补充而不齐奏复制 clave。
- 若用户指定 3–2、rumba clave、timba 或录音的句法明显以另一方向组织，保留其完整两小节朝向，再重排 montuno、低音和打击；不按加载顺序或每小节随意翻转方向。

## 从两小节 clave 写出全组互动

1. **先标 clave 朝向。** 在 4/4 两小节框中明确写 `2–3 Son`：第一小节 `2、3`；第二小节 `1、2&、4`。将这组节奏当作组织网格，不必让每个乐器都演奏 clave 音符。
2. **写两小节 montuno。** 先确定和弦换位落在哪小节/拍，再写贯穿 2–3 clave 整个两小节周期的 piano montuno/guajeo：短促切分和弦分布在 clave 的空隙和反应位置，pattern 入口、重音和收束保持同一朝向。钢琴 voicing 控制在中高音区，避开 bass 和主唱；和弦改变时先保留可连续的共同音，再改变一个音或起音位置。
3. **用预期音建立 tumbao。** 本地默认 son bass cell 将下一小节/和弦的根音提前到前一小节第 4 拍，并持续越过小节线，至少占住下一小节第 1 拍；例如 `onset_qn=cycle_start_qn+3`、`offset_qn=cycle_start_qn+5`，然后在下一小节 2&（`+5.5`）奏五度或和弦音。这样第 1 拍由预备根音延续而非另起根音，2& 留给独立回应。按实际和弦换位移动 anticipation，但保留“第 4 拍预备根音—跨线延续—2& 回应”的关系。只有用户指定录音在强拍另起根音时，才用强拍型低音路线。
4. **让 tumbao 与 clave 咬合但不重奏 clave。** 两小节 clave 是时间组织轴，bass 用提前根音/2&回应形成自己的低音型；若 bass 逐个复制 clave 击点，低音就不再形成独立的和声推动，节奏组也失去相互错开的张力。试听 2–3 周期中低音anticipation是否指向正确和弦，并确认长音跨线没有把周期听成另一个方向。
5. **分配打击乐职责。** 依可用编制选择 conga、bongo、timbales、bell、maracas 或电子替代；每件只承担一种主要层次（开放/闷击回应、稳定细分、乐段标记或句尾 fill）。乐段转入 montuno/mambo 时再增加 bell 或更密的打击，不从前奏起就全开。
6. **安排问答与段落能量。** 有人声时，主句与 coro/pregón 的应答放在对应乐句间；montuno 段让两小节钢琴型和合唱构成循环，solo/间奏由一件乐器暂时接管前景。器乐作品则用钢琴型、bass 句和铜管/主奏回应承担相同的 call-and-response 职责。
7. **检查循环朝向。** 连续演奏两小节及其整数倍，确认下一轮的两击侧重新接回正确方向；过门、break、和弦提前不能把周期听感误导成 clave 翻转。

## 和声、编制与可演奏性

- Salsa 使用 son 传统中反复循环的和声完全可行；不强迫古典式 V–I 终止。实际和弦按宿主确认的旋律、低音和歌段选择，montuno 负责把和弦节奏化，而不是另造一套和弦。
- 先写钢琴与 bass 的互锁，再安排铜管短句、合唱或弦乐。铜管齐奏用于指定段落的重音/回答；让主唱句头和 clave 朝向清楚可辨，铜管不要持续覆盖整段。
- MIDI 中写出每个打击声部的音色/奏法映射、起音和力度差异；单一鼓轨同时塞入 clave、bell、conga 和 timbales 时，拆成可读角色轨，而不是以轨数伪装演奏关系。
- 本默认使用 2–3 Son clave，不等同所有 Salsa 的唯一结构；二拍 Salsa、Rumba clave 或其他 Cuban-rooted 分支由用户指定/材料证据触发切换。

## 锁定与组合

- 用户锁定的旋律、和弦、速度、clave 或乐段结构优先；只在缺失项上采用 2–3 默认。若现有音乐与 2–3 不兼容，优先测试完整换向为 3–2，而非移动单个击点让表面像“对上”。
- 可与歌曲主题、人声状态、影视用途或 AI 生成条件叠加；本配置决定 clave 周期及组内关系，宿主保留总曲式、旋律创作与最终输出责任。
- 仅当同一段被同时锁定为互斥 clave 朝向时暂停该段排序；其他不受影响的乐段和声部继续编配。

## 提示词、音符事件与编译

AI 生成时读取宿主[生成控制 Reference](../../references/ai-generation.md)。若有词，默认先由主唱给完整 pregón/陈述句，再在句后让 coro 回答；进入 montuno 段时持续重复简洁 coro 与钢琴型。用户指定语言、句长或无合唱时保留原状，不能用西语或群唱标签替换已锁歌词。

人声 Style Prompt 起句：

最终 Style Prompt 以宿主蓝图确定的 BPM、拍号、曲式、段落长度和回返为准；本子级默认只作起点。
```text

Global Metadata: son-based salsa, <final blueprint BPM> in <final blueprint meter>, two-bar 2–3 Son clave cycle, interlocking piano montuno, bass tumbao and layered percussion, <band energy and room>.
Vocal Details: <language, singer/register>; verse lead gives a complete rhythmic call, then coro answers after each completed lead call; in montuno, repeat <user-approved response text> with clear entrances and a distinct response register.
Arrangement: clave cycle is <2–3 default / explicitly requested direction>; piano montuno keeps that two-bar orientation; bass anticipates the next harmony on the previous bar beat 4 and answers on next-bar 2&; add <one percussion layer> at <actual section entry>, reserve brass hits for phrase ends. Follow <final blueprint section order, lengths and returns>.
```

按实际歌词/语言从四条中选一句放入 `Vocal Details`，并对应到完整乐句：
- Pregón："Let the verse lead deliver a complete two-bar call, with the key word clear of the piano montuno accent."
- Clave pickup："Place a short lead pickup on beat 4 only when it keeps the next two-bar clave direction audible."
- Coro："After the completed lead call, let the approved short coro answer through the montuno cycle."
- 终句长音："Sustain the final cadence only at the section close, then leave the next clave-cycle downbeat clear."
没有歌词时不要生成拟西语音节；器乐方向用乐器/铜管 call-and-response 替代 vocal 指令。

器乐方向将 piano guajeo/montuno 或主奏动机写入 `Motif / Front Identity`；在 `Instrumental Form` 中标明 clave 周期、打击乐层进入、铜管回答和循环/终止方式。没有旋律和和弦时，不能要求 AI 捏造精确 montuno 音符。

MIDI 以每小节 4 QN 计，两小节 `cycle_start_qn` 的 2–3 Son clave 默认在第一小节 `+1,+2`，第二小节 `+4,+5.5,+7`；第二小节起点是 `cycle_start_qn+4`。bass tumbao 在前一小节 `+3` 起根音，`offset_qn=cycle_start_qn+5`（即越过 barline 并完整占住下一小节第 1 拍），再留空到下一小节 `+5.5` 的五度/和弦音回应。钢琴 montuno 用实际和弦音，落在 clave 间隙并保持两小节方向；具体起音随和弦/参考确定。力度工作起点 clave 70、conga 65、bell 72、bass 88、piano 74、主唱 85；力度分层由各自音源校准，不能用同一重音复制 clave。打击轨按目标音源 map，不把 percussion note 编成假旋律。

通用谱编译时，ABC/MusicXML 在两小节网格中写出 clave 的真实拍位、tumbao 根音跨线延续和 2& 回应：在小节线处分成首尾相接、音高相同的两段 tie，使后一段越过边线至少占住第 1 拍，然后于 2& 前留出空隙；不要把 offset 设为新小节起点。montuno 按实际和弦音/休止写出并标明段落中打击层进退。Clave 与 bell/conga 若由目标软件支持打击谱记法则使用其 percussion mapping；否则可用清楚的角色表配合实际 MIDI 轨。钢琴音符为可演奏 voicing，跨声部时值和小节总量逐小节核验。精确字段与文件检查见[输出契约 Reference](../../references/output-contracts.md)。 YuE2 外部 ABC 的事件选择与投影由主 Skill 统一处理，见[YuE2 外部谱编译](../../references/yue2.md)。

## 返回宿主与验收

把 clave 朝向和两小节拍点、和弦换位、montuno pattern、tumbao 支点/anticipation、打击乐角色、段落加减层和人声问答写入宿主第三步蓝图、第五步分段声部表。第七步按选定分支交付生成条件、谱面或 MIDI；第八步检查 clave 周期、tumbao/montuno 朝向、乐器起音分工、段落进退和主唱清晰度。

## 方法依据与范围

- 作品单元采用 Celia Cruz 与 Fania All-Stars 的《Quimbara》（1974 Zaire 74 现场版）。CSU East Bay 音乐系的[逐段听赏指南](https://csuebmusic.github.io/mus302/module1/track2-cruz.html)把开头 cuerpo（主题歌词）与其后 montuno 明确分开：转段由 percussion/horn break 打开，之后固定 coro 与 Cruz 的即兴 guía 交替，乐队维持 clave、percussion、bass tumbao、piano montuno 和 horn mambo 的不同职责；现场录音超过一半为 montuno。迁移时先写歌曲正文和 montuno 分工，再让固定 coro 留给合唱、lead call 留给歌者，打击/钢琴/铜管各承担独立层；段落时长由本作能量决定，不复制现场时长或具体速度。
- Rebeca Mauleón, *Salsa Guidebook for Piano & Ensemble*, Ch. III–V，提供 clave、乐器角色、montuno 与合奏结构的方法背景；出版社目录和样页可核该书的主题范围，但本规则不把未见的 bass 原谱归给她。
- Adrian Poole, “Timing and Groove in the Performance of Cuban Bass and Conga Patterns,” *Analytical Approaches to World Musics* 10/2 (2022), Figure 4 与正文 [22]–[24]，把 2& 与 4 标为常见 anticipated bass 的两个起音，并说明第 4 拍音跨小节线连到下一小节第 1 拍、预示和弦变化。Smithsonian Folkways 的 Salsa 教学指南也讲第 2 拍后半与第 4 拍的两次起音及第 4 拍预示和弦变化。这里的“第 4 拍根音—跨线—下一小节 2& 五度/和弦音”是本配置选定的可执行音高安排；Poole 的正文支持节奏位置与和声预期，不单独证明这一具体根音/五度映射。
- David Peñalosa, *The Clave Matrix: Afro-Cuban Rhythm: Its Principles and African Origins* 讨论 clave 在不同 son/rumba 等传统中的组织差异；本文因此精确限定为 2–3 Son clave，不把一种 clave 方向外推到所有 Afro-Cuban 音乐。
