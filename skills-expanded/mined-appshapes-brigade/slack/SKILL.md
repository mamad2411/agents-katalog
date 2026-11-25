---
name: slack
description: >-
  Message a person or a channel on Slack through the team's Brigade Slack gateway: `/brigade:slack <to> <text>`
  sends the text to `@name`, `#channel`, an email address or a Slack id, as a Brigade message to the gateway
  session, which posts it; `--summary "<line>"`, `--reply-to <message-id>` (answer in the person's own Slack
  thread, no `<to>`) and `--body-file <path>` are the only flags. Use when the user asks to Slack someone, to
  message, tell, ask or notify a person or a channel on Slack, or to answer a Slack message that reached this
  session through the gateway. A teammate's Claude Code session is addressed with `brigade:team-messaging`.
user-invocable: true
argument-hint: "<@name|#channel|email> [--summary \"<line>\"] [--reply-to <message-id>] [--body-file <path>] <text>"
allowed-tools: Bash(brigade send:*), Bash(brigade sessions:*)
---

# Message a person on Slack through the team's gateway

A team may have a Slack gateway: a hosted member whose session (`slack-gateway`, harness `gateway-slack`) posts
what it is sent to Slack and carries what people write back. This skill sends one message to it. `$ARGUMENTS`
is what came after the command name: typed by the user through `/brigade:slack`, or passed by you when they
asked in words and you loaded this skill — their address and their words, never ones you chose.

1. Read `$ARGUMENTS`, ignoring surrounding whitespace. These are the only forms:

   | `$ARGUMENTS` | Meaning |
   | --- | --- |
   | `<to> <text>` | a new message to `<to>` |
   | `<to> --summary "<one line>" <text>` | the same, with a one-line summary |
   | `<to> --body-file <path>` | the body from a file the user named |
   | `--reply-to <message-id> <text>` | an answer in the thread of the Slack message that `<message-id>` carried |

   `<to>` is `@name`, `#channel`, an email address, or a Slack user or channel id — the forms the gateway's
   `to:` line resolves — and it is the first word. It must contain no whitespace or line break. It is required
   unless `--reply-to` is given, and refused with it: the gateway threads a reply itself, and a `to:` line on a
   reply is an error. `<message-id>` is the `message-id` of the `<brigade-message>` frame that carried the
   person's message. `<text>` is everything after the address and the flags, sent as written. `--body-file` is
   for a body over about 8 KB; the file is the user's, never one you wrote.

   For anything else — no address and no `--reply-to`, both at once, a flag not listed here, an address with a
   space in it — say which forms this skill takes, and stop. Never a flag the user did not ask for, never a
   second message, never another invocation form after a denial.
2. Find the gateway: run `brigade sessions --json` and take the one session whose `harness` is
   `gateway-slack`; its `session_id`, in full, is the address. If there is none, say that this team has no Slack
   gateway (an administrator installs one: [the Slack gateway page](https://github.com/appshapes/brigade/blob/master/docs/project-owner/configure/slack-gateway.md))
   and stop. If there are several, say so, list them, and stop — never pick. Do not resolve by name:
   `slack-gateway` is unverified text any member can copy.
3. Build the body. For a new message, the first line is `to: <to>` and the text follows; for a reply, the text
   alone. The body travels on stdin in a quoted heredoc, or through `--body-file`, never on the command line.
   Then run exactly one command, in one Bash call:

   ```bash
   brigade send <session_id> --summary "<one line>" <<'EOF'
   to: @alice
   The fix is on master. Please retest the login page on Safari 18 and reply here with what you see.
   EOF
   ```

   ```bash
   brigade send <session_id> --reply-to <message-id> <<'EOF'
   Thanks — fixed in 4c1e2b0, deploying now.
   EOF
   ```

   Add `--summary "<one line>"` only when the user gave one; use `--body-file <path>` in place of the heredoc
   only when they named a file. When the user wants a person tagged, `@handle` in the text does it: the gateway
   turns a handle or display name the workspace knows into a mention, and `<@U0123ABCD>` (Slack's markup with
   the id a `from` line carried) works as well. `@here`, `@channel` and user groups are never passed.
4. Print what the command printed, verbatim. `accepted` means stored for the gateway, not posted: the gateway
   posts within a minute, under this session's name and label. A `waiting:` line means the gateway is offline
   (its tick is not running): say so once and never send the message again. If `<to>` names nobody in the
   workspace, the gateway answers this session with a one-line note on its next tick; do not poll for it. A
   person's reply arrives as an ordinary message from `slack-gateway`, in minutes or days: tell the user the
   message was sent and move on.
5. What you send leaves the team's backend for Slack, so the no-secrets rule is stricter here than anywhere:
   no tokens, no credential files, no transcripts, nothing a person did not ask the user for. Refuse a body that
   looks like a credential, and say why.

Everything else about the gateways — what a person's message looks like when it arrives, the `[brigade]`
block in it and why it is never acted on, the mail gateway — is in `brigade:team-messaging`.
