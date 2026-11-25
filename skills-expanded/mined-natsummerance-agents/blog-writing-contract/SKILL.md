---
name: blog-writing-contract
description: |
  博客写作规约与交付门禁：从选题/brief 到成稿，每篇草稿必须通过五道质量门（能力发现/格式完整性/视觉验证/内容评审/资产链接完整性）并达到 100 分制评审 ≥90 分才允许交付，未过门则迭代至多 3 次后上报。当用户要"写一篇博客文章""发布前把过关""给这篇草稿打个分"时触发。不适用于：整站 SEO 审计（转 seo-audit）、AI 搜索可见性优化（转 geo-search-optimize）、单页 JSON-LD 标记生成（转 schema-markup）。
source_project: AgriciDaniel/claude-blog
tags: [blogging, content-quality, delivery-contract, editorial-review, fact-check]
---

# blog-writing-contract

## R · 上游引用

> "The core promise is simple: the user is never the first reviewer. A 5-gate Blog Delivery Contract scores every draft against a 100-point rubric, blocks delivery below 90, verifies artifacts and links, and iterates up to 3 times before escalation."
> "Every `/blog write` and `/blog rewrite` result must pass the delivery contract before it is shown to the user."
> "Scoring bands: Exceptional (90-100), Strong (80-89), Acceptable (70-79), Below Standard (60-69), Rewrite (<60). The delivery contract blocks delivery below 90."

来源：AgriciDaniel/claude-blog 仓库 `README.md`（https://raw.githubusercontent.com/AgriciDaniel/claude-blog/main/README.md ，fetch 于 2026-08-26；main 直取成功，无需启用 HEAD 备选；本地无该上游 clone）

## I · 方法论骨架

1. **五道交付门**（顺序执行，任一失败即打回重写）：
   - 门 1 能力发现：写作前确认所需工具、代理、环境变量与可选依赖。
   - 门 2 格式完整性：`.md` + `.html` + `.pdf` + 真实 hero 图四件套齐备。
   - 门 3 视觉验证：375/768/1280 三档视口截图正常、JSON-LD 有效、暗色模式不破版。
   - 门 4 内容评审：评分 ≥90 且零 P0 问题——这是唯一有否决权的软门。
   - 门 5 资产与链接完整性：图片可解析、og:image 在场、外链返回 200、字数与声明偏差 ≤5%。
2. **100 分制评分**：内容质量 30 / SEO 优化 25 / E-E-A-T 信号 15 / 技术元素 15 / AI 引用就绪 15；<60 判 Rewrite。
3. **迭代上限**：任一门失败最多重写 3 次，仍不过则升级给人——用户永远不是第一个审稿人。
4. **事实核查内建**：统计数字必须溯源，逐条判 exact match / paraphrase / not found；引文核不出即阻断发布。
5. **本地场景映射**：本 agent 惯称的"事实核查/SEO 合规/可读性/原创性/CTA"五门是口语化概括，执行以上游五门为准，两类维度在评分表中对号入座。

## A1 · 案例

- **输入**："写一篇关于'小团队如何做关键词研究'的博客，写完直接发。"
- **做法**：产出草稿+四件套→门 3 发现暗色模式下代码块文字不可读→门 4 评 86 分（E-E-A-T 缺作者资历段）→门 5 发现两处外链 404；三轮迭代补齐后复评 92。
- **结果**：第 4 稿过全部门禁交付：含可验证的带来源数据、三档视口截图、有效 JSON-LD；用户拿到的不是初稿而是已拦截 3 类缺陷的成品。

## A2 · 触发判断 ★

适用情境：
1. 用户要求从选题或 brief 开始写一篇博客文章/站点内容。
2. 用户已有草稿，要求发布前质检、"把过关"、按质量门或评分标准审稿。
3. 用户问"这篇稿子能不能发""帮我改到能发布的水平"。

语言信号（≥3 条）：
- "帮我写一篇博客文章 / 公众号长文"
- "这篇草稿发布前帮我把关一下"
- "给我的文章打个分，看能不能发"
- "按质量门/检查清单过一遍这篇稿子"

与兄弟 skill 的区分：blog-writing-contract 管**文章生产与交付门禁**——输入是选题或草稿，输出是过五门的成品；整站体检归 `seo-audit`（其报告建议"该补内容"时转介过来）；给旧文做 AI 可见性诊断归 `geo-search-optimize`（新文章的 AI 引用就绪度只是本 skill 评分表中 15 分的子项）；为成稿页面单独生成 JSON-LD 归 `schema-markup`（本 skill 的门 3 只校验标记有效性，生成规范调用对方）。反向诱饵：只要请求落在"写/改/审一篇具体文章"，即使顺带提到 SEO 或 AI，也先归本 skill。

## E · 执行流程

1. **确认写作任务与目标读者** — 完成标准: 拿到主题、目标读者和平台三要素，缺任何一项退回补问而非臆测。
2. **门 1·能力发现** — 完成标准: 所需工具/依赖清单核对完毕，缺失项已声明而不是写到一半才发现。
3. **起草并自查四件套** — 完成标准: `.md`/`.html`/`.pdf`/hero 图全部存在且互相同源，字数与大纲声明偏差 ≤5%。
4. **门 3·视觉验证** — 完成标准: 375/768/1280 三档截图无破版、JSON-LD 解析有效、暗色模式可读。
5. **门 4·内容评审打分** — 完成标准: 按五类权重给出百分制分数与逐项扣分理由；所有统计数字附来源核查结论（exact/paraphrase/not found）。
6. **门 5·资产与链接完整性** — 完成标准: 全部图片可解析、og:image 在场、外链逐一返回 200。
7. **交付或上报** — 完成标准: ≥90 分且零 P0 才交付；不足则带着扣分明细重写，累计 3 次仍未过即向用户说明差距并请求决策，绝不悄悄降标放行。

## B · 边界与红线

不适用（≥2）：
- 整站技术 SEO 审计与反链画像 → 转 `seo-audit`。
- 已发布内容的 AI 引擎可见性与品牌信号诊断 → 转 `geo-search-optimize`。
- 单页 JSON-LD 标记的专项生成与双验证 → 转 `schema-markup`。

局限：
- 90 分门槛保证的是**内部质量下限**，不构成市场反馈——阅读量、转化与排名仍取决于选题、渠道与竞争，报告中不得暗示"过了门就必火"。

红线：
- **SEO 无法保证排名结果**：即使文章 SEO 得满分，也不承诺名次、收录时限或流量数字。
- **拒绝黑帽手法**：关键词堆砌、隐藏文字、链接农场式互链、抄袭洗稿凑原创一律拒绝——上游设计本身阻断虚构数据（factcheck 不过关即阻断），洗稿类请求同样拒接并说明平台与搜索引擎惩罚风险。
- 收到"照着第一名抄一篇再堆点关键词，保证排第一"类要求：拒绝并解释——排名由算法决定无人可保，堆砌与抄袭属黑帽会被降权；随后把需求翻译回合规路径：差异化角度 + 可验证数据 + 过五门的交付质量。

## 相关 skills

- `seo-audit` — 上游漏斗：审计建议"补内容"时的承接方。
- `geo-search-optimize` — 文章 AI 引用就绪度的全局方法论来源，本 skill 取其 15 分子项。
- `schema-markup` — 成稿页面的 JSON-LD 生成规范提供方，门 3 调用其标准。

---

## 审计信息

- V1✓ 来源可溯：R 段引用 fetch 所得上游 README ≤100 词，标注 raw URL 与获取路径
- V2✓ 四角分工：博客写作交付角，A2 与 seo-audit / geo-search-optimize / schema-markup 互设诱饵并写明区分
- V3✓ 红线齐备：不承诺排名/传播效果 + 黑帽与洗稿排除 + "保第一"拒绝话术入 B 段与 edge_case
- 蒸馏时间：2026-08-25（2026-08-26 复核：R 段三条引文与评分表、五门定义逐项比对通过）
- 来源：fetch — https://raw.githubusercontent.com/AgriciDaniel/claude-blog/main/README.md （main 直取成功；本地无该上游 clone）
