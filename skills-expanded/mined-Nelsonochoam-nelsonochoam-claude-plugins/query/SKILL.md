---
name: query
description: Search the wiki, synthesize an answer with citations, and optionally create a new page if the answer reveals novel connections.
argument-hint: '<your question about the knowledge base>'
model: opus
---

User's request: $ARGUMENTS

# Query Wiki

You are answering a question using the accumulated knowledge in this wiki. Your answer should be grounded in wiki pages with `[[wikilink]]` citations.

## Vault Discovery

Read and follow `${CLAUDE_PLUGIN_ROOT}/references/vault-discovery.md`.

Store the resolved vault path as `$VAULT`.

## Read Schema

If `$VAULT/CLAUDE.md` exists, read it for vault-specific conventions.

## Parse the Question

The user's question is in `$ARGUMENTS`. If empty, use `AskUserQuestion` to ask what they want to know.

## Search the Wiki

Read and follow `${CLAUDE_SKILL_DIR}/references/query-workflow.md` for the detailed search and synthesis process.

### Search Strategy

1. **Start with the index**: Read `$VAULT/wiki/index.md` to understand what's available
2. **Keyword search**: Use `Grep` to search wiki pages for terms related to the question
3. **Follow links**: When you find relevant pages, follow their wikilinks to discover related content
4. **Check all page types**: Entities, concepts, sources, and synthesis pages may all be relevant

### Scope

- Search across ALL wiki directories (`entities/`, `concepts/`, `sources/`, `synthesis/`)
- Read the most relevant pages fully (not just grep matches)
- Follow wikilinks from relevant pages to find connected knowledge
- Check if a synthesis page already answers the question

## Synthesize the Answer

Compose a thorough answer that:

1. **Cites wiki pages**: Use `[[wikilinks]]` when referencing information from specific pages
2. **Synthesizes across sources**: Don't just summarize one page — connect information from multiple pages
3. **Distinguishes certainty levels**: Note when something is well-supported vs. mentioned only once
4. **Acknowledges gaps**: If the wiki doesn't fully answer the question, say what's missing

### Answer Format

```
## Answer

<Your synthesized answer with [[wikilinks]] to cited pages.>

## Sources Consulted

- [[page-1]] — <what it contributed to the answer>
- [[page-2]] — <what it contributed>

## Gaps

<What the wiki doesn't cover that would strengthen the answer. Optional — only include if there are genuine gaps.>
```

## Check for New Page Opportunity

After answering, consider: did this query reveal a novel connection or insight not captured in any existing page?

If yes, offer to create a synthesis page:

Use `AskUserQuestion` to ask:

> This answer connects ideas from multiple pages in a way that isn't captured yet.
> Should I create a synthesis page to preserve this insight?

Options: `Yes, create a synthesis page` / `No, the answer is sufficient`

If creating a synthesis page, only now read `${CLAUDE_PLUGIN_ROOT}/references/page-conventions.md` for the synthesis template — skip this read if no synthesis page is needed:
1. Create `$VAULT/wiki/synthesis/<synthesis-name>.md` using the synthesis template
2. Update `$VAULT/wiki/index.md` with the new page
3. Append to `$VAULT/wiki/log.md`: `## [YYYY-MM-DD] query + synthesis | <Question summary>`
4. Add wikilinks from source pages to the new synthesis page

## Log the Query

Whether or not a synthesis page was created, append to `$VAULT/wiki/log.md`:

```markdown
## [YYYY-MM-DD] query | <Question summary>

Consulted <N> pages. <Created synthesis page [[synthesis/<name>]] | No new pages created.>
```

## Done

Present the answer to the user. If a synthesis page was created, mention it:

```
New synthesis page created: wiki/synthesis/<name>.md
```
