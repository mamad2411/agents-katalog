---
name: blueprint-supabase-deploy
description: "With approval, apply the migrations to the person's Supabase project and publish the screen, built for that project, on Cloudflare."
---

# Publish to Supabase and Cloudflare

This step's gates are **deploy-production** and **credential**: the user has approved publishing, and signing in to
their own Supabase and Cloudflare accounts. You never handle a password, an access token or the secret key.

1. **The Supabase project.** Ask the person, through the blueprint question tool, to create a project on the free
   plan in the Supabase dashboard (or name an existing empty one) and to run, in this folder, `yarn supabase login`
   and then `yarn supabase link --project-ref <ref>` — it asks for the database password, which only they type. If
   the free plan has no room for another project, stop and say so: a paid project is theirs to decide.
2. **The schema.** `yarn supabase db push` applies the migrations. Never `--include-seed`: the seed's accounts and
   passwords are for trying the app locally, not for production.
3. **Sign-in settings.** Add the published URL to `site_url` and `additional_redirect_urls` in
   `supabase/config.toml` once it is known (step 6), with `enable_signup` as the spec says, and apply them with
   `yarn supabase config push`.
4. **What the page gets.** `yarn supabase projects api-keys --project-ref <ref>` (never `--reveal`) gives the
   publishable key. Write `.env.production` with `VITE_SUPABASE_URL=https://<ref>.supabase.co` and
   `VITE_SUPABASE_PUBLISHABLE_KEY=<publishable key>` — both are public by design, and nothing else goes in it — and
   the same URL to `.blueprint/supabase-url`. It must be the project this folder is linked to: the check reads the
   migrations and the linter from the linked project, and refuses a URL that names another.
5. **The screen.** `yarn wrangler whoami`; if not signed in, ask the person to run `yarn wrangler login` in this
   folder. Then build for production and give this build an id:
   `yarn vite build --mode production && node -e 'console.log(require("crypto").randomUUID())' > .blueprint/build-id && cp .blueprint/build-id dist/blueprint-build.txt`,
   then `yarn wrangler deploy`.
6. Write the URL it published to (`https://…workers.dev`, or the custom domain the spec names) to
   `.blueprint/deploy-url`, then do step 3 with it and tell the person the URL.

Done when the check passes: the URL in `.blueprint/deploy-url` serves the id this deploy wrote, lets the page connect
to the Supabase in `.blueprint/supabase-url` and talks to it (and to no other), carries no secret or service_role key —
in the page and in every chunk of `dist/`, which must still hold this deploy's build (do not rebuild after deploying) —
and renders; the production database applied exactly the migrations in `supabase/migrations/`, as they read now, and
passes Supabase's security linter. (The check resets the local database to compare, so the local stack must run.)

## Always

- Read `.blueprint/spec.md` first. It is the agreed specification; do not widen it.
- When you need a decision, ask it through the blueprint question tool and stop. Do not guess.
- Never enable billing, deploy to production, delete data or handle a credential unless this step's gates say the
  user approved exactly that.
- Say you are done by stopping; the executor runs the check. Do not claim success yourself.
