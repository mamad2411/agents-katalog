---
name: QIDEA - Research and Ideation
description: Research topics across multiple sources, synthesize findings, generate options matrix, and provide recommendations - no code implementation
version: 1.0.0
agents: [general-purpose]
tools: []
references: [research-methodology.md, options-matrix-template.md]
claude_tools: Read, Grep, Glob, Write, Bash
trigger: QIDEA
---

# QIDEA Skill

## Purpose

Research and ideation skill for exploring topics, comparing options, and generating recommendations **without writing code**.

**Use QIDEA when**:
- Exploring new technologies, frameworks, or tools
- Comparing multiple solutions before implementation
- Researching market trends, competitors, or best practices
- Generating ideas and validating hypotheses
- Planning architecture or design decisions

**Do NOT use QIDEA for**:
- Code implementation (use QCODE)
- Writing tests (use QCODET)
- Refactoring existing code (use QCODE)

---

## Workflow

### Phase 1: Research Planning

**Agent**: general-purpose (Explore mode)

**Actions**:
1. Parse user's research query
2. Identify research objectives (decision, comparison, validation, exploration)
3. Break down into sub-questions (3-7 focused questions)
4. Define search strategy (queries, sources, depth)

**Output**: Research plan

---

### Phase 2: Information Gathering

**Agent**: general-purpose (Explore mode)

**Actions**:
1. Search web for relevant information
2. Read documentation, articles, discussions
3. Collect data points from multiple sources
4. Validate source credibility

**Tools**: Web search (via Claude's built-in capabilities), Read

**Output**: Raw research data

---

### Phase 3: Synthesis

**Agent**: general-purpose (Explore mode)

**Actions**:
1. Organize findings by sub-question
2. Identify patterns, trends, and insights
3. Highlight contradictions or uncertainties
4. Extract key takeaways

**Output**: Synthesized findings

---

### Phase 4: Options Analysis

**Agent**: general-purpose (Explore mode)

**Actions**:
1. Generate options matrix (if comparing solutions)
2. Evaluate trade-offs (pros/cons, cost/benefit)
3. Assess fit for project context
4. Identify risks and dependencies

**Output**: Options matrix with trade-off analysis

---

### Phase 5: Recommendations

**Agent**: general-purpose (Explore mode)

**Actions**:
1. Provide clear recommendation with rationale
2. Outline next steps
3. Flag open questions or uncertainties
4. Estimate implementation effort (if applicable)

**Output**: Recommendation memo

---

## Input

**From User**:
- Research query: `QIDEA <topic>`
- Optional depth: `QIDEA <topic> --depth=deep`
- Optional focus: `QIDEA <topic> --focus=pricing`

**Examples**:
```bash
QIDEA best static site generators for documentation
QIDEA OAuth providers comparison
QIDEA serverless vs containers for edge functions
QIDEA AI coding assistant market positioning
```

---

## Output

### Research Analysis Document

File: `research/<topic-slug>/analysis.md`

```markdown
# Research Analysis: [Topic]

## Executive Summary
[2-3 sentence overview of findings and recommendation]

## Research Objectives
- [Objective 1]
- [Objective 2]

## Sub-Questions
1. [Sub-question 1]
2. [Sub-question 2]
3. [Sub-question 3]

## Findings

### [Sub-question 1]
**Summary**: [1-2 sentences]

**Key Points**:
- [Point 1] (Source: [link])
- [Point 2] (Source: [link])

**Insights**: [Analysis]

### [Sub-question 2]
...

## Options Matrix

| Criteria | Option A | Option B | Option C |
|----------|----------|----------|----------|
| Cost | $$ | $ | $$$ |
| Ease of Use | High | Medium | Low |
| Performance | Excellent | Good | Excellent |
| Community Support | Large | Small | Medium |
| Learning Curve | Low | Medium | High |
| Best For | [Use case] | [Use case] | [Use case] |

## Trade-Off Analysis

### Option A: [Name]
**Pros**:
- [Pro 1]
- [Pro 2]

**Cons**:
- [Con 1]
- [Con 2]

**Best For**: [Context where this option excels]

### Option B: [Name]
...

## Recommendation

**Recommended Option**: [Option X]

**Rationale**:
- [Reason 1]
- [Reason 2]
- [Reason 3]

**Next Steps**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Open Questions**:
- [Question 1]
- [Question 2]

**Estimated Implementation Effort**: [X SP or Y weeks]

## Sources
1. [Source 1 title] - [URL]
2. [Source 2 title] - [URL]
...
```

---

## Examples

### Example 1: Technology Comparison

**Query**:
```bash
QIDEA OAuth providers for SaaS app (Google, GitHub, Auth0)
```

**Output**: `research/oauth-providers/analysis.md`

**Content**:
- Sub-questions: Pricing, ease of integration, supported features, reliability
- Options matrix comparing Google, GitHub, Auth0
- Trade-off analysis
- Recommendation: Auth0 for multi-provider support, Google for simplicity

**Estimated Effort**: 0.5 SP (30-40 minutes)

---

### Example 2: Market Research

**Query**:
```bash
QIDEA AI coding assistants market positioning for solo founder
```

**Output**: `research/ai-coding-market/analysis.md`

**Content**:
- Sub-questions: TAM, competitors, pricing models, unmet needs
- Findings: Market size, top 5 competitors, pricing benchmarks
- Options matrix: Positioning strategies (price, features, niche)
- Recommendation: Focus on niche (e.g., indie devs) with freemium model

**Estimated Effort**: 1-2 SP (1-2 hours)

---

### Example 3: Architecture Decision

**Query**:
```bash
QIDEA serverless vs containers for real-time API
```

**Output**: `research/serverless-vs-containers/analysis.md`

**Content**:
- Sub-questions: Cost, latency, scaling, vendor lock-in
- Options matrix: AWS Lambda, Cloud Run, ECS, self-hosted
- Trade-off analysis: Cold start vs always-on cost
- Recommendation: Cloud Run for real-time API (balance of cost and latency)

**Estimated Effort**: 0.5-1 SP (30-60 minutes)

---

### Example 4: Best Practices Research

**Query**:
```bash
QIDEA password hashing best practices 2026
```

**Output**: `research/password-hashing/analysis.md`

**Content**:
- Sub-questions: Algorithms, salt strategies, computational cost, future-proofing
- Findings: bcrypt vs Argon2, OWASP recommendations
- Recommendation: Argon2id with cost factor 2 (OWASP current guidance)
- Next steps: Install argon2 library, implement wrapper function

**Estimated Effort**: 0.3 SP (15-20 minutes)

---

## Configuration

### Default Settings

- **Depth**: medium (20-40 minutes)
- **Sources**: Web search, official docs, community discussions
- **Output Format**: Markdown

### Custom Configuration

Create `.qidea.json` in project root:

```json
{
  "depth": "medium",
  "max_duration_minutes": 40,
  "output_dir": "research",
  "include_sources": true,
  "options_matrix": true,
  "trade_off_analysis": true,
  "recommendation_required": true,
  "source_credibility_check": true
}
```

---

## Integration with Other QShortcuts

### With QPLAN (Planning)

```bash
# 1. Research options
QIDEA OAuth providers comparison

# 2. Read recommendation
cat research/oauth-providers/analysis.md

# 3. Plan implementation
QPLAN implement OAuth with Auth0

# 4. Implement
QCODE
```

---

### With QWRITE (Content)

```bash
# 1. Research topic
QIDEA AI coding assistants market trends

# 2. Write article based on research
QWRITE educational article on AI coding trends --source=research/ai-coding-market/analysis.md
```

---

### With QARCH (AI Systems)

```bash
# 1. Research learning algorithms
QIDEA reinforcement learning vs supervised learning for game AI

# 2. Design AI system
QARCH design game AI using reinforcement learning

# 3. Implement
QCODE
```

---

## Quality Checklist

Before marking QIDEA complete, verify:

- [ ] Research objectives are clear
- [ ] Sub-questions are specific and answered
- [ ] Findings are sourced (include URLs)
- [ ] Options matrix covers relevant criteria
- [ ] Trade-off analysis explains pros/cons
- [ ] Recommendation is clear with rationale
- [ ] Next steps are actionable
- [ ] Open questions are documented

---

## Common Patterns

### Pattern: Technology Evaluation

**Sub-Questions**:
1. What is the technology and how does it work?
2. What are the key use cases?
3. What are the limitations and trade-offs?
4. Who are the vendors/projects?
5. What are the adoption trends?

**Sources**: Official docs, GitHub repos, Stack Overflow, Reddit discussions

---

### Pattern: Competitive Analysis

**Sub-Questions**:
1. Who are the direct competitors?
2. What are their positioning strategies?
3. What are their pricing models?
4. What do users complain about?
5. What are the gaps in their offerings?

**Sources**: Company websites, product reviews, Reddit, Twitter, G2 Crowd

---

### Pattern: Best Practices Research

**Sub-Questions**:
1. What do industry leaders recommend?
2. What are the current standards (OWASP, NIST, etc.)?
3. What are common pitfalls?
4. What are emerging trends?

**Sources**: OWASP, NIST, Mozilla, Google Security Blog, official documentation

---

### Pattern: Pricing Research

**Sub-Questions**:
1. What are common pricing models in this space?
2. What do competitors charge?
3. What are customers willing to pay?
4. What are the cost drivers?

**Sources**: Competitor pricing pages, SaaS pricing databases, user surveys

---

## Anti-Patterns to Avoid

❌ **Too Broad**: "Research AI"
✅ **Focused**: "Research AI coding assistants market positioning for solo founders"

❌ **No Options Matrix**: Just list findings
✅ **Structured**: Compare options in a matrix with clear criteria

❌ **No Recommendation**: Leave decision to user
✅ **Actionable**: Provide clear recommendation with rationale

❌ **Unsourced Claims**: "Most developers prefer X"
✅ **Sourced**: "75% of developers prefer X (Source: Stack Overflow Survey 2025)"

❌ **Implementation Details**: Include code snippets
✅ **Research Only**: Focus on comparison, defer implementation to QCODE

---

## Troubleshooting

### Issue: Research Too Broad

**Problem**: QIDEA returns unfocused results

**Solution**: Narrow the query
```bash
# Instead of: QIDEA authentication
# Use: QIDEA OAuth vs JWT for API authentication
```

---

### Issue: No Clear Recommendation

**Problem**: User wants a recommendation but QIDEA presents only options

**Solution**: Add explicit recommendation request
```bash
QIDEA <topic> --recommend
```

---

### Issue: Research Takes Too Long

**Problem**: QIDEA exceeds time budget

**Solution**: Reduce depth
```bash
QIDEA <topic> --depth=quick  # 10-15 minutes
```

Or set max duration:
```bash
QIDEA <topic> --max-duration=20
```

---

### Issue: Outdated Information

**Problem**: Research returns old data

**Solution**: Specify recency requirement
```bash
QIDEA <topic> --since=2025
```

---

## Story Point Estimation

| Depth | Duration | Sub-Questions | Sources | Effort (SP) |
|-------|----------|---------------|---------|-------------|
| Quick | 10-15 min | 2-3 | 3-5 | 0.2-0.3 |
| Medium | 20-40 min | 4-5 | 8-12 | 0.5-1 |
| Deep | 60-120 min | 6-8 | 15-25 | 1-2 |

**Baseline**: 1 SP = Medium-depth comparative analysis with options matrix and recommendation

---

## References

See `references/` directory:
- `research-methodology.md` - Research planning and execution guide
- `options-matrix-template.md` - Template for options comparison

---

## Research Quality Standards

### Source Credibility Tiers

**Tier 1 (Highest Credibility)**:
- Official documentation
- Peer-reviewed papers
- Industry standards (OWASP, NIST, W3C)
- Government/academic institutions

**Tier 2 (Moderate Credibility)**:
- Reputable tech blogs (Mozilla, Google, Microsoft)
- Stack Overflow (high-vote answers)
- GitHub repos (>1k stars)
- Conference talks

**Tier 3 (Use with Caution)**:
- Reddit discussions
- Twitter threads
- Medium articles
- Personal blogs

**Rule**: High-stakes decisions require ≥2 Tier 1 sources per key claim.

---

## Contributing

For issues or enhancements to QIDEA skill:
- **Email**: skills@sparkry.ai
- **License**: MIT
