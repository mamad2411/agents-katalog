---
name: hermes-profile-distribution
description: "Use when a repo ships its own Hermes agent. Package it."
version: 1.1.0
author: coder role of hermes-fleet-apps
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, profile, distribution, packaging, agent-as-product]
    related_skills: [secure-build]
---

# Hermes profile distribution

When a repo ships an agent for its own tool, do not write a template plus a
copy script. Hermes already packages a whole agent as a folder and installs
it in one command. Docs: hermes-agent.nousresearch.com/docs/user-guide/profile-distributions
(fetch the page with curl if your web tool cannot extract it). The coordinator's
`hermes-agent-factory` skill holds the lean-profile method (ROLE, SOUL, TOOLS,
KEYS, VERIFY); read it, never edit it.

## Layout (fixed by the runtime)

```
agent/
  distribution.yaml     name, version, description, hermes_requires, env_requires
  SOUL.md               IDENTITY · VOICE · LIMITS · REPORTING, under 2 KB, plain
  config.yaml           platform_toolsets only — never model or provider
  .gitignore            the docs' list; ships with the folder
  skills/<name>/SKILL.md
```

Install: `hermes profile install ./agent --alias` then `<name> setup`.
The installer never copies `.env` and writes `.env.EXAMPLE` from
`env_requires` — secrets stay blank by construction, not by discipline.

## Rules learned by running it

- **Add `skills` to `platform_toolsets.cli`.** With `[terminal, file]` alone
  `prompt-size` shows the skills index at 0 B and the shipped skill never
  loads. Measured; the docs do not say it.
- **Ship no model line.** Hard rule for public packs, and the installer
  preserves the user's config.yaml on update, so a shipped model would be
  the one thing they could never shed. Setting the model on the owner's
  install is `hermes -p <name> config set model.default X` — settings, not
  secrets; the key itself is never touched.
- **Never run `profile delete` with the shell cwd inside the profile.**
  On Windows the delete fails half-way (WinError 32) and leaves a tombstone
  in `profiles/.deleted/<name>` that blocks every reinstall, `--force`
  included, with a FileNotFoundError deep in `mkdir_under_hermes_home`.
  Fix: remove the tombstone file and the directory by hand.
- **Guard the pack in CI by shape:** paths, keys, model names, private
  references, and the presence of the four fixed files. Sabotage each guard
  with a key-SHAPED string — a redacted placeholder matches nothing and the
  case passes by changing nothing.
- **Verify:** `hermes -p <name> prompt-size`, `hermes -p <name> skills list`,
  one `chat -q` that asks the agent what it is and what it refuses. Record
  the numbers. Say which OS it was tested on.
