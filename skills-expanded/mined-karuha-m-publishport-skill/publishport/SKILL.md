---
name: publishport
description: Publish, cross-post and schedule content on social and content platforms — X/Twitter, Reddit, LinkedIn, Medium, Dev.to, Hashnode, Substack, Bluesky, Mastodon, Threads, Telegram, Tumblr, Pinterest, YouTube, TikTok, plus Chinese platforms such as Xiaohongshu (RedNote), Douyin, Bilibili, Zhihu, Weibo and WeChat — through the user's own logged-in browser via PublishPort. Also covers setting PublishPort up for the user, checking which accounts are connected, attaching images or video to a post, and confirming a post actually went live. Use whenever the user asks to post, publish, cross-post, repost or schedule content, asks to set up or connect PublishPort, asks which of their platform accounts are connected, or asks to pull back the link or stats of something they published.
license: MIT
---

# Publishing with PublishPort

PublishPort runs publishing commands **on the user's own machine, inside their own logged-in
browser**. No platform API keys, no cloud account impersonation — every action comes from the
user's real session, which is why platforms with no public write API (Xiaohongshu, Douyin,
Zhihu, WeChat…) can be published to at all.

Two rules matter more than everything else below:

- **Never guess a flag.** Ask the CLI for its schema; it is the only accurate source.
- **Never publish twice.** A command that errors may still have posted. Check, then retry.

Throughout this file, `publishport` means the official CLI. Run it as
`npx -y publishport@latest <command>`, or install it once with `npm install -g publishport`.

## 0. Setup

If you were pointed at this file to set PublishPort up, do these steps in order. If
`publishport status` already reports a credential, skip step 2.

1. **Install this skill**, so future sessions know how to publish without being sent here again:

   ```bash
   npx -y skills add https://www.publishport.app/skill.md -g -y
   ```

   It installs into every agent it detects on this machine; add `-a <agent>` (for example
   `-a claude-code`, `-a codex`, `-a cursor`) to install for yourself only. Without Node.js, save
   this file yourself as `publishport/SKILL.md` in your skills folder. In a hosted chat with no
   persistent skills folder, skip this step.

2. **Connect the user's account.**

   ```bash
   publishport login
   ```

   It prints an authorization link and a confirmation code, then exits. Give the user both, and
   ask them to open the link, sign in or create an account, check that the code matches, and
   click **Authorize**. Then run:

   ```bash
   publishport login --wait
   ```

   It returns as soon as they approve and saves the credential to
   `~/.publishport/config.json`. Exit code 3 means they have not approved yet: run it again.
   If you cannot talk to the user while a command runs, end your turn after sharing the link and
   run `--wait` when they reply. Links expire after 10 minutes; `publishport login` makes a new
   one.

   Do not ask the user to paste a token or an access address into the chat. If they already have
   one from the desktop app, `publishport login <address>` saves it directly.

3. **Check the machine side.**

   ```bash
   publishport capabilities
   ```

   It lists the user's online devices and which platforms are signed in on each. No device online
   means the user still needs the PublishPort desktop app (<https://www.publishport.app/download>),
   running and signed in with the same account. A platform shows as signed in once the user has
   logged into it in the desktop app.

Finish by telling the user what is ready and what is left for them to do.

The credential can run commands on the user's machine. Never print it, put it in a file inside a
project, or send it anywhere except PublishPort's own endpoints. In a sandbox that is thrown away
after the session, the login does not survive; `PUBLISHPORT_TOKEN` in the environment works in
its place.

## 1. Pick the channel

Publishing always goes through PublishPort's relay, which runs the command on the machine where
the user's desktop app is signed in. Two ways to reach that relay:

**a. The CLI** — the default. Every command goes through the relay, so it works whether or not
you are on the user's machine:

| What | CLI |
|---|---|
| Online devices, login state per platform | `publishport capabilities` |
| A platform's fast path plus its live `--help` schema | `publishport guide <platform> --device <d>` |
| Run one command on the device | `publishport run --device <d> -- <command...>` |
| Copy a file onto / off the device | `publishport upload` / `publishport download` |
| Anything else | `publishport call <tool> --json '{...}'` (`publishport tools` lists them) |

**b. PublishPort MCP tools are already connected** (`list_capabilities`, `local_bash`,
`publish_guide`, …) — use them instead and follow their own instructions, which are more
detailed than this file. They map one-to-one onto the CLI: `list_capabilities` =
`capabilities`, `publish_guide` = `guide`, `local_bash` = `run`, `prepare_upload` /
`read_local_file` = `upload` / `download`.

If neither works — no Node.js and no MCP tools — stop and tell the user what is missing.
Do not substitute scraping, headless logins, or unofficial platform APIs.

**Do not reach for a locally installed `ppcli` and run it yourself**, even when the desktop app is
on the same machine and you can see the binary. The relay is what resolves which device to run on,
checks login state, and keeps the run accounted for; going around it silently drops all three, and
breaks the moment the user's agent moves off that machine.

Everywhere below, `ppcli <platform> …` means *run that command through your channel* — as
`publishport run --device <d> -- ppcli <platform> …` on the CLI, or `local_bash` on MCP.

## 2. Publish

1. **Confirm the account.** `ppcli auth status` lists login state per platform, but it is cached
   and can be stale — before a real publish run `ppcli <platform> whoami`. If that reports
   `AUTH_REQUIRED`, ask the user to sign in again in the desktop app instead of pushing ahead.
2. **Read the real schema.** `publishport guide <platform> --device <d>` returns the fast path plus a
   one-line index of the platform's subcommands; for the full parameters of the one you need, run
   `ppcli <platform> <command> --help` (over MCP, pass `command` to `publish_guide`). Required arguments
   differ per platform (some need a cover image, a topic, a category id). Fill in every required
   argument deliberately; defaults are rarely what the user wants.
3. **Stage the content as files.** Put the body on the device first —
   `publishport call write_local_text --json '{"device":"<d>","path":"post.md","content":"…"}'`,
   or `write_local_text` over MCP — then pass it with `--file` (or the command's own
   `--<name>-file`). Never inline a long body in the command line: quoting breaks on the first
   apostrophe, and long multi-line text gets truncated on Windows. Media the user's machine does
   not already have goes over with `publishport upload` / `prepare_upload`.
4. **Show the user what you are about to post** — the text, the target platform, and the account —
   and get a yes before the first publish of a session. After that, a summary per post is enough.
5. **Run one command per action.** Give uploads a generous timeout (video can take minutes):
   `--timeout-ms` on the CLI, `timeout_ms` on MCP — the default is 300 s, which a large video
   upload can exceed. `publishport run` waits for long commands itself. On MCP a command that runs
   longer than about 45 s returns `[STILL_RUNNING]` with a handle instead of a result: call
   `local_bash` again with `wait_for=<handle>` (no `command`) to collect it, and never resend the
   command itself. If you need to wait between steps, wait in a separate command rather than
   chaining with `&&`.
6. **Verify.** Use the returned URL or id, or re-query the platform's own listing, and hand the
   user a link they can click. A publish is not done until you have seen it exist.

Cross-posting the same piece to several platforms means repeating steps 2–6 per platform: length
limits, required media and tag rules genuinely differ, so re-read each one's schema instead of
reusing the previous argument set.

## 3. When something goes wrong

- **A publish command failed or timed out.** Do not re-run it. Query the platform's latest posts
  or the user's profile first; only publish again once you have confirmed the content is not
  there. Blind retries are the number one cause of duplicate posts.
- **Missing media.** If the task needs an image or video and none was provided, say so and stop.
  Do not go looking through the user's disk for something that might fit.
- **Browser commands keep timing out** (even `whoami`): retry once with `--site-session ephemeral`
  before the subcommand. If everything still times out, ask the user to restart the desktop app.
- **The relay says there is no device online.** The desktop app is closed or signed out. Ask the
  user to start it; do not look for a local fallback.
- **The CLI says it is not logged in, or the credential is invalid.** Run the login steps in
  section 0 again; the user may have revoked it from their account page.
- **The platform is not in the list.** Say so plainly. The catalogue of supported platforms is
  public at <https://api.publishport.app/api/registry>, and the account only works for platforms
  the user has actually signed into.

## Pacing

These are the user's real accounts, on platforms that do police automation. Publish at a human
rhythm — space posts out, don't fire the same text at a dozen accounts on one platform, and don't
work around a rate limit or a cooldown by retrying in a loop. If a platform pushes back, report it
and stop; getting the account restricted costs the user far more than a delayed post.
