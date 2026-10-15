---
name: quick-fix-suggestion
description: |
  Use this skill when the user wants to get quick fix suggestions for an issue,
  "how to fix this issue", "where should I make changes", "quick-fix-suggestion",
  "suggest fix", "fix suggestion", "how to implement this issue",
  or before starting implementation to understand the scope of changes.
  This skill analyzes the issue content, locates relevant code in the repository,
  and suggests which files to modify with draft implementation plans.
  Requires Gitee MCP Server to be configured and must be run in a local git repository.
version: 1.0.0
requires:
  mcp-servers:
    - gitee
---

> **Note**: If you have `mcporter` installed locally, you should use `mcporter` to invoke the MCP tool instead of directly calling the MCP tool. The `mcporter` CLI provides a more convenient interface and better error handling.

# Quick Fix Suggestion via Gitee MCP

Analyze a Gitee Issue and generate intelligent fix suggestions including:
- Identification of files that need to be modified
- Code location hints (line numbers, function names)
- Draft implementation code snippets
- Step-by-step implementation plan

## Prerequisites

- Gitee MCP Server configured (tools: `get_repo_issue_detail`, `list_issue_comments`, `search_files_by_content`, `get_file_content`)
- Must be executed in a local clone of the repository
- User must provide: repository owner, repository name, Issue number

## Local-First Search Strategy

> **Why Local-First?**
>
> This skill prioritizes **local file operations** over Gitee API for code search:
> - **Speed**: Local searches complete in milliseconds vs. seconds for API calls
> - **No Rate Limits**: No 100 requests/minute restriction
> - **Real-time**: Searches include uncommitted local changes
> - **Cost**: Zero API usage costs

### Tool Selection Priority

| Priority | Tool | Availability |
|----------|------|--------------|
| 1st | `glob`, `grep` (built-in) | 100% |
| 2nd | `ast_grep_search`, `lsp_find_references` | 100% |
| 3rd | Git commands (via bash) | ~90% |
| Last | Gitee API (`search_files_by_content`) | Fallback only |

## Steps

### Step 1: Fetch Issue Details

Use `get_repo_issue_detail` to retrieve full Issue information:
- Title and description
- Labels (bug/feature/enhancement)
- Existing comments

### Step 2: Analyze Issue Content

**Identify Issue Type:**
- `bug`: error, crash, broken, not working, 错误, 失败
- `feature`: add, support, implement, new, 新增, 添加
- `enhancement`: improve, optimize, 改进, 优化

**Extract Code Entities:**
- Function names (in backticks or patterns)
- Class names
- File names
- Error messages / stack traces

### Step 3: Search Code (Local-First)

Use built-in tools in priority order:

```typescript
// 1. File name search (fastest)
glob(`**/*${keyword}*.{js,ts,py,go}`, { cwd: localRepoPath })

// 2. Content search
grep({
  pattern: `function\\s+${funcName}`,
  path: localRepoPath,
  output_mode: "content"
})

// 3. AST search (semantic)
ast_grep_search({
  pattern: "function $NAME($$$) { $$$ }",
  lang: "javascript",
  paths: [localRepoPath]
})

// 4. Fallback: Remote search (max 3 calls)
if (localResults.length < 3) {
  search_files_by_content({ owner, repo, query: keyword, limit: 10 })
}
```

### Step 4: Read and Analyze Key Files

Read each candidate file to:
- Identify relevant functions/classes
- Understand code structure
- Assess how the Issue relates to this file

### Step 5: Generate Fix Suggestions

Present results in this format:

```markdown
## Issue #{number}: {title}

**Type**: {bug/feature} | **Confidence**: {score}% | **Complexity**: {low/medium/high}

### Primary Files (Must Modify)

**1. `{file_path}`** [Confidence: XX%]
- **Change**: {modify/add/delete}
- **Location**: Around line {X}

<details>
<summary>Code Draft</summary>

```{language}
// Current:
{existing_code}

// Suggested:
{suggested_code}
```
</details>

### Secondary Files (May Need Changes)

- `{file_path}`: {reason}

### Implementation Plan

1. **{step 1}** - File: `{file}`, ~{time}
2. **{step 2}** - File: `{file}`, ~{time}

### Testing Suggestions

- {test suggestion}

### Questions for You

1. {uncertainty_question}
```

### Step 6: Handle User Response

- **Approve**: Summarize and transition to `implement-issue` skill
- **Adjust**: Re-analyze with new information
- **Search More**: Expand search scope
- **Cancel**: Offer other help

## Notes

- Always indicate confidence level - ask for clarification when uncertain
- Follow existing code patterns when suggesting changes
- Warn immediately if Issue mentions credentials/secrets
- If unable to locate relevant code, ask for more context rather than guessing

## References

- [Tool Reference Guide](references/TOOL_REFERENCE.md) - Detailed search patterns and tool usage
