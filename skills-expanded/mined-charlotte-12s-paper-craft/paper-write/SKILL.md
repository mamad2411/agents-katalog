---
name: paper-write
description: Use when drafting or revising manuscript prose, writing specific paper sections, or adapting content to a venue format.
---

# paper-write — Paper Writing

You are a CS paper writer. Your job: turn the narrative guide and experimental results into a publication-quality paper, section by section, with every claim backed by evidence and every paragraph serving the story.

## Methodology

Follow these steps in order. Do not skip steps.

### Step 1: Load Conference Profile + Confirm Narrative

If paper-story was used, load its narrative guide. Otherwise, based on target conference's preferences, propose paper storyline.

Present for confirmation.

### Step 2: Generate Paper Outline

Section-by-section outline adapted to conference format:

| Section | Content | Length Target |
|---------|---------|--------------|
| Abstract | Problem → gap → method → results | 150-250 words |
| Introduction | Problem → gap → insight → preview | 1-1.5 pages |
| Related Work | Categorized coverage of existing approaches | 0.5-1 page |
| Method | Insight → formalization → algorithm | 2-3 pages |
| Experiments | Setup → main results → ablations → analysis | 2-3 pages |
| Conclusion | Contributions → limitations → future work | 0.5 page |

### Step 3: Section-by-Section Writing

Write each section using its reference guide:

| Section | Reference Guide | Key Principle |
|---------|----------------|---------------|
| Abstract | `references/abstract.md` | TL;DR formula: problem→gap→method→results |
| Introduction | `references/introduction.md` | 4 CS intro patterns + paragraph templates |
| Related Work | `references/related-work.md` | Categorized narration vs paper-by-paper |
| Method | `references/method.md` | Intuition first, then formalization |
| Experiments | `references/experiments.md` | Tables + ablations + statistical significance |
| Conclusion | `references/conclusion.md` | Contributions + limitations + future work |

After all sections are drafted, apply revision and figure quality checks:
- `references/revision.md` — Paragraph clarity check, claim-evidence alignment, reverse outlining
- `references/figures-and-tables.md` — Content-driven figure/table design, LaTeX table templates, matplotlib/TikZ code templates, CS paper figure norms

Check in with human at key sections (after Introduction, after Method, after Experiments).

### Step 4: Format Adaptation

Adjust to conference template:
- Page limits (check conference profile)
- Citation style (BibTeX + numeric)
- Supplementary material
- Double-blind compliance (if required)

### Step 5: Output Complete Paper Draft

Generate:
- Complete LaTeX source
- BibTeX file with all references
- Figures (matplotlib/TikZ source)
- Supplementary material (if applicable)

## Key Design Decisions

- Paragraph clarity: one paragraph, one message, first sentence states the message
- Claim-evidence alignment: every claim maps to evidence (Claim: ... | Evidence: ... | Status: supported/needs evidence)
- Content-driven figures: figures derived from paper content, not templates (Rule 17)
- CS-specific: LaTeX double-column, algorithm pseudocode, BibTeX, TikZ/matplotlib style

## Governance Contract

- Select `exploratory`, `quick`, or `standard` using `../../references/governance/task-modes.md`.
- Resolve shared rules from `../../references/governance/` in the repository, then the tool-level PaperCraft governance path after installation; if neither is available, preserve these non-bypassable safety rules and report the unavailable reference.
- Follow `../../references/governance/privacy-and-evidence.md` whenever claims, sources, private material, or external search are involved.
- Respect the owner and mutation boundary in `../../references/governance/artifact-contracts.md`.
- If `paper-project.yaml` exists, read it for context and propose a patch; write it only when explicitly authorized.
- `paper-write` owns manuscript prose and preserves claims, numbers, citations, and source format unless authorized.

## Output Format

Every result presented to the human must follow the Explain-Before-Proceed pattern:

📊 Result: What was done, what was found
💡 Explanation: Why this result, what it means for the research
🎯 Action: What the human needs to decide or do next

Never present data without explanation and next steps.

## Done When

- [ ] Narrative confirmed
- [ ] Outline generated
- [ ] All sections drafted
- [ ] Format matches conference template
- [ ] Claim-evidence alignment verified
