---
name: indexion-search
description: '"Where is this function?" "Any O(n^2) hotspots?" "Which files are similar?" "Find code that does X" — pick the right indexion command for your search intent. Covers token patterns, structural queries, semantic similarity, file-level exploration, and cached index lifecycle.'
---

# indexion search — Codebase Search & Exploration

Find what you need in a codebase. This skill covers every search intent —
pattern matching, structural queries, semantic similarity, file-level exploration,
and purpose-based function lookup — and tells you which tool to reach for based on
what you're actually trying to do.

## Start Here: What Are You Looking For?

Don't pick a command first. Start with your intent.

### "Where is X defined / used?"

You know the name. You need to find it.

**Exact name match** — `Ident:X` matches the exact token text. Finds definitions and all call sites:

```bash
# Find a type definition and all references
indexion grep "TypeIdent:DigestManifest" src/

# Find only the function definition (fn keyword + identifier)
indexion grep "fn Ident:parse_config" cmd/

# Find both definition and call sites (Ident without fn)
indexion grep "Ident:parse_config" cmd/

# List all pub struct definitions
indexion grep "pub struct *" src/
```

**Substring match** — `--semantic=name:X` matches as a substring. Use when you don't remember the exact name:

```bash
# Find all functions containing "build_graph" (matches build_graph_from_source too)
indexion grep --semantic=name:build_graph src/ cmd/

# Find all functions containing "sort"
indexion grep --semantic=name:sort src/
```

`Ident:build_graph` only matches a token with exactly that text.
To find `build_graph_from_source`, use `--semantic=name:build_graph` instead.

**Token-level search** — `indexion grep` is not text grep. It searches over the
token structure defined by KGF specs. `pub fn *` matches the keyword `pub`, the
keyword `fn`, then any identifier — it won't match `pub fn` inside a string literal
or comment.

**Pattern syntax:**

| Pattern | Meaning |
|---------|---------|
| `pub`, `fn`, `for` | Language keyword (auto-resolved via KGF aliases) |
| `KW_fn` | Token kind exactly |
| `Ident:foo` | Kind + text (exact match) |
| `*` | Any single token |
| `...` | Zero or more tokens (non-greedy) |
| `!pub` | Negation — any token except this |
| `(`, `)`, `{`, `->` | Punctuation (aliases) |

**Output control:**

```bash
# File paths only (like grep -l)
indexion grep --files "pub fn *" src/

# Match count per file (like grep -c)
indexion grep --count "pub fn *" src/

# Context lines around matches
indexion grep --context=3 "for ... for" src/

# Filter by file pattern
indexion grep --include='*.mbt' --exclude='*_test.mbt' "pub fn *" src/
```

### "Find code that does X" (by description)

You don't know the name. You know what it does.

Two tools serve this intent, with a key trade-off:

| Tool | Build step? | Speed | Best for |
|------|------------|-------|----------|
| `grep --semantic="similar:..."` | No | Moderate | One-off queries, small codebases |
| `digest query` | Yes (cached) | Fast after build | Repeated queries, large codebases |

**One-off (no build step):**

```bash
# Find functions that parse JSON configuration
indexion grep --semantic="similar:parse JSON configuration" src/

# Find error handling patterns
indexion grep --semantic="similar:handle error and return result" src/

# Find tokenization-related code
indexion grep --semantic="similar:tokenize source code into tokens" src/
```

Results are ranked by cosine similarity. Use descriptive phrases —
"parse JSON configuration" works better than just "json".

**Repeated queries (cached index):**

```bash
# First: build the index (once, then incremental updates)
indexion digest build src/

# Then: query by purpose
indexion digest query "parse configuration file"
indexion digest query "calculate similarity between two texts"
indexion digest query "walk directory tree and collect files"
```

`digest query` auto-updates the index if source files have changed since the
last build — you don't need to manually rebuild. See [Index Lifecycle](#index-lifecycle)
for details.

**Full-text semantic search (code + wiki + docs):**

```bash
# Search across everything — code, wiki pages, documentation
indexion search "how does the KGF parser work" src/ .indexion/wiki/

# Filter by attributes
indexion search --filter="node_type:code" "tokenizer" src/
indexion search --filter="language:moonbit" "parse" src/

# File paths only
indexion search --files "configuration parsing" src/

# JSON output for scripting
indexion search --json "error handling" src/

# Control result count and minimum relevance
indexion search --top-k=50 --min-score=0.1 "similarity" src/
```

`search` differs from `digest query`: it searches across file content
(not just function purpose), and can include wiki pages and documentation.
`digest query` is function-granular and purpose-indexed.

### "Find structural patterns" (code smells, complexity)

You're looking for a *shape* of code, not specific text.

```bash
# Nested for loops (O(n^2) candidates)
indexion grep "for ... for" src/

# Undocumented public API
indexion grep --undocumented src/

# Functions longer than 50 lines
indexion grep --semantic=long:50 src/

# Functions shorter than 3 lines (trivial?)
indexion grep --semantic=short:3 src/

# Functions with 4+ parameters (complexity smell)
indexion grep --semantic=params-gte:4 src/

# Proxy functions (wrappers that just delegate)
indexion grep --semantic=proxy src/

# Functions by name substring
indexion grep --semantic=name:sort src/
indexion grep --semantic=name:parse src/
```

These are **semantic queries** — they analyze function structure, not just text.
`--semantic=proxy` examines whether a function body is a single forwarded call.
`--semantic=long:50` counts lines of the function body.

**Combining for code review:**

```bash
# Post-commit quality check
indexion grep "for ... for" src/                    # O(n^2) hotspots
indexion grep --undocumented src/                    # Missing docs
indexion grep --semantic=proxy src/                  # Unnecessary wrappers
indexion grep --semantic=long:50 src/                # Overly long functions
indexion grep --semantic=params-gte:4 src/           # Complex signatures
```

### "Which files are similar to each other?"

You want to understand overlap and relationships across files.

```bash
# Quick similarity scan — sorted pairs above threshold
indexion explore --format=list --threshold=0.7 \
  --include='*.mbt' --exclude='*moon.pkg*' src/

# Cluster similar files together
indexion explore --format=cluster --threshold=0.6 src/

# Full similarity matrix (small file sets only)
indexion explore --format=matrix src/module_a/ src/module_b/

# JSON for scripting
indexion explore --format=json --threshold=0.5 src/

# Compare specific files
indexion explore file_a.mbt file_b.mbt --threshold=0

# Function-level structural comparison (slower, more precise)
indexion explore --strategy=apted --format=list src/
indexion explore --strategy=tsed --format=list src/

# Statistical correction for large codebases
indexion explore --fdr=0.05 --format=list --threshold=0.5 src/
```

**Strategies — when the default isn't enough:**

| Strategy | What it compares | When to use |
|----------|-----------------|-------------|
| `hybrid` (default) | BM25 + JSD lexical, TSED structural fusion | General purpose — start here |
| `tfidf` | Token vocabulary overlap | Fast scan, vocabulary-level |
| `bm25` | Term frequency relevance | Similar to tfidf, different weighting |
| `jsd` | Token distribution divergence | Probabilistic similarity |
| `ncd` | Compression-based similarity | Language-agnostic, byte-level |
| `apted` | Function-level tree edit distance | Precise structural comparison |
| `tsed` | Tree structure edit distance | Precise structural comparison |

**Noise reduction tips:**
- `--exclude='*moon.pkg*'` — package config files all look alike
- `--exclude='*_wbtest.mbt'` — test files share boilerplate
- Files at 40-60% with no structural overlap are "concept neighbors" — they share
  vocabulary because they work in the same domain (see indexion-refactor skill)

### "Compare two specific texts"

Direct pairwise similarity between two texts or files.

```bash
# Compare two texts
indexion sim "hello world" "hello there"

# Compare file contents (shell reads)
indexion sim "$(cat a.mbt)" "$(cat b.mbt)"

# Choose strategy
indexion sim --strategy=ncd "text1" "text2"
indexion sim --strategy=tfidf "text1" "text2"

# Output control
indexion sim --output=similarity "text1" "text2"   # 0.0-1.0 only
indexion sim --output=distance "text1" "text2"     # distance only
indexion sim --output=both "text1" "text2"         # both (default)
```

### "Trace references before refactoring"

Before moving or renaming something, find all references.

```bash
# All references to a type (definition + usage sites)
indexion grep "TypeIdent:DigestManifest" src/ cmd/

# All references to a function (definition + call sites) — Ident:X is exact match
indexion grep "Ident:parse_config" cmd/

# Substring match when you only know part of the name
indexion grep --semantic=name:build_graph src/ cmd/

# Verify no references to the old name remain after a rename
indexion grep "Ident:old_function_name" src/ cmd/
```

**Note:** `Ident:X` and `TypeIdent:X` are different token kinds. Type names use
`TypeIdent`, variable/function names use `Ident`. When unsure, use `--semantic=name:X`
which matches regardless of token kind.

## Index Lifecycle

`digest` and `search` build cached indexes for fast repeated queries.
These indexes can become stale when source files change.

### How Drift Detection Works

The digest index maintains a **manifest** at `.indexion/digest/` that tracks:

| What | How | Detects |
|------|-----|---------|
| File content | SHA-256 hash per file | Modified, new, deleted files |
| Function identity | Hash of file_hash + symbol_id + name + kind | Changed function bodies |
| Call graph | Hash of source_hash + sorted callers + callees | Changed relationships |
| KGF spec | Spec fingerprint | Language grammar changes |

When you run `digest query`, it automatically compares current file hashes against
the manifest. If files have changed, it **incrementally re-indexes** only the
affected functions — no full rebuild needed.

### Check Index Health

```bash
# Show what has changed since the last index build
indexion digest status src/

# Show index statistics (size, function count, providers)
indexion digest stats
```

`digest status` reports:
- Modified files (content hash differs)
- New files (not in manifest)
- Deleted files (in manifest but gone from disk)
- Estimated affected functions

### When to Rebuild vs. Incremental Update

| Situation | Action | Command |
|-----------|--------|---------|
| Normal development | Auto-update on query | `indexion digest query "..."` (auto) |
| Skip auto-update for speed | Query saved index only | `indexion digest query --no-update "..."` |
| Many files changed | Manual incremental build | `indexion digest build src/` |
| KGF spec changed | Full rebuild | `indexion digest rebuild src/` |
| Index corrupted or version mismatch | Full rebuild | `indexion digest rebuild src/` |
| First time setup | Initial build | `indexion digest build src/` |

### Keep Index Fresh During Development

After significant code changes (new module, major refactor), run:

```bash
# Check what's stale
indexion digest status src/

# If many changes: explicit build (faster than auto-update during query)
indexion digest build src/

# Verify
indexion digest stats
```

For wiki search indexes, rebuild with:

```bash
indexion wiki index build --full --wiki-dir=.indexion/wiki
```

## Choosing the Right Tool

| Intent | Tool | Why |
|--------|------|-----|
| Find by name | `grep "Ident:X"` | Token-level, precise |
| Find by keyword pattern | `grep "pub fn *"` | Token pattern matching |
| Find by description (one-off) | `grep --semantic="similar:..."` | No build step |
| Find by description (repeated) | `digest query` | Cached, fast after build |
| Find across code + docs + wiki | `search` | Broadest scope |
| Find structural patterns | `grep --semantic=long:50` | Structural analysis |
| Find similar files | `explore --format=list` | Pairwise similarity |
| Compare two specific texts | `sim` | Direct comparison |
| Trace all references | `grep "TypeIdent:X"` | Before refactoring |

## Common Pitfalls

**"grep found nothing but I know it exists"**
- **Token kind mismatch:** `Ident:Config` won't match `TypeIdent:Config`.
  When unsure of the kind, use `--semantic=name:Config` (matches any kind, substring).
- **Exact vs substring:** `Ident:build_graph` won't match `build_graph_from_source`.
  For substring matching, use `--semantic=name:build_graph`.
- **Wrong target directory:** Check that you're searching the right path.
  You can specify multiple directories: `src/ cmd/`.

**"explore shows 95% similarity between types.mbt files"**
- Type definition files share structural patterns (pub struct + getters).
  This inflates TF-IDF scores. It's structural similarity, not duplication.
  Exclude with `--exclude='*types.mbt'` or use `--strategy=apted` for function-level.

**"digest query returns irrelevant results"**
- Use descriptive purpose phrases, not code keywords.
  "calculate text similarity using TF-IDF" beats "tfidf".
- Check `digest status` — the index may be stale.

**"search is slow on a large codebase"**
- Build a digest index first: `indexion digest build src/`
- Use `--include` to narrow scope: `indexion search --include='*.mbt' "query" src/`

**"`...` in grep matches too much"**
- `...` is non-greedy — it matches the *shortest* span. `for ... for` finds the
  closest pair of for loops, not the furthest. This is usually correct for nesting detection.
