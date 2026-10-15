---
name: artifact-cafe
description: >
  artifact.cafe is the home for AI-generated work: publish interactive static
  artifacts (HTML apps, dashboards, mockups, reports, slides, docs) to a review
  URL that humans open with no login and comment on directly — pinning feedback
  to elements and text. Authors then publish new immutable versions. Use when
  asked to "publish this for review", "share this for feedback", "put this
  online for comments", "get review on this", "ship a preview", "make a review
  link", "publish an artifact", "send this to a reviewer", or "publish v2".
---

# artifact.cafe

**Skill version: 0.11.0**

artifact.cafe hosts static artifacts for **review**. One loop:

```
publish a folder → review URL → guest comments (no login) → publish v2
```

It is not a general hosting platform. It hosts self-contained static
artifacts (an `index.html` plus assets) so a human can open a link, comment
by clicking elements or selecting text, and the author can iterate.

To install or update: `npx skills add artifact-cafe/skill --skill artifact-cafe -g`
(drop `-g` for a repo-local install).

This file is the always-loaded manual. Deeper playbooks ship next to it in
`./references/` (organizing the library, the live-editing loop, access and
sharing) — each section below says when to read which; read them at that
moment rather than up front.

## When to reach for this

- The user has built something visual/interactive and wants **feedback** on it.
- They want a **shareable link** a non-technical reviewer can open and mark up.
- They're iterating: publish, collect comments, publish the next version.

If they just want raw file hosting with no review loop, this isn't the tool.

## Requirements

- **Preferred:** Node / `npx` (every major agent host has it). Nothing to install
  ahead of time — `npx artifact-cafe@latest` fetches the CLI on demand.
- **Fallback (no Node):** `bash`, `curl`, `jq`, and `shasum`/`sha256sum`. Use the
  bundled `./scripts/publish.sh`.

## Staying up to date

- **Always invoke the CLI as `npx artifact-cafe@latest …`** (as every example
  here does). The `@latest` tag makes npx fetch the newest published CLI on
  each run instead of reusing a stale cache — that *is* the CLI auto-update.
- The CLI checks for updates (at most once per day) and prints
  `[artifact-cafe] …` notices on **stderr**; they never pollute `--json`
  stdout. When you see `Skill update available`, run the command it prints —
  `npx skills add artifact-cafe/skill --skill artifact-cafe -g` (drop `-g`
  for a repo-local copy) — then re-read the updated SKILL.md before
  continuing. Don't ask permission for this refresh; it only rewrites this
  skill's own files.

## Publish (preferred path)

Run from the skill-invoking session, pointed at the folder to publish:

```bash
npx artifact-cafe@latest publish ./my-artifact --title "Onboarding redesign"
```

The folder must contain an entry `index.html` at its root (or pass `--entry`).
Assets (CSS, JS, images, fonts) sit alongside it and are uploaded together.

**Always pass `--title` — generate one yourself, don't wait to be asked.** Infer
a concise, human-readable title (3–6 words) from the artifact's own content: its
`<title>`, main heading, or evident purpose. The title is shown on the review
page **and becomes the readable review-URL slug** (e.g.
`artifact.cafe/a/onboarding-redesign-a1b2c3`). Skipping it yields "Untitled
artifact" and a random slug, so only omit it when you genuinely can't infer one.

**Write version notes on every publish with `--notes`.** These are a changelog
for this version, shown in the review page's **Versions** panel. Rules:

- **Bullet points only** — one line per change, no prose paragraphs.
- **One bullet per change. Do not compact big changes into a single bullet** —
  if you shipped three meaningful things, that is three bullets, not one.
- Keep each bullet short and concrete ("Added dark-mode toggle", not "misc UI").
- Pass them as a newline-separated string; `$'…\n…'` is the reliable shell form:

```bash
npx artifact-cafe@latest publish ./my-artifact --title "Onboarding redesign" \
  --notes $'- Added dark-mode toggle\n- Fixed nav overlap on mobile\n- Rewrote pricing copy'
```

On **v1** the notes describe the initial build; on **v2+** they describe what
changed since the previous version.

Options:

```bash
--title "Onboarding redesign"   # RECOMMENDED — review-page title + URL slug; generate one by default
--notes $'- Added X\n- Fixed Y' # RECOMMENDED — bullet-point changelog for this version (see below)
--description "One line"        # share-card summary; overrides the entry HTML (see below)
--entry index.html              # entry file (default: auto-detect)
--artifact art_xxx              # publish a new version to an existing artifact
--workspace acme                # explicit team workspace
--folder specs                  # folder in that workspace — SETS VISIBILITY, see below
--review off                    # plain artifact: no review tools (see below)
--json                          # machine-readable output (use this for agents)
--no-open                       # don't try to open a browser
```

**Leave review open unless the user asks otherwise.** Getting comments back is
the point of publishing here. `--review off` gives a plain artifact with no
review layer at all — right when the user wants a deliverable, demo, or
portfolio piece rather than feedback, and only when they've said so.
`--review readonly` keeps existing comments readable and refuses new ones.
Either can be changed later, with the publish token and no account:

```bash
npx artifact-cafe@latest review readonly   # close it to new comments
npx artifact-cafe@latest review open       # reopen it
```

Comments are never deleted by this and come back when review reopens.

**`--folder` decides who can open the review link.** A folder carries a
visibility (`public` or `workspace`) and the artifact inherits it on publish.
Land in a `workspace` folder and the review URL stops being a link anyone can
open — it asks for a sign-in, and only members of that workspace get through.
Without `--folder`, a new artifact is `unlisted`: anyone with the link, no
account. So discover the folder's visibility first with
`npx artifact-cafe@latest folders --workspace <handle> --json`, and say so
before you publish anywhere that isn't `unlisted`. Filing is still the
default — see "Keep the library organized".

`publish --json` reports the result as `visibility`
(`public` | `unlisted` | `workspace` | `private`) — read it and tell the user
what the link they're about to send actually does. See "What to tell the user".

On the **first** publish of a new folder the command prints a **review URL**
and a **claim URL** (shown once). It writes `.artifactcafe/config.json` with the
artifact id and a secret publish token, and gitignores it.

Decide the destination **before** the first publish — see "Choose where to
publish" below. Always use `--json` and report its `destination` and
`destinationSource` fields.

## Make the shared link unfurl right

When the review URL is pasted into X, Threads, Slack, Telegram, or Discord, the
preview card is built from the artifact. By default it is a generated
artifact.cafe card whose copy is about reviewing. That fits a dashboard you
want feedback on. It reads wrong for anything meant to be read.

**Put these in the entry file's `<head>` whenever you build something to be
read rather than reviewed** (an article, a report, a guide, a comparison):

```html
<meta name="description" content="One line on what this is.">
<meta property="og:image" content="cover.png">
<meta name="author" content="Ada Lovelace">
```

The API reads them at publish time, so this works from every path: the npm CLI,
the bash fallback, and a raw API call. `og:description` and `article:author`
are accepted too. Skip all three and the link behaves exactly as it always has.

The image is the part with rules, all enforced server-side:

- **It must be a file inside the folder you publish.** `cover.png`,
  `./cover.png`, and `/assets/cover.png` all work. A remote URL, a
  protocol-relative URL, and a `data:` URI are refused outright.
- PNG, JPEG, WebP, or GIF, under 5 MB. 1200x630 is the right size. No SVG.
- Anything refused quietly falls back to the generated card. Nothing breaks,
  and the description and byline still ship.

`--description "…"` overrides whatever the entry file declares. Reach for it
when the document's own meta description is not the sentence that belongs on a
timeline.

**A gated artifact declares nothing.** Password-protected, workspace, and
private artifacts always unfurl as the locked card whatever their tags say, so
there is nothing to set there.

## Choose where to publish (do this before a new artifact)

This applies to the **first** publish of a new folder. A new *version* reuses
the destination already recorded in `.artifactcafe/config.json` — skip all of
this and just `publish` again. Resolve the destination in this priority order:

**1. Check login first.** Run `npx artifact-cafe@latest whoami --json`.

- **Logged in** (exit 0): publish under that account. A logged-in user should
  never land on an anonymous, 24-hour artifact by accident — that is the bug
  this order exists to prevent. Note that keys resolve **per origin** and
  `ARTIFACT_CAFE_URL` selects the origin: if `whoami` fails for the origin you
  are about to publish to, the account key won't apply to the publish either —
  surface that (they're logged out for this origin) instead of silently
  publishing anonymously.
- **Not logged in** (non-zero exit): publish directly. This is an **anonymous**
  artifact — it expires in 24h and returns a one-time claim URL. Tell the user
  it's anonymous, and that `artifact-cafe login` first gives a permanent,
  account-owned artifact instead.

**2. Then pick the workspace (logged-in only).** If the user named an explicit
`--workspace`, or a project `artifact-cafe.json` default applies, use it and
don't ask. Otherwise list the account's workspaces with
`npx artifact-cafe@latest workspaces --json` and choose:

- **Only Personal** (no team workspaces): publish to Personal, no question.
- **Personal plus team workspaces**: do not silently default to Personal. Look
  at what the artifact is about; if its evident subject matches one of the
  user's workspaces (e.g. planning for a "hellyeah" product when a `hellyeah`
  workspace exists), **ask** the user whether to publish to that workspace or to
  Personal, then pass `--workspace <handle>` accordingly.

Content is only a hint for *what to ask* — never silently commit an artifact to
a workspace you guessed from its content; the user's choice decides. `--json`
disables the CLI's own interactive workspace picker, so a logged-in agent that
skips this step defaults straight to Personal — which is exactly why you run
these two checks yourself.

## Keep the library organized (folders)

Every workspace — Personal included — has a **flat** list of folders (no
nesting). Filing is part of publishing well: place each artifact at publish
time instead of leaving everything in one unfiled pile.

**3. Pick a folder (after the workspace, before the first publish).** Once the
workspace is decided, list its folders:

```bash
npx artifact-cafe@latest folders --workspace <handle> --json
```

- If an existing folder clearly matches the artifact's subject, publish with
  `--folder "<name>"` (exact name, case-sensitive — or the folder id). Match
  on meaning, not string equality — a "Specs" folder is the home for a new
  spec even if no words overlap.
- If nothing fits, leave the artifact unfiled rather than forcing a bad
  match. Create a folder (`folders create "<name>" --workspace <handle>`)
  only when a real group exists — **never for a single artifact** — and
  reuse before creating: the CLI refuses a duplicate name; treat that as
  "use the existing folder".
- **⚠ A folder's visibility becomes the artifact's.** Publishing or moving
  into a `public` folder makes the artifact public, with no confirmation
  prompt anywhere — confirm with the user before any public placement, and
  report every visibility change (see "--folder decides who can open the
  review link" above).
- Re-file without republishing: `npx artifact-cafe@latest move --folder
  "<name>"` (`--artifact <id>` to target one, `--unfiled` for the root). No
  new version; comments untouched.

**When the user asks you to organize their library** ("organize my
artifacts", "clean up my workspace"), read `./references/organize.md` first
and follow its plan-first flow — never bulk-move or bulk-create without
showing the plan. It also has the folder-creation rules, naming guidance,
and `move`/`list --workspace` details. Folder commands need the Node CLI
and a signed-in account; the bash fallback can't manage placement.

## Publish without Node (fallback)

The same static publish pipeline, pure bash — for environments where `npx`
isn't available:

```bash
./scripts/publish.sh ./my-artifact --title "Onboarding redesign"
```

It supports `--title`, `--entry`, `--artifact`, `--json`, and `--no-open`,
speaks the same API, and writes the same `.artifactcafe/config.json`. Workspace
discovery, project defaults, and the human picker require the npm CLI. If a
new artifact has an `artifact-cafe.json` policy, the fallback refuses instead
of silently publishing to a different destination.

## Publish a new version

Versions are **immutable** — a new publish never mutates an existing version,
and comments stay attached to the version they were made on. To ship v2, just
publish the same folder again from the same directory:

```bash
npx artifact-cafe@latest publish ./my-artifact \
  --notes $'- Moved the CTA above the fold\n- Tightened hero spacing'   # → v2, v3, …
```

**Pass `--notes` describing what changed since the last version** — a new
version with no changelog leaves reviewers guessing what to re-review.

The stored publish token in `.artifactcafe/config.json` authorizes the new
version automatically. From a fresh checkout that lacks the token, set
`ARTIFACT_CAFE_TOKEN` (the publish token) or target it with `--artifact <id>`.
If you're logged in, `artifact-cafe link --artifact <id>` binds the folder to
one of your own artifacts (or `link --json` to list them first) so later
commands run bare — no token needed, owner actions use your login.

## Pull comments

The read side of the loop — what reviewers said, so the agent can address it:

```bash
npx artifact-cafe@latest comments            # open threads on the current version
npx artifact-cafe@latest comments --json     # structured, for programmatic handling
./scripts/comments.sh                 # no-Node fallback
```

Filters: `--status open|resolved|all`, `--version current|all`. Each thread
carries its author, the version it was made on, the anchor (a quoted text span
or an element path), the message body, and replies. Address the feedback,
publish the next version, then close the loop with `reply`/`resolve` (below).

Both the CLI and the fallback also accept `--artifact <id>` (or
`ARTIFACT_CAFE_ARTIFACT_ID`) to read an artifact without its folder — the same
detached targeting as `publish`; add `ARTIFACT_CAFE_TOKEN` for a
password-protected one.

## Respond to comments

The write side of the loop — how the agent answers feedback after publishing a
version that addresses it. Take each thread's `id` from `comments --json`:

```bash
# Post what changed back into the thread, then close it — one step
npx artifact-cafe@latest reply <threadId> --body "Fixed in v2 — CTA moved above the fold." --resolve

npx artifact-cafe@latest reply <threadId> --body "…"     # reply, leave it open
echo "$msg" | npx artifact-cafe@latest reply <threadId>  # long body from stdin
npx artifact-cafe@latest resolve <threadId>              # close a thread you addressed
npx artifact-cafe@latest reopen <threadId>               # undo — reopen a resolved one
```

A publish-token reply is attributed to **the agent**: the reviewer sees
"Yulong's Claude" with your tool's mark — your name for yourself (detected, or
`--as "Claude Code"`) joined to the artifact's owner. Replying under a signed-in
account renders as the owner instead, with the tool as a "via" label. Prefer `reply --resolve` over a bare `resolve` —
it tells the reviewer *what* you changed instead of silently closing the thread.
Same detached targeting as the rest (`--artifact <id>` + `ARTIFACT_CAFE_TOKEN`,
or your account key); every command takes `--json`.

Fix or retract a message you wrote — take the id from `comments --json` (each
thread's `messageId` for its opening comment, each reply's `id`):

```bash
npx artifact-cafe@latest edit <messageId> --body "Revised — moved the CTA, not removed it."
npx artifact-cafe@latest delete <messageId>
```

You can only edit or delete a message **you** authored — a token-authored agent
reply, or your own account comment; the same credential that wrote it authorizes
the change. `edit` adds an "edited" marker (no history). `delete` is a *soft*
delete: the comment becomes a "Comment deleted" tombstone and any replies under
it survive.

## Open a review thread

`reply` answers an existing thread; `comment` **opens a new one** — for leaving
your own review notes on an artifact:

```bash
npx artifact-cafe@latest comment --quote "Where AI work lives" --body "This headline is vague."
npx artifact-cafe@latest comment --body "Overall this reads well."   # page-level, no --quote
```

Unlike the rest of the loop, `comment` authors as **your account**, so it needs
`artifact-cafe login` — a publish token can't open threads (agents respond;
accounts originate) and returns a login hint if that's all you have. `--quote`
anchors the thread to matching text (`--prefix`/`--suffix` disambiguate a quote
that repeats); with no `--quote` it's a page-level comment. `--as "Claude Code"`
sets the label shown after your account name — additive, never a mask, and
detected from your environment when you leave it off.

`comment`, `edit`, and `delete` (like `listen`) need the Node CLI — no bash
fallback.

## Offer live editing mode (opt-in)

Publishing and live editing are separate actions. After publishing and sharing
the review URL, ask the user whether they want to enter **live editing mode**:
you stay attached to the local artifact, receive new comments as they arrive
(`npx artifact-cafe@latest listen --json --timeout 540`), revise, and publish
new immutable versions while they review.

**Do not start live editing mode automatically.** A user may want to share the
link and collect feedback asynchronously without keeping an agent session
active. After a clear yes, read `./references/live-editing.md` and run the
loop it describes (listen → edit → publish → `reply --resolve` → listen). When
`listen` exits `2` (timeout), tell the user the listening window ended and ask
whether to continue before running it again — never keep an unattended session
alive indefinitely.

## Open the review page

```bash
npx artifact-cafe@latest open     # prints (and, in a terminal, opens) the review URL
```

## Local config and the publish token

After the first publish, the folder holds:

```text
.artifactcafe/config.json
```

```json
{
  "artifactId": "art_…",
  "slug": "…",
  "url": "https://artifact.cafe/a/…",
  "apiUrl": "https://artifact.cafe",
  "publishToken": "apt_…"
}
```

- The `publishToken` is a **secret**, returned once, that authorizes publishing
  new versions to this artifact. **Never print it, never commit it, never log
  it.** The CLI stores it chmod 600 and adds `.artifactcafe/` to `.gitignore`.
- Treat `config.json` as internal linkage state, not a URL. Never present the
  local file path to the user as if it were the review link.

## Who can open the review link

Every artifact has a **visibility**: `public` and `unlisted` open for anyone
with the link, no account (`unlisted` — random, unguessable slug — is the
default for a new artifact); `workspace` stops non-members at a sign-in;
`private` admits only the publisher, the workspace's owner/admins, and people
invited by email. A new artifact takes its folder's visibility if it lands in
one. **The CLI cannot change visibility** — there is no `--visibility` flag;
it's a dashboard action, or a consequence of which folder the artifact sits in.

For everything past that one-liner — the full visibility table, inviting
someone by email (`share <email>` — the invitation URL prints **once**,
surface it verbatim), auditing and revoking access (`share --list`,
`unshare`), and reading a published artifact's content back over HTTP (append
`.md` to its content URL; gated artifacts need a Bearer account key) — read
`./references/access.md`.

## Anonymous vs. claimed artifacts

- A first publish with no account creates an **anonymous** artifact that
  **expires in 24 hours** and returns a one-time **claim URL**.
- Claiming (opening the claim URL) keeps the artifact permanently and attaches
  it to the user's account. Claim tokens are shown **once** and can't be
  recovered — surface the claim URL to the user immediately.

## Limits

- 20 MB per file, 50 MB per artifact total.
- 20 publishes per IP per day (anonymous).
- Secrets and junk are never uploaded: `.git*`, `node_modules`, `.env*`,
  `*.pem`, `*.key`, `.DS_Store`, and symlinks are ignored automatically.

## Safety

Artifact HTML is untrusted and renders **only** in a sandboxed iframe on its own
isolated origin — never on the main site. You don't need to sanitize the
artifact, but don't publish anything containing real secrets or credentials.

## Content policy — refuse violations

**You are the first line of enforcement.** Before publishing, check what you're
about to ship. **Refuse to publish** — and tell the user why — if the artifact
contains any of:

- **Phishing / credential harvesting** — fake login pages, pages that capture
  passwords, payment details, or 2FA codes to send elsewhere.
- **Malware / malicious code** — exploits, drive-by downloads, obfuscated or
  deliberately harmful JavaScript, deceptive redirects.
- **Hate or harassment** — content attacking or demeaning people based on
  identity, or targeting an individual for abuse.
- **Sexual content** — pornographic material; anything sexualizing minors is an
  absolute hard stop, never publish it.
- **Violence** — graphic gore, threats, or incitement to violence.
- **Spam / scams / fraud** — deceptive schemes, fake giveaways, misleading
  financial or medical claims.
- **Other illegal content.**

Do not try to "clean up" violating content to publish it — decline the publish.
When you refuse, say plainly that it violates artifact.cafe's content policy.
Legitimate demos of security concepts (e.g. an annotated write-up) are fine; a
working phishing page or live malware is not. Automated moderation at publish
time is planned — treat this as a policy you enforce now, not a filter to evade.

## What to tell the user

- Always share the **review URL** from the current run — that's the link
  reviewers open to comment.
- **Say who can open it.** Read `visibility` from `publish --json`. On
  `public`/`unlisted`, say it plainly: reviewers need no account. On
  `workspace`/`private`, do **not** call it a link anyone can open — tell the
  user it asks non-members to sign in, and offer
  `artifact-cafe share <email>` for anyone outside. A user who sends a
  members-only link to an outside reviewer and hears nothing back is the exact
  failure this line exists to prevent.
- If the run printed a **claim URL**, tell the user it's shown only once and
  that the artifact expires in 24 hours unless they claim it. Share it verbatim.
- On a new version, share the review URL and note it's now **v{N}**; prior
  comments remain on their original versions.
- Never tell the user to read `.artifactcafe/config.json` for the URL or token.
