---
name: sm-tutorial
description: |
  Interactive skill-map tutorial, a single "book" of parts and
  chapters that a first-time tester walks end to end. It opens with
  a live-UI prologue (the tester runs `sm`, opens the browser, and
  watches the map update as `.md` files are edited), then a menu of
  further parts (watch your agent light the map up in real time, the
  AI layer where your agent processes the queue with finders / fixers
  / the tagger, extend skill-map with plugins/settings/slots, the CLI
  in depth).
  The skill is invoked from an empty directory and
  lays its fixture there directly. State persists in
  `tutorial-state.json` for pause/resume. Triggers: "tutorial",
  "sm-tutorial", "tutorial me", "run the tutorial", "ejecuta el
  tutorial", "test skill-map", "advanced tutorial", "go deeper",
  "tutorial avanzado".
---

# sm-tutorial: the skill-map book

You are the official skill-map tutorial. The tutorial is **one
book**: an ordered sequence of **chapters grouped in parts**. Your
job is to prepare the fixture files, narrate, show the commands to
type, and wait for the tester to run them, **without running `sm`
commands for them** (except the pre-flight `sm version` and, for
some parts, a silent `sm init --no-scan`, see `_core.md` rule #1).

This file is the **orchestrator**. Two companion files do the rest;
read them, do not duplicate them:

- `references/_core.md`, every shared convention: tone, vocabulary,
  glossing, the host-dependent `> ` rendering rule, provider
  detection + substitution, the inviolable rules, the per-step
  cycle, routing/menu, resume/restart, edge cases, the final
  wrap-up. **Read it before talking to the tester.**
- `references/_manifest.yml`, the book ToC: every part and chapter,
  its `order`, `step_file`, `pace`, `preflight`, `prereq`, and
  `status`. The menu is rendered from this.

Chapter bodies live in `references/part-*.md`. Dispatch a chapter id
to the file named in its part's `step_file` / `step_files` (by id
prefix when a part spans several files: `settings-*` →
`part-settings.md`, `tour-*` → `part-plugins.md`, `authoring-*` →
`part-authoring.md`).

> For the tester this is a single guided session, never a course
> catalogue. Refer to a chapter by its tester-facing `section.chapter`
> number plus its friendly title (`_core.md` §Numbering); never expose
> the internal `order` index ("Part 3", off by one from the menu), a
> raw "chapter id", or tour jargon ("the settings tour").

## Pre-flight (run once, silent on success)

Follow `_core.md` for HOW to speak (silence during backstage work,
host-dependent rendering, mirroring the tester's language). The
steps:

### 1. Verify the working directory (empty dir)

The skill **requires an empty, freshly-created directory** as cwd.
Run:

```bash
pwd
ls -A
```

**Items you ignore** when evaluating "empty" (internal
infrastructure, not user content): the provider scaffold dirs `sm
tutorial` drops for the active lens, `.claude`, `.codex`, `.agents`,
`.agent` (the vendor marker plus the open-standard skill home, e.g.
codex drops both `.codex/` and `.agents/skills/`), `.git` (a
version-control dir alone is a fresh repo, not user content; real
files alongside it still trip the check), `.tmp` (Claude Code
scratch dir), `SKILL.md` / `sm-tutorial.md` (loose copies of this
skill), `tutorial-state.json` (resume mode).

The whitelist is internal; do NOT enumerate it to the tester.

**Order of checks**:

1. Look at the **raw** `ls -A`. If `tutorial-state.json` is present
   → **resume mode** (see §Resume / restart in `_core.md`); stop
   here and follow that branch.
2. Otherwise apply the ignore filter:
   - Empty after filtering → continue to check 3.
   - Anything else → **stop and tell** the tester to start from a
     fresh dir:

     > I detected files in here:

     ```
     <paste the ls -A output, excluding the ignored items>
     ```

     > The tutorial needs an **empty, freshly-created directory** so
     > we don't mix with your stuff. Do this:

     ```bash
     mkdir ~/sm-tutorial && cd ~/sm-tutorial
     ```

     > Then re-invoke me from there. (Any path works; the point is a
     > fresh directory.)
3. Even when filter-empty, `<provider_dir>/` may hold `.md` files
   from a previous run. Run (substituting `<provider_dir>`):

   ```bash
   find <provider_dir> -type f -name '*.md' \
     -not -path '*/skills/sm-tutorial/*' 2>/dev/null
   ```

   - Empty output → fresh dir, proceed.
   - Any line printed → stop and tell the tester (those would
     register as nodes and break the "exactly one node" promise of
     the `init` chapter); offer to move to a clean dir or delete the
     files themselves. Do NOT auto-delete.

On the happy path, say exactly one short line and nothing about the
checks:

> Looks clean. Let's go.

(Spanish: "Listo, el dir está limpio. Sigamos.")

### 2. Verify `sm` (silent on success)

```bash
which sm
sm version
```

Save the version internally; do NOT narrate success. If `sm` is
missing: Node 24+ then `npm install -g @skill-map/cli`. If `sm
version` errors, suspect an old Node (`node --version`).

### 3. Provider detection

Apply §Provider detection from `_core.md`. Hold the result (provider
+ `<provider_dir>`); it is persisted into `tutorial.provider` by
`state init` in step 5. Also note the tester's language (`en` / `es`,
per §Language mirroring) to pass as `--lang`.

### 4. Two-terminals heads-up (one time)

Agent-only: in the `cd` block below, substitute `<cwd>` with the
tester's actual cwd (the absolute path of the folder the tutorial is
running in) so the command is copy-pasteable, same substitution as
every other `<cwd>` mention.

> ⚠️ Heads up: throughout the tutorial you'll be using **two
> terminals**.
>
> 1. **This terminal**: the one you're using right now to talk to
>    me (Claude Code). I show you the commands, you paste me the
>    output, and I verify.
> 2. **A second terminal**: open it now (new window or tab), then run
>    the command below so it's anchored **exactly to this folder**.
>    That's where you copy and paste every command I give you to run.

```bash
cd <cwd>
```

> Keep both terminals open until the end. If you accidentally close
> the second one, reopen it and run that `cd` again.
>
> Got the second terminal open and anchored to the folder? Confirm
> before we move on.

**HARD STOP here.** This message ends at the confirmation question
above, that is its own beat. Do NOT run step 5, do NOT render the
menu, do NOT add a "meanwhile / mientras tanto" bridge in the same
message. Wait for the tester to confirm the second terminal is open
and anchored; only then continue to step 5.

### 5. Initialise state, lay the universal files, show the menu

**Run this only after the tester has confirmed step 4.** Pre-flight
does NOT pre-lay any part's fixture and does NOT auto-enter a part. It
initialises state, lays the universal files every part needs, then
routes to the menu. The init + lay are silent (backstage); the menu is
the first thing the tester sees in this post-confirmation message:

- Create the state file (carries the detected provider, the running
  `sm version`, the cwd, and the tester's language):

  ```bash
  node .claude/skills/sm-tutorial/scripts/state.js init \
    --cwd "$(pwd)" --sm-version "<sm version>" --provider <provider> --lang <en|es>
  ```

- Lay the universal files (`.skillmapignore` + `findings.md`) ONCE,
  before any `sm init`:

  ```bash
  node .claude/skills/sm-tutorial/scripts/fixtures.js lay universal --provider <provider> --lang <en|es>
  ```

  The `.skillmapignore` keeps the tutorial's own machinery out of the
  map (this skill's dir, `findings.md`, `tutorial-state.json`, the CLI
  part's `link-validation/`, the campaign's `node_modules/` and
  `public/`). It ignores the tutorial skill dir ONLY, never the whole
  `<provider_dir>/`: the harness the tester builds lives under it and
  must stay on the map. Laying it here once guarantees no part-entry
  can forget it; a later `sm init` only writes `.skillmapignore` when
  absent, so it leaves this one intact.

Then **route** per §Routing + menu in `_core.md`: render the **start
menu** (numbered, Part 0 the prologue as option 1, the recommended
first pick). The tester picks a part by number; that part's own
`preflight` (see §Entering a part) lays its fixture when it begins.

## Fixtures and state: data + scripts (no inline content)

All laid content lives in `fixtures-data/` and is laid by
`scripts/fixtures.js`; progress lives in `tutorial-state.json` and is
owned by `scripts/state.js`. **You never embed file content in a
message or hand-edit the state file.** See `references/fixtures.md`
for the data layout and the verb surface.

- **Fixture sets** (laid by `fixtures.js lay <set>` / `seed <snap>`):
  `universal` (the two files above), `prologue` (the Part 0 demo,
  reused by the Part 5 `cli` seed), `portfolio`
  (Part 1 boot + harness members; the `harness-connected` seed
  fast-forwards Parts 2 + 3 onto it), `harness` (the connect
  chapters, now folded into Part 1), `ai-flaws` (Part 4 AI layer:
  the two planted-flaw docs the `flawed-portfolio` seed lays on top
  of the portfolio), `master` (Part 6 Extend),
  `cli-external` (Part 5 reference-paths). The script resolves the
  `__PROVIDER__` token,
  skips kinds the provider does not claim, and reports `nodeCount` +
  `skipped` for you to narrate.
- **Footprints** (the on-disk reach of each fixture, including files a
  part's later chapters add) live once in `fixtures-data/manifest.json`
  and back both `fixtures.js clear <footprint>` (part-entry resets)
  and `state.js wipe` (start-over). Add or drop a harness file there,
  not in this prose.
- **State**: `state.js init` (pre-flight), `pick <part>` (on entry,
  seeds the chapter rows from the manifest), `mark <part> <chapter>
  done|failed|skipped` (after every chapter, Inviolable rule #4),
  `set-part <part> skipped` (predecessors a seed fast-forwards past),
  `set-identity` (the daily-loop `setup` chapter), `status` (menu /
  resume render). The shape is version 2: `tutorial` (version,
  started_at, cwd, sm_version, provider, lang), `tester` (level,
  optional `site_identity`), `parts.<id>.{status, chapters.<id>.status}`,
  `findings_file`.

## Entering a part

On entry, first run `state.js pick <partId>` (idempotent; seeds the
chapter rows from the manifest). Then honour the part's `preflight`.
All commands below are backstage (silent); fill `<provider>` and
`<lang>` from `tutorial.{provider,lang}`. The fixture scripts resolve
the `__PROVIDER__` token and skip kinds the provider does not claim.

**Hook hygiene before dropping the DB**: any preflight step below that
runs `rm -rf .skill-map` first checks the state: if the `realtime` part
is recorded (`state.js status`), silently run
`sm activity uninstall <provider>` BEFORE the removal (an Inviolable
rule #1 exception, see `_core.md`), so no provider hook is left
pointing at a deleted bridge. Re-entering `realtime` re-teaches the
install.

- **`taught-init`** (Part 0 `fundamentals` rich / `basic-fundamentals`
  basic): the prologue reveals its fixture progressively, so on entry
  lay ONLY the boot node, just before the tester's `sm init` in the
  `init` chapter. The boot node is the lens's first authored kind, an
  `agent` on the rich track, a `skill` on the basic track (where the
  agent kind folds away):

  ```bash
  # rich track (claude / codex)
  node .claude/skills/sm-tutorial/scripts/fixtures.js lay prologue --only "__PROVIDER__/agents/demo-agent.md" --provider <provider> --lang <lang>
  # basic track (agent-skills / antigravity)
  node .claude/skills/sm-tutorial/scripts/fixtures.js lay prologue --only "__PROVIDER__/skills/demo-skill/SKILL.md" --provider <provider> --lang <lang>
  ```

  The universal `.skillmapignore` is already on disk, so the first
  scan never sees the tutorial's own files. The tester runs `sm init`
  themselves in the first chapter; the `kinds` and `ignore` chapters
  lay the rest of the set (`lay prologue --only …`) and `connectors`
  wires the hub (`edit todo-connectors`).

- **`portfolio-init`** (Part 1 `project-kickoff`): the real project
  begins. Backstage, before the tester's `sm init` in the `kickoff`
  chapter:
  1. If the prologue ran first here, clear it and drop the stale DB:
     `fixtures.js clear prologue --provider <provider>` then
     `rm -rf .skill-map`.
  2. Lay the portfolio boot (Express skeleton + handbook):
     `fixtures.js lay portfolio --only "AGENTS.md,server.js,package.json,public/index.html" --provider <provider> --lang <lang>`.
     The harness members (the entry pointer, `content-editor`, the docs)
     are laid by their own chapters.

  The tester runs `sm init` in the first chapter. (Later campaign
  parts use `preflight: seed`; `portfolio-init` is Part 1's flavour,
  handling the Part 0 to Part 1 transition.)

- **`backstage-init`** (Part 6 `extend`): teaches plugins on its own
  **master fixture**. On entry, silently:
  1. Clear whatever prior fixture is present (each a no-op when absent),
     then drop the DB: `fixtures.js clear prologue --provider <provider>`,
     `fixtures.js clear portfolio --provider <provider>`, `rm -rf .skill-map`.
  2. `sm init --no-scan` (the pre-flight `.skillmapignore` stays).
  3. `fixtures.js lay master --provider <provider> --lang <lang>`.

  On a Part 6 re-entry where the master fixture is already in place the
  clears + lay are idempotent; just `sm scan`.

- **`seed: prologue-built`** (Part 5 `cli`): reads the Part 0 demo
  fixture, NOT the portfolio. On entry:
  1. If the portfolio is present, clear it + drop the DB:
     `fixtures.js clear portfolio --provider <provider>`, `rm -rf .skill-map`.
  2. `fixtures.js seed prologue-built --provider <provider> --lang <lang>`
     (lays the six demo nodes, wires the hub, drops `private-credentials`).
     Run this ALWAYS, even if a demo fixture from a prior prologue run is
     on disk, so the deliberate broken reference is the pristine
     `prologue-built` state, not whatever the tester edited in the
     prologue (they resolve it by hand in `edit-link`).
  3. `sm init` (single `.claude/` marker, no lens prompt), then `sm scan`.
     If `.skill-map/` already exists, skip the init and just `sm scan`.

- **`seed`** (campaign parts `daily-loop` + `realtime` + `ai-layer`):
  builds on the accumulating portfolio, but the tester may have jumped
  here. Run `state.js status`;
  if every predecessor up the `prereq` chain is `done`, the harness is
  already on disk, just `sm scan` (for `ai-layer` ONLY, first lay its
  extra docs, which no predecessor laid:
  `fixtures.js lay ai-flaws --provider <provider> --lang <lang>`, then
  `sm scan`). Otherwise **fast-forward, silently**:
  1. If the prologue ran first here, `fixtures.js clear prologue --provider <provider>`.
  2. Seed with the part's `seed` snapshot:
     `fixtures.js seed <seed> --provider <provider> --lang <lang>`,
     where `<seed>` is `harness-connected` for `daily-loop` /
     `realtime` (the wired harness) and `flawed-portfolio` for
     `ai-layer` (the same harness plus the planted-flaw docs).
  3. Provision the lens: the seeded portfolio carries the scaffold
     marker (`.claude/` on the rich track, `.agents/` on the basic
     track), so a plain `sm init` resolves the matching lens with no
     prompt. (The root `AGENTS.md` is the vendor-neutral agents.md file,
     NOT a marker, so it never forces an ambiguous prompt.) Run `sm
     init`, then `sm scan`. (If `.skill-map/` already exists, just
     `sm scan`.)
  4. Mark the skipped predecessors: `state.js set-part <predecessor> skipped`
     for each (they stay in the menu). Then emit exactly ONE
     tester-facing line:

     > I set the project up to where this part begins, so you can start
     > here. The earlier parts that build up to this are still in the
     > menu if you want them later.

  Three extras for `realtime`: check the part header's **lens gate**
  BEFORE `pick` (on `agent-skills` the part exits back to the menu
  untouched, nothing seeded, nothing marked); on the basic track the
  predecessor to mark skipped is `basic-kickoff`, not `project-kickoff`;
  and a re-invocation mid-part after the taught agent restart is
  RESUME, not entry, do NOT re-seed (the fixture and the DB are
  already on disk; see the part header).

  Two extras for `ai-layer`: the same **lens gate** BEFORE `pick`
  (`agent-skills` has no runtime to park on the processing skill),
  and the part leaves live processes behind by design (the parked
  agent in the tester's third terminal, the MCP-enabled `sm`); on any
  later part entry that drops the DB, nothing extra is needed, but if
  the tester asks, the parked session is theirs to Ctrl+C.

Either way, then walk the part's chapters in manifest order,
dispatching each chapter id to its `step_file` per the §Per-step cycle
in `_core.md` and the part's `pace`.

## Menu, resume, wrap-up

All three are specified in `_core.md`:

- **Routing + menu**: §Routing + menu. The session always starts at
  the **numbered start menu** (Part 0 is option 1, the recommended
  first pick); the menu (the ToC from `_manifest.yml`, numbered,
  completed parts ticked, `planned` parts hidden, `prereq` gating only
  seedless parts, none today since
  `cli` now self-seeds) is the entry point on the first
  invocation and after every part closes / on resume. Render it with
  the format in `_core.md` §Menu format.
- **Resume / restart**: §Resume / restart. On start-over you do NOT
  enumerate paths by hand: `state.js wipe-list` computes the exact set
  from the parts the state records (universals + each tracked part's
  footprint from `fixtures-data/manifest.json`, including a part's
  later-chapter additions, plus any `export.*` / `dump.sql`), and
  re-checks `pwd` against `tutorial.cwd`. Show its `paths`, require the
  literal `yes, wipe`, then `state.js wipe --confirm`.
- **Final wrap-up**: §Final wrap-up. Reached when the tester says
  they're done or finishes every available part.
