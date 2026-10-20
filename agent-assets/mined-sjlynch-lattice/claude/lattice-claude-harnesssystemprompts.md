# backend/src/harnessSystemPrompts

Per-project, per-harness overrides of the **agent's own built-in system prompt**
(not a Lattice-authored brief — that's `instructionTemplates/`). For each harness
(`claude` / `codex` / `pi`) a project can supply an **Append** string (added on
top of the built-in prompt) and/or a **Replace** string (swaps it entirely).
Edited in Settings → Agent prompts ("Harness system prompts"), stored on
`UserSettings.harnessSystemPrompts`, and injected at every spawn of that harness
in the project. `../harnessSystemPrompts.ts` is the public barrel.

## How each harness is overridden

The mechanism differs per harness because each CLI exposes the override
differently. All follow Lattice's "resolve in the backend, apply at spawn" split.

- **Claude** — `claude --system-prompt-file <replace>` and/or
  `--append-system-prompt-file <append>` (both work in interactive sessions).
  The text is written to a scratch file and the terminal-server adds the flag
  (`terminal/claudeSystemPrompt.ts`), the path riding a child-env var so it's
  never interpolated into shell source. Claude's *default* prompt is proprietary
  and can't be shown — the editor says so; the override still works.
- **Codex** — `-c developer_instructions=<append>` (an additive developer-role
  message) and/or `-c model_instructions_file=<replace-file>` (replaces the base
  instructions; needs a recent Codex, and OpenAI discourages it). The `-c`
  strings are applied by `configureCodexSystemPrompt` in `terminal/codexTrust.ts`
  on their own `LATTICE_CODEX_SYS_<i>` env-var series (distinct from the MCP
  overrides so both coexist).
- **Pi** — a Lattice-installed `before_agent_start` extension
  (`.pi/extensions/lattice-system-prompt.ts`) reading a JSON sidecar
  (`lattice-system-prompt.json`) with `{append, replace}` (see `piShim.ts`). Pi
  has no shell-safe CLI flag for a multi-line prompt and writing `.pi/SYSTEM.md`
  would clobber a user's own file, so the extension — mirroring
  `piExtension.ts`/`piMcp/` — is the collision-free route for both modes. Written
  into the session cwd by the backend at spawn (never rides the wire). The
  Lattice preamble (below) always rides the append side, so every Pi spawn in a
  managed project writes the pair even with no override; it is removed only when
  the resolved `append` and `replace` are both empty (an unmanaged project with
  no Pi override), so a reused cwd there doesn't keep a stale prompt.

## The always-on Lattice preamble

Separate from the per-project overrides above, Lattice folds its OWN one-
paragraph preamble into the **append** side of every harness system prompt, in
every project that has a `.lattice/` dir. It names Lattice's trigger words
(task board, lanes, worktrees, merging, workflows, startup terminals) and the
absolute path of that project's generated `.lattice/LATTICE_API.md`, so an
agent working in an unrelated repo can answer "what is the Lattice board?" and
drive the API instead of guessing. Lives in `latticePreamble.ts`.

Why the system prompt and not something cheaper — both alternatives were tried
and neither reaches a model:

- **Env vars can't work.** The old `LATTICE_DOCS`/`LATTICE_PROJECT`/… pty
  breadcrumbs were invisible: no harness loads the environment into its
  context. They are gone (`terminal/launchContext.ts`).
- **The terminal banner can't work.** `terminalBanner.ts` appends to the
  session SCROLLBACK — the browser's replay buffer. The pty child never
  receives those bytes. It stays, as chrome for the *user*.
- **Writing into the pty would work but is unacceptable**: the text arrives as
  the session's first user turn, which Claude Code then uses to NAME the
  session, and the user sees it in their terminal.

Composition rules (`composeSystemPromptAppend`): the preamble comes first, the
project's own Append second (the user's text reads as the more specific
instruction when it comes last). All three join with a blank line.

**Codex on cmd.exe** is the one lossy channel: its inline
`-c developer_instructions='''…'''` value transits cmd.exe (the Windows pty
default) as `"%VAR%"`, which strips inner double quotes (re-splitting the value
on spaces) and ends the command at an expanded linefeed — a multi-line or
quote-bearing Append used to break every Codex spawn in the project. So
`prepareCodexSystemPrompt(project, extra, shell)` normalizes the composed append
(`normalizeCodexAppendForCmd`) when the shell is cmd.exe **or unknown**: line
breaks → one space, `"` → typographic “ ”. The caller (`resolveCodexSpawn`,
`terminalServerClient/spawnCodex.ts`) passes `resolveDefaultShell()` — the same
resolution the terminal-server's `launchContext` uses, inherited env and all. A known
POSIX / PowerShell shell gets the text verbatim (`"$VAR"` / `"$env:VAR"` carry
both). On every shell a run of 3+ `'` is spaced out (`' ' '`) so it can't close
the TOML multi-line literal early. The Settings Codex card says so in its Append
description (`defs.ts`). The preamble text itself stays one line with no double
quotes, so it reaches Codex byte-identical to what Claude and Pi see.

A project with no `.lattice/` dir gets no preamble at all — Lattice never seeds
that dir into a project it doesn't manage, so an unmanaged cwd spawns with a
stock system prompt.

A **task-worktree spawn** (task run/resume, worktree merge resolver — the
spawn's `mcpScope`, see `mcp/taskWorktreeScope.ts` `isTaskWorktreeSpawn`) also
gets the one-line task verification rule (`../taskVerification.ts`: "don't run
tests, builds or type-checks") folded in right after the preamble — the
`extra` argument of the three `prepare*` functions. Claude writes that variant
to its own `claude-append-task.md`, since the shared `claude-append.md` is only
race-safe while every spawn of the project writes identical content.

## Modules

- `defs.ts` — **leaf catalog** (`HARNESS_SYSTEM_PROMPT_CATALOG`): per-harness
  read-only overview + best-available default text (real for Codex/Pi, an honest
  "not viewable" note for Claude) + per-field docs + source link, plus the
  shared types. Imports nothing from the resolver/injector, so both can import
  the catalog without a cycle.
- `resolve.ts` — `resolveHarnessSystemPrompt(projectPath, harness)`: the saved
  `{append, replace}` trimmed to only its non-empty sides, else `null`. The
  non-empty guard means a blank field never blanks out the built-in prompt.
- `editorData.ts` — `buildHarnessSystemPromptEditorData(project)`: the settings
  payload (catalog + the project's current Append/Replace text). Backs
  `GET /api/harness-system-prompts`.
- `piShim.ts` — renders + reconciles the Pi `before_agent_start` extension and
  its JSON sidecar (`applyPiSystemPromptForSpawn`). Byte-significant like
  `piExtension/template.ts`; skips a write when unchanged, removes the pair only
  when the resolved `append` and `replace` are both empty (no preamble — an
  unmanaged project — and no override).
- `latticePreamble.ts` — the always-on Lattice preamble described above:
  `buildLatticePreamble(docPath)` (pure text), `resolveLatticePreamble(project)`
  (generates/refreshes the reference via `ensureLatticeApiDoc`, returns `null`
  for an unmanaged project), and `composeSystemPromptAppend` (preamble-then-user
  join with a configurable separator).
- `inject.ts` — turns the resolved override **plus the Lattice preamble** into
  per-harness injection at the spawn chokepoint: `prepareClaudeSystemPrompt`
  (write files → paths), `prepareCodexSystemPrompt` (build `-c` arg strings),
  `preparePiSystemPrompt` (reconcile the extension). In a managed project each
  produces output even when the project configured nothing, because the
  preamble alone is enough. Scratch files live under
  `~/.lattice/per-project/<hash>/system-prompts/` (home-scoped, atomic writes).

## Where it's wired

- Resolved + applied at the single spawn chokepoint `resolveHarnessSpawnBody`
  (`terminalServerClient/spawnBody.ts`; `createSession.ts` only re-exports it),
  which dispatches per harness to `resolveClaudeSpawn` / `resolveCodexSpawn` /
  `resolvePiSpawn` (`spawnClaude.ts` / `spawnCodex.ts` / `spawnPi.ts`), so all
  spawn sites (task run/resume, workflow step, post-merge hook, push, QA,
  sidebar terminal, conflict resolver) are covered. Claude/Codex
  ride new `SessionWireBody` fields applied by `terminal/launchContext.ts`; Pi's
  files are written directly (like `piMcp`).
- The Pi extension + sidecar are registered Lattice-owned files in
  `worktree/managedFiles.ts` (gitignored + worktree-excluded).

## Invariants

- **A blank/whitespace-only field is ignored** (falls back to the built-in
  prompt on that side) — the safety net against an accidentally-cleared box.
- **The Lattice preamble is not user-suppressible and always leads.** It is
  Lattice telling the agent what harness it is running under; a project Replace
  swaps the harness's own prompt but leaves the append channel (and so the
  preamble) intact on all three harnesses.
- **Best-effort at spawn** — a resolve/write failure degrades to a plain spawn
  and never blocks it (the per-harness resolvers in
  `terminalServerClient/spawn{Claude,Codex,Pi}.ts` wrap each `prepare*` call in
  `.catch`).
- Injection is resolved in the main backend and applied by the terminal-server
  (Claude/Codex) or written as cwd files (Pi) — matching the MCP control plane,
  so a prompt edit is a backend-only change with no terminal-server respawn.
