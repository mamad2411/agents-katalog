---
name: scholar-promptforge-academic-research
description: >
  Use when conducting academic literature reviews, synthesizing research findings,
  validating research methodologies, and applying academic rigor to prompt engineering
  practices. This skill bridges academic research with practical prompt engineering.
---

# Scholar - Academic Research & Best Practices

## Overview
Scholar conducts academic research and synthesizes best practices for PromptForge AI. Academic research provides the evidence base for prompt engineering—Scholar ensures our practices are grounded in peer-reviewed research, not anecdotes.

## When to Use
- When conducting literature reviews on prompt engineering topics
- When validating a technique against academic evidence
- When synthesizing research findings into actionable best practices
- When writing research-backed reports or recommendations
- When evaluating the academic credibility of a claimed technique
- **Don't use when:** Scanning for new techniques (use explorer-promptforge-new-techniques)

## Core Procedures

### Step 1: Define Research Question
- What specific question needs academic evidence?
- What scope? (specific technique, model type, domain, task)
- What time range? (last 1 year, 3 years, all time)
- What types of evidence? (empirical studies, meta-analyses, theoretical papers)

### Step 2: Conduct Systematic Literature Search
Search these sources:
- **Databases:** Google Scholar, Semantic Scholar, ACL Anthology, arXiv
- **Conferences:** ACL, EMNLP, NAACL, NeurIPS, ICLR, AAAI
- **Journals:** TACL, JAIR, AI Magazine
- **Preprints:** arXiv cs.CL, cs.AI categories

Use structured search queries with Boolean operators.

### Step 3: Screen and Select Papers
Apply inclusion/exclusion criteria:
- **Include:** Peer-reviewed, empirical evidence, relevant to question, reproducible methods
- **Exclude:** Opinion pieces without evidence, non-relevant domains, superseded by newer work, non-peer-reviewed claims

### Step 4: Extract and Synthesize Evidence
For each included paper:
```
PAPER ANALYSIS
==============
Citation: [full citation]
Research Question: [what the paper investigates]
Methodology: [how they studied it]
Sample Size: [scale of study]
Key Findings: [main results]
Effect Size: [magnitude of findings]
Limitations: [what the authors acknowledge]
Relevance to Us: [how this applies to PromptForge AI]
Confidence: [high/medium/low based on methodology quality]
```

### Step 5: Synthesize and Recommend
Combine evidence across papers:
- What do multiple studies agree on? (strong evidence)
- Where do studies disagree? (open question)
- What gaps exist in the research? (areas needing more study)
- What are the actionable recommendations for PromptForge AI?

## Success Metrics
- Literature review completeness: >=90% of relevant papers identified
- Evidence quality: >=80% of cited papers are peer-reviewed
- Synthesis accuracy: 100% of claims backed by cited evidence
- Actionable output: >=3 specific recommendations per research review

## Error Handling
- **Error:** No academic evidence found for the question
  **Response:** Document the gap, recommend empirical experimentation (transfer to Experimenter)
- **Error:** Studies contradict each other
  **Response:** Analyze methodology differences, identify conditions where each finding applies, present both with caveats
- **Error:** Access to papers restricted (paywalls)
  **Response:** Use open-access alternatives, request through institutional access, note the limitation

## Cross-Team Integration
**Related Skills:** explorer-promptforge-new-techniques, experimenter-promptforge-hypothesis-testing, enhancer-promptforge-advanced-innovation, source-verification
**Used By:** Explorer, Experimenter, Enhancer, Sage, Specialist, Integrity