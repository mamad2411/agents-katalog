---
name: "skill-discovery"
description: "Find related skills via dependency graph analysis, discover learning paths, and identify skill clusters"
---

# Skill Discovery Skill

## When to activate

- Searching for skills related to a topic (e.g., "I need to work with RAG — what skills should I read?")
- Building a learning path (e.g., "What skills lead up to agent teams?")
- Finding a skill by partial description (you remember what it does, not the exact name)
- Identifying skill clusters and related tools within a domain
- Planning a multi-skill workflow and needing to know what dependencies exist
- Debugging: understanding why a skill references another skill

## When NOT to use

- Searching for non-skill resources (guides, workflows, agents, rules) — use the general repository search instead
- One-off trivial questions (e.g., "Does prompt-caching exist?") — just search the directory
- Generic questions about Claude or LLMs unrelated to UitKit's skill collection

## Instructions

### Step 1 — Ask for a skill or topic

Phrase your query as one of:

- "Find skills related to [topic]" → Returns all skills in that domain category
- "What leads into [skill name]?" → Shows skills that reference the target skill (prerequisites)
- "What builds on [skill name]?" → Shows skills that the target skill references (next steps)
- "Show me a learning path for [goal]" → Builds a sequence of skills, each building on the previous
- "I need a skill for [description]" → Semantic match against skill names and descriptions
- "Find orphaned skills" → Lists skills with no cross-references (useful for archival or revival decisions)
- "What are the most central skills?" → Returns high-degree nodes (widely depended on)

### Step 2 — Generate or fetch the dependency graph

Run the dependency graph script and parse the output:

```bash
node scripts/dependency-graph.js --json
```

This produces an adjacency list: `{ "skill-name": ["ref1", "ref2", ...], ... }`

If you need stats instead (e.g., to find orphans):

```bash
node scripts/dependency-graph.js --stats
```

### Step 3 — Analyze the graph for your query

#### For "related skills" queries:

1. Find the skill in the graph by name (exact match, lowercase, hyphens)
2. Return all skills it references (outbound edges) — these are "downstream" or "expanding" skills
3. Also find all skills that reference it (inbound edges) — these are "upstream" or "prerequisite" skills
4. Group by category (e.g., `skills/ai-engineering/`, `skills/backend/`, etc.) for clarity

**Example:**
Query: "What skills relate to prompt-caching?"
- Outbound: prompt-caching references → [advanced-tool-use, llm-eval, ...]
- Inbound: [agent-handoff, skill-composition, ...] → reference prompt-caching
- Result: "prompt-caching is a foundational skill used in advanced tool use, LLM evaluation, and agent handoffs."

#### For "learning path" queries:

1. Start at the target skill
2. Recursively follow inbound edges (skills that lead into the target) up to 3 hops
3. Order the path by dependency: prerequisites first, target last
4. Include brief descriptions of each skill

**Example:**
Query: "What's a learning path to agent-teams?"
1. agent-teams references: [agent-handoff, multi-agent-memory, ...]
2. agent-handoff references: [session-handoff, agent-tracing, ...]
3. Order: session-handoff → agent-handoff → agent-teams (with agent-tracing as optional parallel)

#### For "orphaned skills" queries:

Compare the JSON graph output with the full skill inventory:
- Skills in the JSON graph = have inbound or outbound edges
- Skills not in the JSON graph = zero references to/from other skills

Report both categories:
- **True orphans**: No incoming or outgoing edges (consider archival or documentation)
- **Root skills**: No incoming edges but have outgoing edges (foundational, used by many)
- **Leaf skills**: Incoming edges but no outgoing edges (specialized, self-contained)

#### For "most central skills" queries:

1. Count outbound edges per skill (how many other skills it references)
2. Count inbound edges per skill (how many skills reference it)
3. Define "centrality" as inbound degree (how much depended on)
4. Return top 10–15 by centrality with their edge counts

**Example:**
```
Top central skills (by in-degree):
1. prompt-engineering: 18 incoming
2. agent-handoff: 16 incoming
3. claude-api: 14 incoming
```

### Step 4 — Present results with context

For each result, provide:

1. **Skill name** and **description** (from the skill's metadata or title)
2. **Location** (e.g., `skills/ai-engineering/`)
3. **Direction of relationship** (prerequisite, expansion, alternative, or related)
4. **Brief summary** of why the skills are related
5. **Suggested reading order** if it's a learning path

**Example output:**

```
### Skills related to "RAG"

**Prerequisites:**
- prompt-engineering (skills/ai-engineering/) — Understanding how to structure prompts before implementing retrieval
- llm-eval (skills/ai-engineering/) — Evaluating retrieval quality and relevance

**Core RAG:**
- rag-architect (skills/ai-engineering/) — Building end-to-end RAG systems

**Expansions:**
- enterprise-search (skills/ai-engineering/) — Scaling RAG to production
- mcp-server-builder (skills/ai-engineering/) — Integrating RAG with MCP servers

**Learning Path:**
1. prompt-engineering
2. llm-eval
3. rag-architect
4. (choose: enterprise-search OR mcp-server-builder)
```

### Step 5 — Offer interactive exploration

If the user wants to dig deeper, offer to:
- Visualize the full graph using the D3.js interactive visualizer (see `scripts/visualize-graph.js`)
- Explore a specific skill's neighbors in detail
- Compare two skills' reference patterns
- Run the full skill audit workflow (see `workflows/skill-audit.md`) to detect gaps or overconnections

---

## Example

**User Query:** "I want to learn about multi-agent workflows. Where should I start?"

**Skill Discovery Process:**

1. Search for "multi-agent" in skill names → find `multi-agent-memory.md`, `agent-teams.md`
2. Query the graph for these:
   ```json
   {
     "multi-agent-memory": ["agent-handoff", "agent-tracing", "session-handoff"],
     "agent-teams": ["agent-handoff", "managed-agents"]
   }
   ```
3. Find prerequisites for both: agent-handoff references session-handoff, agent-tracing
4. Build the path:
   ```
   session-handoff (basic agent communication)
   ↓
   agent-handoff (structured handoff protocol)
   ↓
   agent-tracing (observability)
   ↓
   multi-agent-memory OR agent-teams (choose path)
   ```

**Result:**
```
Multi-agent workflow learning path:

1. **session-handoff** — understand how agents hand off state
2. **agent-handoff** — structured protocols for agent-to-agent transfer
3. **agent-tracing** — observe multi-agent execution and debug issues
4. Choose one:
   - **multi-agent-memory** (if you need shared state across agents)
   - **agent-teams** (if you're building coordinated agent groups)

Estimated reading time: 20–30 minutes
```

---

## Integration with the Dependency Graph

This skill relies on `scripts/dependency-graph.js` and should be invoked whenever a user asks a discovery question. The skill effectively makes the graph queryable in natural language.

For programmatic use in other tools or workflows, reference the guide at `guides/skill-dependency-graph.md`.

---
