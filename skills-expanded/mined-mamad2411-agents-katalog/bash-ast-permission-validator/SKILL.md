---
name: bash-ast-permission-validator
description: Validate agent bash commands by parsing them into an AST (bash-parser) and evaluating each subcommand of a pipeline/&&/|| chain against an allowlist, instead of regex-matching strings.
category: agent-sdk
version: 1.0.0
version_origin: extracted
tags: [bash, ast, permissions, safe-mode, bash-parser]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/lukilabs/craft-agents-oss.git
source_ref: main
source_commit: 61f7d48a5b4fd0a8094f002c9e3aea5f3824dcfb
source_project: craft-agents-oss
source_path: packages/shared/src/agent/bash-validator.ts
imported_at: 2026-04-18T00:00:00Z
---

# Bash AST permission validator

## When to use
- Agent has a `Bash` tool and you want fine-grained allow/deny in "Explore" / read-only mode.
- Regex matching on the raw string keeps letting dangerous constructs through (command substitution, process substitution, redirects).
- Need to show the user WHY a compound command was blocked, pointing at the specific subcommand.

## How it works
1. Parse with `bash-parser` (npm) -> AST with nodes like `Command`, `LogicalExpression` (&&/||), `Pipeline` (|), `Subshell`, `Redirect`, `CommandExpansion` ($(...)), `ParameterExpansion` (${var}).
2. Walk the AST; classify each node:
   - `Command`: look up `name.text` in the safe-command allowlist. OK if name + flags are allowed.
   - `LogicalExpression` or compound: ALL children must be allowed.
   - `Pipeline`: block entirely in safe mode (writes to network / side effects via the pipe target).
   - `Redirect`: block anything except `<` (input redirect).
   - `CommandExpansion`, `ProcessSubstitution`, `ParameterExpansion` (with unsafe defaults): block.
   - Background `&`: block.
3. Return a `BashValidationResult` with: `allowed`, primary `reason` (typed discriminated union), and `subcommandResults[]` so the UI can highlight the offending subcommand.
4. In "compound partial fail", report both passed + failed lists so the user can trim the command and retry.

## Example
```ts
import bashParser from 'bash-parser';

function validate(cmd: string, allowlist: CompiledBashPattern[]): BashValidationResult {
  const ast = bashParser(cmd);
  const results: SubcommandResult[] = [];
  walk(ast, (node) => {
    if (node.type === 'Command') {
      const ok = allowlist.some(p => p.matches(node.name.text, node.suffix));
      results.push({ command: renderCommand(node), allowed: ok,
        reason: ok ? undefined : 'not in allowlist' });
    } else if (node.type === 'Pipeline') {
      results.push({ command: renderCommand(node), allowed: false,
        reason: 'pipelines blocked in explore mode' });
    } // etc.
  });
  const allowed = results.every(r => r.allowed);
  return allowed ? { allowed } : {
    allowed: false,
    reason: { type: 'compound_partial_fail',
      failedCommands: results.filter(r => !r.allowed).map(r => r.command),
      passedCommands: results.filter(r => r.allowed).map(r => r.command) },
    subcommandResults: results,
  };
}
```

## Gotchas
- `bash-parser` can throw on malformed input - wrap in try/catch and return `{ allowed: false, reason: { type: 'parse_error', error } }`. Don't default-allow on parse failure.
- Don't forget Windows: this validator is bash-only; for PowerShell you need a parallel `powershell-validator.ts` that shells out to the PS parser or parses with a separate grammar.
- `$(foo)` command substitution must be blocked even if `foo` alone would pass - the substituted result is used as part of another command.
- Keep subcommand rendering in sync with the AST nodes so error messages show the actual text the user typed.
