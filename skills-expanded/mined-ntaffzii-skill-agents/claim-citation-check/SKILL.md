---
name: claim-citation-check
description: Use this skill before finalizing any research output, report, or summary that contains citations, statistics, or specific factual claims — to verify each citation actually exists, actually supports the claim it's attached to, and that no uncited sentence is quietly asserting a specific fact. Trigger on "check my citations", "verify sources", "fact check this", "did I cite this correctly", or automatically as a pre-finalization step for daily-news-report, github-skill-research, project-discovery, or any research summary with sourced claims.
---

# Claim / Citation Integrity Check

## Overview

LLM-generated research writing has a well-documented failure mode: citations that don't exist, or citations attached to a claim the source doesn't actually support (topically related but not actually saying that). Neither failure is visible from reading the text alone — the sentence reads as confidently sourced either way. This skill is a pre-finalization gate: before a research output ships, walk every citation and every uncited specific claim through an explicit check instead of trusting that "it has a citation" means "it's verified."

This is a general-purpose research-integrity check, not specific to academic papers — it applies to `daily-news-report`, `github-skill-research`, `project-discovery`, or any output that cites sources.

## When to use

- ก่อนส่งมอบ research report, news brief, หรือ summary ที่มี citation/สถิติ
- ตรวจว่า claim แต่ละอันมี source รองรับจริง ไม่ใช่แค่ "ดูน่าเชื่อถือ"
- Reviewing a draft where numbers, dates, or attributed quotes appear — verify each against its actual source before finalizing
- As the last step of any workflow that produces a sourced output (pairs naturally with `markdown-report`, `daily-news-report`, `github-skill-research`)

## When NOT to use

- The output contains no citations, statistics, or specific factual claims — general reasoning/opinion/code doesn't need this check
- The claim is genuinely common knowledge with no realistic chance of being wrong (e.g. "Python is a programming language") — citing every sentence, including trivial ones, is its own failure mode (noise that buries the claims that actually need scrutiny)

## Core knowledge

**Three questions for every citation, in order**:

1. **Does the source exist?** A URL, DOI, paper title, or quote that looks plausible can still be fabricated. If a tool with real web access is available (WebFetch/WebSearch), actually resolve the citation rather than trusting that it looks well-formed.
2. **Does the source say what the claim attributes to it?** A citation can be to a real, existing source that simply doesn't support the specific claim next to it — topically related is not the same as actually supporting the claim. This is the failure mode most likely to slip through casual review, because the citation "checks out" at a glance.
3. **Is the number/date/quote exact?** A citation can correctly support the general claim while misquoting the specific figure (rounding, unit confusion, conflating two different reported numbers). Check the exact figure against the source, not just the general direction.

**Uncited factual claims**: a sentence making a specific, checkable assertion (a percentage, a date, "X happened," "Y reported Z") with **no citation at all** is its own risk — it reads as confident regardless of whether it's actually verified. Flag these explicitly rather than only checking sentences that already have a citation marker attached.

**Calibrate citation density**: not every sentence needs a citation. General/definitional statements and the writer's own synthesis/opinion don't need one; specific, checkable, or surprising claims do. Over-citing trivial statements dilutes attention away from the claims that actually matter.

## Common mistakes

1. Confirming a citation "exists" (the link resolves, the paper is real) and stopping there, without checking it actually supports the specific claim attached to it.
2. Treating every sentence with a citation marker as verified just because it has one, without spot-checking a sample against the actual source.
3. Missing uncited factual claims entirely because review only scanned sentences that already had a citation marker.
4. Citing a secondary source's claim about a statistic (e.g. "Report X says Study Y found Z%") as if it were independently verified, without noting the report is repeating someone else's number.
5. Applying academic-paper levels of citation density to something like a Slack summary or quick brief, where it reads as noise rather than rigor.

## Code

`extract_claims.py` — pure regex, no dependencies. This is a **structural helper for locating candidates to check**, not a fact-checker — it cannot itself confirm a source exists or supports a claim; that step needs an actual fetch/read of the source.

- `extract_claims_with_citations(text)` → list of `ClaimCitation(sentence, markers)` for every sentence carrying a recognizable citation marker (`[1]`, `(Author, Year)`, `^1` styles)
- `find_uncited_factual_sentences(text)` → sentences with a numeric/attribution cue word (%, "according to", "found that", etc.) but **no** citation marker — candidates for "should this have a citation?"

Run `python3 extract_claims.py` for the self-test.

## Known limitations

- The marker-recognition regex covers a few common citation styles deliberately, not every possible format — a citation style not in the pattern list will be missed (false negative), which is the safer failure direction than flagging non-citations as citations.
- This skill does not verify anything on its own — it locates candidates. Actual verification requires fetching/reading the source, which needs a tool with real access (WebFetch, WebSearch, or a human doing the check).
- The uncited-claim heuristic (cue-word matching) is approximate — review its output, don't treat "not flagged" as "definitely fine" or "flagged" as "definitely a problem."
