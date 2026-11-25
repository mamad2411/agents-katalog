---
name: looot-mcp
description: Work on the looot-mcp repo, the stdio bridge and MCP Registry entry for the hosted looot MCP server. Use when changing the bridge, server.json, the per-client install docs or llms-install.md, or when preparing a release of looot-mcp.
---

# looot-mcp

## What this repo is

A thin npm package. `bin/looot-mcp.js` starts a pinned `mcp-remote` that bridges stdio to
`https://api.looot.ai/mcp`. `server.json` registers the hosted server in the MCP Registry as
`ai.looot/looot`, remote first. The README and `llms-install.md` hold one setup per client.
The server itself is hosted by looot; nothing here implements tools.

## Build and test

```bash
npm install --ignore-scripts        # installs the pinned mcp-remote only
npm test                            # offline unit tests of the argument builder
npm run test:live                   # free public routes only, no token
npm run scan                        # leak scanner
git config core.hooksPath .githooks # pre-commit runs the scanner
```

There is no build step: the bin is plain ESM.

## Dependencies

Exact versions only. Before adding or bumping one, run
`python3 ~/.claude/skills/pin-guard/scripts/verify.py <pkg>` and record any warning in the PR.
mcp-remote 0.14.3 passed with one warning: a single maintainer.

## Release later (only after the owner says yes)

1. Remove `"private": true` from `package.json`.
2. Bump the version in `package.json`, `server.json` (both `version` fields) and `CHANGELOG.md`.
3. `npm publish` from a clean checkout, then publish `server.json` with the MCP Registry
   publisher after verifying the `looot.ai` domain for the `ai.looot` namespace.
4. Tag `vX.Y.Z`.

## Public looot surface this repo may use

- `https://api.looot.ai/mcp` and `https://api.looot.ai/.well-known/*`
- `https://api.looot.ai/llms.txt`, `/llms-full.txt`, `/openapi.json`, `/skill.md`
- `https://looot.ai/docs`, `https://looot.ai/agents/*.md`

## Never

- Copy code, text or config from the private gateway repo.
- Commit a token, key, `.env` file or any secret, even a revoked one.
- Write internal hosts (database, pooler, hosting provider dashboards) or local machine paths.
- Include customer data, workspace or organization ids, or personal emails.
- Name private repos or private branches in code or docs meant for the public.
- Run a paid tool in tests. Live tests call free public routes only.
