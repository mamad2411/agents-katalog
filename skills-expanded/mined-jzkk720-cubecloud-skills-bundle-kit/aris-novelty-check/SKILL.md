---
name: aris-novelty-check
description: Verify research idea novelty against recent literature. Use when user says "novelty check", "check novelty", "has anyone done this", or wants to verify a research idea is novel before implementing. Ported from wanshuiyin/Auto-claude-code-research-in-sleep (ARIS) — methodology only, Claude-Code-specific MCP deps stripped for VS Code Copilot.
---

# Novelty Check Skill

Check whether a proposed method/idea has already been done in the literature.

The user will provide the method or idea description as part of their request.

## Instructions

Given a method description, systematically verify its novelty:

### Phase A: Extract Key Claims
1. Read the user's method description
2. Identify 3-5 core technical claims that would need to be novel:
   - What is the method?
   - What problem does it solve?
   - What is the mechanism?
   - What makes it different from obvious baselines?

### Phase B: Multi-Source Literature Search
For EACH core claim, search using all available web sources:

1. **Web Search**:
   - Search arXiv, Google Scholar, Semantic Scholar
   - Use specific technical terms from the claim
   - Try at least 3 different query formulations per claim
   - Include year filters for recent work (last 2 years)

2. **Known paper databases**: Check against:
   - Recent conference proceedings (ICLR, NeurIPS, ICML, ACL, CVPR, etc.)
   - Recent arXiv preprints

3. **Read abstracts**: For each potentially overlapping paper, fetch its abstract and related work section

### Phase C: Self-Review Verification
After gathering the literature, perform a critical self-review of novelty:

1. Write a dossier (e.g., `NOVELTY_DOSSIER.md`) containing:
   - The proposed method description
   - All papers found in Phase B
   - The question: "Is this method novel? What is the closest prior work? What is the delta?"

2. Review the dossier critically, acting as a skeptical reviewer:
   - For each claim, identify the closest prior work
   - Determine the actual delta (what is genuinely new vs. incremental)
   - Consider whether a reviewer would cite the prior work as making this redundant

### Phase D: Novelty Report
Output a structured report:

```markdown
## Novelty Check Report

### Proposed Method
[1-2 sentence description]

### Core Claims
1. [Claim 1] — Novelty: HIGH/MEDIUM/LOW — Closest: [paper]
2. [Claim 2] — Novelty: HIGH/MEDIUM/LOW — Closest: [paper]
...

### Closest Prior Work
| Paper | Year | Venue | Overlap | Key Difference |
|-------|------|-------|---------|----------------|

### Overall Novelty Assessment
- Score: X/10
- Recommendation: PROCEED / PROCEED WITH CAUTION / ABANDON
- Key differentiator: [what makes this unique, if any]
- Risk: [what a reviewer would cite as prior work]

### Suggested Positioning
[How to frame the contribution to maximize novelty perception]
```

### Important Rules
- Be BRUTALLY honest — false novelty claims waste months of research time
- "Applying X to Y" is NOT novel unless the application reveals surprising insights
- Check both the method AND the experimental setting for novelty
- If the method is not novel but the FINDING would be, say so explicitly
- Always check the most recent 6 months of arXiv — the field moves fast
- **Anti-hallucination for Closest Prior Work.** Never fabricate arXiv IDs, DOIs, or titles from memory. Every paper in the prior-work table must be verified via web search. If a paper cannot be verified, tag it `[UNVERIFIED]` and surface the uncertainty rather than dropping it.
