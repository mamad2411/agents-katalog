---
name: pet-rate-rings
description: Install, repair, validate, remove, or explain local Codex pet rate-limit rings. Use when someone asks for live 5-hour and weekly Codex rate-limit rings around the active Codex pet without patching Codex app files, app.asar, pet config, or pet spritesheets.
---

# Pet Rate Rings

This skill installs a local Electron sidecar that draws Codex rate-limit rings
around the active Codex pet. It uses the bundled template under
`assets/pet-rate-rings-template` and the installer scripts under `installer/`.

## Safety Boundary

- Do not patch Codex app files, `app.asar`, pet config, or pet spritesheets.
- Do not edit Codex source code.
- Do not write outside the chosen install directory, the user's Codex skill
  directory, and `~/Library/LaunchAgents`.
- Stop before replacing a non-empty install directory unless the user confirms
  `--force`.

## Workflow

1. Confirm the host is macOS with `uname -s`.
2. Resolve this skill directory from the installed `SKILL.md` path.
3. Choose an install directory. Use `$HOME/dev/pet-rate-rings` when `$HOME/dev`
   exists; otherwise use `$HOME/pet-rate-rings`.
4. Run `bash installer/install-template.sh --target-dir "$TARGET_DIR"`.
5. Run `bash installer/validate-install.sh "$TARGET_DIR"`.
6. From the target directory, run `npm run install-agent`.
7. Ask the user to show the Codex pet with `/pet`.
8. Verify that rings appear around the active pet and track movement.

## Repair

Use the same installer with `--force` only after the user confirms replacing the
target directory:

```bash
bash installer/install-template.sh --target-dir "$TARGET_DIR" --force
bash installer/validate-install.sh "$TARGET_DIR"
```

## Uninstall

From the installed sidecar directory:

```bash
npm run uninstall-agent
```

Then remove the sidecar directory only if the user asks for file cleanup.

## Verification Commands

Run these from the installed sidecar directory before claiming success:

```bash
npm test
node scripts/read-rate-limits.mjs
npm run install-agent
source scripts/lib/launch-agent.sh
launchctl print "gui/$(id -u)/$(launch_agent_label)"
```

`node scripts/read-rate-limits.mjs` may print `status: unavailable` when Codex
has no current App Server or JSONL rate-limit data. The overlay must still
render track rings and unavailable chip text in that state.
