---
name: agent-memory-design
version: 1.0.0
min_mindforge_version: 10.0.4
status: stable
triggers: agent memory design, short-term memory, long-term memory, memory retrieval, memory consolidation, memory decay, episodic memory, semantic memory, memory architecture, working memory, memory indexing, knowledge persistence
---

# Skill — Agent Memory Design (Multi-Layer Knowledge Persistence)

## When this skill activates
When designing memory systems for AI agents, implementing context persistence across
sessions, building knowledge retrieval mechanisms, or architecting memory consolidation
pipelines. Use for any agent that needs to remember information beyond a single context
window.

Core principle: **Memory is retrieval, not storage** — the value of a memory system
is measured by: can the agent find the RIGHT information at the RIGHT time? Storage
without retrieval is a graveyard.

## Mandatory actions when this skill is active

### Memory Layer Architecture

1. **Four-tier memory model:**
   ```
   Layer 1 — Working Memory (context window)
   - Scope: current conversation turn
   - Capacity: model context limit (8K-200K tokens)
   - Persistence: none (gone when context resets)
   - Access: immediate (already in context)
   - Priority: highest — this is what the agent "sees"

   Layer 2 — Short-Term Memory (session scratchpad)
   - Scope: current session/task
   - Capacity: 10-50 key facts
   - Persistence: session duration
   - Access: explicit retrieval (agent requests it)
   - Format: JSONL scratchpad file
   - Use for: intermediate results, task progress, recent user preferences

   Layer 3 — Medium-Term Memory (project knowledge)
   - Scope: current project/workspace
   - Capacity: hundreds of entries
   - Persistence: project lifetime
   - Access: semantic search + key lookup
   - Format: structured markdown files, JSON indexes
   - Use for: architectural decisions, user patterns, project conventions

   Layer 4 — Long-Term Memory (permanent knowledge)
   - Scope: cross-project, cross-session
   - Capacity: unbounded
   - Persistence: permanent (with decay)
   - Access: semantic similarity search + knowledge graph traversal
   - Format: vector DB + knowledge graph
   - Use for: learned patterns, user preferences, domain expertise
   ```

### Retrieval Strategies

2. **Retrieval by memory layer:**
   ```
   Working Memory:
   - Already in context — no retrieval needed
   - Manage carefully: don't waste on retrievable facts

   Short-Term Memory:
   - Recency-weighted retrieval (most recent = most relevant)
   - Key-based lookup: "what was the last error message?"
   - Cleared at session end (or explicit flush)

   Medium-Term Memory:
   - Keyword + semantic hybrid search
   - Structured queries: "what auth pattern does this project use?"
   - Indexed by: topic, file path, date, relevance score

   Long-Term Memory:
   - Semantic similarity search (embedding-based)
   - Knowledge graph traversal (entity → relationship → entity)
   - Confidence-weighted (higher confidence = higher ranking)
   - Decay-adjusted (older unreinforced memories rank lower)
   ```

3. **Retrieval decision flow:**
   ```
   When agent needs information:
   1. Check working memory (already in context?) → use it
   2. Check short-term memory (recent session fact?) → retrieve and inject
   3. Check medium-term memory (project knowledge?) → search and inject summary
   4. Check long-term memory (learned pattern?) → search, verify relevance, inject
   5. If not found anywhere → ask user or research from scratch
   ```

### Memory Consolidation

4. **End-of-session consolidation pipeline:**
   ```
   Session ends → Consolidation triggers:

   1. Extract key learnings from session:
      - New facts learned (user preferences, project decisions)
      - Patterns observed (what worked, what failed)
      - Corrections received (mistakes to avoid next time)

   2. Classify each learning:
      - Short-term only (task-specific, won't matter next session) → discard
      - Medium-term (project-relevant) → write to project memory
      - Long-term (generalizable pattern) → write to permanent memory

   3. Summarize, don't dump:
      - Raw conversation → extract 5-10 key facts
      - Include WHY something matters, not just WHAT happened
      - Link to existing memories (reinforce or update)

   4. Update indexes:
      - Add new entries to search indexes
      - Update confidence scores on existing memories
      - Deprecate contradicted memories
   ```

   Rules:
   - Consolidation must be LOSSY (summarize, compress, extract — not raw dump)
   - Every memory entry needs: content, source, timestamp, confidence, tags
   - Contradictions: new information supersedes old (but keep old as "deprecated")

### Memory Decay

5. **Confidence decay model:**
   ```
   Each memory entry has a confidence score [0.0 - 1.0]:

   Initial confidence:
   - User explicitly stated: 1.0
   - Inferred from behavior: 0.7
   - Assumed from patterns: 0.5

   Decay rules:
   - Unreinforced memory: confidence -= 0.05 per week
   - Reinforced memory (used successfully): confidence = min(1.0, confidence + 0.1)
   - Contradicted memory: confidence = 0.0 (deprecated, kept for history)
   - Below threshold (confidence < 0.2): excluded from retrieval results

   Reinforcement triggers:
   - Agent retrieves memory and uses it successfully
   - User confirms a remembered fact
   - Pattern matches current observation
   ```

### Implementation Patterns

6. **Storage format by layer:**
   ```
   Short-term (JSONL scratchpad):
   {"key": "last_error", "value": "TypeError at line 42", "ts": "...", "confidence": 1.0}
   {"key": "user_intent", "value": "refactoring auth module", "ts": "...", "confidence": 0.9}

   Medium-term (structured markdown):
   ## Project: MindForge
   ### Architecture Decisions
   - Auth: JWT with refresh tokens (decided 2024-03-15, confidence: 1.0)
   - Database: PostgreSQL with Prisma ORM (decided 2024-03-10, confidence: 1.0)
   ### User Preferences
   - Prefers functional style over OOP (confidence: 0.8)
   - Wants verbose error messages in dev (confidence: 0.9)

   Long-term (vector DB + knowledge graph):
   Entry: {id, embedding, content, source, timestamp, confidence, tags, relationships}
   Graph: (pattern)--[applies_to]-->(domain)--[learned_from]-->(project)
   ```

7. **Working memory budget management:**
   ```
   Context window is finite — manage it:

   Priority for inclusion in working memory:
   1. Current user message and task context (always)
   2. Relevant retrieved memories (top-k by relevance)
   3. System instructions and constraints (always)
   4. Recent conversation history (sliding window)

   If context is filling up:
   - Summarize older conversation turns (don't drop, compress)
   - Move detailed context to short-term memory (retrieve if needed)
   - Keep only TOP-5 most relevant retrieved memories in context
   - Never sacrifice system instructions for conversation history
   ```

## Self-check before task completion

Before marking a task done when this skill was active:

- [ ] Did I define all four memory layers with clear scope and access patterns?
- [ ] Is retrieval strategy defined per layer (recency, semantic, key-based)?
- [ ] Is there a consolidation pipeline that extracts and summarizes key learnings?
- [ ] Is consolidation lossy (summarize, don't dump raw conversation)?
- [ ] Is memory decay implemented (confidence decreases without reinforcement)?
- [ ] Are contradicted memories deprecated (not deleted)?
- [ ] Is working memory budget managed (prioritized inclusion, compression when full)?
- [ ] Does every memory entry have: content, source, timestamp, confidence, tags?
