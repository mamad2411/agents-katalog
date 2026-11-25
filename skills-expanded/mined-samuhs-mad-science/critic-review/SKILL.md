---
name: critic-review
description: Review the project docs and experiments for gaps between what is documented, what was implemented, and the state of the art. Use when the user wants a critical assessment of the whole project, wants to check for missing experiments, bad assumptions, or weak evidence.
---

# Critic Review

The main goal of this skill is to evaluate the entire project to understand what is
good, what could be better, and which gaps remain. With that, if necessary, propose
new experiments to make the project more scientifically robust.

## Critic Review Flow

1. **Read the main docs of the project**
   - Every important doc lives under `docs/...`.
   - Look for the implemented notebooks in the folders. If a notebook does not
     exist, the experiment was not run.

2. **Analyze the docs and the results, if any.**

3. **Against the project's main goal and the analysis above, check:**
   - Is the proposed experiment enough to validate the hypothesis?
   - Is there enough evidence to validate the hypothesis? How strong is it?
   - Are there any wrong assumptions drawn from the results?

4. **Evaluate the project against the scientific process**
   - What is good?
   - What could be better?
   - What are the gaps?
   - How strong is each piece of evidence relative to the hypothesis and its premises?
   - How strong is the project as a whole?

5. **Give the final assessment based on the review flow**
   - Write a report from the full analysis performed.
     - Save it in `docs/critic-review/<today-date>_<critic_review_name>.md`
   - If necessary, propose new experiments to fill the gaps and strengthen the project.
   - Before finishing, ask the user whether they want a more thorough review using
     the `/literature-research` skill. Give your recommendation on this point based
     on the final assessment.
     - If it was done, run the full review again to check everything.