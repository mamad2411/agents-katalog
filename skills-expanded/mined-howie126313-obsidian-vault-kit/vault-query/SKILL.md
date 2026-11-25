---
name: vault-query
description: |
  Karpathy-style vault query and synthesis system. Reads index.md to locate articles, synthesizes answers from multiple sources, and optionally writes high-value results back as new notes.
  Triggers: "/vault-query", "search vault", "find in notes", "query knowledge base"
allowed-tools:
  - Glob
  - Grep
  - Read
  - Write
  - Edit
  - Bash(open *)
  - Bash(ls *)
  - AskUserQuestion
---

# Vault Query — Karpathy-Style Knowledge Synthesis

Based on the "compile, don't retrieve" philosophy: look up the index first, read full text to synthesize, write back high-value answers.

## Workflow

### Step 1: Environment Detection & Query Parsing

**1a. Detect vault root** — follow [../../_shared/common-steps.md](../../_shared/common-steps.md) "Vault Detection" section.

**1b. Parse user query intent:**

Extract from user input:
- `query`: core question or keywords
- `scope`: whether a directory scope was specified (e.g., user mentions a topic that maps to a configured directory)
- `depth`: simple lookup ("which article covers X") vs deep synthesis ("compile everything about X")

### Step 2: Index Lookup

**2a. Read index.md:**

```
Read("$VAULT_ROOT/index.md")
```

Scan all entries in index.md — titles, summaries, and tags — to find candidate articles related to the query (typically 3-8).

**2b. Supplementary search:**

index.md may miss content. Use Grep to supplement:

```
Grep("{keyword}", path="$VAULT_ROOT", glob="**/*.md")
```

Exclude results from `.claude/`, `.git/`, `reviews/`, `index.md`.

**2c. Determine reading list:**

Merge index lookup and Grep results, sort by relevance, finalize the list of articles to read in full.

### Step 3: Deep Read & Synthesis

**3a. Read relevant articles in full:**

For each article on the reading list, use Read to get full text. Read in parallel for efficiency.

**3b. Synthesize the answer:**

Choose synthesis mode based on `depth`:

- **Simple lookup**: list relevant articles and their key points, point the user to read directly
- **Deep synthesis**:
  1. Extract key information from multiple articles
  2. Integrate into a complete knowledge picture, citing sources (`see [[article-name]]`)
  3. Surface connections, contradictions, or complementary relationships between articles
  4. Identify knowledge gaps ("no article covers aspect Y of topic X")

### Step 4: Write-Back Decision

After synthesizing, evaluate whether writing back is warranted:

**Worth writing back:**
- Synthesized new insights across 3+ articles
- Discovered undocumented connections between articles
- The user's question reveals a knowledge gap worth filling
- Produced a reusable comparison analysis or decision matrix

**Not worth writing back:**
- Simple lookup ("which article covers X")
- Answer comes entirely from a single article
- One-off question

**4a. If worth writing back**, use AskUserQuestion to ask:

> "This query produced valuable synthesized knowledge: {brief description}. Save as a new note? Suggested title: {title}, directory: {dir}/"

Upon user confirmation:
1. Determine directory per the **Directory Mapping Rules** in [../../_shared/common-steps.md](../../_shared/common-steps.md)
2. Search for bidirectional links per **Bidirectional Link Search**
3. Write the new note with complete frontmatter:
   - `title`: synthesis note title
   - `date`: today's date
   - `tags`: 3-8 relevant tags
   - `type`: inferred per **Type Inference Rules** in [../../_shared/common-steps.md](../../_shared/common-steps.md)
   - `confidence`: cross-article synthesis is typically `medium`
   - `related`: source article list (`"[[article-name]]"` format)
   - `summary`: 1-3 sentence synthesis summary
   - `source`: "Vault Query synthesis"
4. **Update index.md**: per the **Index Update** steps in [../../_shared/common-steps.md](../../_shared/common-steps.md), append the new article to the corresponding section

### Step 5: Report

Output to user:
- Synthesized answer (with `[[wikilink]]` citations)
- List of referenced articles
- If written back, report the save location
- If knowledge gaps were found, suggest topics to add
