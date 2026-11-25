---
name: blueprint-from-collection-import-production
description: "After the publish, move the copied records and their files into the production D1 and R2 with the import proven locally."
---

# Move the records into production

This step's gates are **deploy-production** and **credential**: the user has approved writing the copied records into
their Cloudflare account, signed in with their own `wrangler login`. If `.blueprint/source/source.json` says `records`
is `false`, there is nothing to do: stop.

1. `yarn wrangler whoami`. If not signed in, ask the person, through the blueprint question tool, to run
   `yarn wrangler login` in this folder themselves and tell you when it is done. Never handle an API token.
2. Run `yarn import-source --remote` — the same import the local step proved. Do not change it here; if it fails,
   say why and stop. The publish step already created the database, applied the migrations and created the bucket
   `wrangler.jsonc` binds.
3. Tell the person how many records went into each table, and how many files into the bucket.

Done when the check passes: the production D1, read back through wrangler, has every record with every stored field
equal to the source, and every pointed-at file is in the R2 bucket named in `.blueprint/r2-bucket` with the source's
bytes.

## Always

- Read `.blueprint/spec.md` first. It is the agreed specification; do not widen it.
- When you need a decision, ask it through the blueprint question tool and stop. Do not guess.
- Never enable billing, deploy to production, delete data or handle a credential unless this step's gates say the
  user approved exactly that.
- Say you are done by stopping; the executor runs the check. Do not claim success yourself.
