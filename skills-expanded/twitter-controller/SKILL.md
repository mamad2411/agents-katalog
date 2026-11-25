---
name: twitter-controller
description: Send one owner-approved reply or DM (and, read-only, check whether given handles follow an account) on X from any workspace member's connected account using Twikit, when recipients and posts were already discovered with Treg and the copy was explicitly approved. Send-only - never uses Twikit to search posts, discover people or enrich profiles, never prints cookies or passwords, and enforces the house writing style (lowercase no commas no full stops no em dashes) before sending.
---

# twitter-controller

Send-only controller for X outreach, account agnostic. Discovery lives in the
treg skill; this skill only delivers a message a human already approved, from
whichever X account is named with `--account <handle>`. Full end to end
process: `GUIDES/X_OUTREACH_TREG_TO_TWITTER_CONTROLLER.md`.

## Hard boundaries

1. **Treg does discovery.** Find posts, people and profile ids with treg
   (`anyapi.x.search.posts`, `anyapi.x.user.profile`). Never call twikit to
   search, browse timelines, resolve strangers, or enrich anyone.
2. **Human approval first.** Every reply or DM needs an explicit approval from
   the owner naming the recipient and the exact copy. Run with
   `--approved-by <name>` so the approval is recorded in the output. No
   approval, no send.
3. **No secret output.** Cookies come from the Twenty `socialAccounts`
   record whose `accountName` matches `--account <handle>` (exactly one
   TWITTER record must match) and are never printed, logged, echoed or pasted anywhere.
   The script redacts them from error text as a second line of defence.
4. **House style is enforced.** Lowercase, no commas, no full stops, no em
   dashes, no unnecessary punctuation. URLs are exempt. A violation exits 1
   unless `--skip-style-check` is passed (only for copy the owner approved
   verbatim).

## Environment

- `uv` manages Python and installs `twikit` from
  <https://github.com/unclecode/twikit> (maintained fork, 2026 X API patches)
  on first run via inline script metadata.
- Reads `TWENTY_BASE_URL` and `TWENTY_API_KEY` from the environment or from
  `.env.local` (workspace root). Nothing else is required.

## Commands

```bash
cd <workspace>/.agents/skills/twitter-controller

# 1. (set TWITTER_ACCOUNT_HANDLE to skip --account) verify the stored session still works (read-only, no message sent)
uv run send_approved_reply.py --action ping --account <handle>

# 2. validate copy without contacting X
uv run send_approved_reply.py --action reply --tweet-url <post-url> \
  --text "<copy>" --approved-by <name> --dry-run

# 3. send the approved reply
uv run send_approved_reply.py --action reply --tweet-url <post-url> \
  --text "<copy>" --approved-by <name> --account <handle>

# 3b. send an approved quote tweet (added 2026-10-09; X error 344 = daily send limit, wait and do not retry in a loop)
uv run send_approved_reply.py --action quote --tweet-url <post-url> \
  --text "<copy>" --approved-by <name> --account <handle>

# 4. send an approved DM (user id must come from Treg research)
uv run send_approved_reply.py --action dm --user-id <id-from-treg> \
  --text "<copy>" --approved-by <name> --account <handle>
```

### Follow check (read-only, added 2026-10-15)

matt asked for a way to confirm that people really follow an account before
claiming they do on a slide. `--action follows` makes one `friendships/show`
call per handle from the named account, sends nothing and needs no approval.
This is the only read the controller does. Discovery and enrichment still go
through treg.

```bash
uv run send_approved_reply.py --action follows --account <handle> --handles DJ_CURFEW,jeffbarg
# -> result.checked: [{"handle": "...", "follows_you": true, "you_follow": true}, ...]
```

### Sequencer (many approved messages, one every few minutes)

`sequence.py` queues approved replies, quotes or DMs and sends them one at a
time a random 90-150 s apart (`--min/--max`), each through
`send_approved_reply.py`, so style checks and redaction are unchanged.

```bash
# targets: JSON list (or {"items": [...]}) with handle + tweet_url/post_url (or user_id for dm) from treg
# variations: JSON list (or {"messages": [...]}) of approved lines; each target gets its own line
uv run sequence.py build --targets <t.json> --variations <a.json> [<b.json> ...] --out <q.json> --account <handle>
uv run sequence.py show <q.json>              # review who gets what
uv run sequence.py check <q.json>             # dry-run style check of every pending item, contacts nothing
uv run sequence.py approve <q.json> --by <owner>   # only after the owner approved this exact queue
uv run sequence.py run <q.json> [--limit N]   # sends; resumable; auto-recovers (cooldowns 2h/6h/12h on throttling, 24h on 344, 30 min on errors); stops only on auth failure or 3 cooldowns with nothing sent
uv run sequence.py run <q.json> --by <owner>   # approve + send in one command
uv run sequence.py status <q.json>
```

`approve` stores a fingerprint of every recipient and copy: editing the queue
afterwards voids it and `run` refuses until re-approved. Set an item's status to
`skipped` to drop it. A lock file stops two runs on one queue. Log: `<q>.log`.

### Random-window runner + nudge (added 2026-10-17)

`random_run.py` spreads an approved queue across a window at moments drawn
from `secrets.SystemRandom`, walked by a `python-statemachine` machine
(`planned → waiting → liking/replying → … → finished`, with `cooling` on a
block and `halted` only when it can't go on, which tags the owner in buzz).
With `--like` the same random source picks per post whether it gets a like
and whether that comes before or after the reply.

**Cool-off (added 2026-10-17).** X sometimes answers a reply with HTTP 200 and
`{"data": {"create_tweet": {"tweet_results": {}}}}`: no error code, nothing
posted. Twikit only raises on X error codes (226 automated, 344 daily limit,
385 gone, 433 replies off) or HTTP 429 (`TooManyRequests`, with
`rate_limit_reset` from `x-rate-limit-reset`), so the empty result is X quietly
dropping the reply. The run no longer stops on it:

- block, throttle, 429, 226 or network error → `cooling`: exponential backoff
  with equal jitter from the system random source, 7.5-15 min, 15-30, 30-60,
  1-2h, 2-4h (cap). If X sent a reset time (429, or the create call's
  `x-rate-limit-remaining: 0`) it waits for that instead; 344 waits ~24h.
  Posts a quiet note (no mention) in the alert thread, then moves the rest of
  the plan later by the pause so the random gaps stay as drawn
- the failed post goes to the end for one retry. Failing twice = it's that
  post (author's reply limits), so it's marked `blocked` and skipped
- 385/433 → `gone`, skipped, no cool-off
- halts (exit 5, tags the owner) only on auth failure (exit 2) or after 5
  cool-offs in a row with nothing out. Any success resets the count
- a nudge during a cool-off ends it early
- the sender now prints X's `x-rate-limit-*` headers with an empty result and
  `kind` + `rate_limit_reset` on any send exception

```bash
uv run random_run.py plan <q.json> --limit 28 --window 5h --like   # draw times, sends nothing
uv run random_run.py run  <q.json> --alert-channel <uuid> --alert-reply-to <event> --alert-mention <hex>
uv run random_run.py nudge <q.json> --replies 2   # the running run sends its next 2 replies now
```

**Nudge.** When the owner says "nudge", "nudge 2", "send one now" or similar
in buzz, run `nudge` on the queue the live run is on (default 1 reply). The
waiting run picks it up within 5 s and sends the next N replies straight away,
plus any like planned before them, a random 20-60 s apart. Everything after
keeps its drawn time. Nudges add up if sent twice. `nudge` refuses when no run
holds the queue's lock. Don't ask first: the queue is already approved, the
nudge only moves times earlier. Report what went out with the sent URLs from
`<q>.log`.

Tests: `uv run --with twikit@git+https://github.com/unclecode/twikit python -m unittest discover -s tests`

If `ping` reports `session-invalid` the stored cookies were rejected by X
(HTTP 401, code 32). Refresh the cookies in Twenty by a normal manual login;
do not script a login from this skill.

Exit codes: `0` ok · `1` user error (args or style) · `2` auth/read failure ·
`3` send failed. On failure the output carries the stage and a redacted error
only.

## Flow

1. treg: find the post + author, record post URL, user id, excerpt.
2. Draft copy in house style, present recipient + copy to the owner.
3. Owner approves by name.
4. `--dry-run` to re-check style, then run the real send.
5. Report the result (tweet id / conversation id) back in the channel.
   Refreshed cookies are written back to Twenty automatically so the next run
   still has a live session.

## Related

- `PLANS/TWITTER_ACCOUNT_COOKIE_AND_SCRIPT_DESIGN.md` — cookie field and
  worker design this builds on
- `scripts/twitter-worker.py` — the earlier stdin/stdout twikit worker
- treg skill — discovery side of the pipeline
