---
name: domino-cli
description: Use the Domino command-line client (domino login, run, create, init, get, restore, sync, upload, download, download-results, upload-dataset, create-snapshot, create-dataset-from-snapshot, help, version) and the Domino R package (library(domino) with domino.login, domino.get, domino.run, domino.download, domino.sync, domino.init, domino.upload) that wraps it. Covers installing the CLI graphically or headless on Linux, signing in with a browser or the device-code flow over SSH, working on a Domino File System project from a laptop, large uploads to Datasets, downloading run results, moving a project between deployments, force-restoring a broken local project, and proxy settings in domino.vmoptions. Use when the user mentions the Domino CLI, a `domino` shell command, syncing project files from a laptop, the Domino R package, or running Domino jobs from R or a terminal. Not the `dom` SSH tool kit and not python-domino.
compatibility: Domino 6.3 and Domino Cloud. CLI builds older than 6.2.3 can no longer sign in; download the installer from the deployment you use. The R package (CRAN domino 0.3.1, 2017) shells out to the installed CLI and is documented as possibly outdated.
---

# Domino CLI and R package

Applies to Domino 6.3 and Domino Cloud.

Product pages: https://docs.domino.ai/cloud/reference/cli (index, install, reference, download
files, force-restore, move a project, proxy) and
https://docs.domino.ai/cloud/reference/r-package/domino-r-package. The 6.3 pages are the same
content under `/6.3/`.

## What it is, and what it is not

| Tool | Use it for | Not for |
|---|---|---|
| **Domino CLI** (`domino`) | a laptop or server working on a **Domino File System project**: pull and push files, start a Job, download results, bulk-upload to a Dataset; on a Git-based project, the DFS-backed **Artifacts** | REST automation (use the API with a token), Git-based project code (use git) |
| **R package** (`library(domino)`) | the same CLI commands from an R console | calling the Domino API from R (write `httr` calls against the API instead) |
| `dom` tool kit | SSH into a running Workspace for local IDE development | project file sync |
| python-domino, REST | automation and integrations | interactive file sync |

The CLI is a Java application (the headless install needs a JRE); it keeps its project link in
`.domino/config.json` and its proxy settings in `domino.vmoptions`.

## Install and sign in

1. **Account > Download CLI** in the Domino UI, pick the OS, run the installer (macOS prompts
   for admin credentials; cancel and add `/Applications/domino` to `PATH` yourself if you lack
   them). Headless Linux:
   `apt install openjdk-8-jre-headless`, `wget https://<domino-url>/download/client/unix -O /tmp/domino-install-unix.sh`, `sh /tmp/domino-install-unix.sh`.
2. Close and reopen the terminal, then `domino login https://<your-domino-url>`. The CLI opens
   a browser to the Domino sign-in page and receives the authorization itself.
3. No browser on this machine (SSH, a Workspace)? `domino login --device https://<your-domino-url>`
   prints a verification URL and a short code; open it on any device, sign in, **Grant Access**.
   The code expires quickly; rerun the command for a new one.

A CLI older than 6.2.3 uses a retired authentication client and cannot log in; reinstall from
**Download CLI**. After `domino login` the CLI keeps its own session; there is no token or
API-key login for the CLI. Full install notes, OS support and proxies:
[CLI-INSTALL.md](./CLI-INSTALL.md).

## Everyday workflow (DFS project)

```bash
domino get owner/project          # first copy of an existing project; creates ./project
cd project
domino run train.py 20            # upload changed files, start a Job with arguments, return at once
domino run --wait train.py        # block until the Job ends
domino run --direct "pip freeze | grep pandas"   # shell command instead of a file
domino run --tier "Large" train.py               # hardware tier by name
domino download                   # pull results and collaborators' changes
domino sync                       # download then upload
domino upload -m "add data"       # push without starting a Job
domino download-results --filter 'results/*' 42  # files from run number or id 42 into results/run-42
```

File and run commands act on the project folder you run them in (the CLI keeps the link in
`.domino/config.json`); `domino get` and `domino create` make that folder. `domino init [name]`
turns the current folder into a new project without uploading; `domino create [name]` makes a
new folder and project; `domino restore` reconnects a folder (for example a `git clone`) to its
project. `--owner <org>` on `create` and `init` assigns the project to an organisation. `--no-sync`
runs server-side code without uploading local changes; `--local` records a run that executes on
your machine. Every command, flag and example: [CLI-REFERENCE.md](./CLI-REFERENCE.md).

## Datasets from the CLI

```bash
domino upload-dataset --fileUploadSetting Overwrite --targetRelativePath raw/2026-10 owner/project/dataset-name /local/folder
domino create-snapshot owner/project/dataset-name
domino create-dataset-from-snapshot owner/project/dataset-name 3 new-dataset-name
```

`upload-dataset` overwrites existing files unless `--fileUploadSetting Ignore|Rename` (values are
case-sensitive). Tune big uploads with `DOMINO_UPLOAD_CHUNK_BYTES` (default 3 MB) and
`DOMINO_UPLOAD_THREADS` (default 8). Quotas and limits: [domino-datasets](../domino-datasets/SKILL.md).

## R package in one screen

```r
install.packages("domino", repos = "http://cran.r-project.org", type = "source")
library(domino)
domino.get("owner/project")             # or setwd() into an existing project folder
domino.run("myScript.R", 1, "someString")   # arguments become the script's command-line args
domino.download()                       # bring results back, then load() them
domino.sync(); domino.init("name"); domino.upload("message")
```

CRAN `domino` 0.3.1 (2017) runs the installed CLI with `system()`, so install and log in with the
CLI first (the browser or device flow above). Its `domino.login(username, password, host)` feeds
a username and password to the CLI's old interactive prompt and may fail against the current
CLI; prefer a terminal `domino login`. Exported functions,
signatures and limits: [R-PACKAGE.md](./R-PACKAGE.md).

## Pitfalls

- The CLI syncs the **Domino File System**. On a Git-based project that is the **Artifacts**
  section; code goes through git and Jobs through the UI or API
  ([domino-jobs](../domino-jobs/SKILL.md)).
- "blob file not found" on `domino run`: run `domino sync` first.
- More than about 1,000 files in one `upload` can time out; upload in batches.
- "too many open files" during `sync`: add an empty `.noLock` file at the project root.
- Keep files out of sync with `.dominoignore` at the project root; `.git/` is always ignored.
- Broken local metadata: `rm -rf .domino` then `domino restore` (force-restore); files on the
  server that are missing locally come down, local changes go up on the next `sync`.
- Moving a project to another deployment copies only the latest files, never history or
  collaborator settings.

## Related skills

- [domino-projects](../domino-projects/SKILL.md): DFS versus Git-based projects
- [domino-datasets](../domino-datasets/SKILL.md): Datasets, snapshots, quotas
- [domino-jobs](../domino-jobs/SKILL.md): what a run becomes, logs, scheduling
- [domino-workspaces](../domino-workspaces/SKILL.md): the `dom` SSH tool kit for Workspaces
- [domino-python-sdk](../domino-python-sdk/SKILL.md), [domino-api-intro](../domino-api-intro/SKILL.md): API automation instead of the CLI
