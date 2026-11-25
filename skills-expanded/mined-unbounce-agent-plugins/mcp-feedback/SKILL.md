---
name: mcp-feedback
description: Record a user's feedback about the Unbounce MCP tools — a bug, praise, a feature request, confusion, or anything else — straight to the team via the submit_feedback tool, with no copy/paste. Use when the user wants to report a bug, share feedback, praise something, request a feature, or flag that a tool was confusing. Also covers login/connection issues — the user can't connect the MCP in their client, sees an OAuth error ("access denied", "invalid_grant", a failed redirect), or keeps getting asked to log in again. You may also offer it after a hard MCP tool failure. It confirms the exact content with the user and redacts secrets before anything is stored.
requires:
  mcpServers:
    - unbounce-mcp
---

# Submit Unbounce MCP feedback

Record the user's feedback about the **Unbounce MCP tools** to the team's store by
calling the **`submit_feedback`** tool. The tool persists the record server-side, so
nothing has to be copied out of the conversation into Slack or anywhere else.

> The `mcp-` prefix here means "pertains to Unbounce MCP," not "about a page." This
> skill is about capturing feedback on the MCP tools themselves — whether they broke,
> delighted, confused, or fell short.

## Hard rule: report, don't repair

**Do NOT try to fix, retry, or work around the thing being reported.** This skill
records feedback on what already happened. Never invent tool-call arguments or error
text — anything not actually present is `unknown`. (Fixing the underlying task, if the
user wants that, is separate work done after the feedback is recorded.)

## 1. Gather the feedback

Settle two things — from the conversation where possible, asking only what you can't
infer:

- **`type`** — one of `bug` · `praise` · `feature_request` · `confusion` · `other`.
- **`message`** — the feedback in the user's own words. Keep it faithful; don't
  editorialize.

For a **`bug`**, also assemble the **`context`**: the verbatim failing tool call(s)
from the transcript — exact tool name, exact arguments JSON, and the raw result/error
text (call out any `code`/`reason`/`remedy` fields). Include the relevant one(s),
especially the failing call. If the failure happened in another session and isn't in
the transcript, ask a couple of targeted questions and mark transcript-only fields
(exact arguments, exact raw error) as `unknown`. For non-bug types, `context` is
usually unnecessary — include a light pointer (the tool or page in question) only if
it genuinely helps.

**Login / connection problems** are a `bug`: capture what the user was doing, the
client they're in, and the exact error text (e.g. `access denied`, `invalid_grant`, a
failed redirect, repeated re-login prompts). Note that if the MCP can't connect _at
all_, `submit_feedback` itself won't be reachable — that's expected, and step 4's
inline fallback is how the feedback still gets out.

## 2. Redact secrets

Replace any access token, API key, password, or bearer token in the `message` or
`context` with `«REDACTED»`. Count how many you redacted. (The server re-scrubs as a
backstop, but do your pass first — the user is about to review this content.)

## 3. Confirm the exact content, then submit

Show the user the **exact record** you're about to store — the `type`, the `message`,
and the `context` if any (post-redaction) — and get an **explicit yes** before
calling the tool. This is the consent step; do not skip it and do not submit
silently. (Same ask-first bar the page tools hold for Dynamic Text Replacement.)

On yes, call **`submit_feedback`** with `type`, `message`, and `context` (if any). The
server stamps identity, timestamp, and build itself — you don't pass those.

## 4. On failure, don't lose the feedback

If `submit_feedback` fails (an error result, the tool isn't available, or an older
deploy predates it): **retry once.** If it still fails, **print the composed,
already-redacted record inline** in the conversation and tell the user to pass it to
the team directly. There is no file to write — the goal is simply that the feedback is
never silently lost.

## 5. Report back

On success, print to the conversation — nothing more:

1. **Recorded.** A one-line plain-language summary of what was captured, with the
   `type`.
2. The returned **`feedback_id`**.
3. **Only if the server redacted something you missed:** `Server redacted N
additional secret(s).` (compare the tool's `redacted_secrets` to your own count).

Example:

> Recorded your **bug** report: `set_page_url` returned `DOMAIN_NOT_FOUND` for a domain
> `list_client_domains` had just listed. (feedback_id `a1b2c3d4`)
