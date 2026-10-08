---
name: linkedin-profile-perfector
description: >-
  Audit and rewrite a LinkedIn profile into a recruiter-grade report from the
  user's material (PDF, resume, website, or pasted text). Use when the user asks
  to optimize, improve, review, or audit their LinkedIn profile, headline, About
  section, or experience, or wants help with personal branding, LinkedIn for job
  search, LinkedIn for consulting or clients, or growing a creator profile. Runs
  a 7-step adaptive intake, scores every section 0-10, applies a recruiter
  6-second-scan, produces Current-to-Optimized rewrites, and renders report.md
  plus report.html. Four goal modes re-weight the pipeline: personal branding,
  job search, creator growth, and consulting.
---

# linkedin-profile-perfector

## Overview

This skill turns your LinkedIn material (PDF export, resume, website, or pasted text) into:

1. A **section-by-section audit** scored 0–10, with a recruiter 6-second-scan applied across all modes.
2. **Copy-paste-ready rewrites** for headline, About, every experience role, and skills — formatted as Current → Optimized pairs.
3. A **slim, prioritized action checklist** tuned to your goal mode.
4. Two output files: `runs/<YYYY-MM-DD>-<slug>/report.md` and `runs/<YYYY-MM-DD>-<slug>/report.html`.

**Four goal modes — select one in Step A:**

| Mode | Purpose |
|---|---|
| **1. Personal branding** | Build authority; position yourself; About-as-manifesto |
| **2. Job search** | Recruiter scan, ATS keywords, searchability, completeness |
| **3. Creator / grow profile** | Hook quality, profile-as-landing-page, follower conversion |
| **4. Consulting / win clients** | Proof, ROI, services clarity, client-attraction copy |

**Honest limits:** This skill works from the material you provide. It cannot read live LinkedIn metrics (SSI, profile views, post impressions, engagement rate) from a PDF export — those are flagged as "not available — check at linkedin.com/sales/ssi" rather than estimated. It does not auto-post to LinkedIn, generate profile images or banners, or access your LinkedIn account directly. See `INSTALL.md` for setup instructions and the full honest-limits section.

---

## Step A — Run the Adaptive Intake

Load `references/intake-questions.md` for the full 7-step flow spec, progress-bar render format, and auto-fill algorithm. Then execute the intake as follows.

**Before each question, print the progress bar** using the exact format defined in `references/intake-questions.md`:

```
🟩🟩🟩⏭️🟩⬜⬜   Step 5 of 7
✅ 1. Goal — Job search
✅ 2. Material — PDF + website + resume
✅ 3. Target role — Senior PM  (read from your profile)
⏭️ 4. Industry — B2B SaaS  (auto-filled, skipped)
▶️ 5. Audience …
```

Legend: 🟩 answered · ▶️ current · ⏭️ auto-filled/skipped (with one-line reason) · ⬜ pending.

**For each question, use the AskUserQuestion tool** to render it as a **dropdown** with:
- Options generated from the user's parsed material and context (specific, not generic).
- A **"🤖 Recommend for me"** option on every question.
- An **"Other (type your own)"** escape on every question.

**The 7 steps:**

**Step 1 — 🎯 Goal mode** *(always asked)*
Question: "What's the #1 thing you want this profile to do?"
Options: Personal brand (build authority) · Land a job · Grow as creator · Win consulting clients · 🤖 Help me decide · Other.
This answer sets the mode for every subsequent step.

**Step 2 — 📥 Material** *(always asked)*
Question: "Drop everything you've got — in one place."
Multi-select: LinkedIn PDF (provide file path) · Resume/CV (provide file path) · Website URL · Portfolio/project links · Pasted profile text · Personal notes/wiki · "Just describe me — I'll type it here" · 🤖 Recommend what to gather.
After the user answers, immediately prompt for the path, URL, or text for each selected type. Ingest all of it before Step 3.

**Step 3 — 🧑‍💼 Target role / niche** *(auto-fill eligible)*
Frame the question to match the mode:
- Job search → "What title do you want to land?"
- Consulting → "What service or role do you offer?"
- Personal branding / Creator → "What do you want to be known for?"

Generate dropdown options from the material (e.g. current title, titles mentioned in experience). **If Step 2 material clearly reveals the answer (high confidence), auto-fill and mark ⏭️ in the progress bar with a one-line reason.** Otherwise ask with generated options + 🤖 + Other.

**Step 4 — 🏢 Industry / field** *(auto-fill eligible)*
Question: "What industry or field is that in?"
**Skip entirely if the material already shows the industry (high confidence) — mark ⏭️.** Otherwise generate options from material signals + 🤖 + Other.

**Step 5 — 👥 Target audience**
Question: "Who most needs to be impressed when they land on your profile?"
Generate options tuned to mode + context:
- Personal branding → business owners, industry peers, media/journalists
- Job search → recruiters, hiring managers, department heads
- Creator → niche audience, collaborators, brand sponsors
- Consulting → potential clients, procurement decision-makers, referral partners
Always include 🤖 + Other.

**Step 6 — ⭐ Top achievements / selling points**
Question: "What are your top 2–3 achievements or biggest selling points?"
Extract top candidates from the material and propose them as pre-selected options. The user picks, edits, and/or adds their own. Always include 🤖 (use what I found in your material) + Other.

**Step 7 — 🔑 Keywords to rank for**
Question: "What keywords should your profile rank for?"
**Auto-generate a keyword list** from goal + role + industry using `references/copy-playbooks.md` keyword-sourcing rules. Present them as pre-selected options for the user to confirm or adjust. Offer: "Paste a target job description to sharpen this list." Always include 🤖 + Other.

**Auto-fill / skip rule (Steps 3–4 in particular):** After ingesting Step 2 material, attempt to answer Steps 3, 4, 5, 6, and 7 from the parsed content. If confidence is high, present as a pre-filled confirmation ("I found X in your material — confirm or change?") or mark ⏭️ and proceed. If confidence is low, ask with generated options. Never skip Step 1 or Step 2.

---

## Step B — Ingest Material

Read all material the user provided in Step A using the appropriate tool for each type:

- **LinkedIn PDF / resume PDF / resume doc** → use the `Read` tool with the exact file path the user provided.
- **Website or portfolio URLs** → use the `WebFetch` tool on each URL.
- **Pasted text or notes** → treat as inline content already in the conversation.

Merge everything into a single **working profile model** with these fields:

```
profile_model:
  headline: <string>
  about: <string>
  experience:
    - title, company, dates, description, bullets[]
  skills: []
  education: []
  recommendations: []
  role_signals: []       # inferred job titles, levels
  industry_signals: []   # inferred industries, domains
  audience_signals: []   # inferred audiences from language/context
  achievements: []       # quantified wins, impact statements
  keywords: []           # recurring terms, explicit skill mentions
  pdf_gaps: []           # fields not present in a PDF (SSI, views, etc.)
```

Note every field that could not be extracted from the provided material — these become audit gaps. Mark any live-only metrics (SSI score, profile views, post impressions, follower count from private data) in `pdf_gaps` with the label: "not available — check at linkedin.com/sales/ssi".

---

## Step C — Classify

Using the working profile model from Step B combined with the intake answers from Step A, determine:

1. **Industry** — the primary industry or field (e.g. B2B SaaS, Healthcare, Finance, Marketing, Consulting, Creative).
2. **Profile type** — the user's seniority and function (e.g. IC contributor, manager, executive, founder, freelancer, creator).
3. **Target audience** — the primary audience the profile needs to impress (confirmed from Step A-5).

Record these three signals. They drive which industry benchmarks are selected in Step D and which copy formulas are prioritized in Step E.

---

## Step D — Audit

Load the following three reference files in full before scoring:

- `references/scoring-framework.md` — 0–10 rubrics per section, weighted overall score, mode weight tables, PDF gap handling rules.
- `references/benchmarks.md` — industry benchmark ranges; use as context to calibrate the score narrative, never fabricate live metrics.
- `references/industry-best-practices.md` — All-Star checklist, recruiter visibility rules, recommendations strategy, featured section, content cadence.

**Score each profile section 0–10** using the rubrics in `references/scoring-framework.md`:

| Section | Notes |
|---|---|
| Photo | Score only if image is available; else flag as "not assessable from PDF" |
| Banner | Score only if image is available; else flag as "not assessable from PDF" |
| Headline | Always scoreable |
| About | Always scoreable |
| Experience | Score each role; flag missing metrics |
| Skills | Score count, relevance, top-3 pinned |
| Recommendations | Score count, recency, quality signals |
| Activity / posts | Flag as "not available from PDF — check linkedin.com" if not provided |

**Apply the recruiter 6-second scan.** The scan is defined canonically in
`references/industry-best-practices.md §6` (surfaces, the CLICK/SKIP test, and the
trigger checklists); `references/scoring-framework.md` carries only the output format.
**If the two files differ on the scan, `industry-best-practices.md §6` wins.** Run it:
"In 6 seconds from the headline + first ~300 chars of About + current role, would the
target audience click or skip?" Flag skip-triggers (vague headline, no value prop,
missing keywords, "seeking opportunities" language) and click-triggers as positives.

**Apply mode weights** from `references/scoring-framework.md` to compute the weighted overall score. For example: Job search weights Headline + Experience + Keywords higher; Creator weights About + Activity; Consulting weights About + proof elements.

**Calibrate deduction severity with industry context.** Before finalizing each section
score, check `references/benchmarks.md` for the profile's industry: the same gap can be a
red flag in one field and normal in another (e.g. "2 recommendations is weak in
consulting but average in finance"; "generic recommendations are not a red flag in
finance"). Soften or sharpen the deduction accordingly, and name the industry context in
the scorecard's **Top Fix** column so the user understands why a gap was or wasn't
penalized.

**Flag every gap** found: missing sections, weak copy, absent metrics, keyword gaps, incomplete education or skills, no recommendations.

**Mark live-only metrics** as: `not available — check at linkedin.com/sales/ssi`.

---

## Step E — Rewrite

Load `references/copy-playbooks.md` in full before writing any copy.

> **Anti-fabrication guardrail (highest priority — see `copy-playbooks.md §1.0`).**
> Never introduce a metric, employer, job title, date, client name, dollar figure, or
> achievement that is not present in the user's material. Optimize how true facts are
> *expressed*; do not invent new ones. Where a stronger line clearly needs a number the
> source lacks, insert a bracketed placeholder (`[add metric: …]`, `[add client name]`,
> `[add timeframe]`) for the user to fill. This overrides every other copy rule.

Produce **Current → Optimized** pairs for every rewriteable section. Use the formulas, examples, and per-mode variant tables in `references/copy-playbooks.md`. Tune emphasis to the selected mode:

**Headline:**
- Format: `[Role] | [Key Expertise] | [Value Prop]` (max 220 chars).
- Job search → keyword-dense, ATS-optimized, target title prominent.
- Creator → value prop for followers, what they get by following you.
- Consulting → outcome-led, client result prominent.
- Personal branding → point-of-view, what you stand for.

**About:**
- Limit: ~1,500–2,000 chars (2,600 max).
- Structure: hook (first ~300 chars must work as "see more" preview) → who you are → achievements → what you offer or seek → CTA.
- Tune narrative voice and CTA to the selected mode.

**Experience (every role):**
- Format: title · company · dates · 2–3 line summary + 4–6 short bulleted achievements.
- Each bullet: active verb + result/metric + keyword where natural.
- Job search → metric-driven, keyword-rich, ATS terms visible.
- Consulting → outcome and ROI visible in bullet structure.
- Show `Current:` and `Optimized:` blocks for each role.

**Skills:**
- Up to 50 skills, top 3 pinned.
- Align to keywords from Step A-7 and target job/audience language.
- Remove vague or outdated terms; add keyword-relevant gaps.

For every rewrite, apply the embedded copy rules from `references/copy-playbooks.md`: short & concise · keyword-rich · bullet every experience role · benefits over features · active voice · metrics where possible · cut weak intensifiers ("really", "very", "just") · strip AI-filler ("I hope this finds you well", "leverage", "synergy", "passionate about").

**Project the optimized score (before → after).** After producing the rewrites, re-score
the **Optimized** copy against the *same* rubrics and mode weights from
`references/scoring-framework.md` used for the current audit in Step D. This yields a
**projected** score per section and a projected overall score. Rules:

- The projected score reflects only the rewritten copy — it must be defensible from what
  the Optimized version actually says. Do **not** inflate it, and never count a metric
  the rewrite only left as a `[add metric: …]` placeholder (see the anti-fabrication
  guardrail above). A section whose lift depends on the user filling placeholders should
  note that.
- Always label projected numbers "(projected)" so they read as an achievable target on
  the same rubric, not a promise about LinkedIn's algorithm.
- Carry both numbers forward to Step G as `now → projected` for the overall score and
  each scorecard row.

---

## Step F — Action Checklist

Produce a **slim, mode-specific, prioritized action checklist** — no more than 10–12 items. Prioritize by impact on the selected goal mode. Tie each item to a specific audit gap or rewrite from Steps D and E.

Mode framing:
- **Job search** → recruiter visibility, Open-to-Work settings, target-role keyword gaps, recommendation count, completeness for ATS.
- **Personal branding** → content pillars, signature topics, featured section, engagement habits.
- **Creator / grow** → posting schedule, hook formula, profile-as-landing-page, CTA in About.
- **Consulting** → services section, proof/case-study copy, lead magnet, social proof, outreach.

---

## Step G — Render

Fill the templates with all content from Steps D, E, and F. Before substituting, compute
these tokens — they are easy to miss because they control color and structure, not just text:

**Score → color class** (HTML only). The template no longer hardcodes a color; you must set
the class token from the actual score so the badge color matches the number:

| Token | Set from | Value |
|---|---|---|
| `{{SCORE_CLASS_BEFORE}}` | current overall score | `score-green` if ≥75 · `score-amber` if 50–74 · `score-red` if <50 |
| `{{SCORE_CLASS_AFTER}}` | projected overall score | same thresholds as above |
| `{{SCAN_CLASS}}` | recruiter scan verdict | `scan-click` if CLICK · `scan-skip` if SKIP |

**Before → after scores** (from Step E projection):
- `{{OVERALL_SCORE_BEFORE}}` and `{{OVERALL_SCORE_AFTER}}` — the current and projected overall (out of 100).
- Each `{{SCORECARD_ROWS}}` row must include both the **Now** and **Projected** section scores (0–10), e.g. `Headline | 4 | 9 | …`.

**Keyword gap table** `{{KEYWORD_GAP_TABLE}}` — one row per target keyword with ✅/⬜ for whether it currently appears in each surface, using the placement priority in `references/copy-playbooks.md`: `keyword | Headline | About | Experience | Skills`.

**Profile infrastructure** `{{PROFILE_INFRA_CHECKLIST}}` — a checklist covering custom URL, banner, Featured section, Open-to-Work / Providing-services settings, and recommendations strategy. Items not assessable from the material are marked accordingly rather than scored.

Then:

1. Read `assets/report-template.md` — fill every `{{PLACEHOLDER}}` token with the corresponding audit scores, rewrites, checklist items, and metadata. Write the result to:
   `runs/<YYYY-MM-DD>-<slug>/report.md`
   where `<YYYY-MM-DD>` is today's date and `<slug>` is a short kebab-case name derived from the person's name or target role (e.g. `alex-chen`, `senior-pm`, `marketing-consultant`).

2. Read `assets/report-template.html` — fill every `{{PLACEHOLDER}}` token identically. Write the result to:
   `runs/<YYYY-MM-DD>-<slug>/report.html`

3. **Verify** both output files have zero unfilled `{{...}}` tokens before reporting done. If any remain, fill them or replace with a clearly labeled "not available" note.

4. Tell the user the exact paths to both files:
   - `runs/<YYYY-MM-DD>-<slug>/report.md`
   - `runs/<YYYY-MM-DD>-<slug>/report.html`

5. Ask: "Want me to open the HTML report in your browser?" If yes, run `open runs/<YYYY-MM-DD>-<slug>/report.html`.
