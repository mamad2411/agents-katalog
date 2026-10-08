# LobeHub: `paulrberg-dot-agents-biome-js`

This file documents how to use the **LobeHub Skills Marketplace** CLI for this skill. The full `SKILL.md` is installed by the CLI into this folder (or `~/.cursor/skills/` when using global installs).

## Register (once per machine; rate-limited)

```bash
npx -y @lobehub/market-cli register \
  --name "YOUR_AGENT_NAME" \
  --description "Short description of this Cursor agent." \
  --source cursor
```

## Install this skill for Cursor (project-local)

From the repository root:

```bash
npx -y @lobehub/market-cli skills install paulrberg-dot-agents-biome-js --agent cursor
```

Then open the installed directory (typically `.cursor/skills/paulrberg-dot-agents-biome-js/` or similar) and read **`SKILL.md`**.

## Search the marketplace

```bash
npx -y @lobehub/market-cli skills search --q "biome"
```

## Skill overview (from marketplace)

- Extend shared Biome configs via npm `extends` while **always** defining your own `files.includes`.
- Frontend apps may combine **base** + **UI** presets when using a shared package (e.g. Sablier devkit patterns).
- Monorepos can inherit from root with `"extends": ["//"]`.
- Use **overrides** for tests (relax strict rules) and generated/ABI files (disable format/lint/sort where needed).
- Integrate **lint-staged** (or similar) for pre-commit checks.

This repo applies the structural parts of that guidance directly in `biome.jsonc` (no shared npm `extends` unless you add one).
