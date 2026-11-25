---
name: huashu-research
description: Structured web research workflow that ensures research findings are saved incrementally to files and not lost due to session interruptions. Use when the user says "research", "search for information", "look this up", "find out about", or "latest information".
---

# Research Skill

A structured web research workflow with one core objective: real-time persistence of research findings to prevent loss due to session interruptions.

## When to Use

- Conducting preliminary research before writing an article
- Learning about new products, new technology, or recent releases
- Gathering competitor information or industry trends
- Any information-gathering task requiring multiple web searches

## Execution Workflow

### Step 1: Create the Research File Immediately

- Create the file **before** starting any searches
- Path: `_knowledge_base/research-<topic>-<YYYYMMDD>.md`
- Initial content includes: research objective, key questions, expected output

```markdown
# [Topic] Research Notes

Research Date: YYYY-MM-DD
Research Objective: [One-sentence summary]

## Key Questions
1. [Question 1]
2. [Question 2]
3. [Question 3]

## Findings

(To be filled in progressively during research)

## Source List

(Append after each search)
```

### Step 2: Search and Save Incrementally

- After every web search, immediately append findings to the file
- Tag each finding with the source URL and date
- Follow the source priority rules (see SHARED-RULES.md)

### Step 3: Stage Summaries

- After every 3 searches, save a "stage summary" to the file
- Format: `### Stage Summary (Round N)` + current key findings

### Step 4: Final Brief

At the end of research, organise the file into a structured brief:

```markdown
## Research Conclusions

### Key Facts
1. [Fact 1] (Source: URL)
2. [Fact 2] (Source: URL)

### Source List
| Source | URL | Publication Date | Credibility |

    param($m)
    $inner = $m.Groups[1].Value
    # Split by | and fix each cell separator
    $cells = $inner -split '\|'
    $fixedCells = $cells | ForEach-Object {
      $cell = ---
name: huashu-research
description: Structured web research workflow that ensures research findings are saved incrementally to files and not lost due to session interruptions. Use when the user says "research", "search for information", "look this up", "find out about", or "latest information".
---

# Research Skill

A structured web research workflow with one core objective: real-time persistence of research findings to prevent loss due to session interruptions.

## When to Use

- Conducting preliminary research before writing an article
- Learning about new products, new technology, or recent releases
- Gathering competitor information or industry trends
- Any information-gathering task requiring multiple web searches

## Execution Workflow

### Step 1: Create the Research File Immediately

- Create the file **before** starting any searches
- Path: `_knowledge_base/research-<topic>-<YYYYMMDD>.md`
- Initial content includes: research objective, key questions, expected output

```markdown
# [Topic] Research Notes

Research Date: YYYY-MM-DD
Research Objective: [One-sentence summary]

## Key Questions
1. [Question 1]
2. [Question 2]
3. [Question 3]

## Findings

(To be filled in progressively during research)

## Source List

(Append after each search)
```

### Step 2: Search and Save Incrementally

- After every web search, immediately append findings to the file
- Tag each finding with the source URL and date
- Follow the source priority rules (see SHARED-RULES.md)

### Step 3: Stage Summaries

- After every 3 searches, save a "stage summary" to the file
- Format: `### Stage Summary (Round N)` + current key findings

### Step 4: Final Brief

At the end of research, organise the file into a structured brief:

```markdown
## Research Conclusions

### Key Facts
1. [Fact 1] (Source: URL)
2. [Fact 2] (Source: URL)

### Source List
| Source | URL | Publication Date | Credibility |
|--------|-----|-----------------|-------------|
| ...    | ... | ...             | High/Med/Low |

### Unconfirmed Items
- [Points that require further verification]

### Writing Recommendations
- [Suggestions for follow-up writing based on research findings]
```

## Key Principles

- **Create the file before searching**: Ensures even the first search result is saved
- **Save incrementally, not all at the end**: Append after each search
- **Research and writing are separate**: This Skill only does research — do not start drafting
- **Note credibility levels**: Distinguish between first-hand (official) and second-hand (media/community) information
- **Ignore outdated sources**: Zhihu/Baidu (pre-2025), marketing content

## Relationship with Other Skills

- After research is complete, the user can trigger `/topic-generation` to determine the writing direction
- The research file serves as input material for subsequent writing
- If information found during research is worth keeping long-term, save it to the relevant `_knowledge_base` category directory

## Output Location

- Research notes: `_knowledge_base/research-<topic>-<YYYYMMDD>.md`
- Long-term knowledge: `_knowledge_base/<category>/<topic>-<YYYYMM>.md`

**Last Updated**: 2026-02-06

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
.Trim()
      if ($cell -match '^:?-+:?
| ...    | ... | ...             | High/Med/Low |

### Unconfirmed Items
- [Points that require further verification]

### Writing Recommendations
- [Suggestions for follow-up writing based on research findings]
```

## Key Principles

- **Create the file before searching**: Ensures even the first search result is saved
- **Save incrementally, not all at the end**: Append after each search
- **Research and writing are separate**: This Skill only does research — do not start drafting
- **Note credibility levels**: Distinguish between first-hand (official) and second-hand (media/community) information
- **Ignore outdated sources**: Zhihu/Baidu (pre-2025), marketing content

## Relationship with Other Skills

- After research is complete, the user can trigger `/topic-generation` to determine the writing direction
- The research file serves as input material for subsequent writing
- If information found during research is worth keeping long-term, save it to the relevant `_knowledge_base` category directory

## Output Location

- Research notes: `_knowledge_base/research-<topic>-<YYYYMMDD>.md`
- Long-term knowledge: `_knowledge_base/<category>/<topic>-<YYYYMM>.md`

**Last Updated**: 2026-02-06

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
  
| ...    | ... | ...             | High/Med/Low |

### Unconfirmed Items
- [Points that require further verification]

### Writing Recommendations
- [Suggestions for follow-up writing based on research findings]
```

## Key Principles

- **Create the file before searching**: Ensures even the first search result is saved
- **Save incrementally, not all at the end**: Append after each search
- **Research and writing are separate**: This Skill only does research — do not start drafting
- **Note credibility levels**: Distinguish between first-hand (official) and second-hand (media/community) information
- **Ignore outdated sources**: Zhihu/Baidu (pre-2025), marketing content

## Relationship with Other Skills

- After research is complete, the user can trigger `/topic-generation` to determine the writing direction
- The research file serves as input material for subsequent writing
- If information found during research is worth keeping long-term, save it to the relevant `_knowledge_base` category directory

## Output Location

- Research notes: `_knowledge_base/research-<topic>-<YYYYMMDD>.md`
- Long-term knowledge: `_knowledge_base/<category>/<topic>-<YYYYMM>.md`

**Last Updated**: 2026-02-06

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
