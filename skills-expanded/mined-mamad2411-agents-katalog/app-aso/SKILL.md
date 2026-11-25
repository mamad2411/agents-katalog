---
name: app-aso
canonical_id: discoverability.app-aso
aliases: [aso, app-store-optimization, google-play-optimization, store-listing]
version: 1.0.0
status: stable
created_date: 2026-05-25
parent: discoverability-orchestrator
layer: L12
sibling-skills:
  - web-seo          # 标准 web SEO（不重叠）
  - web-aeo          # AI search（不重叠）
  - web-local-seo    # Local SEO（不重叠）
upstream:
  - discoverability-orchestrator
  - uiux-product-orchestrator
downstream:
  - enterprise-qa-testing      # release evidence bundle 引用 ASO evidence
allowed-tools: Read, Grep, Glob
forbidden-tools: WebFetch
disable-model-invocation: false
description: >-
  App Store Optimization (ASO) — store-side discoverability for the iOS App Store and Google Play: metadata, visual assets, localization, ratings and reviews, store experiments, product page optimization, and ASO measurement (keyword difficulty, ranking, conversion, install funnel). Not web SEO, AI search, Local SEO or security, and never writes app implementation code.
---

# App Store Optimization (L12 / app-aso)

> **本 skill 仅负责 App Store / Google Play 商店内的可发现性。**
> 上游：`discoverability-orchestrator` 路由进入。
> 兄弟：`web-seo` / `web-aeo` / `web-local-seo`（4 域严格独立，不互相串味）。

---

## 1. 概述与适用场景

### 1.1 适用

- iOS app 上架 **App Store**（Apple App Store Connect 管理）
- Android app 上架 **Google Play**（Google Play Console 管理）
- 同时上 iOS + Android 的 cross-platform app
- 已在线 app 的 listing audit / 优化 / experiment 配置

### 1.2 不适用

- 纯 web app / PWA（→ `web-seo` / `web-aeo`）
- 仅在第三方分发渠道（如企业内部 MDM、TestFlight 私测、Google Play 内测轨道）的 app —— 这些不参与 store 公开 discovery
- 中国 Android 第三方应用市场（华为 / 小米 / OPPO / VIVO / 应用宝等） —— 本 skill 不覆盖，需另设独立 skill 治理

### 1.3 严格不做

| 主题 | 路由到 |
|---|---|
| App 本身的 Swift / Kotlin / Flutter / React Native 代码 | L5 Platform: `apple-ios-hig` / `apple-swiftui` / Android 相关 skill |
| Apple Human Interface Guidelines / Material Design 实施 | L5 Platform |
| 标准 web SEO（Google / Bing 搜索引擎收录） | `web-seo` |
| AI search（ChatGPT Search / Claude Search / Perplexity） | `web-aeo` |
| Local SEO / Google Business Profile / Apple Maps | `web-local-seo` |
| Security / threat model / pentest | `appsec-security-orchestrator`（独立主线）|
| 隐私政策法律审核 / GDPR / CCPA 合规法律咨询 | 法律 / Compliance（不在本 skill 范围）|

**铁律**：本 skill 不写一行 app 代码。ASO 是 store-listing artifact 治理 + listing audit + experiment readiness。

---

## 2. 目标链路

```
store metadata → visuals → localization → ratings/reviews → experiments → analytics
       │            │           │              │               │             │
       ▼            ▼           ▼              ▼               ▼             ▼
  字段长度/    icon/截图/    多语言       评分/评论      A/B 测试       store
  关键词       预览视频      listing 覆盖   响应率         配置          搜索/转化
                                                                         指标
```

每一段都有专门的 evidence 产出（见第 10 节）。链路前段（metadata、visuals）是 release blocker，后段（experiments、analytics）是持续优化层，但都属于本 skill 治理范围。

---

## 3. 执行宪法（继承 L12，调整为 ASO 现实）

L12 上层 `discoverability-orchestrator` 定义了 **Script-first, Skill-second, AI-last** 5 层优先级。ASO 域内的现实差异：

- **Script-first 范围更窄**：App Store Connect API / Google Play Developer API 能读写部分 metadata，但远不覆盖全部（如截图视觉质量、文案写作质量、competitor benchmark 无 API）
- **Artifact-check 比例更高**：截图、icon、preview video、feature graphic 是文件 artifact，工具能验"格式 / 尺寸 / 数量"，但**不能**判定"视觉质量 / 营销力 / 文化适配"
- **Manual review 不可避免**：visual quality、写作质量、competitor analysis、experiment 创意必须人工

### 3.1 ASO 执行优先级（重写自 L12 通用版）

```
ASO Execution Priority

1. Deterministic API / config check
   App Store Connect API（读取 metadata 字段）
   Google Play Developer API（读取 listing fields）
   字段长度计算（character count，注意 UTF-16 / grapheme 差异）
   privacy policy URL 可达性（HTTP 200）
   visual asset 文件检查（尺寸 / 格式 / 透明度 / 数量）

2. Listing artifact parser
   读 fastlane metadata 目录（fastlane/metadata/ 或 fastlane/android/metadata/）
   读 Google Play 的 listings/<locale>/ 目录结构
   生成 store-listing.json evidence

3. Structured evidence aggregator
   汇总各 locale × 各 store 的字段覆盖
   计算 localization coverage matrix
   不调 AI，纯结构化产出

4. AI synthesis from evidence
   读 store-listing.json + screenshots-previews.json
   生成 finding narrative / 修复优先级 / 建议
   AI 不替代 visual quality 判断

5. Manual review（仍是 ASO 头等环节，不只是 last resort）
   - visual quality of screenshots / icon / feature graphic
   - 文案 voice/tone 是否 on-brand
   - localization 是否真的"本地化"（不只是机翻）
   - competitor benchmark
   - experiment 创意 ideation
```

**反规则**（违反即 BLOCKED）：
- ❌ 让 AI 凭感觉给"截图营销力打分"当作客观 evidence
- ❌ 跳过 API / artifact 检查直接靠 AI 总结 metadata 完整性
- ❌ 把 AI 生成的 keyword 列表当作"App Store 官方 ranking factor"

### 3.2 可自动 vs 必须人工

| 任务 | 可自动 | 必须人工 |
|---|:---:|:---:|
| metadata 字段长度（30 / 80 / 170 / 4000 char 限制） | ✓ | |
| privacy policy URL 存在 + HTTP 可达 | ✓ | |
| privacy policy URL 内容法律合规 | | ✓ |
| localization coverage matrix（哪些 locale 缺哪些字段） | ✓ | |
| localization 翻译质量 / 文化适配 | | ✓ |
| screenshots 数量 / 尺寸 / 格式合规 | ✓ | |
| screenshots 视觉质量 / 营销力 / 信息密度 | | ✓ |
| icon 尺寸 / 透明度 / 边角合规（Apple 不允许 alpha + transparent corner，iOS 18+, Apple App Store Guidelines spec 2024-06） | ✓ | |
| icon 视觉辨识度 / brand consistency | | ✓ |
| keywords field 是否填写（Apple，100 byte limit，按 UTF-8 计算） | ✓ | |
| keywords 关键词研究 / competitor benchmark | | ✓（用 Sensor Tower / data.ai / AppTweak）|
| ratings 整体分数 + review 响应率 | ✓ | |
| review reply voice/tone 是否符合 brand | | ✓ |
| Apple PPO / Google Play Store Listing Experiment 是否配置 | ✓ | |
| experiment 创意 / 假设 / 解读 | | ✓ |

---

## 4. App Store（Apple）核心检查

### 4.1 Metadata 字段

| 字段 | 长度限制 | 是否必填 | 是否高搜索权重 | 备注 |
|---|---|:---:|:---:|---|
| **app name** | 30 字符 | 必填 | 极高 | App Store 搜索算法权重最高字段之一；不能堆关键词 |
| **subtitle** | 30 字符 | 选填（强推） | 高 | 第二高权重；与 name 联合优化 |
| **description** | 4000 字符 | 必填 | 低（不参与 keyword 索引） | 转化要素，不是搜索要素 |
| **promotional text** | 170 字符 | 选填 | 不参与索引 | 可随时更新，无需新版本（适合时令活动）|
| **keywords field** | **100 bytes**（UTF-8 byte 长度，不是字符；逗号分隔，不含空格更优） | **必填 + localizable**（对 launch 必填，但已发布版本的变更非紧急 → 见第 8 节 warn） | 极高 | Apple 搜索算法核心输入；不向用户展示。**CJK / emoji / 多字节字符按 UTF-8 byte 计算**（1 个汉字通常 3 byte，1 个 emoji 通常 4 byte），按字符数计算会严重高估容量 |
| **category** | 1 primary + 1 secondary | primary 必填 | 中 | 影响 browse + 排行榜可见性 |
| **privacy policy URL** | URL | **必填**（缺则被拒）| 不参与排名 | App Store Review 强制要求 |
| **support URL** | URL | 必填 | 不参与排名 | |
| **marketing URL** | URL | 选填 | 不参与排名 | |
| **age rating** | 4+/9+/12+/17+ | 必填 | 影响可见性范围 | 通过 questionnaire 自动评定 |
| **in-app purchase 描述** | 单个 IAP 最多 30 字符 name + 45 字符 desc | 有 IAP 时必填 | 中 | IAP 名称也参与搜索索引 |
| **what's new** | 4000 字符 | 新版本必填 | 不参与索引 | 影响更新转化 |

**关键 do/don't**：
- ✅ app name 用品牌 + 1-2 核心 value keyword（例："Notion - Notes, Docs, Tasks"）
- ❌ app name 不要塞 5+ 关键词逗号串（违反 App Store Review Guideline 2.3.7）
- ✅ keywords field 用 single words / 短词组，逗号分隔，**避免空格**和重复；长度按 **UTF-8 byte** 计算，不是字符数（CJK / emoji 占多 byte）
- ✅ 不要在 keywords field 重复 app name 和 subtitle 中已出现的词（Apple 索引会自动合并 app name + subtitle + keywords field）
- ✅ 不要用 competitor brand 名作为 keyword（违反政策 + 法律风险）

### 4.2 Visual 素材

| 素材 | 规格 | 数量要求 | 备注 |
|---|---|---|---|
| **app icon** | 1024×1024 PNG | 1 个 | **不允许 alpha channel**；**不允许 transparent corner**（Apple 会自动应用 mask；iOS 18+, Apple App Store Guidelines spec 2024-06） |
| **iPhone 6.9" screenshots**（iPhone 16 Pro Max / 17 Pro Max 等当前主规格） | 1290×2796 | **1-10 张**（min 1，推荐 3-5 张以铺满 list view） | 当前 Apple 主推 iPhone 规格 |
| **iPhone 6.7" screenshots** | 1290×2796 / 1284×2778 | 1-10 张（兼容老的 6.7" 设备） | iPhone 15 Pro Max / 14 Pro Max 等 |
| **iPhone 6.5" screenshots** | 1242×2688 / 1284×2778 | 1-10 张（选填，回退兼容） | 兼容老设备 |
| **iPhone 5.5" screenshots** | 1242×2208 | 选填（部分新 app 不再要求） | iPhone 8 Plus 时代规格 |
| **iPad Pro 13" screenshots**（M4 当前规格） | 2064×2752 | iPad app 必填，1-10 张 | 当前 Apple 主推 iPad 规格 |
| **iPad Pro 12.9" screenshots**（旧 6th gen / 5th gen） | 2048×2732 | 选填（回退兼容） | 兼容老 iPad |
| **app preview video** | H.264 / ProRes，每个 device 最多 3 个，15-30s | 选填（强推） | 极大提升转化；与 screenshot 1 共用第一帧 |

**关键 do/don't**：
- ✅ Screenshot #1 是首屏最重要的转化要素（list view 默认只显示前 3 张）
- ✅ Apple 官方允许 **每组 1-10 张**；blocker 是"min 1 张 per required device class"；3-5 张为 warn-only 推荐（不是 blocker）
- ✅ 截图可以是 marketing composition（叠加文字、设备框、营销文案），**不必**是纯 raw screenshot
- ❌ icon 含透明 corner 会被 Apple Review 拒（自动 mask 会露出透明区，丑）
- ❌ icon 含 alpha channel 会被自动拒收

### 4.3 Localization（App Store）

- 每个 storefront 语言**独立** metadata（name / subtitle / description / keywords / promotional text 全部独立）
- screenshots 可按 locale 替换（极大影响转化，文化适配 > 文字翻译）
- preview video 可按 locale 替换
- 默认 locale 必须填全；其他 locale 缺失字段会 fallback 到默认 locale

**支持的 storefront**：约 175 个国家/地区，约 40 种语言。常见优先 locale：
- en-US, en-GB, en-AU
- zh-Hans (China), zh-Hant (Taiwan), zh-HK
- ja, ko
- de, fr, es-ES, es-MX, pt-BR, it, nl
- ru, ar, hi, tr, pl, id, th, vi

**关键 do/don't**：
- ✅ 至少把 top 5 target market 完整本地化（含 screenshots）
- ❌ 不要只翻译 text 不本地化 screenshots（错失大量市场）
- ❌ 不要用机翻直接发布；至少 native speaker review

### 4.4 Privacy / Compliance（与 store discoverability 相关部分）

> 本 skill 只做**与 listing 可发现性相关**的 privacy / compliance artifact 检查。**不做法律合规审查**，不替代法律咨询，也不做 AppSec threat model。

| 项目 | 是否 blocker | 备注 |
|---|:---:|---|
| **privacy policy URL 字段填写** | ✓ | App Store Review 强制；缺 URL 直接被拒 |
| **App Privacy "nutrition label"** | ✓ | 数据收集 / tracking 声明；填错会被 reject |
| **App Tracking Transparency 描述**（如使用 IDFA） | 条件性 ✓ | 使用 IDFA 时必填 NSUserTrackingUsageDescription |

字段是否填写可自动检查，**填写内容是否准确反映 app 行为不在本 skill 范围**（需要 product + legal review）。

### 4.5 Product Page Optimization (PPO)

Apple 自 iOS 15 提供的 App Store 内置 A/B 测试工具：

| 维度 | 规则 |
|---|---|
| 同时跑的 treatment | 最多 3 个 + 1 个 control（共 4 variant） |
| 可测变量 | app icon / screenshots / app preview videos |
| 流量分配 | 至少 1% per treatment（建议 25%）|
| 持续时间 | 至少 7 天，建议 90 天 |
| 结果指标 | impressions, product page views, conversion rate |
| 灵活性 | 可中途 promote winning treatment 为 default |

**Listing audit 检查项**：
- 是否启用 PPO（new release / major redesign 时强推荐启用）
- 是否有 hypothesis 文档（人工 artifact）
- 是否每个 treatment 都有明确假设 + 成功指标

### 4.6 Custom Product Pages (CPP)

Apple 自 iOS 15 提供，按 paid campaign / referral source 定制 store page：

| 维度 | 规则 |
|---|---|
| 数量上限 | 最多 35 个 CPP per app |
| 可定制 | screenshots / preview videos / promotional text |
| 不可定制 | name / subtitle / description / keywords / icon |
| 使用场景 | Apple Search Ads、社交广告 deeplink、邮件 campaign |

**Listing audit 检查项**：
- 是否定义了 channel-specific CPP（有 paid acquisition 时强推荐）
- 每个 CPP 是否有命名约定 + 用途 doc

### 4.7 In-App Events（Apple，iOS 15+）

App Store 内被**索引的发现面**：event card 可出现在 Search、Today、以及 product page，直接带来曝光与下载。是 listing 之外的独立 discoverability surface（闲置 = 漏掉一个免费曝光位）。

| 维度 | 规则 |
|---|---|
| 类型 | challenge / competition / live event / major update / new season / premiere / special event |
| 展示位 | Search 结果、Today tab、product page event card、editorial（可被推荐）|
| 元数据 | event name（30 字符）/ short description（50）/ long description / deep link / event card art |
| 数量 | 同时最多 5 个 active；每个有 start/end time |

**Listing audit 检查项**：
- 是否使用 In-App Events（有 live ops / 季节性内容 / 重大更新的 app 强推荐）
- event 是否配 deep link（点击直达对应 app 内内容）
- event card art 是否符合 Apple 规格（不堆文字）

> 闲置即 warn `in_app_events_unused`（Apple）—— warn-only，不阻断 release。

---

## 5. Google Play 核心检查

### 5.1 Metadata 字段

| 字段 | 长度限制 | 是否必填 | 备注 |
|---|---|:---:|---|
| **app title** | 30 字符 | 必填 | 主搜索字段；与 short description 联合权重 |
| **short description** | 80 字符 | 必填 | listing 上方摘要；高搜索权重 |
| **full description** | 4000 字符 | 必填 | 搜索算法**会**索引（与 Apple description 不同）|
| **app icon** | 512×512 PNG / 32-bit | 必填 | 透明度允许，但不推荐 |
| **feature graphic** | 1024×500 PNG / JPEG（不能用 alpha） | 必填 | 上架必需；list view 顶部展示 |
| **screenshots（手机）** | 至少 320 px，最长边 ≤ 3840 px，宽高比 16:9 ~ 9:16 | publish minimum **2 张**（Google publish 门槛），最多 8 张 | |
| **screenshots（7-inch tablet）** | 同上 | 若声明 tablet support，**至少 4 张**（Google large-screen eligibility 门槛） | 区分 publish minimum（手机 2）vs large-screen eligibility（tablet/Chromebook 4） |
| **screenshots（10-inch tablet）** | 同上 | 若声明 tablet support，**至少 4 张** | 同上 |
| **screenshots（Chromebook / large-screen）** | 平台专用规格 | 若声明 Chromebook support，**至少 4 张** | Chromebook 与 tablet 同属 large-screen eligibility |
| **screenshots（Wear OS / Android TV）** | 平台专用规格 | 若声明 form factor 必填（按 Google 当前规则；Android TV 通常 ≥ 1，Wear OS ≥ 1）| |
| **promo video** | YouTube URL | 选填 | 与 feature graphic 互斥展示 |
| **app category** | 1 个 | 必填 | |
| **tags** | 最多 5 个 | 选填（强推） | Google Play 推荐系统输入 |
| **contact details** | email / phone / website | email 必填 | |
| **privacy policy URL** | URL | **必填**（缺则被拒） | Google Play Policy 强制 |
| **content rating** | IARC 评级 | 必填 | 通过 questionnaire 自动评定 |
| **data safety form** | 数据收集声明 | 必填 | 类似 Apple App Privacy |

**关键 do/don't**：
- ✅ app title + short description + full description 都参与搜索索引（与 Apple 不同，Apple 的 description 不参与索引）
- ✅ short description 是 above-the-fold 转化关键，前 80 字符决定点击
- ❌ keyword stuffing 在 title / description 会被算法降权（Google Play Policy: Repetitive Content / Spam）
- ❌ 使用 Apple / iOS 字眼推广跨平台 app 时小心 trademark 风险

### 5.2 Localization（Google Play）

- 每种语言**独立** store listing（title / descriptions / graphic assets）
- 至少覆盖 **top 5 target market**
- Google Play 自动翻译可选，但**不推荐**直接采用（流于机翻）
- 默认语言之外的 locale 缺失字段会回退到默认

**支持的 locale**：约 70+ 种语言。常见优先 locale 与 App Store 类似。

### 5.3 Store Listing Experiments

Google Play 提供的官方 A/B 测试：

| 维度 | 规则 |
|---|---|
| 同时跑的 experiment | 最多 5 个 per app |
| 可测变量 | app icon / feature graphic / screenshots / short description / full description / promo video |
| 流量分配 | 自动分配；可调比例 |
| 持续时间 | 至少 7 天 + 足够 install 信号（per Google 建议 ≥ several thousand installs per variant） |
| 结果指标 | retention-adjusted install conversion |
| 跨 locale | 可按 locale 跑独立 experiment |

**Listing audit 检查项**：
- 是否启用 Store Listing Experiment
- experiment 是否有 hypothesis + 成功阈值
- 是否每个 experiment 跑满 7 天（早停会导致假阳性）

### 5.4 Custom Store Listings

Google Play 按维度定制 listing：

| 维度 | 可定制要素 |
|---|---|
| **country / region** | 整体 listing |
| **install state**（已安装 / 未安装 / 已卸载） | descriptions / graphics |
| **pre-registration** | 上线前 teaser listing |
| **Google Ads campaign** | 整体 listing 按 ad source 区分 |

数量上限：最多 50 个 custom store listings per app。

**Listing audit 检查项**：
- 有 pre-launch 阶段是否配置 pre-registration listing
- 有 paid acquisition 时是否配置 campaign-specific listing

### 5.5 Promotional Content / LiveOps（Google Play）

Google Play 对应 Apple In-App Events 的发现面：promotional content / LiveOps cards 让 major update / event / offer 出现在 Play Store 发现面（store listing 之外）。

| 维度 | 规则 |
|---|---|
| 类型 | major update / event / special offer / pre-registration milestone |
| 展示位 | Play Store 发现面 / listing 上的 promotional card |
| 适用 | 有 live ops / 周期活动 / 季节内容的 app |

**Listing audit 检查项**：
- 是否使用 promotional content / LiveOps（有周期活动的 app 强推荐）
- promo 是否配 deep link + 起止时间

> 闲置即 warn `promotional_content_unused`（Google）—— warn-only。

---

## 6. 共同 ASO 原则（跨 store）

### 6.1 关键词研究

- **必须**用 store-specific 工具：Sensor Tower / data.ai (App Annie) / AppTweak / Mobile Action / ASOdesk / Apptopia
- **绝不**直接照搬 web SEO keyword research：
  - App store search behavior 短、即时、转化导向（"video editor" 而非 "best free video editor for iOS without watermark 2026"）
  - 长尾词在 store 不如 web 重要
  - Apple keywords field 是不展示的元数据，与 SEO meta keywords（已废）不同性质
- **优先指标**：search volume, difficulty, current ranking, competitor coverage
- **locale keyword 套利（Apple）**：Apple 的 keywords field 按 locale 各算 100-byte 预算——给 en-GB / es-MX 等额外 locale 填 keyword field，即便 app 主要面向美国，也能拿到**额外**关键词覆盖（同语言不同 locale 的字段会被一并索引）。低成本扩词手段；注意别在多个 locale 重复同一批词（浪费预算）。

### 6.2 keyword stuffing 严禁

- Apple App Store Review Guideline 2.3.7：禁止 misleading / spammy app name 和 metadata
- Google Play Policy: Spam（Repetitive Content）：禁止重复关键词
- 违反后果：listing rejection / 强制改 metadata / 严重时下架

### 6.3 Screenshots 是头等转化要素

研究反复证明：**很多用户不读 description**，只看 icon + 前 3 张 screenshot 就做下载决定。

- Screenshot #1 必须 self-explanatory（首屏不依赖 #2-#10）
- 截图叠加文字（"caption screenshots"）转化率通常优于纯 raw UI
- 视频 preview / app preview 是锦上添花，但**不能**取代 screenshots

### 6.4 App Preview / Feature Graphic 决定 above-the-fold 印象

- App Store list view：icon + name + subtitle + screenshots #1-#3
- Google Play list view：icon + name + short description + feature graphic（或 promo video）

这是 store-level browse 时的"广告位"，比 description 重要得多。

### 6.5 Ratings 是 search ranking 直接信号

- Apple App Store: ratings 影响搜索排名 + browse 推荐 + 编辑推荐
- Google Play: ratings 是 install conversion 强信号，间接影响 ranking
- 4.0 ⭐ 以下需要 active intervention（review reply / product fix）

### 6.6 Localized creatives, not just translations

- 文字翻译只是入门；真正的 localization 包括：
  - screenshots 按文化习惯重做（颜色 / 模特 / 内容场景）
  - icon 按文化偏好调整（部分市场偏好不同视觉风格）
  - preview video 按市场重拍 / 重新配音
  - 价格按区域调整（Apple / Google 自动支持，但需检查 tier）
- **不本地化 screenshots** 是 ASO 最常见漏洞之一

### 6.7 Respond to reviews

- Apple 和 Google 都允许开发者回复 review，且公开展示
- 回复率影响：
  - 用户感知 brand responsiveness
  - 部分用户会修改 rating（差评 → 好评）
  - 算法层面对"active development"的 signal
- 回复 voice/tone 必须 on-brand，避免模板化机械回复

**回复模板（reply-template，按场景改写 — 不要逐字复用成机械模板）**：

| 场景 | 回复骨架（on-brand 改写后用）|
|---|---|
| 差评 / bug 报告 | 「抱歉给你带来了 {具体问题}。我们 {version X.Y} 已修复 / 正在修，能否 {联系渠道} 给我们 {复现步骤 / 设备信息}？修好会回来更新。」——**先共情 → 给具体动作 → 留升级渠道**，绝不辩护 |
| 功能缺失请求 | 「谢谢建议！{feature} 已记入 roadmap / 已在 {版本} 计划。这类反馈对我们排优先级很有帮助。」——承认但不承诺不存在的日期 |
| 好评 | 「谢谢 {具体提到的点}！很高兴 {功能} 帮到你。」——提一句用户实际写的内容，证明不是模板 |
| 误解 / 已有功能 | 「这个能力其实在 {路径} 已经有了 —— {一句怎么用}。需要的话 {渠道} 找我们。」——纠正但不居高临下 |

**差评升级路径（escalation）**：
1. **1-2★ 且涉及 data-loss / 崩溃 / 计费 / 隐私** → 标 high-priority，48h 内回复 + 路由给工程/支持工单，**不只在 store 回**。
2. **重复同一 bug 的多条差评** → 聚合成一个 issue，回复里引同一 fix 版本；修复后回到这些 review 更新回复（部分用户会改 rating）。
3. **疑似 data-loss / 安全 / 隐私泄漏的指控** → 不在公开 review 里讨论细节，引导私下渠道；若证实涉私密数据泄漏 → 这是 AppSec 范畴，**escalate 给 AppSec**（本 skill 不做安全处置）。
4. 用平台原生 API 一视同仁征集评分：iOS `SKStoreReviewController` / Android Play In-App Review API（**绝不**只向满意用户选择性弹窗 —— 见 §7 `selective_review_solicitation` blocker + §12#5b/#5c 合规禁令）。

> **§8 的 30% / 90 天 reply-rate SLA 是本 harness 设定的内部运营建议阈值，不是 Apple / Google 官方强制要求** —— 项目可按支持团队产能调整；它是 warn（运营提醒），不是 §7 blocker。

---

## 7. Blocker（必须阻断 release）

下列任一为真，release 被本 skill gate 阻断。除非显式 waiver（必须在 `discoverability.config.yaml` 注明原因 + 责任人）。

| Blocker ID | 触发条件 |
|---|---|
| `app_store_listing_missing_required_metadata` | Apple 必填字段（name / description / category / privacy policy URL / age rating / support URL）任一缺失 |
| `google_play_listing_missing_required_metadata` | Google 必填字段（title / short description / full description / app category / privacy policy URL / content rating / data safety / contact email）任一缺失 |
| `privacy_policy_missing_for_app_distribution` | 任一 store 的 privacy policy URL 字段为空，或 URL 返回非 2xx |
| `screenshots_min_1_for_iOS_per_device_class` | Apple：iPhone 主截图组 < 1 张 / iPad app 缺 iPad 截图组（任一 required device class < 1 张）；Apple 官方下限为 1，每组上限 10 |
| `screenshots_min_2_for_android_phone` | Google：手机截图组 < 2 张 |
| `screenshots_min_4_for_large_screen_eligibility` (Google) | Google：声明支持 tablet（7"/10"）/ Chromebook / Wear OS / Android TV 但任一 form factor < 4 张 → 失去 large-screen surface eligibility（手机 publish 最低 2 张；large-screen eligibility 最低 4 张）|
| `icon_not_meeting_store_specs` | Apple：icon 不是 1024×1024 / 含 alpha channel / 含 transparent corner；Google：icon 不是 512×512 / 不是 32-bit PNG |
| `app_name_or_title_exceeds_character_limit` | Apple app name > 30 / subtitle > 30；Google title > 30 / short description > 80 / full description > 4000 |
| `content_rating_or_age_rating_missing` | Apple age rating questionnaire 未完成；Google IARC questionnaire 未完成 |
| `in_app_purchase_metadata_missing_or_inconsistent` | 有 IAP 但 IAP localized name / description 缺失或与 app metadata 矛盾 |
| `feature_graphic_missing` (Google only) | Google Play 必填 feature graphic 缺失 |
| `data_safety_form_incomplete` (Google only) | Google Play data safety 表未填或与 manifest 声明不一致 |
| `selective_review_solicitation` (review gating) | App 内 review prompt 对用户做满意度筛选（仅引导高分用户去 store / 把差评导向 support） —— 违反 Apple App Store Review Guideline 1.1.7 + Google Play Developer Policy + FTC 规则。修复：改用 SKStoreReviewController / Play In-App Review API，对所有用户一视同仁 |

**Blocker 触发后**：
- 在 channel evidence `evidence/discoverability/<tag>/aso.json` 的 `findings[]` 写一条 `severity: blocker` 的 finding（**不**自产 `gate-result.json` —— gate 产物只由 `discoverability-sdk gate.check` 写 `<tag>/gate-result.yaml`）
- 报告中标红
- `discoverability-orchestrator` 的 `gate-result.yaml` 会聚合反映该 blocker
- release 流程必须阻断或显式 waive

---

## 8. Warn-only（不阻断 release，但写入 report）

下列项不阻断 release，但应在 report 中显著提示，长期改进。

| Warn ID | 触发条件 | 建议 |
|---|---|---|
| `screenshots_not_localized` | 多 locale listing 但 screenshots 全 locale 共用 | 至少 top 3 market 本地化 screenshots |
| `app_preview_video_missing` | Apple：无 app preview video；Google：无 promo video | 强推荐添加，转化提升显著 |
| `ratings_review_response_rate_low` | 过去 90 天 review reply 率 < 30%（任一 store） | 设立 review reply SLA |
| `product_page_experiment_not_configured` | Apple：未启用 PPO；Google：未启用 Store Listing Experiments | 新 release / major update 强推荐启用 |
| `keyword_field_unused` (Apple only) | 已发布版本的 Apple keywords field 为空或 byte 使用率 < 50%（按 UTF-8 byte 计算） | 100 byte 几乎免费的搜索权重，不用浪费。**注意**：keywords field 是 Apple required field —— 新 release 时空字段属于 `app_store_listing_missing_required_metadata` blocker；已发布版本的优化属于 warn |
| `few_localizations_for_target_market` | 声明的 target market 数 > 已 localize 的 locale 数 | 至少覆盖 top 5 |
| `feature_graphic_low_visual_quality` (Google only) | 主观判断；manual review flag | 设计 review |
| `custom_product_pages_unused` (Apple only) | 有 paid acquisition 但未配置 CPP | 按 channel 定制 CPP |
| `custom_store_listings_unused` (Google only) | 有 paid acquisition / pre-launch 但未配置 custom store listings | 按 use case 定制 |
| `iap_pricing_tier_not_localized` | IAP 价格在所有 locale 一致（未按购买力调整） | 按市场审视价格 tier |
| `release_notes_generic` | "Bug fixes and performance improvements" 类无信息 release notes | 写具体改动以提升更新转化 |
| `tags_unused` (Google only) | Google Play tags 字段空着或 < 3 个 | 用足 5 个 tags |

---

## 9. CLI / Tooling

### 9.1 自动化覆盖范围

| 任务 | 工具 / API | 自动化程度 |
|---|---|---|
| App Store metadata 读取 | App Store Connect API | 部分（多数字段可读）|
| App Store metadata 写入 | App Store Connect API + fastlane deliver | 部分（多数字段可写）|
| Google Play metadata 读取 | Google Play Developer API | 部分 |
| Google Play metadata 写入 | Google Play Developer API + fastlane supply | 部分 |
| Visual asset 上传 | App Store Connect API / Google Play Developer API + fastlane | 高 |
| 字段长度 / 必填 / 格式校验 | 本 skill runner 脚本 | 完全 |
| Privacy policy URL 可达性 | curl / runner 脚本 | 完全 |
| Localization coverage matrix | 解析 fastlane metadata 目录 | 完全 |
| Screenshots 尺寸 / 格式 / 数量 | runner 脚本（用 sharp / ImageMagick） | 完全 |
| Visual quality / 营销力 | **必须人工** | 无 |
| Competitor benchmark | Sensor Tower / data.ai / AppTweak | 工具辅助，需人工解读 |

### 9.2 第三方 ASO 工具（evidence-only，不强制选 specific）

- **Sensor Tower** — keyword research, competitor tracking, market intelligence
- **data.ai** (前 App Annie) — comprehensive store intelligence
- **AppTweak** — ASO + market intel, 性价比较好
- **Mobile Action** — keyword tracker
- **ASOdesk** — keyword research focus
- **Apptopia** — competitive + monetization intel

本 skill **不强制**选某个具体工具，但 evidence 输出应记录使用了哪个工具版本，以保持 audit trail。

### 9.3 CLI 契约

跟 L12 上层契约一致，子命令 `--domain aso`。

> **路径约定（v1.2 harness）**：raw 脚本产物写 tag-scoped `evidence/discoverability/<tag>/raw/`，经 `discoverability-sdk evidence.append <tag> aso <file>` 归一化进 canonical channel evidence `evidence/discoverability/<tag>/aso.json`。gate 评估走 orchestrator 的 `discoverability-sdk gate.check <tag>`（**不是** per-domain gate 命令），产物只有 `<tag>/gate-result.yaml`。**禁止**写 flat `evidence/discoverability/aso/`（无 `<tag>` 维度）。下例用 shell 变量 `TAG` 占位。

```bash
# 跑 ASO 全套 evidence collection（raw 产物落 <tag>/raw/）
pnpm discoverability:audit:aso --config discoverability.config.yaml --out "evidence/discoverability/$TAG/raw"

# 归一化进 canonical channel evidence
python scripts/discoverability-sdk.py evidence.append "$TAG" aso "evidence/discoverability/$TAG/raw/aso-evidence.json"

# 跑 gate 检查（orchestrator 统一 gate.check，写 <tag>/gate-result.yaml）
python scripts/discoverability-sdk.py gate.check "$TAG"

# 解释某条 ASO finding 的修复方法
python scripts/discoverability-sdk.py explain "$TAG" --finding aso-screenshots-missing-locale-zh-hans
```

可选 sub-task：

```bash
# 仅检查 App Store 一侧
pnpm discoverability:audit:aso --platform ios

# 仅检查 Google Play 一侧
pnpm discoverability:audit:aso --platform android

# 仅跑 localization coverage 检查
pnpm discoverability:audit:aso --check localization
```

**注意**：本 skill 不强制具体实现语言。可用 Node.js / Python / Ruby（fastlane 是 Ruby）。Runner 实现细节由项目决定，本 skill 只规定**契约**（输入：config.yaml + metadata 目录 / API token；输出：raw 产物落 `evidence/discoverability/<tag>/raw/`，归一化后落 canonical `evidence/discoverability/<tag>/aso.json`）。

---

## 9.4 quality_gates 字段映射

`discoverability.config.yaml` 的 `quality_gates.aso.*` 字段与本 SKILL 章节的对应关系。runner 拿 config 字段决定 audit 严格度时用此表反查具体 check 的所在节。

| Config 字段 | 对应 SKILL 章节 | Blocker / Warn |
|---|---|---|
| `require_store_listing_metadata` | §4.1 App Store metadata + §5.1 Google Play metadata + §7 `app_store_listing_missing_required_metadata` / `google_play_listing_missing_required_metadata` | blocker |
| `require_privacy_policy_url` | §4.4 + §5.1 + §7 `privacy_policy_missing_for_app_distribution` | blocker |
| `require_localized_assets_for_target_regions` | §4.3 + §5.2 Localization + §8 `screenshots_not_localized` / `few_localizations_for_target_market` | warn |
| `forbid_keyword_stuffing` | §4.1 (Apple 2.3.7) + §5.1 (Google Play Spam) + §6.2 keyword stuffing 严禁 + §12 反模式 #2 / #7 | blocker（违反 Apple Review Guideline 2.3.7 / Google Play Spam policy → listing rejection）|
| `require_screenshots_min_count` | §4.2 App Store visuals + §5.1 Google Play screenshots + §7 `screenshots_min_1_for_iOS_per_device_class` / `screenshots_min_2_for_android_phone` / `screenshots_min_4_for_large_screen_eligibility` | blocker（thresholds: ios_iphone / ios_ipad / android_phone — config 显式数值，runner 按该数值校验）|
| `require_feature_graphic_for_google_play` | §5.1 Google Play metadata (feature graphic 必填) + §7 `feature_graphic_missing` | blocker（Google only）|
| `require_data_safety_form_for_google_play` | §5.1 Google Play metadata (data safety form 必填) + §7 `data_safety_form_incomplete` | blocker（Google only）|

字段名在 `quality_gates.aso.*` 下显式 false 时，对应 check 降级为 info 或跳过；显式 true 或缺省按上表 severity 强制。

---

## 10. Evidence 输出

归一化后的 channel evidence 落 `evidence/discoverability/<tag>/aso.json`（canonical channel key `aso`，由 `discoverability-sdk evidence.append <tag> aso <file>` 写入；其 `findings[]` 聚合 blocker + warn，`source` ∈ {api, fastlane_metadata, manual, third_party_tool}）。下列 raw 脚本产物落同一 tag 的 `raw/` 工作目录，被 `aso.json` 的 `findings[].evidence_path` 反查引用：

```
evidence/discoverability/<tag>/
├── aso.json                         # ← canonical channel evidence（findings[] 聚合 + source，append 产出）
└── raw/                             # raw 脚本产物（pre-append 工作文件）
    ├── app-store-listing.json       # App Store metadata 全量字段 + 长度 + 缺失项
    ├── google-play-listing.json     # Google Play metadata 全量字段 + 长度 + 缺失项
    ├── screenshots-previews.json    # 各 store / device / locale 的截图与视频 inventory + 规格合规
    ├── localization.json            # locale coverage matrix（哪些 locale × 哪些字段已填）
    ├── ratings-reviews.json         # rating 分布 + review reply 率 + 近期 review 摘要
    ├── experiments.json             # Apple PPO / Google Store Listing Experiments 状态
    ├── visual-assets-inventory.json # icon / feature graphic / app preview 详细规格
    ├── compliance-artifacts.json    # privacy URL / App Privacy / data safety 字段存在性（非法律审查）
    └── aso-evidence.json            # raw 聚合中间产物（append 进 aso.json 后即可 GC）
```

> **禁止** flat `evidence/discoverability/aso/`（无 `<tag>`）、顶层 `findings.json` / 自产 `gate-result.json`。channel 聚合统一为 `<tag>/aso.json`；gate 产物只由 `discoverability-sdk gate.check` 写 `<tag>/gate-result.yaml`。

### 10.1 evidence schema 硬规则

继承 L12 上层规则：

- 所有 `*-evidence.json` 必须有 `source` 字段：`api` / `fastlane_metadata` / `manual` / `third_party_tool`
- 所有 finding 必须有 `severity`（`blocker` / `warn` / `info`）
- 所有 finding 必须有 `evidence_path`（具体 JSON path / API endpoint / 文件路径）
- 同一 finding 在 `report.md` 出现时，必须能反向追溯到 `evidence/` 下的原始数据

### 10.2 raw aggregate (`raw/aso-evidence.json`) schema 示例

> 这是 **pre-append 的 raw 聚合中间产物**（落 `<tag>/raw/aso-evidence.json`），喂给 `evidence.append <tag> aso` 后归一化进 canonical `<tag>/aso.json`。`files` 路径都相对 `raw/`。

```json
{
  "schema_version": "1.0",
  "generated_at": "2026-05-25T12:00:00Z",
  "source": "fastlane_metadata + app_store_connect_api",
  "platforms": ["ios", "android"],
  "default_locale": "en-US",
  "localizations_present": ["en-US", "zh-Hans", "ja", "de"],
  "summary": {
    "blockers": 1,
    "warns": 5,
    "infos": 12
  },
  "blockers_present": [
    "screenshots_min_1_for_iOS_per_device_class"
  ],
  "warns_present": [
    "screenshots_not_localized",
    "keyword_field_unused",
    "app_preview_video_missing",
    "ratings_review_response_rate_low",
    "product_page_experiment_not_configured"
  ],
  "files": {
    "app_store_listing": "raw/app-store-listing.json",
    "google_play_listing": "raw/google-play-listing.json",
    "screenshots_previews": "raw/screenshots-previews.json",
    "localization": "raw/localization.json",
    "ratings_reviews": "raw/ratings-reviews.json",
    "experiments": "raw/experiments.json",
    "visual_assets_inventory": "raw/visual-assets-inventory.json",
    "compliance_artifacts": "raw/compliance-artifacts.json"
  }
}
```

---

## 11. 标准 Workflow（5 步）

```
Step 1  读 config + 平台确认
  └─ 读 discoverability.config.yaml 的 aso.platforms（ios / android / both）
     若无配置 → 询问用户；绝不猜测
     → 写 00-activation.json 中 aso 子节

Step 2  收集 metadata（每 store × 每 locale）
  └─ 优先 fastlane metadata 目录解析
     无 fastlane → App Store Connect API / Google Play Developer API
     无 API token → 询问用户 → 标 source: manual
     → 写 app-store-listing.json + google-play-listing.json

Step 3  Visual asset inventory
  └─ 解析 fastlane/metadata/screenshots/ 或 listings/<locale>/graphics/
     校验：尺寸 / 格式 / 透明度 / 数量
     → 写 screenshots-previews.json + visual-assets-inventory.json

Step 4  Localization + ratings/reviews + experiments
  └─ Localization coverage matrix
     Ratings / review reply 率（API 或人工导出）
     PPO / Store Listing Experiment 当前状态
     → 写 localization.json + ratings-reviews.json + experiments.json

Step 5  Gate 评估 + finding 汇总
  └─ 跑第 7 节 Blocker checklist + 第 8 节 Warn checklist
     → 写 raw 聚合 <tag>/raw/aso-evidence.json，再 evidence.append 进 canonical <tag>/aso.json
     → orchestrator 跑 discoverability-sdk gate.check <tag> 聚合到 <tag>/gate-result.yaml（本 skill 不自产 gate-result.json）
```

每一步必须有 evidence 落盘。manual review 部分（visual quality / 文案 quality / competitor benchmark）作为单独 `manual-review.md` artifact 提交。

---

## 12. 常见误区 / 反模式

1. ❌ **把 web SEO 检查直接搬到 ASO**
   - web SEO 看 sitemap / robots / meta tags / structured data；ASO 看 store listing fields / visual assets / store experiments
   - 关键词研究方法不同：web 长尾 vs store 短词、立即转化导向
   - structure 不同：web 有 HTML head + body；store 是 metadata fields + binary asset uploads

2. ❌ **Keyword stuffing 在 app title / subtitle / description**
   - 违反 Apple App Store Review Guideline 2.3.7
   - 违反 Google Play Policy: Spam (Repetitive Content)
   - 严重时直接 listing rejection

3. ❌ **只翻译文字不本地化 visuals**
   - 错失 50%+ 的潜在市场转化
   - 文化适配 > 文字翻译；模特肤色 / 颜色偏好 / UI 习惯都影响

4. ❌ **不开 Product Page Optimization / Store Listing Experiments**
   - 这是 Apple 和 Google **免费提供**的 A/B 工具
   - 不用相当于把"猜"当 ASO 决策依据

5. ❌ **用假评 / pay for reviews**
   - 违反 Apple 和 Google 政策
   - 部分司法管辖区可能违法（如 FTC 规则）
   - App 长期会被算法惩罚 / 下架

5b. ❌ **Review gating（selective review solicitation）**
   - "只主动邀请满意客户留评 / 只把 NPS 高分用户导向 store / 用问卷高分作为 gate" —— 同样禁止
   - 违反 **Apple App Store Review Guideline 1.1.7**（"You can not require users to rate your app, review your app, [...] If your app does include such functionality, you should provide a clear, optional way for users to opt-in."）
   - 违反 **Google Play Developer Policy**（store rating / review 必须对所有用户一视同仁，禁止 conditional solicitation）
   - **FTC 已有 enforcement 案例**：Fashion Nova（2022, $4.2M settlement）、Amazon Echo 评价案（2023, Section 5 settlement）
   - 实操：用官方 SKStoreReviewController（Apple） / Play In-App Review API（Google），对所有用户一视同仁地展示，不做"满意度筛选 gate"

5c. ❌ **Negative feedback deflection**
   - "差评导流到 support，好评才进 store" —— 同样禁止
   - 这是 review gating 的常见伪装形式
   - 同样违反 Apple 1.1.7 + Google Play policy + FTC 规则

6. ❌ **缺 privacy policy URL**
   - 直接 release rejection
   - 这是最常见的"为什么我的 app 被拒"原因之一

7. ❌ **app name 堆关键词**
   - 例："VideoEditor - Video Maker, Photo Editor, Reels Maker, Story Editor, GIF Maker"
   - 触发 Apple 2.3.7；Google Play 也会降权

8. ❌ **把 description 当 SEO meta description 写**
   - Apple 的 description **不参与**搜索索引（与 web 不同）
   - Google 的 full description 参与索引，但 keyword stuffing 仍然有害
   - description 的真正作用是**转化**：feature highlights、social proof、CTA

9. ❌ **混淆 Apple keywords field 和 web SEO meta keywords**
   - Apple keywords field 是 active ranking signal
   - Web SEO meta keywords 几乎所有搜索引擎已忽略

10. ❌ **截图只截 raw UI**
    - 头部 app 几乎都是 "caption screenshot"（叠加营销文案）
    - 纯 raw UI 转化通常不如有 caption 的版本

11. ❌ **release notes 永远写 "Bug fixes and performance improvements"**
    - 浪费一个免费的 reactivation / 更新转化 surface
    - 应该写具体改动 + value proposition

12. ❌ **把 ASO 当一次性任务**
    - ASO 是持续优化（experiments / keyword 调整 / seasonal 推广）
    - 上架后至少季度审视一次

13. ❌ **跳过 competitor benchmark**
    - keyword / screenshot / pricing 都要参照 top 3-5 competitor
    - 闭门造车的 ASO 通常表现差

14. ❌ **混淆 Apple Search Ads (ASA) 和 ASO**
    - ASA 是付费投放（Apple 搜索结果广告位）
    - ASO 是 organic 优化
    - 两者互补但不互替

---

## 13. 权威来源

引用最关键的 1-2 个，作为 audit 时的 ground-truth 参考：

### Apple

- **App Store Connect Help** — metadata field 长度 / 必填项 / 视觉素材规格
  https://developer.apple.com/help/app-store-connect/
- **App Store Review Guidelines** — Section 2.3 (Accurate Metadata)、Section 4 (Design)、Section 5.1 (Privacy)
  https://developer.apple.com/app-store/review/guidelines/
- **App Store Product Page Optimization** — 官方 PPO 文档
  https://developer.apple.com/app-store/product-page-optimization/
- **Apple App Privacy & data collection** — App Privacy "nutrition label" 规范
  https://developer.apple.com/app-store/app-privacy-details/

### Google

- **Play Console Help: Optimize your store listing** — Google 官方 ASO 指南
  https://support.google.com/googleplay/android-developer/answer/4448378
- **Play Console Help: Store Listing Experiments** — 官方 A/B 测试文档
  https://support.google.com/googleplay/android-developer/answer/6227309
- **Google Play Policies** — Spam / Repetitive Content / Metadata Policy
  https://play.google.com/about/developer-content-policy/
- **Data safety section** — Google Play 数据安全表填写指南
  https://support.google.com/googleplay/android-developer/answer/10787469

**审计时**：当 finding 严重程度 = blocker，必须能反向引用到上述某条 official guideline。AI 不能凭"印象"创造 ranking factor。

---

## 14. 何时**不**用本 skill

- **纯 web app / PWA** — 没有 store listing；跳过，走 `web-seo` / `web-aeo`
- **企业内分发 app**（Apple Enterprise / Android Enterprise / MDM only） — 不参与公开 store discovery
- **TestFlight / Google Play Internal Testing 仅限私测** — 没有正式 listing；上线再启用本 skill
- **第三方中国 Android 应用市场治理**（华为 / 小米 / OPPO / VIVO / 应用宝） — 不在本 skill 范围

---

## 15. 与 sibling skill 边界（再强调）

| 你的问题 | 路由到 |
|---|---|
| "我的 app 在 App Store 搜不到" | **app-aso** ✓ |
| "我的 app 在 Google 搜索引擎搜不到" | `web-seo`（app 营销 landing page） |
| "ChatGPT 不引用我的 app 介绍页" | `web-aeo` |
| "我的 app 公司没在 Google Maps 上" | `web-local-seo` |
| "我的 app 截图被 Apple 拒了" | **app-aso** ✓ |
| "我的 app 有 SQL injection 漏洞" | `appsec-security-orchestrator` |
| "我的 SwiftUI 代码不符合 HIG" | `apple-ios-hig`（L5 Platform） |
| "Apple 拒收因为隐私政策 URL 缺失" | **app-aso** ✓ |
| "我要做 keyword 研究" | **app-aso** ✓（用 Sensor Tower 等）|
| "我要做 sitemap.xml" | `web-seo` |

---

## 16. Skill 内部 invariants（自检清单）

本 skill 自身的不变量，每次更新都要保证：

- [ ] 本文档不把 web SEO 检查项作为 **active** ASO check（即不在第 4-10 节作为 blocker / warn / evidence 字段）。第 12 节反模式段引用 sitemap / robots / structured data / meta keywords 等只是**为了划清边界**，说明"这些是 web SEO 的事，不是 ASO 的事"
- [ ] 本文档不引用任何 AI search / llms.txt / AEO 检查项
- [ ] 本文档不引用任何 Local SEO / GBP / NAP 检查项
- [ ] 本文档不包含任何 security / threat model / pentest / OWASP 内容
- [ ] 本文档不写 Swift / Kotlin / Flutter / React Native 代码示例（那是 L5）
- [ ] 所有 blocker / warn 都能反向追溯到 Apple / Google official guideline
- [ ] CLI 契约与 discoverability-orchestrator 一致
- [ ] Evidence 路径是 tag-scoped canonical `evidence/discoverability/<tag>/aso.json`（raw 产物在 `<tag>/raw/` 下）；不写 flat `evidence/discoverability/aso/` / 顶层 `findings.json` / 自产 `gate-result.json`
- [ ] 第三方工具引用仅作 evidence-only，不强制某个供应商

如有违反，标 issue 并修正。

---

## 16.5 L12 Harness Integration (v1.2+)

app-aso 在 L12 harness v1.0 模式下作为 **`aso` channel** 的 auditor。Evidence 通过 `discoverability-sdk.py evidence.append <tag> aso <file>` 写入。

### Channel key

Config (`discoverability.config.yaml`) → `channels.aso`; evidence / SDK / harness canonical (= config 同名) → `aso`; narrow skill (frozen) → `app-aso`; evidence path → `evidence/discoverability/<tag>/aso.json`.

### Script-first 强制

- Deterministic source: App Store Connect API / Google Play Developer API / fastlane metadata parser / Schema.org validator / store-listing JSON validator
- 全 `manual_ai_scan` evidence → `disc-evidence-validator` 标 `hard_rule_violations` → gate.check `decision = BLOCKED`
- 反模式: 让 AI 不读 store API 数据，凭印象给 ASO listing 评分 / 估算 keyword density

### Blocker（永远 blocker — Apple / Google policy 强制）

1. `app_store_listing_missing_required_metadata`（含 Apple keywords field byte-count）
2. `google_play_listing_missing_required_metadata`
3. `privacy_policy_missing_for_app_distribution`
4. `icon_not_meeting_store_specs`
5. `screenshots_min_1_for_iOS_per_device_class`（Apple 下限 1，上限 10）
6. `screenshots_min_2_for_android_phone`（Google publish 门槛）
7. `screenshots_min_4_for_large_screen_eligibility`（tablet / Chromebook）
8. `app_name_or_title_exceeds_character_limit`（Apple keywords field 按 UTF-8 byte 算）
9. `content_rating_or_age_rating_missing`
10. `feature_graphic_missing`（Google）
11. `data_safety_form_incomplete`（Google）
12. `selective_review_solicitation`（review gating — 违反 Apple 1.1.7 + Google Play + FTC）

### Warn-only

`screenshots_not_localized` / `app_preview_video_missing` / `keyword_field_unused`（Apple） / `custom_product_pages_unused`（Apple PPO） / `custom_store_listings_unused`（Google） / `in_app_events_unused`（Apple In-App Events 闲置） / `promotional_content_unused`（Google LiveOps 闲置） / `release_notes_generic`

### Frozen names + 依赖

受保护 (safety surface, 不可改名): skill `app-aso`, channel `aso`, evidence `evidence/discoverability/<tag>/aso.*`. Contract: `~/.claude/templates/discoverability/harness-contract.md` §1 (channel keys) §4.2 (ASO listing required field → blocker).

---

## 16.6 Post-launch ASO measurement（上架后效果测量 — ◇mobile-conditional, measurement-only）

> **加入 2026-06-15（CAPABILITY-UPGRADE L5）。** §4-§13 是**上架前 listing audit**（字段 / 视觉 / 本地化是否合规）；本节是**上架后测量**（真实曝光 / 转化 / 关键词排名）。
>
> **◇ mobile-conditional（与 Q3 / Q5-mobile 同语义）**：本节**只对 app 项目有意义**。非 app 项目（纯 web / PWA / backend）→ 本节**休眠**（dormant），不触发、不产 evidence —— 和 `app-aso` 整个 skill 在 `project_type ∈ {mobile_app, web_app_plus_mobile_app}` 才激活的逻辑一致（orchestrator §4 activation 表）。用户画像里 Mobile 是**备选战场**，本节进库即可，不主推。

### 16.6.0 一句话定位

- **§4-§13（已有）= pre-launch listing audit**：审 listing 形状，产 `aso.json` channel evidence，进 audit gate（§7 blocker / §8 warn）。
- **§16.6（本节）= post-launch measurement**：拉真实商店指标（impressions / conversion / keyword ranking），产 `measurement.json`（measurement-only），**绝不进 gate**。

两条流并行、互不污染。与 L1 post-launch measurement（harness-contract §2.4 `measure.pull` / `measure.compare`）同属上线后只读数据流。

### 16.6.1 pre-launch listing audit vs post-launch measurement（关键区别表）

| 维度 | §4-§13 pre-launch listing audit | §16.6 post-launch measurement |
|---|---|---|
| 问题 | listing 字段 / 视觉 / 本地化合规吗？ | 上架后**实际**曝光 / 转化 / 排名如何？ |
| 输入 | fastlane metadata / 商店 API 读字段 | App Store Connect Analytics API / Play Console + keyword 工具 |
| 工具 | runner 脚本（字段长度 / 尺寸校验） | `facundoolano/aso`（keyword 难度/流量）+ Apple/Google Analytics API |
| 产物 | `aso.json`（channel evidence） | `measurement.json`（measurement-only artifact） |
| 进 gate？ | ✅ §7 blocker / §8 warn | ❌ 否（`gate.check` 完全忽略） |
| 何时跑 | 上架前（release gate） | 上架后（持续监测 / 优化前后对比） |
| 非 app 项目 | skill 整体 disabled | 本节同样 dormant |

> **铁律**：本节产物 **measurement-only**，**不**触发 `state.json.gate_status`、**不**进 `gate-result.yaml`、**不**作为 release verdict。Apple / Google 都不公开 store search ranking 算法 —— keyword ranking / conversion 是观测值，不是"ASO 官方分数"。这与 §3.1 反规则"把 AI 生成的 keyword 列表当 App Store 官方 ranking factor"同源。

### 16.6.2 Script-first 红线（AI 永不编造商店指标）

继承 §3 执行宪法 + harness §8.2：

1. **每个指标必须来自一次真实 API 调用**（App Store Connect Analytics Reports API / Google Play Console / `facundoolano/aso`）。AI（本模型）**绝不**凭印象写"你的转化率大概 X%" / "这个词难度大概 Y"。
2. **无凭证 → `status: skipped`**，绝不编造。由 L1 的 `disc-measurement-puller` agent 拉取（`measure.pull --provider aso`，provider 已在 SDK `MEASUREMENT_PROVIDERS` 中，`PROVIDER_CHANNEL["aso"]="aso"`）。无 App Store Connect API key / Play 凭证时记 skipped。
3. **BYO creds 从环境变量取**（App Store Connect API key 用 `.p8` + key-id + issuer-id；Google Play service account JSON），**绝不**提交进仓库 / `.env` / chat / report。
4. AI 的角色只在**最后一步**：解读 `measurement.json` 里的真实漏斗 / 排名，关联到 §4-§6 哪些 listing 改动可能起效（如 conversion 低 → §6.3 screenshots / §4.2 首屏；keyword 掉排名 → §4.1 keywords field / §6.1 关键词研究）—— 不产生任何指标本身。

> **本 skill 读权限边界不变**：`app-aso` frontmatter 是 `allowed-tools: Read, Grep, Glob`（无 Bash / Write，`forbidden-tools: WebFetch`）。本节的 API 拉取**不由本 skill 自己跑**，而是 RETURN 给 L1 的 `disc-measurement-puller` agent（有 Bash）执行 `measure.pull`，本 skill 只**解读**归一化后的 `measurement.json` —— 与 §11 Workflow"无 API token → 询问用户 → 标 source: manual"的既有读权限模型一致。

### 16.6.3 工具：facundoolano/aso（keyword 难度/流量，双店）

> **参考 / 可吸收**：`facundoolano/aso`（MIT, npm）。双店（App Store + Google Play）keyword **难度分 + 流量分**估算，纯 CLI / Node API。

| 能力 | 说明 | 命中本 skill 章节 |
|---|---|---|
| keyword **difficulty** score | 估算某关键词竞争难度（基于 title 命中 / rating / installs 等公开信号） | §6.1 关键词研究（优先指标 difficulty）|
| keyword **traffic** score | 估算某关键词流量潜力 | §6.1（优先指标 search volume）|
| **suggest** keywords | 从 seed app / competitor 反查关键词候选 | §6.1 competitor benchmark |
| app / similar / reviews scrape | 拉 listing 公开数据 + competitor | §6.1（competitor coverage）|

```bash
# 由 disc-measurement-puller agent 跑（本 skill 不直接执行 Bash）；npm i aso
# keyword 难度 + 流量（双店），JSON 出到 raw/，供 measure.pull 归一化
node -e "const aso=require('aso')('itunes'); aso.scores('video editor').then(s=>console.log(JSON.stringify(s)))" \
  > "evidence/discoverability/$TAG/raw/aso-keyword-scores-ios.json"
node -e "const aso=require('aso')('gplay'); aso.scores('video editor').then(s=>console.log(JSON.stringify(s)))" \
  > "evidence/discoverability/$TAG/raw/aso-keyword-scores-android.json"
```

> **难度/流量是 estimate，标 internal/third-party heuristic**：`facundoolano/aso` 的分数是基于公开信号的**估算**，不是 Apple / Google 官方数字。evidence 里标 `source: third_party_tool`（§10.1 既有 source enum），不冒充官方 ranking。与 §9.2 第三方工具（Sensor Tower 等）evidence-only 同等对待。

> **live scrape 对环境/地区敏感，可能无声失败**：`facundoolano/aso`（及其底层 `app-store-scraper`）靠抓 App Store / Play 的公开响应，在**受限网络 / 部分地区 / 缺特定 header** 的环境下可能**静默抛 `undefined`**（无 message / stack）——即使包装好、`itunes.apple.com/search` 返 HTTP 200，`aso.scores()` / `store.search()` 仍可能解析失败。这是第三方库脆性，**不是 bug**。**失败即按 §16.6.2 记 `status: skipped`，绝不退化为 AI 估算的难度/流量数字**（§16.6.6 反模式）。高可靠场景**优先官方 Analytics API**（§16.6.4，真实漏斗 + 免费）而非依赖 scrape 估算。E2E 实测：包真装成功、方法齐全，但 live `scores()` 抛 undefined → measure.pull 正确落 `skipped`，护栏有效。

### 16.6.4 工具：官方 Analytics API（真实漏斗，免费）

| 平台 | API | 真实指标 | 凭证 |
|---|---|---|---|
| **Apple** | **App Store Connect Analytics Reports API**（免费） | **impression → product page view → tap (下载)** 漏斗 + 来源（search / browse / referral）+ conversion rate | App Store Connect API key（`.p8` + key-id + issuer-id，env）|
| **Google** | **Google Play Developer Reporting API** / Play Console | store listing acquisition（impressions / store listing visitors / installers）+ conversion + keyword（部分）| service account JSON（env）|

```bash
# 由 disc-measurement-puller agent 拉取（App Store Connect Analytics Reports API）
# 真实漏斗：impressions / product_page_views / conversion_rate（绝不编造，无 key → skipped）
# 归一化进 measurement.json（measurement-only）
python ~/.claude/skills/discoverability-orchestrator/scripts/discoverability-sdk.py \
  --project-root . measure.pull "$TAG" --provider aso \
  "evidence/discoverability/$TAG/raw/asc-analytics-funnel.json"

# 优化前后对比（真实曝光/转化/排名 delta，纯算术）
python ~/.claude/skills/discoverability-orchestrator/scripts/discoverability-sdk.py \
  --project-root . measure.compare "$TAG" --baseline-tag "$BASELINE_TAG"
```

> **App Store Connect Analytics Reports API 是漏斗的真相源**：impression（在搜索/榜单被看到）→ product page view（点进 listing）→ tap/download（转化）。conversion 低在哪一段，直接指向 listing 优化重点（impression→view 低 = §4.2 icon/首屏；view→download 低 = §6.3 screenshots / §4.1 description 转化要素）。

### 16.6.5 measurement 指标 → listing 优化映射（AI 解读用）

| 真实指标（measurement.json） | 信号 | 回到哪个 listing 章节优化 |
|---|---|---|
| keyword ranking 掉 / 难度高于流量 | 关键词竞争失利 | §4.1 keywords field / §6.1 关键词研究 + competitor |
| impressions 低 | 在搜索/榜单曝光不足 | §4.1 app name/subtitle 权重词 / §4.4 category |
| impression → page view 转化低 | icon / 首屏没吸引点击 | §4.2 icon / §6.4 feature graphic（above-the-fold）|
| page view → download 转化低 | listing 内容没说服下载 | §6.3 screenshots（caption）/ §4.1 description 转化要素 / §4.2 preview video |
| 某 locale 转化显著低 | 本地化不到位 | §4.3 / §6.6 localized creatives（不只翻译）|

> AI 只做这层**解读 + 路由**，指标本身 100% 来自 API。**绝不**反过来用 listing 形状去"推算"应该有多少曝光/转化。

### 16.6.6 measurement-only 边界（与 §7 audit gate 不重叠）

| 流 | 产物 | 进 gate？ | owner |
|---|---|---|---|
| pre-launch listing audit（§4-§13） | `aso.json` channel evidence | ✅ §7 blocker / §8 warn | app-aso（本 skill）|
| post-launch measurement（§16.6） | `measurement.json`（`measurement_only: true`）| ❌ 完全忽略 | app-aso（本 skill）+ L1 measure.pull |

**反模式**：
- ❌ 把 keyword ranking / conversion rate 写进 release gate（观测值，store 算法未公开，永不 blocker）
- ❌ 无凭证时让 AI 编一个曝光/转化数字（必须 `status: skipped`）
- ❌ 把 `facundoolano/aso` 的 estimate 难度分冒充 Apple / Google 官方数字
- ❌ 把 measurement 产物写进 `aso.json` 污染 pre-launch channel evidence
- ❌ 在非 app 项目上跑本节（dormant —— 与 skill 整体 activation 一致）

### 16.6.7 SDK 依赖说明（已落地 —— 2026-06-27 sync）

L1 已落地 `measure.pull` / `measure.compare`。`aso` provider **已在** SDK 的 `MEASUREMENT_PROVIDERS`（现为 `("gsc","ga4","bing","aso","aeo","gbp")`）+ `PROVIDER_CHANNEL["aso"]="aso"`。L5 的 Apple/Google Analytics 漏斗归一化**直接复用**，**无需新增 SDK provider**。

ASO 漏斗特有指标键**已在** `MEASURE_METRICS`（2026-06-15 补齐）：`product_page_views` / `conversion_rate` / `keyword_rank` —— 因此 `measure.compare` 能自动 delta 这些。`facundoolano/aso` + Analytics API 的 JSON 经 `measure.pull --provider aso` 归一化即可。

---

## 17. 版本历史

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-05-25 | Initial release; L12 Discoverability narrow skill #4 of 4 |
| 1.1.0 | 2026-06-15 | CAPABILITY-UPGRADE L5: §16.6 post-launch ASO measurement (◇mobile-conditional, measurement-only — `facundoolano/aso` keyword 难度/流量 + App Store Connect Analytics Reports API 漏斗; 复用 L1 measure.pull --provider aso; 绝不进 gate) |
