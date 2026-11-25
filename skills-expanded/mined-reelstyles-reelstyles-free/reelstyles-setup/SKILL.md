---
name: reelstyles-setup
description: "Set up ReelStyles on this computer for the user's AI agent. Checks and installs Node.js 22+, ffmpeg, Chrome for HyperFrames (and Git Bash on Windows), connects ReelStyles to the user's agents (Claude Code, Codex, OpenCode, Cursor, Gemini CLI, GitHub Copilot, Cline, Windsurf, Roo Code), then renders a 5 s test film. Use when the user says \"set up ReelStyles\", \"install ReelStyles\", or before the first ReelStyles video if setup has not passed."
---

# ReelStyles setup

The scripts live in `setup/` at the root of the ReelStyles folder (two folders above this file, the folder that holds `AGENTS.md`). Call it `<repo>`. `setup/setup.sh` (macOS, Linux, WSL, Git Bash) and `setup/setup.ps1` (Windows PowerShell) take the same commands. Below, `SETUP` means:
- macOS / Linux / WSL / Git Bash: `bash <repo>/setup/setup.sh`
- Windows PowerShell: `powershell -ExecutionPolicy Bypass -File <repo>\setup\setup.ps1`

1. **Detect the system.** Find the OS (Windows, macOS, Linux, WSL) and the shell your terminal tool uses, and pick the matching script. On Windows use `setup.ps1` unless your shell is already bash (Git Bash or WSL).
2. **Check.** Run `SETUP check`. It lists Node.js 22+, ffmpeg + ffprobe, git (on Windows: Git Bash, which every kit's `tools/render.sh` needs), free disk and Chrome for HyperFrames, and exits non-zero if anything required is missing. If it prints READY, go to step 4.
3. **Install what is missing, with the user's OK.**
   - Run `SETUP install --dry-run`. It prints, per missing tool, the exact command it would run (winget, Homebrew, apt or dnf; Node through fnm, nvm or the official nvm installer when the system Node is old).
   - Show the user every command and ask which ones to run. **Never install anything the user has not agreed to**, and say clearly when a command uses `sudo`.
   - Run `SETUP install --yes <tool> [<tool>...]` with only the tools the user agreed to (or let the user run `SETUP install` themselves: it asks per tool). If a command needs a password, ask the user to run it in their own terminal.
   - Node or git installed just now may need a new terminal before they are on the PATH. Then run `SETUP check` again until it prints READY.
4. **Connect the agent.**
   - If your working folder is `<repo>` itself, skip this step: the folder already has `AGENTS.md`, `GEMINI.md`, `.claude/CLAUDE.md`, `.agents/skills/`, `.github/skills/` and `.cline/skills/`, which every supported agent reads.
   - If the user works in another project folder, ask before you change it. Run `SETUP wire list` to see which agents are detected, tell the user which files `wire` will add there (short pointer files such as `.agents/skills/reelstyles/SKILL.md`, `.cursor/rules/reelstyles.mdc` or a marked block in `AGENTS.md` / `GEMINI.md`), and after a yes run `SETUP wire auto --dir <project>` (or `SETUP wire <agent>... --dir <project>`; agents: `claude codex opencode cursor roo cline gemini copilot windsurf`). It never copies the kits. Add `--global` if the user wants ReelStyles in every project. Claude Code users who installed the plugin need no wiring.
5. **Smoke test.** Run `SETUP test`. It renders a 5 s test film and prints the mp4 path and the render time. If it fails, run `SETUP check`, fix what it lists, and try again.
6. **Report plainly.** Tell the user, in a few short lines: what was already there, what you installed, which files you added (or "none"), the test film's path and how long it took. End with: "ReelStyles is ready: ask me for a video in any style from STYLES.md" (`skills/reelstyles/STYLES.md`). If the user also asked for a film, go on with `skills/reelstyles/SKILL.md`.

Notes
- Nothing here sends data anywhere: HyperFrames telemetry is switched off by the scripts. The first run downloads the HyperFrames npm package and, if no Chrome is installed, its headless Chrome.
- The scripts are safe to run again; they skip what is already done.
- On Windows, when your terminal is PowerShell or cmd, run the kits' render script with the full Git Bash path that `setup.ps1 check` prints (a plain `bash` there can be WSL, a different system), for example `& 'C:\Program Files\Git\bin\bash.exe' tools/render.sh`.
