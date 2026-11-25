---
name: tweet-draft-approval-payload-builder
version: "2.1"
description: Runs the tweet-draft approval flow end to end yourself — collect the Lark tweet draft or approval-card action, audit it with your own model, build the exact Lark post/card, and post it to the source chat.
metadata:
  category: plain
  tag:
    - aevatar
    - s-capability
    - tweet-draft
    - lark
    - payload-builder
  clawdbot:
    emoji: "memo"
    files:
      - "references/*"
      - "scripts/*"
---

# Tweet Draft Approval

Use this when someone submits a Twitter/X draft in Lark for aelf content review, or when an admin
clicks the approve/reject button on the review card.

**You (the agent) run the WHOLE flow yourself with your own tools, then POST the approval card to
the chat.** Do NOT refuse, do NOT just describe, do NOT claim "the skill only formats" — drive the
flow. This skill has no Lark 审批 instance: its terminal action is posting the post/approval CARD
back to the source chat. Never ask the user for tokens — your NyxID-brokered tools broker all
credentials.

## How to run it

1. **Resolve inputs.** From the current Lark invocation (no `approval_code` here): for a chat
   draft pull `chat_id`, sender `open_id` as `employee_id`, and the message `content.text` as
   `tweet_draft`; for an admin card click pull `action`, `chat_id`, `employee_id`, `tweet_draft`
   from the card `action.value`. If you only have a message id, COLLECT the message first (step 2).

2. **Collect from Lark.** Read the message/card via NyxID-brokered Lark OpenAPI using `nyxid_proxy`
   `{slug:"api-lark-bot", path:"/open-apis/im/v1/messages/{message_id}", method:"GET"}` when you
   need to look up the draft by id; otherwise use the event fields already attached to the chat
   invocation. Public web context (e.g. a linked article) goes through `web_fetch`.

3. **Analyze the tweet draft with your own model.** For a chat draft, audit it against the aelf
   policy — strategic value, audience fit, plain-language clarity, compliance/PR risk — and produce
   strict JSON `{ "status": "APPROVED" | "REJECTED", "report": "<detailed audit report>" }`. For an
   admin card click, skip the audit and use the admin action directly.

4. **Build the exact Lark payload by running the bundled builder.** Call
   `scripts/build_tweet_draft_approval_payload.js` via `code_execute` with `language: "javascript"`
   (NO stdin — inline the data):
   - chat draft: `const {buildPayload}=require('./scripts/build_tweet_draft_approval_payload.js');
     console.log(JSON.stringify(buildPayload({mode:"build_ai_review_payload", chat_id, employee_id,
     tweet_draft, status, report})))`
   - admin click: same `require`, then `buildPayload({mode:"build_admin_action_payload", action,
     chat_id, employee_id, tweet_draft})`
   - raw event normalization: `buildPayload({mode:"parse_event", body:<event>})`.
   Use the returned `lark.body` and `lark.path`. If you genuinely cannot execute code, build the
   body by following `references/tweet-draft-approval-contract.md` field-for-field.

5. **Terminal — post the card to the source chat.** Send the built post/approval CARD into the
   source chat with `reply_with_interaction` (for the interactive admin-review card) or
   `lark_messages_send` / `lark_messages_reply` using the `lark.body` from step 4. The underlying
   Lark REST target is `POST /open-apis/im/v1/messages?receive_id_type=chat_id`. For a URL
   verification body, return the builder's `webhook.responseBody`.

6. **Report** one line: which branch ran (`ai_rejected`, `ai_approved_admin_review`,
   `admin_approved`, or `admin_rejected`) and that the card was posted to the chat.

## Payload builder reference

`scripts/build_tweet_draft_approval_payload.js` exports `buildPayload(data)`. Modes:
`parse_event` (normalize a raw URL challenge / text message / card-action event), `parse_ai_result`
(parse raw audit text into `status` + `report`), `build_ai_review_payload` (default — AI-rejected
post or AI-approved admin-review card), `build_admin_action_payload` (admin-approved or
admin-rejected post), and `auto`. Output carries `lark.path` and a `lark.body` whose
`receive_id` / `msg_type` / stringified `content` already match Lark's send-message API. Exact
aliases, branch behavior, and examples are in `references/tweet-draft-approval-contract.md`.

## Guardrails

- Use real event fields and your own model output; never invent chat ids, open ids, admin ids,
  tweet drafts, approval actions, status, or reports. The admin `<at>` id stays the literal
  `ou_PLACEHOLDER_OPEN_ID_1` from the source flow unless a real admin open id is supplied.
- Prefer running the bundled script; it is the deterministic source of truth for the Lark payload.
- Route all sending and credential exchange through your NyxID-brokered Lark tools; never handle
  raw secrets.
