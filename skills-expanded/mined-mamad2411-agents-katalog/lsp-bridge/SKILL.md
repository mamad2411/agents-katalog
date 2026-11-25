---
name: lsp-bridge
description: "Universal wrapper for Language Server Protocol integration. Detects LSP MCPs (typescript-language-server-mcp, pyright-mcp, gopls-mcp, etc.). Falls back to CLI tools (mypy, tsc, go vet) if MCP unavailable. Used by dor-validator, senior-engineer-reviewer, dod-validator for type checking and references analysis."
---

# LSP Bridge

Universal LSP integration с fallback на CLI tools.

## Когда применять

- DoR validation: type check before task starts
- SE review: refactoring impact analysis
- DoD validation: verify references not broken после changes

## Detection workflow

### 1. Detect LSP MCPs

Check available MCPs by name pattern:

```bash
# Examples of LSP MCPs (community)
- typescript-language-server-mcp
- pyright-mcp
- gopls-mcp
- rust-analyzer-mcp
- jdtls-mcp (Java)
```

If MCP available для project's language - use it.

### 2. Fallback to CLI tools

Если MCP не установлен - use CLI tools:

```yaml
# From config:
cli_fallback:
  python: "mypy --json-report"
  typescript: "tsc --noEmit"
  javascript: "tsc --noEmit"  # via JSDoc
  go: "go vet ./..."
  rust: "cargo check"
  java: "javac -Xlint"
```

CLI tools: less features (нет real-time semantic analysis) но still useful для type checking.

### 3. If neither available

- Log warning "LSP integration unavailable for {language}"
- Skip LSP-based checks
- DoD criterion 12 (lsp_no_errors) marked N/A

## Operations supported

### Type checking

Check files for type errors:

**Via MCP**:
```python
mcp_client.call("typescript-language-server", "textDocument/diagnostics", {
    "textDocument": {"uri": file_uri}
})
```

**Via CLI fallback**:
```bash
mypy src/ --no-incremental --json-report /tmp/mypy.json
# Parse output для errors
```

Returns: list of type errors with file/line/severity.

### Reference analysis

For each changed function/class - find usages:

**Via MCP**:
```python
mcp_client.call("pyright", "textDocument/references", {
    "textDocument": {"uri": file_uri},
    "position": {"line": L, "character": C}
})
```

Returns: list of usages.

**Via CLI fallback** (limited):
```bash
# Manual grep - не perfect но usable
grep -rn "function_name(" --include="*.py"
```

CLI fallback не considers scope/context - may have false positives.

### Renaming impact analysis

When refactoring renames things - check if refs broken:

**Via MCP**:
- Get all references
- Check if all references updated to new name

**CLI fallback**:
- Limited - just grep based check

### Definition lookup

For "go to definition" type checks:

**Via MCP**:
```python
mcp_client.call("typescript-language-server", "textDocument/definition", {...})
```

**CLI fallback**:
- Use language-specific tools (`pyflakes`, `tsc`, `gopls definition`)

## Workflow в DoR

Before task starts (dor-validator calls):

```python
def lsp_dor_check(task, current_state):
    if not lsp_available():
        return {'status': 'skipped', 'reason': 'no LSP available'}
    
    # Quick check: are project files в healthy state?
    errors = check_project_type_errors()
    
    if errors:
        return {
            'status': 'warn',
            'reason': f'{len(errors)} pre-existing type errors',
            'details': errors[:5]  # show top 5
        }
    
    return {'status': 'pass'}
```

## Workflow в DoD

After sprint changes (dod-validator calls):

```python
def lsp_dod_check(sprint):
    if not lsp_available():
        return {'status': 'na', 'reason': 'no LSP available'}
    
    changed_files = get_changed_files_in_sprint(sprint)
    
    errors = []
    for file in changed_files:
        file_errors = check_file_type_errors(file)
        errors.extend(file_errors)
    
    if errors:
        return {
            'status': 'fail',
            'errors_count': len(errors),
            'details': errors,
            'message': f'LSP found {len(errors)} type errors in changed files'
        }
    
    # Also check references not broken
    refs_check = check_references_intact(changed_files)
    if not refs_check.passed:
        return {
            'status': 'fail',
            'message': 'LSP found broken references',
            'details': refs_check.broken_refs
        }
    
    return {'status': 'pass'}
```

## Output

`.sprints/active/lsp-check-results.md`:

```markdown
# LSP Check Results

**Engine**: {{MCP_NAME or CLI_TOOL or 'unavailable'}}
**Detected at**: {{TIMESTAMP}}

## Type errors in changed files

{{ERRORS_LIST}}

или "No type errors found."

## Broken references

{{BROKEN_REFS}}

или "All references intact."

## Status

{{PASS | FAIL | SKIP}}
```

## Performance

LSP queries:
- Simple type check: <5s typical
- Project-wide refs analysis: 10-60s
- Caching: results cached per file hash

CLI fallback:
- Often slower (full project scan)
- Cache external tool results когда possible

В permissive mode - some checks могут skip для speed.

## Limitations

### MCP detection
- Manually detect MCP names - не all LSP MCPs follow naming convention
- May miss some LSP integrations
- Falls back to CLI which is OK

### CLI fallback
- Less semantic understanding
- Reference checks via grep могут have false positives
- Type checks могут miss subtle issues vs full LSP

### Multi-language projects
- Need run multiple checks (one per language)
- Slower but works

### LSP не perfect

Even с full MCP integration:
- Type system loopholes (generics, union types) могут miss issues
- Dynamic typing (Python decorators) sometimes confuses LSP
- Generated code может быть mistakenly flagged

So LSP results: WARN/FAIL but могут be false positives. SE review applies judgment.

## Configuration

В `.sprints/config.yaml`:

```yaml
lsp:
  enabled: true
  
  # Detection settings
  fallback_to_cli: true
  
  # Per-language CLI commands
  cli_fallback:
    python: "mypy --no-incremental --json-report"
    typescript: "tsc --noEmit --pretty false"
    javascript: "tsc --allowJs --noEmit"
    go: "go vet ./..."
  
  # What to check
  checks:
    type_errors: true
    references: true
    renames: true
  
  # Strictness
  fail_on_pre_existing_errors: false  # only fail на new errors caused by sprint
```

## Integration

Used by:
- **dor-validator**: pre-task type health check
- **senior-engineer-reviewer**: refactoring impact analysis в test review section
- **dod-validator**: post-sprint type check + reference check

Output cached в `.sprints/active/lsp-check-results.md` для visibility и reuse.
