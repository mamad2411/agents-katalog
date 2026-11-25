---
name: review
description: Aggressively review all commits on this branch against a provided branch and write findings as severity-rated todos in a git-ignored reviews folder.
---

Please aggressively review the code from all commits on this branch against the provided branch. If the provided branch is not specified ask. Write what you find in a Markdown review file in the git-ignored reviews folder as a list of to-dos to address. Don't sacrifice on making the problem easy to solve.  Give a one-sentence summary in bold at the top of each todo. Assign a severity rating from the range :large_green_circle: :large_yellow_circle: :large_orange_circle: :red_circle:, with :large_green_circle: being nitpicks and :red_circle: being blockers.
