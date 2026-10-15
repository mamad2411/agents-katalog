---
name: vercel-github-actions-deploy
description: Set up GitHub Actions to deploy any Vercel project using the Git Author Override method, enabling teammates to deploy on the free Hobby plan. Use when the user asks about Vercel deployment via GitHub Actions, CI/CD for Vercel, letting teammates deploy on Vercel free plan, bypassing Vercel's Hobby plan deploy restrictions, or automating Vercel production deploys. Covers workflow setup, GitHub Secrets configuration, and package manager variants (bun, npm, pnpm).
license: MIT
metadata:
  author: itsOmSarraf
  version: "1.0"
  tags: [vercel, github-actions, ci-cd, deployment, free-plan]
---

# Vercel GitHub Actions Deploy (Git Author Override)

Deploy Vercel projects from GitHub Actions on the **free Hobby plan** — letting any teammate trigger production deploys.

## The Problem

Vercel's free plan ties deployments to the **account owner**. When a teammate pushes to `main`, Vercel checks the git commit author and rejects it. Normally requires Pro plan ($20/mo per member).

## How It Works

```
Teammate pushes to main
        ↓
GitHub Actions triggers
        ↓
Rewrites commit author to account owner (on CI runner only)
        ↓
Vercel CLI builds and deploys to production
```

- Runs on every push to `main` — by **anyone**
- Manual deploy via GitHub Actions tab (`workflow_dispatch`)
- Actual repo history stays **untouched** (rewrite only on disposable runner)
- Works on the **free Vercel plan**

## User Action Required — What You Need Before Starting

This skill generates the workflow file automatically, but **you must provide 5 values** that only you have access to. The AI assistant **cannot** obtain these for you.

### Checklist: Things You Must Do Manually

| # | Action | Where to Do It | What You Get |
|---|--------|----------------|--------------|
| 1 | **Create a Vercel deploy token** | Go to [vercel.com/account/tokens](https://vercel.com/account/tokens) → Create Token → Copy it | `VERCEL_TOKEN` |
| 2 | **Link your project to Vercel** | Run `npx vercel link` in your project root (follow prompts) | Creates `.vercel/project.json` |
| 3 | **Copy Org ID and Project ID** | Open `.vercel/project.json` → copy `orgId` and `projectId` values | `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID` |
| 4 | **Know the Vercel account owner's identity** | The email and name on the Vercel account that owns the project | `DEPLOY_EMAIL`, `DEPLOY_NAME` |
| 5 | **Add all 5 secrets to GitHub** | Go to your repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret** | Secrets stored in GitHub |

**IMPORTANT:** The AI assistant will create the workflow YAML file for you, but it **cannot** create the Vercel token, link your project, or add GitHub secrets — you must do steps 1-5 yourself.

### The 5 Required GitHub Secrets

Add each of these at: `https://github.com/<owner>/<repo>/settings/secrets/actions`

| Secret Name | Where to Get It | Example Value |
|-------------|-----------------|---------------|
| `VERCEL_TOKEN` | [vercel.com/account/tokens](https://vercel.com/account/tokens) → Create Token | `pZt7x...` (long string) |
| `VERCEL_ORG_ID` | `.vercel/project.json` → `"orgId"` field | `team_aBcDeFgHiJkLmN` |
| `VERCEL_PROJECT_ID` | `.vercel/project.json` → `"projectId"` field | `prj_xYzAbCdEfGhIjK` |
| `DEPLOY_EMAIL` | Email of the person who owns the Vercel project | `owner@example.com` |
| `DEPLOY_NAME` | Display name of the Vercel project owner | `Om Sarraf` |

### How to Get the Org ID and Project ID

```bash
# Step 1: Install Vercel CLI (if not installed)
npm install -g vercel

# Step 2: Link your project
npx vercel link
# → Follow prompts: select scope, link to existing project or create new

# Step 3: A file is created at .vercel/project.json
# It looks like this:
# {
#   "orgId": "team_aBcDeFgHiJkLmN",
#   "projectId": "prj_xYzAbCdEfGhIjK"
# }

# Step 4: Make sure .vercel is gitignored
echo ".vercel" >> .gitignore
```

## Quick Start (5 min)

Once you have all 5 secrets ready, setup takes under 5 minutes.

### Step 1: Pick your workflow

Choose based on your package manager:

- **Bun** (has `bun.lock`) → `examples/deploy-bun.yml`
- **npm** (has `package-lock.json`) → `examples/deploy-npm.yml`
- **pnpm** (has `pnpm-lock.yaml`) → `examples/deploy-pnpm.yml`

Copy the chosen file to `.github/workflows/deploy.yml` in your repo.

### Step 2: Add your 5 GitHub Secrets

**(You must do this manually — see "User Action Required" above)**

Go to `https://github.com/<owner>/<repo>/settings/secrets/actions` and add:

1. `VERCEL_TOKEN`
2. `VERCEL_ORG_ID`
3. `VERCEL_PROJECT_ID`
4. `DEPLOY_EMAIL`
5. `DEPLOY_NAME`

### Step 3: Push and deploy

```bash
git add .github/workflows/deploy.yml
git commit -m "ci: add Vercel deploy workflow"
git push origin main
```

Watch it deploy in the **Actions** tab of your GitHub repo.

## Workflow Template (Bun)

```yaml
name: Deploy to Vercel

on:
  push:
    branches: [main]
  workflow_dispatch:

env:
  VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
  VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Override git author to repo owner
        run: |
          git config user.email "${{ secrets.DEPLOY_EMAIL }}"
          git config user.name "${{ secrets.DEPLOY_NAME }}"
          git commit --amend --reset-author --no-edit

      - uses: actions/setup-node@v4
        with:
          node-version: 20

      - uses: oven-sh/setup-bun@v2

      - name: Install Vercel CLI
        run: npm install -g vercel

      - name: Pull Vercel environment
        run: vercel pull --yes --environment=production --token=${{ secrets.VERCEL_TOKEN }}

      - name: Build project
        run: vercel build --prod --token=${{ secrets.VERCEL_TOKEN }}

      - name: Deploy to Vercel
        run: vercel deploy --prebuilt --prod --token=${{ secrets.VERCEL_TOKEN }}
```

**Using npm?** Remove the Bun step.
**Using pnpm?** Replace the Bun step with `uses: pnpm/action-setup@v4`.

See `examples/` for ready-to-use workflow files for each package manager.

## Preventing Double Deploys

If the account owner pushes, both Vercel's Git integration and GitHub Actions will deploy. To avoid this:

1. Go to **Vercel Dashboard** → your project → **Settings** → **Git**
2. Set **Ignored Build Step** command to: `exit 0`
3. Click **Save**

This disables Vercel's built-in Git deploys and lets GitHub Actions handle everything.

**(This is a manual step in the Vercel dashboard — the AI assistant cannot do this for you.)**

## Preview Deploys for PRs

To deploy previews on pull requests, change the trigger and remove `--prod`:

```yaml
on:
  pull_request:
    branches: [main]

# In the build step:
- run: vercel build --token=${{ secrets.VERCEL_TOKEN }}

# In the deploy step:
- run: vercel deploy --prebuilt --token=${{ secrets.VERCEL_TOKEN }}
```

## Environment Variables

`vercel pull` fetches all env vars from your Vercel project automatically. No need to duplicate them in GitHub Secrets.

**Note:** Your project's env vars must already be configured in the Vercel dashboard. If you haven't added them yet, go to: **Vercel Dashboard** → your project → **Settings** → **Environment Variables**.

## FAQ

**Does the author override mess with my git history?**
No. The rewrite only happens inside the disposable GitHub Actions runner. Your actual repo commits are untouched.

**Does this work with monorepos?**
Yes. Make sure `vercel link` points to the correct project. See [templates/deploy-workflow-template.md](templates/deploy-workflow-template.md#monorepo-support) for multi-project setup.

**What about environment variables?**
`vercel pull` fetches all env vars from your Vercel project automatically — but they must exist in the Vercel dashboard first.

**The deploy worked but my site didn't update?**
You might have Vercel's Git integration also deploying (race condition). Set **Ignored Build Step** to `exit 0` in Vercel project settings.

**I'm getting "VERCEL_TOKEN is not set"?**
GitHub Secrets are case-sensitive. Make sure the name is exactly `VERCEL_TOKEN`, not `vercel_token` or `Vercel_Token`.

## Additional Resources

- Full step-by-step setup guide: [templates/deploy-workflow-template.md](templates/deploy-workflow-template.md)
- Ready-to-use workflow files: [examples/](examples/)
- Vercel CLI docs: https://vercel.com/docs/cli
- GitHub Actions docs: https://docs.github.com/en/actions
- Vercel tokens page: https://vercel.com/account/tokens
