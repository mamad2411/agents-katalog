---
name: create-cloudflare-deploy-button
description: Add a Deploy to Cloudflare button to README so others can deploy the project in one click
argument-hint: "[repo-url] [--subdir <path>] [--paid]"
related:
  - create-cloudflare
  - follow-service-cloudflare
  - deploy-to-cloudflare
  - update-docs
  - deep-review-codebase
  - report
  - ask-me
  - run-deploy

---

## Goal

Make the repo ready for the Deploy to Cloudflare button — when someone clicks it in the README, Cloudflare clones the repo into the clicker's account, auto-provisions resources (KV, D1, R2), sets up Workers Builds CI/CD, and deploys right away.

## Scope

- Workers applications only — Pages is not supported
- The repo must be public on `github.com` or `gitlab.com` only — private repos and self-hosted Git are not supported
- Covers: check prerequisites, prepare the `wrangler` config, build the button URL, insert the snippet into `README.md`
- Use /create-cloudflare-worker if needed

## Execute

### 1. Verify Button Requirements

> Goal: Confirm the repo can use the Deploy Button

1. Check the git remote with `git remote -v` — it must be `github.com` or `gitlab.com` only
2. Verify the repo is public — `gh repo view --json visibility` for GitHub
3. Check that `wrangler.toml`/`wrangler.jsonc` has `name` plus `main` or `[assets]` complete
4. If any check fails → report the blocker and stop (e.g. a private repo must be made public first)

### 2. Prepare Worker Config

> Goal: the repo has a config the button can really deploy

1. If `wrangler.toml`/`wrangler.jsonc` is missing → run `/follow-service-cloudflare` to create the config per project type (static assets, SPA, Workers API)
2. Declare all bindings in the config (`[[kv_namespaces]]`, `[[d1_databases]]`, `[[r2_buckets]]`, `[[queues]]`) — the Deploy flow auto-provisions them for the clicker
3. If there is a build step → check `package.json` has a `build` script and the output dir matches `[assets].directory`
4. If paid Workers features are used (e.g. Queues, Durable Objects) → `paid=true` is required in the next step

### 3. Build Button URL

> Goal: get a URL correct for the repo structure

1. Base form:
   ```
   https://deploy.workers.cloudflare.com/?url=<git-repo-url>
   ```
2. Take the repo URL from `git remote -v` — drop the `.git` suffix, e.g. `https://github.com/<owner>/<repo>`
3. Monorepo → point at the subdirectory via a tree path:
   ```
   https://deploy.workers.cloudflare.com/?url=https://github.com/<owner>/<repo>/tree/<branch>/<subdir>
   ```
   the subdirectory must be self-contained including dependencies — otherwise the build fails
4. For paid features → add `&paid=true` to the href and `?paid=true` to the image src

### 4. Insert Snippet Into README

> Goal: the button sits in the README where it is easy to see

1. If `README.md` exists → insert under the title or in the existing badges row; if not → run `/update-readme-md` first
2. Markdown snippet:
   ```markdown
   [![Deploy to Cloudflare](https://deploy.workers.cloudflare.com/button)](https://deploy.workers.cloudflare.com/?url=<repo-url>)
   ```
   Or HTML for layout control:
   ```html
   <a href="https://deploy.workers.cloudflare.com/?url=<repo-url>"><img src="https://deploy.workers.cloudflare.com/button" alt="Deploy to Cloudflare"/></a>
   ```
3. If the project already deploys via Workers Builds → alternative: open the Worker dashboard → click the share button and copy the generated snippet
4. Verify the URL in the snippet matches the real repo — never leave a placeholder repo in

### 5. Verify And Report

> Goal: confirm the button works

1. Open the button URL with `/open-web` or `webfetch` to check the deploy flow renders correctly (shows the repo, build config, and resources to provision)
2. Commit and push `README.md` — run `/git-commit`
3. Run `/report` with columns `No.`, `Field`, `Value` — show the repo URL, subdir, paid flag, and resources to auto-provision
4. Run `/suggest-next-action`

## Rules

### 1. Platform Constraints

- Use /deploy-to-cloudflare if needed
- The repo must be public — if private → report and stop; never change visibility yourself
- Monorepo with several Workers apps → create a separate button per subdirectory, never one shared button

### 2. URL Correctness

- `?url=` must be the real repo URL at the latest push — always verify against `git remote -v`
- The subdirectory must be self-contained — dependencies outside the subdir make the build fail
- `paid=true` must be set on both the image src and the link href

### 3. Secret Safety

- Use /README if needed
- For env vars the clicker must set themselves, list them in a README `## Environment Variables` section

- Use /follow-service-cloudflare if needed
- Use /create-cloudflare-worker if needed
- Use /update-readme-md if needed

- Use /deep-review-codebase if needed
- Use /run-deploy if needed
- Use /ask-me if needed
- Use /update-docs if needed


## Expected Outcome

- `README.md` has a Deploy to Cloudflare button with the correct URL
- The repo passes the prerequisites: public, Workers app, complete wrangler config
- The button URL really opens the deploy flow
- The report shows the repo URL and the resources to auto-provision
