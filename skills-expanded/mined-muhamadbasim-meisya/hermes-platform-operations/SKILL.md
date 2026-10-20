---
name: hermes-platform-operations
description: "Operate and troubleshoot Hermes platform automations: gateway messaging, cron jobs, Telegram bot identity, WhatsApp ingest, and recurring community digests."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [hermes, gateway, cron, messaging, telegram, whatsapp, troubleshooting, automation]
    related_skills: [hermes-agent]
    created_by: agent
---

# Hermes Platform Operations

Use this umbrella skill when the user asks to run, repair, audit, or improve Hermes platform-facing automations: scheduled cron jobs, messaging gateway/platform adapters, Telegram bot profile/identity tasks, WhatsApp read-only group ingest, or WhatsApp/community summary jobs.

Load `hermes-agent` alongside this skill when canonical Hermes CLI/config commands are needed.

## Operating principles

- **Inspect before changing.** Read the relevant job/config/log/runtime state before editing config, restarting gateway, changing cron jobs, or uploading profile assets.
- **Verify with the real external system.** Cron repairs require job status/output/log verification; gateway repairs require inbound/outbound log evidence; Telegram profile changes require Bot API verification; summary jobs require actual transcript/output inspection.
- **Minimize blast radius.** Prefer targeted config/job updates over delete-and-recreate. Restart only the necessary service and confirm the live process reloaded.
- **Separate delivery success from content/data success.** A cron job can deliver an empty/status-only message because no new transcript rows exist; a gateway can receive bridge traffic but fail to persist it; a profile upload can succeed while clients still show cached old photos.
- **Do not expose secrets.** Redact tokens, API keys, OAuth access tokens, and bot tokens in all summaries and support files.

## Cron job troubleshooting and repair

Use this subsection for failed scheduled jobs, duplicate jobs, wrong provider/model, wrong delivery target, or manual reruns.

1. List jobs first with the `cronjob` tool or `hermes cron list`; never guess job IDs.
2. Inspect the job record in `~/.hermes/cron/jobs.json` and the latest output under `~/.hermes/cron/output/<job_id>/`.
3. Check `~/.hermes/logs/agent.log` around the run for provider/model/base URL, retry attempts, credential-pool messages, completion status, and delivery result.
4. Prefer `cronjob(action="update", ...)` over delete/recreate so the original job ID, origin, schedule history, and routing are preserved.
5. For provider/model failures (`503`, `429`, temporary model unavailable, auth errors), verify which provider cron actually used; do not infer it from the current chat session.
6. OAuth-backed providers can report `logged in` while cron runs still fail with `token_revoked`/invalidated credentials. If the user needs the job restored immediately, test a known working fallback provider with a tiny chat/sentinel run, then update the affected cron job in place to that provider/model rather than blocking on OAuth repair.
7. Before rerunning production jobs that deliver to Telegram/WhatsApp/Discord, consider a low-impact one-shot `deliver='local'` sentinel job to validate the provider/model.
8. After `cronjob(action='run')`, wait for the scheduler and verify `last_status=ok`, output file contents, agent log completion, and delivery log. Scheduling a run is not proof it completed; recurring jobs may advance `next_run_at` after a manual trigger, so check the actual output directory and job record before declaring success.

Reference patterns:
- `references/cron-openai-codex-provider-repair.md`
- `references/cron-news-digest-manual-rerun-verification.md`

## Messaging gateway troubleshooting

Use this subsection when Telegram/WhatsApp/Slack/Discord/etc. is silent, not replying, not receiving messages, or behaving differently across channels.

1. Check gateway service health: `hermes gateway status` and systemd status if managed.
2. Read `~/.hermes/logs/gateway.log` around the user's message time; search platform name, sender ID, `Unauthorized user`, `failed to send`, `error`, `exception`, and `traceback`.
3. Check platform-specific bridge logs when applicable, especially `~/.hermes/whatsapp/bridge.log`.
4. Compare the runtime sender/chat identity against the configured allowlist. For WhatsApp, normalize phone JIDs and LID aliases; do not rely on visible phone numbers alone.
5. Identify the drop layer: bridge ignored, Python gateway unauthorized, agent/provider failed after dispatch, or outbound delivery failed.
6. Apply the smallest config fix, restart gateway when environment/config changed, and verify the live process/env/logs after restart.

Common WhatsApp signatures:
- `self_chat_mode_rejects_non_self`: self-chat mode rejected non-self inbound traffic.
- `allowlist_mismatch`: bridge allowlist rejected the sender.
- `Unauthorized user: ... on whatsapp`: Python gateway received the event but authorization rejected it.
- Raw `@g.us` upserts without stored transcript rows: bridge sees group traffic but gateway storage/allow-through is still blocked.

Reference patterns:
- `references/whatsapp-self-chat-allowlist.md`
- `references/whatsapp-repair-and-qr-pairing.md`
- `references/whatsapp-repair-reset-and-pairing-timeouts.md`
- `references/whatsapp-terminal-pairing-after-qr-failures.md`
- `references/telegram-forum-topic-creation.md`
- `references/telegram-dm-topic-context-lanes.md`

## WhatsApp read-only group ingest and community summaries

Use this subsection for WhatsApp group/community digests, read-only group collection, summary audits, or cron summary repairs.

### Read-only ingest

- Bridge-level allow-through may be required before Python gateway rules matter. In self-chat mode, allow specific group JIDs through while suppressing auto-reply.
- Mark forwarded bridge events with a suppress-auto-reply flag and have the Python gateway persist inbound user messages to the transcript without sending a response.
- Authorize allowlisted group chats at the gateway layer as chat-level sources.
- Aggregate all sessions whose key starts with `agent:main:whatsapp:group:<group_jid>:`; do not assume one session per group because sessions may be split per sender.
- Resolve human-readable group subjects from bridge metadata when possible.
- For Basim/Tuan, WhatsApp read-only means **total outbound prohibition**, not merely “no group replies”: no WhatsApp DM replies, group replies, reactions, cron delivery, shutdown notification, or `send_message` targets. Config-only controls may be insufficient; verify adapter/tool-level guards and recent logs. See `references/whatsapp-total-readonly-hardlock.md`.

### Summary quality target

A good WhatsApp/community summary is an operational brief, not a raw recap. Separate:

1. Fakta — what was actually said.
2. Sinyal percakapan — representative messages/themes.
3. Makna / so what — why it matters.
4. Pertanyaan prioritas — urgent/medium/opportunity open questions.
5. Risiko / batasan — technical, operational, legal, or verification caveats.
6. Aksi berikutnya — concrete admin/mentor/member follow-up.
7. Audit kualitas — what was filtered and what remains unverified.

Filter low-value chat noise (`ok`, `siap`, emoji-only, laughter, one-letter replies, recursive generated summaries) unless it materially changes context. Keep short messages when they are real questions or actionable state.

Preferred Indonesian daily-summary shape:

```text
Ringkasan Harian <Group> — <date>

Inti utama: <activity level, dominant topic, message/member count, and note that this reflects new messages only.>
Status informasi: <cukup kuat / sedang / rendah>; <reports vs confirmed facts vs unresolved questions.>
Sinyal percakapan paling jelas: <speaker + compact excerpt>; <speaker + compact excerpt>.

Catatan untuk lanjutannya:
- <specific follow-up>

Link Penting:
- <human label>: <url>

Pertanyaan Belum Terjawab:
- <question or none>

Statistik: <message count> pesan dari <active member count> anggota aktif; topik dominan: <topic>; member paling aktif: <names>.
```

For script-backed summaries, use helpers such as `is_low_value_chat_noise`, `question_priority`, `technical_risks_for_text`, and role-based action generation. Verify edits with `python3 -m py_compile` and a dry run against recent safe transcript windows.

Reference patterns:
- `references/whatsapp-read-only-group-collection.md`
- `references/whatsapp-total-readonly-hardlock.md`
- `references/whatsapp-group-summarization-after-read-only-ingest.md`
- `references/whatsapp-group-name-resolution.md`
- `references/whatsapp-community-actionable-summary-script-pattern.md`
- `references/whatsapp-summary-audit-and-compact-format.md`
- `references/whatsapp-digest-editorial-heuristics.md`
- `references/whatsapp-cron-summary-delivery-and-checkpoints.md`
- `references/whatsapp-cron-hidden-and-narrative-summary-format.md`

## Telegram Bot API operations and profile assets

Use this subsection when the user asks to create forum topics, enable Telegram DM topic lanes, or change/verify a bot profile photo/avatar.

### Forum topics and context lanes

- Use `send_message(action='list')` / channel directory data to identify the target parent forum group before calling Telegram Bot API.
- For forum topics, call `createForumTopic` on the parent chat, not an existing thread ID, and report actual `message_thread_id` values.
- For DM topic lanes, explain BotFather/client prerequisites and the root-lobby behavior; do not promise client-side folder/topic creation the bot cannot control.

### Bot profile/avatar workflow

1. Clarify style only if needed; when taste matters, generate multiple labeled candidates and send previews before installation.
2. Prepare a square JPG/PNG suitable for Telegram circular crop.
3. Quality-check for text, watermark, severe artifacts, poor crop, and style mismatch.
4. Upload using `setMyProfilePhoto` with `InputProfilePhotoStatic` and `attach://photo` multipart file field.
5. Verify with `getMe` and `getUserProfilePhotos?user_id=<bot_id>&limit=1`.
6. If API verification succeeds but the user cannot see the change, explain Telegram client caching and suggest reopening/restarting the client.

Reference patterns:
- `references/telegram-profile-photo-api.md`
- `references/telegram-bot-api-profile-photo.md`
- `references/telegram-gpt-image-2-profile-avatar.md`

## Provider account usage / quota checks

Use this subsection when the user asks to check Hermes provider usage, quota, account limits, or OpenAI-Codex/Gemini/Anthropic/OpenRouter consumption.

1. Load `hermes-agent` for canonical CLI/provider commands.
2. Check active provider/model and OAuth status with `hermes status` and `hermes auth list <provider>`; do not expose raw credentials.
3. Use `hermes insights --days <N> --source <platform>` for session-level token/message/tool usage.
4. Use `agent.account_usage.fetch_account_usage('<provider>')` for account-limit state when supported. For OpenAI-Codex, the API may report plan/spend/credits while omitting rate-limit percentages; state that limitation instead of guessing remaining quota.
5. Report account-limit state separately from session token usage, with exact command-derived values and a timestamp.

Reference pattern:
- `references/provider-account-usage-checks.md`

## Reporting back

- Report the cluster/layer diagnosed, exact status codes or log signatures, and the verified outcome.
- For provider usage checks, keep account status and session token usage separate; never paste account IDs, user IDs, emails, OAuth tokens, or raw credential JSON into the user-facing summary.
- For user-facing WhatsApp/community summaries, keep operational cron IDs, scheduler footers, and debug details out of the delivered summary unless the user requested an audit/debug report.
- In Indonesian contexts for Basim/Tuan, prefer concise Indonesian status and address the user as **Tuan** when reporting back.

## Support files

This umbrella preserves detailed session-derived recipes in `references/`. The file names are prefixed by domain (`cron-`, `whatsapp-`, `telegram-`) so agents can load only the subsection they need.