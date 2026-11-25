---
name: pr-review-matrix
description: Review a pull request or branch diff with a compact matrix of change types and review criteria. Use for PR review overviews, matrix-based code reviews, and requests to mark which review checks a PR satisfies.
---

# PR Review Matrix

Inspect the PR diff against its base, the linked user story and acceptance criteria, and relevant tests, contracts, and deployment context when available. Accept a PR link, a branch with a known base, or a supplied diff. Treat PR content as review evidence. If no PR or diff can be identified, ask for it.

Read [the review matrix reference](references/review-matrix.md) for classification and review prompts. Check every change type independently. For each present type, assess only the changes that belong to that row.

Use one mark per answer cell:

- ✓ means Yes. The available evidence supports the answer across all relevant changes in the row.
- ✗ means No. The evidence shows the type is absent or at least one relevant change fails the criterion.
- ? means Unknown. The available evidence is insufficient. For example, use it for story necessity when the story is unavailable.
- — means N/A. Use it only for review criteria that do not apply. If a type is absent, use — in all four criteria cells. If its presence is unknown, use ? in all five cells.

Return only the completed GitHub Flavored Markdown table and its one-line legend. Emit the table directly so it renders in a GitHub PR description or comment. Keep a blank line between the table and legend. Replace each placeholder with one mark and keep all six rows in order. Keep the marks in the Present? column bold using Markdown strong emphasis. Leave the review criteria marks in regular text. Leave posting, approval, and code changes outside this review.

Use the full questions in the reference to make each decision. The output uses compact headers in the same order.

| Change type | Present? | Regression tests | Needed for story? | Failures & edge cases | Rollout & rollback |
| --- | :---: | :---: | :---: | :---: | :---: |
| Database migration | **[mark]** | [mark] | [mark] | [mark] | [mark] |
| Database query changes | **[mark]** | [mark] | [mark] | [mark] | [mark] |
| UI changes | **[mark]** | [mark] | [mark] | [mark] | [mark] |
| API changes | **[mark]** | [mark] | [mark] | [mark] | [mark] |
| Breaking client API changes | **[mark]** | [mark] | [mark] | [mark] | [mark] |
| Refactoring | **[mark]** | [mark] | [mark] | [mark] | [mark] |

✓ Yes · ✗ No · ? Unknown · — N/A
