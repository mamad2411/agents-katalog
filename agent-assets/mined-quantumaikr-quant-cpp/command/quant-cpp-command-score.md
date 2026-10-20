---
description: Run the 5-dimension scoring harness and display results
---

# Score

Run the quant.cpp scoring harness to measure project completeness across 5 dimensions.

## Steps

1. Run `bash score.sh` (full evaluation) using the Bash tool
2. Read the `.score` file for the numeric score
3. Present the results to the user in a clear summary:
   - Total score (X.XXXX / 1.0000)
   - Each dimension's percentage (structure, correctness, quality, performance, integration)
   - The LOWEST scoring dimension (this is the bottleneck)
   - Specific items scoring 0 that could be improved next
4. If `.score_history` exists, show the trend (improving/declining/stagnant)
5. Suggest the single highest-impact next action based on the score breakdown
