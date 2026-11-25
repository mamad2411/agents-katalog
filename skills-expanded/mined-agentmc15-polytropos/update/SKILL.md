---
name: update
description: Check and refresh everything this repo installs into its harnesses — Claude plugin cache staleness, Copilot and Codex bundle drift, generated pricing mirrors, and docs snapshot freshness. Use when the user asks to update or refresh the plugin or a harness install, asks whether installs or pricing docs are stale, or after pulling or merging changes into this repo. Args: optional "apply" to refresh after checking (check-only is the default).
allowed-tools: Bash, Read
---

# Update

Run the engine that ships with this plugin. Use the `${CLAUDE_PLUGIN_ROOT}` env var Claude Code
sets for plugin-executed content; if it is unset, fall back to resolving
`../../bin/harness_update.py` relative to this SKILL.md to an absolute path before shelling out
(bash cwd is not the skill dir).

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/bin/harness_update.py" check
python3 "${CLAUDE_PLUGIN_ROOT}/bin/harness_update.py" apply --dry-run
python3 "${CLAUDE_PLUGIN_ROOT}/bin/harness_update.py" apply
python3 "${CLAUDE_PLUGIN_ROOT}/bin/harness_update.py" preflight
python3 "${CLAUDE_PLUGIN_ROOT}/bin/plugin_staleness.py" --loaded "${CLAUDE_PLUGIN_ROOT}"
```

## Check-first law — binding, not a suggestion

Always run `check` first and report its card, no matter why the skill was invoked. Run `apply`
only when the user has explicitly asked for a refresh in **this conversation** — being invoked
to look at freshness is not consent to write. If it is unclear whether the user wants a refresh
or just a look, run `apply --dry-run` and show the would-do plan rather than guessing either way.

## Refreshing the Claude plugin — preflight first, then the user's go-ahead

`claude plugin update` copies the checkout the plugin installs from — wholesale, ignoring
`.gitignore` — and copies nothing unless the version changed. Before relaying the refresh
commands, run `preflight` and report every gate it prints:

- Relay the commands only when it exits 0 (`verdict: ready`), and run them only on the user's
  explicit go-ahead in this conversation.
- `version-changed` failing means a bump comes first: `python3 bin/release_gate.py bump <next>`
  in the repo, which refuses on uncommitted work and never commits; the bump is then reviewed and
  merged like any change.
- `on-branch` or `clean` failing means someone is working in the install source. Report it; never
  switch its branch or clear its work to make the gate pass.
- `no-credential-files` failing names the file. It has to leave the checkout before the copy.
- `matches-marketplace` failing means the checkout that was vetted is not the one the update
  copies: the marketplace installs from somewhere else. Point the marketplace at the vetted
  checkout, or run `preflight` without `--source`, before trusting the other gates.

After the restart, confirm the session loaded the new copy with the `--loaded` line above:
`current` means done; `restart needed` means this session still runs an older cached version; `not
the installed copy` means a `--plugin-dir` session, which no restart changes.

## What `apply` can and cannot do

- **Copilot home:** overwritten in place — `install_copilot`'s own inherited behavior; the
  bundle's files are replaced, files it doesn't know about are untouched. State this plainly,
  it is not a no-clobber channel.
- **Codex home is two channels with different contracts** (corrected at P2 review — this is the
  load-bearing wording, never say "no-clobber" for the whole codex home):
  - `~/.codex/prompts/*.md` are plugin-generated deprecated mirrors and are **overwritten in
    place unconditionally** — every destination that differed before this run is listed and
    labeled, never a silent rewrite.
  - `AGENTS.md` and `codex/skills/<name>/` are user-editable and **no-clobber** — a differing
    destination is reported `skip-differs` and preserved; only mention "preserved" when the
    report actually lists something there.
  - Project-scope agent TOMLs (`<repo>/.codex/agents/*.toml`) and the modern plugin component
    are **outside apply's reach** — name this coverage limit explicitly and point at
    `harness_select install --harness codex` for those, rather than implying apply covers codex
    completely.
- **Repo generated mirrors** (pricing refs, codex prompt surfaces) are refreshed via the same
  sync scripts the repo already uses.
- **`~/.claude` is never written**, in any mode. For a stale Claude plugin cache, relay the
  framing line together with the remedy commands the engine prints — never the remedy alone.
  The remedy text itself opens with "stale install"; only the framing line makes that
  conditional on what `check` actually found, because `apply` reads no installed manifest and
  determines nothing about Claude freshness on its own. Note the commands take effect on
  restart, and only run them via Bash on the user's explicit go-ahead — never automatically.
  (The repo's own CLAUDE.md invariant against touching `~/.claude` binds unprompted work in
  this repo; a user's explicit go-ahead to run the printed remedy is the one sanctioned path,
  and the engine still never runs it itself.)

**Card-reading gloss:** in the codex section, the `install:` count comes straight from
`install_codex`'s own return shape and includes overwrites, not just new writes. The real signal
for how much actually changed is the `prompts differing before this run: N` line beneath it,
together with the listed destinations.

**A `preserved:` list under the copilot section is not a failure.** Those destinations were left
exactly as found because the installer does not own them, or because they were edited after
install. Report them and their reasons; the fix is the user's call, not `apply`'s. If they want
the bundle's version anyway, the command is
`python3 bin/harness_select.py install --harness copilot --adopt-existing`, which keeps each
prior file beside its destination as `<name>.polytropos-bak`. Never run it on your own initiative.

## What `check` cannot do

Pricing NUMBERS and docs snapshot TABLES are never auto-edited by this engine — a stale
`cached_date` or a stale docs label means a human refresh from the source data, both changed
together in one edit (the repo's CLAUDE.md rule). Point the user at `docs/REFERENCE.md`'s
"Updating prices" section for the `data/pricing.json` refresh runbook, and at `docs/COPILOT-HARNESS.md`'s own runbook lines for
the `data/pricing.copilot.json` refresh.

## Reading the card

- Exit code 3 means drift somewhere; the card's verdict line names which of the four sections
  (claude / copilot / codex / data) drifted.
- "not installed" is an absence, not a failure — report it as such.
- `whole tree:` in the claude section means every tracked file was compared, so a SHA STALE
  result has been settled one way or the other. SHA STALE itself appears only when git could not
  list the tracked files.
- `!! credential-shaped file inside the installed copy` is drift to fix now: that file sits in
  the plugin cache.
- A `cache:` line names other version directories that no update removes.
  `python3 bin/plugin_staleness.py` prints one `rm -rf` line for each; relay them, and run them
  only on the user's explicit go-ahead.
- An `unmanaged` result on codex is a warning worth mentioning, not an alarm.
- A codex `project agents: N not applicable here (install source)` line means `--repo-root` is
  the checkout the Claude marketplace installs from (its `known_marketplaces.json` record, the
  same one `preflight`'s `matches-marketplace` gate reads). That clone never carries
  `.codex/agents/`, so those agents are listed but not drift. Report them as not applicable;
  never install them there — an untracked `.codex/` would be copied into the plugin cache.
- A codex `conflict` count means destinations differ from what the bundle would write (an
  edited managed file, or an unresolved placeholder) — real drift, worth naming; a
  `managed-update` means a managed copy is waiting on a refresh.
- `apply` can also end `status: error` / exit 1 — a writer raised; the card carries the error
  verbatim. Report it plainly and stop; do not retry blind.

## Two things to warn about before pasting output anywhere

- `check --json` and `apply --json` are **different envelopes** — `check` emits four sections
  plus `status`/`exit`; `apply` emits `dry_run`/`targets`/`results`/`errors`/`status`/`exit`.
  Treat them as two separate shapes to parse, by design, never interchangeably.
- **Both embed absolute home paths** (install paths, Codex destinations, prompts overwritten,
  skip-differs entries), and so do two HUMAN cards: `apply`'s, which lists destination paths line
  by line, and `preflight`'s, which names the install source. `check`'s human card is path-free.
  Scrub paths before pasting any of these anywhere outward — a chat, an issue, a PR description,
  anything leaving this machine.
