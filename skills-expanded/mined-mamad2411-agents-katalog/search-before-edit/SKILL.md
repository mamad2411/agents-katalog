---
name: search-before-edit
description: >
  Mandatory discipline requiring grep/search before any file modification.
  Prevents breaking existing patterns by ensuring all usages, imports, and
  dependencies are understood before edits are applied.
---

# Search Before Edit

MANDATORY: Always search/grep before modifying ANY file. This prevents breaking existing patterns and ensures changes fit the codebase.

## The Rule

Before editing ANY file, you MUST:
1. Search for existing usage patterns
2. Understand the file's context
3. Check for related code that may need updates

## Required Searches

### Before Creating New Code

DO:
- Search for similar existing implementations
- Check if the functionality already exists
- Look for established patterns in the codebase
- Find related files that might be affected

```bash
# Example: Before creating a new button component
grep -r "Button" src/components/
grep -r "btn-" src/styles/
grep -r "button" src/  # case variations
```

### Before Modifying Existing Code

DO:
- Search for all usages of what you're changing
- Find imports/exports of the modified code
- Identify dependent files
- Check for tests that might need updates

```bash
# Example: Before renaming a function
grep -r "oldFunctionName" .
grep -r "from.*module-with-function" .
grep -r "oldFunctionName" **/*.test.*
```

### Before Deleting Code

DO:
- Search for ALL references to the deleted code
- Check for dynamic imports or string references
- Verify nothing will break
- Look for documentation references

```bash
# Example: Before deleting a component
grep -r "ComponentName" .
grep -r "component-name" .  # kebab-case
grep -r "componentName" .   # camelCase
```

## Search Strategies

### Multiple Query Wording

Run multiple searches with different terms. First-pass results often miss key details.

```bash
# Don't just search once
grep -r "authentication"

# Also try variations
grep -r "auth"
grep -r "login"
grep -r "session"
grep -r "signin"
grep -r "sign-in"
```

### Semantic First, Then Specific

Start with broad, high-level queries, then narrow down:

1. **Broad:** "authentication flow"
2. **Medium:** "verifyToken"
3. **Exact:** function signature or unique string

### Check Related Files

When modifying a file, check its neighbors:
- Same directory siblings
- Import sources
- Test files (`*.test.*`, `*.spec.*`)
- Type definition files (`*.d.ts`, `types.ts`)
- Story files (`*.stories.*`)
- Documentation

### Use File Type Filters

```bash
# Only TypeScript files
grep -r "pattern" --include="*.ts" --include="*.tsx"

# Exclude node_modules and build
grep -r "pattern" --exclude-dir=node_modules --exclude-dir=dist
```

## Anti-Patterns

DON'T:
- Edit files without understanding their context
- Assume you know all usages of a function
- Skip searching because "it's a simple change"
- Rely on memory of the codebase structure
- Modify exported functions without checking importers

### Common Mistakes

```
// MISTAKE: Renaming without searching
Rename: getUserById -> fetchUserById
Result: 12 files still call getUserById, app breaks

// CORRECT: Search first
Search: grep -r "getUserById"
Found: 12 files use this function
Action: Update all 12 files, then rename
```

## Verification After Edit

After making changes, verify:
1. Run the search again - did you miss anything?
2. Check that all usages still work
3. Run relevant tests
4. Verify no TypeScript/linter errors

```bash
# Post-edit verification
grep -r "oldPattern"  # Should return nothing
npm run typecheck     # Should pass
npm run lint          # Should pass
npm run test          # Should pass
```

## Minimum Search Requirements

### Thresholds by Operation Type

**New file creation:** 2 searches minimum
- Existing similar patterns
- Similar file names

**Modifying existing file:** 3 searches minimum
- All usages of modified exports
- Import statements referencing file
- Related test files

**Deleting code:** 5 searches minimum
- All references to deleted item
- Dynamic/string references
- Test files
- Documentation
- Configuration files

**Renaming:** 4 searches minimum
- Exact name matches
- Case variations
- Partial matches
- Import paths

## Examples

### Good Pattern

```
User: "Add a logout button to the header"

Agent thinking:
1. Search for existing header: grep -r "Header" src/
2. Search for existing auth UI: grep -r "logout" . && grep -r "signOut"
3. Search for auth patterns: grep -r "useAuth" .
4. Search for button patterns: grep -r "Button" src/components/
5. Now I understand the patterns, implement the change
```

### Bad Pattern

```
User: "Add a logout button to the header"

Agent: *immediately creates new component without searching*
Result: Duplicates existing LogoutButton, uses wrong auth pattern,
        doesn't match existing button styles
```

## Integration with Other Skills

This skill works with:
- **debugging-first:** Search for error sources before fixing
- **cursor-code-style:** Search for existing style patterns
- **lovable-pitfalls:** Searching prevents "writing without reading"
