---
name: life-engine-setup
description: >-
  Design and safely launch a recurring personal briefing assistant. Use when connecting Claude
  Code to Telegram or Discord, a private data store, and scheduled briefing delivery.
---

# Life Engine Setup

Build a personal briefing assistant with explicit authorization boundaries. Treat habit,
schedule, and briefing data as sensitive. Pause before every external write, credential change,
deployment, or message send.

## Required inputs

Ask for these inputs, then wait:

1. Telegram or Discord.
2. Briefing cadence and timezone.
3. Information sources the assistant may read.
4. Actions it may draft and actions it may execute.
5. Whether the user already has a Supabase project or prefers another private store.
6. The delivery account or channel that should be allowlisted.

## Architecture and trust boundary

Use this flow:

```text
allowlisted channel identity
  -> backend channel handler
  -> server-side channel-to-user binding
  -> user-scoped database operations
  -> briefing draft
  -> approved delivery
```

Never trust a `user_id` supplied by an incoming message. The backend must derive the user from the
verified Telegram or Discord identity, reject missing or disabled bindings, and scope every query
to that resolved user. A Supabase service key bypasses row-level security; keep it backend-only and
pair every use with these application-level authorization checks. Browser, desktop, prompt, log,
and chat contexts must never receive it.

## Setup workflow

### 1. Create the channel bot

- Guide the user through the official Telegram BotFather or Discord Developer Portal flow.
- Request only the permissions needed to receive commands and deliver briefings.
- Store the bot token in the channel adapter's supported secret store or environment configuration.
- Never print, paste into a prompt, write into this repository, or commit a token.
- If a token appears in terminal history, chat, or source control, stop and rotate it.
- Run Claude Code with normal permission checks. Grant only the channel and data tools required for
  this workflow; never use `--dangerously-skip-permissions`.
- Complete the platform pairing flow and restrict access to the intended account or channel.

Pause and verify a non-sensitive test message in both directions.

### 2. Create the private data model

For Supabase, have the user review and run this idempotent schema in the SQL editor. If they use a
different store, reproduce the same ownership and binding constraints there.

```sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS life_engine_channel_bindings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  provider TEXT NOT NULL CHECK (provider IN ('telegram', 'discord')),
  channel_user_id TEXT NOT NULL,
  enabled BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (provider, channel_user_id)
);

CREATE TABLE IF NOT EXISTS life_engine_habits (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  cadence TEXT NOT NULL DEFAULT 'daily',
  active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS life_engine_briefings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  period_start TIMESTAMPTZ NOT NULL,
  period_end TIMESTAMPTZ NOT NULL,
  content TEXT NOT NULL,
  delivery_status TEXT NOT NULL DEFAULT 'draft'
    CHECK (delivery_status IN ('draft', 'approved', 'sent', 'failed')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE OR REPLACE FUNCTION life_engine_set_updated_at()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS life_engine_habits_updated ON life_engine_habits;
CREATE TRIGGER life_engine_habits_updated
BEFORE UPDATE ON life_engine_habits
FOR EACH ROW EXECUTE FUNCTION life_engine_set_updated_at();

ALTER TABLE life_engine_channel_bindings ENABLE ROW LEVEL SECURITY;
ALTER TABLE life_engine_habits ENABLE ROW LEVEL SECURITY;
ALTER TABLE life_engine_briefings ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS channel_bindings_owner ON life_engine_channel_bindings;
CREATE POLICY channel_bindings_owner ON life_engine_channel_bindings
FOR SELECT TO authenticated
USING (auth.uid() = user_id);

DROP POLICY IF EXISTS habits_owner ON life_engine_habits;
CREATE POLICY habits_owner ON life_engine_habits
FOR ALL TO authenticated
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS briefings_owner ON life_engine_briefings;
CREATE POLICY briefings_owner ON life_engine_briefings
FOR ALL TO authenticated
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

REVOKE ALL ON life_engine_channel_bindings FROM anon;
REVOKE ALL ON life_engine_habits FROM anon;
REVOKE ALL ON life_engine_briefings FROM anon;
```

Explain that RLS protects authenticated user access but does not constrain `service_role`. The
backend channel handler must therefore enforce this sequence on every request:

1. Verify the provider's signed request or trusted gateway event.
2. Read the provider's immutable channel user identifier.
3. Resolve an enabled `(provider, channel_user_id)` binding server-side.
4. Reject the request if no binding exists.
5. Ignore any caller-supplied user identifier.
6. Add `WHERE user_id = <resolved user>` to every data operation.
7. Record a minimal audit event without tokens or briefing content.

Create the initial binding through an authenticated admin flow, not through a chat command.

### 3. Define the briefing contract

Draft a compact contract containing:

- timezone and schedule;
- permitted sources and freshness expectations;
- sections, maximum length, and delivery channel;
- facts that require citations or source links;
- actions that remain drafts;
- conditions that require approval, escalation, or no delivery;
- retention and deletion expectations.

Have the user approve the contract before scheduling anything.

### 4. Implement and dry-run

- Build the source reads and briefing generation as separate, testable steps.
- Use least-privilege credentials for each source.
- Mark unavailable sources explicitly rather than inventing data.
- Generate a local or private draft first; do not send it.
- Test the unauthorized-user, disabled-binding, stale-data, empty-source, and delivery-failure paths.
- Inspect logs to confirm that no tokens, personal content, or service keys are recorded.

Pause for approval of the draft and test evidence.

### 5. Schedule and operate

- Schedule the smallest reliable job supported by the chosen environment.
- Add retry limits and idempotency so one run cannot send duplicate briefings.
- Store the delivery result as `sent` only after the channel acknowledges it.
- Alert privately after repeated failures; never fall back to a public channel.
- Review permissions, bindings, retained data, and delivery quality monthly.
- Provide a documented off switch that disables the schedule and channel binding immediately.

## Completion report

Return:

1. Architecture and authorization boundary.
2. Secrets and where they are stored, naming locations but never values.
3. Approved briefing contract.
4. Test results, including rejected unauthorized access.
5. Schedule, monitoring, and off-switch instructions.
6. Remaining risks and required follow-ups.

## Provenance

Original Cloud Byte Consulting implementation based on the personal-briefing setup request captured
in the [Document Hub record](https://app.notion.com/p/760902e00f6f4db39cc0722fe7d18401).
