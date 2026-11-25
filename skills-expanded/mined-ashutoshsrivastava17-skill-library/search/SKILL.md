---
name: search
description: >
  Search across all connected company tools in one unified query. Finds
  results from email, chat, documents, wikis, tickets, and other enterprise
  sources, then ranks and presents them in a single, actionable result set.
  TRIGGER when: user asks to search, find, look up, locate, or query for
  something across company tools, or asks "where is X", "find me X",
  "search for X", or uses a simple search query.
argument-hint: "<search query> [--source EMAIL|CHAT|DOCS|WIKI|TICKETS] [--from PERSON] [--since DATE]"
user-invocable: true
---

# Enterprise Unified Search

Execute a search across all connected enterprise tools and return a merged, ranked, and deduplicated result set.

## Search Execution Process

### Step 1: Parse the Search Query

Extract structured parameters from the natural language query:

| Parameter   | Extraction Pattern                              | Example                        |
|-------------|--------------------------------------------------|--------------------------------|
| Keywords    | Core topic words                                 | "deployment process"           |
| Source hint | "in email", "on Slack", "in Jira"                | source:email                   |
| Person      | "from Alice", "by the backend team"              | from:alice@company.com         |
| Date range  | "last week", "in March", "since Q1"              | since:2026-01-01               |
| Type        | "document", "thread", "ticket", "page"           | type:document                  |
| Project     | "in Project Alpha", "for the migration"          | project:alpha                  |
| Status      | "open tickets", "resolved", "draft"              | status:open                    |

### Step 2: Execute Parallel Searches

Search all relevant sources simultaneously:

| Source          | Query Adaptation                                          |
|-----------------|-----------------------------------------------------------|
| **Email**       | Subject + body search; filter by sender, date, attachments|
| **Chat**        | Message search; filter by channel, sender, reactions      |
| **Documents**   | Title + content search; filter by owner, type, folder     |
| **Wiki**        | Page title + content; filter by space, labels, author     |
| **Tickets**     | Summary + description + comments; filter by status, label |
| **Calendar**    | Event title + description; filter by date, attendees      |
| **Code**        | File content + names + commit messages; filter by repo    |

### Step 3: Merge and Rank Results

Ranking factors by weight:

| Factor              | Weight | Description                                             |
|---------------------|--------|---------------------------------------------------------|
| Text relevance      | 35%    | How closely content matches the query                   |
| Recency             | 25%    | More recent results rank higher                         |
| Engagement signals  | 15%    | Views, reactions, comments, shares                      |
| Source authority     | 15%    | Wiki > Docs > Email > Chat for factual queries          |
| User affinity       | 10%    | Content from user's team, frequented channels, owned docs|

### Step 4: Deduplicate

Remove or merge duplicate results:
- Same link shared across email, chat, and tickets — show once, note all sources
- Document with multiple versions — show latest, note version count
- Forwarded emails — show original thread, note forwards

## Output Format

```
# Search Results: "[query]"
Found [N] results across [N] sources ([time] elapsed)
Filters applied: [list any active filters]

## Top Results

### 1. [Title or Subject]
**Source**: [Icon] [Source name] | **Date**: [date] | **By**: [author]
**Match**: [brief excerpt with **highlighted** query terms]
[Relevance: why this result ranked high]

### 2. [Title or Subject]
**Source**: [Icon] [Source name] | **Date**: [date] | **By**: [author]
**Match**: [brief excerpt with **highlighted** query terms]

### 3. [Title or Subject]
**Source**: [Icon] [Source name] | **Date**: [date] | **By**: [author]
**Match**: [brief excerpt with **highlighted** query terms]

[... up to 10 results ...]

## Results by Source
| Source   | Results | Top Match                          |
|----------|---------|------------------------------------|
| Email    | [N]     | [title of best email result]       |
| Chat     | [N]     | [title of best chat result]        |
| Docs     | [N]     | [title of best doc result]         |
| Wiki     | [N]     | [title of best wiki result]        |
| Tickets  | [N]     | [title of best ticket result]      |

## Suggested Refinements
- Add filter: [suggestion based on results, e.g., "from:engineering"]
- Narrow to: [specific source that had best results]
- Related searches: [alternative query suggestions]
```

## Search Modifiers

Users can apply these modifiers to refine searches:

| Modifier          | Syntax                      | Example                         |
|-------------------|-----------------------------|---------------------------------|
| Exact phrase      | `"phrase"`                  | `"deployment pipeline"`        |
| Exclude term      | `-term`                     | `deployment -staging`           |
| Source filter     | `--source NAME`             | `--source slack`                |
| Author filter     | `--from NAME`               | `--from alice`                  |
| Date filter       | `--since DATE`              | `--since 2026-01-01`           |
| Date range        | `--since DATE --until DATE` | `--since 2026-01-01 --until 2026-03-01` |
| Type filter       | `--type TYPE`               | `--type document`               |
| Project filter    | `--project NAME`            | `--project alpha`               |
| Sort order        | `--sort relevance|date`     | `--sort date`                   |
| Result limit      | `--limit N`                 | `--limit 20`                    |

## Source-Specific Search Tips

### Email
- Search attachments by filename: `attachment:report.pdf`
- Filter by thread length for substantive discussions: `replies:>3`
- Look for decisions: combine with keywords like "approved", "decided", "go ahead"

### Chat / Slack
- Search specific channels: `in:#channel-name`
- Find shared links: `has:link`
- Find files: `has:file`
- Reactions as signals: messages with many reactions are often important

### Documents
- Filter by document type: spreadsheet, presentation, document
- Search in shared drives or specific folders
- Recently modified documents often have the most current info

### Wiki
- Search by space or category for scoped results
- Labels and tags are strong signals for relevance
- Parent page hierarchy indicates topic structure

### Tickets
- Search by status: open, in-progress, resolved, closed
- Labels and components narrow results significantly
- Comments often contain the most useful context

## Quality Standards

- **Response time**: Present initial results within 5 seconds; complete results within 15 seconds
- **Minimum results**: Always search at least 3 sources before reporting "no results"
- **Context**: Show enough context (50-100 chars around match) for users to evaluate relevance
- **Freshness**: Indicate index freshness if results may be stale
- **Accuracy**: Never fabricate results; only show actual matches from sources

## Edge Cases

- **Empty query**: Ask the user what they are looking for; suggest recent activity or popular searches
- **Very broad query** (e.g., "project"): Ask for clarification or return results grouped by source with a suggestion to narrow
- **No results**: Report which sources were searched, suggest alternative terms, check for typos
- **Single character or very short query**: Require at least 2 meaningful characters; suggest expanding
- **Special characters**: Escape special characters in queries; warn if query syntax looks malformed
- **Rate-limited source**: Return available results and note which sources were partially searched

## Follow-Up Actions

After presenting results, offer:
1. "Want me to expand result #N with full content?"
2. "Should I narrow these results by [suggested filter]?"
3. "Want me to synthesize the top results into a summary?"
4. "Should I search with different terms?"

## Quality Checklist

- [ ] Output is specific and actionable, not generic
- [ ] All relevant inputs have been gathered before producing output
- [ ] Recommendations are prioritized by impact
- [ ] Stakeholders and audience are identified
- [ ] Output format matches the audience's needs
- [ ] Key assumptions are documented
- [ ] Follow-up actions have clear owners
