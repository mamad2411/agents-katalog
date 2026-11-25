---
name: project-setup
description: Set up a new project from this Next.js + Sanity starter step by step, from `sanity init --template` or a plain `git clone` to a running site and go-live. Checks what is already done, then walks through Node and pnpm, `pnpm install`, the Sanity project and tokens, `web/.env.local` and `studio/.env(.local)`, linking `sanity.blueprint.ts` (CORS + revalidate webhook, `pnpm blueprints:plan` / `blueprints:deploy`), the first content (Studio, or `pnpm seed` when the project has it), checking `pnpm dev` and the Studio, the optional rename and brand files, and go-live on Vercel, stopping for confirmation after each step. Use when the user asks how to set up, bootstrap or start a project from the starter, to continue a half-done setup, which env vars to set, what the Next steps screen means, or why a fresh clone doesn't run.
---

# Set up a new project, step by step

Walk the user through the steps below **in order, one at a time**:

- **Check first.** Each step starts with a check. If it shows the step is done, say so
  in one line and move on. The skill often starts on a half-set-up repo.
- **Done when.** Each step ends with a condition. Don't move on until it holds, or the
  user chooses to skip (then tell them what will break).
- **Stop between steps.** After each step, report in one or two lines what is done
  and what the next step is, and wait for the user to confirm before you start it.
- **Ask only for what you can't detect**, at the step that needs it.

The user runs the commands that need their accounts or change Sanity or hosting. In
this file a leading `!` marks such a command: give it to the user to run in their
terminal (in Claude Code, typing `! <command>` runs it in the session so the output
lands in the conversation; other agents ask the user to paste the output).

## Project layout

A pnpm monorepo with `web/` (Next.js, Studio embedded at `/admin`) and `studio/`
(standalone Studio). `<scope>` below is the npm scope from `web/package.json`'s
`name` (`<scope>/web`). Run every command from the project root (the folder with
`pnpm-workspace.yaml`). `pnpm agent:install` repairs the agent adapters,
`pnpm agent:doctor` reports versions, which env vars are set and agent integrations,
and `docs/guides/agent-tools.md` covers optional MCP servers.

## Ground rules

- **Never read, print or `cat` a `.env` file**, and never echo a token or secret back.
  Check a file exists with `test -f web/.env.local && echo yes`; check variables with
  `pnpm --filter <scope>/web envs:validate`. When the user gives you a value that is not
  a secret (project ID, dataset, domain), write it into the file without quoting it back.
- **Never ask the user to paste a token or secret into the chat.** Anything typed into
  the conversation leaves their machine and stays in the transcript. Tell them which line
  of which file to paste it into in their own editor, then confirm it with
  `envs:validate`, which never prints values. If they paste one into the chat anyway,
  write it into the file without quoting it back and suggest they rotate it at
  sanity.io/manage.
- Commands that change Sanity access, content or deployed infrastructure are the
  user's: `sanity login`, `sanity cors …`, `sanity tokens …`, `sanity dataset …`,
  `sanity deploy`, `pnpm blueprints:deploy`, `pnpm seed`. You may run
  `pnpm blueprints:plan` (read-only).

## Step 0: where are we?

Run this and report the result as a short checklist:

```bash
node -p "require('./web/package.json').name"
node -p "Boolean(require('./package.json').scripts.seed)"
node --version; pnpm --version
test -d node_modules && echo "installed: yes" || echo "installed: no"
test -f web/.env.local && echo "web/.env.local: yes" || echo "web/.env.local: no"
test -f web/.env && echo "web/.env: yes" || echo "web/.env: no"
{ test -f studio/.env || test -f studio/.env.local; } && echo "studio env: yes" || echo "studio env: no"
test -f .sanity/blueprint.config.json && echo "blueprint linked: yes" || echo "blueprint linked: no"
```

If the env files exist, also run `pnpm --filter <scope>/web envs:validate`.

**Came from `sanity init --template`?** (`web/.env.local` exists right after the
create command.) The CLI already made the project and dataset, the localhost CORS
origins, a read token (`SANITY_API_READ_TOKEN`, plus a write token when the template
asks for one), wrote `web/.env.local` and `studio/.env`, and installed the
dependencies. Mark Steps 1–2 done, fill the gaps `envs:validate` names in Step 3
(usually `SANITY_REVALIDATE_SECRET`), then go on to Step 4.

Then say which step you start at.

## Step 1: get the code and install

**Check:** `node_modules` exists and `node --version` is ≥ 22.12.

From the template (the user runs it; it is interactive):

```bash
! npm create sanity@latest -- --template <owner>/<repo>/<folder>
```

Or by hand: clone the repo and `cd` into the folder with `web/` and `studio/`.

Requirements: **Node ≥ 22.12** (`.nvmrc`) and **pnpm 12** (`corepack enable` picks the
version from `packageManager` in `package.json`). Always `pnpm`, never `npm` or `yarn`.

```bash
pnpm install
```

**Done when:** `pnpm install` finishes without errors.

## Step 2: Sanity login, project and tokens

**Check:** Step 0's `envs:validate` passes the project ID and dataset, or the user
already has a project ID. Ask: an existing project ID, or create one now? Which
dataset (usually `production`)? When the project has `pnpm seed`, a fresh dataset is
safest, because the seed replaces documents (Step 5).

```bash
! pnpm exec sanity login
```

New project: sanity.io/manage → **Create new project**, note the project ID. Create the
dataset if the wizard didn't: `! pnpm --filter <scope>/studio exec sanity dataset create production`.

Tokens: sanity.io/manage → project → **API → Tokens → Add API token**. The user creates
them and keeps them at hand for Step 3, where they paste them into `web/.env.local`
themselves. Never ask for them in the chat:

| Token | Permission | Variable | Why |
|---|---|---|---|
| Read token | **Viewer** | `SANITY_API_READ_TOKEN` | Recommended. Draft mode, the visual editor, a private dataset. Without it the site runs on a public dataset with draft mode off (`/api/draft-mode/enable` answers 500 with the reason) |
| Write token | **Editor** | `SANITY_API_WRITE_TOKEN` | Only for scripts that write content (`pnpm seed`, a skill's `--apply` step). The older name `SANITY_API_TOKEN` still works. Revoke it when no script needs it |

**Done when:** the user has the project ID, the dataset exists and the tokens they
want are created.

## Step 3: environment files

**Check:** `envs:validate` passes and lists no missing recommended variable, and the
studio env file exists.

All env files are gitignored. On a hand clone, create them from the examples:

```bash
cp web/.env.example web/.env.local
cp studio/.env.example studio/.env.local
```

After copying, write the project ID and dataset into both files yourself (they are not
secrets). Then have the user open `web/.env.local` in their own editor and:

- paste the tokens from Step 2 on the `SANITY_API_READ_TOKEN` and
  `SANITY_API_WRITE_TOKEN` lines;
- set `SANITY_REVALIDATE_SECRET` to the output of `openssl rand -hex 32`, run in their
  own terminal, not with `!` (that prints it into the chat); keep a single line of it;
- check the `SANITY_BLUEPRINT_*` lines at the end: empty both unless they already know
  the values (Step 4).

When they say it's done, run `envs:validate` to confirm the variables are set.

**`web/.env.local`** (or `web/.env`; both are read and `.env.local` wins, as in Next).
`web/src/setup/envVariables.ts` validates it: `pnpm dev` and `pnpm build` refuse to
start only without the project ID or dataset. The recommended ones
(`web/src/setup/env-recommendations.ts`) print a warning and show on the Next steps
screen. An empty value (`KEY=`) counts as unset.

| Variable | Required | Value |
|---|---|---|
| `NEXT_PUBLIC_SANITY_PROJECT_ID` | yes | The project ID from Step 2 |
| `NEXT_PUBLIC_SANITY_DATASET` | yes | The dataset from Step 2 |
| `SANITY_API_READ_TOKEN` | recommended | Viewer token |
| `SANITY_REVALIDATE_SECRET` | recommended | A random string: `openssl rand -hex 32`. The webhook signs with it, so production must have the same value. Without it a published change waits for the 30-day cache |
| `NEXT_PUBLIC_BASE_URL` | no | Unset falls back to the Vercel URL, else `http://localhost:3000` (`web/src/setup/base-url.ts`). Set it to the real domain once known. **No trailing slash** |
| `SANITY_API_WRITE_TOKEN` | scripts only | Editor token |
| `NEXT_PUBLIC_SANITY_API_VERSION` | no | Defaults to `2024-12-01` |
| `IS_INDEXABLE` | no | Unset locally. On a public deploy set `"false"` until launch, then `"true"` or unset on Vercel (`docs/guides/before-release.md` → 2.2) |
| `HTTP_BASIC_AUTH` | no | `user:password` to lock a staging deploy |
| `NEXT_PUBLIC_GTM_ID` | no | Google Tag Manager. Cookie consent needs no env: it runs offline |
| `RESEND_API_KEY`, `CONTACT_FORM_RECIPIENT_EMAIL`, `CONTACT_FORM_FROM_EMAIL` | no | Contact form. Without them the form can't send |
| `SANITY_BLUEPRINT_SITE_URL` | no | The site's origin with the protocol and no trailing slash (`https://acme.com`). Empty until there is a domain. Read only by `sanity.blueprint.ts` |
| `SANITY_BLUEPRINT_EXTRA_ORIGINS` | no | Comma-separated origins, each with the protocol (`https://www.acme.com`), or empty |

**`studio/.env.local`** (or `studio/.env`; the Sanity CLI reads both). Only the
standalone Studio (`pnpm dev:studio`, port 3333) and CLI commands run in `studio/` use
it. The Studio embedded at `/admin` reads `web/.env.local`.

| Variable | Value |
|---|---|
| `SANITY_STUDIO_PROJECT_ID` | Same project ID |
| `SANITY_STUDIO_DATASET` | Same dataset |
| `SANITY_STUDIO_API_VERSION` | `2024-12-01` unless there's a reason to change it |
| `SANITY_STUDIO_APP_URL` | `http://localhost:3000`. The Styleguide tool, the SEO preview and preview links use it |

**Both files must point at the same project and dataset.** A mismatch is the most
common silent failure: the Studio edits one project while the site reads another.

**Done when:** `pnpm --filter <scope>/web envs:validate` passes, and the user confirms
the studio file has the same project ID and dataset.

## Step 4: link the Sanity blueprint (CORS + webhook)

**Check:** `.sanity/blueprint.config.json` exists and `pnpm blueprints:plan` shows no
pending changes.

`sanity.blueprint.ts` in the project root declares the CORS origins and the revalidate
webhook. Full guide: `docs/guides/sanity-blueprints.md`.

**Before `init`, settle the two blueprint variables** in `web/.env.local`. The blueprint
reads them at `init`, `plan` and `deploy` and stops on anything that isn't a full
origin. Ask for the production domain now; not knowing it yet is fine.

- Domain known → `SANITY_BLUEPRINT_SITE_URL=https://<domain>`.
- Not known yet → `SANITY_BLUEPRINT_SITE_URL=` empty. Step 9 adds it.
- `SANITY_BLUEPRINT_EXTRA_ORIGINS` → empty, or comma-separated origins with protocol.

Write the value the user gives you, or tell them which line to set. If `init` or `plan`
fails with `[blueprint] "…" is not an origin`, one of these holds a bare host
(`acme.vercel.app`) or a placeholder: add `https://` or empty it, then rerun.

```bash
! pnpm exec sanity blueprints init . --project-id <projectId> --stack-name production
pnpm blueprints:plan        # read-only, you may run it
! pnpm blueprints:deploy
```

`init` keeps the existing `sanity.blueprint.ts` and writes the stack link to `.sanity/`
(gitignored). Each teammate links their own checkout once.

**Localhost.** The blueprint declares no localhost origin. Sanity creates
`http://localhost:3333` with every new project, and `sanity init` adds
`http://localhost:3000`, both outside the stack. On a **hand clone**, have the user add
`:3000` once (the site and `/admin` need it):
`! pnpm --filter <scope>/studio exec sanity cors add http://localhost:3000 --credentials`.
Another local port goes into `SANITY_BLUEPRINT_EXTRA_ORIGINS` (`http://localhost:3001`).
Without `SANITY_BLUEPRINT_SITE_URL` the plan creates nothing, or only the extra
origins. That is expected until go-live.

**Warn about a possible `409 Duplicate origin` before the first deploy.** An origin the
blueprint declares already exists in the project (made by hand or by an earlier setup).
Blueprints can't adopt an existing origin, and the failed deploy rolls back everything,
so nothing is half-applied. To fix it:

1. Collect every `Failed to create "cors-…"` line from the log. The deploy stops at the
   first conflict, so compare `pnpm blueprints:plan` with
   `! pnpm --filter <scope>/studio exec sanity cors list` to catch the rest at once.
2. Have the user delete each of those origins and deploy again, back to back:
   ```bash
   ! pnpm --filter <scope>/studio exec sanity cors delete <origin>
   ! pnpm blueprints:deploy
   ```
3. From then on the stack owns those origins.

Never tell them to delete `http://localhost:3000` or `:3333`: the blueprint doesn't
declare them, so they can't cause the 409. **Never have the user delete a resource the
stack owns by hand** (sanity.io/manage, `sanity cors delete`): the next
`blueprints destroy` then fails with `HTTP 404` and rolls back. Remove it from the
blueprint and deploy instead.

**Done when:** the blueprint is linked, the deploy succeeded (or the plan is empty
because there is no domain yet), and `http://localhost:3000` is a CORS origin.

## Step 5: first content

**Check:** `pnpm dev` and open `http://localhost:3000`. If the site renders, this step
is done.

Every route shows the **Next steps** screen (`web/src/ui/getting-started/`, gated by
`getSetupStatus()` in `web/src/sanity/lib/queries/setup-status.ts`) until these four
documents are published. The screen lists what is missing and which recommended env
vars are unset, and goes away by itself.

| Document | Notes |
|---|---|
| `site` (Site settings) | Singleton: site title, logo, SEO defaults |
| `page` with slug `/` | The homepage |
| `header`, `footer` | Singletons; their menus may stay empty |

**Project with `pnpm seed`** (Step 0 printed `true`). `pnpm seed` runs
`sanity dataset import` on the archive in `seed/` with `--replace`, into the dataset in
`NEXT_PUBLIC_SANITY_DATASET` (`--dataset=<name>` overrides it). It brings the full demo:
pages, posts, case studies, header, footer, Site settings and the image assets.

- It authenticates with `SANITY_API_WRITE_TOKEN` (Editor) when set, otherwise with the
  CLI login from Step 2.
- `--replace` overwrites every document whose ID is in the archive; others stay. On a
  dataset with real content, seed into a new dataset instead.
- It is the user's command: `! pnpm seed`. Assets upload too, so it takes a minute.
- Restart `pnpm dev` afterwards so the site and Studio pick up the content.

**Otherwise**, create the content in the Studio:

1. Open `http://localhost:3000/admin` and log in.
2. Publish Site settings, Header, Footer and a Page with the slug `/`. The Next steps
   screen ticks each one off.
3. Listing pages (`/blog`, `/case-studies`, any other `*-listing-page` singleton) 404
   until their singleton is published. Publish each one the site will use.
4. Add sections to the homepage from the insert menu. **Styleguide → Sections** in the
   Studio shows every section with sample data, so the user can pick.

**Done when:** `http://localhost:3000` shows the homepage, not the Next steps screen.

## Step 6: verify locally

**Check:** always run it once Steps 1–5 are done.

```bash
pnpm --filter <scope>/web ts:typegen
pnpm --filter <scope>/web manifest    # regenerates web/public/admin/static/* with your project ID
pnpm typecheck
pnpm dev                              # web on :3000, standalone Studio on :3333
```

Report each as pass or fail:

- `http://localhost:3000` renders the homepage.
- `http://localhost:3000/admin` lets the user log in and lists the documents.
- In the Studio, **Open in Visual Editor** on the homepage shows the page with overlays.
- Editing a published page and viewing it **outside** draft mode still shows the old
  version locally. That is expected: the revalidate webhook can't reach localhost, so
  the published cache only refreshes on restart. Don't debug it.

**Done when:** all four pass. Then suggest revoking the write token if no script needs
it.

## Step 7: rename the starter (optional, any time)

**Check:** the scope from Step 0 is still the starter's placeholder. Ask whether to
rename now; if yes, ask for the display name and the npm scope (kebab-case, `@acme`).

Nothing breaks without it: the site, Studio and scripts run under `<scope>`. Follow
`docs/agents/template-setup.md` (indexed from the root `AGENTS.md` → "This repo is a
TEMPLATE"): it lists every file for this starter. Then:

```bash
pnpm install          # relinks the workspace after the scope rename
pnpm typecheck
git grep -in "<old name>"   # only regenerated artifacts you haven't rebuilt yet
pnpm --filter @<project>/web manifest
```

**Done when:** `pnpm install` and `pnpm typecheck` pass and `git grep` finds the old
name only in regenerated artifacts.

## Step 8: brand and design (optional, any time)

**Check:** `BRAND.md` starts with a `brand-template` line (not filled in yet) or
describes a demo company instead of the user's.

Every skill that writes copy or builds a section reads `BRAND.md` (what the site says)
and `DESIGN.md` (how it looks):

- **`BRAND.md`:** a short interview, one question per section (who you are, audience,
  voice, messaging, product facts, what must not be invented). Write the answers into
  the sections in the user's words and delete the `brand-template` line. Leave a
  section's placeholder in place rather than invent an answer.
- **`DESIGN.md`:** with a client design (Figma, brand guide), change the tokens in
  `web/src/styles/app.css` and the matching `DESIGN.md` sections in the same change
  (`docs/agents/web-styling.md`). Without one, keep the starter's look for now.

**Done when:** the user is happy with both files, or chose to leave them for later.

## Step 9: go live (when the domain is known)

**Check:** a Vercel project exists and `pnpm blueprints:plan` with the production
values below shows no pending changes.

No Vercel project yet: import the project's repository on Vercel (the README's Deploy
with Vercel button opens that screen) with **Root Directory `web`** and the env vars from
item 1 set before the first deploy. Then tell the user to add the Vercel domain
(`https://<project>.vercel.app`) to the Sanity CORS origins: item 2, or by hand in
sanity.io/manage → API → CORS origins with **Allow credentials** on. Without it `/admin`
can't log in. A hand-made origin makes a later `blueprints:deploy` fail with
`409 Duplicate origin` until it is deleted (README → "Next steps after init", step 3).
To work locally on a project created that way, clone it and
`! vercel env pull web/.env.local`.

1. **Vercel → Project → Settings → Environment Variables**: the required and
   recommended `web/` vars, `NEXT_PUBLIC_BASE_URL` set to the domain,
   `IS_INDEXABLE="false"` until launch day, and the **same** `SANITY_REVALIDATE_SECRET`
   as in the blueprint command below.
2. **CORS + webhook for the domain**:
   ```bash
   SANITY_BLUEPRINT_SITE_URL=https://<domain> SANITY_REVALIDATE_SECRET=<prod secret> pnpm blueprints:plan
   ! SANITY_BLUEPRINT_SITE_URL=https://<domain> SANITY_REVALIDATE_SECRET=<prod secret> pnpm blueprints:deploy
   ```
   Add `www` or a preview wildcard with `SANITY_BLUEPRINT_EXTRA_ORIGINS`
   (`https://*-<team-slug>.vercel.app`, never `https://*.vercel.app`; the blueprint
   refuses it). To keep these out of every command, put `SANITY_BLUEPRINT_SITE_URL` in
   `web/.env.local`.
3. Until the dataset has content the deployed site shows the Next steps screen, and
   `/admin` can't log in until the domain is a CORS origin (step 2).
4. Before launch, work through `docs/guides/before-release.md` with the user: indexing,
   SEO title and description on every routed page, CORS, webhook, redirects, and a
   Lighthouse or PageSpeed Insights run (mobile) on the homepage and one heavy page.

**Done when:** the production URL serves the site, `/admin` logs in there, publishing a
change shows up without a redeploy, and `before-release.md` has no open item the user
hasn't accepted.

## Finish

End with a short table: each step marked done, skipped (with the reason) or open, plus
the open items in order. Then point to what usually comes next, only the ones that
apply:

- A section the site doesn't have yet → `create-section`.
- Blank tiles in the Studio insert menu, or a visual catalog of the sections in use →
  `sanity-module-catalog`.
- Images without alt text, e.g. after `pnpm seed` or a content import → `generate-alts`.
- Editors pasted full URLs to the site's own domain → `link-fix`.
- Query cost and fetch patterns before launch → `sanity-optimizations`.

If the user hit a problem this skill doesn't cover, offer to add it to this file.
