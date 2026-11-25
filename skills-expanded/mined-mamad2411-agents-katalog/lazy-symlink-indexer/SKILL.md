# Lazy-Symlink Indexer
> **ID**: lazy-symlink-indexer
> **Layer**: DISK I/O OPTIMIZATION (PON23)
> **Priority**: HIGH — Eliminate 177K+ symlink directory scanning overhead
> **Token Cost**: 0 (pure local file system optimization)

## Problem
177,842 symlinks across 21 platforms = massive directory readdir() overhead. Every time an AI scans its skills folder, it resolves 8,000+ symlinks per platform. This causes:
- CPU spikes during skill discovery
- Disk I/O bursts
- Memory allocation for inode tables
- Device heating from sustained I/O

## Solution
Build a **single index file** per platform that replaces live directory scanning.

### Index Format
```json
{
  "version": 2,
  "platform": ".codex",
  "generated": "2026-09-15T23:00:00Z",
  "skill_count": 8460,
  "skills": [
    {"name": "skill-name.md", "target": "/Users/.../skills-catalog/skill-name.md", "size": 1200, "keywords": ["token","optim"]}
  ]
}
```

### Rules

#### LSI1: INDEX-FIRST POLICY
```
IF skill_discovery_requested:
  → Read index file (1 file read, ~50KB) instead of readdir() on 8460 entries
  → NEVER scan directory unless index is stale (>24h old)
  → Return skill list from index cache
```

#### LSI2: INCREMENTAL UPDATE
```
IF new_skill_added:
  → Append to index file (O(1), no full rescan)
  → Update skill_count
IF skill_removed:
  → Mark as "deleted" in index (don't remove, keep tombstone)
  → Rebuild full index only on next session start
```

#### LSI3: KEYWORD PRECOMPUTE
```
→ Pre-compute keyword tags for each skill at index build time
→ When AI searches for "token optimization", grep index JSON instead of opening 8460 files
→ Reduces disk I/O from 8460 reads to 1 read + 1 grep
```

#### LSI4: STALE CHECK
```
IF index_age > 24h:
  → Rebuild index in background (low priority, nice 19)
  → Continue using old index until new one is ready
  → Never block user-facing operations for index rebuild
```

## Implementation
```bash
# Build index for one platform
python3 -c "
import os, json, time
cat = os.path.expanduser('~/.agents/skills-catalog')
files = sorted(os.listdir(cat))
skills = []
for f in files:
    if not f.endswith('.md'): continue
    path = os.path.join(cat, f)
    sz = os.path.getsize(path)
    # Extract keywords from filename
    kws = [w for w in f.replace('.md','').replace('-',' ').split() if len(w)>2]
    skills.append({'name': f, 'target': path, 'size': sz, 'keywords': kws})
idx = {'version':2, 'platform':'.codex', 'generated': time.strftime('%Y-%m-%dT%H:%M:%SZ'),
       'skill_count': len(skills), 'skills': skills}
out = os.path.expanduser('~/.codex/skills/.skill_index.json')
with open(out, 'w') as fp: json.dump(idx, fp)
print(f'Index: {len(skills)} skills → {os.path.getsize(out)//1024}KB')
"
```

## Config Integration
```yaml
lazy_symlink_indexer:
  enabled: true
  index_file: .skill_index.json
  stale_after_hours: 24
  rebuild_priority: low  # nice 19
  keyword_search: true
  never_scan_directory: true  # CRITICAL
```
