# AGENTS.md

Conventions agents must follow when working in this repository.

## Deployment workflow (always use git, never scp)

The production host `brandon@192.168.1.195` is a Linux desktop with an
NVIDIA GTX 1080 GPU. It runs this code from `/opt/speciesnet/animaltracker`,
which is a clone of the same `origin` (`github.com/bpasker/animaltracker`,
branch `main`). Both ends use passwordless SSH key auth and `NOPASSWD` sudo
for `brandon`.

After ANY source change in `src/`, `config/`, or `systemd/`:

1. **Locally**: stage and commit the change with a clear message, then push.
   ```bash
   git add -A && git commit -m "<concise message>" && git push origin main
   ```
2. **Remote**: pull on the production host and restart the service.
   ```bash
   ssh brandon@192.168.1.195 'cd /opt/speciesnet/animaltracker && \
     sudo git pull --ff-only origin main && \
     sudo systemctl restart animaltracker && \
     sudo systemctl is-active animaltracker'
   ```

   The `animaltracker.service` unit runs the **whole pipeline** (every
   camera in `config/cameras.yml` + the web UI on :8080) in a single
   process. Only one instance can run at a time — a second would fail
   to bind :8080 and crash-loop.

Do **not** `scp` files to the remote or hand-edit
`/opt/speciesnet/animaltracker/...` directly. Treat the remote checkout as
read-only except via `git pull`. If a hotfix was applied via scp in the past,
revert any `*.bak` files and reconcile to git before continuing.

## Notes

- A single `animaltracker.service` unit runs both cameras and the web UI.
  Any code change in `src/`, `config/`, or `systemd/` requires restarting it.
- For PTZ tracking incidents (overshoot, missed centering, stale detections,
  cam1/cam2 handoff problems, or requests to review a clip), use the
  `ptz-incident-review` skill and the `scripts/ptz_review.py` tool to
  correlate the video, sidecar `.log.json`, PTZ decisions, and journal logs
  before changing controller logic.
- For config-only edits to `/opt/speciesnet/animaltracker/config/cameras.yml`
  done directly on the remote (e.g. via the Web UI), commit the result back to
  git on the remote and push, so local stays in sync.
- Never commit secrets. `config/secrets.env` is gitignored; if it isn't,
  add it before committing.
