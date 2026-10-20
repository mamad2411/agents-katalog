Verify every citation in `docs/paper_draft.tex` is a real, published work using web search. For each citation that is vague, incorrect, or unverifiable, attempt to find the correct bibliographic information and update the entry in the .tex file.

Reply to the user in terse caveman lingo to save tokens, e.g.
"why lot word when few word do trick". Keep technical facts correct.
Do not apply caveman lingo to bibliography entries, code, filenames, commands,
academic prose, generated docs, or quoted text.

## Step 1 — Extract all citations

Read `docs/paper_draft.tex` and extract every `\bibitem{key}` entry from the `\begin{thebibliography}` block. List them all before proceeding.

## Step 2 — Verify each citation

For every bibitem, use WebSearch to verify it exists as a real published work. Search using the title, authors, and venue listed in the entry.

For each citation, determine one of:
- **VERIFIED** — found an exact or near-exact match (correct title, authors, venue/journal/conference, year)
- **CORRECTED** — entry is real but has wrong title, authors, year, or venue; you found the correct details
- **FABRICATED / NOT FOUND** — no credible source found after searching; the work does not appear to exist
- **VAGUE** — entry lacks enough detail to be a proper academic citation (e.g., "ResearchGate document", "Scribd document", no authors, no year); attempt to find the real paper it was intended to reference

Search strategy per entry:
1. Search for the exact title in quotes first: `"<title>" site:arxiv.org OR site:ieeexplore.ieee.org OR site:dl.acm.org`
2. If not found, try author + title without quotes
3. For arXiv entries, verify the arXiv ID exists and the title/authors match
4. For IEEE/ACM entries, search IEEEXplore or ACM DL

## Step 3 — Fix the .tex file

After verifying all citations:

1. **For CORRECTED entries**: Update the `\bibitem` in `docs/paper_draft.tex` with the accurate title, authors, venue, and year. Use standard IEEE bibliography format.

2. **For VAGUE entries where you found the real paper**: Replace the vague entry with a proper bibliographic record.

3. **For FABRICATED / NOT FOUND entries**: Add a `% UNVERIFIED` comment on the line and note what was searched. Do not delete the entry (it may still be cited in the body text), but flag it clearly for the author to review.

4. **Do not alter** any citation that is VERIFIED and already correctly formatted.

## Step 4 — Report

After all edits, produce a concise summary table:

| Key | Status | Notes |
|-----|--------|-------|
| goel1981implicit | VERIFIED | — |
| atpg-overview-scribd | VAGUE→CORRECTED | Found: "..." (IEEE 1985) |
| trojan-delay-unm | FABRICATED | No match found |
| ... | ... | ... |

Flag any `\bibitem` keys that are cited in the paper body (`\cite{key}`) but whose entry was marked FABRICATED, as these require author attention before submission.

$ARGUMENTS
