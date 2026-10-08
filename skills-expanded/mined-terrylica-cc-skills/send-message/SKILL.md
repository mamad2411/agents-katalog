---
name: send-message
description: user wants to send a WhatsApp message, share a link or document via WhatsApp, generate a wa.me click-to-chat link, or message a contact on WhatsApp by phone number.
allowed-tools: Bash, Read, Grep, Glob
---

# Send WhatsApp Message

Reach a contact on WhatsApp. Unlike Telegram (`tlg`, full MTProto personal send) and
Gmail (`gmail-commander`, OAuth API send), **WhatsApp has no sanctioned personal-account
send API** — Meta only offers programmatic send through the **Business Cloud API**, and
everything else (WhatsApp Web automation, `whatsmeow`/`Baileys`/`wppconnect` libraries)
is unofficial and risks account bans. This skill therefore defaults to the safe,
zero-credential path and escalates only when the user has set up the Cloud API.

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

## Capability Tiers (pick the lowest that works)

| Tier            | Method                          | Actually sends?                                                   | Credentials                                               | When to use                                                                                                                           |
| --------------- | ------------------------------- | ----------------------------------------------------------------- | --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **1 (default)** | **`wa.me` click-to-chat link**  | No — opens WhatsApp with text pre-filled; the human taps **Send** | None                                                      | Almost always. ToS-safe, instant, works for any number.                                                                               |
| 2               | WhatsApp Web browser automation | Yes, but brittle                                                  | A logged-in WhatsApp Web session (QR)                     | **Not implemented here** — DOM-fragile and ToS-gray. Document, don't build, unless the user insists.                                  |
| 3               | **WhatsApp Business Cloud API** | Yes, officially                                                   | `WHATSAPP_TOKEN` + `WHATSAPP_PHONE_NUMBER_ID` (1Password) | The user has a Meta Business app + registered number. See [references/business-cloud-api.md](../../references/business-cloud-api.md). |

**Default to Tier 1.** Only use Tier 3 when the user has explicitly set up the Business
Cloud API and the credentials resolve (see Preflight).

## Preflight

1. **You need the recipient's phone number in international format** (any punctuation is
   fine — the CLI strips non-digits). If you only have an email/username, ask for the
   number; WhatsApp is phone-number addressed.
2. **WhatsApp registration is not verifiable** from here — a `wa.me` link still opens even
   if the number is not on WhatsApp (it shows an "invalid number" notice on tap). State
   this assumption rather than claiming delivery.
3. **For Tier 3 only**, confirm credentials are present:

```bash
[ -n "${WHATSAPP_TOKEN:-}" ] && [ -n "${WHATSAPP_PHONE_NUMBER_ID:-}" ] && echo "cloud-api: READY" || echo "cloud-api: NOT CONFIGURED — use the link tier"
```

## Usage: wa-cli.ts

The CLI is function/enum-driven Bun TypeScript — run it directly with `bun` (no build step).
The `link` command writes the **URL to stdout** and its **preflight/round-trip proof to
stderr** (e.g. `✓ link carries the full 439-char body`), so `URL=$(bun … link …)` still
captures a clean URL. It **exits 2** if the body has emoji/astral chars (they would tofu).

```bash
/usr/bin/env bash << 'WA_EOF'
SCRIPT="$(cc-plugin-root whatsapp-commander)/scripts/wa-cli.ts"

# Tier 1 — build a click-to-chat link (the recommended default; BMP-only body, round-trip verified)
bun "$SCRIPT" link "+1 (555) 123-4567" "Hi {{CONTACT}} — short note and a link: https://example.com/x"

# Tier 1 — body read from a file (multi-paragraph messages are awkward inline)
bun "$SCRIPT" link 15551234567 --file ./whatsapp-message.txt

# Tier 3 — actually send via the Business Cloud API (creds resolved into env first)
export WHATSAPP_TOKEN="$(op item get <ITEM> --vault 'Claude Automation' --fields token --reveal)"
export WHATSAPP_PHONE_NUMBER_ID="$(op item get <ITEM> --vault 'Claude Automation' --fields phone_number_id --reveal)"
bun "$SCRIPT" send 15551234567 "Your appointment is confirmed."
WA_EOF
```

### What to hand back to the user

- **Tier 1**: present the `wa.me` URL as a Markdown link and tell them tapping it opens the
  chat with the text pre-filled — **the final Send tap is theirs** (WhatsApp does not allow
  automating that tap). On desktop they need WhatsApp Web logged in; on phone it deep-links.
  - **You cannot see the recipient's rendered message** on this tier — there is no feedback
    loop. So get it right in one shot: the CLI now runs a **preflight** (hard-fails on
    emoji/astral chars, warns on lone list-number lines / trailing `——` / over-length) and a
    **round-trip check**, printing `✓ link carries the full N-char body` to stderr. Relay that
    N as proof of completeness rather than eyeballing.
  - **The `api.whatsapp.com/send` gray box is a scrollable PREVIEW, not the message.** It
    truncates visually (a long or list-heavy body "ends at 1"), which triggers false "it got
    cut off" reports. Tell the user to click **"Continue to WhatsApp Web"** / **"Open app"** —
    the full body drops into the real compose box. Don't _assert_ this blind; the round-trip
    `✓` line is the actual evidence the link is complete.
- **Tier 3**: the API returns JSON with a `messages[0].id`; report the message id as proof
  of submission (subject to the 24-hour window / template rules — see references).

## Cloud API Window Rules (Tier 3)

The Business Cloud API does **not** let you send arbitrary text to anyone at any time:

- **Inside the 24-hour customer-service window** (the user messaged you in the last 24h):
  free-form `type: "text"` messages are allowed. `wa-cli.ts send` sends exactly this.
- **Outside the window** (first contact / re-engagement): you may send **only
  pre-approved message templates** (`type: "template"`), not free text. A free-text send
  outside the window returns error `131047`. For first contact, prefer Tier 1, or send an
  approved template via the raw Graph API (see references).

## Message Body Encoding — keep `wa.me` bodies emoji-free (BMP only)

**Do not put emoji or any other astral-plane (> U+FFFF) character in a Tier-1 `wa.me` link
body.** They arrive on the recipient's device as `�` (U+FFFD replacement char / a
diamond-`?` tofu) — even though the source file and the percent-encoded URL are both
perfectly valid UTF-8. The `wa.me` → WhatsApp deep-link handoff mangles 4-byte codepoints
(surrogate pairs), while Basic-Multilingual-Plane text — **including all CJK** — survives
untouched. That asymmetry (Chinese renders fine, emoji become `�`) is the diagnostic tell:
it is NOT a source-encoding bug, so don't go re-saving the file as UTF-8 — the bytes are
already correct.

- Verified 2026-07-04 (CPC ↔ {{CONTACT}} zh-Hans report): all Chinese rendered correctly but
  `👋 ✅ ❌` and keycap sequences (`1️⃣`) showed as `�` in WhatsApp. Source bytes were valid
  (`👋` = `f0 9f 91 8b`; the URL held `%F0%9F%91%8B`). Removing the emoji fixed it entirely.
- Substitute BMP markers: headings `【…】`, bullets `-`, numbering `1)` / `2)`, quotes
  `「…」`, arrows `—`. All ≤ U+FFFF, render everywhere.
- Guard before building a link — fail if any codepoint is astral or an emoji selector:

  ```bash
  python3 - "$MSG_FILE" <<'PY'
  import sys
  t = open(sys.argv[1], encoding="utf-8").read()
  bad = sorted({hex(ord(c)) for c in t
                if ord(c) > 0xFFFF or ord(c) in (0xFE0F, 0x20E3)
                or 0x1F000 <= ord(c) or 0x2600 <= ord(c) <= 0x27BF})
  print("ASTRAL/EMOJI PRESENT — will tofu to ⬜/�:", bad) if bad else print("BMP-only: safe")
  PY
  ```

Tier 3 Cloud API `send` transmits real UTF-8 in the POST body and does **not** have this
problem — the mangling is specific to the Tier-1 click-to-chat deep link.

> The `link` command now enforces the emoji check itself (hard error, exit 2) and prints a
> round-trip `✓ link carries the full N-char body` line — so you rarely need to run the guard
> above by hand, but it's kept for quick pre-checks on a draft file.

## Keep Tier-1 bodies short and structurally flat

The landing-page preview is a **fixed, scrollable box**. Long or list-heavy bodies scroll out
of view and _look_ truncated, which reads as a bug to the recipient/operator even though the
link carries everything. Two of the three round-trips in the CPC ↔ {{CONTACT}} case (2026-07-04) were
this false alarm, not real defects. So, for Tier-1:

- **Keep it concise** (the CLI warns past ~700 chars). WhatsApp messages are read on phones;
  a tight 300–450-char note beats a wall of text.
- **Inline the asks as `(1) … (2) …` inside a paragraph** — do NOT start a line with a bare
  `1)` / `1.`. A line that is just `1` is the classic "message got cut at 1" preview artifact.
- **Never end a line with `——`** flowing into a numbered item — it renders as a dangling
  `-- 1`. Use a colon lead-in (`…问两件事：`) instead.
- The CLI's preflight warns on all three; treat the warnings as "fix before you hand it over".

## Anti-Patterns (NEVER DO)

| Anti-Pattern                                                                                     | Why It Fails                                                                                                          |
| ------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------- |
| Claiming a `wa.me` link "sent" the message                                                       | It only **pre-fills**; the human taps Send. Say so.                                                                   |
| Using an unofficial library (`Baileys`, `whatsmeow`, `wppconnect`) to send as a personal account | Violates WhatsApp ToS; risks number ban. Not part of this skill.                                                      |
| Passing a number without a country code                                                          | `wa.me` needs full E.164; the CLI rejects <8 digits.                                                                  |
| Free-text Cloud API send to a cold contact                                                       | Outside the 24h window only approved templates send (error 131047).                                                   |
| Hardcoding the Cloud API token in a script/commit                                                | Resolve from 1Password into env at call time (mirrors `gmail-commander`/`tlg`).                                       |
| Emoji / astral-plane chars (`👋✅❌`, keycaps) in a `wa.me` link body                            | Arrive as `�` (U+FFFD) — the deep-link handoff drops 4-byte codepoints; BMP/CJK survive. Keep Tier-1 bodies BMP-only. |

## Error Handling

| Symptom                                              | Cause                                                                                                                    | Fix                                                                                                                                                     |
| ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CLI: `too few digits`                                | Number missing country code                                                                                              | Pass full international format                                                                                                                          |
| CLI: `Cloud API send needs WHATSAPP_TOKEN…`          | Tier 3 creds absent                                                                                                      | Use Tier 1 `link`, or resolve creds via 1Password                                                                                                       |
| API `Cloud API HTTP 401`                             | Token expired/invalid                                                                                                    | Rotate the token in Meta → update 1Password                                                                                                             |
| API error `131047`                                   | Outside 24h window                                                                                                       | Send an approved template, or use Tier 1                                                                                                                |
| `wa.me` opens but shows "invalid number"             | Recipient not on WhatsApp / wrong number                                                                                 | Confirm the number with the user                                                                                                                        |
| Recipient sees `�` / diamond-`?` where emoji were    | Astral-plane emoji lost in the `wa.me`→WhatsApp deep-link decode (source UTF-8 fine; CJK survives)                       | Strip emoji from the body; use BMP markers (`【】`, `-`, `1)`). See "Message Body Encoding".                                                            |
| User reports the message "ends at 1" / looks cut off | The `api.whatsapp.com/send` gray box is a scrollable **preview**, not the message; long/list-y bodies scroll out of view | Not a bug — the round-trip `✓ carries N chars` proves completeness. Tell them to click "Continue to WhatsApp Web"; keep bodies short & inline `(1)(2)`. |

## Evolution Log

- **2026-07-04 (later) — hardened the Tier-1 path against the two failure modes above.** Added
  to `wa-cli.ts link`: (1) an **emoji/astral preflight** (hard error, exit 2) so a tofu body is
  never emitted; (2) **structural warnings** for lone list-number lines / trailing `——` /
  over-length that make the preview _look_ truncated; (3) a **round-trip check** that decodes
  the built URL and asserts it equals the input, printing `✓ link carries the full N-char
body`. Lesson baked in: on Tier-1 the agent has no view of the rendered result, so verify
  what's verifiable (round-trip) and never assert preview behavior blind. Cost that motivated
  this: one CPC ↔ {{CONTACT}} message took three user round-trips (emoji → dangling dash → false
  "truncated" preview) — all now caught before hand-off.

- **2026-07-04 — emoji tofu on the Tier-1 link path.** A zh-Hans report (CPC ↔ {{CONTACT}}) rendered
  all Chinese correctly but showed `👋 ✅ ❌` / keycaps as `�` in WhatsApp. Root cause: the
  `wa.me` → WhatsApp deep-link handoff drops astral-plane (4-byte) codepoints while BMP text,
  including CJK, survives — the source file and percent-encoded URL were both valid UTF-8.
  Fix + guard documented in the new "Message Body Encoding" section: keep Tier-1 bodies BMP-only.

- **2026-06-22 — initial skill.** WhatsApp has no personal-account send API. Modelled on
  `tlg`/`gmail-commander` conventions but split into capability tiers because the platform
  forbids the equivalent of MTProto/OAuth personal send. Default = `wa.me` link (the path
  proven in the VanJobbers ↔ CPC engagement); Cloud API send wired but credential-gated.
  CLI written as function/enum-driven Bun TypeScript per the repo language preference.

## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did the command succeed?** — If not, fix the instruction or error table that caused it.
2. **Did `wa-cli.ts` flags or output change?** — Update the Usage block to match.
3. **Was a workaround needed?** — Capture it here so the next run doesn't rediscover it.
4. **New convention learned about WhatsApp's limits?** — Add it to the tier table / window rules.

Only update if the issue is real and reproducible — not speculative.
