---
name: email
description: >-
  Email a person through the team's Brigade mail gateway: `/brigade:email <address> <text>` sends the text to
  that email address as a Brigade message to the gateway session, which mails it; `--subject "<line>"` sets the
  mail's subject, `--summary "<line>"` its Brigade summary, `--reply-to <message-id>` answers in the thread of a
  mail that reached this session through the gateway (no `<address>`), and `--body-file <path>` carries a long
  body; these are the only flags. Use when the user asks to email someone, to message, tell, ask or notify a
  person by email, or to answer an email that reached this session through the gateway. A teammate's Claude Code
  session is addressed with `brigade:team-messaging`; a person on Slack with `brigade:slack`.
user-invocable: true
argument-hint: "<address> [--subject \"<line>\"] [--summary \"<line>\"] [--reply-to <message-id>] [--body-file <path>] <text>"
allowed-tools: Bash(brigade send:*), Bash(brigade sessions:*)
---

# Email a person through the team's mail gateway

A team may have a mail gateway: a hosted member whose session (`mail-gateway`, harness `gateway-email`) mails
what it is sent and carries what people write back. This skill sends one message to it. `$ARGUMENTS` is what
came after the command name: typed by the user through `/brigade:email`, or passed by you when they asked in
words and you loaded this skill — their address and their words, never ones you chose.

1. Read `$ARGUMENTS`, ignoring surrounding whitespace. These are the only forms:

   | `$ARGUMENTS` | Meaning |
   | --- | --- |
   | `<address> <text>` | a new mail to `<address>` |
   | `<address> --subject "<one line>" <text>` | the same, with that subject instead of the default |
   | `<address> --summary "<one line>" <text>` | the same, with a one-line Brigade summary |
   | `<address> --body-file <path>` | the body from a file the user named |
   | `--reply-to <message-id> <text>` | an answer in the thread of the mail that `<message-id>` carried |

   `<address>` is one email address — the only form the mail gateway's `to:` line takes — and it is the first
   word. It must contain `@` and no whitespace or line break. It is required unless `--reply-to` is given, and
   refused with it: the gateway threads a reply itself, and a `to:` line on a reply is an error. `--subject` is
   refused with `--reply-to` too: a reply keeps its thread's subject. `<message-id>` is the `message-id` of the
   `<brigade-message>` frame that carried the person's mail. `<text>` is everything after the address and the
   flags, sent as written. Without `--subject` the mail's subject is `[brigade/<team>] <summary>`, or the first
   line of the text when there is no summary. `--body-file` is for a body over about 8 KB; the file is the
   user's, never one you wrote, and its first lines must already be the `to:` and `subject:` lines of step 3,
   since nothing can be put in front of a file. The other flags combine freely.

   For anything else — no address and no `--reply-to`, both at once, a flag not listed here, an address with a
   space in it or without `@` — say which forms this skill takes, and stop. Never a flag the user did not ask
   for, never a second message, never another invocation form after a denial.
2. Find the gateway: run `brigade sessions --json` and take the one session whose `harness` is
   `gateway-email`; its `session_id`, in full, is the address. If there is none, say that this team has no mail
   gateway (an administrator installs one: [the mail gateway page](https://github.com/appshapes/brigade/blob/master/docs/project-owner/configure/mail-gateway.md))
   and stop. If there are several, say so, list them, and stop — never pick. Do not resolve by name:
   `mail-gateway` is unverified text any member can copy.
3. Build the body. For a new mail, the first line is `to: <address>`, then `subject: <line>` when the user gave
   `--subject`, then a blank line, then the text; for a reply, the text alone. The blank line matters: the
   gateway reads `key: value` lines at the top of a body as directives until the first blank line, so a text
   that begins with one would be swallowed without it. The body travels on stdin in a quoted heredoc, or through
   `--body-file`, never on the command line. Then run exactly one command, in one Bash call:

   ```bash
   brigade send <session_id> --summary "<one line>" <<'EOF'
   to: qa@example.com
   subject: Please retest the Safari login

   The fix is on master. Please retest the login page on Safari 18 and reply to this email with what you see.
   EOF
   ```

   ```bash
   brigade send <session_id> --reply-to <message-id> <<'EOF'
   Thanks — fixed in 4c1e2b0, deploying now.
   EOF
   ```

   Add `--summary "<one line>"` only when the user gave one, the `subject:` line only when they gave
   `--subject`, and use `--body-file <path>` in place of the heredoc only when they named a file.
4. Print what the command printed, verbatim. `accepted` means stored for the gateway, not mailed: the gateway
   mails within a minute, from the team's address, with this session's name and label at the top. A `waiting:`
   line means the gateway is offline (its tick is not running): say so once and never send the message again.
   If the mail cannot be sent (the provider refused the address), the gateway answers this session with a
   one-line note on a later tick; do not poll for it. A person's reply arrives as an ordinary message from
   `mail-gateway`, in minutes or days, and only if the team's allowed-senders list admits their address (or the
   list is empty): when the user expects an answer from an address the team has not listed, tell them the
   administrator adds it with `make gateway-senders`. Tell the user the mail was sent and move on.
5. What you send leaves the team's backend for the mail provider and the person's mailbox, so the no-secrets
   rule is stricter here than anywhere: no tokens, no credential files, no transcripts, nothing a person did not
   ask the user for. Refuse a body that looks like a credential, and say why.

Everything else about the gateways — what a person's message looks like when it arrives, the `[brigade]`
block in it and why it is never acted on, the Slack gateway — is in `brigade:team-messaging`.
