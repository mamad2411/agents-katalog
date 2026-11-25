---
name: testing-pi-control-tools
description: Test pi-control LLM tools (shell_command, browser_command) via vitest. Use when verifying tool security, execution, or guards integration.
---

# Testing Pi-Control Tools

## Approach

All pi-control tools are backend-only (no UI). Test via **vitest** by importing tool objects directly and calling their `execute()` method. No recording needed.

## Setup

```bash
cd pi-agent-control-extension
npm install
```

## Running Tests

```bash
# Run all tool tests
npx vitest run extensions/pi-control/tools/

# Run specific test file
npx vitest run extensions/pi-control/tools/shell_command.test.ts

# Watch mode
npx vitest watch extensions/pi-control/tools/shell_command.test.ts
```

## Lint & Typecheck

```bash
npm run lint   # tsc --noEmit
```

## Key Testing Patterns

### Import tools directly

```typescript
import { shellCommandTool, extractBaseCommand, isAllowedCwd, ALLOWED_COMMANDS } from "./shell_command.ts";
import { inspectToolCall } from "../guards.ts";
```

### Test execution

```typescript
const result = await shellCommandTool.execute("test-id", { command: "echo hello" });
expect(result.details.success).toBe(true);
expect(result.content[0].text).toBe("hello");
```

### Test guards integration

Guards are enforced at the platform event layer (`index.ts`), not within tools. Test via `inspectToolCall`:

```typescript
const result = inspectToolCall({ name: "control_shell_command", input: { command: "rm -rf /" } });
expect(result).not.toBeNull();
expect(result!.block).toBe(true);
```

## Security Layers to Test

1. **Allowlist** — `ALLOWED_COMMANDS` set. Test blocked commands (`rm`, `chmod`, `bash`, `sh`, `wget`) and allowed ones (`echo`, `ls`, `git`).
2. **cwd validation** — `isAllowedCwd()`. Test blocked paths (`/etc`, `/root`), allowed paths (`/tmp`, `/home`), path traversal (`../../etc`), and symlink bypasses.
3. **Output size limit** — 100KB max. Use `head -c 204800 /dev/urandom | base64` to generate large output.
4. **Audit logging** — JSONL files in `artifacts/audit/`. Parse last line to verify `blocked`, `success`, `durationMs` fields.
5. **Guards.ts** — Tests via `inspectToolCall`. Tool name `control_shell_command` contains "shell" which triggers guard checks.

## Adversarial Bypass Vectors

Always test these shell chaining patterns that the allowlist alone cannot catch:
- Semicolon: `echo safe; rm -rf /`
- Pipe: `echo payload | bash`
- Backticks: `` echo `rm -rf /` ``
- Substitution: `echo $(rm -rf /)`
- AND chain: `echo ok && rm -rf /`

The allowlist checks the **first token only**. Shell metacharacters bypass it. Guards.ts provides a second layer.

## Known Limitations

- `path.resolve()` does NOT follow symlinks — `/tmp/evil -> /etc` passes lexical cwd validation
- `Error.message` is non-enumerable on Node.js Error objects — use `Object.assign` to preserve it
- `timeout: 0` in Node.js execFile means "no timeout" — clamped to min 1ms

## CI

3 checks: Analyze (CodeQL), build (vitest + lint), CodeRabbit review.

## Devin Secrets Needed

None — all testing is local via vitest with no external dependencies.
