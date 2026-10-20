---
description: "Add, update, or deduplicate content in Markdown or plain-text files."
argument-hint: "Required: #file:path/to/file and the content to add"
---

# Add Content to a File

## 1. Inspect the File
1. Read the target file.
2. Identify its headings, sections, list patterns, and style conventions.
3. Find an exact heading match for the requested content.
4. Find an exact content match.
5. If no exact match exists, find the closest heading based on keyword overlap.

## 2. Resolve the Request
- Choose exactly one insertion target.
- Prefer an exact heading match.
- If no exact heading match exists, use the nearest section based on heading keywords.
- If no suitable section exists, propose a new section.
- Place the new content where it best fits within the target section.
- Append it to the end of the section only when it belongs there.
- Preserve the existing spacing, indentation, and capitalization.
- Do not make unrelated formatting changes.
- If duplicate content exists, update it instead of adding a second copy.
- Correct only clear grammar errors, such as subject-verb agreement or missing articles.

## 3. Safety Rules
- **Execution boundary:** Apply the edit only after presenting the plan and receiving the user's explicit confirmation.
- **No rephrasing:** Never rephrase existing sentences.
- **Grammar scope:** Limit grammar corrections to those described in the rules above.

## 4. Review Plan Format
Use this exact markdown schema:

### Scope
- Target: <file path>
- Mode: <read-only | apply-after-confirmation>

### Result
- Summary: <ADDED | UPDATED | SKIPPED>

### Evidence
- <file path>:<line> - <location and what changed>
- Duplicates: <none | item1; item2>
- Improvements: <none | item1; item2>

### Next Action
- <single minimal next step or `none`>

### Verdict
- READY | NEEDS FIXES | BLOCKED
