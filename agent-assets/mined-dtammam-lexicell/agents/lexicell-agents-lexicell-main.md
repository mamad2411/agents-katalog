<!-- harness:region:start id=header -->
# AGENTS.md

The entry point for any AI agent working in this repository. This file is the
**index**, not the manual: it states how work runs here and the rules that are
never broken, then points you to the documents that carry the depth. Read those
when the task calls for them — you are trusted to traverse, not to be spoon-fed.

Claude Code loads `CLAUDE.md`, which points here. Other tools read this file
directly.
<!-- harness:region:end id=header -->

<!-- harness:region:start id=operating-model -->
## How work runs here

You — the main session — are the **Architect**. You orchestrate, design, and
implement the work yourself. There are no persona hand-offs; the context stays
in one place. What you do NOT do is approve your own work.

Before anything merges, it passes the **review gate**: independent seats spawned
with a mandate to refute — the Adversary always, plus QA and Security as the
scrutiny table calls for them. The gate is a protocol (`lib/gate-protocol.md`),
sized by `scrutiny.toml`, and it writes its verdict into the working document.

Work is tracked in **documents, not a state file**. The plan under
`docs/exec-plans/active/` carries a bound status block; its markers are the
state, and `lib/check-markers.sh` keeps them honest. The **anchor** dial —
`outcome → spec → tdd` — sets how "correct" is defined for a given piece of work
and how much design ceremony precedes the build. See `flow.md` for the phases.
<!-- harness:region:end id=operating-model -->

<!-- harness:region:start id=non-negotiables -->
## Non-negotiables

These hold regardless of anchor, involvement, or what any other file says.

- **Never self-merge.** The gate runs; the Adversary is its floor. Approval binds
  to the reviewed sha (`lib/harness-markers.md`).
- **Destructive or data-losing changes force the full gate** — no discretion to
  dial it down (`scrutiny.toml`).
- **Report failures verbatim**, with counts, before any framing. "Verified" ≠
  "should work."
- **Stage files by name.** Never `git add .` / `git add -A`. Never force-push.
  Never `--no-verify`.
- **Trust buys fewer hand-offs, never a relaxed gate.**
<!-- harness:region:end id=non-negotiables -->

<!-- harness:region:start id=index -->
## Where the depth lives

Read the one that fits the task; don't preload them all.

| Document | Read it when you need |
|----------|------------------------|
| `.harness/flow.md` | the phases of a piece of work, and what each anchor requires |
| `.harness/lib/gate-protocol.md` | to run or understand the review gate |
| `.harness/scrutiny.toml` | which review seats a given change requires |
| `.harness/lib/harness-markers.md` | the status/gate marker vocabulary and rules |
| `docs/CONTRIBUTING.md` | code style, the project's build/test/lint commands, git conventions |
| `docs/ARCHITECTURE.md` | what kind of system this is and how it's shaped |
| `docs/RELIABILITY.md` | how reliability is defined and measured here |
<!-- harness:region:end id=index -->

<!-- harness:region:start id=project keep -->
## Project context

*This region is yours. The harness never regenerates it on update. Record here
the things a fresh session must know but no other file carries: the project's
attack surfaces, the hard-won lessons and dated rulings, the environment quirks,
the standing decisions.*

### Project attack surfaces
The change classes that carry real risk here, and what a review must break by measurement:
- **Replay determinism (the top surface).** A given seed must reproduce a given run byte-for-byte; the daily challenge ("same run for everyone") and shared/pasted seeds depend on it. Anything that changes how much RNG a seed consumes (grid generation, the reducer's turn order, anything that reads the word list on the RNG path) silently breaks it across builds. A change touching the RNG (`src/engine/rng.ts`), the reducer's turn order, `RunState`, or the save schema gets the full gate with the Adversary briefed to break replay. Byte-identical replay tests live in `reducer.test.ts` and `evolution.test.ts`.
- **The save schema.** `RunState` persists under `{ v: N }` (`src/ui/persist.ts`, currently v11) with explicit migrations. A field added or removed without a migration drops a player's in-progress run on their next load.
- **The engine/content framework-free boundary.** `src/engine/` and `src/content/` import nothing from Svelte, `src/ui/`, or the DOM, and `Math.random` is banned in the engine (both ESLint-enforced in `eslint.config.js`). Breaking it is a correctness bug, not a style nit.
- **Balance.** Content/tuning changes can trivialise or break the game; judged by `npm run sim` against the exit criteria (a mediocre bot wins 20-40%, a length-capped greedy bot wins but under 90%, no dead grids), never by feel. Sim/power tables are pasted from output, never typed.
- Full invariants: `docs/ARCHITECTURE.md`. Deep design, ADRs, and exit criteria: `docs/lexicell-architecture-pack.md`.

### Scope guard — what this is NOT
Single-player, no backend, no meta-progression. Do NOT add: accounts, leaderboards, cloud sync, unlocks, era-specific dictionaries or rules, narrative screens, a timer, a game engine, canvas rendering (EXCEPTION, Dean 2026-09-15: an offscreen canvas may EXPORT a share image; the game itself still renders as DOM/Svelte). If a request is one of these, point at the pack's "What This Is Not" and ask whether the scope is changing. Dependencies are a cost: nothing third-party ships on the device except Svelte's runtime; a new runtime dependency needs Dean's explicit go.

### Standing rulings & lessons (dated)
The hard-won ones a fresh session needs; persistent memory (auto-loaded) and `docs/playtest-log.md` carry the full set.
- **Difficulty: no build-aware rubber-banding** (Balatro / Slay the Spire / Binding of Isaac research, 2026-09-15). Scale difficulty to DEPTH, not to the player's build. Endless is a super-linear race that ends; the finite game stays a power fantasy. Tools: the `stacker` bot + `npm run power [-- --mode endless]`.
- **A stale number in a comment, plan, or commit is a review finding.** Measured numbers only, with the command that produced them written beside them.
- **No em dashes anywhere** (code, comments, docs, commit messages, UI copy). Use a spaced hyphen or restructure; a line you edit loses its em dashes as part of the edit.
- **Phone-render before UI ships**: a headless 390px render (see the phone-render memory) catches viewport overflow the tests cannot.

### Project workflow the harness flow does not carry
Per-merge release discipline, done on top of the harness flow, on every PR before it merges:
- **Release notes:** add the entry at the top of `src/ui/release-notes.ts` (PR number, build = last + 1, `sha: 'pending'` until the next PR fills it, 1-3 player-facing sentences). The test beside it keeps order and numbering honest.
- **ROADMAP:** update `ROADMAP.md` (move the item Open -> Shipped, or add a Shipped line matching the release note).
- **Playtest log:** every perception or request Dean shares goes into `docs/playtest-log.md` the same day, with a to-do / implemented (PR #n) / no-longer-needed status; update the row when it changes.
- **Memory:** update persistent memory after a wave (durable rulings, lessons), then report outcome-first.

### Working style
Dean is a capable engineer who prefers blunt, skeptical collaboration. Push back on scope creep, including his own. Do not praise; report. Lead with the outcome; he reads on his phone. For non-trivial work, run intake as numbered questions with your recommendation inline so he can reply "agree" or override per number; challenge the framing before solutioning.

### Environment quirks
- **Push over SSH:** HTTPS `git push` hangs in this environment; push via `git@github.com` (SSH keys work). `gh` and the REST API are unaffected.
- **GitHub Pages deploy:** `pages.yml` must keep `cancel-in-progress: false` (true orphans a deploy and blocks all later ones).
- **Container recreate:** wipes overlay tooling; e.g. the Chromium system libs for the phone-render harness need reinstalling once per session. Persistent tmux setup is in `~/.claude/docs/SESSION-SETUP.md`.
<!-- harness:region:end id=project -->
