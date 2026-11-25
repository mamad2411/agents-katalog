---
name: vercel-cli-with-tokens
description: Deploy and manage projects on Vercel using token-based authentication. Use when working with Vercel CLI using access tokens rather than interactive login, e.g. deploy to vercel, set up vercel, add environment variables to vercel.
license: MIT
metadata:
  version: 0.1.0
---

# Vercel CLI with Tokens

Deploy and manage projects on Vercel using the CLI with token-based
authentication, without relying on `vercel login`. The token is resolved
once, held outside the conversation and the repo, and the project/team
binding is remembered between runs.

This skill bundles its own steer runtime at `scripts/steer.py`; the
commands below invoke it with `python3` and need nothing installed
(the Vercel CLI itself excepted). Paths are relative to this skill's
directory: when your working directory is elsewhere (it usually is),
use the skill's full path
(`python3 <path-to-this-skill>/scripts/steer.py ...`).

## Before you start

1. **Ground yourself.** Run `python3 scripts/steer.py context --tools vercel,node,npm` and
   read the snapshot; it tells you the platform, git state (including
   whether a remote exists), and whether the Vercel CLI is installed.
   If the CLI is missing: `npm install -g vercel`.
2. **Apply past lessons.** Run
   `python3 scripts/steer.py learn show` and follow what it
   says; those lessons came from real previous runs.

## Step 1: Resolve the token

Never read a token value into the conversation; check by name, export by
substitution. Work through these in order:

1. **Ask steer.** `python3 scripts/steer.py secrets check VERCEL_TOKEN`
   resolves the environment, the OS keychain, and steer's own secret
   store in one command. If present, make it available to the CLI:

   ```bash
   export VERCEL_TOKEN="$(python3 scripts/steer.py secrets get VERCEL_TOKEN)"
   ```

2. **A `.env` file may hold it.** Detect variable NAMES only; do not
   print values (Vercel tokens look like `vca_...`):

   ```bash
   grep -o '^[A-Za-z_]*VERCEL[A-Za-z_]*=' .env 2>/dev/null
   export VERCEL_TOKEN="$(grep '^<VARIABLE_NAME>=' .env | cut -d= -f2-)"
   ```

   Then offer to persist it for future runs so this discovery never
   repeats: ask the user to run
   `python3 scripts/steer.py secrets set VERCEL_TOKEN`
   (hidden prompt, lands in the keychain or a 0600 file, never in the
   repo or the chat).

3. **No token anywhere: ask the user.** They can create one at
   vercel.com/account/tokens, then run
   `python3 scripts/steer.py secrets set VERCEL_TOKEN`.
   Never ask them to paste the token into the chat. Re-check with
   `secrets check`, then export as in 1.

**Important:** once `VERCEL_TOKEN` is exported, the CLI reads it
natively. **Do not pass it as a `--token` flag**; command-line arguments
leak into shell history and process listings.

```bash
# Bad: token visible in shell history and process listings
vercel deploy --token "vca_abc123"

# Good: CLI reads VERCEL_TOKEN from the environment
export VERCEL_TOKEN="$(python3 scripts/steer.py secrets get VERCEL_TOKEN)"
vercel deploy
```

## Step 2: Resolve the project and team

This binding is workspace state; remember it so future runs skip
discovery:

```bash
python3 scripts/steer.py store get vercel_binding --scope workspace
```

If unset, discover it the usual way:

```bash
printenv VERCEL_PROJECT_ID
printenv VERCEL_ORG_ID
grep -o '^[A-Za-z_]*VERCEL[A-Za-z_]*=' .env 2>/dev/null    # names only
cat .vercel/project.json 2>/dev/null || cat .vercel/repo.json 2>/dev/null
```

From a project URL like `https://vercel.com/my-team/my-project`, the
team slug is the first path segment. Once known, record it:

```bash
python3 scripts/steer.py store put vercel_binding '{"team_slug": "<team>", "project_id": "<id>", "org_id": "<org>"}' --scope workspace
```

If you have both `VERCEL_ORG_ID` and `VERCEL_PROJECT_ID`, export them
together (setting only one causes an error); the CLI then skips any
`.vercel/` directory.

## Deploying a project

Always deploy as **preview** unless the user explicitly requests
production.

### Quick deploy (project ID known, no linking needed)

```bash
vercel deploy -y --no-wait
vercel deploy --scope <team-slug> -y --no-wait      # with a team scope
vercel deploy --prod --scope <team-slug> -y --no-wait   # production, only when asked
vercel inspect <deployment-url>                     # check status
```

### Full deploy flow (no project ID: link first)

Check project state first:

```bash
git remote get-url origin 2>/dev/null
cat .vercel/project.json 2>/dev/null || cat .vercel/repo.json 2>/dev/null
```

Link (`--repo` reads the git remote and is more reliable than matching
by directory name):

```bash
vercel link --repo --scope <team-slug> -y           # with git remote (preferred)
vercel link --scope <team-slug> -y                  # without git remote
vercel link --project <project-name> --scope <team-slug> -y   # specific project
```

Then deploy:

- **With a git remote (preferred): git push deploy.** Ask the user
  before pushing; never push without explicit approval. Commit and
  push; Vercel builds automatically and non-production branches get
  preview deployments. Retrieve the URL with
  `vercel ls --format json --scope <team-slug>` (latest entry in
  `deployments`).
- **Without a git remote:** `vercel deploy --scope <team-slug> -y --no-wait`,
  then `vercel inspect <deployment-url>`.

For a repository not cloned locally: clone it, `vercel link --repo`,
then deploy as above. After any successful link or deploy, update
`vercel_binding` in the store (Step 2) so the next run starts warm.

### About `.vercel/`

`vercel link` writes `project.json` (projectId + orgId);
`vercel link --repo` writes `repo.json` (orgId, remoteName, projects
map). Neither is needed when `VERCEL_ORG_ID` + `VERCEL_PROJECT_ID` are
set. **Do NOT** run `vercel project inspect` or `vercel link` in an
unlinked directory just to detect state; they prompt interactively or
silently link as a side effect. `vercel ls` and `vercel whoami` are safe
anywhere.

## Managing environment variables

```bash
echo "value" | vercel env add VAR_NAME --scope <team-slug>              # all environments
echo "value" | vercel env add VAR_NAME production --scope <team-slug>  # one environment
vercel env ls --scope <team-slug>
vercel env pull --scope <team-slug>        # write env vars to .env.local
vercel env rm VAR_NAME --scope <team-slug> -y
```

## Working agreement

- **Never pass `VERCEL_TOKEN` as a `--token` flag.** Export it and let
  the CLI read it natively.
- **Never print a credential value into the conversation.** Check by
  name (`secrets check`, name-only greps), move by substitution.
- **Check steer and the environment for tokens before asking the user.**
- **Default to preview deployments.** Production only when explicitly
  asked.
- **Ask before pushing to git.** Never push without approval.
- **Do not modify `.vercel/` files directly.** Reading them is fine.
- **Do not curl or fetch deployed URLs to verify.** Return the link.
- **Use `--format json`** when structured output helps follow-up steps.
- **Use `-y`** on commands that would prompt, to avoid interactive
  blocking.

## Learning

This skill improves with use. As you work:

- The moment the user corrects you, or something fails and then works a
  different way, capture it:
  `python3 scripts/steer.py learn note "<one imperative rule>" --kind correction`
  Lessons are atomic rules ("Use X not Y when Z"), never secrets.
- When a lesson from `python3 scripts/steer.py learn show`
  helped, run `python3 scripts/steer.py learn confirm <id>`;
  when one was wrong, `python3 scripts/steer.py learn dispute <id>`.
- Before finishing, record the outcome:
  `python3 scripts/steer.py learn run ok` (or `failed` with
  `--note`).

If a `learnings.md` exists in this skill, read it too; those are
promoted lessons that shipped with the skill.

## References

Load these only when that branch of the work is hit:

- Deploy fails, auth errors, wrong team, CLI missing: first read
  `references/troubleshooting.md`.
- Adding or listing custom domains: first read `references/domains.md`.
- The project's Vercel plan is managed through Stripe Projects
  (upgrades, downgrades): first read `references/stripe-projects.md`.
