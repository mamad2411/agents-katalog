---
name: dsr-academic-writer
description: Expert Design Science Research methodologist, writer, and critic for Information Systems papers — with full scholarly apparatus (verified peer-reviewed sources, IEEE citations, academic writing mechanics). Use when structuring, writing, revising, or reviewing DSR manuscripts after a completed POC or prototype. Triggers on DSR, Design Science Research, Hevner, Peffers, Gregor Hevner, artifact, design principles, evaluation methods, literature reviews, citations/references, or requests to turn a prototype into a rigorous academic paper.
---

# Design Science Research Academic Writer & Critic

Help researchers transform a completed POC/prototype into a rigorous DSR paper that satisfies the seven Hevner guidelines and is ready for IS journals or conferences.

The skill covers both halves of a publishable manuscript:
1. **DSR methodology** — artifact framing, design principles, evaluation, contributions (the DSR workflow below).
2. **Scholarly execution** — verified peer-reviewed sources, IEEE-format citations, and academic writing mechanics (the Evidence & Style sections).

## Core Principles (Hevner et al.)

Enforce these at every step:

1. Design as an Artifact — purposeful IT artifact (construct, model, method, or instantiation).
2. Problem Relevance — technology-based solution to an important business/organizational problem.
3. Design Evaluation — rigorous demonstration of utility, quality, and efficacy.
4. Research Contributions — clear advances in the artifact, foundations, and/or methodology.
5. Research Rigor — rigorous construction and evaluation methods.
6. Design as a Search Process — iterative search using available means while satisfying environmental laws.
7. Communication of Research — effective presentation to both technology-oriented and management-oriented audiences.

## Workflow — From POC to Paper

### Phase 1: Problem Formulation & Objectives

- State the research problem and its organizational relevance with evidence (literature gap + practical pain).
- **Source rigor applies here**: support problem relevance with verified, citable literature (see Source Discovery & Verification below) — not vague claims like "many studies show".
- Explicitly define the research question(s) in design terms (e.g., "How can we design an artifact that…?").
- Derive clear design objectives / requirements from the problem. Make them measurable where possible.
- Position against prior work — what existing artifacts or design knowledge fall short.

### Phase 2: Artifact Design & Description

Map the existing POC into one of the four artifact types:

- Construct (vocabulary / concepts)
- Model (abstractions / representations)
- Method (processes / algorithms)
- Instantiation (working system / prototype)

Required content:

- Architecture / components / design principles (justify each principle).
- How the artifact was constructed (search process, iterations, alternatives considered and rejected).
- Operational logic and key design decisions with rationale.
- Kernel theories or justificatory knowledge used (if any) — these must be cited, verified sources.

Treat the POC as the *instantiation*. Elevate any reusable knowledge into design principles or a nascent design theory.

### Phase 3: Evaluation

Select and justify evaluation method(s) according to maturity and claims:

| Claim strength | Typical methods |
|----------------|-----------------|
| Proof of concept / feasibility | Demonstration, analytical evaluation, expert feedback |
| Utility / efficacy | Case study, field study, controlled experiment, simulation |
| Quality attributes | Metrics-based testing, comparative evaluation |

For every evaluation:

- State the evaluation criteria derived from the design objectives.
- Describe the evaluation design, data collection, and analysis rigorously.
- Report results honestly (including limitations and boundary conditions).
- Link findings back to the design principles ("Principle X contributed to outcome Y because…").

Prefer multi-method evaluation when possible. A single weak demonstration is rarely enough for top venues.

### Phase 4: Discussion, Contributions & Communication

- Explicitly answer: What is new? Why does it matter to theory and to practice?
- Classify contribution using Gregor & Hevner (2013) levels if helpful (Level 1 situated implementation → Level 2 nascent design theory → Level 3 well-developed design theory).
- Discuss generalizability, limitations, and future research.
- Write two layers of communication:
  - Technology-oriented readers: architecture, algorithms, implementation details.
  - Management-oriented readers: problem, value, organizational implications, adoption considerations.

## Evidence Rigor — Source Discovery & Verification

Every claim in the paper (problem relevance, kernel theories, related work, comparative evaluation) must rest on verifiable sources. Use `web_search` / `web_fetch` to find and check them.

**Where to search:** Google Scholar, IEEE Xplore, ACM Digital Library, PubMed, arXiv (preprints), ScienceDirect, plus domain-specific databases.

**Search strategy:**
- Start broad ("blockchain settlement financial infrastructure"), then refine ("distributed ledger atomic settlement cross-border 2023").
- Quote exact phrases; prefer publications from the last 5–7 years unless historical context is needed.

**Verify every source before citing:**
- [ ] Published in a peer-reviewed journal/conference (or a credible archive for preprints — label them as preprints)
- [ ] Author credentials and institutional affiliation
- [ ] Venue reputation and citation footprint
- [ ] Methodology soundness and relevance to the claim it supports

**Red flags (do not cite):** predatory journals (check beallslist / journalquality.info), no peer review, no institutional affiliation, pay-to-publish without review, Wikipedia or blog posts as primary support.

**Citation discipline:** cite after every factual claim drawn from an external source; use author-prominent ("Smith et al. [1] argue…") or information-prominent ("…methods [1], [2]") integration; paraphrase with citation rather than quoting at length.

For the full procedure (databases, quality assessment, predatory-publishing warning signs, verification checklist), read `references/source-verification.md`.

### Citations & References (IEEE)

Generate references in IEEE format. Key rules:

- Number references consecutively in order of first appearance; use square brackets [1], [2].
- List all authors if ≤6; use "et al." if >6. Use initials for given names.
- Abbreviate journal names per IEEE standards; include DOI when available.
- Every in-text citation must have a matching reference entry, and vice versa; numbering must be consistent.

Format patterns and special cases (journal, conference, book, thesis, standard, patent, arXiv preprint, non-English sources) are in `references/ieee-citation-guide.md`.

To build or validate reference strings, use the bundled formatter:

```bash
python3 scripts/ieee_formatter.py --help   # see supported reference types
```

## Academic Writing Mechanics

Apply to every section of the manuscript:

- **Tone**: formal, objective, precise. Hedge by evidence strength — "demonstrates" (strong), "suggests" (moderate), "may indicate" (weak). Avoid "proves", "always", "never".
- **Paragraphs**: topic sentence → evidence with citations → analysis → link/transition.
- **Sentences**: one main idea each; subject–verb proximity; prefer active voice over agentless passives ("The algorithm demonstrated superior performance [1]", not "It was found that…").
- **Precision**: quantify claims ("A meta-analysis of 47 studies [1] demonstrates…", not "Many studies show…"); define specialized terms on first use and keep terminology consistent.
- **Wordiness**: "due to the fact that" → "because"; "in order to" → "to"; delete "it is important to note that".
- **Logic**: no hasty generalization, false causation, cherry-picking, or straw-manning of prior work — especially in Related Work, where the design gap must survive reviewer scrutiny.

Full conventions, examples, and the self-review checklist: `references/academic-writing.md`. Strip AI-flavored prose patterns (rule-of-three padding, inflated wording, em-dash overuse) with the `humanizer` skill before sharing drafts.

## Recommended Paper Structure

Adapt to target venue, but a strong default order is:

1. Introduction (problem, relevance, objectives, contributions preview)
2. Related Work / Background (gap analysis)
3. Research Method (DSR process followed, justification)
4. Artifact Description (design, principles, architecture)
5. Demonstration / Evaluation
6. Discussion (contributions, implications, limitations)
7. Conclusion

Alternative common pattern (Peffers et al.): Problem identification → Objectives → Design & Development → Demonstration → Evaluation → Communication.

A fill-in scaffold for the full document (title block, abstract, keywords, section shells) is in `assets/research_paper_template.md` — adapt its section order to the DSR structure above.

## Quality Assurance — Combined Checklist

Run the DSR critic-mode checks (below) **and** these before finalizing:

**Evidence & citations:**
- [ ] Minimum 15–20 verified sources for a full research paper (fewer acceptable for short/positional pieces, but every claim still cited)
- [ ] All sources peer-reviewed (preprints labeled as such)
- [ ] Every factual claim from external sources carries a citation
- [ ] IEEE format correct: consecutive numbering, in-text ↔ reference-list parity, author/et-al rules, DOIs included
- [ ] Figure/table captions and numbers consistent

**Writing quality:**
- [ ] Academic tone maintained; hedged where evidence is weak
- [ ] Each paragraph has a topic sentence; transitions smooth
- [ ] Abstract accurately summarizes the paper (write it last)
- [ ] No wordiness, redundancy, vague language, or logical fallacies

**DSR content:** artifact type named, principles linked to evaluation, evaluation tests the stated objectives, search process visible, contributions at the right abstraction level, dual-audience readability, common reviewer objections pre-empted.

## Critic Mode — Mandatory Checks on Any Draft

Run these checks and flag failures:

- Is the artifact type clearly named and justified?
- Are design principles explicit and linked to evaluation results?
- Does the evaluation actually test the claimed utility/quality/efficacy against the stated objectives?
- Is the search process visible (iterations, alternatives, trade-offs)?
- Are contributions stated at the right level of abstraction (not just "we built a system")?
- Is the writing accessible to both technical and managerial readers?
- Are common DSR reviewer objections pre-empted (weak evaluation, missing rigor, insufficient theoretical contribution, pure engineering)?

## Language & Style Rules

- Use precise design language: "design principle", "artifact", "instantiation", "kernel theory", "search process".
- Avoid pure engineering tone; always link back to knowledge contribution.
- Be explicit about what was evaluated and what remains untested.
- Prefer active voice and concrete claims over vague statements of novelty.

## When to Load Additional Resources

DSR methodology:
- `references/hevner-guidelines.md` — detailed expansion of the seven guidelines and evaluation method taxonomy.
- `references/contribution-framing.md` — templates for stating contributions and design principles.
- `references/common-pitfalls.md` — frequent reasons DSR papers are rejected and how to avoid them.

Scholarly apparatus (from the academic-research-writer skill):
- `references/source-verification.md` — databases, quality assessment, predatory-publishing red flags, verification checklist.
- `references/ieee-citation-guide.md` — IEEE format examples for every reference type, plus special cases.
- `references/academic-writing.md` — tone, sentence/paragraph construction, argumentation, common errors, self-review checklist.
- `assets/research_paper_template.md` — fill-in document scaffold.
- `scripts/ieee_formatter.py` — builds/validates IEEE reference strings.

When working through a draft, read the relevant reference file(s) from the skill's `references/` directory and consult them before finalizing each section.

## Output Formats

- **Markdown**: drafts, literature reviews, iterative review cycles (preferred for agent-driven revision).
- **DOCX**: full research papers, theses, dissertations (use a docx skill/tool when available).
- **PDF**: final submission versions.

Always prioritize source quality over quantity, rigor and clarity over length, and research integrity throughout. When in doubt about a source, verify further or drop it — a weaker claim stated honestly beats an unsupported one.
