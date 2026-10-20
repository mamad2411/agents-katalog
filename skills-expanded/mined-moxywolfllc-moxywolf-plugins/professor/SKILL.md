---
name: professor
description: Comprehensive academic paper critique system that analyzes research papers through systematic evaluation of authorship authenticity, structural integrity, citation quality, methodological rigor, and contribution validity. Provides brutally honest assessment with detailed, actionable improvement plans to achieve publication-ready quality.
license: Proprietary - MoxyWolf LLC
---

# Professor Skill - Academic Paper Critique

## Overview

This skill performs comprehensive peer review simulation on academic papers, providing the kind of rigorous critique that determines publication success. Unlike generative writing skills, this is **evaluative and critical** - designed to identify weaknesses before reviewers do.

**When to use**: Any time you need to evaluate a research paper for publication readiness, identify critical flaws, verify academic integrity, or create a detailed improvement roadmap.

**Philosophy**: Brutal honesty with constructive guidance. Better to hear hard truths from Claude than from Reviewer 2.

---

## The 10-Phase Critique Methodology

### Overview of Phases

1. **AI Detection Analysis** - Determine authorship authenticity (MUST BE FIRST)
2. **Document Integrity Check** - Verify all cross-references and content exist
3. **Citation Format Analysis** - Identify style and verify consistency
4. **Reference Completeness Audit** - Verify every reference is verifiable
5. **Logic & Argumentation Analysis** - Evaluate reasoning and claims
6. **Methodological Rigor Assessment** - Evaluate research design
7. **Literature Review Critique** - Assess coverage and positioning
8. **Evidence & Results Analysis** - Evaluate empirical support
9. **Writing Quality Assessment** - Academic voice and clarity
10. **Contribution Assessment** - Novelty and significance evaluation

**CRITICAL**: Phase 1 (AI Detection) MUST come first, as it informs interpretation of all subsequent phases.

---

## Phase 1: AI Detection Analysis (ALWAYS FIRST)

### Purpose

Determine whether the paper is human-written, AI-assisted, or AI-generated. This affects credibility assessment and revision recommendations.

### Detection Methodology

#### 1.1 Vocabulary Pattern Scanning

Scan for AI-leaning vocabulary and phrases:

**AI Tells** (flag each occurrence):
- Em dashes (—) - CRITICAL AI signal
- "Furthermore" / "Additionally" / "Moreover"
- "It's worth noting that..." / "It is worth noting"
- "In today's rapidly changing..."
- "At its core..."
- "in order to" (vs. "to")
- "This paper presents..." (vs. active voice)
- "In conclusion" (formulaic closing)
- "delve" / "landscape" / "paramount"
- "robust" / "leverage" / "facilitate" / "crucial"

**Scoring**:
- 0 occurrences: +0 AI score
- 1-3 occurrences: +20 AI score
- 4-6 occurrences: +40 AI score
- 7+ occurrences: +70 AI score

#### 1.2 Sentence Variety Analysis

Extract first 100 sentences, analyze:
- Average sentence length (words per sentence)
- Variance in sentence length
- Range (shortest to longest)

**Interpretation**:
- **Low variance** (<20): Potential AI uniformity (+40 AI score)
- **Moderate variance** (20-80): Inconclusive (+20 AI score)
- **High variance** (>80): Human-like variety (-20 AI score)

#### 1.3 Paragraph Variety Analysis

Analyze first 50 substantive paragraphs:
- Average paragraph length
- Variance in paragraph length

**High variance** (>500): Strong human signal

#### 1.4 Voice Markers

Count instances:
- **First-person** ("I", "we", "our", "my"): Human signal
- **Passive voice**: AI tendency

**Scoring**:
- First-person >20: -20 AI score (strong human voice)
- First-person <5: +20 AI score (AI avoidance)
- Heavy passive voice: +10 AI score

#### 1.5 Calculate AI Score

Total AI score (0-100):
- **0-25**: HUMAN-WRITTEN (minimal AI assistance)
- **25-50**: HUMAN-ASSISTED (likely AI editing/enhancement)
- **50-75**: AI-ASSISTED (substantial AI generation)
- **75-100**: AI-GENERATED (likely fully generated)

### Output Format

```markdown
## PHASE 1: AI DETECTION ANALYSIS

**VERDICT**: [Category] - [X]% confidence in human authorship

**Evidence**:
- AI vocabulary patterns: [N] detected ([list])
- Sentence variance: [value] ([interpretation])
- Paragraph variance: [value]
- First-person voice: [N] instances
- Passive voice: [N] instances

**Assessment**: [2-3 sentence interpretation of findings]

**Recommendation**: [Action items to remove AI tells if needed]
```

### Example

```markdown
## PHASE 1: AI DETECTION ANALYSIS

**VERDICT**: HUMAN-ASSISTED - 70% confidence in human authorship

**Evidence**:
- AI vocabulary patterns: 7 detected ("Furthermore" 2×, "Moreover" 1×, "leverage" 4×)
- Sentence variance: 60.6 (moderate - inconclusive)
- Paragraph variance: 1600.3 (excellent variety)
- First-person voice: 38 instances (strong signal)
- Passive voice: 11 instances (acceptable)

**Assessment**: The paper shows clear human authorship with strong first-person narrative and domain expertise evident throughout. However, AI vocabulary suggests revision/polishing assistance. The personal history ("I co-founded Unified Compliance in 2004") indicates genuine human experience, while formulaic transitions suggest AI enhancement.

**Recommendation**: Remove "Furthermore," "Moreover," and reduce "leverage" usage. Maintain authentic first-person voice while eliminating AI vocabulary patterns.
```

---

## Phase 2: Document Integrity Check

### Purpose

Verify that all tables, figures, and cross-references mentioned in the text actually exist in the document. Avoid false accusations about missing content.

### Methodology

#### 2.1 Content Extraction

Extract all document elements:
- Total paragraphs (text content)
- Total tables
- Total figures/images
- Equations (if applicable)

#### 2.2 Cross-Reference Identification

Search text for references to:
- "Table [N]" or "Table [N]" (all variations)
- "Figure [N]" or "Fig. [N]"
- "Equation [N]" or "Eq. [N]"

Extract all unique references.

#### 2.3 Verification

For each referenced element:
- **Tables**: Verify table exists, note dimensions (rows × columns)
- **Figures**: Verify image/figure exists in document
- **Equations**: Verify equation exists

**Common Extraction Issues**:
- Tables may need special parsing (check document.tables)
- Figures may be embedded as images (check image relationships)
- Captions may be in separate paragraphs following tables/figures

#### 2.4 Table Content Preview

For each table:
- Show first row (typically headers)
- Note table dimensions
- Confirm referenced in text

### Output Format

```markdown
## PHASE 2: DOCUMENT INTEGRITY CHECK

**Content Inventory**:
- Paragraphs: [N]
- Tables: [N]
- Figures: [N]

**Cross-References**:
- Table references: [list]
- Figure references: [list]

**Verification**:
- ✓ Table 1: Referenced and exists ([rows]×[cols])
- ✓ Figure 1: Referenced and exists (embedded image)
- ✗ Table 3: Referenced but MISSING

**VERDICT**: [✓ All verified / ✗ Missing content / ⚠ Incomplete]
```

### Critical Rules

1. **NEVER claim content is missing** without thorough extraction attempts
2. **Try multiple extraction methods** for tables and figures
3. **Check line after tables** - captions often appear as separate paragraphs
4. **If extraction fails**, state "Unable to extract" not "Missing"

---

## Phase 3: Citation Format Analysis

### Purpose

Identify which citation style is used and verify consistency. **DO NOT impose a single "correct" format** - validate the chosen style.

### Methodology

#### 3.1 Style Detection

Search for citation patterns:

**Vancouver (Numbered)**:
- Pattern: `[1]`, `[2,3]`, `[1-5]`
- Typically after punctuation
- References numbered sequentially

**Author-Date (APA/Chicago)**:
- Pattern: `(Author, Year)`, `(Author et al., Year)`
- Typically before punctuation
- References alphabetical by author

**MLA**:
- Pattern: `(Author page)`, `(Author)`
- Less common in scientific papers

**Footnotes**:
- Pattern: Superscript numbers or symbols
- References at page/chapter end

#### 3.2 Determine Primary Style

Count occurrences of each pattern:
- If Vancouver > 2× others: "Vancouver (numbered)"
- If Author-Date > 2× others: "Author-Date (APA/Chicago)"
- If mixed and comparable: "MIXED (inconsistent)" - **SERIOUS ERROR**

#### 3.3 Consistency Check

**For Vancouver**:
- Extract all citation numbers
- Check sequence: [1], [2], [3]... [N]
- Identify gaps (missing numbers)
- Identify duplicates (over-citation is normal for key refs)

**For Author-Date**:
- Verify format consistency
- Check year placement
- Verify parentheses usage

#### 3.4 Reference List Match

Verify reference list format matches citation style:
- Vancouver → Numbered references
- Author-Date → Alphabetical references
- Check if format is consistent

### Output Format

```markdown
## PHASE 3: CITATION FORMAT ANALYSIS

**Detected Style**: [Style name]
- In-text citations: [N] total, [N] unique
- Format: [description]

**Consistency Check**:
- ✓ All citations follow [style] format
- ✗ Missing citation numbers: [list]
- ~ Heavily cited references: [list with counts]

**Reference List**:
- ✓ Format matches detected style
- [N] references in bibliography

**VERDICT**: ✓ Consistent [style] / ✗ INCONSISTENT / ~ Mixed format
```

### Example

```markdown
## PHASE 3: CITATION FORMAT ANALYSIS

**Detected Style**: Vancouver (numbered)
- In-text citations: 51 total, 39 unique
- Format: [N] after punctuation

**Consistency Check**:
- ✓ All citations follow Vancouver format
- ✗ Missing citation numbers: [1], [19], [28], [35-37], [45-46]
- ~ Heavily cited: [10] (8×), [32] (6×)

**Reference List**:
- ✓ Numbered format matches Vancouver style
- 47 references in bibliography

**VERDICT**: ✓ Consistent Vancouver format, but ✗ CRITICAL: 8 citation numbers missing from bibliography
```

### Critical Rule

**NEVER say a citation format is "wrong" just because it's not the one you expected.** Identify the style being used, then validate consistency within that style.

---

## Phase 4: Reference Completeness Audit

### Purpose

Verify that every reference includes a verifiable identifier so readers can locate the source.

### Verifiability Criteria

A reference is **COMPLETE** if it has **ANY** of:
- **URL**: Web address (http:// or https://)
- **DOI**: Digital Object Identifier (doi: or doi.org)
- **ISBN**: International Standard Book Number
- **arXiv**: arXiv identifier (arXiv:XXXX.XXXXX)
- **Patent Number**: U.S. Patent No. XXXXXXX or similar
- **Other persistent ID**: PMID, Handle, URN, etc.

A reference is **INCOMPLETE** if it lacks **ALL** of the above.

### Methodology

#### 4.1 Extract Reference List

Parse the references section:
- Find "References" or "Bibliography" heading
- Extract all individual references
- Number them if not already numbered

#### 4.2 Scan Each Reference

For each reference, check for:
```python
has_url = 'http' in reference or 'https' in reference
has_doi = 'doi:' in reference.lower() or 'doi.org' in reference.lower()
has_isbn = 'isbn' in reference.lower()
has_arxiv = 'arxiv' in reference.lower()
has_patent = 'patent' in reference.lower() and re.search(r'no\.\s*\d', reference.lower())

is_complete = has_url or has_doi or has_isbn or has_arxiv or has_patent
```

#### 4.3 Categorize Incomplete References

For references lacking identifiers, determine type:
- **Web sources**: Should have URL
- **Journal articles**: Should have DOI
- **Conference papers**: Should have DOI or ACL Anthology URL
- **Books**: Should have ISBN or publisher URL
- **Preprints**: Should have arXiv ID
- **Patents**: Should have patent number (often present)
- **Unpublished**: May legitimately lack identifier

#### 4.4 Calculate Completeness

```
Completeness = (Complete References / Total References) × 100%
```

**Grading Scale**:
- **≥90%**: A (Excellent)
- **75-89%**: B (Good)
- **60-74%**: C (Acceptable)
- **40-59%**: D (Poor)
- **<40%**: F (Unacceptable)

### Output Format

```markdown
## PHASE 4: REFERENCE COMPLETENESS AUDIT

**Criteria**: Reference is COMPLETE if it has ANY of: URL, DOI, ISBN, arXiv, Patent Number

**Audit Results**:

[For each reference, show:]
✓ [URL] [N]. Author (Year). Title...
✗ [NO IDENTIFIER] [N]. Author (Year). Title...
     ⚠ [Source type] missing [identifier type]

**Summary**:
- Total references: [N]
- Complete (verifiable): [N]
- Incomplete (unverifiable): [N]
- Completeness rate: [X]%

**GRADE**: [Letter grade] ([assessment])

**Unverifiable References**:
[List all incomplete reference numbers, categorized by type]

**Most Egregious**:
[Highlight top-tier journals or major conferences missing DOIs]
```

### Example

```markdown
## PHASE 4: REFERENCE COMPLETENESS AUDIT

**Criteria**: Reference is COMPLETE if it has ANY of: URL, DOI, ISBN, arXiv, Patent Number

**Audit Results**:

✗ [NO IDENTIFIER] [1]. Alteryx. (n.d.). AI governance glossary.
     ⚠ Web source missing URL
✓ [URL] [3]. Repo-Owner. (2024). GitHub repository. https://github.com/...
✗ [NO IDENTIFIER] [5]. Lastname et al. (2017). Computational Linguistics, 43(4), 837-892.
     ⚠ Journal article missing DOI
✓ [arXiv] [7]. Lastname & Otherlastname (2015). arXiv preprint.
✓ [Patent] [8]. Lastname et al. (2021). U.S. Patent No. 00,000,000.

**Summary**:
- Total references: 47
- Complete (verifiable): 13
- Incomplete (unverifiable): 34
- Completeness rate: 27.7%

**GRADE**: F (Unacceptable)

**Unverifiable References by Category**:

**Web Sources (5)**: [1], [2], [19], [28], [45]
**Major Journals (3)**: [5] Computational Linguistics, [16], [24]
**Conference Papers (15)**: [4], [6], [14], [17], [31], [33], [34], [36], [37], [39], [40], [42], [43], [44]
**Books/Chapters (3)**: [22], [25], [29]
**Other (8)**: [15], [21], [23], [27], [32], [38], [41], [46], [47]

**Most Egregious**:
- [5] Lastname et al. (2017) - **Computational Linguistics 43(4)** - Top-tier journal missing DOI
- [38] Lastname & Otherlastname (2019) - **TACL** - Top-tier journal missing DOI
- [37] Thirdlastname & Fourthlastname (2015) - **NAACL-HLT** - Major conference should be in ACL Anthology
```

### Critical Rules

1. **Be specific**: List EVERY incomplete reference number
2. **Categorize**: Group by source type to show patterns
3. **Defend your claim**: If you say "X% incomplete," enumerate all X
4. **Identify egregious cases**: Top journals or major conferences without DOIs

---

## Phase 5: Logic & Argumentation Analysis

### Purpose

Evaluate the soundness of reasoning, strength of claims, and presence of logical fallacies.

### Methodology

#### 5.1 Thesis Identification

Identify the central claim/thesis:
- What is the main argument?
- Is it clearly stated?
- Is it testable/falsifiable?

#### 5.2 Argument Structure Mapping

Map the logical flow:
1. **Problem** → What gap/issue is addressed?
2. **Root Cause** → Why does this problem exist?
3. **Solution** → What is proposed?
4. **Evidence** → What supports the solution?
5. **Implications** → What follows if correct?

#### 5.3 Logical Soundness Check

Evaluate each step:
- **Validity**: Do conclusions follow from premises?
- **Soundness**: Are premises true?
- **Completeness**: Are counterarguments addressed?

#### 5.4 Fallacy Detection

Check for common fallacies:

**Appeal to Authority**: "A well-known practitioner's implementation validates this" (without empirical comparison)
**Bandwagon**: "A growing body of research" (without quantification)
**Missing Middle**: "X works in research → Our system is needed" (gap)
**Circular Reasoning**: Using conclusion as premise
**False Dichotomy**: "Either A or B" when other options exist
**Post Hoc**: "After X, therefore because of X"

#### 5.5 Gap Identification

Identify logical gaps:
- **Unsupported claims**: Assertions without evidence
- **Missing counterfactuals**: No alternative explanations considered
- **Generalization leaps**: Specific findings over-generalized
- **Assumption failures**: Unstated assumptions that may not hold

### Output Format

```markdown
## PHASE 5: LOGIC & ARGUMENTATION ANALYSIS

**Thesis**: [Statement of central claim]
- Clarity: [✓ Clear / ~ Vague / ✗ Unclear]
- Testability: [✓ Falsifiable / ✗ Unfalsifiable]

**Argument Structure**:
1. Problem: [description]
2. Root Cause: [description]
3. Solution: [description]
4. Evidence: [description]
5. Implications: [description]

**Logical Strengths**:
- [Positive element 1]
- [Positive element 2]

**Logical Weaknesses**:
- [Weakness 1 with explanation]
- [Weakness 2 with explanation]

**Fallacies Detected**:
- [Fallacy type]: [Example from paper]

**Critical Gaps**:
- [Gap 1: Missing evidence/reasoning]
- [Gap 2: Unconsidered alternative]

**Assessment**: [Overall evaluation of argument quality]
```

### Example

```markdown
## PHASE 5: LOGIC & ARGUMENTATION ANALYSIS

**Thesis**: MWE identification must precede text decomposition in domain-specific corpora
- Clarity: ✓ Clear and specific
- Testability: ✓ Falsifiable through empirical comparison

**Argument Structure**:
1. Problem: Existing claim extraction (Claimify) fails on domain-specific text
2. Root Cause: Lack of MWE preprocessing fragments technical terms
3. Solution: Living lexicon architecture with MWE-first processing
4. Evidence: Three-domain demonstration (regulatory, security, AI governance)
5. Implications: All domain-specific NLP should adopt MWE-first principle

**Logical Strengths**:
- Grounded in 20+ years domain experience (credibility)
- Concrete examples showing fragmentation problems
- Clear architectural contribution (living lexicon)

**Logical Weaknesses**:
✗ **No empirical comparison**: Demonstrates problem but never proves solution works better
✗ **Missing counterfactual**: What if improved prompts work without MWE preprocessing?
✗ **Generalization unsupported**: "General principle" tested only in three related domains

**Fallacies Detected**:
- **Appeal to Authority**: Heavy reliance on a well-known practitioner's GitHub implementation without evaluation
- **Bandwagon**: "Growing body of research" without quantifying size or consensus
- **Missing Middle**: "Councils work in research → Our implementation is needed" (gap)

**Critical Gaps**:
- Assumes decomposition is necessary (never questions atomic claim approach)
- MWE discovery circularity: How identify novel MWEs without domain knowledge?
- No threshold validation: Claims about "provenance accumulation" lack empirical basis

**Assessment**: Argument is logically sound but empirically weak. The thesis is testable but untested. The paper presents plausible reasoning but lacks proof.
```

---

## Phase 6: Methodological Rigor Assessment

### Purpose

Evaluate research design, experimental methodology, and validity of conclusions.

### Methodology

#### 6.1 Research Type Classification

Identify paper type:
- **Empirical**: Presents new experimental results
- **Systems**: Describes architecture/implementation
- **Theoretical**: Develops new theory/framework
- **Survey**: Reviews existing work
- **Position**: Argues for approach/perspective

#### 6.2 Methodology Requirements by Type

**Empirical papers require**:
- Clear research questions
- Defined datasets
- Baseline comparisons
- Evaluation metrics
- Statistical validation
- Reproducibility information

**Systems papers require**:
- Architecture description
- Implementation details
- Performance benchmarks
- Comparison to alternatives
- Ablation studies
- Availability (code/demo)

**Theoretical papers require**:
- Formal definitions
- Proofs or derivations
- Illustrative examples
- Connections to existing theory

#### 6.3 Evaluation Checklist

For empirical/systems papers:

**Dataset**:
- [ ] Described clearly
- [ ] Size specified
- [ ] Publicly available or documented
- [ ] Ground truth methodology explained

**Baselines**:
- [ ] Appropriate baselines selected
- [ ] Baseline implementation described
- [ ] Fair comparison (same data/evaluation)

**Metrics**:
- [ ] Metrics defined
- [ ] Metrics appropriate for task
- [ ] Statistical significance tested
- [ ] Effect sizes reported

**Reproducibility**:
- [ ] Code available
- [ ] Hyperparameters specified
- [ ] Random seeds/multiple runs
- [ ] Computational requirements stated

#### 6.4 Grade Methodology

**A**: All requirements met, rigorous design
**B**: Minor gaps, overall solid methodology
**C**: Significant gaps but salvageable
**D**: Major methodological flaws
**F**: No valid methodology / not research

### Output Format

```markdown
## PHASE 6: METHODOLOGICAL RIGOR ASSESSMENT

**Paper Type**: [Classification]

**Critical Flaw**: [Most serious methodological issue if any]

**Required Components**:
- [ ] [Component 1]
- [ ] [Component 2]
- [✓] [Present component]

**What Should Be Included**:
[Specific requirements for this paper type]

**What Is Actually Included**:
[What the paper provides]

**Missing Elements**:
- [Critical missing item 1]
- [Critical missing item 2]

**Grade**: [Letter] - [Justification]

**Recommendation**: [What must be added for validity]
```

### Example

```markdown
## PHASE 6: METHODOLOGICAL RIGOR ASSESSMENT

**Paper Type**: Systems architecture with implementation

**Critical Flaw**: ✗ NO EVALUATION METHODOLOGY

This paper describes a system but provides:
- No benchmark datasets
- No evaluation metrics
- No baseline comparisons
- No ablation studies
- No user studies

**Required Components**:
- [ ] Benchmark datasets with ground truth
- [ ] Baseline implementations for comparison
- [ ] Quantitative evaluation metrics
- [ ] Statistical validation
- [✓] Architecture description (present)
- [✓] Implementation code (GitHub provided)

**What Should Be Included**:
1. **Dataset**: Regulatory documents with annotated MWEs and claims
2. **Baselines**: Claimify (as-is), Claimify + prompts, Static dictionary
3. **Metrics**: Precision, Recall, F1 for MWE identification and claim extraction
4. **Ablation**: Living lexicon vs. static dictionary
5. **Validation**: Expert review of extraction quality

**What Is Actually Included**:
- Table 1: Illustrative examples (not quantitative results)
- Personal narrative of 20+ years experience
- GitHub implementation
- Qualitative comparison to Claimify

**Missing Elements**:
- ✗ No quantitative results whatsoever
- ✗ No accuracy measurements
- ✗ No error analysis
- ✗ No performance benchmarks
- ✗ No user evaluation

**Grade**: D (Poor Methodology)

**Recommendation**: Add comprehensive evaluation:
- Create benchmark dataset (100+ documents, ground truth annotations)
- Implement at least 2 baselines for comparison
- Report Precision/Recall/F1 for MWE and claim extraction
- Conduct ablation study on living lexicon components
- Statistical significance testing (p < 0.05)
```

---

## Phase 7: Literature Review Critique

### Purpose

Assess comprehensiveness of related work coverage and positioning of contribution.

### Methodology

#### 7.1 Coverage Analysis

Evaluate breadth of citations:

**Well-Covered Areas**: [List with citation examples]
**Gaps in Coverage**: [List missing areas]

#### 7.2 Recency Assessment

Analyze citation dates:
- How many from last 3 years?
- How many from last 5 years?
- How many pre-2010?

**Good balance**: ~40% recent (last 3 years), ~40% foundational, ~20% historical

#### 7.3 Citation Quality

Evaluate source types:
- Top-tier venues (Nature, Science, ICML, NeurIPS, ACL)
- Second-tier venues
- Workshops/preprints
- Non-peer-reviewed (blogs, GitHub)

#### 7.4 Self-Citation Analysis

Calculate self-citation rate:
```
Self-citation rate = (Own work citations / Total citations) × 100%
```

**Acceptable**: <15%
**Concerning**: 15-25%
**Excessive**: >25%

#### 7.5 Missing Seminal Works

Identify obvious omissions:
- Foundational papers in the field
- Recent high-impact work
- Competing approaches

### Output Format

```markdown
## PHASE 7: LITERATURE REVIEW CRITIQUE

**Coverage Assessment**:

**Well-Covered**:
- [Area 1]: [citations]
- [Area 2]: [citations]

**Gaps**:
- [Missing area 1]: [Should cite: examples]
- [Missing area 2]: [Should cite: examples]

**Recency Analysis**:
- Last 3 years: [N] ([X]%)
- Last 5 years: [N] ([X]%)
- Pre-2010: [N] ([X]%)
- Assessment: [Good balance / Too recent / Too old]

**Citation Quality**:
- Top-tier venues: [N]
- Second-tier: [N]
- Workshops/preprints: [N]
- Non-peer-reviewed: [N]

**Self-Citation**:
- Own work: [N] citations
- Total citations: [N]
- Rate: [X]%
- Assessment: [Acceptable / Concerning / Excessive]

**Missing Seminal Works**:
- [Work 1]: [Why it matters]
- [Work 2]: [Why it matters]

**Overall Assessment**: [Quality of literature review]
```

---

## Phase 8: Evidence & Results Analysis

### Purpose

Evaluate empirical content, data quality, and strength of evidence.

### Methodology

#### 8.1 Evidence Type Identification

Categorize evidence presented:
- **Quantitative results**: Numbers, measurements, statistics
- **Qualitative findings**: Observations, case studies, examples
- **Theoretical proofs**: Mathematical derivations
- **Anecdotal**: Personal experience, examples without data

#### 8.2 Results Verification

For each claim:
- Is evidence provided?
- Is evidence appropriate?
- Is evidence sufficient?
- Are alternative explanations considered?

#### 8.3 Table/Figure Analysis

For each table/figure:
- **Purpose**: What does it show?
- **Effectiveness**: Does it support claims?
- **Quality**: Is it clear and complete?
- **Type**: Descriptive or evaluative?

#### 8.4 Statistical Rigor

Check statistical reporting:
- Sample sizes reported?
- Significance tests used?
- P-values reported?
- Effect sizes reported?
- Confidence intervals included?
- Multiple comparison corrections?

### Output Format

```markdown
## PHASE 8: EVIDENCE & RESULTS ANALYSIS

**Evidence Provided**:
- Quantitative results: [Yes/No - description]
- Qualitative findings: [Yes/No - description]
- Examples: [Yes/No - description]

**Table/Figure Analysis**:

**Table 1**: [Title]
- Purpose: [What it shows]
- Type: Descriptive / Evaluative
- Strengths: [What works]
- Weaknesses: [What's missing]

**Statistical Rigor**:
- [ ] Sample sizes reported
- [ ] Significance tests
- [ ] P-values
- [ ] Effect sizes
- [ ] Confidence intervals

**Missing Evidence**:
- [Claim 1]: [What evidence is needed]
- [Claim 2]: [What evidence is needed]

**Grade**: [Letter] - [Justification]
```

---

## Phase 9: Writing Quality Assessment

### Purpose

Evaluate academic voice, clarity, and stylistic appropriateness.

### Methodology

#### 9.1 Academic Voice Check

Assess:
- **Active vs. passive voice**: Active preferred ("We analyzed" not "Was analyzed")
- **First-person usage**: Appropriate for methodology ("We propose")
- **Contractions**: None in academic writing
- **Formality level**: Professional but not stilted

#### 9.2 Clarity Assessment

Evaluate:
- Technical terms defined on first use
- Acronyms spelled out initially
- Sentence complexity (readable but not simplistic)
- Paragraph structure (one idea per paragraph)

#### 9.3 Structure & Flow

Check:
- Logical section progression
- Effective transitions between sections
- Consistent terminology throughout
- Clear signposting ("First...", "Second...", "Finally...")

#### 9.4 Common Issues

Flag:
- Redundancy
- Jargon without definition
- Overly long sentences
- Unclear antecedents
- Mixed metaphors

### Output Format

```markdown
## PHASE 9: WRITING QUALITY ASSESSMENT

**Academic Voice**: [Grade] - [Assessment]
- Active voice: [% or assessment]
- First-person: [Appropriate / Excessive / Insufficient]
- Contractions: [✓ None / ✗ Present]
- Formality: [Appropriate / Too casual / Too stiff]

**Clarity**: [Grade] - [Assessment]
- Technical definitions: [Complete / Partial / Missing]
- Acronyms: [Defined / Some undefined]
- Readability: [Excellent / Good / Poor]

**Structure**: [Assessment]
- Section flow: [Logical / Some gaps / Unclear]
- Transitions: [Smooth / Adequate / Choppy]
- Consistency: [Maintained / Some issues]

**Issues Found**:
- [Issue type]: [Examples]

**Strengths**:
- [Positive aspect 1]
- [Positive aspect 2]

**Grade**: [Letter] - [Overall writing quality]
```

---

## Phase 10: Contribution Assessment & Final Verdict

### Purpose

Evaluate novelty, significance, and overall publishability.

### Methodology

#### 10.1 Novelty Assessment

For each claimed contribution:
- Is it actually novel?
- How does it differ from prior work?
- Is the novelty significant or incremental?

#### 10.2 Significance Evaluation

- **Scientific impact**: Advances understanding?
- **Practical impact**: Useful for practitioners?
- **Methodological impact**: New techniques/tools?
- **Scope**: Narrow domain or broad applicability?

#### 10.3 Competitive Positioning

Compare to:
- Existing approaches
- Recent related work
- State-of-the-art

#### 10.4 Publishability Assessment

Consider:
- Novelty of contribution
- Quality of evidence
- Writing quality
- Fit for target venue

#### 10.5 Rejection Risk Scoring

Estimate likelihood of rejection:
- **Low risk** (<20%): Strong accept likely
- **Medium risk** (20-50%): Borderline, depends on reviewers
- **High risk** (50-80%): Likely reject unless major revision
- **Very high risk** (>80%): Almost certain reject

### Output Format

```markdown
## PHASE 10: CONTRIBUTION ASSESSMENT & FINAL VERDICT

**Claimed Contributions**:
1. [Contribution 1]
   - Novelty: [High / Moderate / Low / None]
   - Validity: [Proven / Plausible / Unproven]
   - Significance: [Major / Moderate / Minor]

2. [Contribution 2]
   [Same analysis]

**Competitive Positioning**:
- vs. [Competitor 1]: [Comparison]
- vs. [Competitor 2]: [Comparison]

**Overall Novelty**: [Assessment]
**Overall Significance**: [Assessment]

**Publishability Assessment**:

**Strengths**:
1. [Major strength 1]
2. [Major strength 2]

**Critical Weaknesses**:
1. [Fatal flaw 1]
2. [Fatal flaw 2]

**Rejection Risk**: [Percentage]% - [Risk level]

**Most Likely Rejection Reasons**:
1. [Reason 1]
2. [Reason 2]

**FINAL VERDICT**: [ACCEPT / MINOR REVISION / MAJOR REVISION / REJECT]

**Grade**: [A+ to F] - [Overall assessment]
```

---

## Phase 11: Detailed Path Forward

### Purpose

Provide concrete, actionable plan to transform paper from current state to publication-ready quality.

**CRITICAL**: This must be **detailed and specific**, not generic advice. Each task must have:
- Concrete action items
- Specific deliverables
- Timeline estimates
- Resource requirements

### Methodology

#### 11.1 Identify All Issues

Categorize by severity:
- **CRITICAL**: Must fix for any submission
- **MAJOR**: Required for good review
- **MODERATE**: Strengthens paper significantly
- **MINOR**: Polish and improvement

#### 11.2 Create Phase-by-Phase Plan

Structure improvement as phases:

**Phase 1: Critical Fixes** (urgent, foundational)
**Phase 2: Major Enhancements** (substantial work)
**Phase 3: Validation & Testing** (empirical work)
**Phase 4: Writing & Integration** (synthesis)
**Phase 5: Submission Preparation** (finalization)

#### 11.3 Detail Each Phase

For each phase, specify:

**Tasks**: Numbered checklist of specific actions
**Deliverables**: Concrete outputs
**Timeline**: Week-by-week breakdown
**Resources**: Personnel, tools, budget needed
**Success Criteria**: How to know phase is complete

#### 11.4 Resource Planning

Estimate requirements:
- **Personnel**: Who does what
- **Computational**: API costs, cloud computing
- **Funding**: Total budget needed
- **Time**: Total weeks/months

#### 11.5 Risk Mitigation

Identify risks and mitigation:
- Timeline slippage
- Data availability
- Resource constraints
- Technical challenges

### Output Format

```markdown
## DETAILED PATH FORWARD TO A+ PUBLICATION

**Objective**: Transform paper from [current grade] to publication-ready A+ quality

---

### PHASE 1: CRITICAL FIXES (Timeline: [weeks])

**Objective**: [What must be fixed immediately]

#### Task 1.1: [Specific Task Name]

**Action Items**:
- [ ] [Concrete action 1 with specific details]
- [ ] [Concrete action 2 with specific details]
- [ ] [Concrete action 3 with specific details]

**How to Execute**:
[Step-by-step instructions, specific sources to check, exact procedures]

**Deliverable**: [Specific output - be concrete]

**Timeline**: [Specific timeframe]

---

#### Task 1.2: [Next Task]

[Same detailed structure]

---

### PHASE 2: [MAJOR ENHANCEMENTS]

[Same structure with multiple tasks]

---

### PHASE 3: [VALIDATION]

**Task 3.1: Empirical Evaluation Design**

**Research Questions**:
- RQ1: [Specific testable question]
- RQ2: [Specific testable question]

**Datasets Required**:
- **Primary Dataset**: [Exact source, size, how to obtain]
  - Source: [Specific location/database]
  - Size: [Exact numbers]
  - Annotation: [Who, how, timeline]
  - Cost: [Budget estimate]

- **Secondary Dataset**: [Same details]

**Baselines to Implement**:
- **Baseline 1**: [Exact implementation]
  - Source: [GitHub repo or description]
  - Setup: [Specific steps]
  - Expected results: [What to measure]

**Metrics**:
- [Metric 1]: [Definition, how to compute]
- [Metric 2]: [Definition, how to compute]

**Statistical Tests**:
- [Test type]: [When to use, significance threshold]

**Deliverable**: [Specific output with numbers]

**Timeline**: [Week-by-week breakdown]

---

### RESOURCE REQUIREMENTS

**Personnel**:
- Lead author: [hours/week for X weeks]
- Annotators: [N people × hours × rate = cost]
- Reviewers: [N people × hours × rate = cost]

**Computational**:
- LLM API calls: [$amount]
- Cloud computing: [$amount]
- Storage: [$amount]

**Total Budget**: $[minimum] - $[optimal]

---

### TIMELINE OVERVIEW

| Phase | Weeks | Milestone |
|-------|-------|-----------|
| Critical Fixes | 1-2 | [Specific deliverable] |
| Enhancements | 3-6 | [Specific deliverable] |
| Validation | 7-10 | [Specific deliverable] |
| Writing | 11-14 | [Specific deliverable] |
| Submission | 15-16 | [Venue submission] |

**Total Duration**: [X weeks / months]

---

### RISK MITIGATION

**Risk 1**: [Specific risk]
- **Impact**: [What happens if occurs]
- **Probability**: [Low/Medium/High]
- **Mitigation**: [Specific prevention strategy]
- **Contingency**: [What to do if it happens]

---

### TARGET VENUES

**Primary Target**: [Specific conference/journal]
- Track: [Specific track]
- Deadline: [Date]
- Page limit: [Number]
- Fit rationale: [Why appropriate]

**Secondary Targets**: [Alternatives]

---

### SUCCESS CRITERIA

**Minimum for Publication**:
- [ ] [Specific requirement 1]
- [ ] [Specific requirement 2]

**Target for Strong Accept**:
- [ ] [Higher bar requirement 1]
- [ ] [Higher bar requirement 2]

---

### EXPECTED OUTCOME

**With this plan executed**:

**Publication Venue**: [Specific venue and track]
**Review Scores**: [Predicted score range]
**Grade Prediction**: [Letter grade with rationale]

**Post-Publication Impact**:
- [Expected citation impact]
- [Expected practical adoption]
- [Expected follow-up work]
```

### Example: Reference Completeness Fix

```markdown
### PHASE 1: CRITICAL FIXES (Weeks 1-2)

#### Task 1.1: Reference Completeness (Week 1)

**Target**: Achieve >95% reference completeness (45/47 references)

**Action Items - Journals (add DOIs)**:
- [ ] [5] Lastname et al. (2017) Computational Linguistics
  → Search: doi.org/10.1162/COLI or ACL Anthology
  → Add DOI to reference entry
  → Verify URL resolves
  
- [ ] [16] Fifthlastname et al. (2013) medical NLP
  → Search: PubMed or journal website
  → Get PMID or DOI
  → Add to reference
  
[Continue for ALL incomplete references with specific steps]

**Action Items - Conference Papers (add ACL Anthology URLs)**:
- [ ] [4] Sixthlastname 2009 MWE Workshop
  → Search: aclanthology.org "Sixthlastname multiword 2009"
  → Get ACL Anthology URL (https://aclanthology.org/...)
  → Add to reference

[Continue with specific instructions for each]

**Deliverable**: Updated reference list with 45/47 (95.7%) having verifiable identifiers

**Timeline**: 
- Days 1-2: Search for journal DOIs
- Days 3-4: Search for conference papers
- Day 5: Add URLs for web sources
- Day 6-7: Verify all additions, final check

**Verification**:
- Run completeness audit script
- Manually verify 10 random additions
- Confirm all URLs resolve
```

### Critical Rules for Path Forward

1. **Be Specific**: Never say "add evaluation" - say "implement Claimify baseline on Federal Register corpus with P/R/F1 metrics"

2. **Include Numbers**: Timeline (2 weeks), budget ($3K), sample size (100 documents), metrics (>0.80 Cohen's kappa)

3. **Name Sources**: "ACL Anthology", "SpringerLink", "Federal Register", not "appropriate databases"

4. **Step-by-Step**: For complex tasks, break into daily or weekly sub-tasks

5. **Resource Reality**: Include actual costs, time commitments, personnel needs

6. **Contingencies**: What if timeline slips? What if data unavailable? Have backup plans.

---

## Workflow Summary

### Step 1: Initial Assessment

Run document through all 10 phases in order:
1. AI Detection (ALWAYS FIRST)
2. Document Integrity
3. Citation Format
4. Reference Completeness
5. Logic & Argumentation
6. Methodological Rigor
7. Literature Review
8. Evidence & Results
9. Writing Quality
10. Contribution Assessment

### Step 2: Compile Findings

Create comprehensive critique document:
- Executive summary
- Phase-by-phase findings
- Overall verdict
- Grade (A+ to F)

### Step 3: Generate Path Forward

Based on identified issues:
- Categorize by severity
- Design phase-by-phase improvement plan
- Specify concrete tasks and timelines
- Estimate resources needed

### Step 4: Deliver Critique

Present findings:
- Start with verdict and grade
- Explain major issues first
- Provide detailed analysis
- End with actionable path forward

---

## Output Format Template

```markdown
# PROFESSOR CRITIQUE: "[Paper Title]"

**Paper**: [Title]
**Author(s)**: [Names]
**Affiliation**: [Institution]
**Date Reviewed**: [Date]

---

## EXECUTIVE SUMMARY

**Overall Assessment**: [ACCEPT / MINOR REVISION / MAJOR REVISION / REJECT]

**Key Strengths**:
- [Strength 1]
- [Strength 2]

**Critical Weaknesses**:
- [Weakness 1]
- [Weakness 2]

**Recommendation**: [One paragraph summary]

---

## PHASE 1: AI DETECTION ANALYSIS
[Full analysis]

## PHASE 2: DOCUMENT INTEGRITY CHECK
[Full analysis]

## PHASE 3: CITATION FORMAT ANALYSIS
[Full analysis]

## PHASE 4: REFERENCE COMPLETENESS AUDIT
[Full analysis]

## PHASE 5: LOGIC & ARGUMENTATION ANALYSIS
[Full analysis]

## PHASE 6: METHODOLOGICAL RIGOR ASSESSMENT
[Full analysis]

## PHASE 7: LITERATURE REVIEW CRITIQUE
[Full analysis]

## PHASE 8: EVIDENCE & RESULTS ANALYSIS
[Full analysis]

## PHASE 9: WRITING QUALITY ASSESSMENT
[Full analysis]

## PHASE 10: CONTRIBUTION ASSESSMENT & FINAL VERDICT
[Full analysis]

---

## DETAILED PATH FORWARD TO A+ PUBLICATION
[Complete improvement plan]

---

## REVIEWER PREDICTION

### Review 1 (Likely Score: X/10)
> "[Predicted reviewer comment]"

### Review 2 (Likely Score: X/10)
> "[Predicted reviewer comment]"

### Meta-Review (Decision: [outcome])
> "[Predicted meta-review]"

---

**FINAL GRADE**: [Letter] - [Assessment]
```

---

## Special Cases

### Case 1: Paper Has No References Section

**Response**: "This paper lacks a references section entirely. Academic papers must cite prior work. This is an immediate disqualification for publication."

**Recommendation**: Create references section with:
- 20-30 foundational citations minimum
- Recent work (last 3 years)
- Seminal papers in field

### Case 2: Paper Is Purely Theoretical

**Adjust expectations**:
- No empirical evaluation needed
- Focus on: proof correctness, definitions, examples
- Literature review of theoretical work
- Connections to existing theory

### Case 3: Position Paper / Opinion Piece

**Different criteria**:
- Argument strength paramount
- Empirical evidence optional
- Novel perspective required
- Engagement with counterarguments

### Case 4: Dataset/Tool Paper

**Focus on**:
- Documentation quality
- Availability and accessibility
- Comparison to existing resources
- Use cases and validation

---

## Best Practices

### 1. Start With AI Detection

Always run Phase 1 first - knowing authorship authenticity informs all subsequent interpretation.

### 2. Document Extraction First

Before claiming content is missing, thoroughly attempt extraction. Try multiple methods.

### 3. Identify, Don't Impose

For citation style, identify what's being used rather than imposing what you expect.

### 4. Enumerate Evidence

Never make quantitative claims without listing specific examples that support them.

### 5. Be Constructive

Brutal honesty is good; being destructive is not. Always provide path forward.

### 6. Grade Consistently

Use clear grading rubrics:
- **A**: Publication-ready, minor polish needed
- **B**: Strong work, moderate revision
- **C**: Salvageable, major revision required
- **D**: Significant flaws, borderline
- **F**: Fundamental issues, not ready

### 7. Predict Reviewers

Think like Reviewer 2 (notorious for being critical) - what would they say?

### 8. Provide Specificity

"Add evaluation" → "Implement X baseline on Y dataset with Z metrics"
"Fix references" → "Add DOI for [5], URL for [28], etc."

---

## Common Pitfalls to Avoid

### Pitfall 1: Missing Content False Positive

❌ **Wrong**: "Table 1 is referenced but missing"
✓ **Right**: After extraction attempt: "Table 1 exists (4×6, showing...)"

### Pitfall 2: Citation Format Rigidity

❌ **Wrong**: "This paper uses Vancouver but should use APA"
✓ **Right**: "This paper consistently uses Vancouver format"

### Pitfall 3: Undefended Quantitative Claims

❌ **Wrong**: "Most references lack DOIs"
✓ **Right**: "34/47 references lack DOIs: [1], [2], [4]..."

### Pitfall 4: Generic Advice

❌ **Wrong**: "The paper needs empirical evaluation"
✓ **Right**: "Implement these specific experiments: (1) Baseline comparison on Federal Register corpus using P/R/F1..."

### Pitfall 5: Ignoring Authorship

❌ **Wrong**: Treating all papers as human-written
✓ **Right**: Phase 1 detection influences revision recommendations

---

## Examples

### Example 1: Well-Written Paper Needing Evaluation

**Scenario**: Strong human authorship, clear logic, poor methodology

**Phase 1 Result**: 20% AI score (human-written)
**Phase 4 Result**: 85% reference completeness (B grade)
**Phase 6 Result**: No evaluation (D grade)

**Verdict**: MAJOR REVISION (fix methodology)

**Path Forward**: Focus on Phase 3 (adding evaluation), keep writing quality

---

### Example 2: AI-Generated Paper

**Scenario**: High AI score, formulaic structure, missing evidence

**Phase 1 Result**: 85% AI score (AI-generated)
**Phase 9 Result**: AI vocabulary throughout

**Verdict**: REJECT (rewrite with human authorship)

**Path Forward**: Complete rewrite focusing on authentic voice, remove all AI tells

---

### Example 3: Position Paper Without Empirical Work

**Scenario**: Arguing for approach, no experiments

**Phase 1 Result**: Human-written
**Phase 5 Result**: Strong argumentation
**Phase 6 Result**: N/A (position paper, no methodology expected)

**Verdict**: MINOR REVISION (strengthen argument, add citations)

**Path Forward**: Focus on logic and literature review, empirical work optional

---

## Conclusion

The Professor Skill provides comprehensive, systematic academic paper critique through 10 rigorous phases. By identifying the style of human vs. AI authorship first, verifying all content actually exists, respecting chosen citation formats, demanding verifiable references, and providing detailed actionable improvement plans, this skill delivers the kind of honest assessment that determines publication success.

**Remember**: The goal is not just to criticize, but to provide a roadmap from current state to publication-ready quality. Be brutal, but be constructive.

---

## Quick Reference Checklist

Before delivering critique, verify:

- [ ] AI detection ran first (Phase 1)
- [ ] All tables/figures verified to exist (Phase 2)
- [ ] Citation style identified, not imposed (Phase 3)
- [ ] Every incomplete reference enumerated (Phase 4)
- [ ] All quantitative claims defended with evidence
- [ ] Path forward is detailed and specific (Phase 11)
- [ ] Resources and timeline included
- [ ] Success criteria specified
- [ ] Grade justified with specific reasons
- [ ] Reviewer predictions included
