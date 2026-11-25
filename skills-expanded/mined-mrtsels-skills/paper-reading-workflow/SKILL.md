---
name: paper-reading-workflow
description: "Use when reading academic papers: parse PDFs (GROBID), read via three passes, take structured notes, or turn papers into interactive agents."
metadata:
  openclaw:
    emoji: "🔬"
    category: "tools"
    subcategory: "document"
    keywords: ["paper reading", "PDF parsing", "academic paper", "deep reading", "annotation", "GROBID"]
    source: "wentor-research-plugins"
---

# Paper Reading Workflow

Use this skill when you need to work through academic papers end to end: acquire and parse the PDF, read it at the right depth, capture structured notes, and optionally turn it into an interactive agent for question-answering, knowledge-graph building, or multi-paper comparison. The pipeline below runs in execution order — parse first, then read, then analyze, then explore.

## 1. Paper Acquisition and Parsing

### Input Sources

| Source | Method | Notes |
|--------|--------|-------|
| Local PDF | Direct file path | Best quality, no network needed |
| DOI | Resolve via CrossRef/Unpaywall | Auto-fetches open access version |
| arXiv ID | `https://arxiv.org/pdf/{id}` | Always available |
| URL | Direct download | May require institutional access |
| OpenAlex ID | OpenAlex API + OA link | Includes metadata |

### Section-Aware Text Extraction (PyMuPDF)

Extract clean text grouped by section using bold + font-size heading heuristics. This handles the common challenges of academic PDFs: two-column layouts, footnotes, headers/footers, embedded equations, and supplementary materials.

```python
import fitz  # PyMuPDF

def extract_sections(pdf_path):
    """Extract text grouped by section; headings detected by bold + font size."""
    doc = fitz.open(pdf_path)
    sections = []
    current = {"heading": "Preamble", "text": ""}
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                text = " ".join(span["text"] for span in line["spans"])
                font_size = max(span["size"] for span in line["spans"])
                is_bold = any("Bold" in span.get("font", "") for span in line["spans"])
                if is_bold and font_size > 11 and len(text.strip()) < 80:
                    if current["text"].strip():
                        sections.append(current)
                    current = {"heading": text.strip(), "text": ""}
                else:
                    current["text"] += text + " "
    if current["text"].strip():
        sections.append(current)
    doc.close()
    return sections
```

### High-Fidelity Parsing with GROBID

For higher-quality structural parsing, use GROBID (GeneRation Of BIbliographic Data). It returns TEI XML with structured sections, author affiliations, parsed references, and figure/table captions, and handles complex layouts better than plain text extraction:

```bash
# Start GROBID server
docker run --rm -p 8070:8070 lfoppiano/grobid:0.8.0

# Parse a paper
curl -X POST "http://localhost:8070/api/processFulltextDocument" \
  -F "input=@paper.pdf" \
  -F "consolidateHeader=1" \
  -F "consolidateCitations=1" \
  -H "Accept: application/xml" \
  -o parsed_paper.xml
```

From either parser, capture the paper's identity (title, authors, affiliations, venue, DOI, page count) and type (empirical / theoretical / review / methods / position). Always keep figure and table captions in the parsed output — they carry most of the information in results-heavy papers.

## 2. Three-Pass Reading

Keshav's three-pass method lets you read at increasing depth and stop early when a paper is not relevant.

### Pass 1: Survey (5-10 minutes)

Read only:
1. Title, abstract, and keywords
2. Introduction (first and last paragraph only)
3. All section headings
4. Conclusion
5. Figure and table captions
6. Reference list (scan for familiar papers)

After Pass 1 you should know: **category** (empirical/theoretical/system/survey), **context** (what related work it builds on), **correctness** (do assumptions and claims seem reasonable), **contributions** (main claimed contributions), and **clarity** (is it well-written).

**Screening card**: while surveying, capture five components — identity (title/authors/venue/DOI/type), core argument (1-2 sentences from abstract + introduction), methods snapshot (design, sample/dataset, key techniques), key findings (3-5 bullets), and relevance assessment (High/Medium/Low, quality signal, and recommended action: deep read / cite only / skip).

**Decision**: stop here if the paper is not relevant; otherwise continue to Pass 2.

### Pass 2: Comprehension (30-60 minutes)

Read the full paper, skipping proofs and complex derivations:
1. Examine figures and tables carefully
2. Mark unread references for later
3. Annotate key claims, methods, and results
4. Summarize each section in one sentence

After Pass 2 you should be able to summarize the main contribution to someone else, identify the key evidence supporting the claims, and list the paper's strengths and weaknesses.

### Pass 3: Recreation (1-4 hours)

For papers central to your research:
1. Mentally re-derive the key results
2. Challenge every assumption; identify implicit ones not stated
3. Think about how you would improve the work
4. Compare the approach to alternatives

### Depth by Paper Type

| Paper Type | Focus On | Time Budget |
|-----------|----------|-------------|
| Seminal paper | Full three-pass reading, every detail | 3-4 hours |
| Survey/review | Section headings, taxonomy, open questions | 1-2 hours |
| Methods paper | Algorithm/procedure, pseudocode, evaluation | 1-2 hours |
| Results paper | Figures, tables, statistical tests, effect sizes | 30-60 min |
| Position paper | Arguments, assumptions, counterarguments | 30-60 min |
| Related work (peripheral) | Abstract + conclusion only (Pass 1) | 5-10 min |

### Critical Analysis Checklist (Pass 2/3)

- **Introduction**: What gap does the paper address? What is the research question or hypothesis?
- **Literature review**: Which theoretical frameworks are invoked? Any notable omissions? How does it position itself against competing approaches?
- **Methodology**: Is the design appropriate for the question? Sample size and power analysis reported and adequate? Threats to internal/external validity? Statistical tests appropriate with assumptions met? Reproducibility — sufficient detail?
- **Results**: Do the results support the claims? Effect sizes reported and meaningful? Confidence intervals vs. p-values? Do figures/tables accurately represent the data? Any signs of p-hacking or selective reporting?
- **Discussion**: Are limitations acknowledged? Are alternative explanations considered? Do conclusions follow logically, or are implications overstated?
- **References**: Extract cited works with metadata, identify seminal references, flag self-citations, and map citation clusters by topic.

## 3. Structured Notes

Use a consistent template for every paper you read so notes stay comparable across your library:

```markdown
# Paper Notes: [Short Title]

## Metadata
- **Title**: Full title
- **Authors**: First Author et al. (Year)
- **Venue**: Conference/Journal
- **DOI/URL**: link
- **Date read**: YYYY-MM-DD

## Summary (2-3 sentences)
What does this paper do, and what are the main findings?

## Problem
What problem does this paper address? Why is it important?

## Method
How do they approach the problem? Key technical details.

## Key Results
- Result 1: ...
- Result 2: ...

## Strengths
- Strength 1: ...

## Weaknesses / Limitations
- Weakness 1: ...

## Questions / Things I Don't Understand
- Question 1: ...

## Relevance to My Work
How does this connect to my research? What can I use?

## Key References to Follow Up
- [Author, Year] - Why it seems relevant
```

Also generate a BibTeX entry for the parsed paper (author, title, journal, year, volume, pages, doi) so it drops straight into your reference manager. Maintain a reading log (papers read, dates, ratings, one-line takeaways), read 2-3 papers per week on a schedule, and end every session by writing one sentence on how the paper relates to your own work.

## 4. AI-Assisted Analysis

### Summarization Prompt

```python
summarize_prompt = """Read the following academic paper and provide:

1. ONE-SENTENCE SUMMARY: The core contribution in a single sentence.
2. KEY FINDINGS (3-5 bullet points): findings with specific numbers/results.
3. METHODOLOGY: Describe the approach in 2-3 sentences.
4. LIMITATIONS: List 2-3 limitations acknowledged or unacknowledged.
5. RELEVANCE: How does this relate to [your research topic]?

Paper text:
{paper_text}"""
```

### Critical Analysis Prompt

```python
critique_prompt = """Analyze the following paper critically:

1. VALIDITY: Are the experimental design and statistical analyses sound?
   Identify any threats to internal/external validity.
2. NOVELTY: What is genuinely new? What is incremental?
3. REPRODUCIBILITY: Could you replicate this study from the description
   given? What information is missing?
4. ALTERNATIVE EXPLANATIONS: Are there alternative interpretations of the
   results that the authors do not consider?
5. FOLLOW-UP QUESTIONS: What would you want to investigate next?

Paper text:
{paper_text}"""
```

## 5. Interactive Exploration: Paper-to-Agent

Traditional reading is linear and passive. Turn a parsed paper into an interactive agent (Paper2Agent-style) that answers questions, explains methodology, and supports replication — valuable for interdisciplinary readers, journal clubs, and students learning critical evaluation. Process the paper through three extraction steps first:

**Step 1: Structure Extraction**
- Identify sections (abstract, introduction, methods, results, discussion, references)
- Extract title, authors, affiliations, venue; detect paper type
- Locate figure/table captions and note supplementary materials

**Step 2: Claim Extraction**
- Identify the primary research question or hypothesis
- Extract all major claims; map each to its supporting evidence (data, citations, arguments)
- Rate evidence strength (strong, moderate, suggestive); note acknowledged limitations

**Step 3: Methodology Mapping**
- Document the complete experimental/analytical pipeline
- Extract parameters, dataset descriptions, evaluation metrics, and software tools
- Note preprocessing/cleaning steps; map the methodology to established frameworks

### Interaction Patterns

- **Question-Answering**: answer content questions with source references; explain technical terms in context; compare the approach to alternatives; generate summaries at different depths (tweet-length, abstract, detailed).
- **Critical Analysis**: evaluate statistical validity; identify unaddressed confounds; check whether conclusions follow from the evidence; compare with related work; suggest follow-up experiments.
- **Replication Assistance**: generate step-by-step replication guides; flag missing details; suggest parameter ranges for robustness checks; create data collection templates; list required resources (compute, data, equipment).

Always verify extracted claims against the original text before presenting them, and flag ambiguous or inconsistent writing in the paper instead of silently guessing.

## 6. Knowledge Graphs and Multi-Paper Analysis

### Knowledge Graph Construction

From one or more processed papers, build a knowledge graph:
- Extract entities: methods, datasets, metrics, tools, concepts
- Map relationships between entities (uses, extends, contradicts, supports)
- Link to external knowledge bases (OpenAlex, CrossRef, DOI)
- Track citation chains for key claims
- Identify research lineages and methodological evolution

### Multi-Paper Comparison

When multiple papers are processed (e.g., a systematic review), compare them:
- Compare methodologies across papers addressing similar questions
- Identify consensus findings and areas of disagreement
- Trace the evolution of a research direction over time
- Build synthesis summaries combining evidence from multiple sources
- Detect gaps in the literature that no existing paper addresses

### Batch Processing

```python
import os, json

def process_paper_batch(pdf_dir, output_file):
    """Parse a directory of PDFs and save structured notes as JSON."""
    results = []
    for filename in os.listdir(pdf_dir):
        if not filename.endswith(".pdf"):
            continue
        sections = extract_sections(os.path.join(pdf_dir, filename))
        title = sections[0]["heading"] if sections else filename
        abstract = next((s["text"].strip() for s in sections
                         if "abstract" in s["heading"].lower()), "")
        results.append({
            "filename": filename, "title": title, "abstract": abstract,
            "num_sections": len(sections),
            "total_chars": sum(len(s["text"]) for s in sections),
        })
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    return results
```

Use the same note template for every paper in the batch so the comparison matrix aligns across columns like methods, sample size, key finding, and relevance.

## 7. Tools and Integration

### Annotation Tools Comparison

| Tool | Platform | Highlights | PDF Annotation | AI Features | Collaboration |
|------|----------|-----------|---------------|-------------|---------------|
| Zotero + ZotFile | All | Reference management + PDF | Yes | No (plugins available) | Group libraries |
| Paperpile | Web/Chrome | Google Docs integration | Yes | No | Shared folders |
| ReadCube Papers | All | Smart citations | Yes | Recommendations | Shared libraries |
| Semantic Reader | Web | AI-augmented reading | Yes | Inline explanations, TLDRs | No |
| Elicit | Web | AI paper search | No | Automated extraction | Tables |
| Scholarcy | Web | Flashcard summaries | Yes | Auto-summarization | No |

### Integration with Other Skills

- Use literature search skills to find papers for processing
- Feed extracted knowledge into writing skills for literature reviews
- Connect methodology details to analysis skills for replication
- Store parsed papers in a local knowledge base for future reference
- Generate citation entries compatible with reference management tools

## Pitfalls

- Heading heuristics (bold + font size) fail on some publisher templates — verify section boundaries against the paper's table of contents.
- GROBID needs a running server (Docker/Java); curl calls fail with connection errors if you skip the startup step.
- Don't skip Pass 1's decision gate — most papers only deserve a survey read.
- Never present extracted claims without verifying them against the original text.
- Drop figure/table captions from the parse and you lose most of a results-heavy paper's information.
- For theoretical papers, prioritize definitions, theorems, and proof sketches over narrative text.
- Comparing papers requires the same note template, or the fields won't align.
- Two-column PDFs confuse naive text extraction — prefer GROBID for those layouts.
- Flag ambiguous or inconsistent writing instead of silently guessing at the author's intent.

## References

- GROBID: https://github.com/kermitt2/grobid
- PyMuPDF: https://pymupdf.readthedocs.io
- OpenAlex API: https://api.openalex.org
- Unpaywall API: https://unpaywall.org/products/api
- S. Keshav, "How to Read a Paper" (2007): http://ccr.sigcomm.org/online/files/p83-keshavA.pdf

Longer content (e.g., extended prompt libraries or per-field annotation tool deep-dives) can live in `references/` files within this skill directory if the main file grows beyond comfortable size.
