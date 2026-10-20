---
name: evidence-reference-lookup
description: Use when deciding how to handle a media type, storage mode, or integrity question — searches this plugin's own reference corpus and returns the most relevant passages with their file paths. Triggers - "how do I redact video", "what is object lock compliance mode", "which hash tool on macOS".
allowed-tools: Bash(grep *), Bash(rg *), Bash(command *), Bash(find *), Bash(sed *), Bash(wc *), Read
---

# Reference Lookup

Search this plugin's own reference corpus and return the passages that actually answer
the question, with their paths.

## When to use

- Deciding how to handle a media type, storage mode, or integrity question.
- Checking which tool is appropriate before running it.
- Understanding a concept the pipeline assumes, such as retention mode or WORM media.

## Inputs

- A free-text query. Required.

## Procedure

### 1. Locate the corpus

The corpus lives in `references/` in this skill's directory, organised by topic:
`hashing/`, `timestamping/`, `packaging/`, `metadata/`, `capture/`, `storage/`,
`redaction/`, `custody/`. Resolve the skill directory at runtime and run the searches from it; never hardcode a path.

### 2. Search

```bash
rg -li "$QUERY" references/
```

Fall back to `grep -rli "$QUERY" references/` where `rg` is unavailable. Both are
case-insensitive and list matching files.

### 3. Widen a query that returns nothing

Try the concept rather than the phrasing — "retention" for "how long does it stay",
"WORM" for "write once". Try each significant word alone before concluding there is no
answer. Say which variations were tried.

### 4. Extract context

```bash
rg -n -C 4 "$QUERY" "$FILE"
```

Rank files by how many distinct query terms they match, not by raw hit count — a file
that mentions every term once is usually a better answer than one that repeats a single
term.

### 5. Report

Return the top three files. For each: the path, a one-line statement of what the file
covers, and the matching excerpt with its line numbers. Then answer the original
question in one or two sentences, citing which file it came from.

If nothing matches, say so plainly, name the searches that were run, and suggest where
the answer might live instead. Do not invent guidance and attribute it to the corpus.

## Output

- Ranked excerpts with paths and line numbers, plus a direct answer.
- Nothing is written or modified.

## Notes

- The corpus is original material written for this plugin. It is opinionated and
  deliberately narrow — it covers what this pipeline does, not the whole field.
- It is a starting point, not authority. Anything with legal consequence needs a
  qualified professional, not a reference file.
