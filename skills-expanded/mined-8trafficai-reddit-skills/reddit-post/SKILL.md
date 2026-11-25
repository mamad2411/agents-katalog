---
name: reddit-post
description: >
  Post and comment on Reddit from an agent, through the user's own logged-in Chrome, and verify the
  submission actually survived moderation instead of trusting the HTTP 200. Use whenever someone
  wants to post to Reddit, submit a thread, leave a comment, reply to a thread, publish to a
  subreddit, or automate Reddit posting from a script or agent — including phrasings like "post
  this to r/X", "reply to this Reddit thread", "draft and publish a Reddit post". Also use when a
  Reddit write is failing: 403 errors, a "Prove your humanity" interstitial, an expired session, a
  flair-required rejection, or a post that returned success but is missing from the subreddit. This
  skill contains the diagnosis path for all of those. Single account only — the user's own. Not for
  read-only Reddit research, and not for operating multiple accounts.
---

# Posting to Reddit from an agent

Reddit writes fail for agents in ways that look like bugs but aren't. The naive approaches — a
scripted HTTP client, or Playwright/Puppeteer launching its own browser — hit walls no amount of
retry logic fixes. Understanding why saves a long debugging spiral.

## The architecture, and why

`rdtx` attaches over CDP to a Chrome **the human launched**, and issues writes as same-origin
`fetch` calls from inside the logged-in page. Three measured facts make that the right shape;
`references/browser-session.md` has the evidence.

**The automation flag is set at launch, not by attaching.** Puppeteer and Playwright pass
`--enable-automation`, setting `navigator.webdriver = true`. Start Chrome with *only*
`--remote-debugging-port` and attach afterwards, and it stays `false`.

**"Prove your humanity" is transient.** It's a JS proof-of-work that self-resolves in seconds, not
a block. `rdtx` polls through it. Concluding you've been blocked is the most common way to abandon
a working setup.

**Let the page build the request.** Writes reuse Reddit's own cookies and CSRF material verbatim,
so there's no auth protocol to reimplement or keep in sync.

## Setup, once

Live commands require Node.js 18+, `agent-browser`, and the user's own logged-in Chrome profile;
see `references/browser-session.md`. The synthetic verifier needs only Node.js 18+.

```bash
node scripts/rdtx.mjs launch    # Chrome with a debug port, no automation flags
node scripts/rdtx.mjs login     # the human logs in by hand
node scripts/rdtx.mjs doctor    # cdp / challenge / login, reported separately
```

`rdtx` never handles the password. `doctor` reports each layer independently, so a failure tells
you which one broke.

## Verify the installed runtime without Reddit

Run `node scripts/verify-synthetic.mjs` with no arguments. It starts the production `submit` CLI
without `--yes`, checks the real temporary audit entry and both `remote_checks`, and arms guards
that fail if the CLI tries to reach a network or `agent-browser`. It also exercises the other
shared Reddit contracts with fabricated fixtures. A pass proves the local dry-run boundary only;
it does not authorize or prove a real Reddit write.
Overall `passed` is the AND of all five shared checks; inspect `functional.reddit_post` for this
skill's evidence.

An independent tester can submit the exact named verifier result through the
[structured installed-run report](https://github.com/L4A-ai/reddit-skills/issues/new?template=reddit-skill-installed-run.yml).
Select the `reddit-post` zero-input synthetic option only after running the installed copy. This
proves installation and local contract behavior, not a live Reddit write.

## Commands

| command | what it does | writes? |
|---|---|---|
| `doctor` / `launch` / `login` | session setup and diagnosis | no |
| `requirements <sub>` | flair, rules, gates — check **before** posting | no |
| `read <permalink>` | post + comments + visibility state | no |
| `submit <sub> <title> --text\|--url` | create a post | **yes** |
| `comment <permalink\|tN_id> <text>` | comment or reply | **yes** |
| `me` / `inbox` | karma totals, replies and mentions | no |
| `audit` | every write attempted or executed | no |

## Every write is a dry run unless you pass `--yes`

```bash
node scripts/rdtx.mjs submit test "My title" --text "Body"        # prints a plan, posts nothing
node scripts/rdtx.mjs submit test "My title" --text "Body" --yes  # actually posts
```

An agent composing a post will often run the command just to inspect the payload. A tool that
posts on first invocation turns that into a public, hard-to-undo action. The dry run returns the
requested payload so the subreddit, title, body, URL, and requested flair can be confirmed before
anything leaves the machine. It is fully local: no browser command or Reddit request is made, and
both entries in `plan.remote_checks` report `not_run`. Both dry runs and real writes append to
`~/.rdtx/audit.jsonl` with `executed: true|false`.

## Flair is required in most large subreddits

```bash
node scripts/rdtx.mjs submit ClaudeAI "Title" --text "Body" --flair "Skills" --yes
```

After explicit `--yes` confirmation, `submit` resolves flair by name and checks
`is_flair_required` **before** the write request, so a missing flair fails before Reddit creates a
post. A wrong name returns the subreddit's actual flair list. The default dry run deliberately
does not perform either remote check; it reports the requested flair for review instead.

## A 200 is not proof — this is the part people miss

Large subreddits route new posts through AutoMod, where they sit reachable by direct link but
absent from listings and marked non-indexable. The write returns 200 and reads back perfectly.

Measured on a real post, minutes apart, before and after a moderator approved it:

```
removed_by_category: "automod_filtered"   →   null
is_robot_indexable:  false                →   true
```

`submit` re-reads after writing and reports the result:

```json
"visibility": { "state": "automod_filtered", "public": false, "indexable": false }
```

States are `live`, `automod_filtered`, `not_indexable`, `removed`. Treat anything other than `live`
as not published yet, and **wait rather than reposting** — reposting to escape a filter converts
one filtered post into a spam pattern across the account. Pass `--no-verify` to skip the check.

## Image posts

Image upload works, but only through a **trusted** path. Two things had to be true, and both were
found by failing first:

**Synthetic events are ignored.** Setting `input.files` from page JavaScript sticks on the element
and shreddit's Lit component never reacts; a dispatched `DragEvent` is ignored the same way. The
API route is closed too — `/api/media/asset.json` 403s under modhash, `X-CSRF-Token`, a
`csrf_token` field, and all combinations. What works is `DOM.setFileInputFiles` over CDP, which the
page cannot distinguish from a human choosing a file.

**Most of the file inputs are decoys.** The composer keeps ~7 mounted at once as placeholders for
the other post types, and `setFileInputFiles` **succeeds silently against the inert ones** — the
command returning is not evidence of anything. Only the input with `accept="image/*"` actually
holds the file. `image-post.mjs` sweeps every candidate and keeps whichever ends up non-empty.

```bash
# stage everything, submit nothing (default)
node scripts/image-post.mjs test "My title" --image ./a.png,./b.png

# actually post
node scripts/image-post.mjs test "My title" --image ./a.png --flair "Skill Share" --yes
```

Title goes in via `Input.insertText` after a real `Input.dispatchMouseEvent` click, and Post is
clicked at its measured coordinates — all trusted, all through Reddit's own composer, so there is
no write protocol to reimplement.

**Gotcha: Reddit persists composer drafts.** Images staged in an earlier session are still there
when you navigate back, so a post can go out with more images than you passed. Check the returned
`n` against what you supplied, or clear the draft first.

Image **link** posts remain available and need none of this — `submit --url <image-url>` renders
with a preview.

## Choosing a target when testing

Use `r/test` or the user's own profile subreddit (`u_<username>`). Both exist for this and affect
no community. Proving a setup against a real topical subreddit spends the user's account standing
on a smoke test.

## Pacing

A jittered ~2.3–8s wait precedes each write, keeping you inside Reddit's rate limits. For many
writes, spread them out rather than removing the pacing — Reddit's "You are doing that too much"
costs more time than the waits.

## Scope

**One account — the user's own.** No multi-account, proxy-rotation, or fingerprint-spoofing
support, and none is planned: that targets platform integrity detection rather than getting your
own posting to work, and Reddit's terms prohibit it. If a task seems to need several accounts
looking like unrelated people, raise it with the user rather than engineering around it.

## Troubleshooting

| symptom | cause | fix |
|---|---|---|
| `cdp_reachable: false` | Chrome not started with a debug port | `rdtx launch` |
| title is "Prove your humanity" | transient JS challenge | wait — `settle()` retries |
| `logged_in: false` but status 200 | session expired; an exported cookie file rots in ~a day | `rdtx login` |
| `flair_required` error | subreddit demands flair | `--flair "<text>"` |
| 200 but missing from the subreddit | AutoMod filtered it | check `visibility`; wait for a mod |
| `errors: [["RATELIMIT", …]]` | posting too fast | wait the stated interval |

## Related

- `reddit-seo` — audit whether existing posts are indexable
- `reddit-archive` — capture a post with its media
