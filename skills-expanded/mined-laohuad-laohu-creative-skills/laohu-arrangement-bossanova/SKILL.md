---
name: laohu-arrangement-bossanova
description: 用户要 Bossa Nova/巴萨诺瓦律动时，以直八分的二拍组织、落拍单音低音和拍间切分和弦支撑漂浮旋律。
---

# Bossa Nova：二拍组织、四拍计数、切分和弦与漂浮旋律
## 独立完整新作的项目蓝图
未给拍号/速度/结构而需完整 Bossa 新作时，采用 4/4、96 BPM（四分音符 BPM；每小节数 `1&2&3&4&`，第 1/3 拍作两个宏拍）作项目起点，不把它说成 Bossa 传统速度。结构为 Intro 4 → A1 8 → B1 8 → A2 8 → B2 8 → 器乐回应 4 → B3 8 → Outro 4，共 52 小节；每一段沿用直八分、bass 宏拍支点和拍间和弦，B 段只增加一项旋律/和弦/轻打击。选 2/4 时须按原拍号重写小节数，不能用相同“96”混淆计拍；用户指定的录音/旋律参照和拍号优先于这些起点，旋律事件是否锁定依主文的来源状态判断，不因附件存在就固定。

## 触发与本地默认

- 用户明确要求 Bossa Nova，或指定某首 Bossa 录音作为编曲目标时使用。泛称 Latin、巴西、爵士和弦、轻柔歌曲不能单独触发。
- 无更细路线要求时采用 samba-derived 二拍组织：保持宿主拍号；若写 4/4，照数四个四分拍 `1&2&3&4&`，以第 1、3 拍组成两个二分宏拍；若写 2/4，照数两个四分拍 `1&2&`，两个 2/4 小节等于一个 4/4 小节的四拍计数。八分细分保持 straight，不自动加三连 swing；bass 在 4/4 的第 1、3 拍（或 2/4 的每小节第 1 拍）给根音/五度单音支点，吉他/键盘上声部在 `&` 拍切分和弦，主旋律可弱拍起句、跨拍延留。
- 这条低密度编配路线不等于全体 Bossa Nova 的固定乐器表；选吉他、键盘或其他音源时，仍须保留“低音支点与切分和弦分层”的核心关系。

## 建立可演奏的节奏骨架

1. **先定数拍与宏拍。** 按宿主已定拍号计数；4/4 时清楚写 `1&2&3&4&`，把 1–2 与 3–4 各作一个二分宏拍，2/4 时写 `1&2&`。每个 `&` 仍是直分八分，不是 swing 的三连音弱拍。若用鼓组，以轻声闭合 hi-hat、shaker 或刷奏标细分，kick 只承担低频支点，不复制完整 bass。
2. **写单音 bass 支点。** 4/4 默认第 1 拍弹当小节和弦根音、第 3 拍弹五度；若第 3 拍前和弦已改变，改弹新和弦根音。2/4 默认每小节第 1 拍弹当前根音，第 2 拍只在和弦仍成立且旋律无冲突时弹五度，否则留空。只有连续两小节以上根音相同、且主旋律有至少一拍休止或延音空隙时，才在空隙里加一个连接音；默认取当前和弦内三音，禁止无目标地“增加流动”。下一小节换和弦且旋律在前一小节 `4&` 留空时，可将下一和弦根音提前到 `4&`；若旋律有起音、低音与其他声部冲突或和弦未确认，就不提前。保持单音支点，不写连续 walking bass。
3. **把切分放在和弦上声部。** 吉他或键盘以短和弦音在拍间起音，保持低音与和弦起音分层；吉他可按拇指低音、手指拨弦和弦的协调思路写，键盘则把左手低音与右手短 voicing 分开。切分音不要全部重击，可用时值、力度差形成呼吸。
4. **让旋律浮在节奏上。** 主唱/主旋律可在弱拍进入、延过小节线或在伴奏切分之间留空；关键词和句头优先清楚。伴奏不要每次旋律停顿都填满，句尾只安排一条短回应。
5. **按可观察的旋律/和声冲突安排色彩。** 先遵守宿主已确认的和弦与调式。若主旋律在某和弦上持续至少一拍，先检查该音是否为和弦音：是则保留和弦；若是与和弦相容的 9 音或 11 音，且用户未锁定纯三和弦，可在该处只加入一个对应延伸音，优先 9 音；若与和弦音形成不希望的半音冲突，先尝试改变和弦转位/内声部避让。和弦锁定时不改根音或功能；只有用户授权重写和声且已有旋律长音确实无法由转位/避让解决时，才换和弦，并把新和弦、bass 目标音和旋律关系逐小节写出。没有上述输入信号时，不为“爵士感”添加延伸音或半音连接。
6. **用稀疏增量发展段落。** 主歌保留 bass 支点、切分和弦与轻脉冲；副歌只增加一项，例如高音区和弦、轻打击层、主唱和声或短弦乐。间奏可让吉他/键盘承担主题回应；不要把所有段落都加满打击乐。

## 音区、奏法与邻近边界

- Bass 与和弦乐器默认分开至少一个八度，bass 用根音/五度单音；键盘/吉他中声区以三音 voicing 起步。和弦短音默认 gate 0.5 QN（八分音符）。若和弦音覆盖主唱辅音或与 bass 在同一拍重叠，先删掉冲突起音；只有删后和弦职责断裂时才把 gate 缩至 0.25 QN，并复核声音仍可辨。
- 吉他用真实可演奏的拨弦分工：低音由拇指落拍，上声部在拍间切分；不要写超出手指跨度、同时要求低音长延音又高声部密集切音的单手型。键盘可承担同样声部职责；控制触键长度与力度，使其轻于主旋律。
- 轻打击补二拍内的细分而非主导重拍；避免重摇滚 snare 2/4 或强四踩舞曲 kick 把本路线转成其他编配感觉。
- 区别 Samba：本配置选择小编制、低动态、和弦上声部切分及留白；不复制高密度鼓队/狂欢式声部。Bossa 与 samba 共源，但不能把每种巴西节奏混称 Bossa。

## 锁定项与组合

- 用户锁定速度、拍号、旋律、和弦或指定乐器时照留；若原材料要求强三连 swing 或强四踩，则保留该锁定并标记它改变了本地 Bossa 默认脉冲，不能悄悄改拍感。
- 可与歌词/影视/器乐主题配置叠加；Bossa 决定二拍底层、单音 bass 支点、切分和弦与旋律浮动关系，其他配置只补其负责的维度。
- 同一和弦声部若被要求既持续整小节又每拍间短切音，暂停该处冲突，其他 bass、旋律和段落继续编排。

## 提示词、音符事件与编译

AI 生成时读取宿主[生成控制 Reference](../../references/ai-generation.md)，用直八分与拍间和弦表达二拍组织，不能把“摇摆”当默认词。人声方向起点是亲近、轻声但清楚的旋律主唱；歌词句可在弱拍进入并跨线延留，主歌留出和弦切分间隙，副歌用旋律延展而不是自动加重鼓组。若用户给了更强烈的唱法或实际录音参照，按其节奏重心调整。

人声 Style Prompt 起句：

生成前先把以下字段全部替换为本次明确值：拍号/速度、主唱音区或器乐主奏、真实歌词的弱拍入口/跨线词、逐小节和弦、bass 目标音、和弦起音拍位、所选打击层、仅一项副歌增量。方括号中的说明也必须替换为定值；不得把尖括号或方括号占位符原样交付。

最终 Style Prompt 以宿主蓝图确定的 BPM、拍号、曲式、段落长度和回返为准；本子级默认只作起点。
```text

Global Metadata: bossa nova, <final blueprint meter> at <final blueprint BPM> counted in quarter notes, straight eighth-note subdivision, two-beat organization, light pulse and open space, close and clear production.
Vocal Details: [填本次歌手/音区]; [填真实歌词句子的弱拍起音位置或说明无弱起]; [填实际跨小节延音词或说明无跨线]; keep consonants clear.
Arrangement: [填逐小节和弦]; bass plays [填根音/五度及小节拍位]; guitar or keyboard plays short chord attacks at [填确切拍位，默认 1&、3&]; percussion is [填具体轻打击层或 none]; refrain adds only [填一项声部增量或 none]. Follow <final blueprint section order, lengths and returns>.
```

依据句法与歌手已确认的声线，从下列句式选一条放进 `Vocal Details`：
- 主歌亲近叙述："Use a close, conversational short phrase and leave the space between guitar chord attacks audible."
- 弱拍漂浮："Enter the phrase on the weak eighth-note and sustain its last word across the barline."
- 副歌延展："Repeat the short melodic refrain and lengthen its final vowel without increasing the drum weight."
- 句尾轻收："Release the last phrase softly after its key word only where the singer can keep the consonant clear."
每首取一条主唱基线，句级增量标明实际歌词位置；不因 Bossa 自动假设气声或低音区。

器乐方向用 `Motif / Front Identity` 指定旋律/吉他主题及其弱拍起句和跨小节延音；在 `Instrumental Form` 中写清上声部切分的进退与器乐主题回应位置。不要加入人声气口指令。

MIDI 起音依宿主原拍號。4/4 bass 默认在 `bar_qn+0` 弹根音、`+2` 弹五度（若该拍前和弦改变则弹新根音）；2/4 bass 默认每小節 `bar_qn+0` 弹根音。上聲部和弦固定起音起点：4/4 在 `bar_qn+.5`（1&）与 `+2.5`（3&）；2/4 在 `bar_qn+.5`（1&）。只有人声句末明确落在第 2/4 拍、且其后一个八分格没有新歌词起音、低音/打击起音或和弦变化时，才在 4/4 的 `+1.5`（2&）或 `+3.5`（4&）增加一次和弦；没有该条件就维持每小节两次（2/4 一次）。换和弦前 `4&` 根音提前仅在下一根音已确认且主唱该格留白时使用。力度起点 bass 72、和弦 54、shaker 42、主旋律 76。和弦 MIDI gate 默认 0.5 QN；只有与主唱辅音/低音同拍冲突且删去起音会破坏声部职责时才降至 0.25 QN，并复核可辨性。无自动 swing，微时值只按参照/明确表演意图加入。

通用谱编译时，ABC/MusicXML 按原拍号记录直八分、低音落拍、上声部反拍和弦、旋律跨小节连线与实际休止；弱拍起音不能只用演奏说明文字代替。低音与和弦分成可演奏声部，吉他拨弦型注意同一只手可达到的音域和同时发音限制。若要记谱打击声部，使用目标软件支持的 percussion map；详细符号语法和时值检查见[输出契约 Reference](../../references/output-contracts.md)。 YuE2 外部 ABC 的事件选择与投影由主 Skill 统一处理，见[YuE2 外部谱编译](../../references/yue2.md)。

## 返回宿主与验收

把宿主拍号、宏拍计数、straight 八分细分、bass 支点、切分和弦起音、主旋律进句与留白、各段增量写入宿主第三步蓝图和第五步分段声部表。第七步按目标编译乐谱、MIDI 或生成输入；第八步验收四拍计数/二拍组织是否一致、八分是否被误做成 swing、bass 是否稳住宏拍、和弦切分是否清楚以及主句是否自然浮动。

## 方法依据与范围

- Guilherme Castro, [*Brazilian Rhythm Section Training*（Advance Music, 2008）公开样页](https://content.alfred.com/catpages/01-ADV13021.pdf)中的可定位作品单元：Example 4 以 Jobim/Mendonça《Desafinado》、João Gilberto 与 Stan Getz 录音为参照，标明带提前到下拍“1”的标准切分型；Example 7 以《Doralice》录音说明 2–3 bossa-signature 的 samba-bossa pattern；Example 8 以《Isaura》（João Gilberto 录音）和《Na Baixa do Sapateiro》（Caetano Veloso 录音）示范带 adjustment-bar 的 3–2 方向。迁移到本次编曲时，先由用户/既有录音选定 2–3 或 3–2 朝向，再在相应两小节周期内标出切分与是否需要调整小节；《Desafinado》的提前“1”只作有真实换和弦、下一根音已知且旋律留白时的可选提前，不作为每小节固定必打。
- 同书 §8.4 对《Corcovado》（João Gilberto/Astrud Gilberto/Jobim/Stan Getz 录音）的钢琴职责说明：若与吉他同奏，钢琴不持续重复完整型，而补吉他没弹的和弦/小填句，把基础律动留给吉他；无吉他时才可由钢琴承担 bossa-signature。迁移时先列每小节吉他/钢琴起音，再把另一件乐器限制在缺位拍或短回应，不能双重复制整型。
- Nelson Faria, *The Brazilian Guitar Book: Samba, Bossa Nova and Other Brazilian Styles* 的出版社页确认作者和覆盖范围，但公开样页主要展示 Samba；它仅作背景教材，不再充当 Bossa 实际作品单元的证据。
- 以上均是特定教材中引用的特定录音/伴奏型，不代表该曲全部声部、速度或全体 Bossa Nova 规律。独立新作的 96 BPM、4/4、52 小节及本文件明确的低密度声部起点是项目默认，改编/复现则以用户锁定或可核来源为准。
