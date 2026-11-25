---
name: sdl3
description: SDL3 API reference and documentation. Use when working with SDL3, SDL3_image, SDL3_mixer, SDL3_ttf, or SDL3_net code. Provides function signatures, parameters, return values, remarks, code examples, and related functions.
argument-hint: [function name or topic, e.g. SDL_CreateWindow]
allowed-tools: Read, Grep, Glob
---

# SDL3 Documentation Skill

You have access to the complete SDL3 wiki (4,890 API docs). Use progressive disclosure — start narrow, expand only as needed.

## Lookup strategy (follow in order)

### 1. Specific function/type query → direct lookup

If the user asks about a known symbol (e.g. `SDL_CreateWindow`, `IMG_Load`):

1. Read `lookup.md` (in this skill directory) — find the symbol's category and one-line description
2. Read the full doc: `docs/SDL3/<SymbolName>.md` (or `docs/SDL3_image/`, `SDL3_mixer/`, etc.)
3. Present: signature, parameters, return value, key remarks, code example if available, see-also links

### 2. Topic/domain query → category drill-down

If the user asks about a topic (e.g. "how does audio work", "window management"):

1. Read `index.md` (in this skill directory) — find the matching category and its file path
2. Read the category file (e.g. `docs/SDL3/CategoryAudio.md`) — get the overview + full symbol list
3. Summarize the category, highlight the most relevant functions
4. Only read individual function docs if the user wants specifics

### 3. Fuzzy/unknown query → search

If you can't find it in lookup.md or index.md:

1. `Grep` for the term across `docs/` — check function names, descriptions
2. `Glob` for `docs/SDL3/*<term>*.md` to find matching files
3. Read the best match

## File layout

```
.claude/skills/sdl3/
├── SKILL.md          ← you are here (always loaded)
├── index.md          ← master topic→category map (read first for topic queries)
├── lookup.md         ← symbol→category+description table (read first for function queries)
└── docs/
    ├── SDL3/         ← 4,282 individual API + category docs
    ├── SDL3_image/   ← image loading library
    ├── SDL3_mixer/   ← audio mixing library
    ├── SDL3_ttf/     ← font rendering library
    └── SDL3_net/     ← networking library
```

## Response guidelines

- Lead with the function signature in a C code block
- Include parameter table and return value
- Mention thread safety and version if relevant
- Include code examples when available — these are high value
- Link to related functions the user likely needs next
- For broad topics, give an overview with the 3-5 most important functions before listing everything
