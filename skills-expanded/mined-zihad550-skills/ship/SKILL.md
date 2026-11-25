---
name: ship-skill
description: Ship a skill from the user's own skills repo to every agent — create a new one, or roll out an edit or rename of an existing one.
disable-model-invocation: true
---

# Ship a skill

Take a skill from the skills repo to every agent: authored, pushed, registered in the dotfiles installer, and installed globally. A skill that exists only on disk is not shipped — every step below runs, for a new skill and an edited one alike.

The checkouts live in different places per machine. Below, `<skills>` and `<dotfiles>` stand for:

- On the host: `~/hq/skills` and `~/hq/dotfiles`.
- In a devvm VM (`/etc/profile.d/devvm-tools.sh` exists): `~/skills` and `~/dotfiles`. Pushing from a VM needs `devvm secret use github` run once in its project folder; when a push is refused for missing credentials, ask the user to run it.

Use the name the user gave, or the skill this conversation edited. For a new skill with no name, propose a kebab-case name from its job and confirm it before step 1.

## 1. Scaffold or open

New skill:

```bash
cd <skills>/skills && skills init <name>
```

Existing skill: open `skills/<name>/SKILL.md`. A rename is `git mv skills/<old> skills/<name>`, then `grep -rn '<old>' <skills> --exclude-dir=.git` and update every hit.

Done when `skills/<name>/SKILL.md` exists, and for a rename, the grep finds the old name nowhere.

## 2. Write it

Invoke the `writing-for-agents` skill and write or edit `SKILL.md` under its rules — description as context pointer, steps with checkable completion criteria, reference disclosed behind pointers rather than piled inline. When the change is already written, review it under those rules.

Done when every placeholder line the CLI wrote is gone and the frontmatter `name` matches the directory.

## 3. Scrub sensitive information

Inspect every changed file under `skills/<name>` before staging it. Remove credentials and sensitive information copied from prompts, terminals, configuration, examples, logs, or source material. This includes API keys, access tokens, passwords, private keys, session cookies, connection strings, account identifiers, and private endpoints. Replace values needed for instruction or examples with descriptive placeholders such as `<API_TOKEN>` or environment-variable references.

Review the complete diff and run the repository's secret scanner when one is configured. Treat suspected secrets as sensitive until verified otherwise.

Done when the change contains no real credentials or sensitive values and its examples remain usable with placeholders.

## 4. Commit and push the skill

```bash
cd <skills> && git add skills/<name> && git commit && git push
```

Conventional Commits, matching the log's existing style: `feat: add <thing> skill` for a new skill, `feat(<name>): <change>` or `docs(<name>): <change>` for an edit. Push before step 6 — `skills add` installs from GitHub, so an unpushed skill installs as nothing.

## 5. Register it in the installer

`<dotfiles>/setup/common/setup-skills` is a separate repo. When `<name>` is missing from the `--skill` list on the `skills add Zihad550/skills` invocation, add it, keeping that list alphabetical; for a rename, replace the old name. Commit and push the dotfiles repo. The repo often carries the user's uncommitted work, even in that file — stage only your own hunk (`git apply --cached` with a patch of just that hunk) and leave the rest as you found it.

Done when the skill name appears in that list and your change is pushed, or the name was already there and nothing needed committing.

## 6. Install globally

Read the `AGENTS` array from `<dotfiles>/setup/common/setup-skills` — it is the source of truth for install targets — and run from `~`, naming every skill this change added or edited:

```bash
cd ~ && skills add Zihad550/skills --skill <name> -g --agent <agents from AGENTS> -y
```

Install with `--agent` only. `skills update -g` reinstalls without `--agent`, linking every updated skill into every detected agent, including `~/.claude/skills`, where it duplicates skills a Claude plugin already ships. To refresh all skills, re-run `<dotfiles>/setup/common/setup-skills` instead.

For a rename, remove the old install with `skills remove <old> -g -y`.

In a devvm VM, run `bash <dotfiles>/setup/devvm/setup-skills` instead of the command above: it installs from the VM's checkout with `--copy`, which the VM's redirected agent folders need. Tell the user the host gets the skill only when this step runs there.

Done when `~/.agents/skills/<name>/SKILL.md` and `~/.claude/skills/<name>/SKILL.md` both exist with the pushed content, and for a rename, neither path exists for the old name.
