---
name: large-doc-mastery
description: >
  Large document and codebase synthesis skill. Activates when the user provides
  50k–200k+ tokens of context — codebases, PDFs, legal documents, transcripts,
  research corpora — and needs synthesis, cross-referencing, or insight extraction
  with perfect recall across the entire context. Not a summarizer. A precision
  instrument for finding patterns, contradictions, dependencies, and insights that
  only emerge when you hold the whole thing at once.
  Use when user says: analyze this codebase, read this whole document, find all
  references to X, synthesize across sections, what does this say about Y, find
  contradictions, extract all decisions, map the dependencies, read the whole thing,
  cross-reference, audit the entire document, what changed between sections,
  find every mention of, trace this through the code, what's missing.
  Do NOT activate for: small documents where a direct answer is more useful,
  tasks that don't require cross-document reasoning.
  First response: "Large Document Mode active. Paste or attach your document(s).
  Tell me the synthesis goal — what insight, decision, or structure you're after."
license: Apache 2.0
---

# Large Document / Codebase Mastery

Summaries lose information. "Analyze this 80k-token codebase" with no structure
produces a vague paragraph about architecture that misses the three critical bugs
and the two deprecated modules that half the new code still imports.

The skill is not consuming large context — Claude does that automatically. The skill
is structuring the task so the synthesis is precise: specific questions, specific
output formats, explicit cross-reference instructions, and verification passes that
confirm the model used the actual document rather than its priors.

---

## SLASH COMMANDS

| Command | Action |
| --- | --- |
| `/map` | Build a structural map of the document (sections, components, entities) |
| `/index <topic>` | Find every location in the document that touches a specific topic |
| `/extract <type>` | Extract all instances of a type: decisions, risks, assumptions, TODOs, etc. |
| `/cross-ref <a> <b>` | Find all connections between two topics, sections, or entities |
| `/contradictions` | Surface any internal contradictions or inconsistencies in the document |
| `/gaps` | Identify what's absent — what the document should address but doesn't |
| `/trace <entity>` | Follow an entity (function, concept, person, requirement) through the full document |
| `/timeline` | Extract a chronological sequence of events, changes, or decisions |
| `/compare <section-a> <section-b>` | Directly compare two sections or files |
| `/synthesize <question>` | Answer a specific question using the full document as context |
| `/verify <claim>` | Check whether a specific claim is supported by the document |
| `/hotspots` | Identify the highest-complexity or highest-risk areas |
| `/summary-lossy` | Produce a short summary with explicit list of what was dropped |

---

## HIGH-LEVEL WORKFLOW

```text
User provides large document / codebase
    │
    ├─ Phase 1: Document Orientation
    │     Build structural map; identify key entities and sections
    │
    ├─ Phase 2: Scope Definition
    │     Clarify the synthesis goal — don't analyze everything equally
    │
    ├─ Phase 3: Targeted Extraction
    │     Pull specific patterns, entities, or facts with location references
    │
    ├─ Phase 4: Cross-Reference Pass
    │     Connect extracted elements across sections or files
    │
    ├─ Phase 5: Synthesis
    │     Answer the synthesis question with evidence citations
    │
    └─ Phase 6: Verification
          Confirm claims are in the document, not in prior knowledge
```

---

## PHASE 1 — DOCUMENT ORIENTATION

Before any analysis, build an orientation map. This prevents anchor bias —
where the first section dominates the analysis and the rest is skimmed.

### Orientation map format

```text
DOCUMENT MAP: [title / description]
Total scope: [estimated sections / files / pages]

STRUCTURE
  [Section/File 1]: [1-line description] — [key entities defined]
  [Section/File 2]: [1-line description] — [key entities defined]
  ...

KEY ENTITIES
  [Entity type]: [list] — (e.g., Functions, Classes, Requirements, Actors)

DENSITY DISTRIBUTION
  Heavy:    [sections with most content / complexity]
  Light:    [sections with least content]
  Missing:  [sections referenced but absent]
```

---

## PHASE 2 — SCOPE DEFINITION

Large documents contain far more than any single analysis needs. Before extracting,
define the synthesis aperture — what lens is this analysis using?

### Synthesis aperture types

| Aperture | Question being answered | Best for |
| --- | --- | --- |
| **Decision audit** | What decisions were made, by whom, and why? | Meeting transcripts, PRDs, ADRs |
| **Risk surface** | What can go wrong, and where? | Architecture docs, contracts, plans |
| **Dependency map** | What depends on what? | Codebases, system designs |
| **Consistency check** | Does the document contradict itself? | Legal docs, specs, policies |
| **Entity trace** | How does X evolve through the document? | Code, narratives, regulations |
| **Gap analysis** | What's missing that should be here? | Requirements, audits |
| **Change surface** | What changed between versions / sections? | Diffs, revisions, amendments |

### Scope question rules
- Ask ONE scope-defining question if the synthesis goal is ambiguous
- If the user says "analyze everything," default to: Risk surface + Dependency map
- Never attempt all apertures simultaneously — output becomes noise

---

## PHASE 3 — TARGETED EXTRACTION

Extract with location anchors. Every extracted element must cite where it came from.

### Extraction format

```text
EXTRACTION: [type] — [aperture]

[ID]. [Extracted element]
     Location: [section / file / line / page]
     Context:  [1 sentence: surrounding context that makes this significant]
     Flags:    [RISK | DECISION | ASSUMPTION | TODO | CONTRADICTION | DEPENDENCY]
```

### Extraction rules
- **Cite location for every item.** Uncited extractions cannot be verified.
- **Do not paraphrase.** Quote directly, then interpret in the Context field.
- **Flag before filtering.** Extract everything matching the type, then rank.
- **Note absences.** If a required element (e.g., error handling, auth check) is absent, flag as MISSING.
- **Distinguish document claims from your inferences.** Use "The document states..." vs "This implies..."

### High-value extraction targets by document type

| Document type | High-value extraction targets |
| --- | --- |
| Codebase | TODO/FIXME, dead code, circular deps, missing error handling, hardcoded values |
| Legal / contract | Obligations, conditions, termination clauses, liability caps, ambiguous definitions |
| PRD / spec | Unverified assumptions, missing acceptance criteria, conflicting requirements |
| Research / report | Methodology limitations, sample sizes, confidence intervals, conflicting findings |
| Architecture doc | Single points of failure, unstated assumptions, missing components |

---

## PHASE 4 — CROSS-REFERENCE PASS

The insight that justifies large-context analysis only appears when you connect
elements that are far apart in the document.

### Cross-reference format

```text
CROSS-REFERENCE: [entity A] ↔ [entity B]

Connection 1:
  [Entity A] location: [cite]
  [Entity B] location: [cite]
  Relationship: [DEPENDS_ON | CONTRADICTS | MODIFIES | REFERENCES | UNDEFINED]
  Significance: [1 sentence: why this connection matters]

Connection 2:
  ...

SUMMARY
  Total connections found: [N]
  Critical connections (high-risk or decision-affecting): [list]
  Unresolved: [connections implied but not made explicit in the document]
```

### Cross-reference rules
- Always cite both locations — without both citations, the connection cannot be verified
- `CONTRADICTS` always surfaces first — contradictions are the highest-value finding
- `UNDEFINED` means the relationship exists but the document doesn't specify it — flag these

---

## PHASE 5 — SYNTHESIS

Answer the synthesis question using the extracted and cross-referenced evidence.

### Synthesis output format

```text
SYNTHESIS: [question / aperture]

FINDING
[Direct answer in 1–3 sentences]

EVIDENCE
1. [claim] — Source: [location]
2. [claim] — Source: [location]
3. [claim] — Source: [location]

PATTERNS
[Cross-document pattern that only appears with full context]

ANOMALIES
[Elements that don't fit the pattern; outliers; exceptions]

CONFIDENCE
[HIGH / MEDIUM / LOW] — [1 sentence: what limits confidence]

WHAT'S NOT IN THE DOCUMENT
[What the synthesis question required but the document doesn't contain]
```

---

## PHASE 6 — VERIFICATION

After synthesis, run a verification pass to confirm the output is document-grounded.

### Verification checklist

For each major claim in the synthesis:
- [ ] Can I cite the exact location in the document where this appears?
- [ ] Am I paraphrasing accurately, or am I inferring beyond what's stated?
- [ ] Is this in the document, or is it from my training data?
- [ ] If I'm connecting two things, are both connections cited?

### Verification format

```text
VERIFICATION PASS

Claim: "[claim from synthesis]"
  Status: DOCUMENT-GROUNDED | INFERENCE | TRAINING KNOWLEDGE
  Citation: [location, or NONE]
  Note: [if inference or training knowledge: flag for user review]
```

### Common verification failures in large-context tasks

| Failure | Signal | Fix |
| --- | --- | --- |
| Prior contamination | Claim is true but not in the document | Flag as TRAINING KNOWLEDGE |
| Location drift | Cited location doesn't contain the claim | Re-read and re-cite |
| Paraphrase inflation | Summary adds meaning the original doesn't have | Quote directly |
| Recency bias | Last section dominates synthesis | Re-run extraction on early sections |
| Gap hallucination | Document "says" something it actually omits | Add to WHAT'S NOT IN THE DOCUMENT |
