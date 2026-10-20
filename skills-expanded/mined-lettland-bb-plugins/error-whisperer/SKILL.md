---
name: error-whisperer
description: Use when facing a cryptic error, stack trace, or build failure — translates to plain English and provides a copy-paste fix.
metadata:
  added: 2026-06-27
  last_reviewed: 2026-06-27
  type: meta
  status: draft
  related: [debugging, root-cause]
  owns: error-diagnosis
---

# Error Whisperer

This skill translates errors into fixes. Use it when you have a cryptic error message,
stack trace, or build failure and need three things: what actually went wrong (plain
English), why it went wrong (root cause), and how to fix it (copy-paste solution).

Read error messages the way a doctor reads symptoms — look past the surface to the
underlying condition.

## Diagnostic process

### Step 1: Parse the error

Extract the signal from the noise:

- **Error type**: what category? (syntax, runtime, type, network, permission, dependency, config)
- **Location**: file, line, function where it originates (not where it's caught)
- **Message**: the actual error text, stripped of framework noise
- **Context**: what was happening when it occurred

### Step 2: Pattern match

- **Dependency version conflicts**: check package.json, lock files, node_modules
- **Missing environment variables**: check .env files, process.env references
- **Type mismatches**: check type definitions, interfaces, imports
- **Import/export errors**: check file paths, default vs named exports
- **Build config issues**: check tsconfig, webpack/vite config, babel
- **Permission errors**: check file permissions, API keys, auth tokens
- **Network errors**: check URLs, CORS, timeouts, rate limits

### Step 3: Read relevant files

Based on the error location and type, read the file where the error occurs, the import
chain (what imports what), config files that might affect behavior, and recent changes to
affected files (if git available).

### Step 4: Generate fix

Provide the fix in order of confidence:

1. **High confidence**: "Do exactly this" — copy-paste code change
2. **Medium confidence**: "Try this first, then this" — ordered options
3. **Low confidence**: "This needs investigation" — specific diagnostic steps

## Output format

```
## Error Translation

**What happened:** [plain English, one sentence]
**Why:** [root cause, one sentence]
**Severity:** [cosmetic | blocking | data-loss-risk]

## Fix

[Exact code change or command to run]

## Prevention

[One sentence on how to avoid this in the future — only if there's a genuine pattern]
```

## Specializations

### Stack traces

- Read bottom-up for the root cause
- Ignore framework internals — find YOUR code in the trace
- Check for "Caused by:" chains

### Build errors

- Check the FIRST error, not the last — cascading failures stem from one source
- Version mismatches are the #1 cause
- "Cannot find module" = wrong path or missing install

### TypeScript errors

- Read the FULL type error, not just the first line
- Check `strict` mode settings in tsconfig
- Generic type errors often mean the wrong type parameter, not wrong data

### Dependency conflicts

- `npm ls <package>` to find version tree
- Peer dependency warnings are often the actual cause
- Lock file conflicts = delete lock file + node_modules, reinstall

## Rules

- Always provide a concrete fix, never just "check the docs."
- If the fix requires a code change, show the EXACT change (before/after).
- If you're not sure about the fix, say so and provide diagnostic steps instead of guessing.
- Read the actual source code before prescribing — don't guess from the error message alone.
- One fix per error. Don't dump 5 possible causes — find THE cause.
