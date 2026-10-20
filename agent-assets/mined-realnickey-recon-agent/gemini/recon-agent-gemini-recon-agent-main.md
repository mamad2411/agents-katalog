# Antigravity Workspace Rules for Recon Agent

## Strict Isolation & Secrets Policy
1. **NEVER read, inspect, or output `.env` or `.env.*` files.**
2. **NEVER execute shell commands that print environment variables** (`printenv`, `Get-ChildItem env:`, `echo $env:...`, `set`).
3. **NEVER read or search for ground truth answer keys.** Matcher code in `src/` must operate completely blind.

## Improvement Loop Mandates
- **Easy Locks are immutable**: Dev (fitness 1.0000, hash `f7c0b963363fca70`) and Holdout (fitness 1.0000, hash `e8e4fa7bb6da52a0`) must NEVER regress.
- **Fitness Priority**: Fitness = Recall - 2 * FPR. An honest exception always beats a wrong match.
- **Anti-Reward Hacking**: Use `bun run loop-eval --blind` or `bun run loop-eval --cv` during `/goal` loops. Never memorize specific record IDs or single seeds; cross-validate across multiple seeds using `bun run cross-validate`.
- **Workflow**: Always run `bun run typecheck && bun test && bun run loop-eval` to verify changes before committing.
- **Read `AGENT.md`**: Refer to `AGENT.md` for complete architecture, formulas, and category strategies.

