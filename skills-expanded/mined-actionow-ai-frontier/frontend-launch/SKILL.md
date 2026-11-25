---
name: frontend-launch
description: 前端项目上线前的发布工程收尾：全套 SEO 落地（meta/favicon 接线/OG meta/JSON-LD/sitemap/robots 六项清单）与可选数据监测接入（默认告知可接 Google Analytics，用户同意才接线）。当用户说「上线前检查」「SEO 优化」「接入统计/分析/GA」「配 meta/分享卡片」「sitemap」时触发。消费 frontend-brand 的产物（brand-profile/og-image/logo），缺失时降级处理不阻塞。
---

# frontend-launch · 发布工程收尾入口

## Mandate

为**已有前端项目**做上线前的发布工程收尾——把 SEO 六项（meta / favicon 接线 / OG meta / JSON-LD / sitemap / robots）逐项落地，并按需接入可选数据监测（默认只告知「可接 Google Analytics」，用户显式同意才接线）。消费 `frontend-brand` 已产出的品牌产物，不凭空另造一套视觉。

**何时触发本 skill**：用户说「上线前检查」「SEO 优化」「接入统计 / 分析 / GA」「配 meta / 分享卡片」「sitemap」。

**不替代什么**：
- **与 frontend-brand 分工**：品牌视觉产物（`brand-profile` / logo / og-image / favicon 变体）由 `frontend-brand` 产出，本 skill 只**消费**这些产物做接线 / SEO / 部署收尾，**不重新设计视觉**。favicon 的多尺寸切图与 HTML 接线归本 skill（`frontend-brand` 只交付 favicon 变体 prompt）。
- **与 frontend-templates 分工**：选骨架 / 注入设计体系归 `frontend-templates`；本 skill 是发布前的最后一公里。

## 库根与前置（先确认这一步）

- 库根：`~/frontier`；本 skill 的 references 根 `~/frontier/skills/frontend-launch/references/`（两份 reference 见「库内导航」的分层引用表，Task 8/9 落地后可用）。
- **brand-profile 交接单源（同 frontend-brand）**：两 skill 经消费方项目的 `docs/brand/brand-profile.md` 交接品牌基因——**谁先跑谁生成**，之后**已存在则复用不覆盖**，用户可显式要求重建。它是 SEO meta（品牌名 / `og:site_name` / description 语气 / theme-color 取值）的事实源。
- **缺 brand-profile 时**：现场提取——提取步骤的正文在 `frontend-brand` SKILL.md 的 `## brand-profile 提取步骤` 小节，**指向该节、不复制正文**（快速路径读 graphite 声明，通用路径推断 token，末尾都要问用户产品定位与受众）。
- **消费 frontend-brand 产物的路径口径**：og-image 取 `frontend-brand`「产物路径」表约定的 `public/og-image.png`；favicon 取 `frontend-brand` logo 模块产出的 favicon 变体。资产是否就位在工作流第 2 步盘点，缺失按「降级行为表」处理。
- **库缺失时的行为**：若 `~/frontier` 不存在，**停下来问用户库的位置**（本地路径或 git 地址），不要自行猜测路径、不要跳过。拿到位置后把下文所有 `~/frontier` 替换为实际库根再继续。

## 工作流五步

每步给出「判断依据」与「产出」，逐步推进，不跳步。

### 1. 确保 brand-profile 存在

- **判断依据**：查消费方 `docs/brand/brand-profile.md`。存在且色值未漂移 → 复用；不存在 → 按 `frontend-brand` SKILL.md 的 `## brand-profile 提取步骤` 现场提取；用户要求重建 → 重跑提取覆盖旧档。
- **产出**：一份可用的 `brand-profile.md`——本 session 所有 meta 文案 / theme-color / 结构化数据的**唯一事实源**。

### 2. 盘点现状

- **判断依据**：读消费方 `index.html`（SPA 的 `<head>`）与 `public/` 目录，逐项比对 SEO 六项与所需资产（og-image / favicon），列出「已有 / 缺失 / 需改」清单**给用户过目**，缺资产的项先记账不硬造。
- **产出**：一张现状清单——哪些已接、哪些缺、哪些要改，作为第 3 步的落地依据。

### 3. SEO 六项逐项落地 · analytics 先询问再落地

- **判断依据**：读 `references/seo-checklist.md`（完整路径见「库内导航」），六项**逐项落地**；产物依赖（og-image / favicon）缺失时按「降级行为表」处理，不阻塞其余项。**analytics 默认不接**——先问用户是否接入 GA，**用户同意才**读 `references/analytics.md` 落地；未同意则该项在报告里记「用户未接」。
- **产出**：六项 SEO 接线 diff（`git status` 可见）；analytics 视用户决定接或不接。

### 4. 浏览器实测验收

- **判断依据**：起 dev server（消费方 `pnpm dev` 等），浏览器打开后按下列可操作动作逐项核对，不靠肉眼扫源码想当然：
  1. **view-source / 读 `<head>`**，六项逐条确认在且值正确：① `<title>` + `<meta name="description">`（含 viewport / charset）；② `<link rel="icon">` favicon 接上（正式图或降级占位）；③ `og:*` + `twitter:*` 分享 meta 齐全且 `og:image` 是绝对 URL；④ `<script type="application/ld+json">` 且为 `@graph` 聚合；⑤ `<link rel="canonical">`（生产域名或标 TODO）；⑥ 两条 `theme-color`（浅 / 暗 media 各一）。
  2. **直接访问 `/sitemap.xml` 与 `/robots.txt`** 确认可达、内容正确。
  3. **若接了 GA**：打开 network 面板，过滤 `collect`（GA4 为 `g/collect`）确认打点请求发出、状态正常。
- **产出**：逐项 pass / fail 的实测核对结论，作为报告的证据。

### 5. 输出上线检查报告

- **判断依据**：把六项 + analytics 的落地状态汇成一张表，**TODO 项必须列明原因**（如「canonical 待生产域名」「og:image 待 frontend-brand 产出 og-image.png」），不含糊带过。报告格式如下：

  | 项 | 状态 | 备注 / TODO 原因 |
  | --- | --- | --- |
  | meta（title / description / viewport） | 已接 / TODO | |
  | favicon 接线 | 已接 / 降级占位 / TODO | 降级时注明「待 frontend-brand 出正式 favicon」 |
  | OG + Twitter meta | 已接 / TODO | |
  | JSON-LD（`@graph`） | 已接 / TODO | |
  | sitemap.xml | 已接 / TODO | |
  | robots.txt | 已接 / TODO | |
  | analytics（GA） | 已接 / 用户未接 / 未询问 | 默认不接，需用户显式同意 |

- **产出**：上述状态表 + 第 4 步实测结论；有 TODO 的项说清「卡在什么、需要用户提供什么」（域名 / 是否接 GA / 是否补产物）。

## 降级行为表

产物缺失不阻塞上线收尾，按下表降级并回提用户补齐来源：

| 缺失产物 | 降级行为 |
| --- | --- |
| favicon 缺失 | 用**文字占位 SVG data-URI**（品牌首字母 / 缩写）临时顶上**单条** `<link rel="icon">`；其余 4 条 file-based `<link>`（`favicon.ico` / `32x32` / `16x16` / `apple-touch-icon`）与 `site.webmanifest` **暂不注入**——它们指向尚不存在的 PNG 会 404（JSON-LD `Organization.logo` 引的 `icon-512.png` 同理），改以 HTML 注释列出完整待接清单挂 `TODO`。提示用户**先跑 frontend-brand** 出正式 favicon 变体，再回来把注释里的全家桶 + `site.webmanifest` 补全替换。 |
| og-image.png 缺失 | `og:image` 项**记 TODO 不阻塞其余五项**；报告注明「待 frontend-brand 产 `public/og-image.png`」。 |
| brand-profile 缺失 | **现场提取**（指向 `frontend-brand` SKILL.md 的 `## brand-profile 提取步骤`，不复制正文），提取完再继续，不停在此。 |

## 坑位沉淀（体系性不可犯的错）

初始条目如下，随仓库演进增补：

- **不擅自加第三方脚本**：GA 及任何第三方统计 / 埋点 / 广告脚本**必须用户显式同意**才接；默认只告知「可接 GA」，绝不主动注入 `<script>`。
- **og:image 必须绝对 URL**：`og:image` / `twitter:image` 一律用完整 `https://域名/og-image.png` 绝对 URL——相对路径**多数社交平台抓不到**，分享卡片会空。
- **canonical / og:url 用生产域名不是 localhost**：SPA 的 `<link rel="canonical">` 与 `og:url` 填**生产域名**；没有域名就**问用户**，占位一律标 `TODO`，别把 `localhost` 当成品发出去。
- **theme-color 浅暗双条**：`<meta name="theme-color">` 给浅色 / 暗色**两条**，用 `media="(prefers-color-scheme: light)"` 与 `dark` 区分，别只留一条导致另一主题下地址栏配色错。
- **JSON-LD 用 `@graph` 聚合**：结构化数据用**单个** `<script type="application/ld+json">` 里的 `@graph` 数组聚合多实体（Organization / WebSite / WebPage 等），别散落成多个 script。
- **禁 emoji**：本 skill 的所有产出（meta 文案、上线检查报告、注入的代码与注释）一律不得出现 emoji，用纯文字替代。注意 graphite 的 `check:ui` emoji 护栏只扫 `--source` 指定的 `src/` 树；本 skill 的产物落点（项目根 `index.html`、`public/*`、消费的 `docs/brand/*.html`）都在 `src/` **之外**，不在自动扫描范围内——禁 emoji 靠人工把关，别指望护栏兜住。

## 库内导航

- **分层引用表**（本 skill references，Task 8/9 落地后可用）：按命中步骤只读该份，别两份全读。

  | reference | 完整路径 | 什么时候读 |
  | --- | --- | --- |
  | seo-checklist | `~/frontier/skills/frontend-launch/references/seo-checklist.md` | 工作流第 3 步，SEO 六项逐项落地时 |
  | analytics | `~/frontier/skills/frontend-launch/references/analytics.md` | 工作流第 3 步，**用户同意接 GA 后**才读 |

- **兄弟 skill**：`frontend-brand`（产 `brand-profile` / logo / og-image / favicon 变体）、`frontend-templates`（选骨架 / 注入设计体系）。
- **消费的 frontend-brand 产物路径口径**（详见 `frontend-brand` SKILL.md 的「产物路径」表）：`docs/brand/brand-profile.md`（meta 事实源）、`public/og-image.png`（`og:image` 源）、favicon 变体（logo 模块产出，本 skill 负责切图与接线）。
