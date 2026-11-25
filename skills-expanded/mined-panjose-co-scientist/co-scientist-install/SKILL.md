# co-scientist-install

Goal:

- Explain or execute the project-local Co-Scientist skill installation flow for Claude Code users.

Expected input:

- no arguments for the standard install path
- or a user request to reconcile or uninstall the project-local install

Execution steps:

1. If the user wants a fresh install, tell them to run one of:

   `uv` quick install:

   ```powershell
   uv sync --extra dev --extra mcp
   pnpm --dir apps/dashboard install
   pnpm --dir apps/dashboard build
   powershell -File tools/install/install_co_scientist.ps1
   ```

   `conda` / `pip` path:

   ```powershell
   conda create -n co-scientist python=3.12 -y
   conda activate co-scientist
   python -m pip install -e ".[dev,mcp]"
   pnpm --dir apps/dashboard install
   pnpm --dir apps/dashboard build
   powershell -File tools/install/install_co_scientist.ps1
   ```

   ```bash
   bash tools/install/install_co_scientist.sh
   ```

2. If the user wants to refresh an existing project-local install, use:

   ```powershell
   powershell -File tools/install/install_co_scientist.ps1 -Reconcile
   ```

3. If the user wants to remove the managed project-local install, use:

   ```powershell
   powershell -File tools/install/install_co_scientist.ps1 -Uninstall
   ```

4. After install or reconcile, recommend:

   ```bash
   uv run python -m tools.host.project_cli doctor
   ```

5. Return a short summary of:
   - what command to run
   - what files should appear (`.claude/skills/`, `.co-scientist/installed-skills.json`)
   - how to validate the environment with `doctor`

Rules:

- Treat `skills/` as canonical and `.claude/skills/` as the project-local Claude Code mirror.
- Do not ask the user to edit `CLAUDE.md`; the installer manages its own project-local surface.
- Prefer `doctor` after installation instead of assuming the environment is ready.
