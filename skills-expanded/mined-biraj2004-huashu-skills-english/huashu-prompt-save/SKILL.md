---
name: huashu-prompt-save
description: Automatically identifies the prompt type and saves it to the appropriate category (Technical / Content / Teaching / Product / General). Use when the user mentions "save prompt", "record prompt", or "organise prompts".
---

# Prompt Categorisation & Saving

Automatically identifies prompt types, saves them to the appropriate category, and updates the index — a professional, structured capability.

## When to Use

- The user says "save this prompt", "make a note of this", "store this one"
- The user pastes a prompt and says "help me organise this"

## Core Features

1. **Automatic type identification**: 5 main categories (Technical Development / Content Creation / Teaching Design / Product Consulting / General Tools)
2. **Extract key information**: Purpose, source, applicable scenarios, key characteristics
3. **Auto-save**: `[category]/prompt-[sequence]-[title].md`
4. **Update index**: Add an entry to `INDEX.md`

## 5 Category Rules

| Category | Keywords | Example |

    param($m)
    $inner = $m.Groups[1].Value
    # Split by | and fix each cell separator
    $cells = $inner -split '\|'
    $fixedCells = $cells | ForEach-Object {
      $cell = ---
name: huashu-prompt-save
description: Automatically identifies the prompt type and saves it to the appropriate category (Technical / Content / Teaching / Product / General). Use when the user mentions "save prompt", "record prompt", or "organise prompts".
---

# Prompt Categorisation & Saving

Automatically identifies prompt types, saves them to the appropriate category, and updates the index — a professional, structured capability.

## When to Use

- The user says "save this prompt", "make a note of this", "store this one"
- The user pastes a prompt and says "help me organise this"

## Core Features

1. **Automatic type identification**: 5 main categories (Technical Development / Content Creation / Teaching Design / Product Consulting / General Tools)
2. **Extract key information**: Purpose, source, applicable scenarios, key characteristics
3. **Auto-save**: `[category]/prompt-[sequence]-[title].md`
4. **Update index**: Add an entry to `INDEX.md`

## 5 Category Rules

| Category | Keywords | Example |
|----------|----------|---------|
| Technical Development | programming, debugging, code, optimisation | "Python Code Optimiser Prompt" |
| Content Creation | writing, copywriting, script, creative | "WeChat Article Generator" |
| Teaching Design | curriculum, teaching, explanation, training | "Knowledge Breakdown Prompt" |
| Product Consulting | requirements, product, users, growth | "User Needs Analysis Prompt" |
| General Tools | general, productivity, assistant | "Universal Translation Tool" |

## Save Format

```markdown
# [One-line title]

**Source**: Self-created / From the web / Adapted from xxx
**Tags**: #tag1 #tag2 #tag3
**Applicable Scenarios**: xxx

## Prompt Content
[Full prompt, preserving original format]

## Usage Examples
[If there are examples or usage notes]

## Results / Notes
[Usage outcomes, caveats]
```

## Execution Workflow

1. **Identify type**: Classify based on keywords and content
2. **Extract information**: Purpose, source, tags, applicable scenarios
3. **Generate filename**: `prompt-[auto-increment sequence]-[short-title].md`
4. **Save file**: To `/Prompt-Library/[category]/` directory
5. **Update index**: Add an entry to `/Prompt-Library/INDEX.md`

## Notes

- If the category is unclear, ask the user for clarification
- Titles should be practical and immediately understandable (no more than 15 characters)
- Tags are for quick retrieval — 3–5 tags is ideal
- Preserve the original format and structure of the prompt
- For prompts sourced from the web, record the origin where possible

## Reference Resources

- `/Prompt-Library/CLAUDE.md` — Prompt management rules

**Last Updated**: 2025-11-07

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
.Trim()
      if ($cell -match '^:?-+:?
| Technical Development | programming, debugging, code, optimisation | "Python Code Optimiser Prompt" |
| Content Creation | writing, copywriting, script, creative | "WeChat Article Generator" |
| Teaching Design | curriculum, teaching, explanation, training | "Knowledge Breakdown Prompt" |
| Product Consulting | requirements, product, users, growth | "User Needs Analysis Prompt" |
| General Tools | general, productivity, assistant | "Universal Translation Tool" |

## Save Format

```markdown
# [One-line title]

**Source**: Self-created / From the web / Adapted from xxx
**Tags**: #tag1 #tag2 #tag3
**Applicable Scenarios**: xxx

## Prompt Content
[Full prompt, preserving original format]

## Usage Examples
[If there are examples or usage notes]

## Results / Notes
[Usage outcomes, caveats]
```

## Execution Workflow

1. **Identify type**: Classify based on keywords and content
2. **Extract information**: Purpose, source, tags, applicable scenarios
3. **Generate filename**: `prompt-[auto-increment sequence]-[short-title].md`
4. **Save file**: To `/Prompt-Library/[category]/` directory
5. **Update index**: Add an entry to `/Prompt-Library/INDEX.md`

## Notes

- If the category is unclear, ask the user for clarification
- Titles should be practical and immediately understandable (no more than 15 characters)
- Tags are for quick retrieval — 3–5 tags is ideal
- Preserve the original format and structure of the prompt
- For prompts sourced from the web, record the origin where possible

## Reference Resources

- `/Prompt-Library/CLAUDE.md` — Prompt management rules

**Last Updated**: 2025-11-07

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
) {
        " $cell "
      } else {
        " $cell "
      }
    }
    '|' + ($fixedCells -join '|') + '|'
  
| Technical Development | programming, debugging, code, optimisation | "Python Code Optimiser Prompt" |
| Content Creation | writing, copywriting, script, creative | "WeChat Article Generator" |
| Teaching Design | curriculum, teaching, explanation, training | "Knowledge Breakdown Prompt" |
| Product Consulting | requirements, product, users, growth | "User Needs Analysis Prompt" |
| General Tools | general, productivity, assistant | "Universal Translation Tool" |

## Save Format

```markdown
# [One-line title]

**Source**: Self-created / From the web / Adapted from xxx
**Tags**: #tag1 #tag2 #tag3
**Applicable Scenarios**: xxx

## Prompt Content
[Full prompt, preserving original format]

## Usage Examples
[If there are examples or usage notes]

## Results / Notes
[Usage outcomes, caveats]
```

## Execution Workflow

1. **Identify type**: Classify based on keywords and content
2. **Extract information**: Purpose, source, tags, applicable scenarios
3. **Generate filename**: `prompt-[auto-increment sequence]-[short-title].md`
4. **Save file**: To `/Prompt-Library/[category]/` directory
5. **Update index**: Add an entry to `/Prompt-Library/INDEX.md`

## Notes

- If the category is unclear, ask the user for clarification
- Titles should be practical and immediately understandable (no more than 15 characters)
- Tags are for quick retrieval — 3–5 tags is ideal
- Preserve the original format and structure of the prompt
- For prompts sourced from the web, record the origin where possible

## Reference Resources

- `/Prompt-Library/CLAUDE.md` — Prompt management rules

**Last Updated**: 2025-11-07

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
