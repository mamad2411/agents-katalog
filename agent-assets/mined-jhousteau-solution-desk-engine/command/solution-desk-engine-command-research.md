---
allowed-tools: mcp__context7__resolve-library-id, mcp__context7__get-library-docs, mcp__Ref__ref_search_documentation, mcp__Ref__ref_read_url, WebSearch, Read
argument-hint: [query]
description: Research best practices and solutions
model: claude-opus-4-1-20250805
---

## Research Best Practices

Research lean solutions and best practices for: $ARGUMENTS

### Research Process

1. **Search Documentation**
   - Use Context7 MCP for library-specific documentation
   - Use MCP Ref to search technical documentation
   - Focus on official sources and best practices
   - Look for lean, simple solutions

2. **Evaluate Solutions**
   - Compare multiple approaches
   - Identify the simplest solution
   - Avoid over-engineered patterns
   - Check for standard library alternatives

3. **Web Search (if needed)**
   - Search for recent discussions
   - Find common pitfalls to avoid
   - Look for performance comparisons

### Research Priorities

Focus on finding:
- ✅ Simplest solution that works
- ✅ Standard library alternatives
- ✅ Common anti-patterns to avoid
- ✅ Performance implications
- ✅ Security considerations

### Output Format

```markdown
## Research Results: [Topic]

### Best Practice
[Simplest recommended approach]

### Why This Approach
- [Reason 1]
- [Reason 2]

### Alternatives Considered
1. [Complex approach] - Rejected because...
2. [Over-engineered solution] - Too much abstraction

### Anti-Patterns to Avoid
- [Common mistake]
- [Over-complication]

### Implementation Hints
[Specific, actionable guidance]
```

Remember: Research should lead to LESS code, not more patterns.
