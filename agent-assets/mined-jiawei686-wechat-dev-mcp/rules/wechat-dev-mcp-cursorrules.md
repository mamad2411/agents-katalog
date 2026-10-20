# Cursor / Windsurf Rules — wechat-dev-mcp

You are working inside the `wechat-dev-mcp` project, an MCP server that drives
WeChat DevTools for **both mini-programs and mini-games**.

## Project conventions
- ESM (`"type": "module"`). Use `import`/`export`, file extensions required.
- Entry: `index.js` → `src/server.js` → `src/tools/*`.
- Never write to `stdout` except via the MCP SDK. All logs go to `stderr`.
- Tool definitions live in `src/tools/{common,program,game}.js`; registry in
  `src/tools/registry.js`. Keep handlers small and return `{ content: [...] }`
  or `{ isError: true, content: [...] }`.
- Mini-program-only tools must be guarded with `ensureProgram()` and tagged
  `modes: ["program"]` so `ListTools` auto-hides them for mini-games.
- Mini-game-only tools are tagged `modes: ["game"]`.

## Before changing behavior
1. Run `node --check` on edited files (no real WeChat DevTools in CI).
2. Keep both project types working — do not break mini-program features.
3. Document new tools in `README.md` and `docs/MINIGAME_GUIDE.md`.
