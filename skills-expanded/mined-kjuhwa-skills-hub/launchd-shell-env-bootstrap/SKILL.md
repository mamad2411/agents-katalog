---
name: launchd-shell-env-bootstrap
description: Electron apps launched from Finder/Dock on macOS inherit a minimal launchd PATH — spawn the user's login+interactive shell, parse its env, merge it into process.env so brew/nvm/pyenv work for the agent.
category: electron
version: 1.0.0
version_origin: extracted
tags: [electron, macos, shell-env, launchd, path]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/lukilabs/craft-agents-oss.git
source_ref: main
source_commit: 61f7d48a5b4fd0a8094f002c9e3aea5f3824dcfb
source_project: craft-agents-oss
source_path: apps/electron/src/main/shell-env.ts
imported_at: 2026-04-18T00:00:00Z
---

# Load user's shell env into an Electron macOS app

## When to use
- Electron app that spawns dev-tool subprocesses (git, gh, brew, pyenv, nvm-managed node, etc.).
- macOS users launch your app from Finder/Dock (not Terminal) and the agent can't find their tools.
- Don't want to hand-roll "add /usr/local/bin to PATH" - you want whatever `zsh -l -i` would give them.

## How it works
1. Only run on macOS (`process.platform === 'darwin'`); skip on Linux (desktop environments usually give a full env), skip on Windows (different model entirely).
2. Skip if `VITE_DEV_SERVER_URL` is set (dev mode runs from Terminal, env is already present).
3. `execSync('${SHELL} -l -i -c "echo __ENV_START__ && env"')`:
   - `-l` = login shell (sources `.zprofile`, `.bash_profile`).
   - `-i` = interactive shell (sources `.zshrc`, `.bashrc`).
   - The `__ENV_START__` marker separates shell startup noise from the env dump.
4. Pass minimal env to the child: `HOME`, `USER`, `SHELL`, `TERM=xterm-256color`, `TMPDIR`. Set `APPLE_SUPPRESS_DEVELOPER_TOOL_POPUP=1` + `GIT_TERMINAL_PROMPT=0` to avoid interactive popups during the env dump.
5. Split after `__ENV_START__`, parse `KEY=VALUE` lines, merge into `process.env`.
6. **Filter out unsafe imports** like `VITE_*` - those would make the packaged app try to load the renderer from a dev server.
7. Use `timeout: 5000` - if user has a broken shell, don't hang app startup forever.

## Example
```ts
import { execSync } from 'child_process';

export function loadShellEnv(): void {
  if (process.platform !== 'darwin') return;
  if (process.env.VITE_DEV_SERVER_URL) return;
  const shell = process.env.SHELL || '/bin/zsh';
  try {
    const out = execSync(`${shell} -l -i -c 'echo __ENV_START__ && env'`, {
      encoding: 'utf8', timeout: 5000, stdio: ['pipe', 'pipe', 'pipe'],
      env: {
        HOME: process.env.HOME, USER: process.env.USER, SHELL: shell,
        TERM: 'xterm-256color', TMPDIR: process.env.TMPDIR,
        APPLE_SUPPRESS_DEVELOPER_TOOL_POPUP: '1', GIT_TERMINAL_PROMPT: '0',
      },
    });
    const env = out.split('__ENV_START__')[1] || '';
    for (const line of env.trim().split('\n')) {
      const eq = line.indexOf('='); if (eq < 1) continue;
      const key = line.slice(0, eq); if (key.startsWith('VITE_')) continue;
      process.env[key] = line.slice(eq + 1);
    }
  } catch { /* log, continue */ }
}
```

## Gotchas
- Must run BEFORE any `import` that reads env (require ordering matters). In the main file, make this the literal first import side-effect.
- Interactive shells can emit color codes / prompts; the marker pattern prevents false positives but consider also unsetting `PS1` / `PROMPT`.
- `zsh -l -i` is slow (50-200ms) on some setups. That's the cost of being right. Cache the result across app launches keyed on `zshrc` mtime if startup budget matters.
- Be wary of loading user-defined vars that can break your app (`NODE_OPTIONS=--inspect-brk`) - filter aggressively if you've seen breakage.
- On packaged builds, blocking startup on this is fine; in dev, terminal already has env, so skip.
