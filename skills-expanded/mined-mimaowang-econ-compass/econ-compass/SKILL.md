---
name: econ-compass
description: "Your compass for navigating economics literature. Find the most important, must-read papers in any economics field or research area — from broad subfields like labor economics or macroeconomics to narrow topics like 'carbon pricing' or 'digitalization and firm innovation'. This skill curates essential reading lists by applying rigorous multi-dimensional selection criteria that identify genuinely canonical and irreplaceable papers (not just highly cited ones), and can automatically download PDFs of listed papers. **Activate this skill whenever the user wants to discover, curate, or explore the key literature in economics, finance, econometrics, or any related field — even if they don't explicitly say 'reading list'. Triggers on phrases like 'find important papers', 'build a reading list', 'discover canonical works', 'get up to speed on', 'quickly understand', 'must-read papers', 'what defines', 'key literature in', or any request about the intellectual core of an economics-related domain.**"
license: MIT
---

# 🧭 Econ Compass

Navigate any economics field in minutes — not weeks. Find the papers that built the field, understand why each one is irreplaceable, and download them all with one click.

## Overview

The problem: A researcher or graduate student entering a new economics field faces thousands of papers. Searching by citation count produces a list biased toward convenience references, survey papers, and chronologically old work — not necessarily the papers that define the field's intellectual core. And even after finding the right papers, downloading them one by one wastes hours.

This skill solves both problems:

**Function A: Smart Curation.** Apply five dimensions of selection to identify genuinely canonical papers:
1. **Foundational contribution** — Did this paper create or reshape a research program?
2. **Methodological/empirical innovation** — Did it introduce a new approach to identification, measurement, or modeling?
3. **Empirical significance** — Is the finding economically meaningful and robust?
4. **Coverage** — Does the selected set span all major branches or thematic clusters of the field?
5. **Irreplaceability** — Would removing this paper leave a gap no other paper fills?

**Function B: Automatic PDF Download.** After curating the reading list, offer to download all papers as PDFs, properly named and organized. Papers that cannot be auto-downloaded are reported in a separate file.

The result: a reading list where every paper earns its place through intellectual contribution — not citation count — plus all PDFs ready to read.

---

## When to Use This Skill

Trigger this skill when the user expresses any of these intents (in English or Chinese):

- "Find the most important papers in [field/topic]"
- "Build a reading list for [field]"
- "What are the must-read papers in [field]?"
- "I need to get up to speed on [field] quickly"
- "I want to understand the intellectual core of [field]"
- "帮我找 [领域] 最重要的论文"
- "我想快速了解 [领域]"
- "[领域] 有哪些必读的经典文献？"
- "Curate essential literature on [topic]"
- Any request to discover, explore, or survey the key literature in an economics-related domain

**What counts as a valid domain:** Anything related to economics, finance, or econometrics — from broad subfields (labor economics, macroeconomics, international trade) to narrow research topics (digitalization and firm innovation, carbon pricing, intergenerational mobility, teacher value-added). If the domain is ambiguous, consult `references/field-taxonomy.md` and ask the user to clarify.

---

## When NOT to Use This Skill

Do NOT trigger this skill if the user's request is any of the following. In these cases, answer the question directly or politely decline; do not generate a reading list:

- **Concept introduction or explanation:** "What is macroeconomics?", "Explain general equilibrium", "什么是因果推断？"
- **Textbook or book recommendations:** "Recommend textbooks on econometrics", "有哪些好的宏观经济学教材？"
- **Code or script writing:** "Write a Python script to scrape papers", "帮我写个 Stata 代码"
- **Summarizing or translating a specific paper:** "Summarize this PDF", "翻译这篇论文", "请帮我读一下 Acemoglu (2001)"
- **General research help unrelated to literature curation:** "Help me write my literature review paragraph", "Find the latest working papers this month"

These requests are valid user needs, but they fall outside the scope of econ-compass. Respond directly to the actual question rather than producing a curated reading list.

---

## Core Workflow

### Phase 1: Understand the Request

Before beginning curation, confirm with the user:

1. **Target domain:** What economics field or research topic? Accept anything from broad subfields to narrow topics. If ambiguous, consult `references/field-taxonomy.md` and propose the closest match.
2. **Paper count (N):** How many papers? **Default: 15** if not specified.
3. **Language detection:** If the user's prompt is in Chinese (中文), ask: *"是否需要同时检索中文经济学文献（如《经济研究》《管理世界》等期刊）？"* If the user's prompt is in any other language, do NOT ask this question — proceed with English-only international literature.

   **Accelerated mode exception:** If the user's request explicitly indicates a quick test, trial run, or pre-states constraints (e.g., "测试一下效果", "试试", "quick test", "无需下载", "no PDF needed"), skip all interactive confirmation questions. Proceed directly to curation. Add a brief note in the output header listing which interactive steps were skipped and why (e.g., "[Quick test mode — Chinese literature and PDF download questions skipped per user indication.]").

4. **Output language:** Summaries and inclusion reasons follow the user's prompt language. Paper metadata (title, authors, journal, DOI) always stays in the original language (typically English).
5. **Special constraints:** Any era preference, methodological preference, or topical focus?

### Phase 2: Map the Domain

Load `references/field-taxonomy.md`.

**If the user's domain matches a predefined subfield:**
- Identify all core branches of the subfield
- Note neighboring subfields to avoid redundancy
- Identify key handbooks and review sources for validation
- Goal: know what intellectual territory the N papers must cover

#### Branch Prioritization for Small N

When the user's requested paper count N is smaller than the number of core branches in the subfield, do not mechanically truncate the taxonomy. Instead:

1. **Prioritize branches most commonly emphasized in PhD field exams for that subfield.** These are the branches a field exam committee would consider essential.
2. **Merge closely related branches under a single paper only when that paper genuinely covers both.** Do not force a multi-branch claim onto a paper that only addresses one branch.
3. **Document omissions transparently.** In the Selection Notes, list which branches were omitted due to the small N and explain the rationale.
4. **Avoid simply taking the first N branches from the taxonomy order.** Branch order in `field-taxonomy.md` is organizational, not a ranking of importance.

**If the user's domain does NOT match any predefined subfield (e.g., "digitalization and firm innovation"):**
- Use your knowledge to identify 3-5 thematic clusters within that domain
- These clusters serve as coverage targets (replacing formal branches)
- The predefined taxonomy serves only as a cross-reference — do not reject the request because the domain is not listed
- If you cannot identify meaningful clusters, rely on the general selection criteria and domain consensus

Also load `references/journal-tiers.md` to understand publication venue hierarchy — but remember: judge the paper, not the journal.

### Phase 3: Identify Candidate Papers

Load `references/selection-methodology.md` and apply the full framework.

**For matched predefined subfields:**
- For each core branch, identify the 2-4 most widely recognized papers
- Apply Criteria 1-3 (foundational, methodological, empirical) to each
- Keep the 1-2 strongest candidates per branch

**For non-matched domains:**
- For each thematic cluster, identify the 2-3 most recognized papers
- Apply the same criteria, relying on your knowledge of the domain
- Use Semantic Scholar API or your training knowledge to verify candidates

**Cross-discipline adjustments:**
- **Finance:** Increase weight on Criterion 3 (empirical significance); a major empirical discovery can itself be foundational
- **Econometrics:** Increase weight on Criterion 2 (methodological innovation); a new estimation method is its own classic
- **Complex/agent-based economics:** Increase weight on Criterion 1 (paradigm creation); introducing a new modeling paradigm outweighs a single empirical finding
- **All other fields:** Use the default five-dimension framework

**Validation sources**, in order of authority:
1. PhD field course syllabi from top economics departments
2. Handbook chapters (see field-taxonomy.md for relevant handbooks)
3. JEL and JEP review articles
4. Citation networks within the field

**Do NOT:**
- Use citation count as the primary filter
- Restrict to T5 journals only
- Select based on recency alone
- Ignore important papers published in field-top journals

### Phase 4: Apply the Irreplaceability Filter

This is the decisive step. For every candidate paper, ask:

> "If I remove this paper from the reading list, what is lost? Is there another paper that provides the same intellectual contribution?"

If the answer is "nothing essential," replace it.

If two papers cover the same branch or intellectual contribution:
- Keep the one with the more influential identification strategy, theoretical framework, or empirical finding
- If still tied, keep the earlier paper (foundational priority)

**Document rejected alternatives** — they will appear in the output under "Alternative Candidates Considered."

### Phase 5: Verify and Balance

Load `references/output-specification.md` and verify against the quality checklist.

Key checks:
- Does every core branch (or thematic cluster for non-matched domains) have at least one paper?
- Is there a mix of theoretical, structural, and reduced-form approaches?
- Are foundational classics and recent breakthroughs both represented?
- Would this list pass a PhD field exam committee's scrutiny?

Adjust if necessary, then proceed to output.

### Phase 6: Produce Output

Load `references/output-specification.md` and produce:

1. **`[domain-name]-reading-list.md`** — Complete reading list following the exact template, with:
   - Paper title, authors (Last, First), year, journal, DOI
   - Summary (in the user's prompt language)
   - **"Why Irreplaceable"**: 2-5 concise sentences explaining what unique intellectual contribution this paper made. Prioritize substance over strict brevity — a 4-sentence explanation that genuinely captures the contribution is better than a 2-sentence one that is generic. Focus on: what new idea/method/evidence did it introduce, and why can no other paper substitute for it?
   - Selection notes (branch coverage, balance, alternatives rejected)

2. **`[domain-name]-reading-list.bib`** — BibTeX file with all N papers, keys following `[FirstAuthorLastName][Year][FirstWordOfTitle]` convention

3. **Optional: Notion/Obsidian format** — If the user mentions Notion or Obsidian, offer the alternative format specified in `output-specification.md`

#### Output Quality Requirements

1. **BibTeX is mandatory.** The `.bib` file must contain exactly N valid `@article{...}` entries, one per paper. If you cannot generate a valid BibTeX entry, do not include that paper.

2. **Validation Sources are mandatory.** Selection Notes must include a "Validation Sources" subsection listing:
   - Syllabi reviewed: [N] PhD programs
   - Handbook chapters consulted: [specific chapters]
   - Key review articles: [JEL/JEP articles]
   - Other authoritative sources used

3. **Alternative Candidates must be specific.** Include at least 3 rejected alternatives with:
   - Full citation
   - Specific reason for rejection
   - Which final paper replaced it
   Avoid generic reasons like "overlapping contribution" without explanation.

4. **Use bundled tools.** After drafting the Markdown reading list, run the scripts in `scripts/` to:
   - Generate the BibTeX file (`scripts/generate_bibtex.py`)
   - Validate output format (`scripts/validate_output.py`)
   - Verify DOIs (`scripts/check_dois.py`)
   If validation fails, fix the output before returning it to the user.

### Phase 7: PDF Download

**Trigger rule:** If the user's original request explicitly stated they do not need PDFs (e.g., "无需下载", "no download needed", "不用下载"), skip Phase 7 entirely. Append a note to the reading list output header: *"[PDF download skipped per user request.]"* and end the workflow.

**Otherwise**, proactively ask:

> "是否需要我帮你下载这些论文的 PDF 原文？" (Chinese users)
> "Would you like me to download the PDFs of these papers?" (English users)

If the user says yes, load `references/pdf-download-guide.md` and:

1. Attempt to download each paper's PDF in order using the multi-source fallback chain (Unpaywall → Semantic Scholar → OpenAlex → arXiv)
2. Only keep **published-journal versions**. Deliberately skip preprints, accepted manuscripts, and working-paper versions so the downloaded file matches the cited article
3. Name each PDF: `[NN] Full Title - Authors.pdf` where NN is the two-digit paper number (01, 02, ...)
4. Track which papers were successfully downloaded and which could not be auto-downloaded
5. After all attempts, append a download summary to the reading list:
   - Successfully downloaded (published version): X/N
   - Manual link provided: Y/N
   - Saved to the output directory
6. For papers that could not be auto-downloaded, generate `unavailable-papers.md` listing each paper with title, authors, DOI, a direct access link (DOI resolver or publisher landing page), and the reason auto-download failed

If the user says no, end the workflow.

---

## Selection Principles

Apply these principles throughout the curation process:

1. **A paper's importance is measured by its impact on how economists think, not by its citation count.** A paper that changes the questions researchers ask matters more than one everyone cites as a robustness check.

2. **One paper per branch is sufficient — choose the best one.** Do not include two papers covering the same intellectual ground, even if both are excellent. The goal is maximum coverage with minimum reading.

3. **A reading list is a curriculum, not a greatest-hits album.** The papers should collectively provide systematic understanding of the field, not just a collection of impressive individual papers.

4. **The most recent paper is rarely the most important.** Foundational contributions take time to be recognized. A very recent paper may be brilliant, but it cannot have reshaped the field yet. Include recent breakthroughs only when they have demonstrably changed the research frontier.

5. **When in doubt, ask: "Would a PhD field exam committee consider this omission a gap?"** If yes, the paper belongs on the list.

6. **Speed matters.** The goal is to get the user oriented in a new field within minutes. Do not spend excessive time deliberating between two nearly equivalent papers — choose one, document the alternative, and move on.

---

## Exclusion Rules

The following types of works may **not** be selected as canonical papers in a reading list:

- **Textbooks and monographs:** These are teaching and synthesis works, not primary research contributions.
- **Bestsellers and popular science books:** Works aimed at a general audience (e.g., *Freakonomics*, *Capital in the Twenty-First Century* as a book) are outside the scope.
- **Survey and review articles:** Unless the user explicitly asks for a survey/review-focused list, do not select articles whose primary contribution is summarizing existing literature.
- **Working papers superseded by later research:** Do not select working papers that have been clearly overturned or fully superseded by subsequent published work.
- **Papers outside economics/finance/econometrics:** Do not select papers from unrelated disciplines unless they are foundational to the economics field in question (e.g., a foundational statistics paper for econometrics).

**If the user explicitly requests books or surveys:** Explain that econ-compass focuses on canonical primary research papers, and ask whether they want to switch to a book/survey-oriented mode or proceed with primary papers.

---

## Quality Standards

Every curated reading list must meet these standards:

- **Completeness:** All N papers with full metadata (title, authors, year, journal, DOI)
- **Coverage:** Every core branch or thematic cluster represented by at least one paper
- **Justification:** Each paper has a specific, non-generic "Why Irreplaceable" (2-5 sentences; prioritize substance over brevity)
- **Validation:** At least 3 sources cited (syllabi, handbooks, JEL/JEP reviews)
- **Balance:** Mix of eras, methods, and approaches documented in Selection Notes
- **Honesty:** Alternative candidates considered and reasons for rejection provided
- **PDF completeness:** If Phase 7 is triggered, maximize download success; report failures transparently
- **Metadata verification:** DOI must be in valid format `10.XXXX/XXXX`; never use placeholder values
- **Validation gate:** Output must pass `scripts/validate_output.py` before finalization

---

## Reference Files

Load these bundled resources as needed during curation:

- **`references/field-taxonomy.md`** — Comprehensive taxonomy of 30+ economics subfields with core branches, neighboring fields, and key handbooks. Load during **Phase 1-2** to map the domain.
- **`references/journal-tiers.md`** — Complete journal classification: T5, major general interest, subfield field tops, UTD24/FT50 crossover, and Chinese top journals. Load during **Phase 3** when evaluating publication venues.
- **`references/selection-methodology.md`** — Full multi-dimensional selection framework with criteria definitions, validation sources, search strategy, cross-discipline adjustments, and common pitfalls. Load during **Phase 3-4**.
- **`references/output-specification.md`** — Exact output templates (Markdown, BibTeX, Notion, Obsidian), quality checklist, and Phase 7 output formats. Load during **Phase 5-7**.
- **`references/pdf-download-guide.md`** — Step-by-step instructions for downloading papers after curation, including API strategies, naming conventions, and failure handling. Load during **Phase 7**.

---

## Bundled Tools

In addition to reference files, this project includes executable scripts in the `scripts/` directory. Use them to turn prompt-level guidance into reliable engineering output:

- **`scripts/generate_bibtex.py`** — Generate a valid `.bib` file from the Markdown reading list.
- **`scripts/validate_output.py`** — Validate that the Markdown and BibTeX outputs conform to the required structure and contain exactly N entries.
- **`scripts/check_dois.py`** — Verify that all DOIs are in valid format and resolvable.
- **`scripts/download_pdfs.py`** — Attempt to download PDFs for all listed papers and report failures.

Run these scripts after drafting the reading list and before returning output to the user. Fix any validation failures before finalization.

---

## Usage Examples

### Example 1: English, Broad Subfield

**User:** "Find me the 10 most important papers in development economics."

**Workflow:**
1. Confirm: Development economics, N=10, English
2. Load `field-taxonomy.md` -> Identify 7 core branches of development
3. Load `selection-methodology.md` -> Apply criteria to find anchor papers per branch
4. Search knowledge for canonical papers (T5 + JDE, handbook chapters, PhD syllabi)
5. Apply irreplaceability filter -> Keep best per branch, document alternatives
6. Verify coverage -> All 7 branches represented, balanced methods and eras
7. Produce `development-economics-reading-list.md` + `.bib`
8. Ask: "Would you like me to download the PDFs?"

### Example 2: Chinese, Narrow Topic

**User:** "帮我找 8 篇关于碳定价的经济学经典论文"

**Workflow:**
1. Confirm: 碳定价, N=8, Chinese prompt
2. Ask: "是否需要同时检索中文经济学文献（如《经济研究》《管理世界》等）？"
3. Load `field-taxonomy.md` -> "碳定价" does not match predefined subfield -> use model knowledge for thematic clusters
4. Identify clusters: 碳税理论、碳交易市场、碳的社会成本、碳定价的政策效果
5. Load `selection-methodology.md` -> Find candidates for each cluster
6. Irreplaceability filter
7. Produce `carbon-pricing-reading-list.md` (Chinese summaries and reasons) + `.bib`
8. Ask: "是否需要我帮你下载这些论文的 PDF？"

### Example 3: English, Cross-Discipline

**User:** "I need to understand financial econometrics. Give me 12 essential papers."

**Workflow:**
1. Confirm: Financial econometrics, N=12, English
2. Load `field-taxonomy.md` -> Matches intersection of Finance and Econometrics
3. Apply cross-discipline adjustments: increase weight on methodological innovation (econometrics) and empirical significance (finance)
4. Load `journal-tiers.md` -> Consider both economics T5 and finance top-3 (JF, JFE, RFS)
5. Curate and produce output
6. Offer PDF download

---

## Acknowledgments

This skill was developed using the Anthropic Skill Creator methodology. The field taxonomy draws on the Handbook of Economics series (Elsevier) as an authoritative reference for subfield classifications. Semantic Scholar and Unpaywall APIs are used for paper verification and open-access PDF retrieval.

All paper selections and "Why Irreplaceable" analyses represent original curation work. Paper metadata (titles, authors, DOIs) are factual public information.

The selection methodology reflects established practices in economics pedagogy and is independent of any single scholar's preferences. This project is not affiliated with any of the organizations referenced above.

---

*For feedback or contributions, see the GitHub repository: [github.com/mimaowang/econ-compass](https://github.com/mimaowang/econ-compass)*
