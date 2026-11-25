---
name: explorer-promptforge-new-techniques
description: >
  Use when researching, evaluating, and integrating emerging prompt engineering
  techniques, AI methodologies, and industry innovations. This skill provides
  systematic exploration frameworks for discovering and assessing new approaches
  before they become mainstream.
---

# Explorer - New Techniques & Methodologies

## Overview
Explorer researches and evaluates emerging prompt engineering techniques for PromptForge AI. The AI field moves fast—Explorer ensures PromptForge AI adopts valuable innovations early while avoiding hype-driven dead ends.

## When to Use
- When new prompt techniques are announced (papers, blogs, conferences)
- When evaluating whether to adopt a trending methodology
- When scanning the competitive landscape for innovation
- When building a technology radar for prompt engineering
- When asked "what's new in prompt engineering?"
- **Don't use when:** Optimizing existing techniques (use enhancer-promptforge-advanced-innovation)

## Core Procedures

### Step 1: Scan for Emerging Techniques
Monitor these sources:
- **Academic:** arXiv, ACL, NeurIPS, ICLR papers on prompting
- **Industry:** OpenAI, Anthropic, Google, Meta research blogs
- **Community:** GitHub trending, Reddit r/PromptEngineering, Twitter/X thought leaders
- **Competitors:** What are other prompt engineering companies adopting?
- **Tools:** New prompt libraries, frameworks, and platforms

### Step 2: Triage and Filter
For each new technique discovered:
- **Novelty:** Is this genuinely new or a repackaging of existing work?
- **Credibility:** Peer-reviewed? Reproduced by others? From reputable source?
- **Relevance:** Does this apply to PromptForge AI's work?
- **Maturity:** Research paper, prototype, production-ready?
- **Effort:** How much work to evaluate and potentially adopt?

Score each technique: High/Medium/Low priority for investigation.

### Step 3: Deep Dive Investigation
For High-priority techniques:
1. Read the original paper/documentation thoroughly
2. Understand the core mechanism (why does it work?)
3. Identify prerequisites and constraints
4. Find independent reproductions or critiques
5. Assess potential impact on current practices

### Step 4: Preliminary Evaluation
Quick proof-of-concept to validate claims:
- Implement the technique on a small test set
- Compare against current best practice
- Measure: quality improvement, cost change, speed change
- Document: what worked, what didn't, surprises

### Step 5: Recommend and Transfer
```
TECHNIQUE EVALUATION
====================
Technique: [name and source]
Summary: [what it does in 2-3 sentences]
Novelty: [what's new about it]
Credibility: [evidence quality]
Preliminary Results: [PoC findings]
Recommendation: [adopt/investigate further/monitor/reject]
Next Steps: [if adopt: integration plan; if investigate: full experiment]
Transfer To: [experimenter for testing, enhancer for refinement, or archivist for knowledge base]
```

## Success Metrics
- New techniques identified: >=5 per month
- Evaluation completion rate: >=80% of triaged techniques reach preliminary evaluation
- Adoption rate: >=20% of evaluated techniques are adopted
- Time to awareness: <2 weeks from technique announcement to identification

## Error Handling
- **Error:** Technique claims are exaggerated or false
  **Response:** Document the discrepancy, share as cautionary example, improve source credibility scoring
- **Error:** Technique works in paper but not in practice
  **Response:** Investigate gap between paper conditions and real conditions, document findings
- **Error:** Too many techniques to evaluate (overwhelming pipeline)
  **Response:** Raise triage threshold, focus only on High-priority, delegate Medium to Scholar

## Cross-Team Integration
**Related Skills:** experimenter-promptforge-hypothesis-testing, scholar-promptforge-academic-research, enhancer-promptforge-advanced-innovation, trend-monitoring
**Used By:** Experimenter, Scholar, Enhancer, Sage, Specialist