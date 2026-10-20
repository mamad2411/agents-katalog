# Founder OS - Claude Code Plugin

> This is the generic Founder OS plugin. Install it to give Claude Code the context of who you are, how you work, what you are building, and what you need help with. It replaces 20+ productivity SaaS tools with a single structured Claude Code environment.

## What This Is

Founder OS is a Claude Code plugin that installs an operating system for one founder: your identity, your roles, your priorities, your cadence, your scars - so the AI you work with stops treating you like an anonymous user and starts working like a chief of staff who has been with you for five years.

It is NOT a framework. It is NOT a multi-tenant AI platform. It is a product you install once and run every day.

## Positioning non-negotiables

- The public Founder OS product is single-founder software. ARCAS's enterprise offering has a separate company and per-employee layer. Do not conflate the two, and do not frame the public product as team or collaboration software.
- Founder OS is plain markdown any capable agent can read and drive. Claude Code is the reference runtime we validate against, and where slash commands and hooks run. We do not ship a separate product per agent: no ChatGPT-Projects pack, no per-agent skills pack. The same markdown OS is read by whatever agent the user brings. See "Runtime honesty" below for the per-skill `Runs on:` contract.
- Keep the product's established hook framing. Do not invent demo-length claims, and do not paste private brand internals into this public repo. Match the wording already used elsewhere in this repo.

## Quick Start

Say "set up Founder OS" to personalize this for your situation. If you prefer a slash command, it depends on how you installed: `/setup` on a ZIP or git-clone install, `/founder-os:setup` on a plugin install.

The wizard asks you questions about who you are, what you run, what tools you use, and what is slowing you down. From your answers it generates all the operating files in this repo - personalized to you. Takes 15-20 minutes the first time.

## Updates

Founder OS ships with `/founder-os:update` to pull the latest System Layer files (skills, templates, commands, hooks) without touching your personal data. Run it whenever you want. The command tells you what is changing before applying.

Your User Layer (identity, context, cadence, brain, network, clients, `stack.json`, `os-config.yaml`) is never auto-updated. That is your data and stays exactly where you put it.

Commands:
- `/founder-os:update` - check for updates, show changelog, walk the release packs, apply on confirmation
- `/founder-os:update check` - dry-run, report local vs remote version only
- `/founder-os:update rollback` - revert the last update

### An update is a conversation, not a download (v1.43)

Pulling new files is the easy half. Pulling them into an OS you have personalized for months is where it goes wrong, and the failure is quiet: an overwrite takes your edits away and you find out weeks later when something you fixed is broken again.

So updates arrive as **packs** in `updates/`, one per release per group of changes. Each pack states what changed, who can skip it, the files it touches with the module each belongs to, a step-by-step integration protocol, and a by-hand path naming the one file to copy if you run no tooling at all. **A pack that cannot state that by-hand path does not ship** - if a change cannot be described as a by-hand step, it is too complicated to be an update.

`os-config.yaml` at the root is what makes a pack about your install rather than about the product. It records which of the ten modules you actually run, so the parts about modules you never adopted get skipped and announced rather than walked through. It also holds the two brand values shipped code must never assume - your document font and the author name on generated documents - which is why the pre-ship gate reports those checks as skipped rather than passing on a guess when they are unset. The setup wizard writes it; edit it any time.

For any file you may have edited, the update runs a **three-way merge**: the old shipped version, the new shipped version, and yours. It works out what the release actually changed and proposes that on top of your version, leaving your edits in place. One file, one diff, one yes, never a batch. On a genuine conflict it shows both and writes nothing, because a refused update is a working install and a silently merged one might not be.

## How It Works

After setup, every Claude Code session starts with this CLAUDE.md loaded. Claude reads your context from six files:

- `core/identity.md` - who you are, how you work, what you are building
- `context/priorities.md` - what matters this week and this quarter
- `context/decisions.md` - open decisions, parked items, resolved choices
- `context/clients.md` - prospects, active engagements, closed wins
- `cadence/daily-anchors.md` - today's focus and commitments
- `cadence/weekly-commitments.md` - current sprint and retro

Two more files (`brain/log.md` and `brain/flags.md`) load on demand when you ask Claude to scan history or check what is being avoided.

That is the whole point. A small desk loads every session, and the rest of the repo is a filing cabinet Claude opens only for the task in front of it. Across a long session it does not reload what it already holds and retrieves narrowly for small answers, so context stays lean and the OS does not degrade after many turns. When `brain/log.md` grows past its cap, old entries age into `brain/archive/` and the running log stays small.

`core/avatar.md` is your behavioral profile. Skills load it on demand when behavioral context matters. It is not boot-loaded.

### The OS learns how you want to be worked with (v1.49)

`core/working-preferences.md` is the behaviour layer, and it is read **before** output the same way `core/voice-profile.yml` is read before any writing. That is the whole difference between this and the memory in a chat app. A memory is something a model might recall after you complain. This is a plain file you can open, argue with, and edit, and the OS reads it before it answers.

It ships empty and fills one correction at a time. Three doors, all ending in your yes: you state a preference ("from now on", "never ask me"), you correct how the OS is working ("too long", "you asked me that already", "just pick one"), or `/founder-os:dream` finds one in a rant. The first two apply immediately once you say yes; `/dream` runs unattended so its candidates land in a **Proposed** table and wait, the session brief counts them, and the morning loop asks. Nothing in Proposed ever gates output.

The test it is built to pass is the one `context/names.md` already passes: **the same correction should never have to be given twice.** If you find yourself giving one a second time, that is a bug in the OS - say so, and check whether the row was written and whether anything reads it.

Read points today: the bootloader (every session), `brain/.snapshot.md` (which nine output-producing skills read), `founder-next-move`, and the morning loop. If the file is missing, every one of them carries on without it.

`core/profile.md` is the meet-the-human layer. The setup wizard reads which of five operator variants fits you (founder, career-mover, builder, student, team-internal) and writes what the OS should lead with for your situation. It is read at session start alongside identity, so the OS opens with what your situation needs instead of a generic menu. Nothing locks: every skill stays available to every variant, and the variant only changes what you see first. Say "update my profile" to change it any time.

The brain layer also holds two capture surfaces and a knowledge store. `brain/rants/` captures raw voice dumps via `/rant`. `/dream` distils unprocessed rants into patterns, flags, parked decisions, and client signals. `brain/knowledge/` holds distilled notes from books, calls, and articles, which `proposal-writer` and `strategic-analysis` read back when relevant. Away-from-laptop captures land through `capture/inbox/` and the `catch-up` skill, which files them into `brain/rants/` with a name-correction pass against `context/names.md` (the names glossary) before anything is written.

A separate auto-memory layer at `~/.claude/projects/<slug>/memory/MEMORY.md` (set up by the wizard) holds behavioral guards that persist across every session. Add a guard whenever you correct Claude on something that would otherwise come up again.

When Claude knows all of this, it can give you recommendations instead of asking you to explain context every time.

Founder OS is built for dictation - you talk to Claude more than you type. Write back so it parses cleanly when read aloud: lead with the answer, and avoid deeply nested syntax that breaks a spoken back-and-forth.

## How the OS gives opinions

When the OS gives you an opinion that matters - a recommendation, a go/no-go, a pick between options, a yes or no on a send or a spend - it does not just hand you the answer. It attaches a counter-case, a confidence level, what evidence is missing, and what happens if you do nothing. This is on purpose.

There is no bias-free advice. The model running this OS is a bias engine, the same way your own judgment is. The honest move is not to pretend the bias is gone. It is to name the most likely bias and argue the other side out loud, so you decide with the counter in front of you instead of without it.

### Why your OS pushes back

You cannot see your own bias, because from the inside it looks exactly like normal thinking. A second set of eyes can see it, which is why founders hire advisors and why a good one disagrees with them sometimes. This OS plays that role. When it backs your plan, it tells you when it is backing the plan mainly because the plan is already yours. When a famous name or a confident source is doing the persuading, it separates the name from the evidence. When doing something feels better than waiting, it still names what waiting would cost.

If the OS hands you a counter-case to your own idea, it is not broken and it is not being difficult. It is doing the one job a yes-machine cannot.

Run it on demand against any claim or decision with `/founder-os:devil`. The full guard is in `rules/biases.md`.

## Empty-state behavior

If any of the 6 context files above is missing on session start, the OS is not yet set up. Do not fabricate context, do not invent past decisions, do not pretend to know the founder. Reply with this exact message and stop:

> Founder OS is installed but not personalized yet. Say "set up Founder OS" to start the wizard - it generates your identity, priorities, and cadence files (15 to 20 min). If you prefer a slash command: /setup on a ZIP or git-clone install, /founder-os:setup on a plugin install. Or ask me to bootstrap minimal versions from the templates in templates/.

This rule is non-negotiable. A wrong recommendation built on hallucinated context is worse than no recommendation at all.

## Runtime honesty - any capable agent can drive this OS

Founder OS is plain markdown. Any capable agent that can read your files can drive it. The real constraint is per-skill capability, not which agent you bring or whether it runs in the cloud. We do not ship a separate product per agent; the same markdown OS is read by whatever agent you point at it.

### The `Runs on:` contract

Every skill declares one runtime class on a `Runs on:` line near the top of its `SKILL.md`. Three classes:

- `reasoning` - reads your files and reasons, then writes a reply. Every capable agent can run it.
- `local-writes` - creates or edits files in your OS folder. Any agent pointed at the folder with write access can run it: Claude Code, or a folder-attached desktop surface like Cowork or Antigravity. A read-only surface drafts the change for you to apply.
- `local-exec` - runs a local script against your files. A local-runtime agent runs it (Claude Code is the reference). claude.ai chat or a browser LLM reads the produced artifacts instead and says so.

The class is the highest capability the skill's happy path needs (exec over writes over reasoning). A skill that reads a cache and may rewrite it is `local-writes` even though it often only reads.

### Invocation

Natural language is the universal surface: say what you want and the matching skill runs on any surface that can read the files. Slash commands are an optional shortcut, built and tested for Claude Code. On Cowork, Antigravity or claude.ai chat, do not count on a Founder OS slash command firing - say what you want in words and the same skill runs, or for a `local-exec` skill the agent reads the produced results and helps you act.

### The honest-degradation rule

Before you claim a result, check whether your surface can do what the skill needs. If it cannot (a slash command on a non-Claude-Code surface, a script run in claude.ai chat or a browser LLM, a file write where you have no write access), say so in one sentence and offer the path you CAN do: read the produced artifacts and help act, or replicate the lighter work from templates. Never claim a local write or a script run happened when it did not.

This is the single source for runtime honesty across the OS. `AGENTS.md` and `GEMINI.md` point here rather than restating it.

## Surfaces

Founder OS runs on any capable agent that can read the files. What changes by surface is capability, not whether the OS works. Three buckets (full matrix in `docs/tools-and-mcps.md`):

- **Local Claude Code (the reference):** validated in the terminal tool. Per Anthropic's docs the IDE extensions and the Claude desktop app's Code tab, with a local folder selected, read the same settings, which is not yet tested. Runs `reasoning`, `local-writes`, and `local-exec` skills, plus slash commands and hooks. Codex and other local CLIs are covered by the bridge-file redirect (`AGENTS.md`, `GEMINI.md`).
- **Desktop folder-attached (Cowork, Antigravity):** reads and writes the files through a connected folder, so it runs `reasoning` and `local-writes` skills. Cowork reaches a local folder only while the Claude desktop app is open, and from 6 October 2026 new Cowork tasks on Pro and Max plans run in the cloud. Founder OS hooks and folder commands are not tested there, so do not count on them. Whether `local-exec` works depends on whether the surface can run a script.
- **Cloud and web (claude.ai chat, Claude Code on the web, a browser LLM):** none of them works on a folder that lives only on your computer. claude.ai chat loads a plugin's skills but never runs hooks, so for `local-writes` it drafts the change for you to apply and for `local-exec` it reads the produced artifacts and helps you act. Claude Code on the web runs scripts and, in a single-repo session, a repo's own hooks, but on a GitHub copy in Anthropic's cloud, so its writes land on a branch there, not in your folder.

Apply the honest-degradation rule above: never claim a slash command, a script run, a hook, or a local write happened on a surface that cannot do it. The per-skill `Runs on:` line says what each skill needs.

If the founder context files are missing, the OS is not set up. Do not invent identity, clients, revenue, priorities, decisions, commitments, or past business context. Tell the user to say "set up Founder OS" (`/setup` on ZIP and git-clone installs, `/founder-os:setup` on plugin installs; on a surface without slash commands, bootstrap from `templates/`).

## Roles

Founder OS models the operating functions of a business as six role modes. Four are active by default and switch automatically:

- **COO** (default) - daily operations, calendar, commitments, client delivery
- **BD** - pipeline, outreach, deals
- **CMO** - content, brand, marketing, social
- **Chief of Staff** - weekly retro, stall detection, meta-layer

Switch the four active modes based on the work in front of you, not on what the operator names. Drafting a LinkedIn post is CMO mode whether they said so or not.

Two more ship as reference-until-invoked modes. They stay out of default routing and activate only on an explicit ask ("act as CSO", "switch to CTO"):

- **CSO** - portfolio strategy across everything the operator runs: balance, time allocation, strategy-vs-motion detection
- **CTO** - the tool stack and automations: infrastructure registry, automation design protocol, health monitoring

CFO is not a separate file. Financial questions route through the unit-economics skill. Full routing in `roles/index.md`.

## Tool Stack

Founder OS adapts to your tools, not the other way around. During setup, you tell it which tools you use. It generates the right integration config.

Supported adapters (configured during setup):
- Knowledge base: Notion, Obsidian, Google Drive, or local-only
- Email: Gmail, Outlook, Apple Mail
- Calendar: Google Calendar, Outlook Calendar
- Automation: n8n, Make, Zapier
- CRM: Notion DB, HubSpot, Airtable, or none

## Wiki Conventions

Founder OS is built like a personal wiki the LLM maintains. Three layers underneath your daily files:

- **raw/** - immutable source documents (transcripts, articles, books, threads). Once written, never edited. See `raw/README.md` for the frontmatter spec. Scaffolded on first `/founder-os:ingest` use.
- **The wiki layer** - your operating files: `core/`, `context/`, `cadence/`, `brain/` (including `brain/knowledge/` for distilled notes and `brain/rants/` for raw dumps), `network/`. Edited by skills as you work.
- **The schema** - this `CLAUDE.md` file. Tells Claude how the layers connect.

Two operations the OS supports natively:

- **Ingest** (`/founder-os:ingest <source>`) - process a source into raw/ with provenance, then propose wiki updates you approve. Different from `knowledge-capture`: ingest preserves the source, knowledge-capture organizes takeaways without source preservation. Use whichever fits.
- **Lint** (`/founder-os:lint`) - read-only audit. Flags broken cross-references, orphan pages, stale time-sensitive content, provenance gaps, and contradictions. Never auto-fixes. Recommended cadence: weekly. Run `/founder-os:lint` after `/founder-os:wiki-build`.

**Cross-references between wiki files use `[[page-name]]` syntax.** Example: a decision in `context/decisions.md` referencing your identity might write `as committed in [[core/identity.md]]`. The lint skill catches `[[]]` links pointing to files that don't exist. The wiki-build skill (`/founder-os:wiki-build`, v1.4) walks all wiki files, extracts the `[[wikilinks]]`, and writes them as a machine-readable graph in `brain/relations.yaml`. Idempotent. Run after a session that added cross-references. Existing files that don't use the convention are not retrofitted. The convention applies forward.

All wiki operations are opt-in. The OS works the same with or without them.

### Brain substrate (v1.4)

Three additions sit underneath the daily files. None require setup beyond running `/founder-os:setup` once.

- **`rules/entry-conventions.md`** - bi-temporal + decay convention for entries in `context/decisions.md`, `context/priorities.md`, and the brain layer. Add `Decay after: 14d` (or a date) to a flag and the SessionStart brief surfaces it for keep/kill review when it expires. Add `Superseded by:` + `Invalidated on:` to a decision instead of overwriting it. Convention is forward-only (no backfill).
- **`system/quarantine.md`** - catch-net for silent hook and cron-job failures. Helper functions for PowerShell and bash are in the file. SessionStart counts ACTIVE entries. Hooks fail silently by design. Quarantine makes failure visible without blocking the session.
- **`rules/approval-gates.md`** - explicit list of what auto-runs (brain/log appends, wiki-build, archive moves), what requires your yes (identity edits, decision supersession, sends, public pushes), and what is blocked outright (force push, hard reset, AI attribution in commits). Customize to match how you want the OS to behave.

The SessionStart brief (`.claude/hooks/session_start_brief.py`, run by the cross-platform hook dispatcher `scripts/hooks/dispatch.py` on the `SessionStart` event registered in `.claude/settings.json`) reads all three at every session open and surfaces what needs attention in one screen.

### How the OS maintains itself (v1.43)

Four rules describe how the OS stays usable as it grows, rather than becoming a pile of files nobody trusts. All four are opt-in reading: nothing here changes session-start behavior, and none of them is needed on day one.

- **`rules/os-as-harness.md`** - the four self-maintenance properties, as one doctrine: doctrine files say why they exist, scripts document their own contract, repeated failures get fixed at the engine instead of re-corrected, and the OS fits the person running it. `python scripts/selfdoc_check.py` is the checker behind the first two, surfaced by `/founder-os:lint` as one advisory line. The standing guardrail: this is a self-observing OS, not a self-modifying one. Everything proposes, you decide.
- **`rules/context-discipline.md`** - where tokens go on a long build, what must never be handed to a model, and the running build log plus the 30% rule that make a compacted or restarted session lose nothing.
- **`rules/hands-resilience.md`** - the four-rung fallback ladder for when a tool you depend on dies, the preflight habit before work that needs one, and a registry you fill in with the tools you actually run. Ships with placeholder rows and no claims.
- **`rules/digital-employees.md`** - the org chart doctrine: two faces per job, honest status, the difference between a propose-only job and a draft-only one, and the rule that a job's charter IS its permission grant rather than prose beside it. Since v1.44 `templates/roles/employees.yaml` ships with five starter roles instead of empty. Every one is backed by a skill in this repo and every one starts `gated`, so the chart still claims nothing that has not happened. Only a run you saw moves a row to `active`. Since v1.49 each job also writes its own run line to `brain/agent-runs.jsonl` (`scripts/agent_runs.py`) as its closing act, so you stop being the recording device: `employee_verdict.py render` shows runs beside verdicts, and `drift` reports an `active` row the run log has never seen. A run line says a run happened, never that it was any good - that judgement is still your verdict. Since v1.50 the team grows through one door: the `hire` skill walks a six-rung shape ladder (answer, preference line, skill, script, chartered seat, team) and picks the smallest shape that removes the job, every hire carries an informed-choice passport before your yes, and `scripts/agents_sync.py` generates one `.claude/agents/<seat>.md` per registry row so each seat is an addressable agent whose contract is the same row the charter audit reads. One source, two faces, and firing a seat is retiring its row. Since v1.52 the read-list grows: a `brain/knowledge/` note carrying an optional `seats:` line puts a pointer to itself - id, topic, path, never the body - into each named seat's agent file on the next `apply`. Three states: absent (never reviewed), routed, and `seats: none`, the tombstone that records a decline so the note is never raised again. Nothing auto-tags, and an install with no tagged notes renders byte-identical agent files.

- **`rules/outside-capability.md`** - what to do when you want a capability your OS has no idea how to do (video production, design, deep research). The three layers and which one is actually yours, the five things your own layer must carry (preflight with an honest verdict, a routing table, a money gate with sample-before-batch, a privacy line, and where finished work lands), why the outside tool lives beside your OS rather than inside it, and the plan/run/check seat split that keeps a planner away from the spending. Names OpenMontage as the recommended video tool with its licence and cost caveats stated plainly. Ships no bridge and no vendored files - the doctrine is the deliverable.

- **`rules/security-baseline.md`** - the security picture on one page: what leaves the machine surface by surface (the model session, cloud sessions, each voice tier, the scrape helper, connectors, git push), connector and MCP trust in plain words, the gitignored-only rule for secrets, the guard chain already running, and the five questions to ask before any yes. Point the founder here whenever they are about to connect something new.

`rules/banned-words-exceptions.txt` is the small companion to the voice rules: somewhere for a word you have already decided to accept, scoped to one kind of artifact, so the gate stops re-raising settled judgment. Ships empty.

`templates/culture.md` is the culture layer, and it also ships empty on purpose. Fill it in once you have decisions behind you, reading the principles back out of choices that cost you something. Each one carries its price and the test that would tell you it had been abandoned.

### The daily loop (v1.43)

`/founder-os:morning-loop` is the human half of everything above. The OS notices things and writes them into files, and files do not ask you anything. The loop asks at most four questions drawn from what is genuinely waiting, writes each answer into the file that owns it, then closes the thing that raised it so it stops coming back. It ends with one coach line naming today's single step, which the weekly and monthly reviews read. Once a day, and a quiet morning reports itself as quiet rather than inventing a question.

Two behavior rules ride with it, on `/today` and `/next`:

- **Surfaces report what moved, not what got closed.** A reply that came in, a decision that landed, a payment that arrived. Closing items is motion, and motion is easy to mistake for progress. A brief that always looks productive is one nobody believes by the second week, so when nothing moved that is the honest line.
- **Work needing your own hands surfaces as an action, not as another item on a list.** Never answer a full plate by adding to it. When the plate is full, the OS names the one thing that matters today and says the rest can wait.

Two templates support the loop. `templates/brain/needs-attention.md` is where the OS parks a question only you can answer, and answered rows stay in place so a returning question is distinguishable from a new one. `templates/workflow-map.md` maps each role to the workflows that actually run underneath it, splitting their stages into the deterministic ones that belong in code and the judgment ones that need a model plus a named check. It ships empty, because a map of workflows you intend to build stops matching reality within a month.

### Runtime brain context (v1.10)

`scripts/brain-snapshot.py` writes a small deterministic markdown payload to `brain/.snapshot.md` (open flags, this week's must-do, recent decisions, voice and brand fields, staleness). Nine output-producing skills (meeting-prep, weekly-review, strategic-analysis, decision-framework, founder-coaching, knowledge-capture, unit-economics, priority-triage, brain-log) read it at task time so the output reflects current state instead of starting cold. Snapshot is opt-in via the file existing. Skills proceed with profile-only context if it is missing.

The companion `brain-pass` skill (`/founder-os:brain-pass "<question>"`) synthesises an answer across the brain layer and returns Answer, Evidence, Confidence, and Gaps with stable-ID citations. No embeddings. No API call. Free-tier accessible. `meeting-prep` and `linkedin-post` auto-invoke brain-pass before producing output and fall back to `scripts/query.py` if it is unavailable.

`scripts/memory-diff.py` (added v1.12) is read by the SessionStart brief on every session open. It walks `clients/<slug>/` and flags any folder that has no matching entry in your auto-memory (`MEMORY.md` or `project_<slug>.md`). Closes the gap where a cloud or parallel local Claude session creates a client folder that the next local session boots blind to. Hook-only feature. No new skill, no new command.

## Agent Teams (optional, experimental)

Claude Code has an experimental Agent Teams feature: several Claude Code sessions that work in parallel, message each other and share a task list. Anthropic says it uses significantly more tokens than a single session and suits work whose pieces can run on their own, such as research or review. For a sequential flow, like a meeting's prep, capture, log and client update, a single session or subagents are the better fit.

You do not need Agent Teams to run Founder OS. Subagents are the stable default and cover most real work. Agent Teams is an opt-in upgrade once you are comfortable with the system.

**What it adds:**

- A review or research pass where each teammate takes one angle, then they compare findings
- Any chained skill invocation where the steps do not depend on each other

**How to enable:**

1. Set the environment variable: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`
2. Restart Claude Code

Know before you turn it on: Anthropic says that with the flag set, a subagent Claude names can launch as a teammate without asking, so teams can form when you did not ask for one, and each teammate adds token use. To go back, set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=0`.

**Source:** Anthropic's guide at https://code.claude.com/docs/en/agent-teams. Read it before you flip the flag on a real deliverable.

## Fabric (hooks, commands, routines)

Founder OS ships with a thin fabric layer that makes the files behave like an operating system, not just documentation.

**Slash commands** (`.claude/commands/`)
- `/founder-os:menu` - show 5 to 7 capability suggestions tailored to current state.
- `/founder-os:setup` - interactive setup wizard. Generates your identity, priorities, decisions, cadence files. Run on first install.
- `/founder-os:voice-interview` - capture how you write into `core/voice-profile.yml`.
- `/founder-os:brand-interview` - capture your visual identity into `core/brand-profile.yml`.
- `/founder-os:status` - read-only OS readiness check.
- `/founder-os:ingest <source>` - file a source into `raw/` with provenance, then propose wiki updates.
- `/founder-os:lint` - read-only audit of cross-references, orphans, stale content, and provenance gaps.
- `/founder-os:wiki-build` - refresh the auto-generated graph in `brain/relations.yaml`.
- `/founder-os:query <question>` - return the top 3 to 5 OS nodes for a question.
- `/founder-os:brain-pass "<question>"` - synthesised answer across the brain layer with stable-ID citations.
- `/founder-os:audit` - composite health report across readiness, lint, wiki, brain, and voice.
- `/founder-os:housekeeping [fix]` - one maintenance sweep. Detect (default): every debt item with its fix command, read-only. `fix`: reversible fixes in dependency order plus a judgment punch-list. Say "run housekeeping".
- `/founder-os:forcing-questions <initiative>` - six-question gate before new work starts.
- `/founder-os:os-evolve [source]` - plan the next round of OS improvements into one dated plan file: last cycle scored, gaps with evidence, numbered execute prompts, reconcile lines. It plans; a separate session executes.
- `/founder-os:founder-review [YYYY-MM]` - your own monthly review. A scorecard counted from your files, at most five coaching questions, at most three dated commitments. Private by default.
- `/founder-os:devil <claim>` - devil's advocate; runs the output bias self-check (`rules/biases.md`) against a claim or decision. Read-only.
- `/founder-os:ship-deliverable <path>` - final read-only gate before an external deliverable is sent.
- `/founder-os:legal-setup` - set up legal-compliance for the founder's jurisdiction.
- `/founder-os:legal-add-source <source>` - add a legal source URL or PDF path to the loaded jurisdiction.
- `/founder-os:legal-update` - refresh legal-compliance source freshness.
- `/founder-os:update` - pull latest System Layer files without touching personal data.
- `/founder-os:uninstall` - cleanly remove Founder OS.
- `/founder-os:rant` - qualify a raw voice dump, then route to a decision, draft, plan, log, or capture path.
- `/founder-os:dream` - process unprocessed rants into patterns, flags, parked decisions, needs-input, and client signals.
- `/founder-os:catch-up` - sweep away-from-laptop captures (capture/inbox/ drops, pasted notes, connected meeting-notes transcripts) into `brain/rants/` with the names-glossary correction pass. Say "catch up".
- `/founder-os:changes` - show every file the OS changed this session, with a one-command restore per file. Works with or without git. Say "what did you change".
- `/pre-meeting <name>` - gate before any meeting.
- `/capture-meeting <name>` - route a transcript or brain dump into log, clients, and commitments.
- `/today` - 20-line one-screen view of today.
- `/next` - one recommended next action across priorities, deals, and cadence.
- `/founder-os:queue` - manage the execution queue (read, add, start, done, park). Say "what's on my plate" or "add to queue: <thing>".
- `/founder-os:verify` - read-only substrate health check across 9 checks. Say "verify the OS".
- `/founder-os:strategic-read` - 5-section state-of-the-OS read across identity, commitments, decisions, flags, and recommended moves. Pass an optional section key (`identity`, `commitments`, `decisions`, `flags`, `next-moves`) to scope to one section. Say "read across the OS" or "what does the system look like right now".
- `/founder-os:log-reply` - ingest a pasted conversational thread (WhatsApp export, email body, voice memo transcript) into `brain/log.md` in one pass, with proposed updates to `context/clients.md` and `context/leads.md` you confirm before any write lands. Say "log this reply".
- `/founder-os:since-last-session` - report what shifted since the last run. Reads `brain/.last-session`, computes elapsed time, surfaces new log entries, decayed flags, overdue commitments, and modified `context/` files. Say "what changed since last session" or "catch me up since I was last here".

**Hooks** (one cross-platform Python dispatcher: `scripts/hooks/dispatch.py`, wired to all six events by `.claude/settings.json`; the SessionStart brief renderer lives at `.claude/hooks/session_start_brief.py`)
- SessionStart brief (v1.4 + v1.12 + v1.15 + v1.23) - surfaces open flags, stale cadence, pending decisions, [FILL] client rows, unprocessed rants awaiting `/dream`, ACTIVE quarantine entries, Review Due entries (past their `Decay after:` date), `clients/<slug>/` folders without an auto-memory entry, and a final `Observations:` line stating whether `FOUNDER_OS_OBSERVATIONS=1` is set so the silent-disable case is visible. One screen at session open. The contract is silence-as-signal: every section prints only when it has something to report, so a clean OS opens near-silent and anything the brief does say deserves attention. Do not add always-on lines that would erode that. Registered on the SessionStart event in `.claude/settings.json`. Quietly skips if the repo is not a Founder OS install (no `core/identity.md`). On fresh install (no `core/identity.md`) but with `CLAUDE.md` / `templates/` / `.claude/settings.json` present, the brief prints a one-line welcome nudging `/founder-os:setup` so the new-user path is not silence.
- UserPromptSubmit capture hook (v1.23, extended v1.49) - classifies the operator's prompt against five shapes (rant, named-person + meeting verb, status update, durable preference, correction of how the OS works) and emits a `[capture-suggestion]` system note that Claude reads before composing its reply. Rants are eagerly written to `brain/rants/` so the text is safe even if the operator walks away. The other four shapes are suggest-only - Claude must confirm with the operator before writing. Preferences and corrections propose a row in `core/working-preferences.md`; a correction is applied in the same reply before it is offered for saving. Powered by `scripts/user-prompt-capture.py`. Registered on the UserPromptSubmit event in `.claude/settings.json`. Fails open: if Python is missing, the hook exits 0 and the session continues normally.
- Session-close revenue-loop check - warns if outreach verbs appear in recent brain/log.md without a matching context/clients.md update. Registered on the Stop event in `.claude/settings.json`.
- Session-close auto-save (the caveman-git safety net) - at session end, if there are uncommitted changes AND the privacy name guard is active, records a local version so a session of work is never lost. Local only, never pushes, and shows what it saved (via `scripts/caveman_git.py save`). If the name guard is off it warns instead of committing, so unscanned private names are never auto-committed. Runs AFTER the revenue-loop check in the dispatcher's fixed Stop order so that check can inspect the working tree before this commits it. This replaces the old vague "Claude commits at session end" behavior. Surface scope: fires only in Claude Code opened in the OS folder; on other surfaces, say "save my work" manually (the `save`, `history`, `restore`, and `backup` verbs are `Runs on: local-exec`).
- SessionStart liveness one-liner (v1.30) - reads `brain/.last-session` and prints one line below the brief showing elapsed time since the last `/founder-os:since-last-session` run. Marker missing prompts you to initialize. Pure file read plus integer math, no LLM call, no marker write. Runs inside the SessionStart dispatcher handler, brief first, liveness second.

**Windows note:** every hook event runs through the same Python dispatcher, so there is no shell to be missing - no bash, no PowerShell, no git-bash required. Python 3.11+ (already a hard prerequisite of the OS) is the only thing the hooks need. If the bare `python` command is not on your PATH, setup writes the interpreter it discovered (`python3` or `py -3`) into the hook commands in `.claude/settings.json` for you.

**Routines (the heartbeat).** Founder OS checks in when you open it and runs any routine on demand when you ask - the local floor, no account needed. The SessionStart brief is the on-open daily heartbeat. The `routines` skill lists everything and triggers each in plain English ("what are my routines", "run my weekly review", "what should I change this month"). Wrap any routine with `/loop` to repeat it in a session.

The flagship is `what-to-change`: the three changes worth making now, each gated on a dated source and filtered against parked items so it never manufactures urgency. `weekly-review` rolls the sprint; the daily brief surfaces flags, stale cadence, and connectors not set up.

Unattended while-you-sleep runs are an opt-in upgrade: sync your OS to a remote (start with `backup`), then run a remote claude.ai routine against the synced copy. Native in-session scheduling (`CronCreate`) is session-only and a recurring job expires after 7 days, so the OS does not promise unattended local cron - it gives you the on-open and on-demand floor, and the remote upgrade once you sync. The `routines` skill carries the full glossary.

All fabric pieces are optional. The slash commands ship active. Hooks register in `.claude/settings.json` and ship active. Routines run on-open and on-demand out of the box; unattended is the opt-in remote upgrade.

## Skills (97 total)

The full skill registry lives in one place: [`skills/index.md`](skills/index.md) - all 97 skills and 47 commands in one table, each with its status and one-line purpose. The human-readable long-form (what each skill says, reads, writes, prereqs, and follow-ups) is [`docs/skills.md`](docs/skills.md), which mirrors that registry.

`founder-os-setup` is the entry point. Every other skill activates from natural language ("set up my voice", "what's on for today", "help me decide") or via `/founder-os:<command>`. Say "show me what you can do" (or run `/founder-os:menu`) for a shortlist tailored to your current state.

## Philosophy

- **Local-first.** Your files stay on your machine. What a session reads goes to Anthropic under your Claude plan, the way any Claude conversation does. Anything else that leaves is a surface you turned on, listed in `rules/security-baseline.md`, and ARCAS receives nothing.
- **No lock-in.** All files are plain markdown. Obsidian can read them. So can any other markdown editor. The system does not depend on a proprietary platform.
- **Boundary protection is a feature.** Saying no, parking scope, pushing back on unreasonable requests are designed in, not edge cases.
- **People first. Systems second. AI where it earns the right.**

## Commits

Commit messages follow `rules/commit-naming.md`. Subjects state the user-visible change in plain language. No version-only subjects, no AI attribution, no banned words.

## Getting Help

If something is not working, open Claude Code and say: "Help me fix [specific thing] in my Founder OS."

If you want to add a skill, role, or template: copy an existing one and modify it. The structure is self-documenting.
