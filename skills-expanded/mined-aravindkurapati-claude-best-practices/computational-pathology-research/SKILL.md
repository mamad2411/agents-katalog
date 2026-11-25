---
name: computational-pathology-research
description: >
  Researches computational pathology and health AI literature using HuggingFace
  Papers MCP and Exa web search. Use when user says "find papers on", "research",
  "what's the latest on", "literature review", "survey", or asks about methods
  like MIL, SSL, WSI analysis, attention-based pooling, patch embedding, weakly
  supervised learning in pathology, or asks about specific tasks like tumor
  classification, survival prediction, biomarker detection, or lymphoma subtyping.
  Also activate for: "what has been done on X in comp path", "how do people
  approach Y in WSI analysis", "find related work for Z".
  Do NOT use for: general coding help, non-research queries, clinical deployment
  questions without a research component, or drug discovery / genomics topics
  outside pathology.
context: fork
---

# Computational Pathology Research Skill

## Overview
Researches computational pathology and health AI literature. Runs parallel searches
across HuggingFace Papers (academic, arXiv same-day) and Exa (web, practitioner content,
implementation notes). Triages by relevance and recency, fetches full methodology and
results sections, and synthesizes findings into actionable research context. Teaches
the model how to think about the literature, not just retrieve it.

**Requires:** `hf-papers` MCP + `exa` MCP both configured. See `mcp-tools.md` Research Stack section.

---

## Workflow

### Step 1: Decompose the query
Before searching, decompose the user's topic into 4-5 keyword variants covering:
- The task (e.g. "tumor classification", "survival prediction")
- The method family (e.g. "multiple instance learning", "self-supervised pretraining")
- The data modality (e.g. "whole slide image", "WSI", "histopathology")
- Any model architecture angle (e.g. "vision transformer", "attention pooling", "CONCH", "UNI")
- Any recent trend angle (e.g. "foundation model pathology", "weakly supervised pathology 2024")

### Step 2: Run parallel searches
Search HF Papers MCP and Exa simultaneously using the keyword variants.

**HF Papers MCP** (`hf-papers`) - use for:
- Academic papers, arXiv preprints, peer-reviewed work
- Same-day coverage of new preprints
- Finding papers by method name, task, or dataset

**Exa MCP** (`exa`, `web_search_exa` + `deep_researcher`) - use for:
- Practitioner blog posts, implementation notes
- GitHub repos with working code
- Broader web coverage for applied/industry content
- Cross-reference when HF Papers coverage is sparse

For each result, note: title, authors, date, abstract snippet, venue/preprint.

Priority venues to weight higher:
- MICCAI, CVPR, NeurIPS, ICLR, ECCV (top ML/vision)
- Nature Methods, Nature Medicine, Cancer Cell (high-impact clinical)
- Medical Image Analysis, IEEE TMI (domain journals)
- arXiv cs.CV, eess.IV (preprints - check date, weight recent)

Deprioritize: workshop papers without follow-up, preprints older than 18 months with low citation signal.

### Step 3: Triage by relevance + recency
For each paper, score on three axes (quick pass, not deep read):
1. **Task match** - does it directly address the user's problem?
2. **Method relevance** - does it use or compare against relevant methods?
3. **Recency** - 2023-2025 preferred; older papers only if foundational

Keep top 5-8 papers. Discard the rest.

### Step 4: Fetch and read methodology + results
For the top papers, fetch full content via HF Papers or Exa crawl. Read specifically:
- **Methodology**: what exactly they did, what datasets, what backbone/architecture
- **Results**: key numbers (AUC, F1, C-index, etc.) and what they compared against
- **Limitations**: what they explicitly acknowledge doesn't work
- **Code availability**: note if repo exists

Do NOT summarize abstracts. Read the actual methods and results sections.

### Step 5: Synthesize
Organize findings into:
1. **State of the art** - what's the current best approach for this task and what numbers does it achieve?
2. **Method landscape** - what families of approaches exist and what are their tradeoffs?
3. **Key datasets** - what benchmarks are used (TCGA, CAMELYON, PANDA, internal cohorts)?
4. **Open problems** - what do papers identify as unsolved or underexplored?
5. **Directly relevant papers** - ranked list with one-line summaries and links

### Step 6: Research framing (the thinking layer)
After synthesis, answer: given this landscape, how should the user think about their specific problem?
- What's the right method family to start from?
- What baselines are essential to compare against?
- What failure modes should they anticipate?
- What dataset would best validate their approach?

---

## Domain Knowledge (Hard-coded Priors)

### Method Families to Know
- **Attention-based MIL** (ABMIL, TransMIL, DSMIL) - standard weakly supervised WSI classification baseline
- **SSL pretraining on patches** (SimCLR, DINO, MAE applied to histology) - patch encoder quality drives downstream performance
- **Foundation models** (UNI, CONCH, Prov-GigaPath, CHIEF) - pretrained on large pathology corpora; often best starting point in 2024+
- **Graph-based WSI** (PatchGCN, Hierarchical Image Pyramid Transformer) - captures spatial relationships between patches
- **Survival prediction** (SurvPath, MCAT, PORPOISE) - multimodal (WSI + genomics) is the current frontier

### Key Benchmarks to Reference
- **TCGA** - multi-cancer, multi-task gold standard; subtype classification + survival
- **CAMELYON16/17** - lymph node metastasis detection
- **PANDA** - prostate cancer grading
- **BRACS** - breast cancer subtyping
- **NLST** - lung cancer screening (CT, not WSI, but relevant for clinical context)
- **In-house cohorts** - note when papers use private data; limits reproducibility

### Common Failure Modes in This Domain
- **Label noise in TCGA** - pathologist labels aren't always clean; SSL results can be inflated
- **Train/test leakage across slides from same patient** - always check if splits are patient-level
- **Overfitting on small cohorts** - <500 slides is high-risk territory
- **Stain normalization sensitivity** - models often fail cross-site without normalization
- **Patch resolution matters** - 20x vs 40x changes what features are visible

### Aravind's Prior Work Context
- NYU Langone: SSL pretraining + attention-based MIL on lymphoma WSI datasets
- Familiar with: ABMIL, patch-level DINO pretraining, TCGA lymphoma splits
- Current interest: bridging SSL pretraining quality -> downstream MIL performance
- Relevant comparisons: always benchmark against vanilla ABMIL + ImageNet ViT baseline

---

## Output Format
- Lead with state of the art (1 paragraph)
- Method landscape as a comparison table where possible
- Key papers as a ranked list: `[Title](link) - one-line summary. Key result.`
- Open problems as bullet points
- Research framing at the end, clearly labeled
- Total length: 400-800 words unless deep dive requested
- Do NOT include: paper abstracts verbatim, citation counts, venue prestige signaling

---

## Edge Cases
- **Too broad a query** (e.g. "research deep learning in pathology"): narrow to one task or method family before searching. Ask the user if unclear.
- **Very recent topic with few papers** (e.g. a method from last month): note the gap, fall back to closest related work, flag that the field is moving fast.
- **User asks for a specific paper**: fetch it directly via HF Papers MCP, don't run the full pipeline.
- **Conflicting results across papers**: surface the conflict explicitly. Don't pick a winner - describe what conditions favor each approach.
- **HF Papers MCP unavailable**: fall back to Exa `deep_researcher` for academic content. Note the fallback in output.
