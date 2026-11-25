# Genex publishing in AI Game Studio

You are building inside AI Game Studio. Below the upstream marker is Genex's publishing card,
with the passages of advice Studio does not ship taken out. Where it disagrees with this preface,
this preface wins.

- Publishing is one step: `genex__publish {"operation":"gallery"}` exports the game, updates its
  draft page and makes that same build the public version (`npx genex publish` the first time,
  `preview` then `promote` after). Use it when the user wants the game published or online.
  `npx genex preview` alone is `genex__publish {"operation":"draft"}`: an unlisted test build that
  leaves the public version as it is. Each asks the user first and returns a job: follow it with
  `genex__publish-status {"operation":"wait","jobId":"<jobId>"}`, then give the user the operation’s
  reported link verbatim: `galleryUrl` for a public release, `draftPlayUrl` for a draft. Do not
  construct a URL or report a draft link as the public release. If the job has not succeeded,
  report its actual state rather than claiming publication.
- A draft's link to share and test is `draftPlayUrl`, the draft build's own address
  (`preview--<slug>`): anyone with it plays the draft, as a guest or signed in, in rooms apart from
  the live game. `draftUrl` (`<dashboard>/draft/<slug>`, the card's "your game's page") is the
  owner's draft page and asks for their sign-in: never give it as the place to play or test.
- Studio exports and uploads the game itself. Glue step 3 (the CLI as a dev dependency) and
  `init --convert` do not apply, and `npx genex pull` is not available. Glue steps 1 and 2 still
  apply; for step 2 read `genex__skill {"name":"genex-threejs-embed-auth"}`.
- Studio does not pass on the CLI's preflight lines. `warnings` in `genex__publish-status` carries
  lines about the game's Genex cover instead (no picture sent, a picture refused or not sent, a
  picture too small or not 16:9).
- The card's opening ("The user built this game themselves", "as it is") describes a game whose
  code its owner keeps untouched, such as a folder they brought and asked only to publish.
- The game's Genex cover is the picture kept with `genex__cover` (the `cover` skill). Publish sends
  it once the upload is recorded and takes no picture of its own; with none kept and none the owner
  chose on genex.games, Genex keeps the cover it has.
- `npx genex doctor` is `genex__cli {"command":"doctor"}`. Other commands map onto Studio tools as
  the `genex` skill describes (`genex__skill {"name":"genex"}`).

<!-- upstream @genex-ai/cli-demo/templates/skills/genex-tool-publish/SKILL.md v1.40.0 sha256 5374af3bbaca06cb48605fd67e88a252624beaa27c97c952b9bc6f03f1a4595e -->
---
name: genex-tool-publish
description: Put the game in this folder on the web with Genex — the draft page, `npx genex preview`, then `promote` / `publish`; the link you hand the user, the size limits, and what to do with the preflight lines. Installed once the folder is connected to a hosted Genex game (`npx genex init --convert`). Load it before the first preview.
---

# Genex Tools · Publish

The user built this game themselves and asked for it online. Your job is to
put it there **as it is** — the code, the structure and the assets stay
exactly what they are. Publishing adds glue and nothing else; it never starts
a rework, a design document or a build plan.

## The glue (all of it)

1. **A static build.** The game must build to files with its own build
   command — `npm run build` into `dist/`, or an `index.html` at the root
   with no build step. Asset paths must work from the game's own hosted URL,
   so prefer relative ones (Vite: `base: './'`). Files the game loads at
   runtime — everything in `./assets` — must end up inside the build (Vite:
   a `public/` folder, or copy `assets/` into `dist/` in the build).
2. **Player identity.** Load `$genex-threejs-embed-auth` and add the one
   `initEmbed(...)` call at the very top of the boot code. On a hosted
   page `waitForPlayer()` takes seconds to resolve.
3. **The CLI as a dev dependency** so plain `npx genex` keeps resolving here
   (setup already did this; check `package.json` if in doubt).


## Preview

```bash
npx genex preview
```

Builds, uploads and puts the build on the game's **draft page** — unlisted,
only the user can open it. The dev server forgives paths the hosted build will
not.

**The link is always the game's page on Genex, never the raw play address,
never localhost, never a file path:**

- draft: `<dashboard>/draft/<slug>`
- public, once published: `<dashboard>/<slug>`

`<dashboard>` is the first `dashboardOrigins` entry in `.genex/project.json`
and `<slug>` is the `slug` there. `preview` prints the exact page link as
"your game's page" — use that line verbatim.

## Draft and public version

`preview` updates the **draft** and never touches what players are on. The
first release lists the game:

```bash
npx genex publish --categories games
```

Pick 1–3 categories that fit (`games`, `assets`, `physics`, `terrain`,
`lighting`, `vfx`); `games` when unsure.

After that first release the game is two versions, and the user only ever
hears these two words for them: the **draft** (updated by `preview`) and the
**public version** (what everyone plays). "Publish it", "update it" and "yes"
after the first release ALL mean:

```bash
npx genex promote      # the exact draft build goes public — no rebuild
```

Never run `publish` a second time (it would ship an untried rebuild). If
anything changed since the last `preview`, preview again before promoting.

## Limits and refusals

- **Upload size**: ~95 MB per file, ~500 MB in total. Over that, tell the user
  plainly which part is too large (usually a video, model or audio file) and by
  roughly how much; ask before compressing or removing anything.
- **Terms refusal**: the CLI prints a link, waits for the user's click and
  re-sends by itself — hand the link over and let it finish.
- **`preview` says the folder is behind another machine** (`stale_source`):
  `npx genex pull` takes the newer draft, then redo the change — never
  `--force` over somebody else's work.
- **`promote` or `publish` says the page shows the game's Mac/Windows/Linux
  app** (`native_page_would_be_replaced`): the game ships as desktop apps, and
  this web build would replace the page that offers them. Nothing changed. Ask
  the user whether this folder really is the game's web version; only on a
  clear yes, re-run the same command with `--replace-native-page`. A web
  version that went up by mistake comes off with `npx genex web remove --yes`
  (the apps stay).
- **Out of credits or a lane down**: `npx genex doctor` says which; publishing
  itself costs nothing.
