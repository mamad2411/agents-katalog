---
name: cite-verify
description: Use when verifying bibliography citations in a document or when the user pastes academic citations to check, especially when worried about LLM hallucinations where real DOIs or NBER working paper numbers are paired with fabricated titles. Queries Crossref canonical metadata and flags metadata mismatches.
---

# cite-verify

Verifies bibliography citations against canonical bibliographic metadata from Crossref. Catches the specific LLM-hallucination failure mode where a real identifier (DOI, NBER working paper number, arXiv ID) is paired with a fabricated title.

## When to use

Use when:
- Verifying a bibliography (`.bib`, `.tex`, `.md`, `.docx`, plain text) for hallucinated citations

Invoke this skill when:

- The user asks to check, verify, or lint citations in a document
- The user pastes one or more citations in chat and asks whether they are real
- The user mentions hallucinated references, fake citations, or LLM-generated bibliographies
- The user is preparing a paper, grant proposal, or report and wants to catch hallucinated citations before submission
- The user asks about a specific citation and wants to confirm the title matches the identifier

## When NOT to use

- For general claim-fact-checking (this skill only checks citation METADATA, not whether a cited source actually supports a claim)
- For generating citations from notes (this skill is a CHECKER, not a builder)
- For citations where identity itself is sensitive (the skill sends bibliographic metadata to Crossref, which is a public API)

## Input resolution

Check the user's message in this order:

1. **Pasted citation text in the message.** If the user includes one or more citation strings directly in their message, pipe them into the linter via stdin. No file needed.
2. **File path provided.** If the user gives a path to a `.md`, `.tex`, `.bib`, `.txt`, or `.docx` file, pass the path to the linter as an argument. For `.docx` on macOS, convert first: `textutil -convert txt -stdout -- "$path" | ~/.claude/skills/cite-verify/scripts/lint.sh`
3. **Both.** If the user provides both, process the pasted text first.
4. **Neither.** Ask which citations to check.

## How to run it

```bash
# Pasted text mode:
echo "<citation text>" | ~/.claude/skills/cite-verify/scripts/lint.sh

# Multiple citations - separate with blank lines:
printf 'Citation one here.\n\nCitation two here.\n' | ~/.claude/skills/cite-verify/scripts/lint.sh

# File mode:
~/.claude/skills/cite-verify/scripts/lint.sh /path/to/paper.md

# .docx on macOS:
textutil -convert txt -stdout -- "/path/to/paper.docx" | ~/.claude/skills/cite-verify/scripts/lint.sh
```

## Output interpretation

The linter outputs a Markdown report with these verdict categories:

- **VERIFIED** - the citation's metadata matches a canonical record. Safe to use.
- **PARTIAL_MATCH** - a canonical record exists but one or more fields differ (e.g., year variance between working paper and published version). Review and confirm.
- **METADATA_MISMATCH** - the identifier (DOI or NBER number) resolves to a paper with a different title. **This is the LLM-hallucination failure mode.** Almost always a mistake.
- **NOT_FOUND** - no matching canonical record in Crossref. Could be a legitimate obscure source or a hallucinated paper. Manual verification required.
- **NEEDS_MANUAL_VERIFICATION** - insufficient data to verify (very short title, missing fields).

Present the report to the user. If there are METADATA_MISMATCH or NOT_FOUND entries, surface them prominently and suggest that the user check each one before using the document.

## Scope limits

This skill is deliberately narrow:

- Only queries Crossref (via DOI, NBER working paper number lookup, or title+author search). Does not currently query arXiv or OpenAlex.
- Only checks citation metadata (title, author, year, venue). Does not verify that the cited paper actually supports a claim.
- Only handles the common academic citation formats (APA, Chicago, naive BibTeX, plain references). Does not parse complex LaTeX bibliography files in full.
- `.docx` support on macOS only (requires `textutil`). Linux users should convert to plain text first.
- Maximum 60 citations per invocation (DoS guard).
- Maximum 1 MB input per invocation.

## Privacy notice

cite-verify sends bibliographic metadata (title, author, year, DOI, NBER number) to the Crossref public API. It does NOT send:
- The body of the document
- Any data to the tool's author or any other server
- Anything beyond the citation metadata itself

A local audit log is maintained at `~/.claude/skills/cite-verify/logs/verifications.jsonl` containing SHA-256 hashes of citation strings (not the raw text), verification status, and timestamps. This log stays on the user's machine and is never sent anywhere.

For documents where even the list of cited papers is sensitive (confidential grant proposals, embargoed research, anonymous reviews), do not use this skill. Crossref will see every citation you check.

## Feedback

When presenting results, if the report shows catches or the user gives feedback, mention the feedback footer in the report (it links to `github.com/jonckr/cite-verify/issues`) as the place to share catches, report false positives or false negatives, or suggest improvements.

## Theoretical foundation

This skill applies the validation principle from Ludwig, Mullainathan & Rambachan (2025), "Large Language Models: An Applied Econometric Framework" (NBER Working Paper 33344). The paper proves that LLM-generated outputs contain systematic measurement error that propagates into downstream artifacts unless a validation sample is collected. cite-verify applies this principle to bibliographies: each citation is treated as an LLM-generated label that must be validated against a canonical record before being trusted.
