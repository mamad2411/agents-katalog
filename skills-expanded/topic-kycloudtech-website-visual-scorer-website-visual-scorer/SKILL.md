---
name: website-visual-scorer
description: |
  Evaluate and score any website's visual design quality across 5 dimensions for B2B lead generation effectiveness. Use this skill whenever the user wants to audit, review, score, grade, or evaluate a website's design, visual quality, conversion potential, or compare websites. Triggers on: "评测网站", "评分", "audit this site", "score this website", "evaluate the design of", "compare these sites", "交付前检查", "客户网站评估", or any URL provided alongside words like evaluate/review/score/analyze. Also use when clients are pushing for subjective design changes — generate a score report to ground the conversation in data.

  This skill fetches the target URL, analyzes page structure and content, scores across 5 weighted dimensions (Visual Hierarchy 25pt, Brand Consistency 20pt, Conversion Guidance 25pt, Readability 20pt, Performance Perception 10pt), and outputs a structured 100-point score with actionable findings. For B2B manufacturing, export, and tech sites targeting global inquiries.
---

# Website Visual Scorer Skill

## Purpose
Produce a structured 100-point visual quality score for any B2B website, grounded in conversion-focused criteria. Use the score to manage client expectations, prevent unnecessary revisions, and benchmark against industry peers.

## When to Use
- Client asks for website evaluation or design review
- Before delivering a built site (pre-delivery QA)
- Client is pushing subjective revisions — use the score to redirect to data
- Comparing a client's site against competitors
- Any URL is mentioned alongside evaluation intent

---

## Execution Protocol

### Step 1 — Fetch the page
Use `web_fetch` with `html_extraction_method: markdown` and `text_content_token_limit: 8000`.

If the page returns an error (403/415/timeout), fall back to `web_search` for the domain to retrieve cached content, homepage description, and visible text. Note the limitation in the report.

### Step 2 — Extract signals
From the fetched content, identify:

**Structure signals**
- H1 text and length (ideal: ≤15 words)
- H2/H3 hierarchy presence
- CTA button text and count (first-screen, mid-page, bottom)
- Navigation depth (levels of dropdown)
- Footer contact info completeness

**Trust signals**
- Certifications mentioned (ISO/CE/SGS etc.)
- Client counts or years in business
- Named customer logos or case studies
- WhatsApp / direct contact links

**Content quality signals**
- Placeholder text present? ("Lorem ipsum" = immediate flag)
- Image filenames visible in src attributes (AI-generated names like "Gemini_Generated_Image" = flag)
- Brand name conflicts (certification images from a different company)
- Spelling/grammar errors in visible text
- Chinese text appearing in an English-targeted page (internationalization failure)

**Technical signals**
- Image formats (.webp = good, .jpg/.png only = flag)
- Video autoplay on hero (large file risk)
- Multiple conflicting logo files
- JS-dependent content showing as "0" or raw character strings

### Step 3 — Score each dimension
Read the scoring rubric from `references/scoring-rubric.md` for exact criteria per item.

Score each of the 20 sub-items from 1–10, then apply dimension weights:

| Dimension | Items | Max | Weight |
|-----------|-------|-----|--------|
| Visual Hierarchy | 5 items | 50 raw → 25pt | 25% |
| Brand Consistency | 4 items | 40 raw → 20pt | 20% |
| Conversion Guidance | 5 items | 50 raw → 25pt | 25% |
| Readability | 4 items | 40 raw → 20pt | 20% |
| Performance Perception | 2 items | 20 raw → 10pt | 10% |

Dimension score = (sum of raw scores / max raw) × dimension max points

Total = sum of all 5 dimension scores (out of 100)

### Step 4 — Classify findings
Sort all findings into three tiers:

- **🚨 Block** — Must fix before delivery or launch. Examples: wrong brand's certification, Lorem ipsum, AI image filename exposed, broken CTA links, critical spelling errors in navigation
- **⚠️ Improve** — Should fix to improve conversion. Examples: missing trust band near CTA, vague hero headline, no WhatsApp link, deep nav hierarchy
- **✓ Keep** — Strengths to preserve and replicate. Examples: correct webp usage, good FAQ structure, precise value proposition, industry-appropriate color tone

### Step 5 — Output the report
Use the interactive widget format (show_widget) when in claude.ai. Otherwise output structured markdown.

**Required report sections:**
1. Score summary (total + 5 dimension bars)
2. Verdict label:
   - 85–100: 优秀 — 建议上线
   - 70–84: 良好 — 可小幅优化后上线
   - 55–69: 待改进 — 需专项优化
   - <55: 重构级 — 不建议现状交付
3. Per-dimension breakdown with sub-item scores and reasoning
4. Findings by tier (Block / Improve / Keep)
5. If comparison requested: side-by-side dimension table

**Tone:** Direct and evidence-based. Reference specific page elements (exact headline text, image filename, nav label) rather than vague generalizations. Findings should be actionable within 1 working day.

---

## Industry Context
Adjust scoring emphasis based on detected industry:

| Industry | Key emphasis |
|----------|-------------|
| Manufacturing / Industrial B2B | Trust signals (certs, factory photos), technical spec clarity, WhatsApp |
| SaaS / Tech | CTA clarity, trial/demo flow, social proof, performance |
| Export / Trade | Multi-language handling, contact accessibility, product catalog link |
| Retail / Consumer | Visual polish, mobile CTA, brand differentiation |

If industry is unclear from content, default to Manufacturing B2B emphasis.

---

## Comparison Mode
If user provides 2+ URLs, score each independently then output:
- Side-by-side dimension score table
- Delta column (+ / − vs benchmark)
- Ranked leaderboard
- Cross-site best practices (what site A does well that site B should copy)

---

## Red Flags (auto-escalate to Block tier)
These findings always become Block regardless of overall score:

1. `Lorem ipsum` anywhere on page
2. Image filename contains `Gemini_Generated_Image`, `DALL-E`, `Midjourney`, or similar AI tool names
3. Certification image filename or alt text references a **different company name** than the site being evaluated
4. Navigation menu contains spelling errors
5. Primary CTA button links to `#` (dead link)
6. Chinese/non-target-language alt text on English-targeted pages when the text reveals untranslated source content

---

## Cost Guidance (for reference)
Approximate API cost per evaluation using Claude Sonnet 4.6:
- Input: ~3,000–5,000 tokens (page content + skill prompt)
- Output: ~1,500–2,500 tokens (full report)
- Total cost: ~$0.02–0.05 per evaluation at standard rates
- With prompt caching on the skill system prompt: ~$0.01–0.03 per evaluation

---

## Reference Files
- `references/scoring-rubric.md` — Full per-item scoring criteria with examples for each score band (1–3 / 4–6 / 7–10)
- `references/industry-benchmarks.md` — Average scores by industry vertical for comparison context
