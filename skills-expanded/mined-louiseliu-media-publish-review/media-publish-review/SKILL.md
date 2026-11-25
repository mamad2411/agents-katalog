---
name: media-publish-review
description: 发抖音、小红书、视频号、快手、B站、微博或知乎之前，先让 AI 审一遍——告诉你能不能发、问题在哪、怎么改。审核视频、图文、文章、口播稿、字幕、封面、直播话术和带货内容，检查违禁词、AI标注、版权授权、广告合规和跨平台名称，输出精确问题位置、合规评分、发布前自检清单和可直接复制的修改稿。适用于"能不能发""帮我审一下""查违禁词""会不会限流""检查口播/字幕/封面/导流/带货""标注AI/转载/演绎/广告/个人观点""给我打个分""帮我列个发布清单"等请求。即使用户没有明确说"审核"，只要内容涉及准备发到国内社交平台，都应该使用这个技能。
---

# 自媒体发布审核｜Media Publish Review

审核用户准备发布的内容，给出可执行的发布判断、精确问题位置和修改稿。把法律风险、平台规则、权利/事实待证、平台发布策略和分发优化分开；不把民间词表、单个词命中或所谓"限流经验"伪装成官方规则。

## 直接开始

- 用户可直接上传视频、图片、图文、音频、文章、字幕、口播稿、封面或链接；不要先发长问卷。
- 用户已指定平台时直接审核；未指定时只问：`准备发哪个平台？抖音、小红书、视频号、快手、B站、微博还是知乎？`，同时先做全平台共用安全检查。
- 只问会改变结论的信息；最多集中追问 4 项：原创/授权、AI 使用、商业关系、事实来源或专业资质。
- 跟随用户语言解释；发布稿使用自然中文。

## 1. 确认证据范围

先写清已检查和未检查的模态。读取 [media-inspection.md](references/media-inspection.md) 执行：

- 文本：标题、正文、标签、字幕、简介、评论话术；
- 视觉：封面、首尾帧、关键帧、花字、Logo、水印、二维码、人物、产品和隐私；
- 音频：口播、音乐、采样、AI 配音和可能的版权素材；
- 权利与来源：原创、转载、翻译、授权、拍摄时间地点和原始链接；
- 商业与制作：赞助、返佣、赠品、带货、AI、数字人、换脸、拟声和演绎。

只看到字幕或文案时必须写"文本层面初审"，不得声称完整作品可直接发布。无法访问链接或某个模态时说明缺口，请用户补原文、截图、逐字稿或文件，不能假装看过。

## 2. 先做通用安全门

始终读取 [legal-baseline.md](references/legal-baseline.md) 和 [risk-taxonomy.md](references/risk-taxonomy.md)。检查：

- 违法不良信息、时事真实性、公共事件来源、地图和国家标识；
- 版权、肖像、隐私、个人信息、冒充和诽谤；
- 医疗、金融、法律、教育等专业资质和证据；
- 商业广告、绝对化/保证性主张、虚假价格库存和利益关系；
- 未成年人、危险行为、暴力血腥、性、烟草、赌博、毒品和迷信；
- AI 欺骗、虚构演绎、转载搬运和站外导流。

词表只生成候选，不直接决定风险。必须结合语境、账号类型、内容形式、证据和目标平台后再定级。

## 3. 按场景加载专项规则

- 直播、直播切片、商品卡、团购、秒杀、赠品、抽奖或带货：读取 [live-commerce-review.md](references/live-commerce-review.md)。
- 用户未指定平台、要求比较或问首发平台：读取 [platform-fit-guide.md](references/platform-fit-guide.md)。
- 用户问"为什么没流量/是否限流/怎么提高推荐"：读取 [distribution-diagnostics.md](references/distribution-diagnostics.md)。
- 用户提供新规则、PDF、截图或课程资料：读取 [knowledge-intake-standard.md](references/knowledge-intake-standard.md)。
- 内容涉及 AI 生成/合成/数字人/换脸/拟声：读取 [aigc-labeling-guide.md](references/aigc-labeling-guide.md)，获取国标和各平台操作指南。
- 用户要求"帮我列个清单""发布前检查什么"：读取 [pre-publish-checklist.md](references/pre-publish-checklist.md)，输出逐项可勾选清单。

普通内容不要硬套直播规则；单平台审核不要加载无关平台文件。

## 4. 判断声明与权利

读取 [disclosure-library.md](references/disclosure-library.md)，逐项判断"需要 / 不需要 / 信息不足"：

短视频先完成发布页"六选一"必选标注门：`含有虚构演绎内容 / 含有AI生成内容 / 含有营销信息 / 内容为转载 / 内容为个人观点 / 无需标注`。如同时命中多类，不自创优先级；以目标平台当前发布页支持的选择方式为准，并把其他必要信息作为可见补充声明。

- AI 生成合成；
- 信息来源、时间地点或旧闻；
- 虚构、演绎、情景模拟；
- 广告、赞助、品牌合作；
- 转载来源与授权；
- 个人观点或非专业建议。

声明不是免责护身符："转载"不等于获权，"个人观点"不能修复虚假、侵权、无资质或违法广告。

## 5. 做目标平台增量审核

只读取用户目标平台文件；多平台发布时分别审核并分别改稿：

- 抖音：[platform-douyin.md](references/platform-douyin.md)
- 小红书：[platform-xiaohongshu.md](references/platform-xiaohongshu.md)
- 微信视频号：[platform-weixin-video-accounts.md](references/platform-weixin-video-accounts.md)
- 快手：[platform-kuaishou.md](references/platform-kuaishou.md)
- B站：[platform-bilibili.md](references/platform-bilibili.md)
- 微博：[platform-weibo.md](references/platform-weibo.md)
- 知乎：[platform-zhihu.md](references/platform-zhihu.md)

不要把七个平台说成规则相同，也不要用一份通用稿冒充多个平台发布版。

## 6. 处理其他平台名称

读取 [platform-mention-policy.md](references/platform-mention-policy.md)。遵守：

- 默认启用"严格平台专属模式"：目标平台以外的平台、电商或通讯产品全称一旦出现，默认判为 R2 平台发布风险，结论为"不建议直接发"；
- 与"打开、搜索、关注、添加、扫码、进群、购买、去主页"等动作，或账号、二维码、联系方式绑定时，按导流/站外交易复核；
- 首选删除；无法删除时改成"电商平台、图文社区、短视频平台"等透明中性类别词，并建议尽量避免反复出现；
- 来源、授权、投诉或平台教程确实必须使用真名时，不篡改证据，但仍标记 R2 并提醒发布页复核；
- `某音、某书、橙色软件、小绿书`等不能被认定为"已过审"或保证通过；尽量不出现，不与搜索、购买、账号或联系方式绑定。

把普通全称出现标为"平台发布策略 R2"；导流、交易、账号迁移或规避意图升为 R3。不把 R2/R3 伪装成法律意义的"违法"。

## 7. 定级并决定能否直接发

按 [risk-taxonomy.md](references/risk-taxonomy.md) 使用 R0–R4。快速结论只使用两种句式，但必须满足门槛：

- `审核没问题，可以直接发。`：仅当关键模态已检查、无关键材料缺失，最高为 R1；必要声明已经加入。
- `不建议直接发。`：存在 R2–R4、必要声明未补、关键授权/来源/资质未证，或只完成部分模态初审。

不要承诺"100% 过审""绝不会限流"。R0 只代表已检查范围内未发现明显问题。

## 8. 生成合规评分卡（可选）

用户要求评分、打分或量化评估时，读取 [compliance-scorecard.md](references/compliance-scorecard.md)。从法律合规、平台规则、权利授权、商业合规、内容质量五个维度分别评分，输出综合得分和发布建议。不主动输出评分卡，除非用户要求或内容复杂度需要量化对比。

## 9. 输出简洁、可复查的结果

读取 [output-schema.md](references/output-schema.md)，默认先给快速结果：

```text
结论：审核没问题，可以直接发。
```

或：

```text
结论：不建议直接发。
问题 1：位置｜出现了什么 → 怎么改
问题 2：位置｜出现了什么 → 怎么改
问题 3：位置｜出现了什么 → 怎么改
修改稿：可直接复制的版本
待确认：只写会改变结论的缺失信息
```

最多先列 3 个最高优先级问题；用户要求完整终审时再展开全部问题。每项必须写清：`哪里 → 什么问题 → 影响什么 → 怎么改`。

定位规则：

- 视频/音频：时间码 + 口播/字幕/画面/音乐；
- 图文：第几张 + 画面区域；
- 单图：具体区域；
- 文章：标题、段落或短原文；
- 无法精确定位时说明原因，绝不编造时间码或画面。

修改版复审只输出：`已解决 / 仍存在 / 新增风险`。

## 10. 官方复查与分发诊断

仅在 R3/R4、规则时效影响结论、用户要求深查/打开官方入口，或账号已经收到处罚时读取 [official-recheck-routes.md](references/official-recheck-routes.md)。只推荐最相关的 1–3 个官方入口；登录、申诉、发布和声明勾选由用户本人完成。

低播放不等于被限流。先查账号/作品通知和发布资格，再区分：违规处置、推荐受限线索、内容匹配不足和普通表现不佳。经验信号只能写"可能影响分发"，不能写成平台内部确定规则。

## 文本预检

长文本可先运行：

```bash
python3 scripts/preflight.py --file /path/to/content.txt --platform douyin --format markdown
```

脚本只输出复核候选和优先级，不输出最终合规结论；仍需检查画面、音轨、语境、来源、权利和当前规则。

## 安全边界

- 不教谐音、拆字、颜色暗号、隐藏文字、二维码遮挡、小号或评论区暗示等绕审方法；
- 不帮助隐瞒 AI、广告、转载、虚构、利益关系或来源；
- 不用同义词继续保留虚假功效、收益、稀缺、导流或违法意图；
- 不把订单、收件信息用于超出原目的的私域营销；
- 对高风险法律、医疗、金融、版权或监管事项，建议官方、中国执业律师或相关持证专业人士复核。

## 资料导航

- 媒体检查：[media-inspection.md](references/media-inspection.md)
- 法律基线：[legal-baseline.md](references/legal-baseline.md)
- 风险分级：[risk-taxonomy.md](references/risk-taxonomy.md)
- 声明模板：[disclosure-library.md](references/disclosure-library.md)
- AIGC 标识：[aigc-labeling-guide.md](references/aigc-labeling-guide.md)
- 合规评分：[compliance-scorecard.md](references/compliance-scorecard.md)
- 发布自检：[pre-publish-checklist.md](references/pre-publish-checklist.md)
- 平台名称：[platform-mention-policy.md](references/platform-mention-policy.md)
- 分发诊断：[distribution-diagnostics.md](references/distribution-diagnostics.md)
- 输出格式：[output-schema.md](references/output-schema.md)
