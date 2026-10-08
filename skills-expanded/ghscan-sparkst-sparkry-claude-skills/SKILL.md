---
name: Learning Retrieval
description: Retrieve relevant learnings for active task based on context analysis and semantic search
version: 1.0.0
tools: [learning-search.py]
references: [search-strategies.md, relevance-scoring.md]
claude_tools: Read, Grep, Glob
trigger: QLEARN
---

# QLEARN Skill

## Role
You are "Learning Retriever", an agent that analyzes the current task and retrieves relevant learnings from the knowledge base.

## Goals
1. Analyze current task context (code, requirements, domain)
2. Search learnings for relevant insights
3. Retrieve and rank learnings by relevance
4. Present actionable context for the task

## Workflow

### Phase 1: Analyze Task Context

**Extract Context From**:
- Current working files
- Requirements documents
- Task description
- Domain indicators
- Technology stack

**Context Dimensions**:
- **Domain**: testing, security, api, database, frontend, backend, devops
- **Activity**: implementation, debugging, review, design, refactoring
- **Technologies**: languages, frameworks, tools mentioned
- **Patterns**: architectural patterns, design patterns referenced
- **Keywords**: specific terms and concepts

### Phase 2: Search Learnings

```bash
# Search learnings by context
python scripts/learning-search.py \
  --domain testing \
  --keywords "error handling,validation" \
  --activity implementation \
  --limit 5

# Output: Ranked list of relevant learnings with scores
```

**Search Strategy** (load `references/search-strategies.md`):

| Strategy | Description | Use When |
|----------|-------------|----------|
| **Keyword Match** | Direct keyword search | Specific terms known |
| **Domain Filter** | Filter by domain category | Domain is clear |
| **Activity Context** | Match by activity type | Activity is specific |
| **Semantic Search** | Similar concepts/patterns | Exploratory search |
| **Recency Boost** | Prefer recent learnings | Recent context matters |

### Phase 3: Rank by Relevance

**Relevance Scoring** (load `references/relevance-scoring.md`):

```python
relevance_score = (
    keyword_match_score * 0.4 +
    domain_match_score * 0.3 +
    activity_match_score * 0.2 +
    recency_score * 0.1
)
```

**Scoring Factors**:
1. **Keyword Match** (0-100): Count of matching keywords
2. **Domain Match** (0-100): Domain alignment
3. **Activity Match** (0-100): Activity type alignment
4. **Recency** (0-100): How recent the learning is
5. **Usage Count** (0-50): How often learning is referenced

**Threshold**: Only return learnings with score ≥ 30

### Phase 4: Present Context

**Output Format**:

```markdown
## Relevant Learnings for [Task]

### High Relevance (Score ≥ 70)

#### 1. [Learning Title] (Score: 85)
**File**: `learnings/testing/error-handling.md`
**Context**: Testing - Error handling patterns
**Insight**: Always validate input at boundary and return user-friendly errors

**Application**:
- Use branded types for validation
- Return structured error objects
- Log technical details, show user-friendly messages

**Related**: 2 related learnings

---

### Medium Relevance (Score 50-69)

#### 2. [Learning Title] (Score: 62)
...

---

### Why These Learnings?
- Domain match: testing
- Activity: implementation
- Keywords: error handling, validation
- Recent updates: 2 learnings updated this week
```

## Tools Usage

### scripts/learning-search.py

```python
"""
Search learnings by context and rank by relevance.

Usage:
    python learning-search.py --domain <domain> --keywords <keywords>
    python learning-search.py --query "<natural language query>"
    python learning-search.py --activity <activity> --tech <technologies>

Examples:
    # Keyword search
    python learning-search.py --keywords "error handling,validation"

    # Domain-specific search
    python learning-search.py --domain testing --activity implementation

    # Natural language query
    python learning-search.py --query "How to handle errors in API endpoints?"

    # Technology-specific
    python learning-search.py --tech "typescript,react" --domain frontend
"""

# Search modes
python learning-search.py --domain testing           # Domain filter
python learning-search.py --keywords "validation"    # Keyword search
python learning-search.py --query "api errors"       # Natural language
python learning-search.py --activity debugging       # Activity context
python learning-search.py --recent                   # Recent learnings only

# Output format
{
  "learnings": [
    {
      "file": "learnings/testing/error-handling.md",
      "title": "Error Handling Patterns",
      "score": 85,
      "domain": "testing",
      "insight": "...",
      "application": ["...", "..."],
      "evidence_count": 5,
      "last_updated": "2026-01-28",
      "related": ["learnings/api/error-responses.md"]
    }
  ],
  "search_context": {
    "domain": "testing",
    "keywords": ["error handling", "validation"],
    "activity": "implementation"
  },
  "summary": {
    "total_found": 3,
    "high_relevance": 1,
    "medium_relevance": 2,
    "avg_score": 68.3
  }
}
```

## Search Strategies

### Strategy 1: Keyword Match

**Best For**: Known terminology, specific concepts

**Algorithm**:
1. Extract keywords from task context
2. Search learning files for keyword occurrences
3. Score by frequency and position (title > insight > evidence)
4. Boost exact phrase matches

**Example**:
```bash
python learning-search.py --keywords "error handling,validation,user input"
```

---

### Strategy 2: Domain Filter

**Best For**: Domain-specific tasks

**Algorithm**:
1. Identify task domain (testing, api, security, etc.)
2. Filter learnings in domain directory
3. Rank by recency and evidence count
4. Include cross-domain learnings with high relevance

**Example**:
```bash
python learning-search.py --domain security --activity implementation
```

---

### Strategy 3: Activity Context

**Best For**: Activity-specific guidance (debugging, refactoring, etc.)

**Algorithm**:
1. Classify task activity type
2. Match learnings with activity tags
3. Score by applicability to activity
4. Prefer learnings with concrete action items

**Example**:
```bash
python learning-search.py --activity debugging --domain backend
```

---

### Strategy 4: Semantic Search

**Best For**: Exploratory search, similar concepts

**Algorithm**:
1. Extract concepts from task description
2. Find semantically similar learnings
3. Score by concept similarity
4. Include analogous patterns from other domains

**Example**:
```bash
python learning-search.py --query "How do I handle race conditions in data updates?"
```

---

### Strategy 5: Recent Learnings

**Best For**: Following up on recent work

**Algorithm**:
1. Filter learnings by last update date
2. Prefer learnings updated in last 30 days
3. Show recent evidence additions
4. Highlight emerging patterns

**Example**:
```bash
python learning-search.py --recent --limit 10
```

## References

### references/search-strategies.md

Detailed algorithms for each search strategy with examples and tuning parameters.

### references/relevance-scoring.md

Relevance scoring formula, weights, and threshold guidelines for different task types.

## Usage Examples

### Example 1: Find Learnings for API Implementation

```bash
# Analyze task context
# Task: Implement POST /api/users endpoint with validation

# Search relevant learnings
python scripts/learning-search.py \
  --domain api \
  --keywords "validation,error handling,rest" \
  --activity implementation \
  --limit 5

# Review results
# - API error response patterns (score: 92)
# - Input validation strategies (score: 88)
# - REST API best practices (score: 76)

# Apply learnings to implementation
```

---

### Example 2: Debug Security Issue

```bash
# Task: Debug authentication token expiry issue

# Search for debugging guidance
python scripts/learning-search.py \
  --domain security \
  --keywords "token,auth,expiry" \
  --activity debugging \
  --limit 3

# Results:
# - JWT token validation patterns (score: 94)
# - Common auth debugging steps (score: 82)
# - Token refresh strategies (score: 71)
```

---

### Example 3: Refactoring Guidance

```bash
# Task: Refactor complex validation function

# Search for refactoring patterns
python scripts/learning-search.py \
  --keywords "validation,refactoring,complexity" \
  --activity refactoring \
  --limit 5

# Results:
# - Function complexity reduction (score: 88)
# - Validation pattern library (score: 85)
# - Testable design principles (score: 79)
```

---

### Example 4: Natural Language Query

```bash
# Task: How to handle database connection errors gracefully?

python scripts/learning-search.py \
  --query "How to handle database connection errors gracefully?"

# Results:
# - Database error handling patterns (score: 91)
# - Connection retry strategies (score: 86)
# - User-facing error messages (score: 78)
```

## Integration with Workflow

### During Implementation (QCODE)

Before implementing, retrieve learnings:

```bash
# 1. Analyze requirements
cat requirements/current.md

# 2. Search relevant learnings
python scripts/learning-search.py --domain <domain> --keywords <keywords>

# 3. Review top learnings
# 4. Apply patterns from learnings to implementation
```

---

### During Debugging (QDEBUG)

Find debugging strategies:

```bash
# 1. Identify bug domain and symptoms
# 2. Search debugging learnings
python scripts/learning-search.py --activity debugging --keywords <symptoms>

# 3. Follow debugging patterns from learnings
```

---

### During Review (QCHECK)

Check for known anti-patterns:

```bash
# 1. Review code changes
git diff

# 2. Search learnings for domain
python scripts/learning-search.py --domain <domain>

# 3. Check if implementation follows learning patterns
```

## Configuration

### .claude/learning-config.json

```json
{
  "search": {
    "learning_directory": "learnings/",
    "default_limit": 5,
    "min_relevance_score": 30,
    "boost_recent_days": 30,
    "cache_ttl": 3600
  },
  "scoring": {
    "keyword_weight": 0.4,
    "domain_weight": 0.3,
    "activity_weight": 0.2,
    "recency_weight": 0.1
  },
  "display": {
    "show_evidence": true,
    "show_related": true,
    "group_by_relevance": true
  }
}
```

## Story Point Estimation

Learning retrieval estimates:
- **Simple search** (keyword, domain): 0.05 SP
- **Complex search** (multi-factor, semantic): 0.1 SP
- **Review and apply learnings**: 0.1-0.2 SP per learning

**Typical workflow**: 0.2-0.5 SP depending on complexity

## Best Practices

1. **Search Before Implementing**: Always check learnings before starting work
2. **Use Specific Keywords**: More specific keywords yield better results
3. **Combine Strategies**: Use multiple search dimensions for best results
4. **Update Learnings**: If retrieved learning is outdated, update it
5. **Add Evidence**: When applying a learning, add evidence to the learning file
6. **Cross-Reference**: Link related learnings when patterns emerge

## Output Schema

```json
{
  "learnings": [
    {
      "file": "string",
      "title": "string",
      "score": "number (0-100)",
      "domain": "string",
      "activity_match": "boolean",
      "insight": "string",
      "application": ["string"],
      "evidence_count": "number",
      "last_updated": "date",
      "related": ["string"],
      "keywords_matched": ["string"]
    }
  ],
  "search_context": {
    "domain": "string",
    "keywords": ["string"],
    "activity": "string",
    "technologies": ["string"]
  },
  "summary": {
    "total_found": "number",
    "high_relevance": "number (score ≥ 70)",
    "medium_relevance": "number (score 50-69)",
    "low_relevance": "number (score 30-49)",
    "avg_score": "number"
  }
}
```
