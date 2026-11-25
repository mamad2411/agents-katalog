---
name: academic-pipeline
description: Complete research-to-publication pipeline with 6 stages, integrity verification, multi-format citations, and mode-aware processing (academic/engineering)
category: academic
exposure: standard
---

# Academic Pipeline

A streamlined research-to-publication pipeline that guides users from initial research to final output. Supports both academic rigor and engineering efficiency.

## Mode Selection

**Academic Mode** (default for papers):
- Full 6-stage pipeline with integrity checks
- Citation validation and source verification
- Multi-stage review process
- Use when: writing papers, literature reviews, research proposals

**Engineering Mode** (for technical docs):
- Streamlined 3-stage process
- Focus on clarity and practical examples
- Minimal academic overhead
- Use when: writing documentation, technical specs, README files

## Pipeline Overview

```
Academic Mode (6 stages):
  1. RESEARCH → 2. WRITE → 3. REVIEW → 4. REVISE → 5. FINALIZE → 6. SUMMARY

Engineering Mode (3 stages):
  1. OUTLINE → 2. WRITE → 3. REVIEW
```

## Stage 1: RESEARCH (Academic Mode)

**Goal**: Gather and verify sources, define research question

**Agents**:
- `research_coordinator` — Manages the research process
- `source_verifier` — Checks DOI, author, journal legitimacy
- `literature_analyst` — Analyzes and synthesizes literature

**Outputs**:
- Research Question Brief
- Annotated Bibliography
- Source Verification Report

**Checks**:
- [ ] All sources have valid DOIs or are marked "待验证"
- [ ] No suspicious or retracted papers included
- [ ] Research question is specific and researchable

## Stage 2: WRITE

**Goal**: Create structured draft with proper citations

**Agents**:
- `outline_architect` — Creates paper structure based on type
- `draft_writer` — Writes initial draft
- `citation_manager` — Handles citation formatting and placement

**Outputs**:
- Paper Outline
- First Draft with citation placeholders
- Citation List (formatted according to target style)

**Checks**:
- [ ] Structure matches paper type (IMRaD, Literature Review, etc.)
- [ ] All claims have citation support
- [ ] No orphaned citations (cited but not in references, or vice versa)

## Stage 3: REVIEW

**Goal**: Quality check and improvement suggestions

**Agents**:
- `quality_reviewer` — Checks overall quality and clarity
- `methodology_reviewer` — Reviews research methodology (academic mode)
- `citation_reviewer` — Verifies citation accuracy and completeness

**Outputs**:
- Review Report with scores (0-100)
- Improvement Suggestions
- Citation Verification Report

**Checks**:
- [ ] Score ≥ 70 to proceed
- [ ] All critical issues addressed
- [ ] Citations are accurate and complete

## Stage 4: REVISE (Academic Mode)

**Goal**: Address review feedback and improve draft

**Agents**:
- `revision_coordinator` — Manages revision process
- `content_improver` — Improves clarity and flow
- `citation_fixer` — Resolves citation issues

**Outputs**:
- Revised Draft
- Revision Notes (what changed and why)
- Updated Citation List

**Checks**:
- [ ] All review comments addressed
- [ ] No new issues introduced
- [ ] Citations remain accurate

## Stage 5: FINALIZE

**Goal**: Generate final output in target format

**Agents**:
- `format_selector` — Chooses output format based on target
- `document_generator` — Generates final document
- `quality_checker` — Final quality verification

**Outputs**:
- Final Document (MD/DOCX/LaTeX/PDF)
- Bibliography (formatted)
- Quality Report

**Format Options**:
- Markdown (.md) — For web, version control
- DOCX (.docx) — For Word users, journals
- LaTeX (.tex) — For PDF generation, conferences
- PDF (.pdf) — For submission

## Stage 6: SUMMARY (Academic Mode)

**Goal**: Document the writing process and archive materials

**Agents**:
- `process_documenter` — Records the writing process
- `material_archiver` — Archives all materials

**Outputs**:
- Process Summary Document
- Archived Materials (sources, drafts, reviews)

## Citation Formats

| Format | Use Case | Example |
|--------|----------|---------|
| GB/T 7714-2015 | 国内学位论文 | 张三, 李四. 标题[J]. 期刊, 2024, 1(1): 1-10. |
| APA 7th | 社会科学 | Smith, J. (2024). Title. *Journal*, 1(1), 1-10. |
| IEEE | 工程、CS | J. Smith, "Title," *J.*, vol. 1, no. 1, pp. 1-10, 2024. |
| Chicago | 人文科学 | Smith, John. "Title." *Journal* 1, no. 1 (2024): 1-10. |
| MLA | 文学 | Smith, John. "Title." *Journal*, vol. 1, no. 1, 2024, pp. 1-10. |
| Vancouver | 医学 | Smith J. Title. J. 2024;1(1):1-10. |

## Paper Structures

| Structure | Sections | Use Case |
|-----------|----------|----------|
| IMRaD | Introduction, Methods, Results, Discussion | 实验研究 |
| Literature Review | Introduction, Search, Analysis, Discussion | 综述论文 |
| Theoretical | Introduction, Framework, Analysis, Conclusion | 理论研究 |
| Case Study | Introduction, Case, Analysis, Conclusion | 案例研究 |
| Conference | Introduction, Related Work, Method, Evaluation | 会议论文 |

## Integrity Verification

### Pre-Writing Checks
- [ ] Research question is clear
- [ ] Sources are verified
- [ ] No fabricated data

### Post-Writing Checks
- [ ] All citations are valid
- [ ] No plagiarism
- [ ] Claims are supported
- [ ] Limitations acknowledged

### Red Flags
- Suspiciously perfect results
- Non-existent citations
- Unsupported claims
- Copy-pasted content

## Usage Examples

### Academic Mode
```
Write a research paper on AI in healthcare using APA format and IMRaD structure.
```

### Engineering Mode
```
Write technical documentation for this API. Use engineering mode.
```

### Quick Draft
```
Help me outline a literature review on machine learning in drug discovery.
```

## Integration with Existing Skills

This pipeline integrates with:
- `academic-cnki-parser` — CNKI export parsing
- `academic-cite-match` — Citation matching
- `academic-md2docx` — DOCX generation
- `academic-latex-pipeline` — LaTeX compilation
- `academic-citation-database` — Vector database for citations
- `document-formatting` — DOCX formatting rules
