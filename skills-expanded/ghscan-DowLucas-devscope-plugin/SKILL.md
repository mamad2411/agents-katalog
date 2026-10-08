---
allowed-tools: Bash(bash:*), Bash(source:*), Bash(cat:*), Bash(jq:*), Bash(grep:*), Bash(sed:*), Bash(echo:*), Bash(curl:*), Bash(find:*), Bash(wc:*), Bash(sort:*), Bash(head:*), Bash(tail:*), Bash(stat:*), Bash(date:*), Read, Edit, Write, Glob, Grep, Agent, AskUserQuestion
description: Post-mortem analysis of Claude Code sessions to identify friction, knowledge gaps, and optimize workflows by combining DevScope server analytics with local session analysis
---

## Your task

Run a systematic upskill audit that combines DevScope server analytics with local Claude Code session analysis. The goal is to identify friction, knowledge gaps, and workflow inefficiencies — then propose actionable improvements to CLAUDE.md files, memory entries, and workflows.

**Important**: Present findings from each phase as you go (don't wait until the end). After all phases, synthesize into a prioritized action list.

---

### Phase 1: DevScope Server Analytics

Source the plugin helpers and check if the DevScope server is reachable:

```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/_helpers.sh"

echo "=== CONFIG ==="
echo "URL: $DEVSCOPE_URL"
echo "API_KEY: ${DEVSCOPE_API_KEY:+configured}"

echo "=== HEALTH CHECK ==="
HEALTH=$(_ds_health_check)
HC_STATUS=$?
echo "HC_STATUS: $HC_STATUS"
echo "HEALTH: $HEALTH"
```

**If the server is reachable** (`HC_STATUS` is 0), fetch analytics data. Run these API calls to gather the server-computed baseline:

```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/_helpers.sh"

# Failure clusters — where friction is happening
RAW=$(_ds_api_get "/api/insights/failure-clusters?days=14")
HTTP_STATUS=$(echo "$RAW" | tail -1)
BODY=$(echo "$RAW" | sed '$d')
echo "=== FAILURE CLUSTERS (HTTP $HTTP_STATUS) ==="
echo "$BODY" | jq '.' 2>/dev/null || echo "$BODY"
```

```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/_helpers.sh"

# Tool usage breakdown
RAW=$(_ds_api_get "/api/insights/tools?days=14")
HTTP_STATUS=$(echo "$RAW" | tail -1)
BODY=$(echo "$RAW" | sed '$d')
echo "=== TOOL USAGE (HTTP $HTTP_STATUS) ==="
echo "$BODY" | jq '.' 2>/dev/null || echo "$BODY"
```

```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/_helpers.sh"

# Anti-patterns detected
RAW=$(_ds_api_get "/api/patterns/anti?limit=10")
HTTP_STATUS=$(echo "$RAW" | tail -1)
BODY=$(echo "$RAW" | sed '$d')
echo "=== ANTI-PATTERNS (HTTP $HTTP_STATUS) ==="
echo "$BODY" | jq '.' 2>/dev/null || echo "$BODY"
```

```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/_helpers.sh"

# Effective patterns
RAW=$(_ds_api_get "/api/patterns?effectiveness=effective&limit=10")
HTTP_STATUS=$(echo "$RAW" | tail -1)
BODY=$(echo "$RAW" | sed '$d')
echo "=== EFFECTIVE PATTERNS (HTTP $HTTP_STATUS) ==="
echo "$BODY" | jq '.' 2>/dev/null || echo "$BODY"
```

```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/_helpers.sh"

# AI-generated insights
RAW=$(_ds_api_get "/api/ai/insights?limit=10")
HTTP_STATUS=$(echo "$RAW" | tail -1)
BODY=$(echo "$RAW" | sed '$d')
echo "=== AI INSIGHTS (HTTP $HTTP_STATUS) ==="
echo "$BODY" | jq '.' 2>/dev/null || echo "$BODY"
```

```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/_helpers.sh"

# Token usage and cost
RAW=$(_ds_api_get "/api/insights/tokens?days=14")
HTTP_STATUS=$(echo "$RAW" | tail -1)
BODY=$(echo "$RAW" | sed '$d')
echo "=== TOKEN USAGE (HTTP $HTTP_STATUS) ==="
echo "$BODY" | jq '.' 2>/dev/null || echo "$BODY"
```

```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/_helpers.sh"

# Skill usage
RAW=$(_ds_api_get "/api/insights/skills?days=14")
HTTP_STATUS=$(echo "$RAW" | tail -1)
BODY=$(echo "$RAW" | sed '$d')
echo "=== SKILL USAGE (HTTP $HTTP_STATUS) ==="
echo "$BODY" | jq '.' 2>/dev/null || echo "$BODY"
```

After fetching, summarize the server analytics:
- **Friction hotspots**: Which tools/commands fail most? What failure clusters exist?
- **Anti-patterns**: What bad habits have been detected? How severe?
- **Effective patterns**: What's working well? (preserve these)
- **Cost/efficiency**: Token burn rate, cache hit rates, compaction frequency
- **Skill usage**: Which skills are used? Which are never used?

**If the server is NOT reachable**, skip Phase 1 and note that server analytics were unavailable. Suggest running `/devscope:setup` if the URL looks like the default localhost.

---

### Phase 2: Local Session Analysis

These analyses read local session JSONL files directly — they capture conversation-level signals that the server doesn't track (for privacy reasons).

#### 2a. Conversation Intelligence

Run the conversation analysis script:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/upskill/analyze-conversations.sh" --days 14 --verbose
```

This detects:
- **Corrections**: Where the user told Claude it was wrong (HIGH/MEDIUM confidence)
- **Knowledge gaps**: Where the user had to provide information Claude should have known
- **Repeated instructions**: Same instruction given across 3+ sessions (should be in CLAUDE.md)
- **Workway patterns**: User preferences expressed with "always", "never", "prefer", etc.

#### 2b. Interruption Analysis

Run the interruption analysis script:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/upskill/analyze-interruptions.sh" --days 14 --verbose
```

This detects:
- **Course corrections**: User interrupted and redirected Claude's approach
- **Questions**: User interrupted to ask for clarification
- **Impatience**: User wanted faster progress
- **Abandonment**: User switched to a different topic entirely
- **Friction hotspots**: Sessions with the most interruptions

---

### Phase 3: CLAUDE.md & Memory Hygiene

#### 3a. CLAUDE.md Hygiene

Run the CLAUDE.md hygiene analyzer:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/upskill/analyze-claude-md.sh" --verbose
```

This checks:
- Dead file/directory references in CLAUDE.md files
- Duplicated guidance across multiple CLAUDE.md files
- Dead script references
- Staleness (CLAUDE.md not updated when service code changed)

#### 3b. Memory Quality

Run the memory quality analyzer:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/upskill/analyze-memory.sh"
```

This checks:
- MEMORY.md line count vs 200-line truncation limit
- Broken topic file references
- Stale date references (>30 days)
- Orphaned topic files (exist but not linked from MEMORY.md)

---

### Phase 4: Synthesis

After completing all phases, cross-reference findings and produce a **prioritized action list**. Group actions by type:

| Tag | Source | Action Type |
|-----|--------|-------------|
| `[RULE]` | User corrections | Add to CLAUDE.md — things Claude should stop doing |
| `[KNOWLEDGE]` | Knowledge gaps | Add to CLAUDE.md — facts Claude should already know |
| `[WORKFLOW]` | Repeated instructions | Add to CLAUDE.md or create automation |
| `[CONVENTION]` | Workway patterns | Add to CLAUDE.md — user preferences to codify |
| `[FRICTION]` | Server failure clusters | Investigate and fix root cause |
| `[ANTI-PATTERN]` | Server anti-patterns | Add guardrails or CLAUDE.md guidance |
| `[MEMORY]` | Memory quality issues | Fix broken refs, prune stale entries, rebalance |
| `[HYGIENE]` | CLAUDE.md staleness | Update or remove stale guidance |

**Synthesis checklist:**
1. Cross-reference discoveries with existing MEMORY.md — if not documented, recommend additions
2. When errors suggest architecture misunderstanding, check if the area is in CLAUDE.md. If documented but errors persist, recommend revision. If undocumented, recommend addition
3. Check MEMORY.md line count — if approaching 200, recommend moving large sections to topic files
4. Identify stale memory entries (dates >30 days old with no ongoing relevance) and recommend pruning
5. Look for overlap between server-detected anti-patterns and local conversation corrections — these are the highest-priority items

**Output format**: Present the final action list sorted by priority (high → medium → low). For each action, include:
- The tag (e.g., `[RULE]`)
- What to change and where (specific file + section)
- The evidence (which session, which correction, which failure cluster)
- A draft of the proposed change (ready to apply)

Ask the user which actions they'd like to apply before making any changes.
