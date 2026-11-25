---
name: formal-init
description: Sets a project up for the formal plugin — `formal.toml` over its Lean workspace, the manifest generator in the workspace, the prover session's standing instructions, the `formal-check` hook and the document gates' hooks — and checks an existing setup. Use as `/formal:formal-init`, or when asked to set up the prover side, the formal plugin or the handoff and landing of Lean work in a project. Probes the workspace, the project and the machine with `formal probe`, proposes what is missing and installs it only on the person's word, re-checks on every run what exists against the workspace as it stands, adds what is missing on the person's word and rewrites nothing without it, and reports. When the person says 'formal-init' or 'set up the prover side', they mean this skill — call it every time, even if it ran earlier in the session, and take every step.
license: Apache-2.0
compatibility: Python 3.11 or later for `scripts/formal.py` of the `land` skill; git; the prover, its build and `lake` are the project's, proposed when absent.
metadata:
  version: "0.12.1"
  requires: land
---

# Setting the prover side up

The prover side is what the `handoff` and `land` skills need: a workspace the probe can name, `formal.toml` binding it, a declaration manifest the landing reads and the flow asks about, the standing instructions the prover session reads first, and the check as a hook.
`formal probe` (the `land` skill's `scripts/formal.py`) is the evidence; it writes nothing and installs nothing.

## What a setup is

Required, since a handoff or a landing does not run without it:

- a Lean workspace under the project root with its lakefile, `lean` and `lake` on PATH;
- `formal.toml`, written by `formal init --workspace DIR`, its `[packages]` naming each library root the probe found, one manifest per package and `[manifest] generate` the command that writes each;
- `DeclManifest.lean` in the workspace, copied from the `land` skill's `scripts/`, and the manifest it writes after a build, since `formal check` and the landing read it, and `formal resolve`, which the flow asks, answers from it;
- the prover session's standing instructions at the path `formal.toml` names, from `references/workspace-instructions.md` of the `handoff` skill, its angle-bracket slots filled;
- the `formal-check` hook beside the flow's and the library's.

The formal plugin runs on its own: with no research setup (no `flow.toml`, no `library.toml`) the handoff and the landing work from the document rows and the commit, and `formal.toml`'s record bindings stay empty; where the research plugin is set up, the setup reads its bindings to fill its own, and the flow, finding `formal.toml` at the root, asks the plugin's `formal resolve` for its formal evidence, with no binding to write in `flow.toml`.

Recommended: the prover's language server registered in the project's `.mcp.json`, since the prover agent uses whatever prover tools are registered and works blind without them; `elan`, which installs `lean` and `lake` at the workspace's pin.

## The procedure

1. Probe.
   Run `formal probe` from the project root (`--root DIR` for another; `--json` for the same as data) and read the whole report: the tools, each workspace with its package, roots, toolchain and generator (present, absent, or stale where the workspace's `DeclManifest.lean` differs from the `land` skill's copy, a release having changed it), the project's bindings and its pins, the proposals, the coverage line.
   The project's item `pins at one tag` holds the hooks' `rev`, the marketplace's `ref` in `.claude/settings.json` (to be `latest`, which each release moves to its tag; a tag or no ref is off), the version of each research-kit plugin Claude Code installed for the project (its install record `~/.claude/plugins/installed_plugins.json`; where that is absent the item says so; a linked git worktree reads the install of the main work tree as its own) and this plugin's version to the kit's latest release, which the probe asks GitHub for, and where one is off, the proposal `pins` lists the releases from the oldest pin up to the latest whose **Upgrading** paragraphs to read and the steps that move every pin to it, as the research plugin's setup probe does.
   The probe asks with one retry after a timeout; where the latest release cannot be read, offline, refused or with `RESEARCH_KIT_OFFLINE=1` set, the item says so and why, and compares the pins among themselves, against the newest of them; a pin file with uncommitted changes is named, since a clone reads its committed pin.
   The item `flow.toml` appears where the research setup is absent, as information and never a refusal; the marker `[kit] release` is the research setup's, read by its own probe, and the two plugins are kept at one version by the `pins` step.
A lakefile under a workspace's directory, or one it requires by path, is a package of that workspace, listed under it, never a workspace of its own: the generator goes into the workspace once and runs there for every package, since Lake started inside a nested package resolves that package alone.
2. Plan, in one message.
   Say which workspace the setup binds (ask when the probe found several), what exists and is left alone, what will be written, and what is missing with the proposal for each; ask the person once, in one question, through the agent's question tool where it has one and in the turn otherwise: which proposals to install, and the slots of the instructions the probe cannot fill (the exact commands that re-verify a module, the build time, where the audit modules live).
   Install nothing and register nothing before the answer; in a run nobody can answer, write what the defaults allow and list the rest as left to the person.
3. Install what was chosen, with the proposal's command as shown, then run the probe again.
4. Write the bindings.
   `formal init --workspace DIR` where `formal.toml` is absent: it fills `[packages]` with every root the lakefiles declare, each at its package directory, one manifest and one generate command per package, with no `--own` (the generator's default reads a condition defined in another package of the workspace as a named one, and `formal check` holds the roots it took against `[packages]`), and `package_order` from the requirements.
   It takes what the project already says: `[workspace] instructions` is the instructions file the workspace has (`AGENTS.md`, else `CLAUDE.md`); the manifests are `scripts/decls.txt` for one package and `scripts/<package>-decls.txt` for several, and the generate commands write those; `[handoff]`'s `records`, `id_prefixes` and `meta_names` come from `flow.toml`'s `[paths]` and `[prefixes]`, and `key_patterns` from `library.toml`'s cite prefix, each only where that file exists and binds it and empty otherwise; it prints each binding it took that way.
   Where `formal.toml` exists and `flow.toml` or `library.toml` has come since, its empty `[handoff]` bindings are compared with what those files bind and the ones to fill are proposed on the person's word.
   Read what it wrote against the probe, and bind `[documents]`, `[anchors]` and `[register]` from the project's own gates where it has them; `--force` only when the person asks for the file to be rewritten.
   In `[register]`, a scrub of words that must not ship is a pattern class (`[[register.class]]`), and a check that a lower package names only files of its own or of the packages below it is a file class (`[[register.files]]`), whose `allow` matches another project's files as the mention is written, so a bare name and a path each need their own expression (`^Average\.lean$`, `^Mathlib/`).
5. Place the generator.
   Copy `scripts/DeclManifest.lean` of the `land` skill into the workspace where it is absent, never into a package inside it, and leave the manifests to the prover's first run after a genuine build, as the report says.
   Where the probe reports the workspace's generator stale, replace it with the `land` skill's copy on the person's word, as the proposal `generator of DIR` shows, and regenerate each manifest with the project's `[manifest] generate` commands, run in the workspace after a build: a manifest written by the older generator lacks what the new one writes.
   A difference that is the project's own edit, kept on purpose, is left in place when the person says so.
6. Write the instructions.
   Where the file `formal.toml` names is absent, write it from `references/workspace-instructions.md` of the `handoff` skill with the slots filled from the probe and the answers; where it exists, re-read it against the template and the workspace, add what it lacks on the person's word, and name what is stale with the edit proposed.
   The paragraphs for the project's own instructions file are compared the same way, against what `formal init --print-instructions` prints for `formal.toml` as it stands, writing nothing.
7. Add the hook.
   Add `formal-check` to the kit's block in `.pre-commit-config.yaml`, and `formal-cite`, `formal-anchors` and `formal-register` where their bindings are filled.
8. Verify and report.
   `formal check`, and `flow check` where the research plugin is set up; a manifest not yet generated is a problem `formal check` reports and leaves the flow's formal items unchecked, named in the report as the prover's first move with the generate command; then what was written, installed and declined, and the first handoff as the next step.
   Where the plugin was installed in this session, the report says that the `formal:prover` agent type is loaded when a session starts and appears after a restart; until then a handoff takes the `handoff` skill's general-purpose fallback.
9. Propose one commit.
   Name the files this setup wrote or changed, by path, and ask the person once, through the agent's question tool where it has one, whether to commit them, with the message `research-kit set up`; on a yes, stage those files alone and commit.
   The setup initialises no repository unasked: where the folder is none, say so in the report and leave the commit.

## Rules

- Nothing is installed or registered without the person's word; a proposal is shown as the command or the entry that would be written.
- Every run re-checks everything the setup covers that exists — `formal.toml`, the instructions file, the generator, the hooks — against the workspace as it stands, and adds what is missing; a project set up before is never taken as done because its files are present.
- Nothing that exists is overwritten without the person's word: `formal.toml` (`--force` only when they ask), the instructions file, the generator, a hook block naming `formal-check`; what is stale in one is named with the edit proposed.
- The probe is the evidence: a root it did not read from the lakefile is not invented, and a slot it cannot fill is asked, never guessed.
- A workspace never learns of the project's records through this setup: the instructions file carries the prover session's rules and nothing of the records or the documents beyond the bans `formal.toml` names.
