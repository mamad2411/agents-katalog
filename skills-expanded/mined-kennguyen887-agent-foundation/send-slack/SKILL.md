---
name: send-slack
description: Send a Slack message to a channel or DM using the local send.js script. Use whenever the user asks to send or notify team via Slack.
---

## STOP gate — run this before the send command, every time

Loading this skill is NOT authorization to send. Before running `send.js`, **both** of these must be true:

1. **There is an actual send order, separate from any drafting.** Asking for a message, or iterating on one, is NOT it: "reply ngắn cho anh ấy", "ngắn gọn hơn nữa", "nói tôi đang fix sớm nhất", "add this line", "change the tone" all describe what the text should say — none of them says it should leave the chat.
2. **The user named the exact target** — a specific channel, a specific person to DM, or a default they name themselves ("channel mặc định", "the usual channel"). "Send it to Slack" does not name a target, and neither does the channel guide below on its own: that table tells you which channel *fits* once the user has pointed at one.

Missing either → **post the draft in chat, say which target you would use, ask, and wait.**

**Both present → send. Do not re-confirm.** Not the wording, not a version you reshaped to fit the 300-character ping format, not one where you filled in a `<Name>` placeholder, not a shorter rewrite of the same message. The send order covers the message as it needs to be formatted, and asking again after it is the failure — see the Slack rule in `~/.claude/CLAUDE.md` (Post-PR / Post-Merge Follow-up).

`send.js` has send-only scope (no `chat.delete`; `edit_slack.js` can fix the text, not the channel), so there is no undo on the *target*: a wrong channel means the user deletes it by hand in front of everyone who already read it. That is why item 2 is a gate. It is not a reason to re-litigate text the user already told you to send.

## When to use

When the user asks to send a Slack message, notify a channel, DM someone, or share a PR/update with the team.

## Command

```bash
# Send to a channel
node ~/dev/slack-watcher/src/send.js "#channel-name" "message"

# Review ping — let the tool enforce the 300-char cap (it refuses and prints the count)
printf '%s' "$MSG" | node ~/dev/slack-watcher/src/send.js --cap 300 "#channel-name" -

# DM by username
node ~/dev/slack-watcher/src/send.js "@username" "message"

# Pipe from stdin (for long messages)
echo "message content" | node ~/dev/slack-watcher/src/send.js "#channel-name" -
```

## Channel guide

| Channel | Language | Use for |
|---|---|---|
| `#general` | English | PR review requests, global announcements, external-facing updates |
| `#general-dev` | Vietnamese | Internal dev discussion, debugging, team chatter |

## Steps

1. Compose the message — English for `#general`, Vietnamese ok for `#general-dev`. PR review requests always go to `#general`.

   **Decide which of the two kinds you are writing first — the length rule differs and getting it wrong is why a message gets rewritten.**

   **(a) A ping — "please look at this."** PR review requests, deploy notices, FYIs.

   **A PR review request is HARD CAPPED AT 300 CHARACTERS — always pass `--cap 300` so send.js enforces it** (it counts code points like `wc -m` and refuses over-length instead of sending; a 304-char ping once slipped out because the count and the send ran in one command). If it is refused, cut and resend. It is the link plus **what the PR is for** — one or two sentences, no greeting and no sign-off. **The purpose is not optional padding: a ping that is only a link and a merge order is too short.** The reviewer must be able to tell what they are opening without clicking:

   ```
   Please review: https://github.com/your-org/general/pull/2212 (Next 15 upgrade for prod)
   ```

   **Break it across lines the moment there is more than one link or more than one fact** — the cap is a ceiling on words, never a reason to collapse the layout. Pass the message through stdin (`printf '%s' "..." | node ... -`) so the newlines survive:

   ```
   Please review, the CG team gets 2 emails per cashrentstimate and these merge them into 1:

   listings-api (merge first): https://github.com/your-org/listings-api/pull/755
   legacy-api: https://github.com/your-org/legacy-api/pull/395

   Prod backports:
   https://github.com/your-org/listings-api/pull/756
   https://github.com/your-org/legacy-api/pull/396
   ```

   **Every PR / issue / ticket is a full URL, one per line.** Slack links nothing else: `#493` or `legacy-api #493` is dead text the reader cannot click (2026-10-21, the COM-1154/1156 ping listed five PRs as `#493, #494` — Ken: "viết slack gì ko click vào link đc vậy"). The cap is for words, not links: when the URLs alone push a ping past 300 (five PR links ≈ 280 chars), raise `--cap` by the URLs' length rather than dropping links or the purpose.

   Everything else belongs in the PR body: the full explanation, verification, caveats, risk. Detail that changes nothing about whether someone opens the PR stays out — put it in the PR and let the reviewer read it there.

   Cap history: 1000 → 100 on 2026-08-13, after a 756-character ping; → **300 on 2026-08-14**, because 100 was too tight in the other direction. Two PR links alone are ~110 characters, so a prod+rc pair at 100 forced the *purpose* out of the message entirely and left a bare "prod first: <link>, rc #398" — Ken's words: "mẹ gì ngắn vậy, phải ghi mục đích PR là gì". 300 fits the purpose plus both links and still refuses a wall of text.

   Other pings (deploy notices, FYIs) stay under 1000 characters and follow the same instinct: link plus what happened, two or three sentences at most.

   **(b) A report that asks the reader to decide** — cost, cleanup, incident summary, anything ending in "do I have your OK". **Cap 2000 characters, and use the list form.** The cap in (a) does not apply, because here the numbers *are* the message: the reader cannot approve deleting something without seeing what and how much. Stripping the figures out to hit 1000 just means they have to ask for them.

   Style for both — `Hello <Name>,` … `Thank you.`, polite, explicit first-person `I`, scannable bullets, bold only on the total and the ask, one line for what you verified, one line for anything you deliberately did not do and why: see the Slack style rule in `~/.claude/CLAUDE.md` (Post-PR / Post-Merge Follow-up). Do not restate it here.
2. Pick the target:
   - Channel: `"#general"` (reviews), `"#general-dev"` (internal), etc.
   - DM: `"@firstname.lastname"` (match Slack username exactly)
3. Run the command via Bash tool.
4. Confirm success from the script output.

## Fix a message already sent

`send.js` cannot take a message back; `edit_slack.js` rewrites it in place (`chat.update`, own messages only, same `--cap` / allowlist guards). Fixing a bad send = edit it, never post a second "corrected" copy. Same send gate as above: the user asked for the fix.

```bash
# See which message --last resolves to (search can lag a few seconds and shows pre-edit text for a while)
node ~/dev/slack-watcher/src/edit_slack.js --dry-run --last "#general"
# Edit by permalink (exact) — prefer it once the dry run printed it
printf '%s' "$MSG" | node ~/dev/slack-watcher/src/edit_slack.js --cap 500 "<permalink>" -
```

Verify by reading the message back with `conversations.history` (search keeps the old text for a while).

## Examples

```bash
# PR review request to channel
node ~/dev/slack-watcher/src/send.js "#general-dev" "PR for review: https://github.com/your-org/legacy-api/pull/367 — adds smsOptIn field to registration and lead-message APIs for Twilio integration."

# DM
node ~/dev/slack-watcher/src/send.js "@firstname.lastname" "PR ready for your review: https://github.com/your-org/legacy-api/pull/367"

# Long message via stdin
echo "Hey team, two PRs up for review — BE changes for SMS opt-in..." | node ~/dev/slack-watcher/src/send.js "#general-dev" -
```

## Verification

Script prints confirmation or error. If it errors, check that `~/dev/slack-watcher/src/send.js` exists and the Slack token is configured.
