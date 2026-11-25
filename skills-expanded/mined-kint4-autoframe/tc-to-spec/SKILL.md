---
name: tc-to-spec
description: Convert requirements (pasted text, Notion, Jira, or Linear link) into a runnable Playwright spec. Use when the user runs /tc-to-spec or provides requirements to turn into tests.
---

# /tc-to-spec — Requirements to Spec

**Type:** Functional
**Description:** Takes requirements from any source (pasted text, Notion, Jira, Linear, Confluence, or a plain description) and generates a runnable Playwright spec file.

---

## Input Format

Any of:
- Pasted plain-text requirements or acceptance criteria
- A Notion / Jira / Linear / Confluence URL (fetched via the available MCP connector)
- A natural-language feature description

If the input is a URL and no connector is available, say: "I don't have access to that connector. Please paste the requirements directly here and I'll generate from that." For `.pdf` / `.docx` / `.csv`, ask the user to paste the relevant content.

## Output Format

A spec file at `tests/e2e/[feature-name]/[feature].spec.ts` following the spec conventions in CLAUDE.md, with each requirement mapped to one or more tests across Happy Path, Negative Cases, and Edge Cases.

## Step-by-Step Instructions

1. Read the spec conventions in CLAUDE.md.
2. Acquire the requirements:
   - Plain text → use directly.
   - URL → fetch via the matching connector; fall back to "paste here" if unavailable.
   - Description → ask up to 3 clarifying questions before generating.
   - Binary file → ask the user to paste the content.
3. Extract discrete, testable acceptance criteria. List them back to the user for confirmation if ambiguous.
4. Map each criterion to a test and classify it as Happy Path, Negative, or Edge.
5. Check for an existing Page Object and fixture for the feature; if missing, recommend `/new-page` and use raw `page` with a `TODO` comment in the meantime.
6. Generate the spec following all spec conventions (describe grouping, AAA comments, plain-language names).
7. Save to `tests/e2e/[feature-name]/[feature].spec.ts`.
8. Show a short traceability summary mapping each requirement to its test name.

## Rules

- Never block on a missing connector — always fall back to paste.
- Every requirement must map to at least one test.
- Follow the spec conventions exactly.
