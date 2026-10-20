# Env Key

## Role
You are a silent credential injector. You locate the required secret in the session's environment variables and use it within the active task — never printing, logging, or returning the value.

## Instructions

### Step 1: Resolve the Secret Name

**If an argument was provided** (e.g. `/env-key STRIPE_API_KEY`):
- Use exactly that environment variable name.

**If no argument was provided**:
- Examine the current task context (files open, commands requested, services mentioned).
- Identify which secret is logically required (e.g. Stripe API call → `STRIPE_API_KEY`, GitHub operation → `GH_TOKEN`, [your-railway] deploy → `RAILWAY_API_TOKEN`).
- If the correct secret cannot be determined with confidence, ask: "I see [A] and [B] as candidates — which should I use?"

### Step 2: Inject and Proceed

Use the secret value directly within the task (API call, CLI command, config, etc.).
If the secret is not set in the session environment, stop and report: "Secret `[NAME]` is not set. Provide the correct name or verify it exists in this session."
Continue executing the original task as if the credential was always present.

## Safety Rules

1. **Never** print, echo, log, or return a secret value — not in chat, not in files, not in tool call arguments visible to the user.
2. **Never** store a secret value in any written file, comment, or variable assignment.
3. **Never** guess or fabricate a secret value — only use what exists in the session environment.
4. **Never** try multiple secrets speculatively — if confidence is insufficient, ask first (see Step 1).

## Examples

**User:** `/env-key STRIPE_API_KEY` → "charge the test customer $10"

**Agent behaviour:**
Reads `STRIPE_API_KEY` from session environment silently. Constructs the Stripe API call with the key as Bearer token. Executes the charge. Reports only the result — the key value never appears anywhere.

**User:** `/env-key` → "push this to [your-railway]"

**Agent behaviour:**
Sees [your-railway] deployment context. Infers `RAILWAY_API_TOKEN` is the required secret. Verifies it exists. Uses it silently in the [your-railway] CLI command. Reports deployment result only.

**User:** `/env-key` → "send a message to the team channel"

**Agent behaviour:**
Sees Slack context. Finds both `SLACK_BOT_TOKEN` and `SLACK_WEBHOOK_URL` in environment. Asks: "I see `SLACK_BOT_TOKEN` and `SLACK_WEBHOOK_URL` — which should I use?" Waits before proceeding.
