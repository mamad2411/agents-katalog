---
name: source-credibility
description: Evaluate academic and technical source credibility. Distinguishes peer-reviewed journals, vetted preprints, technical blog posts, and marketing claims.
license: MIT
---

# Source Credibility Evaluation

Use this skill when triaging claims, citations, or newly discovered sources.

## Credibility Hierarchy

1. **Tier 1 (Highest)**:
   - Peer-reviewed archival conference proceedings (NeurIPS, ICML, ICLR, CVPR, ACL).
   - High-impact peer-reviewed biomedical journals (Nature, Science, Cell, NEJM, Lancet).
   - Artifact-backed releases with public code, weights, and replication logs.

2. **Tier 2 (High)**:
   - Major institutional preprints (arXiv, bioRxiv, medRxiv) from established research labs (DeepMind, Anthropic, FAIR, OpenAI, Stanford, MIT, Broad Institute).
   - Official technical reports accompanied by detailed evaluation harnesses.

3. **Tier 3 (Moderate)**:
   - Unverified independent preprints.
   - Engineering blog posts with reproduction steps or code notebooks.

4. **Tier 4 (Low / Skeptical)**:
   - Marketing press releases, non-technical executive summaries, social media threads without links to source papers or code.

## Evaluation Checklist
- [ ] Is there an identifiable author and institution?
- [ ] Are hyperparameters, training compute, and seeds disclosed?
- [ ] Are baseline comparisons apples-to-apples?
- [ ] Are claims tested across multiple benchmarks or cherry-picked?
