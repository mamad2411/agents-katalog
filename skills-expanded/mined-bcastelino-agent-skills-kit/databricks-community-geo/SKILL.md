---
name: databricks-community-geo
description: Guides writing and scoring Databricks Community content (Community Articles, Technical Blog posts, Q&A answers) so it is discoverable by people, search engines, and AI assistants (GEO). Use when the user asks to write a Databricks Community article, optimize a Q&A answer for discoverability, apply GEO best practices to Databricks content, or score/lint a draft against a publishing checklist.
license: MIT
metadata: {version: "1.0.0", tags: [databricks]}
---

# Databricks Community GEO

## Overview

This skill applies Generative Engine Optimization (GEO) best practices to Databricks Community content: Community Articles, Technical Blog posts, and Q&A answers. It ensures content is written to be found and correctly cited by Community search, search engines, and AI assistants, while remaining clear and useful to human readers first.

## Example Triggers

- "Help me write a Databricks Community article about troubleshooting Unity Catalog permission errors."
- "Review this Q&A answer and make it more discoverable."
- "Score this draft against the Databricks GEO checklist."
- "Is this title specific enough for search and AI assistants?"

## When Writing New Content

1. Consult `references/geo-best-practices.md` for the full set of GEO practices before drafting.
2. Write a specific, searchable title naming the feature, product, or exact error message. Do NOT use generic titles like "Need Help" or "Spark Issue."
3. Lead with the answer (BLUF): state the solution or key takeaway in the first paragraph, before any heading. Add context, steps, and code afterward.
4. Structure the body with `##`/`###` headings, short paragraphs, bullet or numbered lists, and fenced code blocks (with language) for commands and examples.
5. Add concrete examples: code snippets, sample output, or a real-world scenario.
6. Use Databricks feature/product names and relevant error messages naturally; avoid keyword stuffing.
7. Link to official Databricks documentation or related Community articles where they add value.
8. State prerequisites, limitations, and version-specific behavior explicitly. Only assert claims that can be supported.
9. For Q&A answers, remind the author to mark the correct response as the **Accepted Solution**.

## When Reviewing an Existing Draft

1. Save the draft as a Markdown file if it is not already one.
2. Run the checklist scorer:

```bash
python scripts/score_content.py --input <draft.md>
```

Add `--qa` if the draft is a Q&A-style answer, to also check for an Accepted Solution mention:

```bash
python scripts/score_content.py --input <draft.md> --qa
```

3. Address every `FAIL` line in the report; each maps to a practice in `references/geo-best-practices.md`.
4. Re-run the script after edits until all checks pass, then apply a final human read-through: the script is a deterministic heuristic linter, not a substitute for judgment.

## Output

A revised or newly written Markdown draft that leads with the answer, is easy to scan, includes examples and links, states limitations, and (for Q&A) reminds the author to mark the Accepted Solution. When scoring, return the full pass/fail report and the concrete fixes needed for each failing check.

## Resources

### scripts/score_content.py
Deterministic checklist linter for a Markdown draft. Checks title specificity, BLUF opening, heading structure, list/paragraph scannability, code block usage, presence of links, and accuracy/limitations language.

### references/geo-best-practices.md
Full distilled GEO best practices, sourced from the Databricks Community article "How to Optimize Your Content for GEO," including the Quick Publishing Checklist and Key Takeaway. Consult before drafting or reviewing content.
