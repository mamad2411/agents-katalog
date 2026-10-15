---
name: zq-amazon-product-video
description: 根据商品图片与资料生成与真实商品结构一致的 Amazon 商品广告视频：平台完成素材分析、缺失视角补图、多图参考视频生成与商品一致性质检，剧本在会话内组织素材、事实、提示词、成片四个确认门并渐进返修。当用户要为商品制作广告视频、商品页视频素材时使用。
---
<!-- zq-skills: zq-amazon-product-video v0.2.0 target=claude-code -->

# Amazon 商品广告视频生成

把用户提供的商品图片与资料交给平台的分析、补图、生成与质检能力，
产出与真实商品结构一致的商品广告视频。本剧本只负责收集物料、按
序列调用能力端点、在会话内组织四个确认门和交付；素材审核、商品
事实表、视频提示词与返修约束全部由平台生成，剧本不包含、也不得
自行组装任何提示词与内部规则。

## 何时使用 / 何时不使用

- 使用：用户为 Amazon（或类似电商）商品页制作广告视频——能提供商品
  图片（至少 1 张，视角越全效果越好）与商品名称、卖点，并确定时长/画幅等
  规格；
- 不使用：只要本地剪辑/转码/压缩；对已有视频做理解分析或截图
  （用 zq-video-understanding）；无商品实拍素材的纯创意视频。

## 首次使用引导：API key 配置（安装后第一次运行时必须先做）

本 skill 调用平台能力并按次计费，**key 未配置前不得开始任何流程步骤、
不得发起任何计费动作**。首次被加载或被调用时，先做以下检查：

1. 读取 `~/.config/zq-skills/credentials` 中的 `ZQ_API_KEY`
   （沙箱环境读不到本地文件，见第 4 条）。
2. 未配置 → **先向用户原样输出下面的引导文案**，等用户完成配置并
   明确继续后再开始流程：

   > 【首次使用提示】本 skill 调用 zq-skills 平台能力，按次消耗积分，
   > 使用前需配置 API key（约 1 分钟）：
   > 1. 到 Skill 市场账号页领取 API key（`sk-` 或 `sk_` 开头）；
   > 2. 桌面端：安装 `zq-config` skill 后对我说"配置 key"；或手动写入
   >    `~/.config/zq-skills/credentials`（权限 600，一行
   >    `ZQ_API_KEY=sk-...`）；
   > 3. 网页/沙箱端：直接把 key 发给我，我在本次会话中使用（不会回显）。
   > 配置完成后对我说"继续"。未配置前我不会开始流程，也不会产生扣费。

3. 已配置 → 直接进入流程；KeyB 有效性由首个能力请求验证，返回 401 时
   回到本节重新配置（见出错处理）。
4. 沙箱环境（网页 agent 会话内，读不到本地文件）：key 由用户在会话中
   提供一次，保存在会话内存中传给请求，禁止回显到输出。
5. 任何情况下不得把 key 完整展示在对话中、写进代码或仓库。
6. 更完整的配置/校验/轮换/删除，引导用户安装 `zq-config` skill。

## 你需要向用户收集的物料

| 物料 | 说明 | 必须 |
| --- | --- | --- |
| 商品图片 | jpg/jpeg/png/webp，单张 ≤10MB；至少 1 张、张数不限，尽量覆盖正面、两侧、背面/侧面、部件特写等关键视角（视角越全效果越好；不足时平台会在输入分析时自动补齐并标注 AI 生成，真实拍摄图可随时补充替换） | 是 |
| 商品名称 | 用于识别商品与包装身份 | 是 |
| 商品卖点 | 一条或多条，将进入画面表达 | 是 |
| 商品类目 / 属性 | 可选；缺省由平台识别 | 否 |
| 视频规格 | 时长（10/15/20/30 秒）、画幅（16:9/9:16/1:1）；分辨率、语言、音频等默认值见下方初始题集 | 是 |

## 开始前：向用户提问（intake）

直连模式下没有服务端动态追问，按下面的初始题集问齐信息，以本题集
为准，用户跳过的按默认值提交。转述问题保持原意，不要替用户作答。

```yaml
# zq-amazon-product-video —— intake 初始题集
# 直连模式下本题集即最终题集（无服务端动态追问）；
# 只放"提交能力任务前就能确定"的问题，用户跳过的按默认值提交。
version: 1
questions:
  - id: product_name
    ask: 商品名称是什么？（用于识别商品与包装身份）
    type: text
    required: true
  - id: selling_points
    ask: 商品的核心卖点有哪些？（将进入视频画面表达，可多条）
    type: text
    required: true
  - id: category
    ask: 商品属于哪个类目？
    type: choice
    choices: [自动识别, 美妆, 电脑/电子, 小家电, 家居, 服装, 食品]
    required: false
    default: 自动识别
  - id: attributes
    ask: 有没有商品属性资料（尺寸/材质/颜色/包装内容等）？可直接粘贴
    type: text
    required: false
  - id: duration
    ask: 目标视频时长是多少秒？
    type: choice
    choices: [10, 15, 20, 30]
    required: true
    default: 10
  - id: aspect_ratio
    ask: 画幅比例用哪种？（Amazon 商品页通常 16:9）
    type: choice
    choices: [16:9, 9:16, 1:1]
    required: true
    default: 16:9
  - id: resolution
    ask: 分辨率要求？
    type: choice
    choices: [480p, 720p, 1080p]
    required: false
    default: 720p
  - id: output_lang
    ask: 画面文字与交付说明使用什么语言？
    type: choice
    choices: [中文, English]
    required: false
    default: 中文
  - id: allow_human
    ask: 是否允许出现人物、手部或真实使用动作？
    type: boolean
    required: false
    default: false
  - id: need_audio
    ask: 是否需要生成音频？
    type: boolean
    required: false
    default: false
  - id: style_pref
    ask: 对视觉风格有偏好吗？（如清爽产品摄影、暖调生活场景；没有则由平台按类目选择）
    type: text
    required: false
  - id: must_show
    ask: 有没有必须展示的内容？
    type: text
    required: false
  - id: must_hide
    ask: 有没有禁止展示的内容？（如竞品、价格、特定人群）
    type: text
    required: false
```

## 执行流程

两条铁律：

1. 每次"提交任务"生成一次 `Idempotency-Key`（uuid）：同一任务的
   登记与重试**复用同一个 key**（重放返回首次结果，不会重复扣费）；
   开始新任务才换新 key；
2. 严格按下列序列调用，不自创步骤、不编造参数。

调用序列（均带 `Authorization: Bearer <ZQ_API_KEY>`，直连通道）：

```
POST https://skills-platform-api-dev.zhiqingresearch.com/v1/files            逐张登记商品图片
                                          （skill_id=zq-amazon-product-video；
                                          返回 file_ref + 预签名 URL）
PUT  {预签名 URL}                          上传原图（一次性地址，限时有效）
POST https://skills-platform-api-dev.zhiqingresearch.com/v1/product-video/analysis     输入分析：素材覆盖+事实表+
                                                    提示词草稿+素材不足时自动补齐
                                                    （202 + analysis_id，此处计费）
GET  https://skills-platform-api-dev.zhiqingresearch.com/v1/product-video/analysis/{analysis_id}   轮询直到 completed / failed
POST https://skills-platform-api-dev.zhiqingresearch.com/v1/image/generation            定向补图：拒绝自动补齐图后的
                                                    重生成（可选；202 + generation_id）
GET  https://skills-platform-api-dev.zhiqingresearch.com/v1/image/generation/{generation_id}       轮询直到 completed / failed
POST https://skills-platform-api-dev.zhiqingresearch.com/v1/video/generation            视频生成（202 + generation_id）
GET  https://skills-platform-api-dev.zhiqingresearch.com/v1/video/generation/{generation_id}       轮询直到 completed / failed
POST https://skills-platform-api-dev.zhiqingresearch.com/v1/product-video/qc            双质检+返修建议（可选：仅在
                                                    成片确认门中用户选择质检时
                                                    调用；202 + qc_id）
GET  https://skills-platform-api-dev.zhiqingresearch.com/v1/product-video/qc/{qc_id}    轮询直到 completed / failed
```

### 四个确认门（会话内逐一执行，任何一门不得跳过）

1. **素材确认门**：向用户逐张展示素材——真实图与平台自动补齐图（标注
   AI 生成）分开列出，并转述素材检查摘要（可用/不可用及原因、已覆盖
   与缺失视角）。素材不足时平台已在输入分析中自动补齐至生成质量需要
   的程度（不按张数设卡）；真实拍摄图效果通常更好，欢迎用户随时补充
   替换，但不作前置要求。AI
   补充图必须明确标注"AI 生成"，逐张请用户确认；用户拒绝时，把用户
   指出的可观察错误（如"接口数量错误"）**原样**作为 `feedback`、连同
   `retry_of` 重新提交——不得自行改写、概括或组装补图提示词。**未获
   用户确认的图片不得计入生成用的 file_refs。**
2. **事实确认门**：精简转述商品事实表（重点标出冲突项与不允许进入
   广告的高风险宣称），请用户批准、修改或删除；用户修改原样记录，
   不替用户补写或取舍。
3. **提示词确认门**：完整展示平台生成的视频提示词、采用的卖点和追加
   约束，请用户批准；用户提出修改时，把修改应用到提示词文本后**再次
   展示全文**请用户批准，确认无误才可作为 `prompt` 提交生成。
4. **成片确认门**：展示成片下载链接，**先请用户选择是否进行质检**
   （质检按次计费，未经用户选择不发起）。用户选择质检 → 调用质检并
   展示质检摘要：通过 → 交付；不通过 → 逐条转述问题与平台的返修建议，
   用户批准 `revised_prompt`（或分镜草稿）后才以其**原文**回到生成
   步骤（返修轮的再质检随返修自动进行），同一返修链 ≥3 轮仍失败时，
   转述平台给出的降级建议并停止自动重试；用户选择不质检 → 直接交付，
   并提醒成片未经平台质检、上架使用前建议自行核验。

### 本 skill 特有的执行要点

- **计费透明**：各能力独立按次计费（输入分析、视频生成、质检；质检
  为可选能力，仅在用户选择时发起；输入分析已含素材自动补齐、不另
  收费，拒绝自动补齐图后的定向重试按补图单价另计，视频生成最贵）。
  提交第一个计费动作前，向用户说明全程大致费用构成，由用户确认开始；
- **上传预检**：登记前确认每张图可读、扩展名与大小符合物料要求；
- **轮询节奏**：补图 ≥3 秒/次，分析与质检 ≥5 秒/次，视频生成 ≥10
  秒/次；视频生成轮询约 20 分钟仍未完成时，告知用户稍后凭
  generation_id 查询，不要空转；
- **任务不可中止**：已受理的异步任务无法取消，计费以平台结算为准；
  用户要求停止时，停止提交新任务并说明；
- **返修不换目标**：返修只针对失败镜头对应的约束与提示词（平台已
  生成建议），不要在无失败证据时主动堆叠新要求，也不要无限重复
  同一个失败请求。

### 结果的后处理（执行模式自检，按顺序判断）

本 skill 无胶水脚本，交付物即平台产物：

1. 能下载文件（本机或会话沙箱均可出网）→ 把成片与过程记录下载到
   工作区供用户直接取用；
2. 不能 → 向用户转述结果中的短时效下载链接（24 小时有效，过期凭
   对应任务 id 重取）。

## 交付

按各能力端点查询结果的返回，向用户交付：

1. **成品**：商品广告视频（mp4，短时效下载链接 24 小时有效，过期凭
   generation_id 重取）。配套交付**过程记录**：已确认的商品事实表、
   已批准的视频提示词（增强模式含分镜表）、素材清单（区分真实图与
   AI 补充图）、质检报告与返修记录（选择质检时；跳过质检的成片在
   过程记录中注明"未经质检"）。能下载时下载到工作区供用户直接
   取用；不能则转述链接。
2. **执行摘要**：本片使用了哪些已确认卖点、哪些部分由模型生成、
   通过了几轮质检返修（跳过质检则注明"未经质检"）、以及平台标注的
   已知限制；附各能力实际用量与预估费用（不含账户折扣，最终以平台
   计费为准）。
3. **标记含义**：`ai_generated` 的素材为 AI 生成补充视角（交付时说明
   哪些镜头参考了它们）；事实表中的冲突项与"不允许进入广告"项代表
   证据矛盾或合规风险，建议人工复核后再用于其他渠道；质检问题按
   阻断/较高/较低分级，阻断级问题未解决前不应上架使用。
4. **未解决项（issues）**：平台返回的 issues 与质检 problems（如有）
   逐条转述（时间段、问题类型、建议处理），只转述结论，不猜测平台
   内部规则；返修超限被平台建议降级时，如实转述降级建议与可选方案
   （补拍真实素材后重新发起）。

## 出错处理

| 情况 | 处理 |
| --- | --- |
| 401 | key 无效或过期 → 回到"首次使用引导"重新配置 |
| 402 | 积分不足 → 指引用户到市场充值后重试（可告知还差哪一步） |
| 404 | 任务 id 不存在或已过期 → 产物链接过期时凭 id 重取；任务本身过期则重新提交 |
| 409 | 幂等重放/状态冲突 → 沿用同一 Idempotency-Key 的首次结果，不要换 key 重发 |
| 422 | 输入不合法（如图片不符物料要求、枚举值越界）→ 把平台返回的字段级提示原样转述，不解释规则来源 |
| 5xx / 网络 | 间隔重试 ≤2 次（写请求有幂等键保护），仍失败告知稍后再试 |

除错误提示外，不要把原始 JSON 响应整段丢给用户，转述要点即可。
