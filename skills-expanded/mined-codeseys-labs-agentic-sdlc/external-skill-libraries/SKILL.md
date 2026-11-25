---
name: external-skill-libraries
description: |
  Install a THIRD PARTY's skill library (ECC, mattpocock/skills, hyperresearch) through that
  library's OWN front door, opt-in and never automatically. Use when: (1) someone asks to
  install, add, update, remove, or check an external/foreign skill library or marketplace
  plugin; (2) a skill name appears twice or the wrong copy loads, and you need the
  collision/duplicate-channel diagnosis; (3) deciding whether a foreign catalog is worth its
  always-on selection-surface cost. Covers the per-library front door and its evidence, the
  first-writer-wins name rule, dry-run-by-default with an explicit --yes, and why this bundle
  never copies upstream bytes (so no NOTICE obligation). NOT for authoring or admitting a
  skill into THIS bundle — the `agentic-sdlc` skill's skill-authoring reference owns whether a
  skill should exist at all, and adapting a foreign IDEA into this repo's own prose. This
  skill installs foreign libraries wholesale into a home; it never vendors, never adapts, and
  admits nothing to this repository.
---

# External Skill Libraries

Install a third party's skill library by running **that library's own installer**, as an
explicit operator step. Read this when a library is wanted, when a name collides, or when
someone asks whether a catalog is worth its cost.

The tool is `scripts/install_external_libraries.py`, wired as four mise tasks. Its supported
catalog is closed and exhaustive: `mattpocock/skills`, ECC (`affaan-m/ECC`), and hyperresearch.
An unlisted library—including gstack—is operator-owned foreign state until a separate verified
onboarding change lands; these tasks do not adopt, inspect for ownership, migrate, or remove it.


```bash
mise run libraries:list      # what is available, its front door, its cost, what is detected
mise run libraries:status    # what is already present in this home
mise run libraries:install   # refuses without an explicit library name
mise run libraries:migrate   # retire another channel's copies of the SAME upstream, then install
```

`install`, `migrate`, and `uninstall` take **explicitly named libraries only**. There is
deliberately no verb that installs everything, and none of these verbs is reachable from
`lifecycle:install`, `lifecycle:install:claude`, `lifecycle:install:codex`, `contributor:setup`, its
deprecated `setup` forwarder, or any gate leaf.

Every library is reachable. `list` prints a `reach it by:` line per library with the exact
command, so a refusal names its own route out rather than reading as a dead end. The states are
`installable`, `installable after migration` (another channel provably holds the same upstream),
`installable accepting duplication` (it holds some names unprovably, so only
`--allow-duplicate-channel` clears it), `installable behind <flag>` (a cost to acknowledge), and
`blocked` — reserved for a library that cannot be honestly run at all, which no library is today.

## The distinction that makes this safe

**Invoking a third party's own installer is not vendoring.** No bytes from any library enter
this repository, so no `NOTICE` donor obligation attaches and no upstream licence text
travels with anything here. Each library writes into the operator's own home, under its own
names, by its own code.

That is the whole difference from the vendoring question, which is settled separately and
stays settled: this bundle still ships only its own skills, agents, and commands, and a
foreign **idea** still enters this repository only as an adapted `references/*.md` file with
a `NOTICE` donor entry. See `docs/adr/0009-external-skill-libraries-are-opt-in-through-their-own-front-doors.md`,
which supersedes in part the blanket "never install" position in
`docs/adr/0008-third-party-skill-libraries-are-the-operators-own-install.md`.

Two costs survive the distinction, and they are why this skill exists rather than a one-line
instruction to run the installer:

1. **Selection-surface pressure.** Every skill a library adds is a row an agent reasons over
   on every turn it selects a skill. This is the cost that does not show up in any diff.
2. **Name collision.** Skill names are one flat namespace per home. First writer holds the
   name; the loser's entry is silently not the one that loads.

## The three libraries, honestly costed

| Library | Surface | Channel | Front door(s) |
|---|---|---|---|
| `mattpocock` | 25 skills | plugin (namespaced), **or** flat via the CLI door | **two doors, split by prerequisite.** `claude plugins install mattpocock-skills` needs an **authenticated** Claude Code session; `npx -y skills@latest add mattpocock/skills --global --agent claude-code --skill '*' --yes` needs none |
| `ecc` | 284 declared / 280 measured skills, 67 agents, 94 commands | flat `~/.claude/skills/` | `npx -y -p ecc-universal ecc install --target claude --profile full` |
| `hyperresearch` | 17 skills + 16 agents, rendered | flat, `hyperresearch`-prefixed | `uv tool install hyperresearch` |

**ECC's surface is the headline.** Against this bundle's 12 skills, 284 entries is a ~24×
multiplication of what a selector must reason over, in exchange for a firing rate nobody has
measured for any individual entry. It writes flat into `~/.claude/skills/<skill-name>/` — the
same namespace this bundle's entries occupy — so every name is a first-writer-wins claim. It is
gated behind `--acknowledge-ecc-surface`, which is about **cost**, not version.

Two ECC facts are easy to get wrong, and both were verified against the published artifact
rather than the README:

- **The README's front door does not exist.** `npx ecc-universal setup` cannot run: the
  published 2.1.0 tarball declares no `ecc-universal` bin and `ecc` has no `setup` verb, so npm
  exits "could not determine executable to run" regardless of any version question. The wired
  front door is the artifact's real one, `ecc install --target claude --profile <name>`, which
  refuses outright unless given a profile.
- **The version gap is accepted, not resolved.** ECC's README documents guided commands
  requiring 2.2.0+ while npm's `latest` serves 2.1.0. The operator accepted npm `latest`; the
  gap survives as a printed caveat on every dry run, and a front-door failure is reported as a
  failure rather than assumed to be a finished install.

Its surface cannot be enumerated offline, so `--names-from` remains available for a real
precheck and its absence is reported as **`precheck: SKIPPED, not passed`** — never as a pass.
The honest enumeration is ECC's own `--dry-run --json` plan, which lists every destination path
it would write; `list` prints that command. Against the resolved `full` profile it measures 983
file operations: 280 flat skill names, 67 agents, 94 commands, 122 rules files, 170 scripts.
`--profile` accepts six narrower profiles (`ecc catalog profiles --json`) for a smaller surface.

**mattpocock is cheap by an order of magnitude** — 25 versioned entries — and it has **two
legitimate front doors that differ in prerequisite, not in payload**. Because the plugin door is
namespaced it cannot *lose* a name; its failure mode is the opposite one, duplication, which
upstream names itself: "Pick one — installing both leaves you with every skill twice."

- **The marketplace door needs an authenticated Claude Code session, and upstream does not say
  so.** Its README calls the official marketplace already listed, so there is no `marketplace
  add` step — true only once a session is logged in and that marketplace has registered.
  Executed 2026-08-20 on a logged-out Claude Code 2.1.238: `claude plugin marketplace list`
  prints "No marketplaces configured" at exit 0 and `claude plugins install mattpocock-skills`
  fails not-found-in-any-configured-marketplace. The bundle's own task behaved correctly there —
  real command, real exit code, install reported FAILED, no false success — but a not-found is a
  dead-end-looking message for a library that is not a dead end. So `list` and `install` read the
  marketplace state offline from `~/.claude/plugins/known_marketplaces.json`, keep the
  marketplace door **primary** whenever at least one marketplace is configured (a missing
  `claude` binary is reported by its own front-door-tool line, not by this check),
  and otherwise print the prerequisite plus a `DIRECTED:` line naming the other door. When the
  door fails with none configured, the failure hint names **both** halves: the
  authenticated-session prerequisite and the exact alternative command.
- **The `skills` CLI door needs no Claude session at all**, and both its runners come from tools
  this repo already pins (`npx` from node, `bunx` from bun), so it adds no prerequisite. Its
  grammar was read off the CLI itself — `npx -y skills@latest --help`, CLI 1.5.23 — not a README:
  `add <package>` with `-g/--global`, `-a/--agent <agents>`, `-s/--skill <skills>` ("use `'*'` for
  all skills"), `-y/--yes`. There is no per-subcommand help; `add --help` reprints the same page.
  Those three scoping flags are what make it noninteractive, and `--agent claude-code` is the
  same one-host scope the removal front door uses.
- **That door is printed, never invoked by this tool.** It writes flat names the operator owns
  into `~/.claude/skills/`, so it is governed by the **flat-channel** collision rules, not the
  plugin-channel ones the precheck applied. Running it from here would install behind a precheck
  that never looked at its namespace — the silent loss this module exists to prevent — so the
  operator runs it deliberately. When that channel already holds the names, `migrate` is the
  route instead: see below.

**hyperresearch is not a skill library at all.** It is a CLI that *renders* skills and agents
into a home or a project. Installing the tool writes no skills; its own `hyperresearch
install` verb does (`--global` for the home). Every name it writes is `hyperresearch`-prefixed,
so its collision surface against this bundle is structurally empty rather than merely
observed to be empty.

**Its 16 agent files are a recorded set, not a live enumeration, and that distinction bit once.**
This front door exposes no verb that lists what it renders — `hyperresearch --help` at 0.10.0
offers install/setup/init/status/… and nothing else, and `install --help` has no `--dry-run` — so
the expected set can only be recorded from an executed install (`hyperresearch install --global`,
then list `~/.claude/agents`; 16 files, v0.10.0, 2026-08-20). The list here stood at 14 against
that **same** upstream version, missing `hyperresearch-browser-fetcher` and
`hyperresearch-cite-checker`, so `status` reported a truthful `14/14` while understating the real
selection surface by two files. Two things now catch the next drift instead: the set is pinned in
`tests/test_external_libraries.py` against the version it was recorded from, so a change fails a
named test rather than nothing; and `status` reports any further `hyperresearch`-prefixed agent
file the recorded set does not name, so a home wider than the record says so on the operator's own
machine. Re-record both sides together — never reconcile by editing one.

Its rendered agent files carry static `model:` frontmatter, which this
repo's validator rejects for agent files — a reason never to vendor its output, not a reason
to refuse to run its renderer in a home, where this repository's validator has no
jurisdiction.

## The collision rule

Before invoking any front door, enumerate the names the library will write and compare them
against (a) this bundle's own skill names and (b) what already occupies the target home.
Then:

- **Collides with a name this bundle installs** → refuse **that library**, not the whole run.
- **Flat-channel name occupied by another writer** → refuse. The library would lose or clobber.
- **Occupied under the library's own name prefix** → a reinstall, not a collision. Proceed.
- **Plugin-channel name already present via another channel** → refuse as duplication,
  overridable with `--allow-duplicate-channel` once the operator accepts it deliberately.
- **Surface not enumerable** → refuse. A precheck that cannot run is not a precheck that passed.

A symlink counts as occupying a name. An entry another installer linked into place holds the
name just as firmly as a real directory, and reading it as absent is exactly what produces a
silent loss.

## Migration: same upstream, different channel

The duplicate-channel refusal is not a dead end. When the names are held by **another channel
serving the same upstream**, removing them is de-duplication rather than capability loss, and
`migrate` does it through that channel's own front door:

```bash
mise run libraries:migrate -- mattpocock          # prints the proof and the exact command
mise run libraries:migrate -- mattpocock --yes    # removes, re-checks, then installs
```

**Provenance is the whole licence for a removal.** Filesystem presence proves presence, not
provenance, so `migrate` consults the *other channel's own lock file*
(`$XDG_STATE_HOME/skills/.skill-lock.json`, else `~/.agents/.skill-lock.json`) and matches each
occupied name's recorded `source` **and** `sourceUrl` against the library's upstream. Anything it
cannot prove, it leaves alone:

- No lock file, an unreadable one, or one at a schema version older than the channel's own
  reader accepts → **refuse**. An unavailable proof is not a passed one.
- A name absent from the lock → **refuse that name**. Occupied but unattributable.
- A name recorded against a different `source`, or the same short name with a different clone
  URL → **refuse that name**. A label is not an identity.
- Any unproven name at all → **refuse the whole migration** rather than half-doing it.

The removal runs `npx -y skills@latest remove --global --agent claude-code --yes <names…>`.
Two scoping choices matter. `--global` because the names are in a home. `--agent claude-code`
because without it that command targets **every** agent it knows: it deletes the canonical
`~/.agents/skills/<name>`, every other agent's link to it, and the lock entry. Scoped to one
agent it removes only `~/.claude/skills/<name>` and leaves the canonical copy, the other hosts'
links, and the lock intact — so resolving a Claude Code collision does not take the skill away
from Codex, and the change is re-linkable.

**This module never deletes anything itself.** No `rm`, no `unlink`, no path touched directly;
the other channel's own verb does the work. Ordering is enforced: removal, then a **fresh
precheck against the real filesystem**, then the install. If removal fails, or if it reports
success while names are still occupied — a partial removal — `migrate` **stops before
installing** and says what remains. Installing over a still-occupied name is exactly the silent
loss the precheck exists to prevent.

The precedent is `scripts/install_skill_bundle.py`, which classifies an entry it does not own
at a managed path as `foreign` and **preserves** it rather than replacing it. That makes
coexistence the default in one direction — a foreign entry survives this bundle's install.
The precheck covers the direction that classifier structurally cannot see: a foreign entry
that took a name *first* blocks the entry that wanted it, from the other side, with no error
for the operator to notice.

## Invocation

Dry run is the default and prints exactly what will run, from where, at what version, and how
many skills it adds. `--yes` is required to invoke anything.

```bash
mise run libraries:install -- mattpocock            # prints the plan, runs nothing
mise run libraries:install -- mattpocock --yes      # invokes the front door
mise run libraries:migrate -- mattpocock            # when another channel holds the names
mise run libraries:install -- ecc --acknowledge-ecc-surface                      # precheck SKIPPED
mise run libraries:install -- ecc --acknowledge-ecc-surface --names-from /tmp/ecc-names.txt
```

Enumerate a library's names with the command `libraries:list` prints for it, never by
guessing. `uninstall` runs the library's own documented removal path or refuses; it never
deletes a path it did not see that library's installer create. ECC's published artifact does
expose `ecc uninstall --target claude`, scoped to what its own install-state recorded, so it is
wired.

## Exit codes: describing is not doing

A dry run and a real install are different operations, and they no longer share an exit path.

| Code | Means |
|---|---|
| `0` | The operation did what it was asked to. For a dry run that **includes describing a refusal** — "these 21 names are occupied", "`claude` is not on PATH, so a real install would refuse". |
| `1` | A real (`--yes`) operation was asked to change something and could not: refused precheck, missing front-door tool, or a front door that exited nonzero. |
| `2` | The invocation itself was unusable — no library named, unknown library, unreadable name list. |

So `libraries:install -- <lib>` without `--yes` exits **0 on any machine**, including one with no
`claude`, no `npx`, and no installed tools, because "the front door is missing" is a fact it
reports rather than a failure it suffered. The refusal is still printed in full, and the dry run
says which case it is.

This was a real defect, not a preference: the old code failed a dry run whenever any refusal
fired, so `mise run check` passed on a developer host that happened to have `claude` on PATH and
went red on a clean machine. Reading a nonzero dry-run exit as "the tool broke" was the confusion.
A real `--yes` install with a missing front door still exits nonzero — that half is asserted
separately so the fix cannot decay into blanket leniency.

## A library with no front door: the ported class (pstack)

Everything above is the **front-door class**: a library reachable because it publishes its own
installable front door, which `install_external_libraries.py` invokes without copying a byte.
Some libraries worth onboarding have no such front door at all — nothing for that script to
invoke — and forcing one into the closed catalog above would misdescribe what actually happens.
`docs/adr/0029-ported-libraries-are-a-second-external-library-catalog-class.md` names that
second class **ported libraries**, and refines rather than supersedes ADR-0009: the closed
three-row catalog, its mechanism, and its boundaries above are unchanged by it.

`pstack` (`github.com/cursor/plugins/tree/main/pstack`, a Cursor-native workflow plugin) is the
first, and so far only, ported-class member. It has no Claude Code front door — no marketplace
plugin, no npm or PyPI package targeting this host — so onboarding it means executing
`references/porting-a-foreign-plugin.md`, the recipe this skill already ships, against a
**pristine read of upstream HEAD** (never against a working copy a prior port has already
modified — that recipe's own checklist item 9), with the exact upstream commit read **recorded**
as a pin per ADR-0029. The ported result lands in the operator's own plugin tree, under the
operator's own ownership, registered through a local marketplace the operator points at their
own checkout — never inside this repository; where the executed 2026-08-19 port landed is
recorded in `docs/progress/2026-08-19-pstack-claude-code-port.md`. Re-porting on a later
upstream change is a fresh recipe run against the new pristine HEAD with a new recorded pin,
never a channel update, because there is no channel to subscribe to.

The same three boundaries this skill applies to the front-door class apply here, unchanged:
**no vendoring** (the ported plugin's files stay in the operator's home; nothing from
`cursor/plugins` is copied into this repository, and no `NOTICE` entry is owed for it — this
skill's own section and the recipe re-express the pattern in this bundle's own words rather
than quoting the ported plugin's files); **name collision** is the operator's own, resolved in
their own plugin tree by their own host's install/upgrade behavior, not by this skill's
precheck, which only reasons about `install_external_libraries.py`'s destinations; **no
installer-task automation** — ADR-0029 creates none, so there is no `libraries:*` verb, no
`mise` task, and no addition to the closed catalog above for the ported class or for pstack
specifically. Automating a port is a separate, not-yet-made decision.

## Standing boundaries

- **This bundle never vendors upstream bytes.** No file from any library is copied into this
  repository, under any name, at any time.
- **No credential handling.** No token is read, written, stored, forwarded, or accepted as an
  argument. A front door needing one is authenticated separately by the operator.
- **No network trust claim.** The tool makes no request of its own. The front-door subprocess
  does, under its own package manager's integrity model. Nothing here verifies a tarball, a
  signature, or a transitive dependency.
- **No new bootstrap prerequisite.** Front doors use tools that are already present or
  already pinned (`uv`); the tool installs no tool of its own and refuses by name when one is
  missing. `mise run check` stays green on a host that has never run any of these tasks.
- **Installing is not endorsing.** A listed library is reachable, not recommended. Licence,
  provenance, and content review remain the operator's.
- **A successful install is evidence, not authorization.** It authorizes no push, no
  publication, no merge, no deployment, and no further install.

## Cross-links

- `references/library-front-doors.md` — the per-library front door with the exact doc line it
  came from, the version facts, and the enumeration command for each surface.
- `references/collision-precheck.md` — the name-collision rules, the installer-ownership
  precedent they build on, and what each refusal means.
- The `agentic-sdlc` skill's `skill-authoring` reference — owns whether a skill should exist
  in **this** bundle, and the adapted-reference path for a foreign idea. This skill never
  admits anything to this repository; that file never installs anything into a home.
- `docs/adr/0009-external-skill-libraries-are-opt-in-through-their-own-front-doors.md` — the
  decision and its evidence.
- `docs/adr/0002-mise-is-the-single-front-door.md` — the prerequisite rule these front doors
  must not raise.
- `references/porting-a-foreign-plugin.md` — the recipe the ported class points at: manifest
  relocation, primitive substitution, the pristine-HEAD-only evidence rule, and what porting
  deliberately does not make safe.
- `docs/adr/0029-ported-libraries-are-a-second-external-library-catalog-class.md` — the
  ported-class decision, pstack as its first member, and why it refines rather than
  supersedes ADR-0009.
