---

name: evidence-based-literature-workflow

description: "Priority evidence-checking coordinator for structured reading and literature verification. Use first when the user says 开始结构性阅读、结构化阅读、结构性读文献、筛选参考文献、候选文献表、文献核验、证据核验、引文核验、引用核验、引文证据、引用证据、证据句、支撑判断 or 证据包, or asks to verify whether cited papers support manuscript claims, mark evidence sentences in PDFs, build a structured reading table, validate acquired full texts, build an about-50-paper candidate pool after a research framework or empirical/experimental results, write an evidence-based literature review, or produce auditable citation-evidence packages for social-science manuscripts. Coordinates reference-fulltext-acquisition, citation-verifier, systematic-literature-review, writing-reference-capture, pdf, and Zotero rather than replacing them."

---



# Evidence-Based Literature Workflow



Use this skill as the coordinator for a full research-writing evidence chain:



`candidate discovery -> metadata verification -> full-text acquisition -> structured reading -> literature-review synthesis -> manuscript citation evidence audit -> final evidence package`.



## Priority Trigger Rule



When the user asks to screen references, build a candidate literature table, start structured reading, do literature verification, audit citations, check whether evidence supports a claim, mark evidence sentences, or build an evidence package, select this skill before isolated `citation-verifier`, `reference-fulltext-acquisition`, `systematic-literature-review`, or `writing-reference-capture`.



It complements, rather than replaces:



- `reference-fulltext-acquisition` for legal PDF/full-text acquisition.

- `citation-verifier` for DOI, metadata, and publication-status verification.

- `systematic-literature-review` for multi-paper synthesis.

- `writing-reference-capture` when only actually used manuscript references should be captured.

- `pdf` or document skills for PDF highlighting, screenshots, and Word outputs.



## Non-Negotiables



1. Do not invent references, DOI, publication status, quotations, page numbers, or evidence sentences.

2. Formal references must be verified through DOI/publisher/journal/index pages, or by user-provided full PDF, CNKI, Google Scholar, OpenAlex, or another public academic search record when DOI is absent.

3. Default formal inclusion requires SCI, SSCI, or CSSCI source status. Exclude working papers, preprints, unpublished manuscripts, grey literature, and papers without SCI/SSCI/CSSCI evidence unless the user explicitly relaxes the rule.

4. A PDF is "acquired" only after title/author/year/venue/DOI or stable source matching. Mismatched files go to a rejected list.

5. Literature-review claims must be traceable to structured reading notes, not only to titles, abstracts, or memory.

6. Manuscript citation evidence must come from the cited source's body text. Do not use title, abstract, keywords, table titles, figure captions, page headers/footers, footnotes used as source chains, or reference lists as final evidence.

7. Evidence must be complete sentences or continuous complete-sentence combinations. Do not highlight keywords, half sentences, broken OCR fragments, whole pages, or irrelevant paragraphs.

8. If a cited source supports only a weaker claim, mark `partially_supported` and revise the manuscript wording. If it does not support the claim, mark `unsupported` and replace, rewrite, or delete the citation.

9. Read and mark evidence source by source. Do not batch-mark citations from keyword hits, search snippets, extracted text alone, or model memory.

10. Do not use a cited author's hypothesis as evidence for a manuscript finding, and do not use a sentence where the cited author is merely reporting another author's claim as evidence for the current citation.

11. Never write annotations into source PDFs or user-provided originals. Work on clean copies under the project output directory and record `inherited_annotation_count=0` before acceptance.

12. If automatic PDF highlighting starts mid-sentence, includes previous/next sentence text, misses final punctuation, or lands in abstract/reference/table material, rebuild that paper with manually verified coordinates.

13. A paper is not accepted until two independent reviews pass: one locator/boundary/source review and one semantic-support review. If either review fails, revise the manuscript claim, evidence sentence, or highlight boundary and rerun that paper.

14. Search-hit or phrase-only highlights are not accepted. If an automatic status such as `highlighted_exact_search` or `highlighted_phrase_fallback` marks only the search phrase, rebuild it as full-sentence highlighting or OCR/manual full-sentence rectangles before final acceptance.

15. Before final packaging, regenerate the audit from the current manuscript and clear stale generated notes, screenshots, and annotated PDFs. No old manual-review notes, screenshots, or accepted statuses from previous claims may remain in the final package.



## Workflow



### 1. Fix Scope and Acceptance Rules



Before searching, record:



- research question and target contribution;

- required language scope;

- source status rule: SSCI/CSSCI, peer-reviewed only, books allowed or not;

- index rule: default `SCI`, `SSCI`, or `CSSCI` evidence required for formal inclusion;

- DOI requirement and allowed DOI exemptions;

- target count by language or topic;

- whether user-provided PDFs count as source evidence;

- output directory.



If the user already supplied rules, follow them and do not re-ask.



### 2. Build Candidate Literature Pool Before Reading



When the user already has empirical or experimental results, a thesis topic, a manuscript framework, or a draft abstract, build the candidate pool before structured reading.



Default target unless the user changes it:



- around 50 candidate references;

- about 20 Chinese sources and 30 English sources;

- prioritize highly cited, formally published, field-recognized work;

- require SCI, SSCI, or CSSCI source evidence before a candidate enters the formal included set;

- include the topic's source literature by default when the user has supplied it, but keep non-SCI/SSCI/CSSCI source literature in background or manual-review status unless the user explicitly approves a waiver;

- inspect upstream and downstream literature of source papers first, then expand to adjacent literature.



Screen references around three jobs:



- theoretical foundation: sources explaining the theory, mechanism, concept, or school of thought behind the study;

- research status: sources that summarize what has already been studied, debated, measured, or left unresolved;

- method or variable grounding: sources about the method, identification strategy, data type, measurement, key variables, or model family.



First pass screening uses title, abstract, keywords, venue, citation signal, and source relation to the user's topic. Output a candidate table before deep reading with:



- reference_id;

- language;

- authors, year, title, journal or source;

- DOI or DOI exemption basis;

- SCI/SSCI/CSSCI index basis or manual-review reason;

- source role: `theory`, `research_status`, `method`, `main_variable`, `topic_source`, `upstream`, `downstream`, or `adjacent`;

- cited-by or impact signal when available;

- why it may matter to the manuscript;

- acquisition status.



After the candidate table, try to acquire and validate full-text PDFs. Put acquired files under the project literature directory; put missing or blocked items in a separate list for user decision. Do not begin structured reading until the candidate table and full-text status are visible.



Use source-specific tools as needed:



- CNKI/CSSCI: use CNKI-oriented discovery and record database evidence.

- English/international literature: use OpenAlex, Google Scholar, DOI/publisher pages, and citation chasing.

- Seed-paper upstream/downstream tracing: inspect references cited by seed papers and papers citing them.



For every candidate, capture raw metadata before screening:



- reference_id;

- authors;

- year;

- title;

- journal/venue;

- DOI;

- source URL or database;

- index status: `SCI`, `SSCI`, `CSSCI`, or `manual_review`;

- source type;

- why it may matter.



Deduplicate by DOI first, then normalized title.



If the task starts from topic keywords rather than a fixed reference list, borrow the local keyword-harvest status model:



- keep a raw no-dedup candidate table before filtering;

- keep high / medium / low or included / background / reject status with reasons;

- keep PDF files separate from HTML/XML/cache/log payloads;

- keep failed-download and retry logs visible;

- after PDF acquisition, produce a dedup manifest that records the kept file, duplicate files, and merge key.



For normal social-science work, PubMed/PMC/Europe PMC are not default search layers; use them only when the topic is biomedical, life-science, medical, or explicitly requires those sources.



### 3. Verify Formal Citation Status



Use `citation-verifier` logic before a paper enters the formal bibliography.



Stable statuses:



- `verified_formal`;

- `verified_book`;

- `verified_cssci_or_cnki`;

- `verified_preprint_or_working_paper`;

- `candidate_only`;

- `rejected`.



When DOI is missing, record the exemption basis explicitly:



- user-provided full PDF;

- CNKI searchable record;

- Google Scholar searchable record;

- OpenAlex searchable record;

- publisher/library/catalog record;

- formally published book.



### 4. Acquire and Validate Full Text



Use `reference-fulltext-acquisition` for PDF acquisition. Keep full texts under the project's literature/source directory, not scattered in Downloads.



Required status files:



- `reference_download_status.csv`;

- `downloaded_pdfs.csv`;

- `provided_originals.csv` when relevant;

- `unable_to_download.csv`;

- `pdf_validation.csv`;

- `acquired_fulltext.md`;

- `missing_fulltext.md`.



Validation checks:



- file exists and opens;

- page count is plausible;

- title/DOI/authors/year match target;

- text is extractable or the first page visibly verifies the source;

- rejected/mismatched PDFs are separated.



### 5. Do Structured Reading Before Writing



Do not write the review section only from bibliographic metadata.



For each included source, extract:



- research question;

- theoretical frame;

- data and sample;

- method;

- core findings;

- limits and identification boundary;

- exact relevance to the user's manuscript;

- possible manuscript claim it can support;

- candidate evidence pages or sections.



Use a structured reading table plus per-article notes. See `references/structured-reading-and-review.md` when drafting a full review.



### 6. Write or Rewrite the Literature Review



Write synthesis, not annotated bibliography. Organize by theoretical problem, method family, empirical finding, or measurement boundary.



Every analytical paragraph should close the PEEL loop:



- Point: what claim the paragraph advances;

- Evidence: which verified sources support it;

- Explanation: why the evidence supports the claim;

- Link: how this advances the user's research question.



Avoid overusing one source; when drafting a formal paper, default to no more than three substantive citations to the same reference unless the user asks otherwise or it is a seed paper.



### 7. Audit Manuscript Citation Evidence



When the user asks to check whether citations really support manuscript claims, use the strict citation-evidence workflow in `references/citation-evidence-audit.md`.



During PDF marking, open each cited source, read the relevant body-text section, select complete sentence evidence, highlight the exact sentence or continuous sentence group in the PDF, and generate a screenshot that shows the highlight plus surrounding context. The highlighted sentence must semantically match the manuscript's use of the citation.



For PDF marking, follow the detailed protocol in `references/citation-evidence-audit.md`: work one paper at a time, create a per-paper round folder, mark only clean output copies, inspect screenshots visually, and accept only the latest round that passed both boundary/source and semantic reviews. New citations added after a draft is rebuilt must re-enter this same audit gate; do not add them only to the reference list.



Minimum outputs:



- `citation_evidence_audit.xlsx`;

- `citation_evidence_audit.docx`;

- `citation_annotated_pdfs/`;

- `citation_evidence_screenshots/`;

- `citation_manual_article_notes/`;

- `citation_manual_review_queue.csv`;

- `citation_evidence_rule.md`;

- `citation_manual_review_completion_summary.md`.



If multiple audit rounds exist, create a final merged evidence package instead of leaving the user to inspect separate versions.



Accepted final packages must satisfy stricter package hygiene:



- `citation_evidence_records.csv` contains only accepted full-evidence statuses such as `highlighted_full_sentence`, `ocr_rect_marked`, or a documented project-equivalent complete-sentence status;

- `citation_manual_review_queue.csv` is empty, unless the remaining rows are explicitly reported as unresolved blockers;

- screenshots, annotated PDFs, and manual notes are from the latest regenerated package, not stale files carried over from prior claims;

- after any manuscript sentence, citation, or evidence sentence changes, regenerate the sentence table and accepted registry before running the two independent reviews.



### 8. Finalize and Package



At the end, provide:



- final formal reference list;

- acquired/missing PDF list;

- structured reading table;

- literature-review draft or revised manuscript section;

- citation evidence audit package;

- unsupported/partial citation repair list;

- final status summary with counts.



## Quality Gate



Do not call the workflow complete until:



- every formal reference has verification status;

- every included PDF is validated or listed as missing;

- every literature-review claim has a structured-reading basis;

- every manuscript citation has `supported`, `partially_supported`, `unsupported`, or `no_pdf_available`;

- every `supported` citation has body-text complete-sentence evidence;

- every `supported` citation has a PDF highlight or an explicitly documented technical fallback screenshot;

- every `partial` or `unsupported` entry has a concrete manuscript revision action;

- final accepted registry covers exactly the current citation table evidence IDs: no missing, duplicate, or extra IDs;

- every accepted PDF audit row has an accepted complete-sentence annotation status such as `highlighted_full_sentence`, `ocr_rect_marked`, `supported_highlighted`, or a documented project-equivalent full-evidence status, plus existing screenshot/annotated-PDF paths and `inherited_annotation_count=0`;

- every text-layer highlight covers the complete evidence sentence or continuous sentence group, not merely a search phrase or keyword span;

- `citation_manual_review_queue.csv` is empty or explicitly reported as an unresolved blocker, and stale manual notes/screenshots from earlier rounds are absent from the final package;

- every accepted paper has two independent PASS reviews on the current regenerated package unless the user explicitly waives this gate;

- final tables and documents point to actual files.
