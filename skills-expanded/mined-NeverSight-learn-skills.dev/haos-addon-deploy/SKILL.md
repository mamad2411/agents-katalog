---
name: haos-addon-deploy
description: "Deploy a self-written app as a Home Assistant OS (HAOS) local add-on (now labelled 'app' in the HA UI/CLI) on a Raspberry Pi for 24/7 operation. Covers the full battle-tested procedure and every known pitfall: git archive delivery, ha CLI quirks (bash -lc, store reload, update vs rebuild), add-on options as config, /data persistence, and base-image (musl vs glibc) selection. Use when deploying, installing, updating or debugging a HAOS local add-on / HA app, or when the user mentions 部署到 RPi / HAOS / HA add-on / HA app."
---

# HAOS Local Add-on Deployment (RPi, 24/7)

Deploy a self-written long-running app (poller, monitor, etc.) as a Home Assistant OS
**local add-on**, running 24/7 on a Raspberry Pi instead of a workstation that sleeps.
Every step below has been verified on real hardware; all pitfalls are marked ⚠️.
In the examples, `ha` = SSH alias, `<slug>` = add-on slug (becomes `local_<slug>` once installed).

## Scope

- Applies to **Home Assistant OS** (or Supervised) installs only — Container/Core
  installs have no Supervisor, no `/addons`, no `ha` CLI; this skill does not apply.
- Battle-tested on a Raspberry Pi 4 (**aarch64**), HAOS 17.x (Supervisor + Docker
  appliance), with the **Advanced SSH & Web Terminal** add-on (Protection mode off —
  see §0, §8).
- ⚠️ Recent HAOS labels add-ons as **"Apps"** in the UI and CLI (`ha apps`), but every
  technical surface still says "addon": the `/addons` path, the `addon_local_<slug>`
  container prefix, and the Supervisor `/addons/...` API. Don't "fix" those names.

## 0. Global Rules (read first)

- ⚠️ **Non-interactive SSH must always be `ssh ha 'bash -lc "…"'`**: a non-login shell
  doesn't load `SUPERVISOR_TOKEN`, so every `ha` CLI / Supervisor API call returns
  `unauthorized`.
- ⚠️ **Disable Protection mode on the SSH add-on** (toggle on its info page), otherwise
  you can't reach the Supervisor API.
- ⚠️ CLI names: use **`ha apps`** (`ha addons` is deprecated); to re-detect local add-ons
  use **`ha store reload`** (`ha apps reload` doesn't exist).
- ⚠️ **Never run the same app on two machines at once** (workstation daemon + RPi add-on):
  it doubles the load on external APIs/sites, and anything with rotating tokens will have
  the two instances kicking each other out. Once migrated, stop the workstation copy and
  disable its autostart.
- A single-SD-card RPi has no redundancy: **take a full HA backup before touching anything**,
  and download it off the card. The web download is slow (HA streaming bottleneck);
  `scp ha:/backup/<file>.tar ~/backups/` is noticeably faster.

## 1. Repo Layout

Keep all HA-specific files in a `haos/` folder in the repo; flatten on delivery:

```
haos/
├── config.yaml      # add-on manifest (name/slug/version/arch/options/schema)
├── Dockerfile
├── run.sh           # entrypoint: create /data subdirs, then exec the main app
└── .dockerignore    # exclude .env, logs/, __pycache__, .git/
```

`config.yaml` essentials:

```yaml
name: My App
slug: my_app            # installed as local_my_app
version: "1.0.0"        # ⚠️ bump this to make HA detect a code update
arch: [aarch64, amd64]
startup: application
boot: auto
map:
  - data:rw             # /data = persistent volume, survives rebuild/update
init: false
options:                # user-editable settings (HA web UI "Configuration" tab)
  some_secret: ""
schema:
  some_secret: password # the password type masks the value in the UI
```

⚠️ **Base image choice (musl vs glibc)**: pure Python/requests → `python:3.12-alpine`
is fine (small); but anything depending on the **onnxruntime / opencv / numpy ecosystem**
(e.g. ddddocr) **must use `python:3.12-slim`** (Debian glibc) — those packages ship no
musllinux wheels, so on Alpine pip falls back to source builds (hangs or fails).
Non-headless opencv additionally needs `apt-get install libgl1 libglib2.0-0`.
Not using the HA official base image → **no bashio**; the app reads its own config
from `/data/options.json` instead.

Idiomatic config loading: if `/data/options.json` exists, upper-case each key into an
environment variable (parse list-typed fields, e.g. a watch list, directly); if it
doesn't (local development), fall back to `.env`.

## 2. Deliver the Code (run on the workstation; git archive, flattened, into /addons)

The device never clones (avoids credentials for private repos); the workstation pushes
a **committed** version:

```bash
# /addons is owned by root; create the folder once to gain write access
ssh ha 'sudo mkdir -p /addons/<slug> && sudo chown $(whoami) /addons/<slug>'
git archive --format=tar HEAD | ssh ha 'tar -x -C /addons/<slug>'
git archive --format=tar HEAD haos | ssh ha 'tar -x --strip-components=1 -C /addons/<slug>'
ssh ha 'rm -rf /addons/<slug>/haos'   # remove the duplicate haos/ subfolder from line 1
```

⚠️ The deploy directory must be **flat and self-contained**: config.yaml/Dockerfile/run.sh
all at the top level of `/addons/<slug>/`.

## 3. Install

```bash
ssh ha 'bash -lc "ha store reload && ha apps install local_<slug>"'
# First build takes minutes (longer with heavy deps like onnxruntime/opencv);
# the build runs in the Supervisor background, so a dropped SSH session doesn't matter
ssh ha 'bash -lc "ha apps info local_<slug> | grep -E \"state:|version:\""'   # a version line = installed
```

## 4. Configuration (add-on options)

⚠️ **`ha apps` has no `options` subcommand** — pick one of two routes:

- **HA web UI** (most reliable): add-on → Configuration tab → fill in and save.
  Secrets (tokens, push topics) always go here — never `.env`, never the repo.
- **Supervisor REST API** (scriptable):
  ```bash
  echo '{"options":{...complete object...}}' \
    | ssh ha 'bash -lc "curl -sS -X POST -H \"Authorization: Bearer \$SUPERVISOR_TOKEN\" \
              -H \"Content-Type: application/json\" -d @- http://supervisor/addons/local_<slug>/options"'
  ```

The schema supports a **list of dicts** (lets the user add/remove entries in the UI,
e.g. monitoring targets):

```yaml
options:
  targets:
    - name: example
      date: "2026-01-01"
schema:
  targets:
    - name: str
      date: str
```

⚠️ The schema only declares types — **format validation is the app's job at startup**;
report which entry is wrong and why, then fail the start (so the user sees it in the
log immediately).

## 5. Start and Verify

```bash
ssh ha 'bash -lc "ha apps start local_<slug>"'
ssh ha 'bash -lc "ha apps logs local_<slug>"'
```

Testing inside the container (e.g. manually trigger one push notification):

```bash
ssh ha 'sudo docker exec addon_local_<slug> python3 -c "…"'
# ⚠️ the SSH add-on user has no docker socket permission — sudo required
```

## 6. Update (⚠️ pick one of three — the wrong one gets rejected)

| What changed | Command |
|---|---|
| Options only (no code change) | `ha apps restart local_<slug>` |
| Code changed, config.yaml version **not bumped** | redo §2 delivery → `ha apps rebuild local_<slug>` |
| Code changed, **version bumped** | redo §2 delivery → `ha store reload` → **`ha apps update local_<slug>`** (rebuild is rejected here: "Local and store versions differ, use Update instead of Rebuild") |

⚠️ **For code updates, always bump `version` and take the update route.** Rebuild
leaves the device reporting the old version while running new code — `ha apps info`
can no longer tell which code the box is actually running, which hurts later
debugging. Reserve rebuild for rapid iterate-and-test cycles where the version
trail doesn't matter yet.

## 7. Persistence and Logs

- **`/data/` is the persistent volume** (host side: `/data/apps/data/local_<slug>/`):
  DB, logs and tokens all live here and survive rebuild/update.
- Log to both stdout (for `ha apps logs`) and `/data/logs/` (rotating files).
- ⚠️ **Never print secrets in the startup log** (`ha apps logs` is visible to anyone
  who can open HA) — print on/off status only.

## 8. SSH Prerequisites (only when touching a new HA host for the first time)

Set an alias in the workstation's `~/.ssh/config` (HostName, User, IdentityFile);
add the public key to the **Advanced SSH & Web Terminal** add-on config (YAML mode):

```yaml
ssh:
  username: <account>
  authorized_keys:
    - >-
      ssh-ed25519 AAAA... public key
```

⚠️ If the saved config keeps reverting, the usual causes are **private key file
permissions too loose** (`chmod 600`) or the YAML nested at the wrong level.
Your SSH lands in the **SSH add-on container** (not the HAOS host, not the HA core
container); `sudo` works there.
