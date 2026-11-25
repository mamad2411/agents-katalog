---
name: skills-manager
description: Work with Agent Skills stored in a Library managed by the `skills` CLI (Skills Manager). Covers finding the Library root, writing or editing skills in it, importing from Git, archives, or local paths, tags, presets, deploying to agents, upstream updates, health repair, and Git backup. Use when creating, editing, installing, organizing, deploying, or updating a skill, or when a request mentions the skills Library, `SKILLS_HOME`, or a `skills` command.
---

# skills-manager

Skills Manager keeps every skill in one directory, the **Library**. `skills deploy` makes a skill available to an agent by putting a symlink to it in that agent's skills directory (for example `~/.claude/skills`). So a new or edited skill always goes into the Library, and an agent sees it only after it is deployed there. Real directories that already sit in an agent folder are reported separately and can be adopted into the Library.

Two references hold the detail. Open them when the task reaches them:

- [references/library.md](references/library.md): the Library's folder structure, where a skill may live, `SKILL.md` rules, every skill status, and what is safe to edit by hand.
- [references/cli.md](references/cli.md): every `skills` command with its flags, `--json` output, which commands need `--yes` or support `--dry-run`, and exit codes.

Run every command with a subcommand. Bare `skills` opens the interactive TUI, and `skills note edit` opens an editor; use `skills note set` instead.

## 1. Find the Library root

Use the root the manager itself would use. It resolves the root in this order and stops at the first one that is set:

1. `--root DIR` on the command line. The program does not expand `~` here; the shell must.
2. The `SKILLS_HOME` environment variable, if it is set at all. An empty value still counts and fails; it does not fall through.
3. The contents of `~/.config/skills-tui/root`, trimmed. The file must hold only the path. A leading `~/` is expanded.

Confirm the result with the manager instead of guessing:

```sh
skills status              # first line: "root: <absolute path>"
skills --json status       # the "root" field
```

Both run a full scan. Read the exit status of `skills` itself; piping it into `head` hides a failure. If it fails with `skills root not set`, `skills root does not exist`, or `skills root is not a directory`, stop and ask the user for the Library path. Do not pick a likely-looking directory such as `~/.skills` or an agent's skills folder. Once the user gives a path, pass `--root PATH` to every command in the session, and offer to persist it (`export SKILLS_HOME=PATH` in their shell profile, or the path written into `~/.config/skills-tui/root`) only if they want that.

If `skills` is not installed, resolve the root by hand with the same three steps, tell the user the CLI is missing, and do the file work without it; the install script is linked from the project README.

A project can also have its own store at `<project>/.agents/skills`. Use it only when the user asks for a project-only skill: CLI commands then take `--local` (current directory) or `--project DIR` in place of `--root`. See [references/library.md](references/library.md#project-stores).

## 2. Orient before changing anything

1. If the root contains `AGENTS.md` or `CLAUDE.md`, read it. The Library owner's conventions (language, naming, review rules) override the defaults in this skill.
2. Run `skills status` for the overview: skill counts by status, configured agents, and what is deployed where. `skills list` searches it (see the reference for query filters).
3. If the root is a Git repository, run `git -C <root> status --short` and leave changes you did not make alone.
4. Run `skills sync status`. If it prints `"enabled": true`, read **Automatic backup** below before running any command that changes the Library.

## 3. Do the task

### Create a new skill

1. Search first: `skills list <keywords>`. Extend a close match rather than adding a near-duplicate, and pick a `name` no other skill declares; two skills with the same declared name collide when deployed to the same agent.
2. Choose the location. A flat skill goes at `<root>/<name>/SKILL.md`. To group skills in folders, put them anywhere under `<root>/local/`, for example `<root>/local/writing/<name>/SKILL.md`. Folders anywhere else are not scanned for nested skills, and `repos/` is reserved for installed sources. Details in [references/library.md](references/library.md#where-a-skill-can-live).
3. Write `SKILL.md`:

   ```markdown
   ---
   name: <name>
   description: <what the skill does>. Use when <case>, <case>.
   ---

   <instructions for the agent>
   ```

   `name` is 1 to 64 characters of lowercase ASCII letters, digits, and single hyphens, with no hyphen at either end. Match the directory name to it unless the user wants otherwise. The manager accepts an empty `description`, but agents decide whether to load a skill from it, so always write one that names the cases that should trigger the skill. Put helper files in `scripts/`, `references/`, or `assets/` next to `SKILL.md` and link them with relative paths. If a `writing-for-agents` skill is available, use it for the wording.
4. Verify (step 4 below). The manager picks up the new directory on its next scan; no registration command is needed.

### Bring in an existing skill

- A directory elsewhere on disk: `skills install PATH` copies it and leaves the original; `skills adopt PATH` moves it in and deletes the original. When PATH sits directly inside a configured agent's skills directory, `adopt` puts a symlink to the Library copy where the original was, so that agent keeps working. Both accept `--name KEY` to choose the Library name.
- A Git repository or archive: preview with `skills install REF --list`, then install the chosen paths with `--select PATH` (repeatable) or `--all`. Name the storage folder with `--repo-alias ALIAS`. A new archive URL also needs `--source-name NAME`. Installed skills land in `repos/<alias>/<name>` and record their source, revision, and content hash. Before installing third-party skills, read their scripts and license, and install only the ones the user asked for. If the source holds several skills and nothing is selected, the command lists them and installs nothing.

### Edit an existing skill

Find its directory with `skills show KEY` (the `path:` line), then edit the files there. What the edit means depends on the status `show` reports:

- `local`: edit freely. Nothing else needs updating while `SKILL.md` stays valid.
- `repository`: the skill came from an upstream source. Any file change turns it `modified`. Tell the user, because the next `skills update --take upstream` (or `--force`) replaces the whole directory with upstream content and discards local files. After the edit, `skills accept KEY` records the current content as the new baseline when the user wants to keep it.

Use the CLI rather than file operations for structural changes:

- Rename the Library key with `skills rename OLD NEW`. It moves the folder and rewrites metadata, tags, presets, and deployment links; renaming by hand breaks all of those. It does not change the `name` in `SKILL.md`.
- Delete with `skills remove KEY --yes`, which also undeploys the skill and removes it from tags and presets.
- If you change the `name` in a deployed skill's frontmatter, its existing agent links keep the old name and `skills status` reports them as `foreign`. `skills repair` previews renaming them, and `skills repair --apply` does it.

### Organize, deploy, update, repair, back up

These follow the same pattern: preview, apply, verify. Full syntax is in [references/cli.md](references/cli.md).

- Tags (`skills tag add KEY TAG...`) are named groups that also work as search filters; reuse an existing one from `skills tag list` where it fits. Presets (`skills preset create NAME --skill KEY...`) are fixed bundles you deploy together.
- Deploy only to the agents the user names: `skills deploy KEY --agent AGENT --dry-run`, then the same command without `--dry-run`. `skills agents list` shows configured agent keys. The link is named after the frontmatter `name`, not the Library key. If the dry run reports `name_conflicts`, ask the user before rerunning with `--same-name replace`.
- Updates: `skills check --all` compares recorded revisions with upstream; `skills update KEY --dry-run` previews. Running `update` on a `modified` skill reports `needs-resolution` until you choose a side: `--take local` skips the update and leaves the skill `modified`, `--take upstream` discards the local edit. Ask the user which. To keep an edit as the new clean state without updating, use `skills accept KEY` instead.
- Health: `skills status` lists problems; `skills repair` previews fixes for managed links; `skills agents clean|relink|remove-link|adopt-link ... --dry-run` handle the rest.
- Backup: `skills sync` commits, pulls, and pushes the whole root, but only when the user asks.

### Automatic backup

When `skills sync status` shows `"enabled": true`, every successful command that changes the Library also commits, merges, and pushes all pending non-ignored files in the root, including changes that have nothing to do with your task. Those commands are `init`, `install`, `adopt`, `accept`, `rename`, `set-source`, `remove --yes`, `update` without `--dry-run`, `agents add`, confirmed `agents adopt-link`, and every `tag`, `note`, `repos`, and `preset` subcommand that writes. Reads, previews (`install --list`, `--dry-run`), and changes that only touch agent directories (`deploy`, `undeploy`, `repair --apply`, preset deploy, `agents clean|relink|remove-link`) never sync. A running TUI also syncs files written by hand once they stop changing.

If `git status` shows changes you did not make, ask the user before running a syncing command.

## 4. Verify

```sh
skills show KEY
```

`skills show` exits 0 even when the skill is broken, so read the `status:` line. The work is done when it reads `local` for a skill you wrote, or `repository` for a fresh install, `name:` and `description:` match what you intended, and `deploy:` lists exactly the agents the user asked for. An `invalid: <reason>` status names the problem, for example `no YAML frontmatter` or `missing SKILL.md`; [references/library.md](references/library.md#skill-statuses) lists them all. Run any tests or syntax checks shipped with the skill's scripts.

Then report the Library key, its path relative to the root, the agents it is deployed to, and whether an automatic backup ran. A skill written by hand is not backed up until a later Library-changing command, a running TUI, or a `skills sync` the user asked for picks it up. An agent may need a new session before it sees a newly deployed skill.
