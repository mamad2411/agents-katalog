---
name: grok-cpa-bootstrap
description: "Reproduce, migrate, or audit a Grok CLI stack on a new Mac: install CLIProxyAPI with Homebrew, route Grok CLI through the local OpenAI-compatible endpoint, deploy a private Cloudflare temporary-email Worker, configure grok-register for Cloudflare mail and CPA OIDC export, perform an explicitly authorized registration batch, recover rate-limited CPA exports, and verify the runtime without committing credentials. Use for new-machine setup, disaster recovery, Grok/CPA configuration drift, Cloudflare temp-mail migration, or batch-registration handoff."
---

# Grok CPA Bootstrap

Rebuild the verified local chain:

```text
Grok CLI -> CPA on 127.0.0.1:8317 -> xAI OIDC auth files
                                      ^
grok-register -> Cloudflare temp mail -+
```

Treat installation, Cloudflare deployment, account creation, and model entitlement as separate checkpoints. A populated model catalog does not prove that a model can answer requests.

## Source Repositories

Use these canonical remotes when rebuilding the stack:

- King AI shared skill and agent runtime: `https://github.com/sukbearai/king-ai.git`
- Grok registration automation: `https://github.com/AaronL725/grok-register.git`
- Cloudflare temporary-mail Worker: `https://github.com/dreamhunter2333/cloudflare_temp_email.git`
- CLIProxyAPI (CPA) upstream source: `https://github.com/router-for-me/CLIProxyAPI.git`

Install CPA through Homebrew as described below. Clone its upstream repository only when source inspection or source-based recovery is required. Before reusing an existing checkout, verify `git remote get-url origin`; record or pin commit IDs when exact reproducibility matters.

## Activate on a New Machine

Clone King AI, then expose this skill directly to Codex:

```bash
KING_AI_REPO="${KING_AI_REPO:-$HOME/workspace/github/pnpm/king-ai}"
git clone https://github.com/sukbearai/king-ai.git "$KING_AI_REPO"
install -d "${CODEX_HOME:-$HOME/.codex}/skills"
ln -s "$KING_AI_REPO/packages/skills/skills/grok-cpa-bootstrap" \
  "${CODEX_HOME:-$HOME/.codex}/skills/grok-cpa-bootstrap"
```

For every King AI agent, point `KING_AI_SHARED_SKILLS` at the directory that directly contains all shared skill folders, then restart the daemon:

```bash
export KING_AI_SHARED_SKILLS="$KING_AI_REPO/packages/skills/skills"
```

Do not point `KING_AI_SHARED_SKILLS` at the individual `grok-cpa-bootstrap` directory. The runtime discovers child directories containing `SKILL.md`.

## Operating Contract

- Target macOS with Homebrew unless the user explicitly asks for another platform.
- Inspect existing installations and configuration before mutating them. Preserve unrelated services, DNS records, shell configuration, and repositories.
- Never commit or print API keys, Cloudflare tokens, JWT secrets, mailbox credentials, passwords, SSO cookies, OAuth tokens, account result files, or complete auth JSON.
- Store the temporary-mail `JWT_SECRET` and JSON-encoded `ADMIN_PASSWORDS` as Cloudflare Worker secrets, not plaintext `[vars]`. Suppress raw Wrangler output until any legacy literal secrets have been migrated.
- Generate fresh secrets on each machine. Do not copy secrets from examples, previous sessions, logs, or this skill.
- Store sensitive local files with mode `600` and secret directories with mode `700`.
- Keep `~/.cli-proxy-api/config.yaml`, `~/.grok/config.toml`, and the managed shell environment block consistent.
- Require explicit user authorization and an exact count before creating real external accounts. Do not infer permission to register accounts from a request to install or audit the stack.
- Pause for the user if a CAPTCHA or manual identity check appears. Do not claim success from browser progress alone.
- Snapshot the public root-domain MX set before any Email Routing mutation and require it to remain unchanged afterward. Never enable, disable, or replace apex routing as a shortcut; bind only the selected mail subdomain catch-all to the temporary-email Worker.
- Treat `personal-team-blocked:spending-limit` as upstream entitlement failure, not CPA import failure.
- Do not publish, deploy unrelated Workers, purchase credits, or subscribe accounts without explicit authorization.

## Required Inputs

Obtain or discover:

- Workspace root for the Python and TypeScript checkouts.
- Cloudflare-managed root domain.
- Mail subdomain, for example `mail.example.com`.
- Worker API hostname, for example `temp-mail-api.example.com`.
- Registration count. Default to a single dry-run mailbox unless real registration is explicitly authorized.
- Grok default model. Prefer a model proven by a live CPA call; `grok-4.5` was the verified default in the source session but availability can change.
- Proxy requirements for the registration browser and CPA OIDC flow. When a proxy is required, use an explicit value and verify the route before registration.

Generate locally:

- CPA downstream API key.
- Temporary-mail `JWT_SECRET`.
- Temporary-mail administrator password.

## 1. Inspect the Machine

Run a read-only preflight:

```bash
sw_vers
uname -m
command -v brew git python3 node pnpm grok jq curl
brew services list | grep '^cliproxyapi' || true
grok --version || true
grok inspect || true
test -f ~/.cli-proxy-api/config.yaml && stat -f '%Sp %N' ~/.cli-proxy-api/config.yaml
test -f ~/.grok/config.toml && stat -f '%Sp %N' ~/.grok/config.toml
```

Check for existing `grok-register` and `cloudflare_temp_email` repositories. Do not overwrite dirty checkouts. Use `git status --short` before touching either repository.

## 2. Install CPA and Source Repositories

Install CPA:

```bash
brew install cliproxyapi
brew services stop cliproxyapi
install -d -m 700 ~/.cli-proxy-api
```

Create `~/.cli-proxy-api/config.yaml` from the installed sample or a minimal configuration. Bind to localhost, set `auth-dir` to the same private directory, and place a newly generated downstream key under `api-keys`. Back up an existing config before changing it.

```yaml
host: "127.0.0.1"
port: 8317
auth-dir: "~/.cli-proxy-api"
api-keys:
  - "GENERATE_A_FRESH_VALUE"
```

Keep the Homebrew service config linked to the private file:

```bash
mv "$(brew --prefix)/etc/cliproxyapi.conf" \
  "$(brew --prefix)/etc/cliproxyapi.conf.bak"  # only when no backup exists
ln -s ~/.cli-proxy-api/config.yaml "$(brew --prefix)/etc/cliproxyapi.conf"
chmod 600 ~/.cli-proxy-api/config.yaml
brew services start cliproxyapi
```

Clone the source repositories into explicit language directories:

```bash
git clone https://github.com/AaronL725/grok-register.git <workspace>/github/python/grok-register
git clone https://github.com/dreamhunter2333/cloudflare_temp_email.git \
  <workspace>/github/typescript/cloudflare_temp_email
```

Read each checkout's `AGENTS.md`, `CLAUDE.md`, README, and ignored-config examples before continuing. Repository schemas and CLI flags may drift.

## 3. Route Grok CLI Through CPA

Use the bundled configurator. Supply the key through an environment variable, never a command-line argument:

```bash
read -s 'CPA_API_KEY?CPA API key: '
export CPA_API_KEY
python3 <skill-dir>/scripts/configure_grok_cpa.py \
  --base-url http://127.0.0.1:8317/v1 \
  --default-model grok-4.5
unset CPA_API_KEY
```

The script updates only managed values in `~/.grok/config.toml` and a marked block in `~/.zshenv`, preserves surrounding content, and sets both files to mode `600`. Start a new login shell or restart any existing King AI daemon so it inherits `XAI_API_KEY`.

Verify without making a model call:

```bash
zsh -lc 'grok models'
```

The output must say `You are using XAI_API_KEY`, list CPA models, and mark the requested default. Existing King AI agents with an explicit `model` setting still override the Grok CLI default.

## 4. Deploy Private Cloudflare Temp Mail

Read [references/cloudflare-temp-mail.md](references/cloudflare-temp-mail.md) before changing Cloudflare. Follow its D1, Worker, custom-domain, Email Routing subdomain, and catch-all verification sequence.

Stop after API and routing verification unless the user has also authorized account creation.

## 5. Configure and Run grok-register

Read [references/registration-cpa.md](references/registration-cpa.md) before creating `config.json` or starting a browser. Keep the config ignored and mode `600`.

Create the Python environment and run the repository tests before a live batch:

```bash
cd <workspace>/github/python/grok-register
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m unittest discover -s tests -v
```

After explicit authorization of the exact count, run the CLI unbuffered and monitor it through completion:

```bash
printf 'start\n' | PYTHONUNBUFFERED=1 .venv/bin/python grok_register_ttk.py cli
```

Do not expose generated passwords, mailbox JWTs, SSO tokens, or verification codes in the final report. Set result files to mode `600` after the process exits.

## 6. Recover CPA OIDC Failures

Registration success and CPA export success are separate. Preserve registered accounts when OIDC export reports `429 slow_down`.

When a proxy is required, set `CPA_OIDC_PROXY` so the device-code request, authorization browser, and token poll use one explicit route. Do not put an authenticated proxy URL on the command line:

```bash
read -s 'CPA_OIDC_PROXY?CPA OIDC proxy: '
export CPA_OIDC_PROXY
```

Run the bundled sequential recovery tool against the saved account file:

```bash
<grok-register>/.venv/bin/python <skill-dir>/scripts/retry_cpa_auth.py \
  --repo <grok-register> \
  --accounts <grok-register>/accounts_<timestamp>.txt \
  --expected-account-count <batch-account-count>
```

When the user asks to retry CPA OIDC exactly once for one saved account, do not rerun registration and do not inherit the default three attempts. Use an account file containing exactly that one record and add both `--expected-account-count 1` and `--attempts 1`.

Unset the override after recovery:

```bash
unset CPA_OIDC_PROXY
```

The tool skips existing auth files, waits between accounts, retries only rate limits, network failures, and upstream `5xx` responses, redacts account identity and OAuth codes, and closes its reusable browser on exit. It stops the recovery run on `invalid_grant`, `access_denied`, identity mismatch, identity unavailable after the bounded consent-page wait, explicit risk-control errors, unknown failures, or exhausted transient retries. Never reduce the cooldown or rotate routes merely to bypass an upstream control.

Treat a browser `Device Authorized` page as consent progress only. Require a successful token response and a private `xai-*.json` file before counting CPA auth success. `invalid_grant: Access denied` is an xAI-side rejection of that device grant; it does not identify the exact cause or prove that the account is permanently blocked. See [references/registration-cpa.md](references/registration-cpa.md) for the stop and reporting rules.

## 7. Verify End to End

Run the safe audit first:

```bash
zsh -lc 'python3 <skill-dir>/scripts/audit_stack.py \
  --expected-total-auth-count <pre-batch-total-plus-expected-batch-auth>'
```

Only when the user wants a billable or quota-consuming inference check, add `--live`:

```bash
zsh -lc 'python3 <skill-dir>/scripts/audit_stack.py \
  --expected-total-auth-count <pre-batch-total-plus-expected-batch-auth> \
  --model grok-4.5 --live'
```

Acceptance requires:

- `cliproxyapi` is running on localhost.
- Authenticated `/v1/models` succeeds.
- Every expected `xai-*.json` is mode `600` and structurally valid.
- `grok models` uses the CPA endpoint and shows the selected default.
- A live Grok CLI request returns an end-turn response when live verification is authorized.
- Cloudflare D1 address and mail counts match the completed batch.
- Both source repositories remain free of unintended tracked changes.

If one model returns a credit error, test only a model the user explicitly wants to verify. Do not conclude that every model is unavailable from a different model's entitlement response.

## Handoff

Report:

- Installed CPA and Grok CLI versions.
- Local CPA URL and selected default model, without the API key.
- Worker name, API hostname, D1 database name, and mail domain, without Cloudflare secrets.
- Requested, registered, batch CPA-auth, total CPA-auth, and terminal-rejection counts.
- Test and audit commands run.
- Any upstream entitlement error by exact model.
- Sensitive file locations and permissions.
- Whether existing daemons must be restarted.

Do not include generated account lines, auth JSON bodies, verification codes, or historical secrets.
