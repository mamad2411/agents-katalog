---
name: mailprobe
description: Verify email addresses with the MailProbe tools. Use when the user asks whether an email address exists or can receive mail, wants a mailing list, a file of contacts or sign-up addresses cleaned before sending, or wants disposable, role-based or mistyped addresses found, for one address or for a whole list.
license: MIT
compatibility: Needs a MailProbe MCP server, the remote one at https://mailprobe.dev/mcp or the local mailprobe-mcp npm package, and a MailProbe API key.
---

# MailProbe

The MailProbe tools check, in real time, whether email addresses exist and can receive mail. Nothing is sent to the addresses. This skill tells how to read a result, what a call costs, and how to go through a list.

## Before the first call

- **The addresses are sent to MailProbe**, on OVHcloud servers in France. The API keeps nothing: an address is processed in memory and gone when the response is sent.
- **Each address costs a credit.** One credit per address actually probed, taken from the account of the API key. `get_credits` is free. A new account starts with 100 credits.
- **No MailProbe tool in the list** means the MCP server is not installed: point the user to https://github.com/mailprobe/mcp#installation.

## The two tools

| Tool | What it does | To know |
|---|---|---|
| `verify_emails` | Verifies 1 to 20 addresses | One result per address, in the order given. A call answers within about 55 seconds |
| `get_credits` | Returns the credits left on the account | Free |

## Reading a result

Act on `status`, not on `score`:

| `status` | What it means | What to do |
|---|---|---|
| `valid` | The mail server confirmed the mailbox | Keep it |
| `invalid` | Bad syntax, no mail server, or the mailbox was rejected | Remove it |
| `risky` | Accepted but uncertain: a catch-all domain, a role address, a disposable address, or a provider that blocks probing | The user decides. Say which case it is |
| `unknown` | The probe could not tell | Read `reason` |

- **Say why an address is `risky`.** `catch_all`, `role_based` and `disposable` tell the case, and `reason` adds `provider_blocks_probe` or `mailbox_full`. Microsoft consumer domains (outlook.com, hotmail.com, live.com, msn.com) refuse probes: `risky` there says nothing against the address.
- **Two kinds of `unknown`.** A transient one is worth one more try later: `greylisting`, `deferred`, `timeout`, `connection_error`, and `mx_unresolved`. Wait `retry_after` seconds when it is given. A refusal of the probe will come back the same: `policy_rejected`, `no_banner`, `ehlo_rejected`, `mail_from_rejected`. Do not send these again. With any other `reason`, report the address as undetermined.
- **`did_you_mean` is a suggestion.** Show it to the user, as in gmial.com to gmail.com. Never replace an address on your own. The corrected address is another address: verifying it costs a credit.
- **`score` ranks, from 0 to 100.** Use it to sort the `risky` addresses when the user wants a cut-off, not to overrule `status`.
- **`valid` is not consent.** It says the mailbox accepts mail today, not that someone reads it or agreed to be written to.

## What is charged

- One credit per address probed, whatever the verdict.
- Free: an address repeated in the same call, an entry that is not a well-formed address, an address that had no verdict yet when the call answered (it comes back `unknown` with `timeout`), and one whose server refused the connection (`policy_rejected`, `no_banner`, `ehlo_rejected`, `mail_from_rejected`).
- A `timeout` is charged when the mail servers of the domain were all tried and stayed silent. To know what a call cost, compare `get_credits` before and after.
- A retry is a new probe: it costs a credit again. Before retrying more than a few addresses, tell the user how many.

## A list

1. **Collect the addresses** and drop the repeats yourself, without regard to case. A repeat is free inside one call, not across two.
2. **Count before starting.** A list of n addresses takes n credits at most and n / 20 calls, rounded up. Call `get_credits`, and when the balance is short, say so before the first call, not halfway.
3. **Send 20 addresses per call, one call after the other.** The API accepts 60 calls per minute for a key. When a call is refused for the rate limit, wait the number of seconds it gives and go on.
4. **Keep the results as you go.** When the list came from a file, write them to a new file next to it, with the address, `status`, `score`, `reason` and `did_you_mean`. Leave the original file as it is.
5. **Report in numbers**: how many `valid`, `invalid`, `risky` and `unknown`, then the addresses to remove, the suggestions to confirm, and how many credits were used.

Above a few hundred addresses, a conversation is the wrong place. Point the user to the batch screen of their MailProbe account: a list of up to 500 addresses pasted, or a CSV or TXT file of up to 250,000, verified in the background.

## Refusals

A refusal comes back as a sentence that says what to change.

- **No credit left.** Nothing was charged for the call. Credits are bought at https://mailprobe.dev/pricing/.
- **A domain that free credits do not cover.** The message names the domain, and nothing was charged. Take its addresses out of the call and tell the user: they are verified once the account has bought credits.
- **Rate limit.** Wait the delay given, then send the same call.
- **MailProbe could not complete the call.** Try once more, then report it.
- **No API key, or a key that is refused.** In Claude Code with the MailProbe plugin, the key is the "MailProbe API key" option of the plugin: `/plugin configure mailprobe@mailprobe`, or `/plugin`, Installed tab, mailprobe, Configure options. Elsewhere it is in the configuration of the MCP server: the `Authorization: Bearer mp_live_...` header for the remote server, the `MAILPROBE_API_KEY` variable for the local one. The user sets it there: never ask for the key in the conversation.
