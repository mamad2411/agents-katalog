---
name: code-smells
description: Analyze code for smells, anti-patterns, and refactoring opportunities. Read-only analysis, no code changes.
---

# Code Smells Detection Skill

Analyze code for smells, anti-patterns, and refactoring opportunities. Read-only analysis — no code changes.

## When to Use
- Before starting a refactoring effort
- During code review to identify structural issues
- When a module "feels wrong" but you can't pinpoint why
- To assess technical debt in a specific area

## Process

1. **Determine scope**: Use `$ARGUMENTS` as target path. Default to current project root.

2. **Automated scan**: Run available tools based on project type:

   **JavaScript/TypeScript:**
   ```
   npx knip --reporter compact 2>/dev/null          # unused exports/deps
   npx depcheck 2>/dev/null                           # unused packages
   wc -l $(find <scope> -name '*.ts' -o -name '*.tsx' -o -name '*.js' -o -name '*.jsx') | sort -rn | head -20
   ```

   **Python:**
   ```
   pylint --disable=all --enable=R,C <scope> 2>/dev/null | head -30
   wc -l $(find <scope> -name '*.py') | sort -rn | head -20
   ```

   **General (any language):**
   ```
   # Largest files (complexity indicator)
   wc -l <files> | sort -rn | head -20

   # Deep nesting
   grep -rn '^\s\{12,\}' <scope> --include='*.ts' --include='*.py' | head -20

   # Magic numbers
   grep -rn '[^a-zA-Z0-9_]\([0-9]\{3,\}\)[^a-zA-Z0-9_]' <scope> | head -20

   # TODO/FIXME/HACK markers
   grep -rn 'TODO\|FIXME\|HACK\|XXX\|WORKAROUND' <scope> | head -30
   ```

3. **Manual inspection**: Read the top 5 largest files. Look for:
   - Functions > 40 lines
   - Classes > 300 lines or 10+ methods
   - Parameter lists > 5 params
   - Nested conditions > 3 levels deep
   - Duplicated code blocks (similar structure in multiple places)
   - God objects (one module importing/used by everything)

4. **Dependency check**: Grep for circular imports:
   ```
   # Map imports to find circular references
   grep -rn "import.*from\|require(" <scope> --include='*.ts' --include='*.js'
   ```

## Severity Classification

| Severity | Criteria | Action |
|----------|----------|--------|
| **Critical** | Bugs likely, blocking testability, circular deps | Fix immediately |
| **Major** | Maintainability risk, high complexity, large duplication | Plan refactoring |
| **Minor** | Style issues, small duplication, naming inconsistency | Fix opportunistically |
| **Info** | Suggestions, potential improvements | Track for later |

## Output Format

```
## Code Smell Report: [scope]

### Quick Stats
- Files scanned: N
- Largest file: [path] (N lines)
- Deepest nesting: [path:line] (N levels)
- TODO/FIXME count: N

### Findings

#### Critical (N)
- **[Smell Type]** `path/file.ts:L` — [description]
  → Suggested: [refactoring pattern]

#### Major (N)
- **[Smell Type]** `path/file.ts:L` — [description]
  → Suggested: [refactoring pattern]

#### Minor (N)
- **[Smell Type]** `path/file.ts:L` — [description]

### Hotspot Files (most smells concentrated)
1. `path/file.ts` — N findings
2. `path/file.ts` — N findings

### Recommended Next Steps
1. [Most impactful action]
2. [Second priority]
3. Run `/refactor <scope>` to execute automated refactoring
```

## Rules
- Read-only. Never modify code.
- Verify every finding with Grep before reporting — no false positives.
- If automated tools aren't available, rely on manual inspection.
- Always include file:line references for every finding.
- Sort findings by severity, then by file (group related smells together).
