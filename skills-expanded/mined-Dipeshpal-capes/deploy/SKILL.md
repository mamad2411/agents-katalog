---
description: Deploy Capes to Vercel production and smoke-test the live server without exposing secrets
disable-model-invocation: true
---

Current state:

!`git status --short`

Steps:

1. If the working tree has uncommitted changes, ask the user whether to commit first. Do not commit or push unless asked. `main` is protected: code reaches it only through a pull request (`docs/project/governance.md`), and deploys are run from a checkout of `main`.
2. Run `/run-tests`. Do not deploy on failures.
3. `vercel deploy --prod` (the project is linked in `.vercel/`; if not, run `node scripts/capes.mjs install`).
4. Smoke test against the live URL from `.capes.local.json`. Read the URL and key with a command that does not print the key, and never echo the key into the conversation:

   ```bash
   U=$(node -p "require('./.capes.local.json').url"); K=$(node -p "require('./.capes.local.json').key")
   curl -s "$U/"
   curl -s -X POST "$U/mcp" -H "Authorization: Bearer $K" -H "Content-Type: application/json" \
     -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | python -c "import sys,json; print(len(json.load(sys.stdin)['result']['tools']), 'tools')"
   ```

5. Expect `"status":"online"` and the tool count that `README.md` lists. A `401` from the URL means Deployment Protection is on; a `404` on `/mcp` usually means a `vercel.json` rewrite crept in.
6. Tell the user to fully restart Claude Desktop (and reload other clients) to refresh their tool list.

The Vercel project is `capes-mcp`. Only its automatic production domain is public; extra aliases from `vercel alias set` sit behind Deployment Protection (302). If the address changes, update every client entry (Claude Desktop uses `mcp-remote` with the URL in `args`).

If environment variables changed, remember they only apply to the next deployment.
