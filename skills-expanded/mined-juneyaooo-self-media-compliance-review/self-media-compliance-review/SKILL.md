---
name: self-media-compliance-review
description: "Use when auditing self-media videos, scripts, covers, subtitles, voiceover, product links, account copy, comments, articles, or publishing packages for platform violation risk; especially before final delivery or publishing after video production or clipping. Covers e-commerce product consistency, Qianchuan material quality, regulated qualifications, efficacy claims, prices, gifts, activities, and pre-selection risk across WeChat, Douyin, Kuaishou, Bilibili, Xiaohongshu, TikTok, and related platforms."
---

# Self-Media Compliance Review

## Core Rule

Run a risk-control review before public content is treated as final. This Skill
does not provide legal advice, decide for a platform, or guarantee approval.
Default to Chinese unless the user asks otherwise.

Missing evidence is `待核验`. Never invent rules, facts, qualifications,
authorizations, prices, provenance, or platform behavior. Do not return `Pass`
when any required audible or visible region remains unreviewed.

## Collect Inputs

Collect or infer:

- target platforms and publishing context;
- final video, script, subtitles, cover, title, caption, tags, comments, product
  link, CTA, and account copy;
- account identity, audience, content intent, source ownership, promotion status,
  and qualifications for regulated topics;
- reviewable evidence such as files, timecodes, frames, transcripts, screenshots,
  manifests, links, and authorization records.

Continue with available evidence when inputs are missing, but list every gap.

## Load Only Relevant References

Always apply the universal workflow below. Then read the matching platform file:

- 微信视频号: `references/wechat-channels.md`
- 微信公众号: `references/wechat-official-account.md`
- 抖音: `references/douyin.md`
- 快手: `references/kuaishou.md`
- B站: `references/bilibili.md`
- 小红书: `references/xiaohongshu.md`
- TikTok or unsupported platforms: universal workflow only; state that no
  dedicated local reference exists.

Read additional workflow references only when their conditions apply:

- A local or acquired video is being reviewed: read
  `references/video-review-workflow.md` and follow its evidence coverage gate.
- E-commerce, 带货、挂车、商品、SKU、千川、选品 or commercial promotion is
  involved: read `references/ecommerce-workflow.md` and its linked commerce
  rules, including `douyin-ecommerce.md`, `qianchuan-low-quality.md`,
  `ecommerce-claims.md`, and when relevant `cases/ecommerce-cases.md`.
- The user explicitly requests current cases or live search: read
  `references/live-evidence-workflow.md`. Live search is off by default.
  Channel tiers, first working tier wins: ① the agent's own computer use
  and ② the agent's built-in browser tools (browser use / MCP browser) —
  self-check the host and start directly, without asking again; ③
  `opencli`, first option of the ask-the-user step, and ④ TikHub (paid
  REST API; explicit consent before spending); ⑤ MediaCrawler
  (`tools/mediacrawler_search.py`) only when ①-④ are all unavailable —
  last resort, own logged-in account, flagged by platform anti-crawl in
  practice, bound by the frequency hard rules.
  The presence of a live-search channel is not authorization; search only
  when the user explicitly asks.
- A serious review or JSON handoff is needed: read
  `references/report-schema.md` and use the published schemas.
- Recent enforcement, creator discussion, account-status, or appeal context is
  relevant: read `references/recent-cases-2025-2026.md`, then the matching file
  under `references/cases/`.
- A remote URL, OCR/ASR, TikHub, Gemini, or another multimodal model is involved:
  read `references/video-evidence-integrity.md`.

For a new platform, add a focused `references/<platform>.md` with scope and
source date, severity and blockers, official category names, risky elements,
and remediation patterns. Keep catalogs out of this file.

## Local Evidence Search

Local static search may run automatically because it makes no network request
and does not require live-search permission.
Use `tools/search_local_evidence.py` for focused lookup across published
`references/**/*.md` and `docs/sources.md`. Never search developer-only
`local/` as installation evidence.

Cite repository path, line, heading, and source type. Call results `本地静态证据`.
No match means only that the shipped corpus has no lexical match; it does not
prove compliance or absence of platform cases.

## Review Workflow

1. Inventory every public and audible surface: video, first frame, cover, title,
   subtitles, voiceover, BGM, caption, stickers, comments, private-message
   prompts, product card, links, QR codes, and profile.
2. Identify intent and regulated domains early, including health, medical,
   finance, legal services, minors, news, fundraising, gambling, drugs, devices,
   health food, and special medical formula food.
3. Prepare traceable evidence. For video, use the dedicated workflow before
   assigning severity. For structured commerce data, run optional prechecks but
   confirm their 商品一致性审核 results against source evidence.
4. Run every universal risk area below, then the selected platform and
   conditional references.
5. Separate official rules, regulatory sources, media reporting, creator
   discussion, automated signals, and reviewer observations.
6. Give each finding an exact evidence pointer, the matching rule or risk area,
   and a concrete fix. Record all unreviewed surfaces and missing proof.
7. Apply the final coverage gate before assigning the report-level result.

## Universal Risk Areas

- Rights and identity: copyright, low-effort reuse, third-party watermarks,
  portrait, name, reputation, privacy, trademark, patent, and authorization.
- Sexual or lowbrow material: nudity, body focus, sexual implication, sexual
  sound or text, sex jokes, and animal mating.
- Violence or discomfort: gore, injury, death, surgery, abuse, horror,
  excretions, dense holes or insects, and disturbing food or animals.
- Illegal or harmful conduct: gambling, pyramid schemes, controlled goods,
  illegal finance, fraud, fake cheating tools, dangerous stunts, and unsafe
  behavior involving minors.
- Marketing and commerce: absolutes, unverifiable data, fake authority,
  inconsistent products, prices, gifts, activities or links, nonofficial sales
  channels, excessive insertion, missing qualifications, and unsupported claims.
- Misinformation: old events presented as current, fabricated interviews,
  unknown-source stories, rumors, unlabeled synthetic incidents, and
  pseudoscience.
- Inducement and diversion: coercive engagement, fake benefits, incomplete
  episodes, off-platform traffic, contacts, QR codes, and private funnels.
- Public order and morals: discrimination, insults, sensationalized abnormal
  relationships, family abuse, and conduct that disrupts public order.
- Production quality: unreadable or wrong subtitles, bad aspect ratio, black
  screens, distortion, audio gaps, audio-video mismatch, and invalid links.

Sensitivity alone is not a finding. Identify the exact visible, audible, or
written element that creates the risk.

## Evidence Standard

Every finding needs at least one pointer: timecode or frame, transcript line,
cover/title/caption/comment/link text, screenshot description, or explicitly
missing proof. Cite official category IDs or policy names when available.

Maintain a source ledger for user material, platform metadata, downloaded media,
local observations, OCR/ASR, and model output. When sources disagree, explain
the mismatch and possible technical causes as `待核验`; do not choose a winner or
accuse anyone of manipulation without independent evidence.

Creator cases and comments may reveal enforcement symptoms, but they are not
binding rules. Optional live evidence belongs in its own section with provider,
search terms, content IDs, dates, and limitations.

## Severity

- `Blocker`: clear illegal or severe platform red line, major user safety or
  property risk, unqualified regulated marketing, porn, gambling, fraud,
  unmasked severe harm, obvious unauthorized reuse, or risky diversion.
- `High`: likely violation or strong enforcement risk; edit or add proof before
  publishing.
- `Medium`: ambiguous or context-dependent risk; revise, disclose, mask, or
  retain stronger evidence.
- `Low`: minor wording, UX, or production-quality risk.
- `Pass`: no material risk found in the evidence that was fully reviewed.

An unresolved `Blocker` or unaccepted `High` means the package is not ready.
If required audio, visuals, product details, qualifications, or authorization
were not reviewed, the conclusion cannot be `Pass`.

## Concrete Fixes

- Audio: mute or replace exact ranges and update matching subtitles or cards.
- Visual: cut, replace, crop, blur, or mask; keep risky frames off the cover and
  opening.
- Claims: remove absolutes and guarantees, add a verifiable source and context,
  disclose marketing, and align products, prices, gifts, specifications, and
  activities.
- Regulated topics: verify qualifications or remove prescriptive marketing and
  convert it to general, supportable information.
- Rights and privacy: replace unlicensed material; attribution alone does not
  cure unauthorized use.
- Diversion: remove coercive CTA, fake benefits, off-platform contacts, risky
  private-message funnels, and QR codes.

## Common Failure Modes

- Rewriting subtitles while risky speech remains audible.
- Reviewing only a script and missing cover, opening, visual, or BGM risks.
- Treating cross-platform public material as authorized or safe.
- Treating detail-page claims, OCR, ASR, or model output as verified facts.
- Calling sampled frames a full-frame review or assigning `Pass` from samples
  while audio or visual regions remain unreviewed.
- Hiding uncertain provenance, qualifications, product consistency, or failed
  media acquisition instead of marking it `待核验`.
- Running commerce review without the product-consistency and Qianchuan checks.

The Skill supports `发布前合规`, `选品前风险`, and `文案生成前风险`. Use
`references/ecommerce-workflow.md` for their distinct scopes and
`references/report-schema.md` for Markdown or machine-readable JSON output.
