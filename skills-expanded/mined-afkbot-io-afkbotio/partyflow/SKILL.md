---
name: partyflow
description: "PartyFlow bot operations through `app.run`. Use when sending messages to PartyFlow, polling bot events, checking bot identity, or joining a PartyFlow conversation with stored credentials."
aliases:
  - partyflow-send
  - partyflow-bot
triggers:
  - partyflow
  - party flow
  - отправь в partyflow
  - сообщение в partyflow
  - канал partyflow
tool_names:
  - credentials.list
  - credentials.request
  - app.run
app_names:
  - partyflow
preferred_tool_order:
  - credentials.list
  - credentials.request
  - app.run
requires_env:
  - AFKBOT_CREDENTIALS_MASTER_KEYS
---
# partyflow

Use this skill for PartyFlow bot operations through unified tool `app.run`.

Tool methods:
- `app.run`
- `credentials.list`
- `credentials.request`

Supported actions (`app_name=partyflow`):
- `get_me`
- `join_conversation`
- `send_message`
- `poll_events`

Credential set (per `profile_name`):
- required: `partyflow_bot_token`

Runtime params for `app.run`:
- `app_name=partyflow`
- `action=<partyflow_action>`
- `profile_name=<credential profile>` (optional; runtime auto-picks default or the only available profile)
- `params=<action payload object>`
- use top-level key `params`

Action payload contract:
- `get_me`
  - required: none
  - optional: `base_url`, `token_credential_name`
- `join_conversation`
  - required: `conversation_id`
  - optional: `base_url`, `token_credential_name`
- `send_message`
  - required: `conversation_id`, `content`
  - optional: `thread_id`, `base_url`, `token_credential_name`
- `poll_events`
  - optional: `cursor`, `limit`, `base_url`, `token_credential_name`

Preferred example:
```json
{
  "app_name": "partyflow",
  "action": "send_message",
  "profile_name": "ops-partyflow",
  "params": {
    "conversation_id": "660e8400-e29b-41d4-a716-446655440001",
    "thread_id": "770e8400-e29b-41d4-a716-446655440002",
    "content": "Hello from AFKBOT"
  }
}
```

Workflow:
1. Resolve `profile_name`:
   - explicit user choice -> use it;
   - otherwise let runtime auto-pick a single/default profile;
   - if multiple active profiles exist without one default, call `credentials.list` with `app_name=partyflow`.
2. Check required credentials in the selected profile.
3. Missing credentials:
   - call `credentials.request` without `value` to trigger secure input recovery;
   - collect the missing bot token securely;
  - continue the original task after the credential is stored.
4. Use `get_me` to confirm bot identity when you need to verify the integration.
5. Use `send_message` for outbound delivery; it will try to join a group/team conversation automatically after a `403` if the bot is not yet a member.

Error handling:
- `credentials_missing` -> collect the missing secret securely and retry.
- `credential_binding_conflict` -> ask the user for exact `profile_name`.
- `profile_policy_violation` -> explain blocked host/policy restriction.
- `app_run_invalid` -> inspect missing/unexpected params and retry with corrected `params`.
- `partyflow_bot_not_in_conversation` -> the bot could not post; if this is a DM, PartyFlow join may not be supported.

Safety:
- Never ask for the bot token in plain chat.
- Never print secret values in the final response.
- Prefer configured credential profiles over ad-hoc secrets.
