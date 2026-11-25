---
name: huashu-info-search
description: Multi-channel search for new products and technologies, cross-validated and saved to a knowledge base. Use when the user mentions "latest information", "new product", "search for resources", "look something up", or "learn about XX".
---

# Information Search & Knowledge Management

Automatically performs multi-channel searches, validates information, and saves results to the knowledge base when new products or technologies are encountered.

## When to Use

- Dealing with new products or technologies (released within the last 3 months)
- Needing to verify the latest information
- When the user says "search this", "look up the latest info"

## Core Features

1. **Multi-channel search**: Official sources + media + community
2. **Source prioritisation**: Authoritative media first; ignore Zhihu/Baidu content from before 2025
3. **Knowledge management**: Save to `_knowledge_base/`, with sources and timestamps noted

## Search Strategy

### What to Search

- Official product/technology information (release date, features, pricing)
- Tech media coverage (TechCrunch, The Verge, Medium, etc.)
- Community discussions (Reddit, Hacker News, X/Twitter)
- Competitor comparison information
- Related concept explanations

### Source Priority

**✅ Prioritise (within the last 6 months)**:

1. Authoritative tech media (TechCrunch, The Verge, MIT Technology Review)
2. Community forums (Reddit, Hacker News)
3. Official documentation and research papers

**❌ Ignore entirely**:

- Zhihu, Baidu: All content from before 2025
- Outdated content: More than 6 months old
- Marketing and advertorial content

### Keyword Combinations

- Topic + year: `"AI detection 2025"`
- Topic + best practice: `"AI text humanization best practices"`
- Topic + Reddit: `"AI writing detection reddit 2025"`

## Knowledge Management

### Save Format

File naming: `[topic]-[date].md`

```markdown
# Information on [Topic]

**Information collected**: 2025-XX-XX
**Next update recommended**: 2025-XX-XX

## Key Findings
- Finding 1
- Finding 2

## Data and Links
- Official documentation: xxx
- Media coverage: xxx

## Sources
1. [Source 1](link)
2. [Source 2](link)
```

### Save Location

- Writing projects: `/writing/_knowledge_base/`
- Video creation: `/video-creation/_knowledge_base/`

## Notes

- All information must be tagged with source and date
- Inform the user when information is uncertain
- When sources conflict, prioritise the most authoritative one

**Last Updated**: 2025-11-07

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
