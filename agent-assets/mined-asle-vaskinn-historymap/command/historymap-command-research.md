# Parallel Research

Spawn multiple research agents in parallel to gather information quickly.

## Instructions

When the user provides a research topic or question, spawn 3-5 agents in PARALLEL using a single message with multiple Task tool calls:

1. **Codebase Agent** - Search existing code for patterns, implementations
2. **Docs Agent** - Search project documentation for specs, decisions
3. **Web Agent** - Search web for external resources, APIs, examples
4. **Architecture Agent** - Analyze architectural implications

## Example Usage

User: "research how to add road date inheritance"

You should spawn ALL agents in a SINGLE message:

```
<Task 1: Codebase search for road date logic>
<Task 2: Docs search for road schema>
<Task 3: Web search for road date inference techniques>
<Task 4: Architecture review of date inheritance patterns>
```

## Agent Prompts

### Codebase Agent
```
Search the codebase for: [topic]
- Find existing implementations
- Identify patterns used
- List relevant files
- Note any TODOs or comments
Return: file paths, code snippets, patterns found
```

### Docs Agent
```
Search project docs for: [topic]
- Check docs/tech/ for technical specs
- Check docs/spec/ for requirements
- Check docs/todo/ for planned work
Return: relevant doc sections, decisions made, gaps
```

### Web Agent (if external research needed)
```
Web search for: [topic]
- Find best practices
- Find library documentation
- Find similar implementations
Return: URLs, key techniques, recommendations
```

### Architecture Agent
```
Analyze architectural implications of: [topic]
- Check schema consistency
- Verify pattern alignment
- Identify dependencies
Return: consistency issues, pattern recommendations
```

## Output Format

After all agents complete, synthesize:

```markdown
## Research Summary: [Topic]

### Existing Code
- [findings from codebase agent]

### Documentation
- [findings from docs agent]

### External Resources
- [findings from web agent]

### Architecture Considerations
- [findings from arch agent]

### Recommended Approach
[Your synthesis of all findings]
```

## Key: PARALLEL Execution

The speed benefit comes from spawning agents IN PARALLEL.

WRONG (sequential):
```
1. Call Task tool for codebase
2. Wait for result
3. Call Task tool for docs
4. Wait for result
...
```

RIGHT (parallel):
```
1. Call Task tool for codebase AND docs AND web AND arch (single message, 4 tool calls)
2. Wait for all results
3. Synthesize
```
