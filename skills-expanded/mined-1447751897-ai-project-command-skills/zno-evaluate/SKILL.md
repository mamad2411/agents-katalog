---
name: zno-evaluate
description: Use when the user writes /zno-evaluate or wants to validate whether a project idea is worth doing before committing. Uses Socratic questioning to challenge the idea across pain points, target users, existing solutions, ROI, risks, and timeline. Outputs a structured evaluation conclusion (do / don't do / defer). Should be used before /zno-init.
---

# Zno-Evaluate — Project Evaluation

Prevent wasted effort on projects without clear value, feasible scope, or viable ROI. Use before `/zno-init`.

## Workflow

1. Use Socratic questioning to challenge the idea. Ask sequentially (not all at once), 2-5 rounds:
   - Pain point: Who has this problem? How painful is it? How do they solve it today?
   - Existing solutions: What alternatives exist? Why would yours be better?
   - Target users: Who specifically would use this? How many? How would they find it?
   - Scope and timeline: What is the minimum viable version? How long to build it?
   - ROI and risk: What do you gain if it works? What do you lose if it fails? What's the biggest risk?
2. Output a structured evaluation:

   ```markdown
   ## Project Evaluation: [Project Name]

   ### Conclusion: DO / DON'T DO / DEFER

   ### Summary
   One paragraph explaining the recommendation.

   ### Strengths
   - ...

   ### Risks
   - ...

   ### Conditions to Proceed (if DEFER)
   - ...

   ### Recommended Next Step
   If DO: proceed to /zno-init with the refined requirement.
   If DEFER: what needs to change before re-evaluating.
   If DON'T DO: alternative suggestions if any.
   ```

3. Do not scaffold any project docs or write any code during evaluation.
4. If the conclusion is DO, suggest running `/zno-init` with the refined requirement statement.
