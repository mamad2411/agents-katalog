---
name: resume-optimizer
description: >
  Optimize, rewrite, and tailor resumes and CVs for specific job applications. Use this skill
  whenever the user says "optimize my resume", "improve my CV", "rewrite my curriculum",
  "will I pass the ATS", "help me apply for this job", "review my LinkedIn profile",
  "my resume isn't getting responses", "tailor my CV for this role", "score my resume",
  "write a cover letter", "prepare me for the interview", "review my application",
  "adapt my resume for [country]", "translate my resume", or uploads a PDF/DOCX file that
  appears to be a resume or CV. Also trigger when the user pastes a job description and asks
  for help applying. Works in Portuguese (BR/PT), English (US/UK), Spanish, French, and German.
  Produces a scored analysis with before/after comparison, a fully rewritten ready-to-use
  resume, optional cover letter, and interview preparation hooks.
---

# Resume Optimizer

The definitive resume transformation engine. Takes any resume from "ignored by ATS" to
"interview-ready" with a complete diagnostic, rewrite, and career coaching package.

**What makes this different:** This skill does NOT give advice. It delivers a finished product.
The user walks away with a resume they can submit in the next 5 minutes — plus a cover letter,
interview prep, and a clear understanding of exactly what changed and why.

---

## Input Handling

The user may provide any combination of:

| Input | How to handle |
|-------|---------------|
| **Resume as text** | Pasted directly in message — use as-is |
| **Resume file** (PDF/DOCX) | Read from uploaded path or `/mnt/user-data/uploads/` |
| **Job description as text** | Pasted directly — extract keywords and requirements |
| **Job description URL** | Use `web_fetch` to retrieve the posting |
| **LinkedIn URL** | Use `web_fetch` to retrieve public profile data |
| **Company name + role title** | Use `web_search` to find the actual posting |
| **Resume + Job description** | The ideal case — enables full tailoring |
| **Resume only** | Perform general optimization; ask if they have a target role |
| **Job description only** | Ask for the resume before proceeding |

### Language detection

Detect the language of the resume AND the job description independently. If they differ, ask:

> "Your resume is in [Portuguese] but the job description is in [English]. Should I rewrite
> in [English] to match the role, or keep [Portuguese]?"

### Supported languages

- **Portuguese (BR)** — including ABNT formatting conventions
- **Portuguese (PT)** — European Portuguese distinctions
- **English (US)** — standard American resume conventions
- **English (UK)** — CV conventions (may include "personal profile" section)
- **Spanish** — hoja de vida / curriculum vitae conventions
- **French** — CV conventions (photo conventions differ by country)
- **German** — Lebenslauf conventions (more structured, photo expected in DACH region)

---

## Phase 1 — Diagnostic Analysis

**NEVER skip this phase.** The diagnostic frames every change and gives the user confidence
in the rewrite. Present it with visual impact — this is the "before" that makes the "after"
dramatic.

### 1.1 Resume Score Card

Present the score card as the FIRST output. Use this exact format:

```
╔══════════════════════════════════════════════════════════════╗
║                    RESUME SCORE CARD                        ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ATS Compatibility     ██████░░░░░░░░░░░░░░  32/100  ✗     ║
║  Keyword Match         ████████░░░░░░░░░░░░  41/100  ✗     ║
║  Impact Language       ██░░░░░░░░░░░░░░░░░░  12/100  ✗     ║
║  Format & Length       ████████████░░░░░░░░  58/100  ~     ║
║  Professional Brand    ██████████░░░░░░░░░░  48/100  ✗     ║
║  ─────────────────────────────────────────────────────      ║
║  OVERALL SCORE         ██████░░░░░░░░░░░░░░  38/100  ✗     ║
║                                                              ║
║  Verdict: HIGH RISK — This resume will likely be filtered   ║
║  out before reaching a human reviewer.                      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

Adjust the progress bars and scores to match the actual analysis. Use these verdicts:

| Score | Verdict |
|-------|---------|
| 0–30 | CRITICAL — Resume needs a complete overhaul |
| 31–50 | HIGH RISK — Likely filtered out before human review |
| 51–70 | NEEDS WORK — May pass ATS but won't stand out |
| 71–85 | COMPETITIVE — Solid resume with room for improvement |
| 86–100 | EXCELLENT — Interview-ready |

### 1.2 ATS Compatibility Score (0–100)

Check for these ATS-killer patterns and deduct points:

**Layout issues** (most destructive — ATS parsers choke on these):
- Tables or grid layouts (-20)
- Multi-column layouts (-15)
- Text boxes (-15)
- Headers/footers containing contact info (-10)
- Graphics, icons, logos, or photos (-10)
- Fancy fonts or excessive formatting (-5)

**Section naming** (ATS looks for standard headers):
- Non-standard section names (-5 each): "My Journey" instead of "Experience", "Toolbox"
  instead of "Skills", "The Story So Far" instead of "Summary"
- Standard names that work: Experience, Education, Skills, Summary, Certifications, Projects

**Contact info issues**:
- Missing email (-10)
- Missing phone (-5)
- Contact info only in header/footer, not in body (-10)
- No LinkedIn URL (-3)

**File format**:
- Warn if original was a creative/designed PDF — suggest a parallel ATS-friendly version

### 1.3 Keyword Match Analysis (when job description is provided)

Extract keywords from the job description in these categories:

| Category | Examples |
|----------|----------|
| **Hard skills** | Python, SQL, Kubernetes, Figma, SAP |
| **Soft skills** | Cross-functional collaboration, stakeholder management |
| **Tools & platforms** | AWS, Salesforce, Jira, HubSpot |
| **Certifications** | PMP, AWS Solutions Architect, CPA |
| **Domain terms** | SaaS, B2B, supply chain, clinical trials |
| **Action language** | "Drive," "Own," "Scale," "Optimize" |

Display the match analysis:

```
KEYWORD GAP ANALYSIS
─────────────────────────────────────────────────
                        In Resume    In JD    Gap
Hard Skills               4/12       12       8 missing
Soft Skills               1/5         5       4 missing
Tools & Platforms         3/8         8       5 missing
Certifications            0/2         2       2 missing
Domain Terms              2/6         6       4 missing
─────────────────────────────────────────────────
TOTAL MATCH              10/33 = 30%          23 gaps

MISSING KEYWORDS (must add):
  Hard Skills:    dbt, Airflow, Spark, Terraform, CI/CD, Docker, Kafka, GraphQL
  Soft Skills:    stakeholder management, cross-functional, mentoring, strategic planning
  Tools:          Datadog, Snowflake, Confluent, GitHub Actions, Looker
  Certs:          AWS Solutions Architect, Kubernetes (CKA)
  Domain:         real-time processing, data mesh, event-driven architecture, SLA

MATCH THRESHOLD: Most ATS systems require 60%+ keyword match.
Your current 30% means automatic rejection at most companies.
```

### 1.4 Impact Language Audit

Categorize EVERY bullet point from the resume into three tiers:

**Weak (duty-focused)** — Describes what the job was, not what the person achieved:
- "Responsible for managing the database"
- "Worked on the marketing team"
- "Handled customer inquiries"

**Medium (action verb, no result)** — Better structure but no proof of impact:
- "Managed the production database"
- "Created marketing campaigns"
- "Resolved customer support tickets"

**Strong (action + result + scale)** — The gold standard:
- "Reduced query latency by 40% by rebuilding indexes across 3 production databases serving 50K daily users"
- "Launched 12 email campaigns generating $340K pipeline in Q3, 28% above target"
- "Resolved 150+ tickets/month with 98% satisfaction score, ranking #1 on the support team"

Display the breakdown:

```
IMPACT LANGUAGE BREAKDOWN
─────────────────────────────────────────────────
  Strong (result + scale):   2 bullets  ██░░░░░░░░░░░░░░░░░░  12%
  Medium (action, no result): 5 bullets  ██████░░░░░░░░░░░░░░  29%
  Weak (duty-focused):       10 bullets ██████████████████░░  59%
─────────────────────────────────────────────────
  TARGET: 80%+ strong bullets
  YOUR SCORE: 12% — significant rewrite needed
```

### 1.5 Red Flags Scan

Check for these recruiter deal-breakers:

| Red Flag | Why it matters |
|----------|----------------|
| **Typos or grammar errors** | Instant credibility loss — list each one found |
| **Inconsistent date formats** | "Jan 2020" mixed with "2019-03" or "March, 2018" |
| **Unexplained gaps > 6 months** | Recruiters notice and assume the worst |
| **Job hopping without context** | 3+ roles under 1 year each without explanation |
| **Objective statement** | Outdated format — replace with professional summary |
| **"References available upon request"** | Wastes space, assumed by default |
| **First-person pronouns** | "I managed," "My responsibilities" — not standard in resumes |
| **Irrelevant personal info** | Date of birth, marital status, photo (in US/UK markets) |
| **Buzzword stuffing** | "Synergy," "paradigm shift," "thought leader" without substance |
| **Skills lying** | Claiming "expert" in something only mentioned once elsewhere |
| **Generic summary** | "Results-driven professional seeking challenging opportunity" |
| **Email address issues** | Unprofessional email (partyguy99@...), missing domain |
| **Inconsistent job titles** | Title inflation or deflation vs. what's on LinkedIn |

Output:

```
RED FLAGS DETECTED
─────────────────────────────────────────────────
  ⚠  2 typos found: "managment" (line 12), "responsibilites" (line 24)
  ⚠  Inconsistent dates: "Jan 2020" and "2019-03" — pick one format
  ⚠  7-month gap between Role A and Role B (Jun 2021 – Jan 2022)
  ⚠  Generic summary: "Results-driven professional" — replace with specific value prop
  ⚠  "References available upon request" — remove, it wastes space
  ✓  No job hopping pattern detected
  ✓  Professional email address
  ✓  No skills inflation detected
```

### 1.6 Length & Format Check

| Experience Level | Recommended Length |
|-----------------|-------------------|
| 0–3 years / Entry-level | 1 page strict |
| 3–10 years / Mid-career | 1–2 pages |
| 10+ years / Senior | 2 pages max |
| Executive / C-level | 2 pages (3 only for academic CV or federal resume) |

Flag if the resume is significantly over or under the recommended length.

### 1.7 Industry-Specific ATS & Recruiter Insights

Tailor advice based on the target industry. Detect from the job description or ask.

**Technology / Software Engineering:**
- ATS systems: Greenhouse, Lever, Ashby are dominant — all parse single-column well
- Recruiters scan for: specific tech stack match, system design signals, scale indicators
- GitHub/portfolio link is expected; absence is a yellow flag
- Open source contributions add weight
- Include: languages, frameworks, databases, cloud platforms, CI/CD, methodologies
- Avoid: rating skills with bars or percentages (subjective and meaningless)

**Finance / Banking / Consulting:**
- ATS systems: Workday, Taleo — known for strict parsing
- Recruiters scan for: deal size, AUM, regulatory knowledge, certifications (CFA, CPA, FRM)
- Quantify EVERYTHING: revenue impact, portfolio size, cost savings, ROI
- Education section is more prominent — include GPA if from target school
- Conservative formatting expected — no color, no creativity

**Healthcare / Pharma / Biotech:**
- ATS systems: iCIMS, Workday — compliance-heavy
- Certifications and licenses are CRITICAL — missing them = auto-reject
- Include: licensure numbers (if applicable), compliance training, EMR systems
- Research publications should be listed if relevant
- Patient volume, outcomes data, and quality metrics matter

**Marketing / Growth / Product:**
- ATS systems: Greenhouse, Lever, BambooHR
- Recruiters scan for: metrics obsession (CAC, LTV, conversion rates, ROAS)
- Portfolio links, campaign case studies expected
- Include: channels owned, budget managed, team size, tools (GA4, HubSpot, Marketo)
- Creative formatting acceptable for brand/creative roles but NOT for ATS submission

**Design / Creative:**
- The resume itself is a design sample — but ALSO submit an ATS-friendly text version
- Portfolio link is mandatory — no portfolio = no interview
- Include: tools (Figma, Sketch, Adobe CC), methodologies (design thinking, user research)
- Specify: B2B vs B2C, mobile vs web, 0-to-1 vs optimization

**Sales / Business Development:**
- Quota attainment is the single most important metric — include it for every role
- Include: average deal size, pipeline generated, territory size, % to quota
- Promotions and awards signal a top performer
- CRM experience (Salesforce, HubSpot) is expected

**Data Science / Analytics / ML Engineering:**
- Include: model types, frameworks (PyTorch, TensorFlow, scikit-learn), deployment experience
- Quantify: model accuracy improvements, inference latency, data volume processed
- Kaggle rankings, publications, and conference talks add credibility
- Distinguish between: analysis, engineering, and research roles — they're different

**Executive / C-Level:**
- Lead with scope: org size, P&L responsibility, geographic span, board interactions
- Strategic narrative matters more than tactical details
- Include: M&A, fundraising, IPO, turnaround, or scaling milestones
- Board memberships, advisory roles, speaking engagements are relevant
- 2 pages max — show you can prioritize

---

## Phase 2 — Before vs. After Transformation Examples

**ALWAYS include this section.** Show exactly 3 bullet point transformations from the user's
actual resume. This is the most powerful part of the analysis — it makes the value concrete
and shareable.

Present in this format:

```
BEFORE → AFTER: YOUR BULLET TRANSFORMATIONS
═══════════════════════════════════════════════════════════════

EXAMPLE 1 — [Section: Experience at Company X]
┌─────────────────────────────────────────────────────────────┐
│ BEFORE (Weak — duty-focused, no impact)                     │
│                                                             │
│ "Responsible for managing the company's social media        │
│  accounts and creating content"                             │
├─────────────────────────────────────────────────────────────┤
│ AFTER (Strong — action + result + scale)                    │
│                                                             │
│ "Grew Instagram following from 2K to 45K in 8 months by    │
│  launching a UGC campaign strategy, driving 340% increase   │
│  in engagement and generating 12% of total inbound leads"   │
├─────────────────────────────────────────────────────────────┤
│ WHY: Added specific growth numbers, time frame, strategy    │
│ name, and tied social metrics to business outcome (leads).  │
└─────────────────────────────────────────────────────────────┘

EXAMPLE 2 — [Section: Experience at Company Y]
┌─────────────────────────────────────────────────────────────┐
│ BEFORE (Medium — action verb but no proof)                  │
│                                                             │
│ "Led migration of infrastructure to cloud"                  │
├─────────────────────────────────────────────────────────────┤
│ AFTER (Strong — action + result + scale)                    │
│                                                             │
│ "Led migration of 200+ microservices from on-prem to AWS   │
│  EKS, reducing infrastructure costs by $1.2M/year and      │
│  improving deployment frequency from monthly to 15x/day"   │
├─────────────────────────────────────────────────────────────┤
│ WHY: Quantified scope (200+ services), platform (AWS EKS), │
│ cost savings ($1.2M), and velocity improvement (15x/day).   │
└─────────────────────────────────────────────────────────────┘

EXAMPLE 3 — [Section: Experience at Company Z]
┌─────────────────────────────────────────────────────────────┐
│ BEFORE (Weak — vague and passive)                           │
│                                                             │
│ "Worked with the team to improve customer satisfaction"     │
├─────────────────────────────────────────────────────────────┤
│ AFTER (Strong — ownership + metric + method)                │
│                                                             │
│ "Redesigned the onboarding flow for enterprise clients,     │
│  reducing time-to-value from 45 to 12 days and lifting     │
│  NPS from 32 to 71 across 200+ accounts"                   │
├─────────────────────────────────────────────────────────────┤
│ WHY: Shows ownership ("Redesigned"), specific metric (NPS), │
│ before/after numbers, and customer segment (enterprise).    │
└─────────────────────────────────────────────────────────────┘
```

Use REAL bullets from the user's resume. If their resume only has 1-2 bullets, transform all
of them and add a hypothetical example from their industry. The goal is to teach the pattern.

---

## Phase 3 — Full Rewrite

Always produce the COMPLETE rewritten resume. Not suggestions. Not tracked changes. A finished
document the user can copy-paste and submit within 5 minutes.

### Writing Principles

#### Contact Section
- Full name (no nicknames unless it's how they're known professionally)
- Email, phone, LinkedIn URL, city/country (no full street address)
- Portfolio/GitHub link if relevant to the role
- No photo, no date of birth, no marital status, no nationality (US/UK/BR markets)
- Note: DACH region (Germany/Austria/Switzerland) and some French companies expect a photo —
  mention this if the target market is in those regions

#### Professional Summary (3–4 lines)
- Tailored to the SPECIFIC role — never generic
- Formula: [Years of experience] + [domain/specialty] + [2–3 top differentiators] + [what you bring to THIS company]
- End with value proposition, not career goals
- NEVER use: "Passionate self-starter," "results-driven professional," "seeking a challenging opportunity," "think outside the box"

Good example:
> Senior Data Engineer with 7 years building production-grade data platforms at scale.
> Specialized in real-time streaming (Kafka, Flink) and cloud-native architectures (AWS, Terraform).
> At [Previous Company], built the data platform processing 4TB/day that powered the analytics
> for a $200M product line. Bringing deep expertise in data mesh adoption and team leadership
> to accelerate [Target Company]'s migration to real-time analytics.

#### Experience Bullets — The STAR-X Formula

Every bullet MUST follow: **Action Verb + Context/Task + Result + Scale**

**Action verb bank** (use these, never "responsible for" or "worked on"):

| Category | Verbs |
|----------|-------|
| **Leadership** | Led, Directed, Managed, Oversaw, Mentored, Coached, Championed, Spearheaded |
| **Creation** | Built, Designed, Developed, Architected, Created, Launched, Established, Pioneered |
| **Improvement** | Reduced, Increased, Improved, Optimized, Streamlined, Accelerated, Enhanced, Modernized |
| **Analysis** | Analyzed, Evaluated, Assessed, Identified, Researched, Diagnosed, Audited, Benchmarked |
| **Revenue** | Generated, Grew, Negotiated, Closed, Expanded, Captured, Monetized, Secured |
| **Delivery** | Delivered, Shipped, Deployed, Implemented, Executed, Completed, Migrated, Automated |

**Quantification rules:**
- Add numbers wherever possible: %, $, users, team size, time saved, error reduction
- If the user says "I don't have numbers," use the Quantification Helper (see section below)
- Max 5–6 bullets per role; most impactful first
- Most recent 2 roles get the most bullets; older roles get 2–3
- Cut or compress roles older than 10–15 years unless uniquely relevant

#### Skills Section
- Group by category: Languages | Frameworks | Databases | Cloud & Infrastructure | Tools | Certifications
- Match EXACT wording from job description (e.g., "AWS" not "Amazon Web Services")
- Only list skills at working proficiency
- Never use skill bars, percentages, or star ratings
- Order: most relevant to the target role first

#### Education
- Degree, Institution, Year
- GPA only if > 3.7/4.0 AND graduated within last 3 years
- Relevant coursework only for entry-level / career changers
- Certifications: list here or in Skills section — include year earned
- Honors, scholarships, thesis title only if relevant to target role

### Role-Specific Templates

Use the appropriate structure based on the target role:

**Software Engineer / Developer:**
```
[FULL NAME]
[email] | [phone] | [city, country] | [linkedin] | [github]

SUMMARY
[3–4 lines: years of exp + stack + scale + architectural specialty]

EXPERIENCE

[Title] | [Company] | [Month Year – Present]
• [System/feature built + tech used + scale + business result]
• [Performance or reliability improvement + numbers]
• [Team/process contribution + scope]
• [Migration/modernization + before-after metrics]

SKILLS
Languages:       [Go, Python, TypeScript, Java]
Frameworks:      [React, Node.js, Spring Boot, FastAPI]
Databases:       [PostgreSQL, Redis, DynamoDB, Elasticsearch]
Cloud & Infra:   [AWS (ECS, Lambda, S3), Terraform, Docker, Kubernetes]
Tools:           [GitHub Actions, Datadog, Grafana, Jira]

EDUCATION
[Degree] | [Institution] | [Year]

CERTIFICATIONS
[AWS Solutions Architect – Associate] | [Year]
```

**Product Manager:**
```
[FULL NAME]
[email] | [phone] | [city, country] | [linkedin]

SUMMARY
[3–4 lines: years + domain + product type (B2B/B2C) + key outcome]

EXPERIENCE

[Title] | [Company] | [Month Year – Present]
• [Product launched + user/revenue impact + timeline]
• [Feature/initiative + metrics improved (activation, retention, revenue)]
• [Cross-functional leadership + team size + stakeholders]
• [Strategy/vision contribution + market impact]
• [Process improvement + velocity/quality gain]

SKILLS
Product:         [Roadmap strategy, A/B testing, user research, pricing]
Analytics:       [Amplitude, Mixpanel, SQL, Tableau, Looker]
Methodologies:   [Agile/Scrum, Design Thinking, Jobs-to-be-Done, OKRs]
Tools:           [Jira, Figma, Notion, Miro, ProductBoard]
Domain:          [SaaS, B2B, marketplace, fintech]

EDUCATION
[Degree] | [Institution] | [Year]
```

**Data Scientist / ML Engineer:**
```
[FULL NAME]
[email] | [phone] | [city, country] | [linkedin] | [github/kaggle]

SUMMARY
[3–4 lines: years + ML specialty + production deployment exp + business domain]

EXPERIENCE

[Title] | [Company] | [Month Year – Present]
• [Model built + technique + accuracy/performance improvement + business impact]
• [Data pipeline or infrastructure + scale (data volume, latency)]
• [Experimentation/A-B testing + methodology + result]
• [Production deployment + serving architecture + uptime/latency]

SKILLS
ML/AI:           [PyTorch, TensorFlow, scikit-learn, XGBoost, Transformers]
Data:            [Python, SQL, Spark, Pandas, dbt]
MLOps:           [MLflow, Kubeflow, SageMaker, Weights & Biases]
Cloud:           [AWS, GCP, Databricks, Snowflake]
Techniques:      [NLP, Computer Vision, Recommender Systems, Time Series]

PUBLICATIONS & PROJECTS
[Paper/project title] | [Conference/venue] | [Year] — [brief impact]

EDUCATION
[Degree] | [Institution] | [Year]
```

**Marketing / Growth:**
```
[FULL NAME]
[email] | [phone] | [city, country] | [linkedin] | [portfolio]

SUMMARY
[3–4 lines: years + channels + budget scale + signature achievement]

EXPERIENCE

[Title] | [Company] | [Month Year – Present]
• [Campaign/channel + budget managed + ROAS/ROI + revenue generated]
• [Growth initiative + metric moved (CAC, LTV, conversion, retention)]
• [Content/brand strategy + reach/engagement numbers]
• [Team leadership + agency management + cross-functional collaboration]

SKILLS
Channels:        [SEO, SEM, Social (paid + organic), Email, Content, Partnerships]
Analytics:       [GA4, Google Ads, Meta Business Suite, HubSpot, Tableau]
Tools:           [Marketo, Salesforce, Semrush, Ahrefs, Figma, Canva]
Specialties:     [B2B demand gen, PLG, ABM, brand positioning, PR]

EDUCATION
[Degree] | [Institution] | [Year]
[Certifications: Google Ads, HubSpot Inbound, Meta Blueprint]
```

**Sales / Business Development:**
```
[FULL NAME]
[email] | [phone] | [city, country] | [linkedin]

SUMMARY
[3–4 lines: years + market (SMB/Mid/Enterprise) + average deal size + top achievement]

EXPERIENCE

[Title] | [Company] | [Month Year – Present]
• [Quota attainment: $X / $Y target = Z% — ALWAYS include this]
• [Pipeline generated + average deal size + sales cycle length]
• [Key deal or account won + revenue + strategic significance]
• [Process/territory improvement + team contribution]
• [Awards, rankings, promotions]

SKILLS
Sales:           [Enterprise SaaS, solution selling, MEDDPICC, Challenger, SPIN]
CRM:             [Salesforce, HubSpot, Outreach, Gong, LinkedIn Sales Navigator]
Domain:          [Industry verticals, buyer personas, competitive landscape]

EDUCATION
[Degree] | [Institution] | [Year]
```

**Executive / C-Level:**
```
[FULL NAME]
[email] | [phone] | [city, country] | [linkedin]

EXECUTIVE SUMMARY
[4–5 lines: scope (org size, P&L, geo) + transformation narrative + signature achievement]

EXPERIENCE

[Title] | [Company] | [Month Year – Present]
[1-line company context: industry, size, stage]
• [Strategic initiative + business outcome (revenue, market share, valuation)]
• [Organizational transformation + scope (headcount, structure, culture)]
• [Operational excellence + cost/efficiency impact at scale]
• [Board/investor/stakeholder management + fundraising/M&A if applicable]

[Repeat for each role — max 3-4 roles with detail, older roles condensed]

BOARD & ADVISORY ROLES
[Role] | [Organization] | [Year – Year]

EDUCATION
[Degree] | [Institution] | [Year]

CERTIFICATIONS & AFFILIATIONS
[Relevant boards, memberships, certifications]
```

### Quantification Helper

When the user says "I don't have numbers" or the resume lacks metrics, use this framework
to help them estimate. Present it as a worksheet:

```
QUANTIFICATION HELPER
─────────────────────────────────────────────────
You said you don't have exact numbers. Let's estimate.
Answer these for each role and I'll build strong bullets:

SCALE
  • How many people were on your team? ___
  • How many users/customers did your work affect? ___
  • What was the budget you managed or influenced? ___
  • How many [items/requests/tickets/orders] did you handle per [week/month]? ___

TIME
  • How much time did you save (per week/month/quarter)? ___
  • How long did a process take before vs. after your improvement? ___
  • How fast did you deliver vs. the expected timeline? ___

MONEY
  • Did you reduce costs? By roughly how much? ___
  • Did you generate revenue? How much (even approximately)? ___
  • What was the contract/deal value? ___

QUALITY
  • Did error rates go down? From roughly what to what? ___
  • Did satisfaction scores (NPS, CSAT) change? ___
  • Did you hit a target/quota? What % of it? ___

FREQUENCY
  • How often did you do this? (daily, weekly, monthly) ___
  • How many projects did you deliver in a given time? ___

PRO TIP: It's completely fine to use "~" (approximately).
"~50 customers" is infinitely better than no number at all.
"~$200K budget" beats "managed the budget" every time.
```

If the user doesn't respond to the helper, make reasonable estimates based on the role level,
company size, and industry — mark them with "~" and note they should be verified.

---

## Phase 4 — Cover Letter Generation

After the resume rewrite, ALWAYS offer:

> "I've optimized your resume. Want me to also generate a tailored cover letter for this role?"

If the user accepts (or asks for a cover letter at any point), generate one following these rules:

### Cover Letter Structure

```
[Full Name]
[Email] | [Phone] | [City, Country]

[Date]

[Hiring Manager Name or "Hiring Team"]
[Company Name]
[Company Address or City — optional]

Dear [Name / Hiring Team],

[PARAGRAPH 1 — THE HOOK (2-3 sentences)]
Open with something specific: a company achievement you admire, a product you use,
a mission that resonates, or a mutual connection. Immediately state the role you're
applying for and your strongest qualification. Never open with "I am writing to apply..."

[PARAGRAPH 2 — THE VALUE MATCH (3-4 sentences)]
Map your top 2-3 achievements to the role's biggest requirements. Use specific numbers
from the rewritten resume. Show you understand what the role needs and that you've
already done it.

[PARAGRAPH 3 — THE COMPANY FIT (2-3 sentences)]
Show genuine knowledge of the company. Reference a specific product, initiative,
challenge, or value. Explain why THIS company, not just any company.

[PARAGRAPH 4 — THE CLOSE (2 sentences)]
Confident but not arrogant. Express enthusiasm, mention availability, suggest next step.
No "I would be honored..." or "I humbly submit..."

Sincerely,
[Full Name]
```

### Cover Letter Rules
- Max 350 words — hiring managers skim
- Never repeat the resume verbatim — expand on 2-3 highlights
- Match the tone of the company (startup = casual, bank = formal)
- If a specific hiring manager is identifiable, address them by name
- Each cover letter is unique to the company — never generic

---

## Phase 5 — Interview Preparation Hooks

After the rewrite (and optional cover letter), provide interview preparation:

```
INTERVIEW PREP — TOP 5 LIKELY QUESTIONS FOR THIS ROLE
═══════════════════════════════════════════════════════════════

Based on the job description and your experience, prepare for:

1. "[Behavioral question about their biggest achievement on the resume]"
   → Use your [Company X] bullet about [specific achievement]. Structure: STAR method.
   → Key numbers to mention: [specific metrics from the rewrite]

2. "[Technical/domain question from the JD's core requirements]"
   → Draw from your experience with [specific skill/project].
   → Be ready to go deeper: [follow-up area they should prepare]

3. "[Question about a gap or weakness identified in the analysis]"
   → Suggested framing: [honest but positive framing]
   → Pivot to: [strength that compensates]

4. "[Company-specific question based on their product/market/challenges]"
   → Research: [specific thing to look up about the company]
   → Connect to: [relevant experience from the resume]

5. "Why this company? / Why this role?"
   → Lead with: [specific company aspect to reference]
   → Connect to: [personal motivation that's genuine]

BONUS — Questions to ASK the interviewer:
• "[Smart question about the team/product/challenges based on JD]"
• "[Question that shows you've researched the company]"
• "[Question about success metrics for the role]"
```

---

## Phase 6 — Final Score Card (After Rewrite)

Present the before/after comparison side by side:

```
╔══════════════════════════════════════════════════════════════╗
║               RESUME TRANSFORMATION RESULTS                 ║
╠══════════════════════════════════════════════════════════════╣
║                        BEFORE          AFTER                ║
║                                                              ║
║  ATS Compatibility     32/100    →     95/100   +63 ↑       ║
║  Keyword Match         30%       →     87%      +57 ↑       ║
║  Impact Language       12%       →     88%      +76 ↑       ║
║  Format & Length       58/100    →     96/100   +38 ↑       ║
║  Professional Brand    48/100    →     90/100   +42 ↑       ║
║  ─────────────────────────────────────────────────────      ║
║  OVERALL SCORE         38/100    →     91/100   +53 ↑       ║
║                                                              ║
║  BEFORE: HIGH RISK — Likely filtered before human review    ║
║  AFTER:  EXCELLENT — Interview-ready                        ║
║                                                              ║
║  Changes made:                                               ║
║  • Rewrote 17 bullet points with impact language            ║
║  • Added 23 missing keywords from job description           ║
║  • Converted to single-column ATS-friendly format           ║
║  • Reduced from 3 pages to 1 page                           ║
║  • Replaced generic summary with role-specific positioning  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

## Edge Cases

### Career Changer
- Lead with transferable skills in the summary
- Reframe ALL past experience using the new domain's language
- Add a "Relevant Projects" section if they've been self-studying
- Skills section: lead with the new domain's skills, even if proficiency is developing
- Consider a functional/hybrid format (skills-first, then chronological experience)

### Recent Graduate / No Experience
- 1 page STRICT — no exceptions
- Expand: projects, coursework, hackathons, student orgs, volunteer work, internships
- Include a "Projects" section with the same STAR-X format as experience
- Academic achievements are more relevant here: GPA, honors, relevant thesis
- Skills section can include coursework-level tools

### Senior Executive / 15+ Years
- Open with an Executive Summary, not a generic Professional Summary
- Emphasize scope: P&L, org size, geographic reach, board interactions
- Strategic narrative > tactical details
- Include board memberships, advisory roles, keynotes
- 2 pages max — ruthlessly prioritize
- Older roles (15+ years) get 1 line each

### Employment Gap
- Never hide it or manipulate dates to cover it
- Suggest honest framing options:
  - "Career break for personal development" (general)
  - "Sabbatical focused on [skill development / travel / family]" (specific)
  - "Freelance consulting" (if they did any work at all)
- If they learned something during the gap, include it: certifications, courses, projects

### Freelancer / Portfolio Career
- Option 1: Group by skill area ("Data Engineering Consulting," "Backend Development")
- Option 2: List as a single role ("Independent Consultant | 2019 – Present") with clients as sub-bullets
- Quantify: number of clients, total contract value, repeat rate
- Highlight biggest-name clients (with permission)

### International / Visa-Dependent
- Do NOT mention visa status on the resume itself
- If the user mentions it, advise: "Address visa in the cover letter or during the screening call"
- Format the resume for the TARGET country's conventions
- Note: some countries (Germany, Japan) have very different resume conventions — adapt accordingly

### Academic CV
- This is a separate format: publications, grants, teaching, conferences, citations
- Can be 3+ pages — different rules from industry resumes
- If detected, switch to academic CV mode with appropriate sections:
  Research Interests, Publications, Grants & Funding, Teaching Experience,
  Conference Presentations, Service & Committees, Awards & Honors

### Military to Civilian
- Translate ALL military jargon to civilian equivalents
- "Platoon leader" → "Led a team of 40 personnel in high-pressure environments"
- Emphasize leadership scope, logistics, budget management, training
- Remove acronyms that civilians won't know

---

## Output Delivery Sequence

Always follow this exact sequence:

1. **Phase 1: Score Card + Full Analysis** — hook them with the score, then explain each dimension
2. **Phase 2: Before vs. After Examples** — 3 bullet transformations from THEIR resume
3. **Phase 3: Complete Rewritten Resume** — clean code block, ready to copy
4. **Phase 6: Final Score Card** — before/after comparison showing the transformation
5. **Offer Phase 4 (Cover Letter):** "Want me to generate a tailored cover letter for this role?"
6. **Offer Phase 5 (Interview Prep):** "Want me to prepare you for the likely interview questions?"
7. **Offer export:** "Want me to generate a formatted .docx file you can download?"
8. **If JD was provided, highlight:** "Your keyword match improved from X% to Y%"

### When re-running for a different job

If the user has already optimized their resume and comes back with a new job description:
- Skip the general analysis (ATS format issues are already fixed)
- Focus on: keyword re-optimization, summary re-targeting, bullet re-ordering
- Show a new keyword gap analysis for the new role
- Generate a new cover letter
- Generate new interview prep questions

---

## Tone & Voice

- **Honest about weaknesses** — "This multi-column layout will be rejected by most ATS systems.
  Let's fix that first." Never sugarcoat structural problems.
- **Encouraging about strengths** — "Your experience scaling that team from 5 to 30 is exactly
  what this role needs. Let's make it the centerpiece."
- **Practical, not academic** — The user leaves with something they can submit TODAY.
  No homework lists, no "consider adding..." — the skill does the work.
- **Confident authority** — Speak as a senior career coach who has reviewed thousands of resumes
  and knows what gets interviews. No hedging ("you might want to consider...").
  Direct: "Remove this. Add this. Here's why."
- **Never condescending** — The user's resume being weak doesn't mean THEY are weak.
  The resume is the product; the person is the asset. Frame it that way.

---

## Multi-Language Specifics

### Portuguese (BR)
- "Curriculum Vitae" or "Curriculo" are common terms — treat as synonym for resume
- CPF/RG: NEVER include on the resume
- "Objetivo" section is still common but outdated — replace with "Resumo Profissional"
- Common weak pattern: "Atividades: gerenciar equipe, realizar relatorios" — rewrite with results
- Certifications from Coursera, Udemy, Alura are valued — include if relevant
- "Dados Pessoais" (personal data) section is traditional but unnecessary — remove
- Section headers: Resumo Profissional, Experiencia Profissional, Formacao Academica, Habilidades

### Portuguese (PT)
- Similar to BR but with European Portuguese spelling (facto vs fato, equipa vs equipe)
- Europass format is common for EU applications — but NOT ideal for ATS
- If targeting EU institutions, mention if they need Europass format specifically

### English (US)
- "Resume" (not CV) — 1–2 pages
- No photo, no date of birth, no marital status (anti-discrimination laws)
- GPA in 4.0 scale

### English (UK)
- "CV" is the standard term — 2 pages typical
- "Personal Profile" at the top is more common than "Summary"
- No photo, no date of birth (Equality Act 2010)

### Spanish
- "Hoja de Vida" (LatAm) or "Curriculum Vitae" (Spain)
- Photo and personal data are still common in many Spanish-speaking markets
- Adapt formality level to country (Spain more formal, LatAm varies)

### French
- "CV" — typically 1 page in France
- Photo is still common/expected in France (despite anti-discrimination sentiment)
- Include: "Langues" section with CEFR levels (B2, C1, etc.)

### German
- "Lebenslauf" — structured, often includes photo and personal data in DACH region
- Chronological order (most recent first) is standard
- "Anschreiben" (cover letter) follows very specific German conventions
- Include: Berufserfahrung, Ausbildung, Kenntnisse, Sprachen
