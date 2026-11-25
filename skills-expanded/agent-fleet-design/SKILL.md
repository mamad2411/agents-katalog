---
name: agent-fleet-design
description: "Use when adding, backing up, or driving the agent fleet."
version: 2.0.0
author: coordinator role of hermes-fleet-apps
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [fleet, multi-agent, roles, orchestration, hermes, profile, organisation]
    related_skills: [hermes-agent-factory, agent-identity-setup, fleet-project-pipeline]
---

# Agent fleet design

The fleet exists so one person can ship software alone: the owner throws ideas
and approves plans; specialised agents own the details. The owner is the
bottleneck (attention, time, maybe no dev training), so every design choice must
reduce their decisions to a few gates. Creating a single profile is
`hermes-agent-factory`; this skill decides WHICH profiles exist and how they hand
off.

## Always-on rules

- **Split by conflict, not by human job title.** A new agent is justified only
  by one of three conflicts: a different SOUL (builder vs judge), different
  tools (video renderer vs compiler), or different risk (may push to git vs
  writes prose). No conflict = the same agent carries several human roles
  (coder = frontend + backend + devops). 5-7 agents cover a small software org.
- **Project state lives in the repo, not in agent memory.** Agents coordinate
  through project files (`SPEC.md`, `.design/`, git log), never by reading each
  other's profile dirs — a profile is who an agent is, not where the work stands.
- **One shared `FLEET.md` next to the profiles** lists who does what,
  inputs/outputs, and the owner's approval gates. Each agent's memory carries ONE
  line pointing at it. Never copy the fleet map into every memory — N copies
  drift the first time an agent is added.
- **Adding an agent = FLEET.md edit + pointer edits** in the SOULs that
  previously held the responsibility (e.g. "brand belongs to coder" → "to
  designer"). Grep every SOUL for the responsibility word before declaring
  the hand-over done.
- **Skills migrate with responsibilities.** When carving a role out of a fat
  agent: `find <profile>/skills -name SKILL.md`, map each skill as stays /
  → new agent / → later agent / remove (off-role), show the owner the map, move
  only after they confirm, then re-run `prompt-size` on both profiles. `mv` by
  default; **copy** only when both sides genuinely run it from their own seat
  (commit-identity rules: coder signs, docs publishes; interview forms: product
  and coder both question the owner). Read the skill's `description` before
  deciding — a review skill written for the *author* ("request a review")
  stays with the builder, one written for the *judge* goes to qa.
- **Build the whole fleet before resuming product work.** A half fleet means the
  first real project hits a missing seat mid-flow.
- **Hermes kanban is the software factory, already built.** `claim`
  (atomic, per-profile), isolated workspace per task, review states,
  `decompose` (routes by profile `description`), `dispatch` daemon. Do not
  hand-write "claimed label / sandbox / one-merge-at-a-time" rules into
  FLEET.md — adopt one board per project once the fleet exists, test with 2-3
  real tasks, then make it the standard path (see `fleet-project-pipeline`).
- **Keep a plan file while restructuring.** Reorganisation spans sessions and
  overwhelms the owner; the coordinator owns a `FLEET-PLAN.md` (decided / open
  decisions / numbered steps) and surfaces ONE open decision at a time. The owner
  does not have to remember the file — the coordinator re-reads it.
- **A per-project knowledge base lives in the project, not per agent** — per-agent
  copies go out of sync.
- **Efficiency settings are baked into the seed**, not applied per agent (e.g.
  `hermes -p seed config set compression.threshold_tokens <n>`). There is no
  config option for "hand off after N compactions" — that is a behaviour rule for
  the seed SOUL (LIMITS) plus the `handoff` skill: endless compaction degrades
  context and silently drops earlier decisions.
- **Shop the hub before writing a role skill**: `hermes skills search <term>`
  then `hermes skills inspect <identifier>`. Prefer `official` trust; read
  frontmatter for `allowed-tools`/CLI needs and reject anything requiring a
  paid or cloud CLI — it silently routes work off-machine. Vet community skill
  repos per `references/community-skill-vetting.md`, give a TAKE / DROP / LATER
  verdict, assign every TAKE to exactly one profile, and record the verdict in
  the plan so it is never re-vetted. Install when that profile is built, not before.
- **One skill per theme per agent.** Two review skills or two spec skills on
  one profile compete for the trigger. When two repos overlap, pick one source
  for that theme and write the pick in the plan.
- **A persona repo ("think like the lazy senior dev") splits in two**: the
  standing rule (e.g. the Ponytail ladder: exists? → in repo? → stdlib? →
  installed dep? → one line? → minimum; never cut validation/security/error
  handling; one small test; end with "what I skipped") goes INTO the SOUL of the
  coding seats, in full, so it holds without the model choosing to load anything;
  the long procedure (`ponytail`, `ponytail-review`, `ponytail-audit`) is
  installed as plain SKILL.md files from the upstream repo, never through a
  third-party plugin wrapper. qa gets `ponytail-review` only (it finds code that
  should not exist, which `code-review` does not). A persona that conflicts with
  a seat's SOUL (non-dev agents) is not installed there at all.
- **Skills an agent cannot do its job without are named in its SOUL at the
  method step where each applies** ("Research `x`; Spec `y`"), names only.
  The skill index is a suggestion the model may skip, and the owner never names
  skills or talks to most agents; the SOUL is read every turn. 2-7 names per
  seat; everything else stays index-only or is named in the coordinator's brief.
- **An agent with no job in the queue is maintenance debt.** Park it as
  FUTURE in the plan with its trigger condition. Check the candidate repos' shape
  first: a repo that is an MCP server plus external tools (`npx ... setup`,
  decompilers, proxies) or has no `SKILL.md` at all is a *tool install*, not a
  hub skill — it needs the owner's explicit install approval, so it cannot be
  built on autopilot like a skill-only agent.
- **Retiring a project's knowledge** (the owner restarts a project from scratch):
  follow `agent-identity-setup` → "Retiring a project's knowledge", and grep
  `FLEET.md` too.
- **Naming**: one word, a trade or a function, no human title. Offer the owner
  five options with a one-clause meaning each; they pick.

## Fleet backup repo

The fleet is the asset; Hermes profiles are its runtime copy. Keep one local
git repo (no remote unless the owner asks) that holds, per agent, exactly the
five portable things: `SOUL.md`, `profile.yaml`, `config.yaml`, `memories/`,
`skills/` plus the marker `.no-bundled-skills`, and at the root the shared
`FLEET.md`, `FLEET-PLAN.md`, a small snapshot/restore script, and project
folders for fleet-level work.

- **Never in the repo**: `.env`, `sessions/`, `cache/`, `state.db*`,
  `skills/.hub/` (hub cache, several MB per profile), `skills/.usage.json`,
  `skills/.curator_*`, `skills/.archive/`, `*.lock`. `.gitignore` them and
  check `git ls-files | grep -cE 'usage.json|curator|\.hub|\.env$'` → 0
  before the first commit — a hub cache alone doubles the repo size.
- **Loop after every agent change**: real test + `prompt-size` → snapshot →
  `git commit -m "<agent>: <reason>"`. One commit per SOUL change; the message
  is the changelog.
- **The snapshot copies only the agents its list names.** A live profile missing
  from that list is not backed up. Add the name first, snapshot, then commit only
  that profile plus the script. Leave other profiles' already-dirty files
  unstaged — a snapshot refreshes every listed profile, and committing them mixes
  unrelated history into this change.
- Do not add `.gitattributes` with `eol=lf` and leave `core.autocrlf`
  unset on Windows: every snapshot then prints thousands of CRLF warnings that
  drown the commit output. Set `git config core.autocrlf false` in the repo.
- Set the repo's commit identity locally (per repo). If the owner later wants a
  remote, say so, so they pick the forge identity.
- Restore = restore one agent's files + rewrite `MEMORY.md` for the host + the
  owner types `.env`. Memory is machine truth, never restored verbatim.

## Driving a fleet agent from the coordinator

- One-shot: `hermes -p <agent> chat -q "<brief>"`. Continue the same
  session with `hermes chat --resume <id> -p <agent> -q "..."` — `hermes
  --resume ...` without `chat` is parsed as a command name and fails.
- A design/render job runs 3-40 min. Launch with `terminal(background=true,
  notify=true)`; never block a foreground call on it and never re-run it
  when the foreground cap promotes it. Tell the owner one line, end the turn.
- The brief names the exact files to read (`SPEC.md`, `../FLEET.md`,
  `.design/ui-plan.md`, `tokens.json`), the output path, and "reply under
  N lines" — the agent's reply is what the coordinator relays to the owner.
- **Route a field's questions to the agent that owns the field, even quick
  ones.** "Give me a list of visual styles" goes to the designer and the
  coordinator relays the comparison. The coordinator's own job is the brief,
  the gate, and the relay.
- **When product is the seat**: any *what* decision, not only a new idea — a
  new feature on an existing app (scope cut + tickets), "does this make
  sense?" (stress-test, competitors, trademarks), a project that lost its
  course (re-read SPEC, push to "later"). Rule of thumb: nothing reaches coder
  that is not in an approved SPEC. Internal demos/videos skip product — the
  coordinator writes those SPECs.
- **Videos made from code are media's job, including quick teasers.** The
  coordinator writes the brief and relays the result; it never renders itself.
  Before setting up any toolchain for a field, look in the owning agent's work
  folder first: a second copy is waste the owner has to find later.
- **Before saying a project "has no style"** (and routing it to the designer),
  search the repo for `tokens.json` anywhere (`find <repo> -name tokens.json -not
  -path '*/node_modules/*'`), plus `DESIGN.md` and logo files. Older projects may
  keep their house style outside `.design/`; a check limited to `.design/`
  misreports it and sends the owner through a needless design gate.
- **Check the GPU before dispatching any render**: another process can hold most
  of the VRAM. If one does, say so and
  let the owner choose (stop it / go anyway). If the owner says stop mid-render,
  kill the background loop first, then the renderer, or the loop starts the next
  item.
- **Video idea menus**: ground each idea in what media's skills already cover
  (chart, diagram, kinetic type, explainer) and say per idea whether the
  project's style exists; recommend the reusable one (a template refilled with
  new data) over a one-off.
- **Fleet demo content is generic**: the fleet is the subject, no owner named
  or shown, professional wording, no hype. Put that in the SPEC; agents
  otherwise write the owner into the story.
- A second visual variant of the same demo is a new project folder
  (`<demo>-<variant>/`) with its own `SPEC.md` and `.design/`, run through the
  same chain — never a branch of the first `.design/`, since media reads one
  tokens.json per folder.
- **Resuming product work after a fleet-building stretch**: no gateway restart
  unless the coordinator's own SOUL/config changed — memory and skills load fresh
  per chat. Open a new chat and paste a handoff prompt (fleet map path, repo
  path, project scope, the chain to run, first step); do not reopen the
  pre-fleet chat, its context predates the agents.
- The owner adds requirements while a job runs: append a dated `## Owner,
  addendum` block to the artifact the agent is still writing
  (`.design/ui-plan.md`) instead of waiting for it to finish — the agent re-reads
  its own file and folds it in; a second round costs 15-30 min.
- "How long?" is answered from evidence, not a guess: `ls -lt` the agent's
  output folder for the latest write, then say which step it is on.
- A round-2 brief says "read ui-plan.md and tokens.json fully again, they
  changed" and "keep the old render as `<name>-v1.mp4`" — a resumed session
  otherwise trusts its earlier reading and overwrites the only copy the owner
  has seen.
- Every render brief ends with "clean your build dir when done": a renderer
  cache outside the project folder can reach several GB per job, and a repo
  sweep never finds it.
- Check the agent's artifact against its own plan before handing on:
  tokens.json names image files → those exact filenames must exist in
  `.design/images/`, and `grep -ril tbd .design` must be empty. Fix trivial
  mismatches yourself and commit; do not bounce the agent for a filename.
- Fleet-level creative work goes through the same chain as a product:
  SPEC.md (the coordinator writes it) → designer Research + Direction (2-3
  options, comparison table) → owner picks → designer Plan (brand, tokens,
  storyboard to the millisecond, images) → media renders → qa checks against the
  storyboard. Do not send media a style brief directly; it takes style only from
  the project's `tokens.json`.
- **Video deliverables**: every text block stays on screen long enough to read
  twice aloud; deliver the full-res file by path and a small preview for chat.
  Gitignore renders with `**/assets/*.mp4` — a root-anchored `assets/*.mp4`
  misses every variant folder.
- **Per-agent artwork or any image set**: ask for ONE style proof before the full
  set, so a wrong style costs one image, not eight. Every generated image gets a
  close-up defect check before it reaches the owner.
- **Third-party imagery**: register every image in `.design/imagery-briefs.md`
  with source URL and licence. Artwork with no open licence is "private demo only;
  replace before any public release", so docs blocks a public ship. "Everyone
  does it" is not a licence — say so once. For Hermes-branded art, check the
  licence file of the upstream `NousResearch/hermes-agent` repo before using its
  `assets/`.

## Fleet runtime ops (gateways, updates)

- SOUL and skill index load at session start. After a SOUL/skills change:
  headless seats need nothing (each job is a new session); running gateways
  need a restart; open CLI sessions need `/new`.
- Find what runs: `for p in */; do hermes -p ${p%/} gateway status; done`
  from the profiles folder, or `hermes update --plan` (lists every live service
  with its restart command, read-only).
- On Windows, restart other gateways through their own launcher, not
  `hermes -p X gateway restart` from the coordinator's shell: a restart spawned
  there stays in its Job Object and dies with the session ("could not break
  away" warning). Run `hermes -p X gateway stop`, then the profile's startup
  launcher, then `gateway status`.
- The coordinator cannot restart or update itself: Hermes blocks `gateway
  stop/restart` and `hermes update` from inside the gateway. Hand the owner the
  one-line command for their own terminal and ask them to ping the chat
  afterwards.
- `hermes update --set-channel stable` only records the channel and exits;
  the actual update is a second `hermes update --backup -y`. Verify first with
  `git merge-base --is-ancestor HEAD <tag>` in the Hermes checkout that the
  stable tag contains the current commit, so state written by newer code is not
  at risk. A fleet usually wants `stable`, not `main`.

## Reference chart (dev fleet)

```
owner ──idea──> coordinator (routes work, talks to the owner)
   product   what & why   -> SPEC.md (scope, users, done-criteria)          <- gate: owner
   designer  how it looks -> .design/ (brand.md, ui-plan.md, tokens.json, logo/)  <- gate: owner
   coder     builds       -> code + tests; front, back, devops, CI
   qa        verifies     -> bug list, security, review. Never edits code
   media     motion/video -> assets from .design/tokens.json
   docs      release      -> README, changelog, store listing, posts        <- not a gate: owner says go per push/tag/post
```

Out until there is work: legal/finance/sales/support/data.

Two stress-tests, not one: product stress-tests the **idea** (users, purpose,
scope cut); coder stress-tests the **spec** (feasibility, risk, gaps). Do not
strip coder's interrogate step when product appears — re-aim it at the spec.

## Fleet inventory one-liner

Run from the profiles folder:

```bash
for p in <names>; do echo "== $p: $(python -c "import yaml;print(yaml.safe_load(open('$p/config.yaml')).get('platform_toolsets',{}).get('cli'))")"; \
  echo "skills: $(find $p/skills -name SKILL.md | wc -l)"; hermes -p $p prompt-size | grep -E 'total|Tool schemas'; done
```

A narrow agent showing 58-68 skills inherited the bundled sync, not chose
them — trim in a dedicated pass, not while creating another agent.

## Designer contract (reusable for any visual role)

- Deliverables in `<repo>/.design/`: `brand.md`, `ui-plan.md` (per screen:
  purpose, layout, components, empty/loading/error states), `tokens.json`
  (single source of truth; media reads it), `logo/` (SVG + PNG exports +
  font licences), `images/`, `imagery-briefs.md` (register: source URL +
  licence per image, prompts for anything the owner must render), `research.md`.
- Rule: no "TBD" anywhere. If coder would have to ask, the plan is not done.
- Flow: Brief → Research (platform guidelines, 3-5 reference apps) → Direction
  (2-3 options via `sketch` mockups) → owner picks → Plan → owner approves →
  coder builds → designer reviews screenshots, returns a punch-list, never code.
- **A creative seat should be able to produce, not only brief**: give it the
  tools for mockups, SVG and image edits it can do locally, and say per job what
  still needs the owner.
- **Design gates can run through Lavish** (`skills-sh/kunchenguid/lavish-axi/lavish`,
  MIT): the designer writes a reviewable HTML page, opens it with
  `npx -y lavish-axi <file>`, the owner annotates in the browser, feedback returns
  via `lavish-axi poll`. Rules that came with it:
  - Never `lavish-axi share` (it publishes to a third-party host). When a
    CLI-backed skill has a publish/share subcommand, ban it in the SOUL at
    install time.
  - **A live gate needs a listener**: the server self-stops when no poll is
    attached, and the owner's notes then sit stranded in the tab. A real review
    brief tells the designer to open the page and then run
    `npx -y lavish-axi poll <file>` in the foreground and wait, launched by the
    coordinator with `terminal(background=true, notify=true)`. If the page died
    anyway: `lavish-axi <file> --reopen` + poll.
  - Headless test only: brief "open it, do NOT poll" — a poll blocks
    `hermes chat -q` until a human answers. After the test: `npx -y lavish-axi
    stop`, delete the scratch dir and the test session.
  - If the owner reviews from a phone chat while the page opens on the PC, tell
    them the tab will appear and that answering in chat is fine.
- Hub skills that fit: `official/creative/impeccable` (UI/UX method),
  `official/creative/sketch` (variant mockups). Read scanner verdicts before
  installing a community logo/design skill: some are blocked for real reasons
  (sub-agents with permissions bypassed, global npm installs).

## Role seat SOULs (~2.5 KB each)

qa: the builder never grades its own work; Scope → Run → Review → Report; never
edits a project file, not even a typo; PASS only on what it ran. product:
Interrogate → Research → Cut → Spec → Tickets; v1 = smallest thing that proves
the idea, the rest to "later"; questions as a small form with options. docs:
Verify (no qa PASS = no release) → Draft → Check (every claim maps to a built
feature) → Ship only on the owner's go; never a trademark as ours.
