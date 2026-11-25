# Catalog-Slim Optimizer
> **ID**: catalog-slim-optimizer
> **Layer**: CATALOG STORAGE OPTIMIZATION (PON24)
> **Priority**: MEDIUM — Reduce catalog disk footprint and memory mapping overhead
> **Token Cost**: 0

## Problem
8,460 files at 48MB total. 7 huge files were 3MB+ uncompressed. Memory-mapped file reads of large files cause RAM spikes.

## Solution

### CS1: GZIP COMPRESSION
```
For any .md file > 50KB:
  → Keep .md.gz version only
  → Remove uncompressed .md from catalog
  → AI reads .gz and decompresses on-demand (only when skill is actually invoked)
  → Saves 60-90% disk space on large files
```

### CS2: CONTENT DEDUPLICATION
```
→ SHA256 hash each file content
→ If two files have same hash, keep one + symlink the other
→ Removes duplicate skills across MCP categories
```

### CS3: SIZE-BASED LOADING
```
IF skill file < 2KB:
  → Safe to preload (cost: ~500 tokens max)
IF skill file 2-10KB:
  → Load on-demand only
IF skill file > 10KB:
  → NEVER load full file into context
  → Use head() + grep() to extract relevant section only
  → Cap injection at 1500 chars max
```

### CS4: CATALOG DEFRAG
```
→ Sort files alphabetically in inode order (rebuild on monthly basis)
→ Reduces filesystem fragmentation
→ Improves readdir() sequential scan performance
```

## Already Applied ✅
- 7 huge files compressed to .gz (saves ~2.8MB disk)
- 342 hermes real files converted to symlinks (saves 3.3MB disk)
- Catalog reduced from 50M → 48M

## Config
```yaml
catalog_slim:
  compress_threshold_kb: 50
  dedup: true
  max_inject_chars: 1500
  never_full_load_over_kb: 10
  defrag_monthly: true
```
