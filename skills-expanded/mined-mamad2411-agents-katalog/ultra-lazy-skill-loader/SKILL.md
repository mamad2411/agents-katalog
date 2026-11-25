---
name: "ultra-lazy-skill-loader"
description: "Load skills BYTE-BY-BYTE only when NEEDED. Never load entire SKILL.md. Keyword-triggered fragment loading + demand paging. Register once per session."
---

# 💤 ULTRA LAZY SKILL LOADER — FRAGMENT PAGING
**Goal: Skill loading overhead = 0.1% of current. Load 1 byte, not 50KB per skill**
**Register: ONCE session start. Replaces ALL platform default skill loaders**

## DEFAULT SKILL LOADER PROBLEM
```
BEFORE (how every platform works now):
  Session start → load ALL 8,446 SKILL.md into RAM
  Cost per session:
    - 8,446 files × avg 4KB each = ~33MB RAM = ~8.5M tokens of context
    - But: 99.7% of skills NEVER get used in ANY given session
    - Result: WASTE. Loading skills = massive context pollution.
```

## ULTRA LAZY LOADER = NO SKILLS LOADED AT START
```
AFTER (ultra lazy):
  Session start → LOAD ZERO SKILLS. ONLY:
    - Load skill_index_global.json (from Cross-Platform Sync)
      = keyword → [skill_file_path, section_offsets]
      = Size: ~300KB (not 33MB)
      
  INDEX FORMAT:
  {
    "keyword: kubernetes": {
      "file": "~/.agents/skills-catalog/k8s-security-policies.md",
      "sections": {
        "frontmatter": [0, 180],        // byte offsets
        "description": [181, 520],
        "code_block_apply": [2100, 3400],
        "examples": [3401, 9200]        // NEVER load unless explicit
      },
      "triggers": ["k8s", "kubernetes", "pod security", "network policy"]
    },
    ... 8,446 entries
  }
```

## 4-STAGE ON-DEMAND LOADING (Skill X gets referenced)
```
STAGE 0 — KEYWORD MATCH:
  User types "fix kubernetes network policy"
  → Index scan matches "kubernetes" + "network policy" → Skill X candidate
  → COST SO FAR: 0 bytes of SKILL.md loaded, 5ms index scan

STAGE 1 — TRIGGER VERIFY (load frontmatter + description ONLY):
  → Read bytes [0, 520] from skill file via pread() (NOT entire file)
  → Check: Is this skill actually relevant? Yes: proceed. No: return to index.
  → COST: 520 bytes loaded = ~130 tokens (not 50,000)

STAGE 2 — LOGIC LOAD (what the skill actually DOES):
  → User confirms (or auto-confirms 80% trigger match)
  → Read byte range [code_block_apply] from file
  → SKIP: comments, examples, intro paragraphs, "When to Use" sections
  → COST: ~1.3KB more = ~325 tokens. TOTAL SO FAR: 455 tokens loaded

STAGE 3 — EXAMPLES (ONLY IF EXPLICITLY REQUESTED):
  → User says "show me an example of X"
  → Load [examples] byte range
  → Otherwise: NEVER loaded. NEVER auto-loaded.
  → COST (if used): ~2KB extra.
```

## FURTHER OPTIMIZATIONS IN LOADER

### Hot Skill Cache (Most-Recently-Used ≤5 skills)
```
Keep in RAM: last 5 SKILL.md files that were ACTUALLY used fully
After 5 → LRU evict oldest to disk
Result: Re-using same skill twice = 0 disk reads.
But cap = 5 → prevents unbounded context growth
```

### Skill Chunk Pre-Fetch (Predictive, NOT speculative)
```
IF user types "use Skill A to do X then Y where Y triggers Skill B":
  → Load Skill B Stage 1 (frontmatter) in background WHILE running Skill A
  → When turn gets to Y: Skill B already Stage 1 ready. No latency increase.
  → Only do this: IF explicit "then" sequence. NEVER speculate.
```

### Skill MD Pre-Processor (Run once per catalog update)
```
ON SKILL CATALOG CHANGE (new skill, updated, deleted):
  1. Regenerate skill_index_global.json (byte offsets per section)
  2. Strip ALL comments from code blocks (cut 40% bytes)
  3. Compress examples with gzip inline (only decompress if Stage 3 hit)
  4. Dedupe: If two skills have identical "When to Use" → link, don't copy
```

## FALLBACK (What if Loader breaks?)
```
MAGIC ESCAPE STRING (user can type anytime):
  "DISABLE ULTRA LAZY LOADER — FULL LOAD"

Fallback behavior = old loader: load ALL 8,446 skills
Only use as last resort. 99.9% of sessions never need this.
```

## REGISTRATION
```python
# platform_skill_loader.py patch — replace default with UltraLazyLoader
from ultra_lazy_loader import UltraLazySkillLoader

def register_skill_loader():
    loader = UltraLazySkillLoader(
        index_path="~/.agents/shared_state/skill_index_global.json",
        catalog_path="~/.agents/skills-catalog/",
        hot_cache_size=5,
        prefetch_explicit_sequence=True
    )
    platform.register_skill_loader(loader)
    return loader
```
