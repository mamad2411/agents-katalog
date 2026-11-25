---
name: light-cloud-deploy
description: Deploy a website, web app or API to Light Cloud and manage it afterwards (status, logs, environment variables, rollbacks, visitor passwords). Use when the user asks to build and put a site online, deploy, host or ship a project, change a live site, or check how their Light Cloud apps are doing. Works with the Light Cloud connector (remote MCP server), the local Light Cloud MCP server, or the `lc` CLI.
---

# Deploy to Light Cloud

Light Cloud hosts static sites, server-rendered apps, APIs and databases. It reads the code, picks the build, and gives back a live `*.light-cloud.io` URL. Static builds go to a CDN; everything else runs as a container that scales to zero when idle.

## Pick the tools

1. **Light Cloud connector** (this plugin's MCP server, or the Light Cloud connector on claude.ai): tools such as `get-workspace-overview`, `create-repository`, `commit-files`. It has no access to local files, so code goes into a git repository and every push deploys it.
2. **Local Light Cloud MCP server** (`npx @light-cloud/mcp-server`): tools such as `connect`, `upload-and-deploy`, `detect-local-framework`. It can deploy the folder on this machine.
3. **Neither**: the CLI, `npx @light-cloud/cli <command>` (or `lc <command>` if installed). Add `--json` to read the output and `--yes` to skip prompts.

If both servers are connected, use the local one for a folder on this machine and the connector for everything else. Don't send the user to the web console for anything these tools can do.

## 1. Start of every task

1. `whoami` (CLI: `lc whoami`): the user's workspaces. Their ids are the `organisation_id` every other tool takes. One workspace: use it. Several: ask which one, by name. Never ask the user for an id.
2. `get-workspace-overview` (connector): every folder, app (status, live URL, custom domain, repository, branch) and database, and the connected GitHub, GitLab and Bitbucket accounts. Answer from it instead of asking the user what they have.

Not signed in:
- Connector: the sign-in happens when the connector is connected. On claude.ai, connect Light Cloud from the plugin's Connectors tab; in Claude Code, run `/mcp`, pick `light-cloud` and sign in. The sign-in page creates an account if the user has none (Continue with Google or GitHub, Free plan, no card).
- Local server: ask for the user's email, call `connect`, and poll `connect-status` until it is approved. CLI: `lc login --device --email <email>`. Both print an 8-character code the user types at `console.light-cloud.com/device` on any device. A new email gets a Free account with no card and no password.

Never ask for a password.

## 2. Ask once, then deploy

Ask only what the tools can't tell you, in one message: which workspace (only if there are several) and whether the site should be public or behind a visitor password. Pass the password as `password` when creating the app.

### A site you write in the conversation

1. `get-git-connections`: is a GitHub, GitLab or Bitbucket account ready?
2. `create-repository` with the files. Private unless the user asked for a public repository.
3. `create-application` with the repository URL it returned, branch `main`, `auto_deploy_on_push: true`, `deployment_type` `static` or `container` (framework `html` for plain pages).
4. `wait-for-deployment`. It returns the live URL when the build finishes; if it comes back with status `building`, call it again.

Changes later: `commit-files` on the same repository (provider, owner, repo from the overview). The push redeploys; confirm with `wait-for-deployment`.

If step 1 finds no ready account, the tool says what the user must do (`connect-github-account`, `get-github-install-url`, or `connect-git-provider` for GitLab and Bitbucket). Give them the link in plain words, wait until they say it is done, check again, and continue where you stopped.

### A repository the user already has

`create-application` with its URL and branch (`detect-framework` reads the branch first if you need the framework), then `wait-for-deployment`.

### A folder on this machine (Claude Code)

- Local server: `detect-local-framework`, then `upload-and-deploy`, then `wait-for-deployment`.
- Connector only: if the folder is already pushed (`git remote -v` shows GitHub, GitLab or Bitbucket), use `create-application` with that repository. Otherwise tell the user the code will go into a new private repository in their account, and use `create-repository` with the source files. Leave out `node_modules`, build output, `.git`, `.env` and any file holding secrets. A folder over 1000 files or 10 MB: zip the source, `request-upload-url`, PUT the zip to its `uploadUrl` with `Content-Type: application/zip` (up to 32 MB), `complete-upload`, then `create-application-from-upload`.
- CLI: `lc init` (link or create the app), then `lc deploy`.

A server must listen on the `PORT` environment variable. Detection covers the common frameworks (Next.js, Nuxt, SvelteKit, Astro, React, Vue, Angular, Django, FastAPI, Flask, Rails, Laravel, Express, NestJS, Go, .NET, Spring Boot and more) and any project with a `Dockerfile`: https://docs.light-cloud.com/platform/frameworks

### A ready-made site

`search-templates`, offer two or three matches with their demo links, `get-template` for the one picked, ask only what its customize hints and required variables need, then `deploy-template` and `wait-for-deployment` with the `template_deploy_id` it returned.

## 3. Hand over

Give the live URL, the visitor password if one was set, and the repository link if you created one. Nothing else is needed.

## 4. If the build fails

Read why: `get-deployment` and `get-build-logs` (CLI: `lc deployment <id>`). Fix the cause in the code (missing start script, wrong port, missing dependency), commit the fix with `commit-files` (or upload again), and wait again. Don't change build settings to hide an error.

## After the deploy

| Task | Tool | CLI |
|---|---|---|
| Status of everything | `get-workspace-overview` | `lc status` |
| Runtime logs | `get-environment-logs` | `lc logs -f` |
| Environment variables | `set-environment-variables`, then `deploy-environment` | `lc env vars set KEY=value --redeploy` |
| Roll back | `rollback-deployment` | `lc rollback` |
| Visitor password | `set-password-protection` | |
| Scaling | `set-scaling` | |
| Databases | see the `light-cloud-databases` skill | `lc db create` |
| Custom domain | see the `light-cloud-domains` skill | `lc domains add <domain>` |

`set-environment-variables` merges: keys not mentioned are kept, and an empty string removes one. Running code sees changes only after a redeploy. Never write a secret into a file, a commit or a reply; if the user gives you one, put it straight into `set-environment-variables` and don't repeat it.

## Plans

Every workspace starts on Free: $1 of usage a month, unlimited static sites, 3 server apps, no card. When the $1 is used up, server apps pause until next month and static sites stay up; a free workspace is never billed. Custom domains and databases need a paid plan.

If a tool is refused by a plan limit, the error names the plan and its price. Tell the user both and get a yes before calling `choose-plan` (CLI: `lc billing upgrade <plan>`): it charges a saved card or returns a Stripe Checkout link the user opens. Then poll `payment-method-status` until the plan has switched. Card numbers never pass through the agent.

## Safety and refusals

- Before deleting anything (an app, a folder, files in a repository) or overwriting the user's work, say exactly what goes and get a clear yes.
- An error ending in `Next step: call X`: call X, then retry.
- `AGENT_ACCESS_DISABLED` or `AGENT_ACTION_BLOCKED`: the account owner switched this off under Settings → Security → Agents & CLI. Tell the user; don't retry or look for another way.
