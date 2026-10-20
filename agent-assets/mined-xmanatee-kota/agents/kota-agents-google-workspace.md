# Google Workspace Module

This directory owns the Google Workspace capability pack — Gmail, Calendar, and Drive tools for agents.

## Auth Setup

This module uses OAuth 2.0 with a refresh token. One-time setup:

1. Open [Google Cloud Console](https://console.cloud.google.com/) and create or select a project.
2. Enable the **Gmail API**, **Google Calendar API**, and **Google Drive API**.
3. Create an **OAuth 2.0 client** (type: Desktop app). Download the credentials JSON.
4. Run the OAuth consent flow to obtain a refresh token with the required scopes:
   - `https://www.googleapis.com/auth/gmail.modify`
   - `https://www.googleapis.com/auth/calendar`
   - `https://www.googleapis.com/auth/drive.readonly`
5. Store credentials in `.kota/config.json` under `modules.google-workspace`:

```json
{
  "modules": {
    "google-workspace": {
      "clientId": "$GOOGLE_CLIENT_ID",
      "clientSecret": "$GOOGLE_CLIENT_SECRET",
      "refreshToken": "$GOOGLE_REFRESH_TOKEN"
    }
  }
}
```

Values starting with `$` are resolved through the shared secret provider, so setup-stored secrets and environment-backed secrets use the same runtime path. Alternatively, store the raw values directly in the config (scope-scoped `.kota/config.json` is gitignored by default).

## Config

| Field          | Required | Default     | Description                          |
|----------------|----------|-------------|--------------------------------------|
| `clientId`     | yes      | —           | OAuth 2.0 client ID or `$ENV_VAR`   |
| `clientSecret` | yes      | —           | OAuth 2.0 client secret or `$ENV_VAR`|
| `refreshToken` | yes      | —           | OAuth 2.0 refresh token or `$ENV_VAR`|
| `userId`       | no       | `"me"`      | Gmail user ID                        |
| `calendarId`   | no       | `"primary"` | Google Calendar ID                   |
| `inbound`      | no       | —           | Sender/organizer trust lists for inbound Gmail and Calendar signal adapters |

## Boundaries

- All tools are in the `productivity` tool group.
- Write tools (`gmail_send`, `calendar_create_event`) are classified as dangerous and queue for approval in autonomous mode.
- Gmail replies select a parent and thread through `gmail_get_message`, then
  pass that selection, exact subject and explicit recipients to `gmail_send`.
  Re-fetch parent metadata after approval; derive RFC identity only from the
  provider, and never infer reply-all. Uncertain send results require mailbox
  inspection before retrying; sending is not idempotent.
- Calendar creates require a caller-chosen random operation UUID before approval.
  Preserve it and the original parameters for recovery; a new meeting uses a new
  UUID even when its details match. `calendar_check_event` checks provider truth
  without writing, including after a redacted queued-approval result. An approved
  repeat of `calendar_create_event` uses the same provider event identity.
- Calendar operation fingerprints use the existing scope-owned idempotency store
  with retained intent, not cached results. Creation requires a live scope store;
  missing authority fails closed. Never expire these bindings into fresh work.
  Provider reads verify the authenticated account, resolved calendar, operation
  marker and current event details. A collision or matching title/time is not
  confirmation. Legacy unkeyed events cannot be attributed by this mechanism.
- Each configured tool set owns one credential-bound token getter, shared by Gmail,
  Calendar and Drive. Reload creates a fresh cache; readiness always verifies
  credentials with a fresh refresh request. Tokens refresh before expiry.
- Credentials are never logged or included in error messages.
- Gmail tools and Google-shaped inbound messages share the typed body decoder in
  `gmail-message.ts`; consumers own presentation, and explicit normalized inbound
  text retains precedence, including empty text. The decoder selects inline plain text through mixed and alternative
  MIME containers. Named or explicitly attached parts are excluded before
  traversal. Separately stored bytes and unsupported representations remain
  explicitly unavailable; snippets are labeled excerpts. Bound parsing and
  output, and disclose partial content instead of implying a complete read.
- When `inbound` is configured, the module contributes bearer-token-protected
  `POST /api/webhooks/google-workspace/gmail` and
  `POST /api/webhooks/google-workspace/calendar` routes. Those routes accept
  Google API-shaped message/event JSON or the module's normalized adapter
  shape, then emit `inbound.signal.received`.
- Gmail, Drive and Calendar listings share bounded traversal in `listing.ts`.
  Service adapters own page decoding and domain meaning; incomplete retrieval
  must retain prior items. Gmail detail failures retain listed IDs, and Drive
  incomplete-search evidence survives subsequent pages.
- Drive reads resolve shortcuts with current target metadata; shortcut MIME hints
  are not read authority. Keep both identities visible, bound resolution, and
  pass target resource keys only through authenticated request headers. Keys and
  provider error bodies must not appear in read diagnostics. Unsupported targets
  do not fall back to binary downloads or permission changes.
- Calendar listings keep time-blocking settings, event status, and attendee
  responses separate. Only provider `self` identifies the selected calendar's
  attendee; never infer it from an email or another guest's response. Apply
  documented defaults without inventing attendance. Retrieval completeness
  describes the event list, not everyone's availability.
- Calendar occurrence identity preserves the supplied original date/time and
  timezone separately from current start/end. Sparse cancellations do not imply
  a known organizer or authorize inferred occurrence times.
- Gmail and Calendar inbound routes only normalize Google source metadata,
  actor trust, and content into `inbound.signal.received`. The shared
  inbound-signals dispatcher decides source eligibility and workflow routing;
  downstream workflows own task capture, replies, owner questions, retries,
  audit, and no-op decisions after routing.
