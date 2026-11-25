---
name: media-publish-check
description: All-platform pre-publish audit and adaptation for creators publishing to 抖音/Douyin、小红书/Xiaohongshu、微信视频号/Weixin Video Accounts、快手/Kuaishou. Review videos, images, graphic posts, audio, articles, transcripts, subtitles, covers, livestream scripts, product claims, reposted material, and overseas content. Use when users need one Skill to check visible content, spoken claims, AI disclosure, sources, rights, commercial context, platform mentions, livestream commerce, or platform-specific release versions. Trigger on requests such as “能不能发”“发布前审核”“查违禁词/敏感词”“会不会限流”“检查口播/字幕/封面/导流/带货”“标注 AI/转载/演绎/广告/个人观点”, “按我的经验库审核”“保存这次审核”“复盘这条内容”.
---

# Media Publish Check｜自媒体发布审核

审核用户已经完成或正在制作的内容，给出可执行的发布判断、精确问题位置和修改稿。把法律风险、平台规则、权利/事实待证、平台发布策略和分发优化分开；不把民间词表、单个词命中或所谓“限流经验”伪装成官方规则。

## 个人账号记忆与复盘（可选、本地）

仅在用户明确说“开启个人账号记忆 / 按我的经验库审核 / 保存这次审核 / 复盘这条内容 / 查看我的账号规则”时，读取 [personal-account-memory.md](references/personal-account-memory.md)。遵守：

- 资料默认只写入当前用户电脑的 `~/.codex/data/media-publish-check/`；不上传、不共享、不写入本 Skill 文件夹或公开仓库，也不读取其他账号目录。
- 未经用户明确要求，不创建档案、不保存内容、不追问反馈；普通审核流程保持不变。
- 首次开启时，只询问一个本地账号代号；用 `scripts/account_memory.py init` 创建空档案。不要索要姓名、手机号、账号密码、完整原片、订单或聊天记录。
- 用户说“保存这次”时，只记录平台、内容形式、风险标签、审核结论和用户同意保存的简短摘要；默认不保存原始视频、图片、全文、联系方式或未脱敏通知。
- 用户说“复盘这条”时，使用简短复盘卡记录：`已发布/未发布`、`正常/收到通知/驳回/未知`、以及可选的已脱敏通知摘要。不能把低播放当作违规反馈。
- 每次复盘后运行 `scripts/account_memory.py rebuild-candidates`。它只能生成“候选账号提醒”；只有用户明确说“启用候选规则”后，才可写入本地生效规则。
- “按我的经验库审核”时，先运行 `scripts/account_memory.py context`，最多带入 3 条与目标平台和风险标签匹配的已启用提醒。它们仅是账号经验，不得覆盖法律、平台官方规则、授权事实或当前证据。
- 独立 Skill 不能在用户离开后主动发消息或后台追踪发布结果。用户下次回来时，可在不打断当前审核的前提下，用一行询问未回收案例的结果；用户不反馈就保持 `未知`，绝不自行推断。

## 直接开始

- 用户可直接上传视频、图片、图文、音频、文章、字幕、口播稿、封面或链接；不要先发长问卷。
- 用户已指定平台时直接审核；未指定时只问：`准备发抖音、小红书、视频号还是快手？`，同时先做四平台共用安全检查。
- 只问会改变结论的信息；最多集中追问 4 项：原创/授权、AI 使用、商业关系、事实来源或专业资质。
- 跟随用户语言解释；中国平台发布稿使用自然中文。

## 1. 确认证据范围

先写清已检查和未检查的模态。读取 [media-inspection.md](references/media-inspection.md) 执行：

- 文本：标题、正文、标签、字幕、简介、评论话术；
- 视觉：封面、首尾帧、关键帧、花字、Logo、水印、二维码、人物、产品和隐私；
- 音频：口播、音乐、采样、AI 配音和可能的版权素材；
- 权利与来源：原创、转载、翻译、授权、拍摄时间地点和原始链接；
- 商业与制作：赞助、返佣、赠品、带货、AI、数字人、换脸、拟声和演绎。

只看到字幕或文案时必须写“文本层面初审”，不得声称完整作品可直接发布。无法访问链接或某个模态时说明缺口，请用户补原文、截图、逐字稿或文件，不能假装看过。

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

- 海外平台、境外事件或外语材料：读取 [overseas-content-adaptation.md](references/overseas-content-adaptation.md)。
- 直播、直播切片、商品卡、团购、秒杀、赠品、抽奖或带货：读取 [live-commerce-review.md](references/live-commerce-review.md)。
- 用户明确说“抖音星图/商单预审/外流/私域/第三方 App 下载”：在抖音通用审核之外，读取 [douyin-xingtu-diversion.md](references/douyin-xingtu-diversion.md)。
- 用户未指定平台、要求比较或问首发平台：读取 [platform-fit-guide.md](references/platform-fit-guide.md)。
- 用户问“为什么没流量/是否限流/怎么提高推荐”：读取 [distribution-diagnostics.md](references/distribution-diagnostics.md)。
- 用户提供新规则、PDF、截图或课程资料：读取 [knowledge-intake-standard.md](references/knowledge-intake-standard.md)。
- 用户开启个人账号记忆、保存审核或提交发布反馈：读取 [personal-account-memory.md](references/personal-account-memory.md)。

普通内容不要硬套直播规则；单平台审核不要加载无关平台文件。

## 4. 判断声明与权利

读取 [disclosure-library.md](references/disclosure-library.md)，逐项判断“需要 / 不需要 / 信息不足”：

短视频先完成发布页“六选一”必选标注门：`含有虚构演绎内容 / 含有AI生成内容 / 含有营销信息 / 内容为转载 / 内容为个人观点 / 无需标注`。如同时命中多类，不自创优先级；以目标平台当前发布页支持的选择方式为准，并把其他必要信息作为可见补充声明。

- AI 生成合成；
- 信息来源、时间地点或旧闻；
- 虚构、演绎、情景模拟；
- 广告、赞助、品牌合作；
- 转载来源与授权；
- 个人观点或非专业建议。

声明本身不能解决授权、真实性、资质或违法广告问题；“转载”也不代表已经获得授权。

## 5. 做目标平台增量审核

只读取用户目标平台文件；多平台发布时分别审核并分别改稿：

- 抖音：[platform-douyin.md](references/platform-douyin.md)
- 小红书：[platform-xiaohongshu.md](references/platform-xiaohongshu.md)
- 微信视频号：[platform-weixin-video-accounts.md](references/platform-weixin-video-accounts.md)
- 快手：[platform-kuaishou.md](references/platform-kuaishou.md)

不要把四个平台说成规则相同，也不要用一份通用稿冒充四个平台发布版。

星图专项是“导流与第三方下载高优先级预检”，不是对全部抖音内容的独立合规结论；不能跳过法律基线、证据范围和正式发布页复核。

## 6. 处理其他平台名称

读取 [platform-mention-policy.md](references/platform-mention-policy.md)。遵守：

- 默认启用“严格平台专属模式”：目标平台以外的平台、电商或通讯产品全称一旦出现，默认判为 R2 平台发布风险，结论为“不建议直接发”；
- 与“打开、搜索、关注、添加、扫码、进群、购买、去主页”等动作，或账号、二维码、联系方式绑定时，按导流/站外交易复核；
- 首选删除；无法删除时改成“电商平台、图文社区、短视频平台”等透明中性类别词，并建议尽量避免反复出现；
- 来源、授权、投诉或平台教程确实必须使用真名时，不篡改证据，但仍标记 R2 并提醒发布页复核；
- `某音、某书、橙色软件、小绿书`等不能被认定为“已过审”或保证通过；尽量不出现，不与搜索、购买、账号或联系方式绑定。

把普通全称出现标为“平台发布策略 R2”；导流、交易、账号迁移或规避意图升为 R3。不把 R2/R3 伪装成法律意义的“违法”。

## 7. 定级并决定能否直接发

按 [risk-taxonomy.md](references/risk-taxonomy.md) 使用 R0–R4。快速结论只使用两种句式，但必须满足门槛：

- `审核没问题，可以直接发。`：仅当关键模态已检查、无关键材料缺失，最高为 R1；必要声明已经加入。
- `不建议直接发。`：存在 R2–R4、必要声明未补、关键授权/来源/资质未证，或只完成部分模态初审。

不要承诺“100% 过审”“绝不会限流”。R0 只代表已检查范围内未发现明显问题。

## 8. 输出简洁、可复查的结果

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

## 9. 官方复查与分发诊断

仅在 R3/R4、规则时效影响结论、用户要求深查/打开官方入口，或账号已经收到处罚时读取 [official-recheck-routes.md](references/official-recheck-routes.md)。只推荐最相关的 1–3 个官方入口；登录、申诉、发布和声明勾选由用户本人完成。

低播放不等于被限流。先查账号/作品通知和发布资格，再区分：违规处置、推荐受限线索、内容匹配不足和普通表现不佳。经验信号只能写“可能影响分发”，不能写成平台内部确定规则。

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
- 平台名称：[platform-mention-policy.md](references/platform-mention-policy.md)
- 星图专项：[douyin-xingtu-diversion.md](references/douyin-xingtu-diversion.md)
- 分发诊断：[distribution-diagnostics.md](references/distribution-diagnostics.md)
- 个人账号记忆：[personal-account-memory.md](references/personal-account-memory.md)
- 输出格式：[output-schema.md](references/output-schema.md)
