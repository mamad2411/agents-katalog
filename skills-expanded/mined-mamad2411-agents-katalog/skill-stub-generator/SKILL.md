# Skill-Stub Generator
> **ID**: skill-stub-generator
> **Layer**: SKILL STUB OPTIMIZATION (PON39)
> **Priority**: MEDIUM — Convert large skill files to stubs for fast loading
> **Token Cost**: 0

## Problem
Some AI CLIs (Claude Code, Hermes) load FULL SKILL.md content at startup, not just frontmatter. With 8789 skills averaging 7KB each = 61MB of text = ~15M tokens. This would take 4+ minutes to load and fill context 75× over.

## Solution: Stub Pattern

### S1: STUB CONVERSION
```
For every skill file > 2KB:
→ Create stub version: frontmatter + 1-line pointer
→ Move full content to skill-name.full.md
→ Stub content:
  ---
  name: original-skill-name
  description: [original description from frontmatter]
  ---
  For full instructions, read skill-name.full.md when this skill is invoked.
→ AI reads stub (200 bytes) at discovery time
→ Reads full file ONLY when skill is actually invoked
```

### S2: FRONTMATTER-ONLY INJECTION
```
→ At session start, inject ONLY:
  - skill name (20 chars avg)
  - skill description (80 chars avg)
  - skill trigger keywords (30 chars avg)
→ Total per skill: ~130 chars = ~35 tokens
→ 8789 skills × 35 tokens = ~307K tokens
→ STILL TOO MUCH → use with skill-router-tree (PON37)
→ With router tree: 50 routers × 500 tokens = 25K tokens ✓
```

### S3: ON-DEMAND BODY LOAD
```
When skill is invoked:
1. Read stub → get frontmatter
2. If stub points to .full.md → read .full.md
3. If .full.md > 10KB → use head + grep to extract relevant section
4. Cap injection at 1500 chars per skill
5. After use → discard from memory (no cache)
```

### S4: STUB AUTO-GENERATION
```python
# Convert large skills to stubs
import os
CAT = os.path.expanduser('~/.agents/skills-catalog')
for f in os.listdir(CAT):
    if not f.endswith('.md'): continue
    path = os.path.join(CAT, f)
    if os.path.getsize(path) > 2048:  # > 2KB
        # Check if not already a stub
        with open(path) as fp:
            content = fp.read()
        if len(content) < 500: continue  # already short
        # Extract frontmatter
        if '---' in content[:200]:
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                # Create stub
                stub = f"---{frontmatter}---\nFor full instructions, read {f}.full.md when this skill is invoked.\n"
                # Save full version
                full_path = path.replace('.md', '.full.md')
                with open(full_path, 'w') as fp:
                    fp.write(content)
                # Overwrite with stub
                with open(path, 'w') as fp:
                    fp.write(stub)
```

## Config
```yaml
skill_stub_generator:
  enabled: true
  stub_threshold_kb: 2
  max_body_load_chars: 1500
  never_full_load_over_kb: 10
  extract_relevant_section: true
  discard_after_use: true
```
