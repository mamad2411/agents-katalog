---
name: upgrade
description: Move the current project to a newer dark-factory release on a work branch — update the template files with Copier, resolve the conflict markers, apply the project steps from each release's "How to upgrade" notes, and list the server steps for the owner in the PR. Invoked by the human as /dark-factory:upgrade [v<N>].
argument-hint: "[v<N>]"
disable-model-invocation: true
---

# /dark-factory:upgrade — move the project to a newer release

A release is the tag `v<N>` of https://github.com/ruslantrachuk/dark-factory with a GitHub Release whose notes end
with **How to upgrade**: the steps a live project or the server must do beyond the file update. Copier updates only
the base template's files; modules (On-call, monitor, release), server units and one-time transitions are in those
notes. This skill does both, on a work branch, and merges like any other change.

## Rules

1. **A work branch and a reviewed merge.** `chore/upgrade-v<N>` from a fresh main, a clean working tree, merge only
   through `scripts/merge-feature.sh`. The pin in `.claude/settings.json` and other fence files change here: their
   writes go through the permission dialog — the owner's yes is the decision to upgrade.
2. **Server steps are named, never run.** `fleet.py provision`, a line in `~/.config/dark-factory/fleet.env`, the
   user-level plugin update — they touch the whole server and are the owner's: list them in the PR's `## Upgrade`
   section and in the final answer.
3. **No conflict marker in a commit.** Resolve every one as `.harness/README.md`, "Updating" says.

## Steps

1. **Versions.** The project's release: `_commit` in `.copier-answers.yml`, else `.harness/base-sha` (`v<N>`; a
   commit SHA means it was copied from a canon checkout — `scripts/harness-diff.sh` first, then add
   `.copier-answers.yml` as "Updating" says). The target: the argument, else the installed plugin's version
   (`${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`, `<N>.0.0` → `v<N>`), else the latest release
   (`gh release list -R ruslantrachuk/dark-factory --limit 1`). Equal → say "on v<N>, nothing to do" and stop.
2. **Notes.** For every release after the project's up to the target:
   `gh release view v<k> -R ruslantrachuk/dark-factory`. Show the owner the list of releases and their "How to
   upgrade" steps, split into *project* (files, settings, docs in this repository) and *server* (provision,
   fleet.env, plugin update). Ask for a yes before changing anything.
3. **Branch and update.** `git switch -c chore/upgrade-v<N> origin/<main>`. **Crossing v24 (the rules layout):**
   before Copier, run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/migrate_agents_md.py"` — a dry run that prints the plan
   (`CLAUDE.md`'s sections into `AGENTS.md` around the canon block, `CLAUDE.md` → `@AGENTS.md`, skills into
   `.agents/skills/` behind the `.claude/skills` link, the session header into `scripts/agent/`). Show it to the owner,
   then run it with `--apply`; set `hooks.SessionStart` in `.claude/settings.json` exactly as it printed (a fence
   file: through the permission dialog), and commit `chore: v24 rules layout` before Copier. It stops without changes
   on an `AGENTS.md` that has text of its own — the owner decides which text the project keeps — and names what it
   left (a skill or script already at its new place, the project's own hooks). A Codex session finds the script in
   the installed plugin (`codex plugin list`). Then
   `uvx copier@9.19.1 update --defaults --conflict inline --vcs-ref v<N>` (without `uvx`:
   `pipx run copier==9.19.1 …`). Find the markers with `git grep -nE '^(<<<<<<<|>>>>>>>) (before|after) updating'` and resolve each: keep the project's
   configuration, take the canon's procedure text, carry the canon's meaning into text the project rewrote. A conflict
   on `.harness/base-sha` or the pin `"ref"` resolves to `v<N>`.
   Then look for duplicate keys, which Copier's text merge leaves without a marker: when the project keeps a block in
   another place than the template (in `.claude/settings.json` typically `extraKnownMarketplaces`/`enabledPlugins`
   after `permissions` and `hooks`), the template's change lands as a second copy of the block, and a JSON reader
   silently keeps the last one — the old pin. Check every changed JSON file:
   `python3 -c 'import json,sys; [json.load(open(f), object_pairs_hook=lambda p: (len(p)==len({k for k,_ in p}) or sys.exit(f+": duplicate key in "+str([k for k,_ in p]))) and dict(p)) for f in sys.argv[1:]]' $(git diff --name-only HEAD -- '*.json')`.
   Merge each duplicate into one block and move it to where the template has it, so the next update merges cleanly.
4. **Project steps.** Apply each project step of the notes, in release order. A step that needs the owner (a secret,
   a GitHub setting) goes into the PR as an open question, not around them.
5. **Check.** Run the project's gates (the fast test suite and linters its AGENTS.md names). After v24:
   `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/canon_block.py" check AGENTS.md` is current and `scripts/harness-diff.sh`
   shows `identical  AGENTS.md#canon`. On a red gate, fix what
   the update broke or stop and report; never skip a test.
6. **PR.** Commit, push, open the PR with `## Done` (releases crossed, files updated, markers resolved, project steps
   applied), `## Decisions`, `## Open questions`, and `## Upgrade` listing the server steps for the owner. Merge with
   `scripts/merge-feature.sh` once CI is green. After the merge, start new sessions: a running one keeps the old
   rules (`/dark-factory:factory-status` flags worktrees behind main).
7. **Verify the install, not the update output.** After the owner's server steps, the plugin must be *installed* for
   this checkout, not only enabled in `.claude/settings.json`: `/dark-factory:factory-status` shows `● plugin`, and
   the SessionStart line says "enforced", not "dark-factory NOT LOADED". `plugin update` answers "already at latest"
   for a project that has no install at all — its output proves nothing. A missing install is fixed by
   `claude plugin install dark-factory@dark-factory --scope project` in the project's main checkout and a restart of
   its sessions; list that step in `## Upgrade` whenever the server steps re-add the marketplace or move the pin.
