---
name: app-project-kickoff
description: "Use when the owner wants an app built or an old tool rewritten."
version: 2.0.0
author: coordinator role of hermes-fleet-apps
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [project, kickoff, planning, fleet, coder, designer, media, desktop, local-app]
    related_skills: [fleet-project-pipeline, hermes-agent-factory, dependency-licence-audit, git-remote-publishing]
---

# App project kickoff

The owner brings an idea ("I want an app that..."). The coordinator does NOT build
it: it vets, shapes, and dispatches. Keep the chat reply short: findings, the
decision asked, the next step.

Scope this skill was written for: local apps and tools — desktop apps, CLIs and
small local web UIs, Python first, from idea to installer and release. Online
services, mobile apps and other stacks are not covered here.

## Procedure

1. **Prior art first**, before any planning — the owner should not have to ask.
   - Search the app stores and package indexes of the target platform, GitHub
     (`api.github.com/repos/<owner>/<repo>` for stars / language / pushed_at /
     licence) and the web.
   - Report: what exists, its stack, how it gets data, where it is weak. Then a
     frank verdict: is there room, and what is the narrower angle.
   - If your web tool cannot fetch a page, use `curl -sL` and strip tags in Python.
   - When the owner already built a similar tool, name that repo as read-only
     prior art in the brief (its lessons) and fence its real data paths by name.
2. **Data sources** — prefer free / keyless APIs. For each: licence, rate limit,
   what it covers. Rate limits decide the cache design, so state them. Keep the
   vetted list in the project (e.g. `docs/data-sources.md`) so the next project in
   the same field starts from it.
   - **ML models: check the WEIGHTS licence, not the code repo's.** Pretrained
     weights often carry their own non-commercial terms while the code is MIT. See
     `dependency-licence-audit`.
   - **Unknown-at-spec engine facts (speed, thresholds, codec licences)**: dispatch
     a coder feasibility spike in a worktree IN PARALLEL with product's SPEC; its
     measured values then supersede the SPEC's assumptions (one status line in the
     SPEC pointing at the spike REPORT). Library default thresholds are often tuned
     for a different task than yours: the spike measures the case you ship.
   - **Test data with personal content** (faces, voices, private media): a separate
     coder job builds it OUTSIDE every repo, with a manifest recording source URL +
     licence per item; research-only benchmark sets are fine for measuring, not for
     shipped tests. Keep a disk cap, and keep the build script + checker in the repo
     so the set is reproducible.
   - **A product to be SOLD adds three checks before the spec**: every dependency
     allows closed-source sale (binaries bundled inside wheels carry their own
     licence → licence-audit ticket + third-party notices file); personal-data law
     where it applies (in-app notice, a delete-everything path, terms flagged for a
     lawyer); payment/licensing either specced or explicitly in "Later" with "spec
     nothing that makes adding it hard".
   - **Zero-budget distribution**: no paid signing by default. Unsigned Windows
     installers show a SmartScreen warning ("More info → Run anyway"): plan an
     illustrated guide on the download page. Ask before proposing app stores or
     certificates.
3. **Scope v1 small** — about 5 core functions and nothing adjacent. Propose the
   cut, let the owner confirm. When the owner says "all features" but also picks a
   small v1, it is not a contradiction: the SPEC lists v1 + v2 (every remaining
   capability); say so in one line instead of asking.
4. **Names** — propose 5, the owner picks. Before calling a name free: a quoted web
   search of the bare name, a search in the same field, GitHub repo search,
   `.com/.app/.io` via `https://rdap.org/domain/<d>` (200 = taken) and a fetch of any
   live site. Obvious field words are always taken. Report what each hit is; say
   trademarks were not checked. Say "verified free" only after these checks.
   Renaming later: `git-remote-publishing` → "Renaming the app".
5. **Lay out the plan** in numbered steps with fleet roles (below), then keep a
   checklist file in the repo and tick it.
6. **Ask only the decisions that change the approach** (name, v1 scope, test
   device) — in one message, then act.
   - Format: numbered questions, options inline, the recommended one marked ★,
     closing line "answer 'all defaults' + exceptions (e.g. 2b, 7c)".
   - Put pushback on the flow in the same message, before the questions: a step
     that asks the user once per item (confirm every file) becomes one ask per
     group — say how many clicks it saves.
   - An unanswered question takes its ★. Resolve factual ones (an account
     spelling) from the source of truth, not from the chat.

## Legacy rewrite (an old tool, often built with a weaker agent)

Same roles, different first steps — prior art and naming are skipped:

1. Read all source once and list the defects in plain words (settings saved but
   unused, no timeouts, UI tangled with logic). Keep the list short; it becomes the
   brief's "known bugs".
2. **Check the live data source yourself before writing the brief** (fetch the
   real page, inspect the real HTML/JSON): a bug report from the end user is a
   symptom, and the brief must state the mechanism (which field to read) or coder
   guesses. Confirm the facts the old code assumes and put them in the brief as
   "verified on <date>".
3. Phase the work: **engine first, UI second, packaging last** (an .exe of a
   terminal app is still a terminal app). When the owner asks "exe or web UI?",
   the answer is usually a local web UI on a clean engine, exe optional on top.
4. When the end user is a third party: what they praised stays byte-identical
   (folder names, layout) and the brief says "keep EXACTLY, fix only X"; what they
   asked for as a joke still goes in the queue as an optional flag.
5. Put the project under git before dispatching: commit v1 untouched as the
   baseline so the rewrite is a readable diff; new code lives in a new package
   beside the old files, untouched until the UI phase replaces them.
6. **Web UI phase brief** (after `.design/` is committed): name the read order
   (SPEC → design doc → tokens → mockups → engine modules) and say "the mockups ARE
   the spec, no design questions"; list the JSON API endpoint by endpoint with the
   error shape (no tracebacks, plain message + hint); any capability the UI needs
   but the engine lacks goes INTO the engine with tests, not into the web layer;
   stdlib server + plain HTML/JS, bind 127.0.0.1, one job at a time, a snapshot
   endpoint so a reload keeps the queue; visual check = the agent drives the real
   app and saves screenshots named like the mockups so the coordinator can compare
   side by side; an `<APP>_HOME`-style env var pointed at scratch for tests so the
   user's real settings stay untouched; packaging is a separate later job.
   - **Browser drag-and-drop never reveals file paths**: a local web UI that must
     copy or move the user's originals cannot use a dropped folder. Offer a native
     folder picker opened by the local server, or a typed path. Flag it at kickoff
     whenever the owner says "drag and drop" for a browser app.

## Later phases (references)

- **Local-AI model apps** (desktop UI over a local model: image, LLM, voice):
  `references/local-ai-app-shape.md` — engine wrapping, pinned catalogue,
  hardware-check wizard, measured thresholds, GPU-generation check
  (`scripts/cuda-archs.py`), privacy defaults.
- **Packaging** (after the web UI is verified and the owner has tried it):
  `references/windows-packaging-brief.md` — two-leg split, runtime rules,
  verification list, the coordinator's own spot-check, handover words.
- **Demo video** (media, after packaging): `references/demo-video-brief.md` —
  Facts section, real screens, local narration first, licensed music, contact
  sheet check.
- **Pre-release polish = the owner's first-run test** (before any launch video or
  push): `references/owner-first-run-test.md`. Change or remove only, no new
  features; one coder batch for the whole list, then rebuild.
- **Before the first public release**: update path, `docs/RELEASING.md`, release
  order, safe uninstall, AI-generated marker, compatibility-testing answers —
  `references/releases-updates-and-compat-testing.md`; the push itself is
  `git-remote-publishing`.

## Fleet roles (who does what)

- **coder** — builds the whole thing; may use its own subagents for parallel
  parts. Reads the official docs of each language and framework before coding.
  How to brief and dispatch it (headless run, numbered definition of done,
  liveness check, verify from disk): `fleet-project-pipeline`.
- **designer** — UI/UX, brand, logo, palette, design tokens, delivered as a plan
  in the repo's `.design/` folder that coder executes. Design is built by the
  design seat, not improvised by coder.
  - **Input is a `SPEC.md` the coordinator writes and commits first** (who the end
    user is, screens with one primary action each, rules, out of scope). Without
    it the designer invents scope.
  - Rounds are fixed in the brief: flow map → 3 directions on the same 2 screens →
    full mockup light + dark with error/empty states → lock → write `.design/`.
    One pick per round; no round reopens an earlier one.
  - If a browser review tool is used for the rounds (see `agent-fleet-design` →
    Lavish), the review page itself is the channel: the owner follows the page,
    the coordinator returns at the end to verify `.design/`. Relaying links round
    by round puts the coordinator one step behind.
  - **Owner-supplied logo or mockup = fixed input, not a direction round.** Copy it
    into `.design/reference/`, check its metadata (`/Author`) before committing,
    sample its colours into a brand-input note, and write Keep (style, layout,
    components) / Adapt (every control that breaks a SPEC rule, plus the screens
    it lacks). Present that list as "my picks, tell me if not"; the designer then
    redraws faithfully and designs only the missing pieces.
  - When the end user is not the owner, say so in the brief: a dense power-user
    look suits the owner, a less technical user needs big targets, a calm layout
    and their own language.
- **media** — presentation video and demo GIFs for the README. Consumes the
  brand, never invents it.

## Headless job hygiene (any agent, any repo)

- Put the repo HEAD in the prompt file, computed at dispatch
  (`"$(git rev-parse --short HEAD)"`), not hand-typed: a commit made between
  writing the brief and dispatching leaves a stale hash.
- Before dispatch, prove no other headless session is working on the same repo.
- On the completion notice verify from disk, never from the summary: the DONE
  marker, `git status -s` empty, `git log --oneline`, `git diff <baseline> --stat
  -- <old files>` empty when the brief said "untouched", the test suite run with a
  clean environment (unset `PYTHONPATH`/`PYTHONHOME` if your agent shell exports
  them), one real CLI call, and smoke folders gone.
- Then sweep `_job/`: move BRIEF/LOG/REPORT to a gitignored `_private/jobs/` (kept
  for the next phase's handoff), delete session logs, prompt files, markers and
  caches, and report the sweep in one line.
- A build job that stops on the compaction rule is NOT a failure: relay it to a
  fresh session via its HANDOFF; tell the owner in two lines (what the leg
  committed and verified, that a new leg is running). Never raise the threshold to
  save legs; a web UI or packaging phase taking 2-3 legs is normal.
- **Compare design vs real app yourself**: build one PNG with PIL — rows =
  screens, left = mockup, right = real screenshot, both resized to the same size —
  then one vision call: "left = mockup, right = real; per row: layout / colours /
  components match? list differences". One image, one call; delete it in the sweep.
- Report to the owner: what exists now, what the coordinator verified itself (✅
  per item), decisions the agent took alone (one line each, with a verdict), what
  was cleaned, then the next phase as a one-line question.

## Repo conventions (every project)

- `git config user.name/user.email` per repo FIRST, as a separate command: with no
  global identity, `git config user.name && ...` exits 1 and silently aborts the
  whole `&&` chain.
- `.gitignore` from day one (`venv/`, `__pycache__/`, `_job/`, `_private/`, local
  secrets such as `.env` and keystores, build output); check `git ls-files | wc -l`
  BEFORE the first commit — a committed venv means a history rewrite.
- On Windows: `git config core.autocrlf false` per repo, or every add on an LF
  project prints one warning per file.
- **Personal vs pushable, split from the first commit**: tracked files (SPEC,
  CHECKLIST, README, code) are written for a generic user — no owner name, no
  owner hardware, no local paths, no sibling projects, no names of personal files.
  Those facts go to a gitignored `_private/NOTES.md`, which briefs tell agents to
  read. Before the first push, `git log -p | grep -iE '<name>|<hardware>|<local
  path>'` must return only the author line; if personal text was committed and
  nothing is pushed yet, rewrite and `git reflog expire --expire=now --all && git gc
  --prune=now`, because a fix in a later commit leaves it in history.
- All artifacts in English (code, comments, README, commit messages), whatever the
  chat language.
- **Sizes the user reads use 1 GB = 1024^3 bytes, labelled "GB"** (what file
  managers and task managers show; a decimal "34.3 GB" for a 32 GB machine reads as
  a bug). One formatter per language that every RAM/disk/download string goes
  through, a test `34359738368 -> "32 GB"`, unknown/0 shows nothing. Internal maths
  stays in bytes; check separately what unit an engine flag expects.
- README is a deliverable: logo, short pitch, screenshots, data-source credits and
  licences.
  - **Write less.** Top = banner, 2-3 lines, screenshot; then Requirements →
    Install → First run → Features (short list) → Privacy; the technical tail
    short or moved to `docs/` with a link.
  - **Banner, logo and tagline say WHAT the app does, never the platform.**
    Platform facts live only in Requirements, stated for this release, with no
    roadmap promises.
  - Banner = a designer card, README = a docs card, same worktree, disjoint files.
- Published under the identity the owner names; commercial products may stay
  private. The coordinator prepares; the owner confirms the push
  (`git-remote-publishing`).
