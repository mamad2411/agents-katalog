---
name: blueprint-cloudflare-deploy
description: "With approval, create the D1 database, apply the migrations, and publish with wrangler deploy."
---

# Publish to Cloudflare

This step's gates are **deploy-production** and **credential**: the user has approved publishing, and signing in to
their Cloudflare account.

1. `yarn wrangler whoami`. If not signed in, ask the person, through the blueprint question tool, to run
   `yarn wrangler login` in this folder themselves and tell you when it is done. Never handle an API token.
2. Create the database once: `yarn wrangler d1 create <name>` and put the `database_id` it prints into
   `wrangler.jsonc`. Apply the migrations to it: `yarn wrangler d1 migrations apply DB --remote`. If `wrangler.jsonc`
   binds R2 buckets, create each once too (`yarn wrangler r2 bucket create <bucket_name>`): the deploy fails on a
   binding to a bucket that does not exist.
3. Secrets the app needs: ask the person to run `yarn wrangler secret put <NAME>` themselves.
4. `yarn build`, then give this build an id and ship it with the site:
   `node -e 'console.log(require("crypto").randomUUID())' > .blueprint/build-id && cp .blueprint/build-id dist/client/blueprint-build.txt`,
   then `yarn wrangler deploy`.
5. Write the URL it published to (`https://…workers.dev`, or the custom domain the spec names) to
   `.blueprint/deploy-url`, and tell the person the URL.

Done when the check passes: the URL in `.blueprint/deploy-url` serves the id this deploy wrote, answers
`/api/health`, sends a Content-Security-Policy, and its page renders text in headless Chrome.

## Always

- Read `.blueprint/spec.md` first. It is the agreed specification; do not widen it.
- When you need a decision, ask it through the blueprint question tool and stop. Do not guess.
- Never enable billing, deploy to production, delete data or handle a credential unless this step's gates say the
  user approved exactly that.
- Say you are done by stopping; the executor runs the check. Do not claim success yourself.
