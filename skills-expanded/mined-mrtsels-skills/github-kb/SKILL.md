---
name: github-kb
description: |
  GitHub Knowledge Base - Unified tool for managing local repos, discovering trending projects, and tracking tech hot topics.
  Use when: (1) searching local GitHub repos, (2) updating repo index, (3) discovering new repos via social media (Xiaohongshu, Twitter/X) and web search, (4) researching topics on Xiaohongshu, (5) fetching Twitter/X post content.
  Triggers: "github-kb", "search repos", "discover repos", "xiaohongshu", "rednote", "twitter", "X post", "tweet"
---

# GitHub Knowledge Base

Unified skill for local repo management + social media hot topic tracking.

## Configuration

**KB_PATH**: Default `~/github`. Customize in project AGENTS.md:
```
KB_PATH: /your/path
```

## Commands

### `/github-kb search <keyword>`
Search local knowledge base.

1. Read `KB_PATH/AGENTS.md` index
2. Match keyword against names, descriptions, tags
3. Display matches with paths
4. Offer to explore repo details

### `/github-kb update`
Sync index with filesystem.

1. Scan KB_PATH for `.git` directories
2. Extract: name, README first line, tech stack tags
3. Diff against existing AGENTS.md
4. Show changes, ask confirmation, write update

**Index format** (keep under 100 lines):
```markdown
# GitHub Knowledge Base

| Name | Description | Path | Tags |
|------|-------------|------|------|
| repo | One-line desc | ./repo | tag1, tag2 |
```

### `/github-kb discover <topic>`
Find trending repos from multiple sources.

1. **Gather** (parallel):
   - Xiaohongshu: See [references/xiaohongshu.md](references/xiaohongshu.md)
   - Twitter/X: See [references/twitter.md](references/twitter.md)
   - Web: `mcp__tavily__tavily-search` query `"<topic> github"`

2. **Extract** GitHub URLs from results

3. **Enrich** via `gh repo view owner/repo --json name,description,stargazerCount`

4. **Present** candidates with source attribution

5. **Clone** user-selected repos: `gh repo clone owner/repo`

6. **Update** index automatically

### `/github-kb xiaohongshu <keyword>`
Direct Xiaohongshu search. See [references/xiaohongshu.md](references/xiaohongshu.md).

### `/github-kb twitter <url>`
Fetch Twitter/X content. See [references/twitter.md](references/twitter.md).

## Tools Reference

| Source | Tool/Method |
|--------|-------------|
| Local repos | `gh` CLI, filesystem |
| Xiaohongshu | `mcp__rednote__*` tools |
| Twitter/X | Jina API via `scripts/fetch_tweet.py` |
| Web search | `mcp__tavily__tavily-search` |

## AI-Driven Query (DeepWiki Mode)

When solving problems, **proactively** search the knowledge base:

1. **Auto-detect relevance**: If user asks about a technology/tool, check KB first
2. **Query before web search**: Prefer local repos over external docs
3. **Deep dive**: Read repo's README, docs/, examples/ for answers

**Trigger phrases** (AI should recognize):
- "How does X work?"
- "Show me an example of X"
- "What's the best practice for X?"

**Workflow**:
```
User asks question → Check KB index → Found relevant repo?
  → Yes: Read repo docs, provide answer with citation
  → No: Use discover to find repos, or fall back to web search
```

**Example**:
```
User: How do I use MCP tools in Codex?
AI: [Checks KB, finds mcp-servers repo]
    Let me check your local knowledge base...
    Found: mcp-servers in ~/github/mcp-servers
    [Reads README.md and examples/]
    Based on your local repo, here's how to use MCP tools...
```

## Example Flows

**Discover new tool:**
```
/github-kb discover Codex MCP
→ [Searches Xiaohongshu, Tavily]
→ Found 3 repos, select to clone
→ Index updated
```

**Research on Xiaohongshu:**
```
/github-kb xiaohongshu Python数据分析
→ [Returns top notes with summaries]
```

**Fetch tweet:**
```
/github-kb twitter https://x.com/user/status/123
→ [Returns full tweet content]
```
