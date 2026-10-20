---
name: bibtex-abstract-generator
description: Generate high-quality academic abstracts for BibTeX bibliography entries by fetching content from URLs or DOIs. Use when a user uploads a BibTeX file and requests abstracts to be generated or added to entries. Automatically processes all entries, skips those with existing abstracts, and outputs a complete properly-formatted BibTeX file ready for import into reference management software.
---

# BibTeX Abstract Generator

## Overview

Automatically generate 2-4 sentence academic abstracts for BibTeX entries by fetching article content from URLs or DOIs, then output a complete, properly formatted bibliography file.

## Pipeline Mode (optional Stage 0 of academic-pipeline)

`bibtex-theme-analyzer` (Stage 1) reads abstracts to map themes, so the pipeline is only as good as the abstracts in the `.bib` file. Run this skill as an optional **Stage 0** whenever the input bibliography has entries with missing `abstract` fields.

- Fetch page content with `mcp__workspace__web_fetch` (Cowork's web-fetch tool). If a domain can't be fetched, leave the entry's abstract empty rather than inventing one.
- In pipeline mode, write the enriched `.bib` to the run folder (e.g. `<run folder>/pipeline/enriched.bib`) and hand that path to Stage 1, instead of presenting it as a chat artifact.
- Standalone, present the completed `.bib` as a file the user can save.

Never fabricate abstract text — only synthesize from fetched source content.

## Workflow

### 1. Parse BibTeX File

Read the uploaded BibTeX file and extract all entries with their fields. Identify entry keys, types (@article, @book, @inproceedings, etc.), and existing fields.

### 2. Process Each Entry

For each entry:

**Check for existing abstract:**
- If `abstract` field exists: Skip this entry entirely (preserve existing)
- If no abstract: Continue processing

**Identify URL source:**
- Use `url` field if present
- If no `url` field, construct from `doi` field: `https://doi.org/{doi_value}`
- Example: `doi = {10.3233/SSW220008}` → `https://doi.org/10.3233/SSW220008`

**Fetch content:**
- Use `web_fetch` tool with the identified URL
- Extract full article text from the response

### 3. Generate Abstract

Create a 2-4 sentence abstract using this structure:

**Sentence 1:** State the central research aim or problem
**Sentence 2-3:** Summarize main approach, methods, and key findings
**Final sentence:** Highlight broader significance, implications, or practical applications

**Quality standards:**
- Clear, accessible language suitable for academic audiences
- Factually accurate - no invented claims
- Synthesizes rather than summarizes superficially
- Logical flow: problem → approach → result → relevance
- Preserves original context and intent

**Abstract generation prompt pattern:**
```
Based on this article content, write a 2-4 sentence abstract that:
1. Opens with the central research aim or problem
2. Summarizes the main approach, methods, and key findings  
3. Concludes with broader significance or practical applications

Use clear academic language. Be factually accurate. Follow: problem → approach → result → relevance.
```

### 4. Update Entry

Add the generated abstract to the BibTeX entry:
- Field name: `abstract` (lowercase)
- Maintain all original fields unchanged
- Preserve proper BibTeX syntax and formatting
- Escape special characters as needed: `\&`, `\%`, etc.

### 5. Output Complete Bibliography

Create an artifact containing:
- All entries (both processed and skipped)
- Proper BibTeX formatting throughout
- New `abstract` fields added where applicable
- No additional commentary or explanation

**Output format:**
```bibtex
@article{key_2023,
    author = {Author Name},
    title = {Article Title},
    journal = {Journal Name},
    year = {2023},
    doi = {10.1234/example},
    abstract = {This study aims to... The authors demonstrate... These findings have significant implications for...}
}
```

## Example

**Input entry:**
```bibtex
@incollection{lastname_shorttitle_2024,
  title = {Short Title: A Subtitle Naming the Contribution},
  author = {Lastname, Firstname and Otherlastname, Otherfirstname},
  year = 2024,
  doi = {10.0000/PLACEHOLDER}
}
```

**Processing:**
1. No `abstract` field found → process
2. No `url` field → construct from DOI: `https://doi.org/10.0000/PLACEHOLDER`
3. Fetch content from DOI URL
4. Generate abstract following structure
5. Add `abstract` field to entry

**Output entry:**
```bibtex
@incollection{lastname_shorttitle_2024,
  title = {Short Title: A Subtitle Naming the Contribution},
  author = {Lastname, Firstname and Otherlastname, Otherfirstname},
  year = 2024,
  doi = {10.0000/PLACEHOLDER},
  abstract = {This paper presents the contribution named in the title, states the problem it addresses, and describes the method used. It reports what the method produced and what the results establish, then states the implications for practitioners in the field. Roughly 120 to 200 words, written in the source's own terms rather than the summarizer's.}
}
```

## Notes

- All entries must have either `url` or `doi` field (per user requirements)
- Existing abstracts are never modified or replaced
- Output is a complete, valid BibTeX file ready for import
- Present output as artifact with no additional commentary
- Preserve all original formatting, field order, and special characters
