---
description: "Conventions for developing camofox CLI commands"
globs: "src/cli/**"
alwaysApply: false
---

# CLI Development Conventions

## Structure
- Register commands in `src/cli/commands/*.ts` grouped by domain.
- Wire modules in `src/cli/index.ts` only.
- Keep command handlers thin: parse input, call transport, format output.

## Command Design
- Prefer `.argument()` + `.option()` signatures with explicit validation.
- Support active tab fallback for optional `[tabId]` where relevant.
- Resolve user via `resolveCommandUser` and default to CLI/global setting.
- Use `printWithOptionalFormat` or context formatter for consistent output.

## Transport and Fallback
- Use `apiRequestWithFallback` / `requestWithFallback` where legacy paths exist.
- Handle 404 fallback explicitly for compatibility branches.
- Keep fallback logic deterministic and minimal.

## Error Handling
- Route all errors to `context.handleError`.
- Throw actionable validation errors for bad CLI input.
- Avoid leaking secrets in errors or logs.

## Auth Vault Safety
- Never print decrypted passwords to stdout.
- For `--inject`, require explicit username/password refs.
- Keep password values in narrow scope and wipe best-effort buffers.

## TypeScript Practices
- Preserve strict typing for command options and action handlers.
- Avoid `any`; use narrow records/interfaces for payloads.
- Keep helpers pure when possible.

## Testing/Validation
- Verify help text and command signatures with `--help` outputs.
- Validate JSON/text/plain formatting behavior.
- Confirm auto-start behavior and `server` command exclusions in preAction logic.
