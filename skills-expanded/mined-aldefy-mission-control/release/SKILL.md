---
name: release
description: Ship a mission-control release end to end - test main, bump the version, release notes, tag and GitHub release, npm publish (the owner runs it), then refresh the release media - README and website screenshots, the walkthrough video, the ronincrew.dev/mission-control page - and draft the Slack post. Use when the user says "release", "ship x.y.z", "cut a release", "new version", "update the website / video / screenshots for this release", or "/release".
---

# Release mission-control

One release touches four places. Do them in this order; each step says what needs the owner.

```text
main (tested) -> release PR (version, ROADMAP, README) -> tag + GitHub release -> npm (owner)
              -> media: screenshots + video -> README PR + ronincrew.dev deploy -> Slack draft
```

Ask once at the start, unless the user already said: the version (patch for fixes only, minor when there are features), and which parts to run (default: all). Never ask again for each step.

## Rules that cost time when skipped

- Work in **clean worktrees** of `origin/main` (`git worktree add --detach <scratch>/rel origin/main`). The owner's checkout is often on an old branch with untracked files: never build, release or record from it.
- The **ronincrew** repo (`~/StudioProjects/ronincrew`) usually has the owner's uncommitted work. Commit only the files you changed (`git add <paths>`), then build and deploy from a clean worktree of that commit. Never `npm run deploy` in the main checkout, or the work in progress ships.
- **Merges, tags and publishing are the owner's.** Open PRs and say the merge command; merge only when the user says "merge". `npm publish` needs a one-time password: the owner runs it in a regular terminal (the `!` prompt cannot open the browser login). If it returns `E409 ... previously staged version`, the browser flow already published it: check the registry before trying again.
- **No real data in media.** Only the synthetic demo, staged by `scripts/media/stage-demo.mjs`. The shot and video scripts fail on local paths; also look at every still for real project names before publishing.
- Long lines get split when the owner pastes commands: give each command on its own short line, or put long ones in a script file and give `sh <file>`.

## 1. Test main

```bash
npm ci && npm run typecheck && npm run build && npm run test:server && npm run test:web
npm pack --dry-run
```

Then a read-only smoke run of the build on a spare port against the owner's real sessions (GET routes only, notifications stay off): `/api/overview` counts, `/api/items` open/closed and `resume`, `/api/settings` defaults. A headless pass over Home, a session page, the sidebar and the tour at 1440x900 and 1280x800 catches layout regressions the tests miss (v2.5 shipped one: titles squeezed to 0px by hidden row icons).

## 2. Release PR

On a `release/<version>` branch: `npm version <version> --no-git-tag-version`, a "Done in v<x.y>" section in ROADMAP.md (credit contributors by name), README updates for new pages, states, settings and write routes (the Security section lists every write route and every command the server runs). Open the PR; CI runs on Node 20.19, 22 and 24.

## 3. Tag, GitHub release, npm

After the owner merges:

```bash
git fetch origin && git tag v<version> origin/main && git push origin v<version>
gh release create v<version> --verify-tag --title "v<version>: <one line>" -F <notes.md>
```

Release notes: what it does for the user in one opening line, an install block, a "v<x.y>" list in plain sentences, credits, and a Security paragraph for anything that writes outside `~/.mission-control` or runs a new command. Show the notes to the owner before creating the release.

npm, for the owner, from a clean checkout of the tag:

```bash
git checkout v<version> && npm ci && npm publish --access public
```

Check with `npm view @aldefy/mission-control version --prefer-online` (a plain `npm view` or `npm install` can read a stale cache for a few minutes).

## 4. Media

Stage the demo in one terminal (it stays up; Ctrl-C stops everything it started):

```bash
node scripts/media/stage-demo.mjs --port 4570
```

Screenshots (README and website both come from these):

```bash
node scripts/media/shots.mjs <scratch>/shots
```

The walkthrough video (about 80 s, silent, 1920x1080). The scenes are the v2.5 walkthrough in `scripts/media/video/director.mjs`: add or edit scenes for the release's new features first (each scene is a `mark()`, a caption via `cap()`, and clicks via `clickEl` / `camGo`). Then:

```bash
MEDIA_OUT=<scratch>/video node scripts/media/video/director.mjs
MEDIA_OUT=<scratch>/video node scripts/media/video/assemble.mjs info
MEDIA_OUT=<scratch>/video node scripts/media/video/assemble.mjs stills 5 15 25 35 45 55 65 75
MEDIA_OUT=<scratch>/video node scripts/media/video/assemble.mjs render
```

Look at the stills (a contact sheet: `ffmpeg -pattern_type glob -i 'stills/*.jpg' -vf scale=640:-1,tile=3x3 sheet.jpg`) before rendering. Known traps, each worth a retake if missed:

- A raw CDP `Enter` key goes to headless Chrome's own UI and backgrounds the page: the screencast freezes. Click buttons instead.
- The recording zooms the page with CSS `zoom: 1.25`; the director already fixes `100vh` for that. If the sidebar footer looks cut off, that fix is missing, not an app bug.
- The phone frame (`/remote.html` in an iframe) needs ~1.5 s before anything reads it, or its mock never installs.
- Renames and pins from an earlier take persist: restart `stage-demo.mjs` between takes.
- Mocked in the page, by design, and to be said in the post: the sidebar settings values (the demo hides Start at login), the phone page's `/api/remote/*`, and the drawn notification banner.

Poster and frame 0: take a settled frame (the hook at ~2.6 s) as `poster.jpg` and replace frame 0 with it (concat the poster with `trim=start_frame=1` of the video) so thumbnails show it.

Web versions for the site:

```bash
sh scripts/media/encode.sh <brag.mp4> <poster.jpg> <scratch>/shots <scratch>/site
```

## 5. Publish the media

- **README:** copy the PNGs into `docs/screenshots/` (and the poster as `docs/screenshots/demo-poster.jpg`), fix the demo link's length ("Watch the N-second demo"), open a PR.
- **ronincrew.dev/mission-control:** copy `mission-control-1080.mp4`, `mission-control-720.mp4`, `poster.jpg` and the six WebP shots (home, run-lanes, run-map, calls, timeline, usage) into `public/mission-control/`. Update the caption length in `src/app/mission-control/page.tsx`, the video's `aria-label` in `src/components/DemoVideo.tsx`, and any screenshot `alt` text that no longer matches. Commit only those paths, then from a clean worktree of that commit: `npm ci && npx next build && npx wrangler deploy` (Turbopack refuses a symlinked `node_modules`). Verify the live files' byte sizes match.

## 6. Slack

Draft (never send) the #self-promo post with the Slack connector: the owner's voice from earlier posts there (a hook, plain full sentences, short bold heads, the npx line, links, an ask for feedback). Tag contributors only after resolving their Slack user id. Tell the owner to attach the video file from the scratch dir.

## Done when

Registry `latest` is the new version, the GitHub release is Latest, the README and ronincrew.dev show the new media, and the owner has the Slack draft. Remove every worktree and stop `stage-demo.mjs`.
