---
name: rite-speak
description: "RiteSpeak/合乎周礼: rewrite Chinese requests as paired 白话译文+文言正文 admonitions with Confucian virtue, story, analogy, parallelism, reversal, solemn endings."
---

# RiteSpeak / 合乎周礼

## Core Effect

Produce RiteSpeak / 合乎周礼 Chinese prose in two coordinated registers:

- **白话译文**: "骨架文言、血肉白话". Mostly readable modern Chinese, but arranged with classical admonition logic: story first, analogy second, moral pressure third, reality last.
- **文言正文**: pure classical-style Chinese using 文言 vocabulary, compact syntax, old-style turns, and admonition format.

The default output is both registers. The two versions must carry the same
meaning, story, analogies, moral argument, and final landing point. The humor
comes from "小题大做": lifting housework, work fatigue, friendship, sleep,
studying, or daily conflict into the realm of 贤德、仁义、君子之道、圣人之训.

## Reference Loading

For any generation longer than one short paragraph, any messy user input, or any
request where the user cares about "像示例那样", read
`references/style-guide.md` before drafting. That reference contains the
long-form blueprint, required rhetorical devices, and example-level constraints.

## Workflow

1. Rebuild the user's real intention before writing.
   - Identify the factual situation, speaker, listener, emotional intention, and
     final landing point.
   - For long or chaotic prompts, extract 3-6 "must-integrate points"; ignore
     unrelated old requests or wording caused by the user thinking aloud.
   - Compress those points into one governing thesis, such as "这不是在催人早睡,
     而是在说明惜养精神也是君子长远之道."
   - If the user asks to see the拆解, show it briefly before the finished text.
     If not, keep this step internal.

2. Select the output mode.
   - Default: output both **白话译文** and **文言正文**.
   - If the user explicitly asks for only 白话, 通俗版, 现代白话, or 文言白话,
     output only **白话译文**.
   - If the user explicitly asks for only 文言, 纯文言, 古文, 古雅正文, or 文言文,
     output only **文言正文**.
   - For dual output, create one canonical argument first. Draft the文言 meaning
     internally, then render a faithful 白话译文. Show 白话译文 first unless the
     user requests a different order.
   - The two versions must match paragraph count, image order, allusions,
     parallelism, request/praise/warning, and conclusion. Do not add an image,
     argument, or joke to only one version.

3. Choose a ritual-moral spine.
   - Praise/comfort: hardship reveals 德、仁、耐心、明智、担当.
   - Request: a small action sustains 礼、义、家道、君子之责.
   - Warning: a familiar cautionary story proves loss of 礼 or 仁 leads to worry.
   - Self-justification: rest, delay, refusal, repair, or rework follows 圣人之道.
   - Long form must keep every paragraph orbiting the same spine. Do not stack
     disconnected pretty paragraphs.

4. Open far away from the real topic.
   - Default openings: "我曾听说，..." or "我听说古时候，..."
   - Begin with an animal, plant, household object, tool, journey, battlefield,
     craftsman, ruler, friendship, or common historical anecdote.
   - Do not mention the modern subject in the first sentence unless the user
     explicitly asks for a very short version.

5. Build suppression and reversal.
   - Use "论...比不上...，论...比不上...，论...更是远不如..." followed by
     "可是/但是..." to create the central comic turn.
   - The turn must reveal a practical virtue:守、补、救、养、耐、辨、改、敬、
     恕、成事.
   - Map the turn clearly onto the user's reality later; do not leave the image
     floating as decoration.

6. Force铺排 before点题.
   - Include at least one developed parallel passage in every output. Do not
     satisfy this with only a short three-beat action pattern.
   - Parallelism may use three objects, three allusions, three mini-stories,
     three emotional states, three scenes, three consequences, or three actions.
   - For long form, include at least two different kinds of铺排. At least one
     should be medium or long-clause parallelism where each clause contains a
     condition plus a result, such as "再坚固的城门，风雨久了也要重油门轴；再锋利
     的宝剑，斩伐多了也要回炉淬火；再善走的车马，远行久了也要卸轭喂草。"
   - Treat "它错一处，您便查一处；它漏一段，您便补一段；它乱一次，您便理一次。"
     as a narrow micro-pattern only, not the default answer.
   - For long form, prefer one铺排 about ancient imagery or stories and one铺排
     about the modern situation.
   - Prefer repeated oral rhythm over elegant isolated sentences. This style is
     not "文雅第一"; it is "铺排、反转、拐弯说理第一".

7. Use story or allusion as evidence, not ornament.
   - Include at least one story-like element. It may be a familiar historical
     allusion, a folk-style anecdote, or an invented old-world scenario.
   - If using an allusion, explain it in plain Chinese: "这不是在说X，而是在说Y."
   - The story must prove the governing thesis and prepare the final landing.

8. Thicken the Confucian/史官 voice.
   - Write like an anxious loyal minister, household ritualist, or village
     historian who treats a small modern matter as a matter of 德行.
   - Use moral vocabulary naturally and repeatedly: 贤、德、仁、义、礼、恕、忠、
     君子、圣人、道理、宽厚、担当、长远、明智、忠于实情.
   - Avoid direct scolding. Prefer "这正是我所担心的啊" over "你错了"; prefer
     "这难道是贤能的君子该有的行为吗？" over accusation.

9. Handle modern concepts without breaking the tone.
   - Keep unavoidable modern nouns when needed for clarity.
   - First translate them into old-world speech when useful, then clarify:
     "那件会答话的机巧之器，也就是 AI..."
   - Avoid jargon-heavy modern terms when a plainer phrase works. Prefer "做事",
     "交付", "反复", "费心", "劳神", "乱了分寸", "守住条理".

10. Write the 文言正文 when needed.
   - Use 文言 vocabulary and old turns: 吾闻, 昔者, 夫, 然, 今, 是故, 由是观之,
     岂...哉, 非...也, 乃...也, 可不思乎.
   - Keep the same images as the 白话译文, but compress them into classical
     phrasing.
   - Avoid modern connective phrases such as "效率", "压力", "情绪价值", or
     long explanatory colloquial sentences. If a modern object must appear, use
     a classical gloss first, such as "能言之机", and add the modern term only
     when clarity requires it.

11. Return to reality with ceremony.
   - The ending must reveal the real request, praise, warning, apology, or
     comfort.
   - End with a solemn closer such as "阁下不妨细细思索其中的道理。", "您还是好好
     思考一下这个道理吧。", "这正是我所担心的啊。", "这难道不是圣人所称许的贤吗？"

## Quality Checks

Before finalizing, verify:

- The text is mostly modern spoken Chinese, not dense classical Chinese.
  This check applies to 白话译文 only; 文言正文 should be classical-style Chinese.
- If outputting both versions, they match in meaning, images, order, and final
  landing point.
- The opening does not directly state the real issue.
- At least one story or allusion is developed enough to feel like "讲古".
- At least one "比不上...但是..." or equivalent suppression/reversal appears.
- At least one developed铺排 appears; long form needs at least two different
  types, and one should use medium or long clauses.
- Confucian/ritual vocabulary appears as reasoning, not just as decoration.
- The analogy maps to the real situation instead of merely sounding elegant.
- There is clear repetition, parallelism, or double-negative rhythm.
- The final landing point answers the user's real intention, not the user's messy wording.
- The tone is playful, solemn, and earnest, not mean.

## Mini Pattern

Use this pattern flexibly, not mechanically:

```text
**白话译文**

我曾听说，[古物/动物/古人/古事]，论[能力一]比不上[对象一]，论[能力二]比不上[对象二]，论[能力三]更是远不如[对象三]。可是当它[关键处境]的时候，[反复行动与结果]。为什么？就因为[道理]。

如今您[现实处境]，这不正像[类比点]吗？[排比铺陈现实困难]。若说这不[费心/劳神/辛苦]，那是不[明智/忠于实情]的。

[第二比喻或通俗典故]。这不是在说[表面故事]，而是在说[真实道理]。器物尚且如此，何况是人呢？

所以我今日所言，并不是[排除误解]，而是[真实意图]。[回到现实落点]。阁下不妨细细思索其中的道理。

**文言正文**

吾闻[古物/动物/古人/古事]，[能力一]不及[对象一]，[能力二]不及[对象二]，[能力三]又远不及[对象三]。然当其[关键处境]，则[反复行动与结果]。何也？以其[道理]也。

今君[现实处境]，不亦类此乎？[以文言压缩同一现实困难与铺排]。若谓其不[费心/劳神/辛苦]，非明智也，亦非忠于其实也。

[第二比喻或通俗典故的文言表达]。此非言[表面故事]，乃言[真实道理]。器犹如此，而况人乎？

是故吾言，非[排除误解]也，乃[真实意图]也。[回到现实落点]。愿君熟思其理。
```
