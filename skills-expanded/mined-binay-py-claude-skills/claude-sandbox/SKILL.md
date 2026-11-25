---
name: claude-sandbox
description: Run Claude Code inside a Docker container that can only see one project folder — non-root user, all Linux capabilities dropped, no-new-privileges, memory and process limits, the host's ~/.claude, SSH keys and other files never mounted. Makes --dangerously-skip-permissions reasonably safe for long autonomous runs. Includes an isolation self-check. Use when the user wants to sandbox Claude Code, run it unattended or in bypass/yolo mode, try an untrusted repo, or protect their machine from rm -rf style accidents.
---

# claude-sandbox

`scripts/sandbox.mjs` (Node 22+) plus `scripts/Dockerfile`. It needs Docker (Docker Desktop on Windows/macOS). The image builds automatically on first run (~2 min).

```
node sandbox.mjs                          # current folder, interactive Claude Code
node sandbox.mjs ~/code/app --yolo        # skip permission prompts INSIDE the container
node sandbox.mjs . --readonly             # project mounted read-only (reviews, audits)
node sandbox.mjs . -- -p "fix the failing test"   # args after -- go to claude
node sandbox.mjs --shell .                # bash in the sandbox
node sandbox.mjs --check .                # prove the isolation (run this first)
node sandbox.mjs --rebuild                # update Claude Code inside the image
```

## What the container can and can't do
| | |
|---|---|
| Sees | only the project folder, at `/workspace` (read-write, or read-only with `--readonly`) |
| Never sees | your home folder, `~/.claude`, `~/.ssh`, other projects, the rest of the disk |
| Runs as | unprivileged user `claude`; `--cap-drop ALL`, `no-new-privileges`, no sudo, 4 GB memory, 1024 processes |
| Keeps | its own login and settings in the Docker volume `claude-sandbox-home` (log in once inside; `ANTHROPIC_API_KEY` is passed through if set) |
| Network | normal outbound access (needed for the API, npm, git). `--no-network` cuts it entirely |

It refuses to mount your home folder, a folder above it (`C:\Users`, `/home`) or a drive root.

## Tell the user
- `--yolo` is only reasonable *because* of the container: Claude can wreck `/workspace` but nothing else. Commit or back up first, or use git so mistakes are one `git checkout` away.
- It is not a perfect boundary. Network access means code in the project can still send data out, and anything inside `/workspace` (including a `.env`) is readable. Don't sandbox a folder that holds secrets you wouldn't hand to the agent.
- Git push from inside needs credentials. Prefer pushing from the host after reviewing the diff.
- First login: run `node sandbox.mjs .` and follow Claude Code's login prompt. It persists in the volume.
