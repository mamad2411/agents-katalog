---
name: wiki-spark
description: >
  Generate creative prompts and thought experiments from wiki content.
  Use when the user wants inspiration, says "spark", "what if",
  "give me ideas", "what should I explore next", or wants creative
  prompts from their wiki, second brain, or knowledge base.
allowed-tools: Bash Read Glob Grep
---

# Personal Wiki — Spark

Generate creative prompts, thought experiments, and research questions drawn from wiki content.

## How It Works

### 1. Survey the wiki

Read `wiki/index.md` to understand the full scope of the wiki. Then sample pages across different categories and domains — aim for breadth, not depth. Read enough to understand the range of topics covered.

### 2. Generate 5-10 prompts

Draw from the wiki's actual content to generate prompts across four categories:

**What-If Questions**
Thought experiments that combine concepts across domains.
- "What if [concept X from domain A] applied to [domain B]?"
- "What would happen if [entity]'s approach to [topic] was used for [different problem]?"
- Draw on real concepts and entities from the wiki, not generic hypotheticals.

**Research Questions**
Open questions the wiki raises but can't answer — directions for further reading.
- Gaps in the wiki's coverage that would be worth filling
- Claims that appear in only one source and could use corroboration
- Topics the wiki touches on but doesn't explore in depth

**Synthesis Prompts**
Prompts for deeper wiki pages that would strengthen the knowledge base.
- "Compare [[Concept A]] and [[Concept B]] — how do they differ in their approach to [topic]?"
- "How does [[Entity A]]'s view on [topic] relate to [[Concept B]]?"
- These should produce pages worth saving to `wiki/synthesis/`.

**Writing Seeds**
Starting points for blog posts, essays, or explanatory pieces.
- "An essay on how [wiki concept] challenges conventional thinking about [topic]"
- "A blog post connecting [idea from source A] with [idea from source B]"
- Draw on the wiki's strongest and most interconnected content.

## Output Format

Present prompts in chat — do not save to the wiki.

Group by category. For each prompt:
- The prompt itself (clear, specific, actionable)
- Brief context explaining why this prompt is interesting given the wiki's content
- References to specific wiki pages via `[[wikilinks]]`

## Constraints

- **Read-only.** Do not create, modify, or delete any wiki pages.
- **No web search.** Draw only from existing wiki content.
- **Chat only.** Present prompts in the conversation, not as saved files.
- **Be specific.** Every prompt should reference actual wiki content, not generic questions.

## Related Skills

- `/wiki-ingest` — process new sources into wiki pages
- `/wiki-query` — ask questions against the wiki
- `/wiki-explore` — discover cross-domain connections
