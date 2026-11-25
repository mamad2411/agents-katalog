---
name: telegram
description: "Telegram Bot API operations via `app.run` for `telegram`. Use when sending messages, fetching bot metadata, or reading updates with stored bot credentials."
aliases:
  - telegram-send
  - tg
  - telegram-bot
triggers:
  - telegram
  - telegram bot
  - telegram message
  - telegrm
  - телеграм
  - сообщение в телеграм
  - отправь в телеграм
tool_names:
  - credentials.list
  - credentials.request
  - app.run
app_names:
  - telegram
preferred_tool_order:
  - credentials.list
  - credentials.request
  - app.run
requires_env:
  - AFKBOT_CREDENTIALS_MASTER_KEYS
---
# telegram

Use this skill for Telegram Bot API operations through unified tool `app.run`.

Tool methods:
- `app.run`
- `credentials.list`
- `credentials.request`

Supported actions (`app_name=telegram`):
- `send_message`
- `send_photo`
- `send_document`
- `get_me`
- `get_updates`
- `ban_chat_member`
- `unban_chat_member`

Action naming:
- prefer canonical snake_case action names such as `send_message`
- common Telegram Bot API camelCase aliases such as `sendMessage` are accepted, but new calls should still use canonical snake_case

Credential set (per `profile_name`):
- required: `telegram_token`
- optional: `telegram_chat_id` (not needed if `params.chat_id` is provided)

Runtime params for `app.run`:
- `app_name=telegram`
- `action=<telegram_action>`
- `profile_name=<credential profile>` (optional; runtime auto-picks default or the only available profile)
- `params=<action payload object>`
- use top-level key `params`

Action payload contract:
- `send_message`
  - required: `text`
  - optional: `chat_id`, `message_thread_id`, `parse_mode`, `disable_web_page_preview`, `token_credential_name`, `chat_id_credential_name`
  - note: `chat_id` may be omitted only if credential `telegram_chat_id` exists
  - note: `message_thread_id` is used for Telegram forum/topic delivery
- `send_photo`
  - required: `photo`
  - optional: `caption`, `chat_id`, `message_thread_id`, `parse_mode`, `token_credential_name`, `chat_id_credential_name`
  - `photo` may be one of: workspace file path, HTTP/HTTPS URL, or existing Telegram `file_id`
- `send_document`
  - required: `document`
  - optional: `caption`, `chat_id`, `message_thread_id`, `parse_mode`, `token_credential_name`, `chat_id_credential_name`
  - `document` may be one of: workspace file path or existing Telegram `file_id`
- `get_me`
  - required: none
  - optional: `token_credential_name`
- `get_updates`
  - required: none
  - optional: `limit`, `timeout`, `offset`, `token_credential_name`
- `ban_chat_member`
  - required: `user_id`
  - optional: `chat_id`, `revoke_messages`, `until_date`, `token_credential_name`, `chat_id_credential_name`
  - note: works only where the Telegram bot has permission to ban users
  - note: not a private-chat block primitive; this is group/supergroup moderation
- `unban_chat_member`
  - required: `user_id`
  - optional: `chat_id`, `only_if_banned`, `token_credential_name`, `chat_id_credential_name`

Preferred example:
```json
{
  "app_name": "telegram",
  "action": "send_message",
  "profile_name": "default",
  "params": {
    "chat_id": "-1001234567890",
    "text": "hello"
  }
}
```

Workflow:
1. Resolve credential profile:
   - if user provided profile name, use it;
   - otherwise let runtime auto-pick a single/default profile;
   - if profile choice is still ambiguous, call `credentials.list` with `app_name=telegram`.
2. Select profile deterministically:
   - exactly one active profile -> use it;
   - marked default profile -> use it;
   - multiple active profiles without one default -> ask user to choose.
3. Check required credentials via `credentials.list` with selected profile.
4. Missing credentials:
   - call `credentials.request` without `value` to trigger deterministic secure-input recovery metadata;
   - let runtime collect the secure value;
   - continue the original task after the credential is stored.
5. Execute `app.run` with target action.

Error handling:
- `credentials_missing` -> collect missing secure value and retry.
- `credential_binding_conflict` -> ask user for exact `profile_name`.
- `profile_policy_violation` -> explain blocked host/policy restriction.
- `app_run_invalid` -> inspect missing/unexpected params and retry with corrected `params`.

Safety:
- Never ask for bot token in plain chat.
- Never print token values in final response.
- Runtime routes the correct skill automatically from `app_name`.
