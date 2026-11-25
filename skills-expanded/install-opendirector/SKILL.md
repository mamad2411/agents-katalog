---
name: install-opendirector
description: Install OpenDirector from source on the current machine. Detect the platform, check and install missing prerequisites, prepare project dependencies, build the application, verify startup, and provide platform-specific launch commands. Use for first installation or repairing an incomplete installation; not for model deployment, application development, or routine startup alone.
---

# Install OpenDirector

Deliver a working local source installation and exact commands the user can run
again. Reply in the user's language, supporting Chinese and English. A request
to create or discuss this skill does not authorize installing the application.

## Locate the source and inspect the host

1. Honor the requested directory and revision. Otherwise reuse an OpenDirector
   checkout in the working directory or the repository containing this skill.
   Identify it by `package.json`, the root `pyproject.toml`, and `scripts/opendirector.py`, rather than its directory name.
2. If there is no checkout, use the source URL in the bundled platform guidance:
   `https://github.com/ThinkFlowLab/OpenDirector.git`. Clone into an available
   `OpenDirector` directory under the working directory. Never overwrite a
   nonempty directory. Record the resolved revision. ZIP sources are acceptable;
   their lack of Git metadata must not prevent installation.
   If Git is missing, inspect the host as below and bootstrap Git first, or use
   a source archive. Do not require Python just to discover the platform.
3. Inspect OS/version, architecture, shell, package managers, executable paths,
   and privileges using native commands before assuming Python or Node exists.
   Distinguish WSL from native Windows, and process architecture from host
   architecture when emulation is involved. Read only the relevant reference:
   [macOS](references/macos.md), [Linux/WSL](references/linux.md), or
   [Windows](references/windows.md).
   For another OS, report the unsupported installation path instead of applying
   a recipe for a different platform.
4. In the target source, read `README.md` or `README.zh-CN.md`, `.nvmrc`,
   `package.json` (including `engines`), the root `pyproject.toml`,
   `requirements.txt`, and the launcher. These files govern the selected revision;
   bundled commands are starting points, not permission to change its manifests.

## Check and install prerequisites

Complete system prerequisite installation and user PATH setup before creating
the project venv or installing application dependencies. Reuse compatible
installed tools; install missing Git, Node.js/npm, Python, FFmpeg and ffprobe
through the platform package manager or supported user-level installer. Python
application packages still belong in the project venv.

- Check actual paths, versions, and successful execution of Node.js, npm,
  Python, `ffmpeg`, and `ffprobe`; require FFmpeg's **exact** `libx264` encoder.
  Git is needed for cloning and for the current launcher in Git checkouts.
  Check Python's ability to create a venv with pip. An existing `.venv` needs
  its own interpreter check. Current source requirements are Node >=24.22.1
  and Python >=3.11; reread the selected source instead of relying on these values.
- Once Python 3.11+ is available, run this skill's standard-library-only helper
  with that interpreter, using absolute paths if necessary:

  ```sh
  python3 /path/to/install-opendirector/scripts/check_environment.py --root /path/to/OpenDirector
  ```

  On Windows, use the selected `python.exe` with PowerShell's `&` operator.
  The helper prints JSON facts and stable status codes for the agent to explain
  in the user's language; exit 1 means action is needed, exit 2 means the source
  or its constraints could not be inspected. It does not install anything or
  start a service. It requires Python 3.11+ and supports simple `>=` runtime
  constraints; inspect newer constraint syntax manually if reported unsupported.
  Facts may include stale `.venv` or missing build files before installation.
  The helper's regression checks can be run with Python 3.11+ using
  `python3 -B /path/to/install-opendirector/scripts/test_check_environment.py`.
- Reuse suitable tools; install only missing or unsuitable prerequisites using
  the relevant platform reference. Recheck after changes. Select an existing
  suitable executable before installing another version. Use a project venv for
  Python packages, never `sudo pip` or an upgrade of the system Python.
- Make prerequisite tools discoverable on the user's PATH, not only through
  absolute paths or a temporary agent export. Inspect the user's shell and
  existing startup configuration, then add only the missing package-manager
  initialization or tool directories to the appropriate user configuration.
  Preserve existing entries and avoid duplicate additions. On Windows, use the
  installer-managed PATH or append missing directories to the user PATH without
  overwriting it. Carry these changes into the current process too.
- Verify discovery and versions in a fresh instance of the user's normal shell
  without inheriting the agent's temporary PATH additions. Check `git`, `node`,
  `npm` (`npm.cmd` on Windows), the selected Python command, `ffmpeg`, and
  `ffprobe`; versioned Python commands such as `python3.12` are acceptable.
  If this fails, finish PATH setup before proceeding. Do not globally add the
  project's `.venv/bin` or `Scripts` directory to PATH.
- Respect the execution environment's network and privilege approvals. Continue
  authorized ordinary installation without extra conversational confirmations.
  If an installer requires user interaction, report the precise pending action
  and continue independent checks. Do not bypass permissions, replace system
  executables, change global registries, or force dependency upgrades.

## Prepare dependencies and build

Run from the source root, checking each command before proceeding. Use the
selected compatible Python to create `.venv` only if a working suitable venv
does not already exist. Preserve an incompatible or broken `.venv` by renaming
it to an unused backup name before recreating it; do not delete its contents.

POSIX (replace `python3` with the selected interpreter):

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -v -e .
.venv/bin/python -m pip check
```

Windows PowerShell (select the Python version before using `py -3`):

```powershell
py -3 -m venv .venv
& .\.venv\Scripts\python.exe -m pip install -v -e .
& .\.venv\Scripts\python.exe -m pip check
```

The pip build backend runs npm ci, the frontend build, and the bundled OpenCode version check. Do not run these stages separately during installation. Wheel installs contain these resources and do not require Node.js; source installs do.

If pip or npm downloads are slow or time out, retry the same installation with
a user-specified or trusted alternative registry scoped to that process.
Preserve global registry settings, lockfiles, and integrity checks.

Skip the venv creation command when reusing one. Do not skip dependency
installation solely because `node_modules` or `.venv` exists. `npm ci` requires
the selected revision's matching lockfile; a mismatch is a concrete blocker,
not a reason to regenerate it silently. Keep the source, user projects, model
credentials, and configuration intact. Stop the failing stage on dependency
resolution or build errors and report the actionable cause. Retry a transient
network failure once with the same inputs; further attempts need new evidence
or a changed network condition.

## Verify and hand off

Follow [verification and delivery](references/verification.md), including the
helper's `--installed` mode and a temporary launch through the real `serve`
entrypoint. Report build success separately from startup and health results.
Stop only the test processes you created, confirm port release, and leave the
application stopped unless the user requested a running instance.

Give the absolute source directory and copyable commands for the user's shell.
The existing startup script is sufficient; do not create another launcher unless
requested. POSIX uses `.venv/bin/python scripts/opendirector.py serve`; Windows
uses `& .\.venv\Scripts\python.exe scripts/opendirector.py serve`. Explain the
default URL `http://127.0.0.1:8000`, keeping the terminal open, `Ctrl+C` to stop,
and `--port 8001` for a conflict. Include prerequisite PATH setup when needed.

Installation does not deploy models or require GPU tooling. Say that AI features
need model configuration in Settings / 设置 → Model access / 模型接入. Do not call
paid model services, configure credentials, create user projects for a smoke
test, enable a persistent service, or expose the server publicly as part of this
workflow. Claim verification only for platforms and operations actually tested.
