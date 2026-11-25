---
name: first-principles
description: "Use only when the user explicitly asks for a first-principles review of a product, requirement, workflow, or implementation: question the requirements, delete what should not exist, then simplify."
---

# First-Principles Review

Question assumptions and find the smallest system that meets the real goal; a review produces analysis and recommendations, not edits.

## Phases

Apply only the phases that serve the goal, in this order. Do not optimize or automate a process that should not exist.

1. **Question the requirements.** Treat every requirement as possibly wrong. State assumptions that change the result, surface competing interpretations, and push back when a simpler approach serves the goal better.
2. **Delete.** Remove parts, configuration and dependencies that the required behavior does not need, and confirm with regression checks. Stop when further deletion would risk required behavior; there is no deletion quota.
3. **Simplify and optimize.** Keep what remains minimal and readable, in the project's own style.
4. **Accelerate.** When speed matters, measure first, fix the slowest path, and check that the speed-up adds no flakiness.
5. **Automate.** Automate only a stable, already simplified process that repeats, and verify that it runs end to end without help.

## Checklist

1. Were the requirements questioned before any code was written?
2. Was only demonstrated waste removed?
3. Is the remaining code minimal and in the local style?
4. If speed mattered, was it measured before and after?
5. If something was automated, does it run cleanly without help?
