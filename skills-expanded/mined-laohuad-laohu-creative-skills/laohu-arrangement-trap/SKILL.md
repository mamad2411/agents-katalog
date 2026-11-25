---
name: laohu-arrangement-trap
description: 当用户要求 trap 编曲或以半拍人声和808为目标时，围绕snare、hi-hat句法与低音动作设计段落能量。
---

本子级由 [laohu-arrangement 主 Skill](../../SKILL.md) 在用户明确要求 trap 风格或按 trap 方法改编时加载。歌词、参考歌或制作人只提到 trap、808、快速 hi-hat 或 Atlanta 不自动触发。沿用用户锁定的人声、调性中心、速度、旋律和目标强度；本配置只返回相应节奏、低音与声部密度选择。

# Trap：让808、鼓组和人声各有清楚的位置
## 独立完整新作的项目蓝图
未锁拍号/速度/结构的 Trap 新作采用 4/4、140 BPM（四分音符 BPM）作项目值；snare/clap 放第 3 拍，所以实际身体重心是 70 BPM 半拍感，而不是把项目 tempo 改为 70。56 小节形式：Intro 4 → V1 16 → Hook 8 → V2 16 → Hook 8 → Outro 4；总计 56 小节。基础 hi-hat 先铺八分；roll 只有在主唱句尾/转段前存在至少一拍真实空隙，且下一强拍需要引回时才加，默认每 8 小节至多一次、长度不超过 1 拍，落在该空隙末端并准确回到下一强拍；没有这类空隙则不做 roll。Southside 的制作访谈支持先建立 snare/hat 关系再组织细分，不给 roll 配额；140 BPM、半拍听法和 56 小节是本项目值。既有 beat/tempo/map/旋律优先。

## 默认节奏骨架

无其他锁定参照时，先按 4/4 半拍骨架搭建：snare/clap 在第 3 拍给出强回落，kick 与 808 共同标出少数低频重心；hi-hat 先用稳定八分细分，再只在人声起句、句尾或转段前加十六分/三连音 roll。这里的半拍是重音解释，BPM 和实际计拍轴保持不变。若用户给的 groove 是直拍四踩、双倍推动或不同拍号，保留该输入并只将后续 trap 语法落到其拍轴上。

先定 snare/clap 的第 3 拍重心，再让基础 hi-hat 细分稳定身体拍感；只在主唱换句、重音推迟、填空或转段前插入短 roll，并让 roll 明确落回主拍。若它盖住辅音或使 snare 失去重量，先减短、降低力度或删去。Southside 在 Complex 访谈中谈到 snare 与 hi-hat 的相互关系；本地路线据此先让二者组成可辨骨架，再把 roll 放在句法节点，而非把连续滚奏当风格配额。

## 808与低频协作

808 默认以和弦根音/低音线标定音高：在需要重击的主 kick 点给短而有起音的 808，需要低频延续时将同音/根音拉长至下一和声或鼓点前；不是每个 kick 都必须双击 808。旋律性连接或转段需要滑音时，写清起音、目标音高和到达点；确认目标音源的 portamento/slide 支持，再让滑音连到下一和弦根音或指定经过音。无音源/和弦依据时不编造滑音音高。kick 与 808 错开时，让两个起音清楚可辨；持续重叠则先改节奏、音符长度、音区或起音包络。

每个 808 音符都检查音高是否贴合和声或刻意构成张力、尾音是否跨过下一音、是否与 kick 形成不可辨的双起音。滑音要以目标音程和到达时点写明，不能笼统标“滑”而让演奏/音源猜。超低频优先保持明确的单声道中心；只有目标音源与播放系统能稳定呈现时才把低频宽度作为效果。

## 旋律与段落分支

用户提供 melody/loop 时先保留识别钩子，再检查是否需要为人声留出频段和空拍。原创伴奏先选一个主要旋律或音色核，再决定空旷、明亮、阴郁或强攻击等具体方向；“trap”本身不规定小调、铜管、钟声、合成器或黑暗情绪。

人声主导时，先让第 3 拍 snare 与 808 低频形成框架，把 hi-hat roll 放在不盖词的句间/句尾；旋律主导或器乐时可把主题留给音色回应，但保留骨架回归。段落能量优先在 hi-hat 细分、808 进入/退出、旋律音区、起音密度、低频重量中选一个主要变化；无需每个副歌都加满或定时加 roll。

## 组合边界

与其他明确选择的专项组合时，本配置负责 trap 节奏/808 关系，其他配置负责其对象的和声、主题或叙事职务。若两个分支对同一段人声的主重拍、同一 808 音程或同一低频进入点互相排斥，交宿主依据参考、锁定旋律与段落目标选择，不按配置顺序覆盖。目标明确为器乐 trap 时不生成歌词或演唱安排。

## 返回与验收

返回实际拍轴与重音假设、snare/clap 位置、hi-hat 细分与 roll 的触发点、808 音高/时长/滑音意图、kick 关系、人声留白和段落主要变化。宿主继续完成全曲蓝图、其他声部及输出格式。

检查低音音高与和声中心、kick 与 808 的起音/尾长、snare 是否仍带动拍感、hi-hat 是否服务而非遮挡主句，并在真实音源上试听滑音和动态。缺少旋律/和弦时标明需要创作的变量；缺少实际音源时不承诺控制器或奏法表现。

## 方法依据与适用边界

Southside 在 Complex 的制作访谈谈到他的 trap 鼓组设计；具体作品单元另取 Lil Uzi Vert《Myron》：Supah Mario 与 Oogie Mane 在[Genius 官方 Deconstructed 拆解](https://www.youtube.com/watch?v=AJFSNRg0jMw)说明该曲从旋律核进入后，先加 hi-hat、snare/open hat，再加 triangle，808 顺着帽子与其余节奏关系组织。迁移到本次新作时，先定半拍 snare，再固定八分帽骨架与 808 根音/时值，最后只在真实句缝或段界触发本地规定的一次短 roll；具体曲目演示的层序不等于所有 Trap 都必用 triangle、808 或滚奏。音高、滑音、饱和仍依据用户参考、旋律及实际音源试听决定。

## 生成提示、演唱与可编辑事件控制

Style Prompt由已选关系直接组句，变量只改标注槽位： 交付 Style Prompt 前，将尖括号槽位替换成已确认、可直接阅读的短语并合成为完整句；未定项留在声音蓝图/Platform Assumptions，不把槽位名投喂。
最终 Style Prompt 以宿主蓝图确定的 BPM、拍号、曲式、段落长度和回返为准；本子级默认只作起点。

Global Metadata：trap hip-hop, <final blueprint BPM>, <final blueprint meter> half-time pocket, snare on beat 3, <sparse / driving> low-end pulse。
Vocal Details：<已确认的主唱身份/音区>，<rap / melodic rap> phrases <在拍上 / 弱起 / 跨小节>，重音音节<定位>，leave space at <句缝>。
Arrangement：808 follows <根音/旋律低音> with <held notes / target-note slides>，hi-hats hold an 8th-note grid and add short <16th / triplet> rolls before <主句入口/转段>；roll resolves to the pulse；按<最终蓝图段落顺序、长度与回返位置>安排
器乐版把Vocal Details改为旋律前景；固定半拍snare与稳定帽子骨架，开放帽子细分、808音长和滑音。主唱句头前加roll只在句头需要推进时；鼓点已密或辅音需清晰时减为八分帽/删roll。目标音源不支持可听滑音时改为离散经过音或无滑音，不用标签冒充奏法。

锁定源旋律时以已核实的拍位、音节重音与尾音为准，按源音符填写精确音高/QN；用户授权新谱曲时填写本轮实际创作的音高/QN；交 AI 探索时锁住关键节奏/重音/落点关系而保留具体音符开放。歌手范围未知时不虚构高音极限。标注弱起、拖过小节线的音节和呼吸。器乐作品不写人声控制。MIDI每个808音符填实际pitch_sounding_midi、onset_qn、offset_qn，kick与808只在要加强的重音同位，其余用错位或短尾分离；roll写成逐个note起止与力度，三连音注明拍轴，不用模糊“快速”。滑音另列按note起点关联的pitch-bend/音源portamento控制点及目标音、到达QN、bend范围；该范围跟目标插件设定，未核对时保留待定，别共用通道滑动同时发声的其他音符。

通用谱编译时，ABC以M:4/4、L:1/16起草帽子/roll，三连音用(3并按小节核平；帽子和鼓件写在V:打击乐声部，音高—鼓件映射依接收解析器/目标方言，解析器不支持时交独立事件表，不把普通音名字母说成通用鼓件。808连续滑音写成目标音/连线并附实现说明，ABC装饰记号不保证播放成滑音。MusicXML打击乐用unpitched/display-step/display-octave记谱位，instrument id指向score-instrument，midi-instrument/midi-unpitched给接收音源鼓件号（MusicXML 1–128，转换raw MIDI 0–127）；808的slide/glissando成对标在起止音notations，note duration按divisions填写，目标软件实播决定是否产生真实滑音。歌词用w:绑定导唱音符。 YuE2 外部 ABC 的事件选择与投影由主 Skill 统一处理，见[YuE2 外部谱编译](../../references/yue2.md)。
