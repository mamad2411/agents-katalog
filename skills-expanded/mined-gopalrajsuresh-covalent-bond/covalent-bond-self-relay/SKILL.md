---
name: covalent-bond-self-relay
description: Deploy the user's own Covalent Bond relay to their Cloudflare account: install wrangler, walk them through the browser login, run the deploy, verify /health, and set COVALENT_RELAY_URL. Use when a user asks to set up, deploy, or host their own relay instead of using the public one.
---

# Deploy your own Covalent Bond relay

The relay is a Cloudflare Worker + one Durable Object. It is untrusted by
design (sees only routing IDs and ciphertext), so self-hosting is a
convenience/availability choice, not a security requirement. A free
Cloudflare account is enough; there are no KV namespaces and no secrets.

## Steps (agent-driven)

1. **Check prerequisites.** `node --version` must be ≥ 18. Install the
   Cloudflare CLI if missing: `npm install -g wrangler` (or use
   `npx wrangler` throughout).

2. **Authenticate (the human does this part).** Run `wrangler login`, which
   opens a browser. STOP and tell the user to sign in (or create a free
   Cloudflare account first at https://dash.cloudflare.com/sign-up). Never
   ask for, handle, or store their Cloudflare credentials or API tokens
   yourself; wait until `wrangler whoami` succeeds.

3. **Deploy.** From the repository root:

   ```bash
   cd cloudflare-worker
   wrangler deploy
   ```

   The `v1-session-do` Durable Object migration in `wrangler.toml` runs
   automatically on first deploy. The output ends with the relay URL:
   `https://covalent-bond-relay.<their-subdomain>.workers.dev`.

4. **Verify.** `curl <relay-url>/health` must return `{"status":"ok",...}`.
   (First request after deploy can take ~a minute to propagate; retry once.)

5. **Configure.** Set `COVALENT_RELAY_URL=<relay-url>` on **both** machines,
   in either place (a real environment variable wins over `.env`):
   - copy `.env.example` to `.env` in the covalent-bond folder and edit the
     value (the MCP server reads it at startup), or
   - put it in the MCP client's server config (`claude mcp add --scope user
     --env COVALENT_RELAY_URL=... covalent -- node .../bin/cli.js`, or the
     `env` block for other clients).

   Then restart the agent session so the MCP server relaunches.

## Notes

- Optional per-IP throttle: uncomment the `IP_LIMITER` binding in
  `cloudflare-worker/wrangler.toml` (per-session limits are always enforced
  inside the Durable Object regardless).
- Local testing without Cloudflare: `npm run relay:dev` (mock relay on
  `http://localhost:8787`) or `wrangler dev` for the real worker locally.
- Full relay documentation: `cloudflare-worker/README.md`.
