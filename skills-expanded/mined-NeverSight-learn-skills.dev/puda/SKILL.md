---
name: puda
description: Setup puda project, CLI installation, and project/experiment structure. Use when initializing a Puda project, puda experiment, or when updating skills is needed
---
## Setting up new puda project
1. **Check installation**: Determine how to invoke the CLI — use `puda` if installed globally, or from the project root use `./puda` on Unix/macOS or `.\puda.exe` on Windows if only a local binary exists. If it's missing, direct the user to the [Puda releases page](https://github.com/PUDAP/puda/releases). Use that same invocation (`puda`, `./puda`, or `.\puda.exe`) consistently in all steps below.
2. **Ensure Python and pip**: Ensure `python3` and `pip` are available; install them first if missing. 
3. **Login**: Log in to puda with `puda login`; you will need to enter a username.
4. **New project folder**: run `puda init` (e.g. `puda init .` or `puda init <folder_name>`).
5. **Install Skills**: run `puda skills install` to install agent skills for puda

Only after the CLI is installed and the project is initialized, proceed with protocol generation, machine commands, or experiment workflows.

## Project Folder Structure

```text
.
├── .agents/                          # puda agent skills (from `puda skills install`)
├── logs/                             # log files from runs
├── project.md                        # single source of truth (puda-memory skill)
├── protocols/                        # generated protocol files (puda-protocol skill)
├── puda.config                       # puda config file
└── puda.db                           # puda database file
```

## Updating puda skills

To refresh or update puda skills:

```bash
puda skills update
```
(or `./puda skills update` / `.\puda.exe skills update` if using the local CLI)
