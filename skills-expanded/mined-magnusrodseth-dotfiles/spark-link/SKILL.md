---
name: spark-link
description: Resolve a Spark email deep link (readdle-spark://) into the underlying Gmail message so it can be read, replied to, drafted from, or acted on with the gws CLI. Use whenever the user pastes a readdle-spark:// link, or refers to "the email I just copied from Spark", "this email" right after copying one, or asks to continue working in gws on something they are looking at in Spark.
---

# Spark link to Gmail

Magnus reads email in **Spark** but acts on it with **gws**. `Cmd+L` in Spark copies a deep link to the focused message. This skill turns that link into a Gmail message id and works from there.

## Resolve the link

```bash
~/dotfiles/scripts/spark/spark-to-gws.sh "<the readdle-spark:// link>"
```

Prints the account, Gmail message id, thread id, date, from, subject, a Gmail web URL, and ready-to-run gws commands. Pass `--id` for just the id when piping. With no argument it reads the clipboard, which is the normal terminal flow but not useful here since you already have the link in the prompt.

The user can also run `sg` in their own terminal, which is the same script.

## What the link actually contains

The payload after `bl=` is base64 (with CRLF and `=` padding percent-encoded) over four `;`-separated fields:

| Field | Meaning |
|---|---|
| `A` | account the message lives in |
| `ID` | the RFC822 `Message-ID` header |
| `gID` | **Gmail's own message id, in decimal** |
| (last) | unix timestamp |

`gID` is the whole trick. Gmail's API speaks hex, so `int -> hex` yields exactly the id the API wants, with no search step. When `gID` is missing (a non-Gmail account), the script falls back to Gmail's `rfc822msgid:` search operator on the `Message-ID`.

## Acting on it

Once you have the id, everything is normal gws:

```bash
gws gmail users messages get --params '{"userId":"me","id":"<ID>","format":"full"}'
gws gmail users threads  get --params '{"userId":"me","id":"<THREAD_ID>"}'
gws gmail +reply --message-id <ID> --body '...' --draft
```

`+reply` handles threading, and takes `-a/--attach`, `--cc`, `--bcc`, `--html`, `--from`. Prefer it over hand-building `message.raw`: serializing MIME yourself with Python's default policy emits bare `\n` instead of CRLF, which silently collapses every paragraph break on send while the draft preview still looks fine.

## Reading it in Spark instead

For the thread as Spark sees it (useful when the account is not Gmail, or you want Spark's own view), the `use-spark` skill wraps the `spark` CLI: `spark thread <message-id>`. Spark also owns meeting transcripts, templates and teams, which gws has no equivalent for.
