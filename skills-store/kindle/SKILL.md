---
name: kindle
description: Send a local ebook to Kindle with the zlib CLI, configure its SMTP delivery, or diagnose a failed send. Use the bundled zlib skill to search or download a book first.
license: MIT
---

# Kindle delivery

Use `zlib kindle send` for a local file. It uses SMTP and does not need a
Z-Library login. If a book must be found or downloaded first, use the bundled
[zlib skill](../zlib/SKILL.md).

## Send

1. Confirm `zlib version` succeeds and the requested file exists. If `zlib` is
   missing, install it as described in the [zlib skill](../zlib/SKILL.md). Resolve an
   ambiguous file choice before sending. Reuse the user's existing choice.
2. If the user requested delivery and settings are already configured, run the
   command below without a TTY. Let the CLI resolve `ZLIB_SMTP_PWD` from its
   environment and `.env` files; checking only the shell variable is insufficient.
3. If settings are missing or the user requests setup, read
   [SMTP setup](references/setup.md), complete the missing settings, then send.

```sh
zlib kindle send "./books/book.epub"
```

Pass the actual file path. Bare `zlib kindle` and `zlib kindle send` open the file
picker; `zlib kindle config` opens delivery settings. Interactive sends share the
TUI confirmation, password, and result pages. Sending mail requires the user's request; an existing instruction to send
this file is sufficient, so do not ask for another confirmation.

In the TUI, a missing SMTP password opens a masked prompt after send confirmation.
It saves `ZLIB_SMTP_PWD` to the global `.env` and current process. Non-interactive
commands still require the variable or an existing `.env` entry before sending.

Report the CLI result and file name. SMTP success means the sending server
accepted the message, not that the Kindle received it. After a timeout or uncertain
result, check the failure before retrying to avoid duplicate messages.

## Failures

| Result | Next action |
| --- | --- |
| Missing configuration or SMTP password | Follow [setup](references/setup.md); never request a password in chat |
| SMTP authentication rejected | Check sender account, provider authentication requirements and settings precedence |
| SMTP timeout / connection failure | Check the host, port and network; `ZLIB_PROXY` affects HTTP requests, not SMTP |
| Unsupported attachment | Report the CLI rejection; do not rename an extension to bypass validation |
| Attachment too large | Report the size error; encoding adds overhead to the SMTP message |
| Send succeeded, book missing | Check recipient, Amazon's approved sender list and any delivery response email |

The current CLI validates file types and size before sending. It rejects MOBI.
From v0.0.11, `smtp_security` selects `tls` (SSL/TLS on connect) or `starttls`.
When it is empty, port 465 means `tls` and any other port means `starttls`.
Earlier versions support only STARTTLS (check `zlib version`). TLS is always
required: a server without STARTTLS fails before login. SMTP errors name the
host, the port and the mode, and suggest the other mode when the failure looks
like a mismatch. Do not guess SMTP settings from the email domain or promise that
switching ports will fix an error.
