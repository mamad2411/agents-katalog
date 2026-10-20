# Agency Platform — Windsurf Rules

Windsurf should follow the same conventions as Cursor. **Single source for stack, prohibitions, RLS, and design tokens:** [.cursor/rules/](.cursor/rules/) — use `base.mdc`, `database.mdc`, `rls.mdc`, `frontend.mdc`, and `tokens.mdc`. When conventions change, update those files only; this file points to them.

**Windsurf-specific:** Use the same Node.js (22.x) and pnpm (10.x) versions as in [TOOLCHAIN.md](TOOLCHAIN.md).
