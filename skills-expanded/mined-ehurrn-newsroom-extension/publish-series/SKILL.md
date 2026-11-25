---
name: publish-series
description: "Coordinated deployment of multi-part investigative series. Sequential editorial gates (each article passes independently). Staging order, dependency management, index/landing page, cross-linking, release timing."
---

# Publish Series Skill

## Overview

Publish Series handles the coordinated deployment of **multi-part investigative series**, where articles are interdependent but must be published as a coordinated package.

**Key difference from Publish Article:** Series articles are **sequenced and gated independently**, but they're released together to maximize impact.

This skill ensures:

- **Sequential editorial gates** (each article approved independently)
- **Dependency management** (Article 2 can't go live if Article 1 has issues)
- **Landing page/index coordination** (series hub links all parts)
- **Cross-article linking** (readers navigate from part to part)
- **Coordinated release timing** (all articles published at agreed moment)
- **Archive protection** (intermediate drafts preserved; no data loss)

---

## Series Planning Phase

Before deployment, define the series structure:

### Series Definition Document

```yaml
series:
  title: "Procurement Breakdown: A 6-Month Investigation"
  slug: "procurement-breakdown"
  description: "How municipal contracts worth $5M went to a single vendor with no competitive bidding. An investigation into broken oversight."

articles:
  - article_id: 1
    title: "How One Vendor Got 94% of City Contracts"
    slug: "how-one-vendor-94-percent"
    publication_date: "2025-04-01 10:00 AM"
    status: "approved_for_publishing"
    wordcount: 2100
    dependencies: []  # First article; no dependencies

  - article_id: 2
    title: "City Council Ignored Its Own Procurement Rules"
    slug: "city-council-ignored-rules"
    publication_date: "2025-04-02 10:00 AM"
    status: "approved_for_publishing"
    wordcount: 1800
    dependencies: [1]  # Depends on Article 1 being live

  - article_id: 3
    title: "Where Is the Oversight? An Audit Trail Goes Missing"
    slug: "audit-trail-missing"
    publication_date: "2025-04-03 10:00 AM"
    status: "approved_for_publishing"
    wordcount: 2300
    dependencies: [1, 2]  # Depends on Articles 1 & 2

landing_page:
  title: "Procurement Breakdown Series"
  slug: "procurement-breakdown-series"
  description: "Read our full investigation into municipal procurement failures"
  featured_image: "images/series-hero.jpg"
  publication_date: "2025-04-01 09:30 AM"  # 30 min before first article

cross_linking:
  - article_id: 1
    teaser_for_2: "Next: How the city council ignored its own rules"
    teaser_for_3: "Coming tomorrow: Where did the audit trail go?"

  - article_id: 2
    teaser_for_3: "Read tomorrow: The missing audit trail"
    previous_link: "Part 1: How one vendor got 94% of contracts"

  - article_id: 3
    previous_link: "Part 2: City council ignored its own rules"
    series_link: "Read the full series"

publication_dates:
  landing_page: "2025-04-01 09:30 AM"
  article_1: "2025-04-01 10:00 AM"
  article_2: "2025-04-02 10:00 AM"
  article_3: "2025-04-03 10:00 AM"

social_strategy:
  day_1_hook: "We spent 6 months investigating. $5M in city contracts went to one vendor. Zero competitive bids. Here's how."
  day_2_teaser: "Part 2 tomorrow: Did city council deliberately ignore procurement rules? Documents suggest yes."
  day_3_teaser: "Final part: The missing audit trail reveals more unanswered questions."
```

---

## Editorial Gates (Sequential & Independent)

Each article must pass editorial review **independently**, but gates are **sequenced by publication order**:

### Article 1: Editorial Gate

**Timeline: 7 days before publication**

- [ ] **Final-editor-review complete** (libel check, fact-check, verification)
- [ ] **Copy-review complete** (readability, SEO, accessibility)
- [ ] **Social marketing hooks drafted** (3 options provided; editor chooses)
- [ ] **Images finalized** (1200×628px social card created)
- [ ] **Metadata complete:**
  - [ ] Meta title (50–60 chars)
  - [ ] Meta description (155–160 chars)
  - [ ] og:image (1200×628px)
  - [ ] Structured data (NewsArticle JSON-LD with series info)
  - [ ] Series canonical link: `<link rel="canonical" href="https://newsroom.org/articles/procurement-breakdown/part-1">`

- [ ] **Editor sign-off:** "Approved for publishing"

### Article 2: Editorial Gate

**Timeline: 1 day before publication**

- [ ] **Article 1 is live** (prerequisite; if Article 1 has issues, Article 2 is delayed)
- [ ] **Final-editor-review complete**
- [ ] **Copy-review complete**
- [ ] **Cross-reference to Article 1 verified** (links work, teasers accurate)
- [ ] **Metadata complete** (including series designation)
- [ ] **Editor sign-off:** "Approved for publishing"

### Article 3: Editorial Gate

**Timeline: 1 day before publication**

- [ ] **Articles 1 & 2 are live**
- [ ] **Final-editor-review complete**
- [ ] **Copy-review complete**
- [ ] **Cross-references verified** (links to Part 1 & Part 2 work; teasers accurate)
- [ ] **Metadata complete** (including series designation)
- [ ] **Editor sign-off:** "Approved for publishing"

---

## Landing Page (Series Hub)

The landing page is the **central hub** for the series. It publishes first and links all articles as they go live.

### Landing Page Structure

```html
<!DOCTYPE html>
<html>
<head>
  <title>Procurement Breakdown: A 6-Month Investigation</title>
  <meta name="description" content="How municipal contracts worth $5M went to a single vendor with no competitive bidding.">
  <meta property="og:title" content="Procurement Breakdown Series">
  <meta property="og:image" content="https://newsroom.org/images/series-hero.jpg">
  <meta property="og:url" content="https://newsroom.org/series/procurement-breakdown">
  <meta property="og:type" content="website">
</head>
<body>

  <header class="series-header">
    <h1>Procurement Breakdown</h1>
    <p class="subtitle">A 6-Month Investigation</p>
    <img src="images/series-hero.jpg" alt="Municipal building">
  </header>

  <section class="series-summary">
    <h2>What We Found</h2>
    <p>Our investigation reveals how municipal contracts worth $5M were awarded to a single vendor over four years with zero competitive bidding. We obtained internal documents, interviewed officials, and traced the decision-making process that bypassed procurement oversight.</p>
  </section>

  <section class="series-articles">
    <h2>Read the Series</h2>

    <article class="series-part">
      <h3>Part 1: How One Vendor Got 94% of City Contracts</h3>
      <p class="date">Published April 1, 2025</p>
      <p class="summary">We analyzed four years of municipal spending and found that one vendor dominated city contracts while others were barely solicited.</p>
      <a href="https://newsroom.org/articles/how-one-vendor-94-percent" class="read-more">Read Part 1</a>
    </article>

    <article class="series-part">
      <h3>Part 2: City Council Ignored Its Own Procurement Rules</h3>
      <p class="date">Published April 2, 2025</p>
      <p class="summary">City council procurement policy requires competitive bidding for contracts over $50K. Internal documents show the council deliberately bypassed this rule.</p>
      <a href="https://newsroom.org/articles/city-council-ignored-rules" class="read-more">Read Part 2</a>
    </article>

    <article class="series-part">
      <h3>Part 3: Where Is the Oversight? An Audit Trail Goes Missing</h3>
      <p class="date">Published April 3, 2025</p>
      <p class="summary">We requested audit records documenting the decision-making process. The city's response: records don't exist, can't be located, or were never created.</p>
      <a href="https://newsroom.org/articles/audit-trail-missing" class="read-more">Read Part 3</a>
    </article>

  </section>

  <section class="series-methodology">
    <h2>How We Did This Investigation</h2>
    <ul>
      <li>Obtained 4 years of municipal contract records via FOIA</li>
      <li>Interviewed 12 current and former city officials</li>
      <li>Reviewed city procurement policy and audit records</li>
      <li>Analyzed vendor bid patterns and contract awards</li>
    </ul>
  </section>

</body>
</html>
```

### Landing Page Pre-Deployment Checklist

- [ ] **Landing page title, meta description, og:image set correctly**
- [ ] **All article links stubbed** (article_id references; articles don't exist yet on first publish)
- [ ] **Series metadata complete:**
  - [ ] `<meta property="og:type" content="website">`
  - [ ] `<meta name="series-title" content="Procurement Breakdown">`
  - [ ] `<meta name="series-parts" content="3">`
- [ ] **Images present and optimized** (series hero, etc.)
- [ ] **Methodology section accurate** (matches what was actually done)
- [ ] **Links tested** (once articles are live, retest all links)

---

## Cross-Article Linking

Each article links to others in the series, creating a **web that keeps readers engaged**.

### Article 1 (First in Series)

**Bottom section:**

```html
<section class="series-navigation">
  <h3>This is Part 1 of a 3-Part Series</h3>

  <div class="series-teaser">
    <h4>Coming Tomorrow: Part 2</h4>
    <p>City Council Ignored Its Own Procurement Rules</p>
    <p>Internal documents reveal how decision-makers deliberately bypassed competitive bidding requirements.</p>
    <a href="/series/procurement-breakdown">Read the series hub for updates</a>
  </div>

  <div class="series-teaser">
    <h4>Coming Friday: Part 3</h4>
    <p>Where Is the Oversight? An Audit Trail Goes Missing</p>
    <p>City records show decision-making documents were never created—or destroyed.</p>
  </div>
</section>
```

### Article 2 (Middle in Series)

**Top section (navigation bar):**

```html
<nav class="series-nav">
  <a href="/articles/how-one-vendor-94-percent">← Part 1: How One Vendor Got 94%</a>
  <span class="current">Part 2: City Council Ignored Rules</span>
  <a href="/articles/audit-trail-missing">Part 3: Missing Audit Trail →</a>
</nav>
```

**Bottom section (teaser for Part 3):**

```html
<section class="series-navigation">
  <h3>Read Part 3 (Publishing Tomorrow)</h3>
  <p>Where Is the Oversight? An Audit Trail Goes Missing</p>
  <p>The city's response to our request for audit records: they don't exist.</p>
  <a href="/series/procurement-breakdown">Check the series hub for updates</a>
</section>
```

### Article 3 (Final in Series)

**Top section:**

```html
<nav class="series-nav">
  <a href="/articles/how-one-vendor-94-percent">← Part 1: How One Vendor Got 94%</a>
  <a href="/articles/city-council-ignored-rules">← Part 2: City Council Ignored Rules</a>
  <span class="current">Part 3: Missing Audit Trail</span>
</nav>
```

**Bottom section (link to series hub and summary):**

```html
<section class="series-wrap-up">
  <h3>You've Reached the End of the Series</h3>
  <p><a href="/series/procurement-breakdown">Return to the series hub</a> to read all three parts.</p>
</section>
```

---

## Dependency Management

Series articles are published in sequence. Each article's publication is **blocked if prior articles have issues**.

### Dependency Matrix

```yaml
article_1:
  blocks: [2, 3]  # If Article 1 fails, Articles 2 & 3 are blocked

article_2:
  blocked_by: [1]  # Can't publish if Article 1 is not live
  blocks: [3]

article_3:
  blocked_by: [1, 2]  # Can't publish if Article 1 or 2 is not live
  blocks: []
```

### Publication Order

**Timeline:**

```
Day 0 (April 1):
  09:30 AM - Landing page goes live
  10:00 AM - Article 1 goes live (no dependencies)

Day 1 (April 2):
  10:00 AM - Article 2 goes live (Article 1 must be live and working)

Day 2 (April 3):
  10:00 AM - Article 3 goes live (Articles 1 & 2 must be live and working)
```

### Blocker Resolution

**If Article 2 can't publish on schedule:**

1. **Identify blocker** (broken link in Article 1? metadata issue?)
2. **Fix offline** (edit Article 2 locally or fix referenced Article 1)
3. **Delay announcement** (notify readers that Part 2 delayed)
4. **Communicate timeline** ("Part 2 publishing Friday" → "Delayed to Monday; we're verifying all links")
5. **Reschedule publication** (update landing page with new date)

---

## Staging Workflow

### Stage 1: Pre-Publication (Landing Page Live, Articles Staged)

**Landing page is live; articles are linked but not yet published.**

**Step 1: Deploy landing page**

```bash
# Landing page links to article stubs or coming-soon pages
# Each article has placeholder: "Coming April 1"
gsutil cp landing_page.html gs://bucket/series/procurement-breakdown.html
```

**Verification:**

```bash
# Landing page is accessible
curl -s https://newsroom.org/series/procurement-breakdown | grep -q "Procurement Breakdown"

# Article links are valid (point to draft or coming-soon page)
curl -s https://newsroom.org/articles/how-one-vendor-94-percent | grep -q "Coming April 1"
```

### Stage 2: Article 1 Deployment

**30 minutes after landing page goes live, Article 1 is published.**

```bash
# Deploy Article 1
gsutil cp article_1_final.html gs://bucket/articles/how-one-vendor-94-percent.html

# Update landing page (change "Coming April 1" link to actual article link)
# OR landing page already had correct link; just verify it works
curl -s https://newsroom.org/series/procurement-breakdown | grep -q "how-one-vendor-94-percent"
```

**Verification:**

```bash
# Article 1 loads
curl -s https://newsroom.org/articles/how-one-vendor-94-percent | head -20

# Article 1 references to Part 2 are present (teasers)
curl -s https://newsroom.org/articles/how-one-vendor-94-percent | grep -q "Part 2"
```

**Social announcement:**

```
Hook: "We spent 6 months investigating. $5M in city contracts went to one vendor. Zero competitive bids. Here's the story."
Link: https://newsroom.org/articles/how-one-vendor-94-percent
```

### Stage 3: Article 2 Deployment (Day 2)

**If Article 1 is live and working, deploy Article 2.**

```bash
# Deploy Article 2
gsutil cp article_2_final.html gs://bucket/articles/city-council-ignored-rules.html

# Verify Article 1 -> Article 2 link works
curl -s https://newsroom.org/articles/how-one-vendor-94-percent | grep -q "city-council-ignored-rules"

# Verify Article 2 -> Article 1 link works
curl -s https://newsroom.org/articles/city-council-ignored-rules | grep -q "how-one-vendor-94-percent"
```

**Social announcement:**

```
Hook: "Part 2: City Council ignored its own procurement rules. Internal documents obtained by our reporters show exactly how."
Link: https://newsroom.org/articles/city-council-ignored-rules
```

### Stage 4: Article 3 Deployment (Day 3)

**If Articles 1 & 2 are live, deploy Article 3.**

```bash
# Deploy Article 3
gsutil cp article_3_final.html gs://bucket/articles/audit-trail-missing.html

# Verify all cross-links work
curl -s https://newsroom.org/articles/how-one-vendor-94-percent | grep -q "audit-trail-missing"
curl -s https://newsroom.org/articles/city-council-ignored-rules | grep -q "audit-trail-missing"
curl -s https://newsroom.org/articles/audit-trail-missing | grep -q "how-one-vendor-94-percent"
curl -s https://newsroom.org/articles/audit-trail-missing | grep -q "city-council-ignored-rules"
```

**Social announcement:**

```
Hook: "Part 3 (final): The missing audit trail. City officials tell us decision-making documents don't exist. We explain what that means."
Link: https://newsroom.org/articles/audit-trail-missing
```

---

## Coordinated Release Timing

### Time-Zone Aware Publishing

**Key decision:** What time zone for publication?

- **Local newsroom time:** Easier to coordinate internally
- **Reader local time:** Complex if audience is distributed
- **UTC:** Ensures consistency; readers convert as needed

**Recommendation:** Use newsroom's local time zone; announce time clearly.

### Publication Announcement

**Announce schedule to readers (before Day 1):**

```html
<section class="series-announcement">
  <h2>Coming This Week: Procurement Breakdown</h2>
  <p>We spent 6 months investigating municipal contracts. Here's when you can read our findings:</p>
  <ul>
    <li><strong>Tuesday, April 1 at 10 AM</strong> – Part 1: How One Vendor Got 94% of Contracts</li>
    <li><strong>Wednesday, April 2 at 10 AM</strong> – Part 2: City Council Ignored Rules</li>
    <li><strong>Thursday, April 3 at 10 AM</strong> – Part 3: The Missing Audit Trail</li>
  </ul>
  <p><a href="/series/procurement-breakdown">Subscribe to be notified when parts are published</a></p>
</section>
```

### Email Notification (Optional)

**If newsroom has subscriber list, send notification on publication day:**

```
Subject: New: Part 2 of Our Procurement Investigation

We just published Part 2 of our 3-part series on municipal procurement failures.

Part 2: City Council Ignored Its Own Rules

City council procurement policy requires competitive bidding. Internal documents show the council deliberately bypassed this policy.

Read Part 2: [link]

(Or start with Part 1: [link])
```

---

## Common Mistakes & Red Flags

### Series Planning Mistakes

| Mistake | Why It's Bad | Fix |
|---|---|---|
| **No landing page** (articles published independently) | Readers can't find the series; no central hub; feels scattered | Create landing page first; design as series hub before individual articles |
| **Unclear dependencies** (Article 3 published before Article 1) | Confuses readers; breaks narrative; defeats investigative build | Document dependencies in series definition; enforce sequential publication |
| **Cross-links not tested** (Article 1 links to non-existent Article 2) | Broken links frustrate readers; poor UX; low trust | Test all cross-links before publication; stagger publishing to avoid broken links |
| **Metadata doesn't identify series** (no `series-title` meta tag) | Search engines don't recognize series; articles rank independently instead of as package | Add series metadata to all articles; link landing page to all parts |

### Editorial Gate Mistakes

| Mistake | Why It's Bad | Fix |
|---|---|---|
| **Article 2 approved before Article 1 is live** | Article 2 might reference things Article 1 doesn't say; broken logic | Gate Article 2 approval on Article 1 publication; stagger editorial review |
| **No cross-reference check** (Article 2 links to wrong URL for Article 1) | Links broken; readers can't navigate series | Cross-reference check must happen 1 day before publication; verify all links in staging environment |
| **Dependencies ignored** (try to publish Article 3 when Article 1 has issues) | Article 3 goes live with broken navigation; readers see error | Enforce dependency checks; block publication if dependencies are not met |

### Timing Mistakes

| Mistake | Why It's Bad | Fix |
|---|---|---|
| **All articles published same day at same time** | No narrative build; loses momentum; no buzz over multiple days | Stagger publication: Day 1, Day 2, Day 3 (different times if possible) |
| **Publish Friday, then Saturday, then Monday** (days scattered) | Readers miss middle installment over weekend; lose momentum | Publish consecutive days (Mon-Tue-Wed or Tue-Wed-Thu); avoid weekends |
| **Social announcement goes out before article is live** | Readers click link; see 404 or old content; frustration | Announce right when article goes live (within 5 minutes of publication) |
| **No announcement; series just appears** | Readers don't know series exists; low traffic on Part 1 | Announce schedule 1 week before; remind readers day before each publication |

### Rollback Mistakes

| Mistake | Why It's Bad | Fix |
|---|---|---|
| **Roll back Article 1 after Article 2 is published** | Breaks Article 2's references; confuses readers; all links broken | Before rolling back, assess impact on downstream articles; may need to roll back entire series |
| **Article 2 has issues; roll back without fixing Article 1** | Leaves article 1 orphaned; readers confused | If rolling back, document why and when Part 2 will re-publish |
| **No record of what was rolled back** | Can't explain to readers why content disappeared | Document rollback reason, date, time, and article(s) affected; add note to homepage |

---

## Landing Page Metadata Checklist

- [ ] **Series title set** (og:title, meta title)
- [ ] **Series description set** (meta description, og:description)
- [ ] **Series image set** (og:image, 1200×628px, unique per series)
- [ ] **Series URL set** (og:url, canonical URL)
- [ ] **Article count documented** (`<meta name="series-parts" content="3">`)
- [ ] **All article links present** (once articles are live)
- [ ] **Methodology section complete** (explains how investigation was done)
- [ ] **Publication dates clear** (readers know when each part publishes)

---

## Post-Series Workflow

### After All Articles Published (Day 4+)

1. **Update landing page** (remove "coming soon" teasers; all articles now live)
2. **Cross-link to related stories** (tag similar investigations; build topic authority)
3. **Archive intermediate drafts** (preserve all versions in version control)
4. **Analyze performance** (which article got most traffic? best social engagement?)
5. **Plan next series** (lessons learned; apply to future investigations)

### Archive Protection

**NEVER delete intermediate drafts or working documents:**

```bash
# Keep all versions
series-procurement-breakdown/
  ├── article_1_draft_v1.html
  ├── article_1_draft_v2.html (copy-reviewed)
  ├── article_1_final.html (published)
  ├── article_2_draft_v1.html
  ├── article_2_final.html (published)
  └── article_3_final.html (published)

# Store in version control or backup storage
git add series-procurement-breakdown/
git commit -m "Archive: Procurement Breakdown series (all versions)"
```

**Why:** If a claim in the series is challenged, you need to show the editing process, fact-checking notes, and decision-making trail.

---

## Escalation

If a series article has **legal issues post-publication**:

1. **Assess severity** (factual error vs. defamatory claim)
2. **Decide: roll back or correct?** (editor + legal decision)
3. **If rolling back:** Remove article; note reason on landing page ("Part 2 temporarily removed for review")
4. **If correcting:** Add correction notice to article; update social posts if necessary
5. **Notify downstream** (if Article 1 is updated, does it affect Article 2's logic?)

