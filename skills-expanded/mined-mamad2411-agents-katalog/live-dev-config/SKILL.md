---
name: live-dev-config
description: Sets up GitHub repositories, links Vercel projects, and collects credentials via a secure local web form. Installs environment variables directly into Vercel and GitHub without shell leakage.
---

# live-dev-config

This skill handles code repository linking, cloud hosting setup, and secure credential collection.

`bash` blocks are POSIX (Git Bash on Windows). Any logic beyond one command/pipe lives in `resources/*.js`, never in shell control flow. If your Bash tool is cmd.exe or PowerShell, translate each snippet before running it.

## 1. Provisioning & Project Linking

Configure or verify repository and hosting resources in this order:

| Resource | Skip if | Constraints |
| --- | --- | --- |
| GitHub repo | a remote exists | `gh repo create --private --source=. --push`, from a repo with ≥1 commit. Repo name defaults to the folder name — ask the user for nothing else. Public only on request. |
| Vercel project | `.vercel/project.json` | `vercel link --yes` — non-interactive. Linking also wires the Vercel↔GitHub integration. |

## 2. Secure Credential Collection

Ensure that credentials never leak into git history, command-line logs, or shell execution paths.

### 2.1 Credential collection

Emit `.credential-fields.json` holding only what this step needs (e.g. service account JSON or specific API keys):

```json
[{ "name": "FIREBASE_SERVICE_ACCOUNT", "label": "Firebase 服務帳戶金鑰",
   "help": "Project settings → Service accounts → Generate new private key",
   "link": "https://console.firebase.google.com/project/<id>/settings/serviceaccounts/adminsdk" }]
```

```bash
node resources/credential-form.js .credential-fields.json   # launch via the TOOL's background mode, NOT a shell `&`
```

- **Credential Form:** Starts a 127.0.0.1-only form, opens the browser, writes to the gitignored `.env.local` file, and exits. Relay the URL to the user if the browser does not open automatically.
- **Manual template fallback:** If no browser can open, write `.env.local.template` as `KEY_NAME=   # description & link` for the user to fill and save to `.env.local`.
- **Command CLI Logins:** For CLI logins (`gh auth login`, `vercel login`, `firebase login`), use each tool's standard device flow.

### 2.2 Security Guidelines

Never `source`/`eval` `.env.local`, never interpolate credentials into double quotes or `<<<` (shell expansions could execute code). Extract using `read-env-value.js` and pipe to stdin:

```bash
node resources/read-env-value.js .env.local FIREBASE_SERVICE_ACCOUNT | vercel env add FIREBASE_SERVICE_ACCOUNT production
# or GitHub secrets:
node resources/read-env-value.js .env.local FIREBASE_SERVICE_ACCOUNT | gh secret set FIREBASE_SERVICE_ACCOUNT
```

Report by key name only: `✅ <KEY> set in Vercel/production` / `✅ <KEY> set in GitHub Secrets`.
