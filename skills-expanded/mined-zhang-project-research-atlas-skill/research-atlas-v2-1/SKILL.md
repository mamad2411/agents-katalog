---
name: research-atlas-v2-1
description: Scientific and technology intelligence workflow for high-recall research landscape mapping. Use when the user wants to search a research direction broadly across papers, reviews, preprints, code, models, datasets, authors, laboratories, grants, patents, projects, companies/startups, trials, and news; deduplicate the corpus; grade strong/medium/weak relevance; snowball from strong seeds; identify leading laboratories; and synthesize evidence-supported novelty and opportunity maps.
---

# Research Atlas V2.1 — Scientific & Technology Intelligence

## Core objective

Convert a research question into a reproducible **Research Landscape + Novelty/Opportunity Map**.

Default execution order:

**Research Question → Concept Expansion → Multi-source Recall → Deduplication → Relevance Engine → Strong Seed Set → Citation/Entity Snowball → Author/Lab Expansion → Code/Model/Dataset → Patent/Grant/Project → Saturation Check → Research Landscape → Novelty/Opportunity Map**.

The governing principle is **recall first, precision later**. Do not discard candidate work during initial collection merely because relevance is uncertain.

## Final architecture

```text
                    Research Question
                           │
                           ▼
                  Concept Expansion
          synonyms / broader / narrower / adjacent
                           │
                           ▼
            ┌────── Multi-source Recall ──────┐
            │                                  │
      Academic layer                    Engineering layer
            │                                  │
 PubMed / Scholar / arXiv          Patents / Grants / Companies
 Semantic Scholar / bioRxiv        Startups / Projects / News
 Reviews / Conferences             Labs / Funding / Clinical trials
            │                                  │
            └─────────────┬────────────────────┘
                          ▼
                     Deduplication
                          │
                          ▼
                    Relevance Engine
                          │
             ┌────────────┼────────────┐
             ▼            ▼            ▼
          Strong        Medium         Weak
          75–100        50–74          25–49
             │
             ▼
        Seed Paper Set
             │
     ┌───────┼─────────┐
     ▼       ▼         ▼
 References Citations Related
     │       │         │
     └──── Citation Snowball ────┐
                                 ▼
                       Author / Lab Expansion
                                 │
                                 ▼
                       GitHub / Model / Dataset
                                 │
                                 ▼
                    Patent / Grant / Project
                                 │
                                 ▼
                       Saturation Check
                                 │
                    New strong work < 5% ?
                         │               │
                        No              Yes
                         │               │
                         └── continue    ▼
                                  Research Landscape
                                         │
                       ┌─────────────────┼─────────────────┐
                       ▼                 ▼                 ▼
                    What exists       Who leads         What is open
                                         │
                                         ▼
                               Novelty / Opportunity Map
```

## 1. Formalize the target as independent axes

Construct a concept lattice before searching.

Required axes:
- **Scientific problem / phenomenon**
- **Disease / pathology / mechanism / phenotype**
- **Modality / data type**
- **Task / output**
- **Model family / algorithm family**
- **Application / deployment setting**
- **Evidence artifact**: paper, review, preprint, code, model, dataset, grant, patent, project, trial, lab, company

For ambiguous terms, create parallel interpretation branches rather than forcing one definition. Example: “pathology attribution” may mean (a) pathophysiological mechanism attribution, (b) biomarker/feature attribution for disease, (c) diagnostic attribution, or (d) computational histopathology. Search each branch and then cluster the results.

## 2. Concept expansion

For every axis, build:
- Canonical terms
- Acronyms
- Synonyms
- Historical terminology
- Broader terms
- Narrower terms
- Adjacent terms
- Likely exclusions / homonyms

Do not depend on the exact vocabulary used by the user. Foundation-model work may be called “large model”, “pretrained transformer”, “self-supervised model”, “generalist model”, “neural foundation model”, “brain foundation model”, etc.

## 3. Query-family ensemble

Generate independent query families instead of one Boolean query:

A. **Exact intersection** — all core axes.
B. **Model-first** — model family × task/domain.
C. **Task-first** — task × modality/domain, model unconstrained.
D. **Modality-first** — modality × task × method variants.
E. **Historical terminology** — terminology predating current FM/LLM names.
F. **Review/benchmark** — review, survey, systematic review, perspective, benchmark.
G. **Recent frontier** — latest 24 months; latest 5 years.
H. **Artifact** — GitHub, Hugging Face, project page, dataset, demo.
I. **Author/lab** — names discovered from strong seeds.
J. **Citation anchor** — exact title/DOI plus references/citations/related.
K. **Funding/IP/project** — grant, award, patent, trial, project, startup/company.

Maintain a query ledger so later searches do not silently repeat the same wording.

## 4. Multi-source recall

### Academic layer
Use complementary source families where available:
- PubMed / PMC / Europe PMC
- Google Scholar / Web of Science / Scopus when accessible
- Semantic Scholar / OpenAlex / Crossref
- arXiv / bioRxiv / medRxiv / OpenReview
- Major venue proceedings (domain dependent)
- Recent reviews and benchmarks

### Engineering / translational layer
Search when relevant:
- GitHub / Hugging Face / project pages
- Dataset repositories
- Author and laboratory pages
- NIH RePORTER / NSF / CORDIS / UK Biobank projects / funder databases
- Patents (Google Patents / Lens / EPO where available)
- ClinicalTrials.gov and related trial registries
- Startups / companies / technical reports / reputable news for emerging non-paper work

A result from news or a company page is not equivalent to peer-reviewed evidence. Keep evidence type explicit.

## 5. High-recall collection rule

During first-pass recall:
- Do **not** require title-level exact match.
- Keep adjacent candidates if one or more target axes match strongly.
- Preserve metadata required for later grading: title, year, authors, venue/type, abstract/summary, DOI/ID, modality, task, model family, disease, code/data/project links.
- Do not summarize conclusions until the candidate pool is reasonably broad.

## 6. Deduplicate and resolve versions

Priority keys:
1. DOI
2. PMID / PMCID / arXiv / bioRxiv identifiers
3. Normalized title + first author + year
4. Canonical project/repository URL

Merge preprint → conference/journal versions into one research work. Record version history but do not double count.

## 7. Relevance Engine

Score **topical relevance**, not prestige.

### Paper/project relevance R (0–100)
- Scientific problem overlap: 0–30
- Task/output overlap: 0–20
- Modality/data overlap: 0–20
- Model/method overlap: 0–20
- Direct linkage to the user's target: 0–10

Classes:
- **Strong:** 75–100
- **Medium:** 50–74
- **Weak:** 25–49
- **Exclude:** <25, unless historically essential

For multi-track questions, score each track separately and add a **Bridge Score B (0–100)** measuring whether the work actually connects the tracks rather than merely belonging to one of them.

### Evidence maturity (separate tag)
- Peer-reviewed primary
- Review/systematic review
- Preprint
- Conference/workshop
- Code/model/dataset
- Grant/project
- Patent
- Clinical trial
- Company/startup/news

Citation count, journal impact factor, institution prestige and recency do not enter R.

## 8. Strong seed set

Create seeds from:
1. Most direct recent primary works
2. Seminal older works
3. High-value recent reviews/benchmarks
4. Strong public models/repos/datasets/projects

Strong seeds drive snowballing. Weak items do not.

## 9. Citation snowball — minimum two rounds in comprehensive mode

For each strong seed:
- Backward references
- Forward citations
- Related/similar papers
- First/corresponding/senior author recent works
- Laboratory/project page
- Linked GitHub/model/dataset/demo
- Related grants/patents/trials/projects

Round 2 repeats the same expansion on newly discovered strong items.

## 10. Laboratory Intelligence

Always produce a **Key Laboratories / Teams** section for comprehensive landscape requests unless clearly irrelevant.

A lab should be surfaced because of repeated evidence, not fame.

### Lab Score L (0–100)
- Number and directness of strong-relevance works: 0–30
- Continuity across ≥2 years / multiple related projects: 0–20
- Evidence of unique data/model/infrastructure: 0–15
- Public code/model/dataset/project ecosystem: 0–15
- Active funded/current pipeline: 0–10
- Bridge relevance to the user's exact topic: 0–10

For comprehensive landscape requests, report **5–10 key laboratories/teams when evidence supports that many**. Rank by the Lab Score, not institutional prestige. If fewer than five have sufficient evidence, report only the supported set.

For each key lab report:
- PI / senior researcher(s)
- Institution
- Why this lab matters
- Strong works/projects
- Modalities and tasks
- Public repos/models/datasets
- Current/ongoing project signal if found
- Whether it is a **direct competitor**, **method source**, or **adjacent leader**

Do not call a lab “top” solely because the institution is famous.

## 11. Artifact and project expansion

For each strong item check:
- GitHub repository
- Model weights / Hugging Face
- Dataset / benchmark
- Project homepage / demo
- Grant/funding project
- Patent/IP
- Clinical trial
- Startup/company implementation

This layer is mandatory for engineering-heavy or rapidly moving AI topics.

## 11.1 Source-coverage matrix and bridge audit

Before synthesis, mark each source family as searched / unavailable / not relevant. For multi-track questions, also produce an **intersection matrix**:
- Exact A×B×C works
- Pairwise A×B works
- Pairwise A×C works
- Pairwise B×C works
- Single-track method sources

This prevents a mature pairwise literature from being mistaken for a mature exact intersection.

For every Strong work, record whether it has been checked for: references, citations/related works, author/lab page, code/model/data, and active project/grant/patent/trial signals.

## 12. Saturation Check

A comprehensive landscape is considered search-saturated only when:
- Major relevant academic and engineering source families were searched
- Query families cover all concept axes
- Recent reviews were checked
- ≥2 snowball rounds were attempted on strong seeds
- Recurring authors/labs were expanded
- Public artifacts/projects were checked
- Two consecutive expansion rounds add **<5% new unique strong items** and no new conceptual cluster

If saturation cannot be established, label the report **high-coverage interim landscape** rather than claiming completeness.

## 13. Research Landscape output

Default output order:
1. Bottom line
2. Interpretation of the research question / concept branches
3. Search coverage and date
4. Strong-relevance table
5. Strong-relevance synthesis by cluster
6. Medium map
7. Weak map
8. Recent reviews / surveys / benchmarks
9. Key laboratories / teams
10. GitHub / models / datasets / project pages
11. Grants / patents / trials / companies where relevant
12. Citation-network findings
13. Research gaps
14. Novelty / opportunity map
15. Search log / saturation status

## 14. Novelty / Opportunity Map

Separate three claim levels:
- **Established:** directly supported by multiple strong works
- **Emerging:** one/few recent papers/preprints/projects
- **Open/underexplored:** no strong direct work found after broad search; explain which adjacent components do exist

Never equate “I did not find it” with “it does not exist.” Phrase novelty claims according to coverage and saturation evidence.

## Special mode — Large Models × Pathology Attribution × Brain Decoding

Automatically create three tracks plus a bridge:

### Track P — Pathology / pathophysiology attribution
Expand:
- disease attribution
- pathophysiological interpretation
- mechanism attribution
- biomarker attribution/discovery
- disease mechanism
- phenotype attribution
- explainable diagnosis
- clinical reasoning
- neural target discovery
- disease-specific network / circuit discovery
- computational pathology / histopathology as a separate interpretation branch

### Track D — Brain decoding
Expand:
- brain decoding / neural decoding
- semantic decoding / language decoding
- mental state decoding
- brain-to-text / neural-to-text
- fMRI-to-text / EEG-to-text / MEG-to-text
- ECoG/sEEG decoding
- brain-to-image / fMRI-to-image
- imagined speech / speech neuroprosthesis
- BCI

### Track M — Large / foundation models
Expand:
- LLM / large language model
- foundation model
- multimodal foundation model
- multimodal LLM / VLM
- brain/neural foundation model
- large EEG model
- pretrained transformer
- self-supervised large-scale pretraining
- generative foundation model

### Bridge search
Search combinations connecting P + D + M, but also search P×M and D×M separately. Grade bridge relevance independently.

Important distinction:
- **Semantic/language decoding** = reconstructing content/words/meaning from brain signals.
- **Clinical/disease decoding** = predicting diagnosis/phenotype/outcome from brain signals.
- **Pathological attribution** = explaining/identifying disease-related neural patterns, biomarkers or mechanisms.

Do not merge these into one category during synthesis.

## Modes

### Rapid
- 3–5 source families
- One snowball round
- 20–50 unique candidates

### Comprehensive (default for “搜全”)
- All relevant source families
- At least two snowball rounds
- Strong/medium/weak grading
- Lab Intelligence
- Artifact/project expansion
- Saturation check

### Update
Reuse ontology and seed set; search only after previous cutoff and report:
- new strong items
- version changes
- new repos/models/datasets
- new grants/projects/patents/trials
- new labs/teams entering the field

## Quality checklist

- [ ] Concept lattice created before search
- [ ] Ambiguous terms searched in parallel branches
- [ ] Multiple query families used
- [ ] Academic + engineering layers searched
- [ ] Reviews from last 5 years checked
- [ ] Preprints checked
- [ ] GitHub/models/datasets checked
- [ ] Strong seeds verified beyond title
- [ ] Backward + forward + related snowball attempted
- [ ] At least two rounds for comprehensive mode
- [ ] Author/lab expansion performed
- [ ] Key labs reported with evidence-based ranking
- [ ] Grants/patents/projects/trials checked when relevant
- [ ] Versions deduplicated
- [ ] Relevance separated from evidence maturity/prestige
- [ ] Bridge score used for multi-track questions
- [ ] Search coverage and saturation status stated
- [ ] Novelty claims distinguish established/emerging/open

## Bundled resources

Load only the resource needed for the current step:

- Use [resources/relevance_and_lab_scoring.md](resources/relevance_and_lab_scoring.md) when assigning work, bridge, or laboratory scores.
- Use [resources/source_coverage_matrix.md](resources/source_coverage_matrix.md) to track searched source families and multi-track intersections.
- Use [templates/report_template.md](templates/report_template.md) to structure the final Research Atlas report.
- Use [templates/lab_intelligence_table.md](templates/lab_intelligence_table.md) for the Key Laboratories / Teams section.
- Use [examples/brain_large_model_example.md](examples/brain_large_model_example.md) when the target combines large models, pathology attribution, and brain decoding.
