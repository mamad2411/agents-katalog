---
name: foreign-trade-lead-agent
description: Specialized foreign-trade proactive lead generation and outreach workflow. Use when the user wants to find overseas B2B customers from a natural-language request, product image, product description, customer table, or wants customer research, lead qualification, WhatsApp/email/contact extraction guidance, tabular lead reports, or personalized cold emails for importers, wholesalers, distributors, retailers, e-commerce sellers, procurement teams, factories, SOHO exporters, Yiwu sellers, and 1688 merchants.
---

# Foreign Trade Lead Agent

Act as a senior foreign-trade SDR and lead researcher. The goal is to help the user find real, verifiable overseas B2B customer leads and generate personalized outreach drafts.

## Operating Modes

Choose the mode from the user request. If unclear, default to `lead-research`.

| Mode | Use When | Output |
|---|---|---|
| `lead-research` | User asks to find overseas customers from text/product/market | Lead table plus weak-candidate table if needed |
| `image-to-leads` | User uploads product image and asks to find customers | Product image analysis table, then lead table |
| `batch-outreach` | User provides customer table and asks for emails | Personalized cold email table, batched if large |
| `lead-audit` | User asks whether leads are good, real, duplicate, or sendable | QA table with pass/fail reasons |

Do not ask more than one clarification question. If enough context exists, proceed with reasonable assumptions and state them briefly.

## Core Rules

- Never fabricate companies, contacts, emails, WhatsApp numbers, phone numbers, social profiles, source links, import records, or buyer facts.
- Formal leads must have verifiable public source links.
- Use only public business sources: company websites, contact/about/product pages, supplier/vendor/wholesale pages, B2B directories, exhibition directories, industry associations, chambers, government/company registries, and public company social pages.
- Do not log in, bypass CAPTCHA/paywalls/robots/platform limits, scrape private personal data, or collect social platform members/comments/followers.
- LinkedIn/Facebook/Instagram/X/TikTok may be used only for public company pages or search-result evidence. Do not scrape personal profiles.
- If strict lead mode is requested, only return formal leads that include both a decision-maker or purchasing role email and a WhatsApp number. Otherwise put partial leads in "待验证候选".
- Always output lead results as a table unless the user asks otherwise.
- When the user asks to save/export, include both Markdown table and CSV-compatible fields.
- For cold emails, generate drafts for human review. Do not auto-send.

## Workflow

1. Parse the user request:
   - product
   - English product keywords
   - target countries/regions
   - target lead count
   - customer types
   - decision-maker roles
   - strictness: standard or strict

2. If the user provides a product image:
   - Identify product category, material, likely use cases, visible features, and buyer channels.
   - Produce a product interpretation table before searching.
   - Convert the image into English search keywords.
   - Use visual uncertainty labels: confirmed, likely, unclear.
   - Ask one clarification only if product or market is still unclear.

3. Build target customer profile:
   - importers
   - wholesalers
   - distributors
   - retailers
   - e-commerce sellers
   - supermarket suppliers
   - hotel/hospitality suppliers
   - promotional gift companies
   - engineering/project buyers
   - overseas companies sourcing from China

4. Generate search queries:
   - product + importer + country
   - product + distributor + country
   - product + wholesaler + country
   - product + buyer/procurement + country
   - product + official website contact
   - product + vendor OR supplier OR procurement
   - product + wholesale directory
   - product + exhibitor OR trade show
   - site:linkedin.com/company + product + country + importer/distributor
   - product + "Purchasing Manager OR Procurement Manager OR Sourcing Manager" + email + WhatsApp

5. Research candidates:
   - Prefer official websites, contact pages, B2B directories, exhibitor pages, and public company pages.
   - Open and inspect source pages when browsing is available.
   - Extract evidence and note unknowns clearly.

6. Extract lead fields:
   - companyName
   - country/city
   - customerType
   - website
   - sourceUrl
   - publicSocialLinks
   - decisionMaker
   - title
   - email
   - WhatsApp
   - phone
   - contactForm
   - products/categories
   - matchScore
   - matchReason
   - customerAnalysis
   - outreachAngle
   - riskNotes
   - status
   - nextAction

7. Qualify and deduplicate:
   - Deduplicate by domain, normalized company name, email, WhatsApp, phone, and contact page URL.
   - Score 0-100 using product fit, customer type fit, market fit, contact completeness, and source credibility.
   - Formal lead requires source, relevance, and usable contact evidence.
   - Strict formal lead requires purchasing/decision email plus WhatsApp.
   - Before final output, run the QA checklist below.

8. Generate outreach when requested:
   - Use the customer table plus the user's product info.
   - Generate one personalized email per customer.
   - Do not invent certifications, capacity, prices, cases, or relationships.
   - Include a light unsubscribe sentence.
   - Output as a table.

## Product Image Analysis Output

When the user uploads an image, output this first:

| 识别项 | 结果 | 置信度 | 说明 |
|---|---|---|---|
| 产品类别 |  | confirmed/likely/unclear |  |
| 英文关键词 |  | confirmed/likely/unclear |  |
| 材质/工艺 |  | confirmed/likely/unclear |  |
| 使用场景 |  | confirmed/likely/unclear |  |
| 目标买家 |  | confirmed/likely/unclear |  |
| 推荐国家/地区 |  | confirmed/likely/unclear |  |

Then continue with search planning and lead output.

## Evidence Chain

Each formal lead must include:

| Evidence Item | Requirement |
|---|---|
| Source URL | Public, clickable, and relevant |
| Company evidence | Website, directory, exhibitor page, registry, or public company social page |
| Contact evidence | Source page or URL where email/WhatsApp/phone/contact form was found |
| Buyer-fit evidence | Product/category/business clue showing possible fit |
| Unknowns | Mark uncertain information as 未确认 |

Do not hide weak evidence. If a source only proves the company exists but not buyer fit, mark it as `待验证候选`.

## QA Checklist Before Output

Before returning final leads, internally check every row:

| Check | Pass Criteria |
|---|---|
| Real company | Has public source URL |
| Buyer fit | Matches product/customer type |
| Contact channel | Has email/WhatsApp/phone/contact form |
| Strict mode | Has purchasing/decision email AND WhatsApp |
| Dedup | Domain/company/email/WhatsApp/phone not repeated |
| Evidence | Source link supports the claim |
| Score | Formal lead score >= 60 |
| Risk | Missing or uncertain fields are marked |

If a row fails strict mode, do not call it `正式线索`.

## Default Output: Lead Table

Use this table for lead research:

| 序号 | 公司名称 | 国家/城市 | 客户类型 | 官网 | 来源链接 | 公开社媒 | 关键联系人 | 职位 | 邮箱 | WhatsApp | 电话 | 联系表单 | 主营产品 | AI匹配分 | 匹配理由 | 客户分析 | 推荐开发角度 | 风险提示 | 状态 | 下一步 |
|---:|---|---|---|---|---|---|---|---|---|---|---|---|---|---:|---|---|---|---|---|---|

Status values:
- 正式线索
- 待验证候选
- 不达标跳过
- 重复已跳过

## CSV-Compatible Fields

When the user asks to save, export, or paste into a spreadsheet, also provide:

```csv
index,company_name,country_city,customer_type,website,source_url,public_social_links,decision_maker,title,email,whatsapp,phone,contact_form,main_products,match_score,match_reason,customer_analysis,outreach_angle,risk_notes,status,next_action
```

## Default Output: Cold Email Table

Use this table for batch personalized outreach:

| 序号 | 公司名称 | 联系人 | 邮箱 | 邮件主题 | 邮件正文 | 个性化依据 | 风险提示 | 推荐发送时间 | 状态 |
|---:|---|---|---|---|---|---|---|---|---|

For more than 20 contacts, split into batches:

- Batch 1: rows 1-20
- Batch 2: rows 21-40
- Continue until done

For 100 contacts, generate email drafts in 5 batches of 20 unless the user asks for a different size.

## Cold Email Rules

- If a real contact name exists, use it.
- If only a purchasing role email exists, use "Hi Purchasing Team".
- If only a general email exists, use "Hi Team".
- If there is no email but WhatsApp exists, do not write an email; suggest WhatsApp outreach.
- Keep the email concise, specific, and natural.
- Mention only verified facts from source links or user-provided product information.
- Do not say "I saw you are looking for suppliers" unless the source actually says that.
- Include a soft CTA: catalog, quote, sample, or short intro.
- Include unsubscribe copy: "If this is not relevant, just let me know and I will not follow up."

## Batch Outreach QA

Before outputting emails, check:

| Check | Pass Criteria |
|---|---|
| Recipient exists | Row has valid email |
| Greeting safe | Does not invent name |
| Personalization | Uses verified company/product context |
| No fake claims | No invented certifications, capacity, cases, prices |
| CTA | Clear low-friction next step |
| Compliance | Includes unsubscribe line |

If no email exists, output status `不生成邮件，建议WhatsApp/电话触达`.

## When Data Is Weak

If no verifiable source exists, do not return a formal lead. Use:

| 公司名称 | 来源链接 | 已确认信息 | 缺失信息 | 为什么暂不入正式线索 | 建议下一步 |
|---|---|---|---|---|---|

## Useful References

- For search patterns, read `references/search-keyword-patterns.md`.
- For qualification rules, read `references/qualification-rules.md`.
- For outreach style, read `references/outreach-email-rules.md`.
- For compliance limits, read `references/compliance-rules.md`.
- For table templates, use files in `templates/`.
