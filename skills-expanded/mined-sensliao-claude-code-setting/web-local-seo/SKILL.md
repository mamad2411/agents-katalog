---
name: web-local-seo
canonical_id: discoverability.web-local-seo
aliases: [web-local-seo, local-seo, geographic-seo]
version: 1.1.0
status: stable
created_date: 2026-05-25
parent: discoverability-orchestrator
layer: L12
sibling-skills:
  - web-seo          # 标准 web SEO（不重叠）
  - web-aeo          # AI search / Generative Engine Optimization（不重叠）
  - app-aso          # App Store / Google Play（不重叠）
children: []
upstream:
  - discoverability-orchestrator
downstream: []
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion
forbidden-tools: []
disable-model-invocation: false
description: >-
  Local SEO - Google Business Profile review, NAP consistency across platforms, LocalBusiness JSON-LD, service-area landing pages, reviews/hours/photos upkeep, Apple Maps and Bing Places presence. Only for businesses with a real physical touchpoint (storefront, office, studio) or a service area; pure online, SaaS or globally distributed products go to `web-seo` + `web-aeo`.
---

# web-local-seo — Local SEO 子层（L12）

## 0. 命名说明 + 适用边界

> **命名说明**：本 skill 在 2026-05-25 前曾名为 `web-geo`，但 "GEO" 在业界 2025-2026
> 已 100% 等同 Generative Engine Optimization（AI search 优化）。为避免歧义，本 skill
> 已改名 `web-local-seo`。Generative Engine Optimization 一律归 `web-aeo`。
> Local SEO（本 skill 覆盖）= 有真实线下接触点（店面 / 办公室 / 工作室）或上门服务区域的业务。

### 0.1 L12 子层分工

| Skill | 负责领域 |
|---|---|
| `web-seo` | 标准搜索引擎（Google / Bing）SEO |
| `web-aeo` | AI search / answer engines（ChatGPT / Perplexity / Gemini / Claude / SGE / AI Overviews / Generative Engine Optimization） |
| **`web-local-seo`（本 skill）** | Local SEO（Google Business Profile / Google Maps / NAP / Apple Maps / Bing Places） |
| `app-aso` | App Store / Google Play 应用商店优化 |

### 0.2 严格边界（什么不在本 skill 范围）

| 主题 | 归属 |
|---|---|
| 标准 SEO（meta / sitemap / canonical / Core Web Vitals / structured data 通用部分） | `web-seo` |
| AI search optimization / generative engines / answer engines / llms.txt / AI Overviews / SGE / Generative Engine Optimization | `web-aeo` |
| App Store / Google Play 优化 | `app-aso` |
| 任何 security / AppSec / threat model / pentest | `appsec-security-orchestrator`（**本 skill 绝不写 security 内容**）|
| Crawler / robots / 爬虫策略的通用部分 | `web-seo` |
| Schema.org 中非 LocalBusiness 的部分（Article / Product / FAQ 等） | `web-seo` |

**铁律**：本 skill 只处理"业务有真实线下接触点或服务区域"这一类场景。其余一律 handoff。

### 0.3 适用 vs 不适用

| 类别 | 是否适用 web-local-seo |
|---|---|
| 餐厅 / 咖啡店 / 实体零售 / 美容美发 / 健身房 | 适用 |
| 诊所 / 牙医 / 兽医 / 律所 / 会计事务所 | 适用 |
| 4S 店 / 修车铺 / 加油站 / 维修门店 | 适用 |
| 上门服务（水管工 / 电工 / 家政 / 搬家 / 园艺） | 适用（service area business）|
| 教培机构（线下校区） | 适用 |
| 酒店 / 民宿 / 旅游景点 | 适用 |
| 多分店连锁（每家分店独立 listing） | 适用 |
| 纯 online business / 纯电商无线下接触 | **不适用** |
| pure SaaS / 全球分发软件 | **不适用** |
| Headless / API 服务 | **不适用** |
| 仅有虚拟办公室 / P.O. box 的业务 | **不适用**（且本 skill 拒绝帮其申请 GBP，见 §4） |

---

## 1. Mission

- 让有真实线下接触点 / 服务区域的业务，在 **Google 本地 SERP + Google Maps + Apple Maps + Bing Places** 上被找到、被信任、被选择
- 强制 **NAP（Name / Address / Phone）一致性**，跨 site / GBP / schema / 第三方目录
- 强制 **LocalBusiness JSON-LD** 与 GBP 实际信息对齐
- 拦截 **Google Business Profile policy 违规**（虚假地址 / 虚拟办公室 / 重复 profile / 不合规业务）—— 这些会导致 listing 被永久 suspend
- 为本地 landing page 提供差异化内容门（拒绝 boilerplate doorway page）

---

## 2. 目标链路

```
真实业务资格（eligibility）
    ↓
Business Profile 创建 / 认领（GBP claim / verify）
    ↓
NAP 一致性（site / GBP / schema / 第三方目录）
    ↓
LocalBusiness JSON-LD（最具体 subtype，与 GBP 对齐）
    ↓
地域 landing page（每 service area 独立 URL + 差异化内容）
    ↓
持续维护（reviews 回复 / hours / photos / posts / Q&A）
    ↓
本地 SERP 排名 + Google Maps presence + 多 maps（Apple / Bing）扩展
```

任一环节断裂 → 本地排名 cap 或被 Google 直接降权。

---

## 3. 执行宪法（继承 L12）

L12 的执行宪法是 **Script-first / Audit-only**。Local SEO 有一个特殊点：**大量动作必须由业主在 Google Business Profile 控制台手动完成**（登录 GBP / 上传认证文档 / 接听验证电话 / 回复 reviews）。

**本 skill 因此采取双轨制**：

| 动作类型 | 是否可自动 |
|---|---|
| 站内 LocalBusiness JSON-LD 注入与校验 | 自动（CLI） |
| 站内 NAP 字符串 audit（site / footer / contact / landing page） | 自动（CLI） |
| 第三方目录 NAP 一致性比对（Yelp / TripAdvisor / Apple Maps / Bing Places / 行业目录） | 半自动（部分需 API key，部分需人工 audit）|
| GBP completeness 检查（categories / hours / photos / services / posts） | 半自动（需 GBP API 或人工 audit）|
| GBP 创建 / 认领 / 验证流程 | **完全人工**（必须业主登录 Google 账号，本 skill 仅产 checklist） |
| Reviews 回复 / 收集 | **完全人工 + 流程指导**（本 skill 不替业主写回复）|
| Photos / posts / Q&A 维护 | **完全人工** |

**铁律**：本 skill 产出的 evidence 文件必须**明确标记**哪些是 auto / 哪些是 manual / 哪些 pending（用 `audit_mode: auto | manual | pending`）。

### 3.1 L12 5 级 priority ladder（本 skill 适用）

按 L12 父层约定，evidence 来源按以下优先级排序。注意 Local SEO 与 web-aeo 的关键差异：GBP API 自动化覆盖率低，大量字段必须由业主在 GBP 控制台 / Apple Business Connect / Bing Places 手动操作。

| Level | 类型 | web-local-seo 中的体现 | auto/manual |
|---|---|---|---|
| 1 | Deterministic script / API / CLI | 站内 LocalBusiness JSON-LD parser、`pnpm discoverability:audit:geo` NAP grep、word-count / boilerplate ratio CLI | 全自动 |
| 2 | Framework adapter | Next.js / Nuxt 等的 LocalBusiness schema 注入器、CMS 端 NAP 来源契约 | 全自动 |
| 3 | Structured evidence parser | normalize JSON-LD / NAP / service-area-pages 输出成本 skill 定义的 schema | 全自动 |
| 4 | AI synthesis from evidence | AI 读 normalized JSON，分类 blocker vs warn（doorway page / NAP conflict / schema mismatch） | 全自动 |
| 5 | Manual AI scan only when no script / adapter | GBP completeness（无 API key 时）、第三方目录 NAP（无开放 API）、Apple Maps / Bing Places audit、reviews 回复质量、photos 真实性、业主回复时效 — **大量 Local SEO check 落在这一级** | **lower confidence**，evidence 必须标 `audit_mode: manual` + `source: manual_ai_scan` |

**与 web-aeo 的差异**：web-aeo 中 Level 1-4 覆盖绝大多数 check；web-local-seo 中 Level 5 manual audit 占比显著更高（见 §13.3 自动化覆盖率边界），因此 `audit_mode` 字段是必填，**不能假装人工部分已 audit**。

---

## 4. Business Profile Eligibility 检查（关键章节）

在帮助任何业务创建或认领 GBP 之前，本 skill **必须**先做 eligibility 检查。如果业务不合规，**拒绝继续**。

### 4.1 合规情况（OK to proceed）

| 业务类型 | 合规要求 |
|---|---|
| Brick-and-mortar（实体店）| 有公开可访问的客户接触点：店面 / 办公室 / 工作室，营业时间内允许客户上门 |
| Service area business（SAB，上门服务）| 业务在客户位置提供服务（如水管工 / 上门修车 / 家政），可隐藏实际办公地址 |
| Hybrid（既有门店又上门）| 同时满足以上两者 |

> **澄清（SAB ≠ P.O. box / 虚拟办公室）**：SAB（service area business）允许在 GBP 中**隐藏 displayed address**（用 `service_area` 字段代替）。**但 hidden 字段也不接受 P.O. box / 虚拟办公室** —— 业务必须有真实的运营地址（可能是住家），只是不对外公开。用 P.O. box 仍然违反 Google policy，触发 §4.2 中的 `fake_or_virtual_location_used_as_physical_location` BLOCKER。

### 4.2 不合规 / 灰色情况（DO NOT proceed —— 直接 BLOCKER）

| 不合规场景 | 违反什么 | 后果 |
|---|---|---|
| 纯 online business，无任何线下接触 | Google Business Profile guidelines | listing 被 suspend |
| P.O. box / 邮政信箱作为 physical address | Guidelines（physical address required）| 永久 suspend |
| 虚拟办公室（regus / wework hotdesk） 作为唯一地址 | Guidelines（must be staffed during stated hours）| 永久 suspend |
| 共享办公空间但无独立招牌 / 无独立接待 | 同上 | 永久 suspend |
| 业务地址实际是住家但不接受客户上门（且不是 SAB） | Guidelines（must be staffed or hidden as SAB） | 永久 suspend |
| 重复 profile（同一业务多个 listing） | Guidelines（one listing per business per location） | 永久 suspend |
| 代理商替不存在的业务批量申请 | Guidelines + Terms of Service | 账号封禁 |
| 用关键词堆砌 business name（如"北京最好的牙科诊所 - 牙博士"） | Guidelines（must match real-world name）| name 被强制改回 + 降权 |
| 业务实际不在 listed 地址运营（pin 漂移到流量好的区域） | Guidelines（must be actual location） | 永久 suspend |

### 4.3 处理流程

```
Step 1 — 询问业务类型 / 地址性质 / 接触模式
Step 2 — 比对 §4.1 / §4.2 矩阵
Step 3 — 若 §4.2 任一命中 → BLOCKER：business_profile_requested_but_business_not_eligible
         本 skill 拒绝继续 GBP 相关操作，并向用户说明：
         "此业务在 Google Business Profile guidelines 下不合规，强行申请将导致
          listing 被永久 suspend，且关联 Google 账号可能被封禁。"
Step 4 — 若 §4.1 命中 → 继续 §5 completeness 检查
```

### 4.4 灰色边缘情形（需 ASK 用户）

| 情形 | 询问要点 |
|---|---|
| 业务在共享办公但有独立 signage + 独立接待 | 是否有独立招牌？营业时间是否有人接待客户？是否能接受客户上门？|
| 业务地址是住家，但是 SAB（隐藏地址）| 是否在客户所在地提供服务？是否在 GBP 设置中隐藏地址 + 指定 service area？|
| 业务有多个分店 | 每个分店是否独立 staffed？是否每个分店有独立 listing？|

权威来源：[Google Business Profile guidelines](https://support.google.com/business/answer/3038177)

---

## 5. Business Profile Completeness 检查

通过 §4 eligibility 后，audit GBP 完整度：

| 字段 | 检查点 | 缺失 severity |
|---|---|---|
| **name** | 与法律名称 / 现场招牌一致；不堆关键词 / 不加城市名（除非招牌就是这样）| HIGH（违规可能被强制改）|
| **primary category** | 必填，最具体的一个 | CRITICAL |
| **secondary categories** | 1-9 个，描述业务其他真实服务 | MEDIUM |
| **address** | physical address 或 service area（SAB）| CRITICAL |
| **service area**（SAB）| 列出实际提供服务的城市 / 邮编 / 半径 | HIGH（SAB 必填） |
| **phone** | local number 优先于 800 / 全国号 | MEDIUM |
| **website** | 完整 URL（含 https）| HIGH |
| **hours** | 含 special hours / holiday hours / 临时关闭 | MEDIUM |
| **photos** | exterior（外观）/ interior（内部）/ team（团队）/ products / services | MEDIUM |
| **products / services** | 列具体 service items 或 product catalog | MEDIUM |
| **attributes** | 如 "wheelchair accessible" / "outdoor seating" / "wifi" 等 | LOW |
| **Q&A** | 业主或员工答常见 Q（不能让用户互相回答错误信息）| MEDIUM |
| **posts** | 周期性 post（promo / event / update）| LOW（但有助于活跃度） |
| **reviews** | 数量 + 平均分 + **业主回复率** | HIGH（回复率低伤排名）|
| **messaging** | 是否启用 chat | LOW |
| **booking link** | 餐厅 / 诊所 / 美容等若有预订系统应链上 | LOW |

### 5.1 Photos 建议

| 类型 | 建议数量 | 说明 |
|---|---|---|
| Exterior | 3-5 张 | 不同角度，含招牌 |
| Interior | 3-5 张 | 用餐区 / 接待区 / 工作区 |
| Team | 2-3 张 | 真实员工，不要用 stock photo |
| Products / Services | 5-10 张 | 主打 SKU / 服务实景 |
| Logo + cover photo | 各 1 张 | 高分辨率 |

**反模式**：纯 stock photo / 网图 / 渲染图作为主要 photos —— Google 可能识别为不真实并降权。

### 5.2 Reviews 关键指标

| 指标 | 目标 |
|---|---|
| 数量 | 至少 ≥ 10（行业 baseline，不同行业差异大） |
| 平均分 | ≥ 4.0（< 3.5 严重影响 CTR） |
| 业主回复率 | ≥ 50%（理想 ≥ 80%），尤其是 negative review 必回 |
| 回复时效 | 平均 ≤ 7 天 |
| 假评比例 | 0%（不买 / 不刷 / 不亲友互评，见 §9）|

---

## 6. NAP Consistency（Name / Address / Phone 跨平台一致性）

NAP 是 Local SEO 的基石。Google 通过跨平台对比来判断业务真实性。任何不一致都会降低 trust signal。

### 6.1 必须一致的位置

| 位置 | 工具 | 必查 |
|---|---|---|
| Site footer | `Grep` site 源码 | 必 |
| Contact page | `Grep` / `Read` | 必 |
| 每个 service area landing page | `Grep` | 必 |
| Schema.org LocalBusiness JSON-LD | 见 §7 | 必 |
| Google Business Profile | GBP 控制台 / API | 必 |
| Apple Maps Connect | maps.apple.com/business | 必 |
| Bing Places for Business | bingplaces.com | 必 |
| Yelp | yelp.com/biz | 行业相关时必 |
| TripAdvisor | tripadvisor.com | 餐饮 / 旅游业必 |
| Facebook Page | facebook.com/businesses | 行业相关时必 |
| 行业目录（医生 → Healthgrades / 律师 → Avvo / 餐厅 → OpenTable）| 各 directory | 行业相关时必 |

### 6.2 NAP 字符串规则

| 字段 | 一致性规则 |
|---|---|
| Name | 完全相同（大小写 / 标点 / 空格 / & vs and 都要统一） |
| Address | 国家邮政规范格式；street type 缩写要统一（"St" vs "Street" 不混用）|
| Phone | E.164 格式（+86 ...）或本地标准格式；区号 / 分隔符要统一 |

### 6.3 自动 audit 策略

```bash
# 提取 site 上所有 NAP candidates
pnpm discoverability:audit:geo --check nap --config discoverability.config.yaml

# 输出比对表：site 上的所有出现 vs GBP canonical NAP
```

CLI 比对结果分三类：
- **exact_match** — 完全一致
- **format_drift** — 同一信息但格式不同（如 "Street" vs "St" / "+86-10-..." vs "010-..."）
- **conflict** — 信息冲突（不同 phone / 不同 address）→ HIGH

第三方目录的 NAP audit 因为多数无公开 API，**建议使用 listing management 服务**（如 Yext / Moz Local / BrightLocal / Whitespark），本 skill 不强制 specific tool，但 evidence 必须记录"已 audit 哪些 directories / 哪些未 audit"。

---

## 7. LocalBusiness Schema（JSON-LD 模板）

### 7.1 完整模板（餐厅示例）

```json
{
  "@context": "https://schema.org",
  "@type": "Restaurant",
  "@id": "https://example.com/#restaurant",
  "name": "Example Bistro",
  "image": [
    "https://example.com/photos/exterior.jpg",
    "https://example.com/photos/interior.jpg",
    "https://example.com/photos/food.jpg"
  ],
  "logo": "https://example.com/logo.png",
  "url": "https://example.com",
  "telephone": "+86-10-12345678",
  "priceRange": "$$",
  "servesCuisine": ["Italian", "Mediterranean"],
  "menu": "https://example.com/menu",
  "acceptsReservations": "True",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "12 Example Street",
    "addressLocality": "Beijing",
    "addressRegion": "Beijing",
    "postalCode": "100000",
    "addressCountry": "CN"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 39.9042,
    "longitude": 116.4074
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "11:00",
      "closes": "22:00"
    },
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Saturday", "Sunday"],
      "opens": "10:00",
      "closes": "23:00"
    }
  ],
  "sameAs": [
    "https://www.google.com/maps?cid=12345678901234567890",
    "https://www.yelp.com/biz/example-bistro",
    "https://www.tripadvisor.com/Restaurant_Review-xxxxx",
    "https://www.facebook.com/examplebistro"
  ]
}
```

### 7.2 @type 选最具体的 subtype

**反模式**：所有业务都用通用 `LocalBusiness`。

**正确做法**：从 schema.org LocalBusiness 树挑最具体的 subtype。

| 业务 | @type |
|---|---|
| 餐厅 | `Restaurant`（细分：`FastFoodRestaurant` / `CafeOrCoffeeShop` / `BarOrPub`）|
| 牙医 | `Dentist` |
| 律所 | `LegalService` / `Attorney` |
| 水管工 | `Plumber` |
| 电工 | `Electrician` |
| 美容美发 | `BeautySalon` / `HairSalon` |
| 健身房 | `ExerciseGym` / `SportsActivityLocation` |
| 兽医 | `VeterinaryCare` |
| 4S 店 | `AutoDealer` / `AutoRepair` |
| 酒店 | `Hotel` / `LodgingBusiness` |
| 加油站 | `GasStation` |
| 药店 | `Pharmacy` |

完整列表：[schema.org/LocalBusiness](https://schema.org/LocalBusiness)

### 7.3 SAB（service area business）模板差异

```json
{
  "@context": "https://schema.org",
  "@type": "Plumber",
  "name": "Example Plumbing",
  "telephone": "+86-10-12345678",
  "url": "https://example.com",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Beijing",
    "addressRegion": "Beijing",
    "addressCountry": "CN"
  },
  "areaServed": [
    {"@type": "City", "name": "Beijing"},
    {"@type": "AdministrativeArea", "name": "Hebei"}
  ],
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Plumbing Services",
    "itemListElement": [
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Emergency Plumbing"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Drain Cleaning"}}
    ]
  }
}
```

SAB 模板规则：
- `address` 可以只包含 city / region / country，不公开 streetAddress
- `areaServed` 必填，列出实际服务的 City / State / AdministrativeArea
- `geo` 可选（无 streetAddress 时通常省略）
- `priceRange` 可选

### 7.4 多分店（multi-location）

每个分店一个独立 JSON-LD block，放在对应分店的 landing page，不要堆在一个 page 里。或者用 `branchOf` 关联到 parent organization：

```json
{
  "@type": "Restaurant",
  "@id": "https://example.com/locations/beijing#restaurant",
  "name": "Example Bistro — Beijing",
  "branchOf": {
    "@type": "Organization",
    "@id": "https://example.com/#org",
    "name": "Example Bistro Group"
  }
}
```

### 7.5 一致性校验

CLI 应做的校验：

| 校验 | 失败 severity |
|---|---|
| `@type` 不是通用 `LocalBusiness`（已选 subtype） | warn-only |
| `name` / `telephone` / `address` 与 GBP 一致 | BLOCKER（localbusiness_schema_claims_unverified_location）|
| `openingHoursSpecification` 与 GBP hours 一致 | warn-only |
| `sameAs` 含 GBP 链接 | warn-only |
| `image` URL 全部可访问 200 | warn-only |
| `geo.latitude` / `geo.longitude` 与 address 大致匹配 | warn-only（detect pin 漂移）|

---

## 8. Service Area Pages（地域 landing page）

### 8.1 必守规则

1. **每个 service area 独立 URL**
   - 正：`/services/plumbing/beijing` / `/services/plumbing/tianjin` / `/services/plumbing/shijiazhuang`
   - 反：`/services/plumbing?city=beijing` （query string）/ 全部塞在一页

2. **内容差异化（不要 boilerplate copy 只换城市名）**
   - 反模式：模板化的 "We provide plumbing in {city}. Best plumber in {city}. Call us today!" —— Google 视为 **doorway page**，整批降权或 deindex
   - 正确：真实本地内容
     - 本地团队 / 该 city 服务的具体技师介绍
     - 该 city 的真实客户案例 / 评价
     - 该 city 的本地知识（当地常见问题 / 当地法规 / 当地标志性地点）
     - 该 city 的服务覆盖范围细节（邮编 / 区县 / 半径）
     - 与 city 相关的实际照片

3. **真实服务区域才创建 page**
   - 反模式：为业务实际不服务的 city / region 创建 page（"plumber in Shanghai" 但只在 Beijing 营业）→ doorway page + 用户体验事故
   - 正确：只为 GBP 中 areaServed 列出的地区创建 page

4. **每个 service area page 含本地化 LocalBusiness JSON-LD**
   - 多分店：每 page 的 `branchOf` 指向 organization，自己用对应分店的 NAP
   - SAB：每 page 的 `areaServed` 收窄到该 city

5. **clear hierarchy**
   - `/services` —— 总览
   - `/services/plumbing` —— 服务类型 hub
   - `/services/plumbing/beijing` —— 服务 × 城市 leaf
   - 内部链接：leaf 指向 hub，hub 列所有 city leaf

### 8.2 内容门（content gate）

| 检查 | 阈值 | 失败 severity |
|---|---|---|
| Unique word count per page | ≥ 400 words 真实独特内容 | HIGH（thin content）|
| Boilerplate ratio | ≥ 70% 内容与其他 service area page 不同 | HIGH（doorway page）|
| 本地化信号（city / region / postal code / 当地地标 / 当地评价）| 至少 3 类 | MEDIUM |
| 内部图片 alt 含 city / location reference | 至少 1 张 | LOW |
| H1 / title / meta description 含 city + service | 必须 | HIGH |

---

## 9. Reviews Management

### 9.1 主动收集（合规方式）

| 合规策略 | 说明 |
|---|---|
| 服务完成后短信 / email follow-up 邀请评价 | 发送给**所有**最近客户，不能只选满意客户 |
| QR code / 名片 / 收据上印 GBP 评价链接 | 公开普适邀请 |
| 员工口头提醒"如果觉得满意，请留个 Google 评价" | OK |

### 9.2 不合规（review gating —— 严禁）

| 不合规行为 | 违反什么 | 后果 |
|---|---|---|
| 只邀请预判为满意的客户留评（review gating）| Google + FTC | review filter + 处罚 |
| 内部预筛：先问"你满意吗"，满意才给 Google 链接，不满意走内部 | Google policy（明确禁止）| reviews 被批量清除 |
| 买评 / 刷评 / 评价交换 / 亲友互评 | Google policy + FTC | listing suspend |
| 用礼品 / 折扣换评（offering incentive for review）| Google policy + FTC | reviews 被清除 |
| 业主自己注册马甲账号留 5 星 | Google policy | listing suspend |

### 9.3 业主回复（必须做）

| 评价类型 | 回复要点 |
|---|---|
| 5 星 | 简短致谢，提到具体服务 / 产品（不要全部"thank you"模板） |
| 4 星 | 致谢 + 询问"哪里可以做得更好" |
| 3 星及以下（negative） | **必回**，礼貌、事实化、对外，**不在 public reply 中暴露任何 PII**；提供 offline 解决联系方式；不在公开回复里争论 |
| 假评 / 恶意评 | 业主回复说明"无此交易记录"，然后通过 GBP "report review" 申诉 |

**反模式**：
- 用 ChatGPT 模板回复所有 review（被识别为不真实）
- 在 negative review 下回复争吵 / 嘲讽客户
- 在 negative review 下暴露客户 PII（姓名 / 订单号 / 病历号等）

### 9.4 Negative review PII 红线（边界声明）

**原则**：public reply 中**绝不能**出现客户的 PII（姓名 / 联系方式 / 地址 / 订单号 / 病历号 / 案件号 / 医疗 / 财务 / 个人信息）。对外用泛指（"this customer" / "the transaction in question"），具体内容通过 offline channel 处理。

本 skill 只负责"识别 public reply 是否触线"。任何具体的 PII 处理流程（redaction policy / data retention / 跨境合规 / PIPL / GDPR / HIPAA workflow）→ handoff 到 AppSec / compliance team（`appsec-security-orchestrator`）。

---

## 10. Maps Presence（多 Maps 覆盖）

仅 Google Maps 不够。基础三家：

| 平台 | 入口 | 优先级 |
|---|---|---|
| Google Maps | 自动同步自 GBP | 必（已含在 GBP）|
| Apple Maps | [Apple Business Connect](https://businessconnect.apple.com) | 必（iOS 用户基础）|
| Bing Places | [bingplaces.com](https://bingplaces.com) | 必（Bing / Microsoft ecosystem local surfaces）|

### 10.1 多 Maps 一致性

| 检查 | 说明 |
|---|---|
| Apple / Bing 的 NAP 与 GBP / site 完全一致 | 用 §6 同样规则 |
| Apple / Bing 的 categories 与 GBP primary category 对齐 | |
| Apple / Bing 的 hours 与 GBP / site 一致 | |
| Apple / Bing 的 photos 至少含 logo + 1 张 exterior + 1 张 interior | |

### 10.2 行业目录（按行业必查）

| 行业 | 目录 |
|---|---|
| 餐饮 | Yelp / TripAdvisor / OpenTable / Zomato / 大众点评（中国大陆）|
| 医疗 | Healthgrades / Zocdoc / WebMD / 好大夫在线（中国大陆） |
| 法律 | Avvo / Martindale / Justia |
| 婚庆 | The Knot / WeddingWire |
| 房产 | Zillow / Realtor.com / 链家 / 贝壳（中国大陆）|
| 酒店 | Booking / Expedia / 携程 / 飞猪（中国大陆）|

行业目录的 audit 多为人工 + 商业 listing service 半自动；evidence 必须标 `audit_mode`。

---

## 11. Blockers（必须阻断 release）

| Blocker | 触发条件 |
|---|---|
| `business_profile_requested_but_business_not_eligible` | §4.2 任一命中 |
| `fake_or_virtual_location_used_as_physical_location` | P.O. box / virtual office / 共享 hotdesk 作为唯一 physical address |
| `local_page_nap_conflicts_with_business_profile` | site 任一 NAP candidate 与 GBP canonical NAP 冲突（非 format drift，是真冲突）|
| `localbusiness_schema_claims_unverified_location` | LocalBusiness JSON-LD 中的 address / telephone / name 与 GBP 不一致 |
| `service_area_pages_are_doorway_pages` | service area pages 之间 boilerplate ratio < 30% 差异，被识别为 doorway page |
| `review_gating_detected` | 业主侧实现了 review gating（按满意度过滤后再请求 Google 评价）|

Blocker 阻断 `gsd-ship` / release。修复后重跑 audit。

---

## 12. Warn-only

| Warn | 触发 |
|---|---|
| `few_business_profile_photos` | GBP photos < 5 张 |
| `low_review_response_rate` | 业主回复率 < 50% |
| `service_area_not_clearly_described` | SAB 但未在 GBP / schema / site 明确列 areaServed |
| `local_landing_page_thin_content` | service area page 独特内容 < 400 words |
| `missing_apple_maps_or_bing_places_listing` | Apple Maps / Bing Places 任一缺失 |
| `localbusiness_schema_uses_generic_type` | @type 是通用 `LocalBusiness`，未选 subtype |
| `nap_format_drift` | site 内 NAP 格式不统一（不算 conflict）|
| `irregular_review_pattern` | reviews 在短期内异常增长（疑似买评，需人工核查）|
| `gbp_post_inactivity` | 近 90 天无 GBP post |

Warn-only 不阻断 release，但 evidence 必须记录。

---

## 13. CLI 命令示例

### 13.1 standalone audit

```bash
pnpm discoverability:audit:geo \
  --config discoverability.config.yaml \
  --out "evidence/discoverability/$TAG/raw"
```

> **路径约定（v1.2 harness）**：CLI 子命令名 `discoverability:audit:geo` 与 config 字段 `quality_gates.geo.*` / `channels.geo` 是 **config 端历史命名**，保留以免破坏已有 project pipeline（本 skill 改名 `web-local-seo` 不连带改 config schema）。但 **evidence 端是 canonical channel key `local`**：raw 脚本产物写 tag-scoped `evidence/discoverability/<tag>/raw/`，经 `discoverability-sdk evidence.append <tag> local <file>` 归一化进 `evidence/discoverability/<tag>/local.json`。**禁止**写 flat `evidence/discoverability/geo/`（无 `<tag>` + `geo` 是 forbidden evidence 文件名 / 目录名；canonical channel = `local`）。下例用 shell 变量 `TAG` 占位。

### 13.2 子命令拆分（按需调用）

```bash
pnpm discoverability:audit:geo --check eligibility
pnpm discoverability:audit:geo --check completeness
pnpm discoverability:audit:geo --check nap
pnpm discoverability:audit:geo --check schema
pnpm discoverability:audit:geo --check service-area-pages
pnpm discoverability:audit:geo --check reviews
pnpm discoverability:audit:geo --check maps-presence
```

### 13.3 自动化覆盖率边界

| 检查 | 覆盖率 | 说明 |
|---|---|---|
| eligibility | 50% | 自动检测：site 是否有 contact page + address；其余需 ASK 业主 |
| completeness | 30%-80% | 取决于是否有 GBP API key；无 key 时仅产 manual checklist |
| nap（site 内）| 100% | Grep + Read |
| nap（第三方目录）| 0-50% | 多数 directory 无 API，依赖 listing service 或人工 |
| schema | 100% | JSON-LD parser |
| service area pages | 100% | site 源码 grep + word count + diff |
| reviews | 20-100% | GBP API 可读 review；业主回复率 / 内容质量需人工 |
| maps presence | 0-30% | Apple / Bing 无开放 audit API，需人工 |

evidence 输出必须标 `audit_mode: auto | manual | pending`，不要假装人工部分已 audit。

---

## 13.4 quality_gates 字段映射

`discoverability.config.yaml` 的 `quality_gates.geo.*` 字段与本 SKILL 章节的对应关系。runner 拿 config 字段决定 audit 严格度时用此表反查具体 check 的所在节。

| Config 字段 | 对应 SKILL 章节 | Blocker / Warn |
|---|---|---|
| `require_business_profile_eligibility_check` | §4 Business Profile Eligibility + §11 `business_profile_requested_but_business_not_eligible` / `fake_or_virtual_location_used_as_physical_location` | blocker |
| `require_nap_consistency` | §6 NAP Consistency + §11 `local_page_nap_conflicts_with_business_profile` | blocker（真冲突）/ warn（format drift）|
| `require_localbusiness_schema_for_local_landing` | §7 LocalBusiness Schema + §11 `localbusiness_schema_claims_unverified_location` | blocker（与 GBP 不一致）/ warn（缺 subtype）|
| `require_localbusiness_subtype_specific` | §7.2 @type subtype 选择 + §12 `localbusiness_schema_uses_generic_type` | warn（缺 subtype）|
| `forbid_doorway_service_area_pages` | §8 Service Area Pages + §11 `service_area_pages_are_doorway_pages` | blocker |
| `min_service_area_page_unique_words` | §8.2 内容门 unique word count + §12 `local_landing_page_thin_content` | warn（默认阈值 400）|
| `min_owner_review_response_rate` | §5.2 Reviews 关键指标 + §12 `low_review_response_rate` | warn（默认阈值 0.50）|

字段名在 `quality_gates.geo.*` 下显式 false 时，对应 check 降级为 info 或跳过；显式 true 或设阈值后按上表 severity 强制。

---

## 13.5 Post-launch local measurement（上线后本地效果测量 — measurement-only）

> **加入 2026-06-27（SEO-doc audit P2-1）。** §4-§13 是**上线前 local audit**（GBP/NAP/schema/service-area pages/reviews 是否合规）；本节是**上线后测量**（真实曝光 / 来电 / 路线请求 / 预订）。补齐前，`local` 是 L12 四个 channel 里**唯一没有** post-launch measurement 的——本节对齐 `web-seo §15` / `web-aeo §20` / `app-aso §16.6`。

### 13.5.0 一句话定位

- **§4-§13（已有）= pre-launch local audit**：审 GBP/NAP/schema 形状，产 `local.json` channel evidence，进 audit gate（§20 blocker / warn）。
- **§13.5（本节）= post-launch measurement**：拉真实 GBP Performance 指标，产 `measurement.json`（measurement-only），**绝不进 gate**。

两条流并行、互不污染，与 L1 post-launch measurement（harness-contract `measure.pull` / `measure.compare`）同属上线后只读数据流。

### 13.5.1 GBP Performance API 是本地业务的 GSC

`web-seo` 用 Google Search Console Search Analytics 测网页搜索表现；**本地业务的等价物是 Google Business Profile Performance API**——按天给 business impressions（maps + search）、`direction_requests`、`call_clicks`、`website_clicks`、`bookings`、`conversations`。这正是 Google 官方文档 baseline（Phase 2）+ 月报（Phase 10）口径的本地版。

| 维度 | §4-§13 pre-launch audit | §13.5 post-launch measurement |
|---|---|---|
| 问题 | GBP/NAP/schema 合规吗？ | 上线后**实际**被多少人看到 / 联系 / 导航？ |
| 数据源 | GBP API 读字段 + site 源码 grep | **GBP Performance API**（`locations/<id>:fetchMultiDailyMetricsTimeSeries`）|
| 产物 | `local.json`（channel evidence）| `measurement.json`（measurement-only）|
| 进 gate？ | ✅ §20 blocker / warn | ❌ 否（`gate.check` 完全忽略）|

### 13.5.2 Script-first 红线（AI 永不编造本地指标）

继承 §20 执行宪法 + harness §8.2：

1. **每个指标来自一次真实 API 调用**（GBP Performance API）。AI **绝不**凭印象写"你大概每月 X 次来电"。
2. **无凭证 → `status: skipped`**，绝不编造。由 L1 的 `disc-measurement-puller` agent 拉取（`measure.pull --provider gbp`，provider 已在 SDK `MEASUREMENT_PROVIDERS` + `PROVIDER_CHANNEL["gbp"]="local"`）。无 GBP 凭证 → skipped。
3. **BYO creds 从环境变量取**（`GBP_OAUTH_JSON` / `GOOGLE_APPLICATION_CREDENTIALS` + account/location id），**绝不**提交进仓库 / chat / report。
4. AI 只在**最后一步**解读 `measurement.json` 的真实漏斗，关联到 §4-§6 哪些 GBP/NAP 改动可能起效——不产生任何指标本身。

> **本 skill 读权限边界不变**：本节 API 拉取**不由本 skill 跑**，RETURN 给 L1 的 `disc-measurement-puller` agent（有 Bash）执行 `measure.pull`，本 skill 只**解读**归一化后的 `measurement.json`。与 §13.3 "无 GBP key 时仅产 manual checklist" 的既有读权限模型一致。

### 13.5.3 拉取（由 disc-measurement-puller agent 跑）

```bash
# GBP Performance API；无 key → skipped，绝不编造
python ~/.claude/skills/discoverability-orchestrator/scripts/discoverability-sdk.py \
  --project-root . measure.pull "$TAG" --provider gbp \
  "evidence/discoverability/$TAG/raw/gbp-performance.json"

# 优化前后对比（真实曝光/来电/路线 delta，纯算术；measure.compare 自动按 metric 方向判 improved/regressed）
python ~/.claude/skills/discoverability-orchestrator/scripts/discoverability-sdk.py \
  --project-root . measure.compare "$TAG" --baseline-tag "$BASELINE_TAG"
```

### 13.5.4 measurement → 优化映射 + relevance/distance/prominence 框架

Google 官方"**local ranking = relevance + distance + prominence**"（§16 来源）是解读这些指标、也是组织 §4-§8 审计的统一框架。distance（用户与门店的物理距离）不可控，但 relevance 与 prominence 完全可由 listing 改动驱动：

| 三因素 | 可控？ | 喂它的审计章节 | 对应 measurement 信号 |
|---|---|---|---|
| **relevance**（业务与查询的匹配度）| ✅ | §4 categories / completeness、§7 LocalBusiness schema | impressions 低 → relevance 弱 |
| **prominence**（知名度 / 权威）| ✅（缓慢）| §5 reviews、§6 NAP/citations、本地外链（→ `discoverability-growth`）| impressions 有但 call/direction 低 → prominence 没转成行动 |
| **distance**（就近）| ❌ | §6 NAP 地址准确性 / §8 areaServed 喂它 | 某 service area 显著低 → 该区 relevance/prominence 弱 |

> AI 只做这层**解读 + 路由**，指标本身 100% 来自 API。**绝不**反过来用 listing 形状去"推算"应该有多少曝光/来电。

### 13.5.5 measurement-only 边界（反模式）

| 流 | 产物 | 进 gate？ |
|---|---|---|
| pre-launch local audit（§4-§13）| `local.json` channel evidence | ✅ §20 blocker / warn |
| post-launch measurement（§13.5）| `measurement.json`（`measurement_only: true`）| ❌ 完全忽略 |

- ❌ 把 GBP impressions / call_clicks 写进 release gate（观测值，Google 本地排名算法未公开，永不 blocker）
- ❌ 无凭证时让 AI 编一个曝光/来电数字（必须 `status: skipped`）
- ❌ 把 measurement 产物写进 `local.json` 污染 pre-launch channel evidence

---

## 14. Evidence 输出

归一化后的 channel evidence 落 `evidence/discoverability/<tag>/local.json`（canonical channel key `local`，由 `discoverability-sdk evidence.append <tag> local <file>` 写入，schema 见 harness contract §4）。下表 raw 脚本产物落同一 tag 的 `raw/` 工作目录，被 `local.json` 的 `findings[].evidence_path` 反查引用：

| raw 文件（在 `<tag>/raw/` 下） | 内容 |
|---|---|
| `business-profile-eligibility.json` | 业务类型 / 地址性质 / 接触模式 / eligibility verdict |
| `business-profile-completeness.json` | 每个字段的 present / missing + completeness score |
| `nap-consistency.json` | site 内 NAP candidates 列表 + GBP canonical NAP + 第三方 directory NAP（已 audit 的）+ conflict / format-drift 列表 |
| `localbusiness-schema.json` | 解析到的 JSON-LD + 校验结果（@type subtype / NAP 一致 / openingHours 一致 / sameAs 含 GBP）|
| `service-area-pages.json` | 每 service area page 的 URL / unique word count / boilerplate ratio / 本地化信号数 / verdict |
| `reviews.json` | review 数量 / 平均分 / 业主回复率 / 回复时效 / 异常模式 |
| `maps-presence.json` | Google / Apple / Bing / 行业目录 listing 状态（present / missing / NAP-conflict / not-audited） |

> **禁止** flat `evidence/discoverability/geo/`（无 `<tag>` + `geo` 是 forbidden evidence 文件名 / 目录名）、自产 `summary.json` / `gate-result.json`。blocker / warn / overall verdict 的聚合由 `discoverability-sdk gate.check` 写 `<tag>/gate-result.yaml`，narrow skill 不自产顶层 summary。

### 14.1 evidence schema 关键字段

每个 JSON 输出必须含：
- `audit_mode`: `auto` | `manual` | `pending` | `mixed`
- `audited_at`: ISO timestamp
- `audit_coverage`: 百分比（已 audit 的字段 / 总字段）
- `unaudited_fields`: 列表（哪些字段未 audit 及原因）

---

## 15. 常见误区 / 反模式

| 反模式 | 正确做法 |
|---|---|
| 帮 online-only / pure SaaS 申请 GBP | 拒绝（Google policy + suspend 风险）|
| 用 P.O. box / 虚拟办公室 / 共享 hotdesk 作为 physical address | BLOCKER |
| Service area page 用 boilerplate 只换城市名（doorway page）| 真实本地内容差异化 |
| Review gating（按满意度过滤后再请求 Google 评价）| 公开普适邀请所有客户 |
| 业主用马甲账号留 5 星 | 严禁 |
| 买评 / 刷评 / 礼品换评 / 亲友互评 | 严禁（Google + FTC）|
| NAP 在不同平台不一致 | 跨 site / GBP / schema / Apple / Bing / 行业目录全部一致 |
| LocalBusiness schema 与 GBP / 可见页面信息不一致 | 三者同 source-of-truth |
| 用通用 `LocalBusiness` 作为 @type | 选最具体 subtype |
| 多分店所有信息塞一个 page | 每分店独立 page + 独立 JSON-LD + branchOf 关联 |
| 业主回复用 ChatGPT 模板批量生成"thank you" | 真人 / 真实 / 提具体服务 |
| Negative review 公开回复中暴露客户 PII（姓名 / 订单号 / 病历号）| public reply 一律泛指 + offline 处理；PII workflow → AppSec / compliance team |
| 把 LocalBusiness JSON-LD 写在 noindex page 上 | 写在对应分店 / service area 的可索引 page 上 |
| GBP business name 堆关键词（"北京最好的牙科诊所 - 牙博士"）| 用真实招牌名 |
| 为业务实际不服务的 city 创建 service area page | 只为真实 areaServed 的 city 创建 |
| 用 stock photo / 网图作为 GBP 主要 photos | 真实店面 / 团队 / 产品 |
| "GBP 一次设置好就不管了"（posts / hours / photos 长期不更新）| 周期性维护（hours 至少季度审，photos 至少半年加，posts 至少月度）|

---

## 16. 权威来源

| 来源 | 用途 |
|---|---|
| [Google Business Profile guidelines](https://support.google.com/business/answer/3038177) | eligibility / name / address / categories / 禁止行为的 official policy |
| [schema.org/LocalBusiness](https://schema.org/LocalBusiness) | JSON-LD 字段定义 + subtype 树 |
| [Google's local search ranking factors](https://support.google.com/business/answer/7091) | relevance / distance / prominence 三因素 |
| [Apple Business Connect](https://businessconnect.apple.com) | Apple Maps listing 入口 |
| [Bing Places for Business](https://www.bingplaces.com) | Bing Maps + Bing search listing 入口 |
| [Google review policies](https://support.google.com/contributionpolicy/answer/7400114) | review gating / 假评 / 买评的 official ban |

---

## 17. 与其他 skill 的接口

### 17.1 来向（谁触发 web-local-seo）

| 来源 | 触发时机 |
|---|---|
| `discoverability-orchestrator` | 检测到业务有线下接触点 / 服务区域，分派到 L12 子层 |
| user 直接 invoke | 用户提到 GBP / Google Maps / Local SEO / NAP / 本地服务 |
| `gsd-pipeline-orchestrator` | spec / plan 阶段识别项目为本地服务业务 |

### 17.2 去向（web-local-seo 把什么 handoff 出去）

| 接收方 | 何时 handoff |
|---|---|
| `web-seo` | 标准 SEO 部分（meta / sitemap / canonical / CWV / 非 LocalBusiness schema） |
| `web-aeo` | AI search optimization / answer engines / llms.txt / Generative Engine Optimization |
| `app-aso` | 如果业务有移动 app，应用商店优化 |
| `appsec-security-orchestrator` | 任何 security / privacy / PII / cookie / GDPR 问题（**本 skill 绝不写 security**） |
| 人工 / 业主 | GBP 创建 / 认领 / 验证 / reviews 回复 / posts 维护 / 第三方目录提交（无 API 的部分）|

### 17.3 与 web-seo 共享但不重复

| 字段 | 在哪做 |
|---|---|
| sitemap.xml / robots.txt / canonical | web-seo |
| meta title / description / OG | web-seo（但 web-local-seo 的 service area page 必须含 city + service）|
| Article / Product / FAQ schema | web-seo |
| LocalBusiness schema | **web-local-seo** |
| Local landing page 的内容差异化门 | **web-local-seo** |
| 通用 Core Web Vitals / page speed | web-seo |
| city + service 的关键词研究 | web-local-seo（local query 含 city + intent，是 local-specific）|

---

## 18. Hard Rules（不可违反）

1. 不帮不合规业务申请 / 维护 GBP（§4.2 任一命中即拒绝）
2. 不替业主写 review 回复（提供 framework + checklist，最终内容由业主决定）
3. 不指导 review gating / 买评 / 刷评 / 礼品换评（Google + FTC 违规）
4. 不为业务实际不服务的地区创建 service area page
5. 不用通用 `LocalBusiness` @type（必须 subtype）
6. 不在 negative review 公开回复中暴露任何客户 PII（具体 PII 处理流程 → `appsec-security-orchestrator` / compliance team）
7. 不假装人工部分已 audit（evidence 必须诚实标 `audit_mode`）
8. 不在本 skill 写 security / AppSec / pentest 内容（一律 handoff `appsec-security-orchestrator`）
9. 不在本 skill 写 AI search / AEO / answer engine / llms.txt / Generative Engine Optimization 内容（一律 handoff `web-aeo`）
10. GBP business name 不堆关键词（必须与法律名称 / 现场招牌一致）

---

## 19. 与 L12 父层的契约

本 skill 是 L12 Discoverability 子层之一。父层（`discoverability-orchestrator`）按以下规则调用本 skill：

| 父层信号 | 是否激活 web-local-seo |
|---|---|
| 项目含线下业务（contact page + physical address + business hours） | 激活 |
| 项目是 SAB（service area business）| 激活 |
| 项目是多分店 / 连锁 | 激活 |
| 项目是 pure SaaS / 全球分发 / online-only | 不激活 |
| 项目是个人 blog / 作品集 | 不激活 |

本 skill 输出的 channel evidence（`evidence/discoverability/<tag>/local.json`）会被 `discoverability-orchestrator` 经 `discoverability-sdk gate.check` 聚合进 `evidence/discoverability/<tag>/gate-result.yaml`，作为 release readiness 的一部分（顶层无 `summary.json` 这种文件）。

---

## 20. L12 Harness Integration (v1.2+)

本 skill 在 L12 harness v1.0 模式下作为 **`local` channel**（canonical key）的 auditor —— **不是 `geo`**。Evidence 写入由 SDK 调度：`python scripts/discoverability-sdk.py evidence.append <tag> local <file>`。

**Channel key canonicalization**（务必区分 config 端 vs evidence 端）：

| 层 | Key | 说明 |
|---|---|---|
| Config 端 | `channels.geo` | 历史兼容字段；语义 = Local SEO（不是 Generative Engine Optimization） |
| Evidence / SDK / harness 端 | **`local`**（canonical） | **绝不**把 `geo` 写到 evidence path —— 避免与 AI search 域 GEO 概念混淆 |
| Narrow skill | `web-local-seo` | frozen 2026-05-25 改名，原 `web-geo`，名称受 §15.1 safety freeze 保护 |
| Evidence path | `evidence/discoverability/<tag>/local.json` | tag 维度由 harness v1.0 引入 |
| 触发条件 | `conditional_local` | `project.physical_locations > 0 OR len(project.service_areas) > 0` |

**Script-first 强制**（继承 L12 执行宪法）：deterministic source 必须来自 GBP API / Apple Business Connect API / Schema.org LocalBusiness validator / 跨 site + GBP + 第三方目录的 NAP audit script。全 `manual_ai_scan` evidence → **BLOCKED**（disc-evidence-validator 标 hard_rule_violation）。反模式：让 AI 凭"看起来合理的"评价业务地理可靠性、虚构 GBP listing 字段、用语义猜测代替 API 查询。

**Local SEO 合规红线**（永远 blocker，evidence-validator / gate.check 不得 downgrade 为 warn）：

1. `business_profile_requested_but_business_not_eligible` —— online-only / virtual office / shared hot-desk 申请 GBP
2. `fake_or_virtual_location_used_as_physical_location` —— 虚拟地址冒充实体 location
3. `local_page_nap_conflicts_with_business_profile` —— 真实 conflict（不同 phone / 不同 address，非格式差异）
4. `localbusiness_schema_claims_unverified_location` —— JSON-LD 声明未经平台 verify 的 location
5. `service_area_pages_are_doorway_pages` —— boilerplate `"{city}"` 模板批量生成
6. `review_gating_detected` —— 区别对待正负评价邀请（违反 Google / FTC）

**Warn-only**（不阻断 release，仅 advisory）：`few_business_profile_photos`、`low_review_response_rate`、`nap_format_drift`（"St" vs "Street" 仅格式差异）、`gbp_post_inactivity`、`missing_apple_maps_or_bing_places_listing`。

**Frozen names + 依赖**（§15.1 safety-critical name freeze 一部分）：受保护名称包括 skill `web-local-seo`、channel `local`、evidence path `evidence/discoverability/<tag>/local.*`。改名 = 同时打掉 disambiguation（与 Generative Engine Optimization 区分）+ harness safety surface（hook / SDK / gate 通过名字识别）。完整契约见 `~/.claude/templates/discoverability/harness-contract.md` §1（全景架构 / channel keys）+ §4.2（Local SEO 合规红线必为 blocker）。

---

## 21. Changelog

- **2026-05-25 v1.1.0**: 改名 `web-geo` → `web-local-seo`（行业 2025-2026 把 "GEO" 100% 等同 Generative Engine Optimization，原名歧义严重）。frontmatter 补齐 15 字段（canonical_id / aliases / parent / layer / sibling-skills / children / upstream / downstream / forbidden-tools / disable-model-invocation），与 `app-aso` 同构。删除/合并 6 处冗余 GEO 命名澄清章节，合并为 §0 单 callout。quality_gates 字段映射补 3 项（require_localbusiness_subtype_specific / min_service_area_page_unique_words / min_owner_review_response_rate）。CLI 命令路径 `discoverability:audit:geo` 与 config 字段 `channels.geo` / `quality_gates.geo.*` 保留 config 端历史命名以避免破坏已有 project 的 audit pipeline（见 §13.1 说明）。注：自 v1.2 harness 起 **evidence 端** canonical channel key 为 `local`，evidence path 为 `evidence/discoverability/<tag>/local.json`（不再用 flat `evidence/discoverability/geo/`，见 §14 / §20）。
- **2026-05-25 v1.0.0**: Initial release（原 `web-geo`）。建立 Geographic / Local SEO 命名约定；定义 4 个 L12 narrow skill 边界；产出 Business Profile eligibility / completeness / NAP / schema / service area pages / reviews / maps presence 七个 audit 维度；定义 6 个 BLOCKER + 9 个 WARN；明确自动化覆盖率边界与 evidence schema。
