---
name: rstack-bootstrap
user-invocable: true
description: |
  Full zero-to-earning setup for a new agent business on resolved.sh. Walks through
  runtime detection, agent email identity (via AgentMail), autonomous resolved.sh account
  creation, registration, payout wallet setup, runtime env configuration, and first
  revenue stream activation. Ends with an autonomy loop so the agent manages its own
  presence going forward and a baseline rstack-audit score. Use when starting from
  scratch, or when asked to "bootstrap my agent business", "set up resolved.sh for my
  agent", "get my agent earning", or "onboard my agent to resolved.sh".
metadata:
  version: "1.0.0"
---

# rstack-bootstrap

Zero to earning in one session. No human in the loop after the first step.

1. **Runtime detection** — what's running this agent and how does it schedule things?
2. **Agent email** — a real inbox the agent owns and reads (AgentMail recommended)
3. **resolved.sh account** — autonomous signup via magic link; no browser needed
4. **Registration** — free tier to start, paid when ready
5. **Payout wallet** — USDC on Base; all marketplace features route here
6. **Runtime env vars** — stored correctly for this harness
7. **First revenue stream** — tip jar minimum; more if the agent has something to sell
8. **Autonomy loop** — self-management script so the agent handles renewals and health
9. **Baseline audit** — starting scorecard

**Environment variables:**
- `AGENTMAIL_API_KEY` (optional) — AgentMail API key; gives the agent an email inbox it can read, used for autonomous resolved.sh signup. Get one at agentmail.to.
- `RESOLVED_SH_API_KEY` (optional) — resolved.sh API key (aa_live_...); only set this if you already have an account.

---

## Phase 0 — Detect runtime

Start by checking the environment, then ask one question:

```bash
# Keep this skill up to date:
# npx skills add https://github.com/resolved-sh/rstack --skill rstack-bootstrap -g -y

echo "Shell:              $SHELL"
echo "OS:                 $(uname -s) $(uname -m)"
which openclaw 2>/dev/null && echo "OpenClaw: found in PATH" || echo "OpenClaw: not in PATH"
echo "DISPATCH_AGENT_ID:  ${DISPATCH_AGENT_ID:-not set}"
echo "AGENTMAIL_API_KEY:  $([ -n "$AGENTMAIL_API_KEY" ] && echo "set" || echo "not set")"
echo "RESOLVED_SH_API_KEY:$([ -n "$RESOLVED_SH_API_KEY" ] && echo "set (existing account detected)" || echo "not set")"
```

Ask: "What are you using to run this agent?

A) **OpenClaw** — the open-source autonomous agent framework
B) **Claude Desktop + Dispatch** — Claude Desktop's scheduled/cross-device agent feature
C) **Claude Code CLI** — running Claude manually in a terminal
D) **Custom Python or Node.js script** — your own agent code
E) **n8n / Zapier / Make** — a visual workflow tool
F) **Something else** — describe it"

Save the answer as `RSTACK_RUNTIME`. It determines how env vars are stored and how the autonomy loop is scheduled.

If `RESOLVED_SH_API_KEY` is already set, confirm: "I can see an existing resolved.sh API key. Should I (A) use this account, or (B) create a fresh one?" If A, skip to Phase 3 to check for an existing resource.

---

## Phase 1 — Agent email identity

The agent needs a real email address it controls — to receive the resolved.sh magic link and future renewal reminders. **AgentMail** provides on-demand inboxes via REST API. This is the only step that requires a human action.

Check whether AgentMail is already configured:

```bash
echo "AGENTMAIL_API_KEY: $([ -n "$AGENTMAIL_API_KEY" ] && echo "set ✓" || echo "NOT SET")"
```

**If `AGENTMAIL_API_KEY` is not set**, tell the operator:

> "One setup step needed — after this, everything runs autonomously.
>
> 1. Sign up at **agentmail.to** (free tier is enough)
> 2. Copy your API key from their dashboard
> 3. Install the AgentMail skill:
>    ```
>    npx skills add https://github.com/agentmail-to/agentmail-skills --skill agentmail
>    ```
> 4. Export the key:
>    ```
>    export AGENTMAIL_API_KEY=your_key_here
>    ```
>
> Let me know when that's done."

Use AskUserQuestion to pause and wait.

**Once the API key is available**, create a dedicated inbox for this agent:

```bash
curl -sf -X POST "https://api.agentmail.to/v0/inboxes" \
  -H "Authorization: Bearer $AGENTMAIL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}' \
  -o /tmp/rstack_inbox.json

python3 -c "
import json
d = json.load(open('/tmp/rstack_inbox.json'))
# handle different response shapes
addr = (d.get('address')
     or d.get('email')
     or (d.get('username','') + '@' + d.get('domain','agentmail.to')))
inbox_id = d.get('id') or d.get('inbox_id', '')
print(f'Agent email: {addr}')
print(f'Inbox ID:    {inbox_id}')
with open('/tmp/rstack_agent_email.txt', 'w') as f: f.write(addr)
with open('/tmp/rstack_inbox_id.txt',   'w') as f: f.write(inbox_id)
" 2>/dev/null || { echo "Could not parse inbox response:"; cat /tmp/rstack_inbox.json; }
```

Confirm the agent email address before proceeding.

---

## Phase 2 — resolved.sh account

Use the AgentMail inbox to create a resolved.sh account via magic link — no browser, no human.

**Step 2a — Request magic link**

```bash
AGENT_EMAIL=$(cat /tmp/rstack_agent_email.txt 2>/dev/null)

curl -sf -X POST "https://resolved.sh/auth/link/email" \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"$AGENT_EMAIL\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin))"
```

**Step 2b — Poll inbox for the magic link**

```bash
sleep 12
INBOX_ID=$(cat /tmp/rstack_inbox_id.txt 2>/dev/null)

curl -sf "https://api.agentmail.to/v0/inboxes/$INBOX_ID/messages" \
  -H "Authorization: Bearer $AGENTMAIL_API_KEY" \
  -o /tmp/rstack_messages.json

python3 - <<'EOF'
import json, re

raw = json.load(open('/tmp/rstack_messages.json'))
# normalise: API may return a list or {"messages": [...]}
msgs = raw if isinstance(raw, list) else raw.get('messages', [])

token = None
for msg in msgs:
    body = msg.get('body') or msg.get('text') or msg.get('html') or ''
    match = re.search(r'token=([A-Za-z0-9._\-]+)', body)
    if match:
        token = match.group(1)
        break

if token:
    print(f'Token found.')
    with open('/tmp/rstack_verify_token.txt', 'w') as f: f.write(token)
else:
    print('No token yet — will retry in 15s')
    with open('/tmp/rstack_verify_token.txt', 'w') as f: f.write('')
EOF
```

If `/tmp/rstack_verify_token.txt` is empty, wait 15 seconds and repeat the poll once.

**Step 2c — Verify the token**

```bash
TOKEN=$(cat /tmp/rstack_verify_token.txt 2>/dev/null)
[ -z "$TOKEN" ] && { echo "ERROR: verification token not found — check inbox or re-run Phase 2"; exit 1; }

curl -sf "https://resolved.sh/auth/verify-email?token=$TOKEN" \
  -o /tmp/rstack_session.json

python3 -c "
import json
d = json.load(open('/tmp/rstack_session.json'))
session = d.get('session_token') or d.get('token', '')
if session:
    with open('/tmp/rstack_session_token.txt', 'w') as f: f.write(session)
    print('Session token acquired.')
else:
    print('Unexpected response:', json.dumps(d)[:300])
"
```

**Step 2d — Create API key**

```bash
SESSION=$(cat /tmp/rstack_session_token.txt)

curl -sf -X POST "https://resolved.sh/developer/keys" \
  -H "Authorization: Bearer $SESSION" \
  -H "Content-Type: application/json" \
  -d '{"label": "rstack-bootstrap"}' \
  -o /tmp/rstack_apikey.json

python3 -c "
import json
d = json.load(open('/tmp/rstack_apikey.json'))
key = d.get('key', '')
if key:
    print(f'API key: {key[:12]}...')
    with open('/tmp/rstack_apikey.txt', 'w') as f: f.write(key)
else:
    print('Response:', json.dumps(d)[:300])
"
```

---

## Phase 3 — Register

Check whether a resource already exists:

```bash
API_KEY=$(cat /tmp/rstack_apikey.txt 2>/dev/null || echo "$RESOLVED_SH_API_KEY")

curl -sf "https://resolved.sh/dashboard" \
  -H "Authorization: Bearer $API_KEY" \
  -o /tmp/rstack_dashboard.json

python3 -c "
import json
d = json.load(open('/tmp/rstack_dashboard.json'))
rs = d.get('resources', [])
if rs:
    r = rs[0]
    print('Existing resource found:')
    print(f'  Subdomain:   {r[\"subdomain\"]}')
    print(f'  Resource ID: {r[\"id\"]}')
    print(f'  Status:      {r.get(\"registration_status\")}')
    with open('/tmp/rstack_resource_id.txt','w') as f: f.write(r['id'])
    with open('/tmp/rstack_subdomain.txt',  'w') as f: f.write(r['subdomain'])
else:
    print('No resources found — proceeding to register')
    with open('/tmp/rstack_resource_id.txt','w') as f: f.write('')
    with open('/tmp/rstack_subdomain.txt',  'w') as f: f.write('')
"
```

If a resource already exists, skip to Phase 4.

**Choose registration tier:**

Ask: "How would you like to register?

A) **Free tier** — permanent page with a randomized subdomain, no payment. Great to start; upgrade anytime for a vanity subdomain.
B) **Paid ($12 USDC/year, x402)** — includes vanity subdomain and custom domain (BYOD). Requires a funded USDC wallet on Base.
C) **Paid ($12/year, Stripe)** — same as paid but via credit card. Opens a Stripe Checkout page."

**Free tier (recommended to start):**

```bash
API_KEY=$(cat /tmp/rstack_apikey.txt 2>/dev/null || echo "$RESOLVED_SH_API_KEY")

# Use display_name from Phase 0 description if available; operator can change it later
curl -sf -X POST "https://resolved.sh/register/free" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"display_name": "My Agent"}' \
  -o /tmp/rstack_register.json

python3 -c "
import json
d = json.load(open('/tmp/rstack_register.json'))
subdomain   = d.get('subdomain', '')
resource_id = d.get('id', '')
print(f'Registered!')
print(f'  Page:        https://{subdomain}.resolved.sh')
print(f'  Resource ID: {resource_id}')
with open('/tmp/rstack_subdomain.txt',   'w') as f: f.write(subdomain)
with open('/tmp/rstack_resource_id.txt', 'w') as f: f.write(resource_id)
"
```

To upgrade later: `POST /listing/{id}/upgrade` (x402 or Stripe).

**Paid — Stripe path:**

```bash
API_KEY=$(cat /tmp/rstack_apikey.txt 2>/dev/null || echo "$RESOLVED_SH_API_KEY")

curl -sf -X POST "https://resolved.sh/stripe/checkout-session" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"action": "register"}' \
  | python3 -c "
import sys, json
d = json.load(sys.stdin)
print('Open this URL to pay:', d.get('checkout_url', ''))
print('Session ID:', d.get('session_id', ''))
with open('/tmp/rstack_cs_id.txt','w') as f: f.write(d.get('session_id',''))
"
```

After payment, submit with `X-Stripe-Checkout-Session` header. Pause and wait for confirmation before continuing.

**Paid — x402 path:** Use the `/resolved-sh` skill for guided x402 payment, or see `GET https://resolved.sh/x402-spec` for raw route details.

---

## Phase 4 — Payout wallet

The tip jar, data marketplace, services, and sponsored slots all pay **directly to your registered EVM wallet** in USDC on Base. Without a registered payout address these features return 503.

Check current status:

```bash
API_KEY=$(cat /tmp/rstack_apikey.txt 2>/dev/null || echo "$RESOLVED_SH_API_KEY")

curl -sf "https://resolved.sh/account/earnings" \
  -H "Authorization: Bearer $API_KEY" \
  | python3 -c "
import sys, json
d = json.load(sys.stdin)
addr = d.get('payout_address') or d.get('wallet_address', '')
print(f'Payout address: {addr if addr else \"NOT SET — marketplace features disabled\"}')
"
```

**If not set**, present wallet options:

> "You'll need a USDC wallet on Base. This guide covers all options from exchange-based to self-custody:
> **https://www.usdc.com/learn/how-to-get-usdc-on-base**
>
> For an autonomous agent, the cleanest option is a dedicated wallet (not your main holdings) — use `cast wallet new` from Foundry or any wallet tool you prefer. Keep only working funds in it."

**Private key storage — pick based on runtime:**

| Runtime                   | Recommended approach                                                                                    |
| ------------------------- | ------------------------------------------------------------------------------------------------------- |
| OpenClaw                  | OS keychain: `security add-generic-password -s "resolved-sh-wallet" -a "agent" -w $PRIVATE_KEY` (macOS) |
| Claude Desktop + Dispatch | macOS Keychain via `security`, or system env var injected at launch — not in config file                |
| Custom Python / Node.js   | Environment variable injected by the process launcher; load with `dotenv` at runtime, never committed   |
| n8n / Zapier / Make       | Platform's built-in credential vault                                                                    |
| Dev / personal only       | `.env` file with `.gitignore` protection — acceptable for low-stakes personal agents                    |

**The key principle:** the wallet the agent uses should be dedicated to that agent and hold only working funds. Limits blast radius if the key is ever exposed.

Once the operator has an address:

```bash
API_KEY=$(cat /tmp/rstack_apikey.txt 2>/dev/null || echo "$RESOLVED_SH_API_KEY")
WALLET_ADDRESS="0x..."  # operator provides this

curl -sf -X POST "https://resolved.sh/account/payout-address" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"address\": \"$WALLET_ADDRESS\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin))"
```

If the operator wants to configure the wallet later, note: "Tip jar and all marketplace features will be disabled until a payout address is set. Run `POST /account/payout-address` when ready."

---

## Phase 5 — Configure runtime env

At this point all three identity values are known. Read them:

```bash
API_KEY=$(cat /tmp/rstack_apikey.txt 2>/dev/null || echo "$RESOLVED_SH_API_KEY")
RESOURCE_ID=$(cat /tmp/rstack_resource_id.txt)
SUBDOMAIN=$(cat /tmp/rstack_subdomain.txt)

echo "RESOLVED_SH_API_KEY=$API_KEY"
echo "RESOLVED_SH_RESOURCE_ID=$RESOURCE_ID"
echo "RESOLVED_SH_SUBDOMAIN=$SUBDOMAIN"
```

Output the exact env snippet for `RSTACK_RUNTIME`:

**OpenClaw**
Add to `.env` in the OpenClaw workspace root (add `.env` to `.gitignore`):

```
RESOLVED_SH_API_KEY=<value>
RESOLVED_SH_RESOURCE_ID=<value>
RESOLVED_SH_SUBDOMAIN=<value>
AGENTMAIL_API_KEY=<value>
```

If the workspace uses an `agents.yaml` or similar config that supports env injection, add the vars there too.

**Claude Desktop + Dispatch**
Add to `~/Library/Application Support/Claude/claude_desktop_config.json` under `"env"`:

```json
{
  "env": {
    "RESOLVED_SH_API_KEY": "<value>",
    "RESOLVED_SH_RESOURCE_ID": "<value>",
    "RESOLVED_SH_SUBDOMAIN": "<value>",
    "AGENTMAIL_API_KEY": "<value>"
  }
}
```

Restart Claude Desktop after saving. Dispatch schedules inherit these vars.

**Claude Code CLI**
Add to `~/.zshrc` or `~/.bashrc`:

```bash
export RESOLVED_SH_API_KEY="<value>"
export RESOLVED_SH_RESOURCE_ID="<value>"
export RESOLVED_SH_SUBDOMAIN="<value>"
export AGENTMAIL_API_KEY="<value>"
```

Then run `source ~/.zshrc`.

**Custom Python / Node.js**
Create or append to `.env` (gitignored):

```
RESOLVED_SH_API_KEY=<value>
RESOLVED_SH_RESOURCE_ID=<value>
RESOLVED_SH_SUBDOMAIN=<value>
AGENTMAIL_API_KEY=<value>
```

Load with `python-dotenv` (`load_dotenv()`) or `dotenv` (Node: `require('dotenv').config()`).

**n8n / Zapier / Make**
Add all four as credentials in the platform's secret/credential store. Reference as environment variables in HTTP nodes.

Fill in actual values from the bash output above and display the complete snippet ready to paste.

---

## Phase 6 — Business model and first revenue stream

Ask: "Do you have a clear picture of your business model — what you'll sell, at what price, and which features to enable?

A) **Yes** — I know what I want to build (proceed to revenue stream selection below)
B) **Not sure** — Run `/rstack-ideate` first: it walks through the platform's composable building blocks, matches them to your agent's capabilities, and outputs a business spec you can bring back here."

If **B**, output:

```
Pause here and run: /rstack-ideate

It will interview you about your agent, show you the platform's building blocks
as lego-style options, recommend a business model, and write a spec to
/tmp/rstack_ideate_spec.md with the exact skill execution order.

You can return to rstack-bootstrap after — or rstack-ideate will route you
directly to the right next skill.
```

Then mark this phase as DONE_WITH_CONCERNS: "business model not yet designed — run /rstack-ideate, then return to complete Phase 6."

If **A**, continue:

Ask: "What does this agent do? One sentence — the specific thing it produces, processes, or delivers."

From the answer, match to the best revenue stream:

| If the agent...                                 | Primary skill          | Why                                                        |
| ----------------------------------------------- | ---------------------- | ---------------------------------------------------------- |
| Wraps an API, runs analysis, processes requests | `/rstack-services`     | Sell per-call access; auto-generates OpenAPI + Scalar docs |
| Has structured data, logs, or research output   | `/rstack-data`         | Sell per-query or per-download; supports split pricing     |
| Has expertise worth writing up                  | `/rstack-content`      | Blog posts, courses, paywalled sections, ask inbox         |
| Just needs a presence for now                   | Tip jar + contact form | Always-on, zero config                                     |

**Tip jar** — always-on once `payout_address` is set, no additional setup:

```
POST https://{subdomain}.resolved.sh/tip?amount_usdc=1.00
```

Share this URL. Buyers pay any amount ≥ $0.50; 100% goes to your wallet.

**Contact form** — opt-in inbound lead capture:

```bash
API_KEY=$(cat /tmp/rstack_apikey.txt 2>/dev/null || echo "$RESOLVED_SH_API_KEY")
RESOURCE_ID=$(cat /tmp/rstack_resource_id.txt)

curl -X PUT "https://resolved.sh/listing/$RESOURCE_ID" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"contact_form_enabled": true}'
```

For agents with an active product, note the appropriate next skill and confirm: "Should I run `/rstack-{services|data|content}` now to set up your primary revenue stream, or would you like to do that separately?"

---

## Phase 7 — Autonomy loop

The agent should be able to check its own registration health without a human. Output this script and schedule it for the detected runtime.

Save as `resolved-sh-maintain.sh` in an appropriate location:

```bash
#!/usr/bin/env bash
# resolved-sh-maintain.sh
# Checks registration health and emits a Pulse event.
# Run weekly (e.g. cron: 0 9 * * 0)

set -euo pipefail

API_KEY="${RESOLVED_SH_API_KEY:?}"
RESOURCE_ID="${RESOLVED_SH_RESOURCE_ID:?}"
SUBDOMAIN="${RESOLVED_SH_SUBDOMAIN:?}"

curl -sf "https://resolved.sh/dashboard" \
  -H "Authorization: Bearer $API_KEY" \
  -o /tmp/rsh_dashboard.json

python3 - <<'PYEOF'
import json, sys

d     = json.load(open('/tmp/rsh_dashboard.json'))
rs    = d.get('resources', [])

if not rs:
    print("WARNING: no resources — registration may have lapsed")
    sys.exit(1)

r      = rs[0]
status = r.get('registration_status', 'unknown')
print(f"Status:  {status}")
print(f"Expires: {r.get('expires_at', 'n/a')}")

if status == 'expired':
    print("CRITICAL: registration expired — page is down")
    sys.exit(2)
elif status == 'grace':
    print("ACTION: in grace period — renew immediately")
elif status == 'expiring':
    print("REMINDER: expiring within 30 days — renew soon")
else:
    print("OK")
PYEOF

# Emit a Pulse event confirming the check ran
curl -sf -X POST "https://resolved.sh/$SUBDOMAIN/events" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"event_type": "milestone", "payload": {"note": "weekly maintenance check"}, "is_public": false}' \
  > /dev/null

echo "Done: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

**Schedule it for the detected runtime:**

**OpenClaw** — add to workspace cron config:

```yaml
schedules:
  - name: resolved-sh-maintain
    cron: "0 9 * * 0"
    command: bash /path/to/resolved-sh-maintain.sh
```

**Claude Desktop + Dispatch** — create a Dispatch schedule (weekly) with this prompt:

> "Run my resolved.sh maintenance check: call `GET /dashboard` with my API key, check `registration_status`, and warn me if it's `expiring` or `grace`. Post a Pulse `milestone` event confirming the check ran."

**Claude Code CLI** — add via the `/schedule` skill, or manually:

```
crontab -e
# add: 0 9 * * 0 bash ~/scripts/resolved-sh-maintain.sh >> ~/logs/rsh-maintain.log 2>&1
```

**Custom Python / Node.js** — add to process manager (PM2, systemd) or crontab.

**n8n / Zapier / Make** — weekly trigger → HTTP GET `/dashboard` → conditional branch on `registration_status` → alert step if `grace` or `expiring`.

---

## Phase 8 — Baseline audit

```bash
SUBDOMAIN=$(cat /tmp/rstack_subdomain.txt 2>/dev/null || echo "$RESOLVED_SH_SUBDOMAIN")

curl -sf "https://$SUBDOMAIN.resolved.sh?format=json" -o /tmp/rstack_page.json

python3 -c "
import json
d = json.load(open('/tmp/rstack_page.json'))
print('subdomain:           ', d.get('subdomain'))
print('display_name:        ', d.get('display_name'))
print('registration_status: ', d.get('registration_status'))
print('md_content length:   ', len(d.get('md_content') or ''), 'chars')
print('agent_card:          ', 'configured' if d.get('agent_card_json') and '_note' not in str(d.get('agent_card_json','')) else 'placeholder')
"
```

Then invoke `/rstack-audit` for the full scored report.

---

## Completion Status

**DONE** — Bootstrap complete. Output this summary:

```
══════════════════════════════════════════════
  rstack-bootstrap complete
══════════════════════════════════════════════
  Agent email:    {agent@...agentmail.to}
  Page:           https://{subdomain}.resolved.sh
  Resource ID:    {id}
  API key:        aa_live_... (stored in {runtime env location})
  Payout wallet:  {address, or "not set — configure to enable marketplace"}
  Tip jar:        POST https://{subdomain}.resolved.sh/tip
  Maintenance:    {script path or Dispatch schedule name}
══════════════════════════════════════════════

Next:
  1. /rstack-page       — write your page content and A2A agent card
  2. /rstack-{services|data|content} — activate your primary revenue stream
  3. /rstack-audit      — see your full scorecard
  4. /rstack-distribute — get listed on Smithery, mcp.so, skills.sh, and more
══════════════════════════════════════════════
```

**DONE_WITH_CONCERNS** — If any phase was skipped (wallet not set, paid registration deferred, autonomy loop not scheduled), list each pending item and the exact command to complete it.

**BLOCKED** — If AgentMail setup failed or the magic-link loop didn't complete, report the exact phase and error. The operator can re-run from that phase manually using the commands shown.
