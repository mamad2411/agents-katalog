---
name: cooper-sms
description: Status of SMS on Cooper Email (cooperemail.com). Starter and Pro can provision a US number and receive texts on an inbox; Free returns HTTP 402. Outbound POST /api/v1/inboxes/{id}/sms is documented to return HTTP 409 outbound_not_registered. Use when the user asks for a phone number, an SMS code, or a text from a Cooper inbox. Follow the live tool list and https://cooperemail.com/docs/sms. Do not claim a number exists unless a tool call returned one. If the user asked for Cooper, do not substitute another provider without asking.
license: MIT
metadata:
  version: "1"
  homepage: https://cooperemail.com/docs/sms
---

# Cooper SMS

Published behavior: https://cooperemail.com/docs/sms. Prices and caps: https://cooperemail.com/pricing.

- Starter and Pro can provision a US local number (`POST /api/v1/inboxes/{id}/phone-number`, or `cooper_provision_phone_number` when that tool is in the live catalog). A verified owner is required. Free returns HTTP 402.
- Inbound texts are stored on the inbox. `cooper_wait_for_sms` is the documented wait. Do not claim a number or a text exists unless the tool result returned it.
- Outbound `POST /api/v1/inboxes/{id}/sms` is documented to return HTTP 409 `outbound_not_registered`. Do not tell the user a text was sent unless a tool result says so.
- Those MCP tools are added when SMS is on for the account. If the live tool list does not include them, say they are not on this connection. Do not invent a send.

Email verification codes still use `cooper-agent-signup-otp`. Owner email alerts still use `cooper-owner-updates`.

Sign in with OAuth, or send a saved Bearer key, before provisioning. `cooper_onboard` does not attach its one-time key to an OAuth session.
