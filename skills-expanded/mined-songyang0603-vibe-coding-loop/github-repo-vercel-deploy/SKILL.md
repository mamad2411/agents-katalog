---
name: github-repo-vercel-deploy
description: Deploy a buildable static, frontend-first, Next.js, SPA, or short-request Web app from a local GitHub repository to Vercel. Use to configure a Vercel project, Root Directory/framework, environment-variable names and target environments, GitHub auto-deploy, and public production URL verification, including supported monorepos. Do not use to deploy long-running Agents, Workers, Queues, persistent-state systems, private-network dependencies, or complex multi-service backends.
---

# GitHub Repo Vercel Deploy

Use this Skill to turn a buildable Web app plus GitHub remote into a Vercel project with a stable public URL and automatic redeploys from production-branch pushes. It can configure Vercel environment variables, but never reads, prints, stores, or commits secret values or credential files.

## Scope gate

Continue only when the deployed unit is a static site, SPA, Next.js app, or request-bounded Vercel Function/Route Handler. Stop and explain the boundary when the requested result needs a long-running Agent, Worker, Queue, cron-driven asynchronous process, database migration/backfill, durable task recovery, private network/VPN/allowlist, container platform, message system, or multi-service orchestration. A Vercel front end may still be one component of such a system, but this Skill does not configure the other infrastructure.

## Required Inputs

Establish these before changing anything:

- Local repository path.
- GitHub remote URL and production branch.
- App root directory inside the repository, such as `.` or `demo`.
- Framework and build command expectations, usually auto-detected for Next.js.
- Whether this is a single deployed app or a monorepo with one or more deployed apps.
- Whether the user wants a new Vercel project or to reuse an existing one.
- Whether deployment protection must be disabled for public access.
- Environment-variable manifest: name, purpose, public/server-only classification, and target environment; never request a value in chat or output one.

If any item is missing and cannot be inferred from package files or existing Vercel settings, ask before changing external state. Do not infer a scope, project, production branch, secret value, public-access policy, or deployment target from a similarly named project.

## Authorization boundary

| May do without a new confirmation | Must show the exact target and obtain explicit confirmation first |
|---|---|
| Read repository state/configuration, inspect package/workspace files, run local build/checks, run `vercel whoami`, list Vercel project or variable names, inspect a deployment, and make HTTP requests | Create or link a Vercel project, connect/disconnect GitHub, change Root Directory/framework/build settings, add/update/remove environment variables, change access protection, modify `.gitignore`/`vercel.json`, commit, push, or trigger a production deployment |

Never read a Vercel credential file, ask the user to paste a token or secret into chat, or use an embedded API-token pattern. Prefer the Vercel dashboard for settings the CLI cannot safely or clearly change.

## Core Workflow

1. Read [references/workflow.md](references/workflow.md) before running deployment commands.
2. Inspect the repo:
   - `git status --short --branch --untracked-files=all`
   - `git remote -v`
   - package/build files under the intended app root.
   - Do not copy a remote URL containing userinfo into a report, issue, audit log, or committed file.
3. Confirm only intended files will be committed. Do not commit docs, handoff files, secrets, `.env*`, or `.vercel/project.json`.
4. Classify the repository before deployment:
   - For a single app/subdirectory, inspect its package file and intended Root Directory.
   - For a monorepo, also inspect the root `package.json`, lockfile, workspace config such as `pnpm-workspace.yaml`, `turbo.json`, or `nx.json`, and determine whether each deployable app needs its own Vercel project.
5. Verify the local build using the repository's actual package-manager/workspace commands. For a pnpm/Turborepo app, first read the app package name and then prefer the root's existing filtered/package script or Turbo task over assuming that `pnpm build` works from the app directory. For Next.js, run available checks such as `pnpm build`, `pnpm lint`, or `pnpm typecheck`; do not invent scripts.
6. Authenticate Vercel:
   - Run `vercel whoami`.
   - If token/login is invalid, run `vercel login` and wait for the user to authorize the device flow.
7. After explicit confirmation, create or link the Vercel project:
   - Run interactive `vercel link` when the user must choose a scope, an existing project, or new-project settings.
   - Use `vercel link --yes` only after the user has confirmed the exact scope/project choice.
8. After explicit confirmation, connect GitHub:
   - Run `vercel git connect` from the linked directory; it discovers the configured Git remote. Use `vercel git connect <git-url>` only when auto-discovery is ambiguous and the user confirmed that exact remote.
   - Verify the connected repo and production branch through `vercel project inspect` or the Vercel dashboard.
9. After explicit confirmation, set project framework/root directory correctly:
   - Root directory must match the app folder, such as `demo`.
   - Framework must be `Next.js` for Next.js apps.
   - If CLI cannot set these fields, stop and ask the user to choose a documented Vercel dashboard or authorized API path. Never read, print, store, or ask for credential files or tokens.
10. After explicit confirmation, configure environment variables only when required:
   - Derive names and public/server-only classification from code and `.env.example`; never display values.
   - Confirm each target environment (`production`, `preview`, `development`, or a preview branch) and whether an existing value may be overwritten.
   - Add values interactively with `vercel env add <NAME> <environment>`; use `--sensitive` for secrets. Never use `--force` without a separate confirmation.
   - Do not run `vercel env pull` by default. It writes cloud values locally; use it only after the user confirms the ignored target file and local verification need.
   - Treat `NEXT_PUBLIC_*` values as browser-visible; never place a server secret behind that prefix.
   - For Next.js, verify server-only variables are not exposed through `NEXT_PUBLIC_*`, `next.config.*` `env`, or a client import path. A `NEXT_PUBLIC_*` change requires a new production build before it can affect the browser bundle.
11. Ensure `.vercel` is ignored in the committed app scope. Add `.vercel` to the relevant `.gitignore` only after confirmation.
12. After explicit confirmation, commit only required deploy-scope files and push to the confirmed production branch.
13. Inspect the deployment:
    - `vercel inspect <stable-or-deployment-url>`
    - `curl -sS -L -o /dev/null -w '%{http_code}\n' <stable-alias>`
    - `curl -sS -L -o /dev/null -w '%{http_code}\n' <stable-alias>/<important-route>`
14. Return the stable public alias, not a protected one-time deployment URL.

## Verification Standard

Before reporting success, collect:

- Vercel project name and scope/team; project ID only when already returned by normal CLI output.
- GitHub repo and production branch.
- Root directory and framework preset.
- Latest commit hash pushed to GitHub.
- Production deployment status `Ready`.
- Stable alias returning final GET HTTP 200.
- Important app route returning final GET HTTP 200.
- Notes about any verification limitation, such as missing Playwright browser binaries.

Use [scripts/vercel_github_deploy_audit.sh](scripts/vercel_github_deploy_audit.sh) after deployment to collect repeatable status evidence.

## Common Pitfalls

Read [references/troubleshooting.md](references/troubleshooting.md) when any of these happen:

- Vercel deploys the repository root instead of a subfolder.
- Vercel detects `Other` instead of `Next.js`.
- `vercel whoami` fails because login is unavailable.
- The one-time deployment URL redirects to Vercel SSO or deployment protection.
- `.vercel/project.json` is accidentally staged.
- Browser screenshot tools fail even though HTTP and Vercel status are healthy.
- `vercel logs` flags differ across CLI versions.

## Output Format

Use a concise deploy result:

```text
Deploy Result
- URL: <stable public alias>
- Vercel project: <scope/project>
- GitHub repo: <owner/repo>
- Production branch: <branch>
- Root directory: <root>
- Framework: <framework>
- Status: <Ready/other>
- Commit: <hash>
- Verified: / GET HTTP 200, <route> GET HTTP 200
```

Then state how future updates work: commit and push to the production branch to trigger a Vercel production redeploy.
