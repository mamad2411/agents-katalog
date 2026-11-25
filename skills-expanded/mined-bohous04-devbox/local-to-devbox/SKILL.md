---
name: local-to-devbox
description: Moves an in-progress LOCAL Claude Code session (on the mac) into a devbox container on the VPS — same repo + branch + uncommitted changes, plus a PoC transfer of the conversation history so it can be continued remotely; it then starts the session in the devbox by itself (auto-resume). Use when the user says "move this to the devbox", "migrate the session to the devbox", "continue on the VPS", "local to devbox".
---

# local-to-devbox

Takes the current local Claude Code session (a git repo on the mac) and replicates it as a
**devbox session** (a container on the VPS), so it can be continued remotely (from a phone /
another machine). It transfers: **repo + branch + uncommitted changes**; and as a **PoC** also
the conversation transcript (see the limitations below).

Prerequisites: you are running in a git repo on the mac, the `dev` CLI works (`dev doctor` green),
the devbox is in the tailnet. Take the values from `~/.config/devbox-cli/config.json`
(`devdUrl`, `sshHost`).

## Procedure

Perform the steps in order. After each step verify the result before moving on. Ask
the user only when something fails or is ambiguous (several devbox targets for the same repo).

### 1) Collect the local state

```bash
DEVD=$(jq -r .devdUrl ~/.config/devbox-cli/config.json)
SSH=$(jq -r .sshHost ~/.config/devbox-cli/config.json)
ROOT=$(git rev-parse --show-toplevel) || { echo "not in a git repo"; exit 1; }
REPO=$(basename "$ROOT")
BRANCH=$(git -C "$ROOT" rev-parse --abbrev-ref HEAD)
# transcript of the current session: project dir = path with '/' -> '-'
PROJDIR="$HOME/.claude/projects/$(printf %s "$ROOT" | sed 's|/|-|g')"
UUID=$(ls -t "$PROJDIR"/*.jsonl 2>/dev/null | head -1 | xargs -r basename | sed 's/\.jsonl$//')
echo "repo=$REPO branch=$BRANCH uuid=${UUID:-none}"
git -C "$ROOT" status --short
```

### 2) Pack uncommitted changes into a patch

Capture staged + unstaged + untracked (binary), without changing anything in the working tree:

```bash
git -C "$ROOT" add -A -N            # intent-to-add: untracked files show up in the diff (content is not staged)
git -C "$ROOT" diff HEAD --binary > /tmp/devbox-migrate.patch
git -C "$ROOT" reset -q             # undo intent-to-add, working tree unchanged
wc -l /tmp/devbox-migrate.patch
```

The patch does not contain **unpushed LOCAL commits** (the branch is not on the remote). So prefer
**pushing the branch** — the commits then reach the container via the remote:

```bash
git -C "$ROOT" push -u origin "$BRANCH" 2>&1 || echo "push failed/no remote — commits will not be transferred, handle manually (git bundle) or continue with the patch only"
```

### 3) Find the devbox target (folder/project/repo) and create the session

`dev _targets` gives `project/repo`; look up the folder in the tree. When there are several repos,
ask the user which one.

```bash
TREE=$(curl -s "$DEVD/api/tree")   # curl from the mac directly to devd (tailnet)
# find the entry with the same repo:
echo "$TREE" | jq -r --arg r "$REPO" '.[] | .repos[]? as $x | select($x.name==$r) | "\(.folder)\t\(.project)\t\($x.name)\t\($x.cloneUrl)"'
```

Pick (folder, project, repo, cloneUrl) and create/open the session (it clones if missing):

```bash
FOLDER=...; PROJECT=...; CLONEURL=...
RESP=$(curl -s -X POST "$DEVD/api/sessions" -H 'content-type: application/json' \
  -d "$(jq -nc --arg f "$FOLDER" --arg p "$PROJECT" --arg r "$REPO" --arg u "$CLONEURL" '{folder:$f,project:$p,repo:$r,cloneUrl:$u}')")
ID=$(printf %s "$RESP" | jq -r .session.id)
# Working directory of THIS session. The new repo layout = its own git worktree outside the
# repo tree (`/srv/dev/_sessions/<id>`), the old layout = the shared `/srv/dev/<folder>/...`
# (then `worktree` is null). Deriving the path from folder/project/repo is no longer enough.
WT=$(printf %s "$RESP" | jq -r '.session.worktree // ""')
echo "session=$ID  workdir=${WT:-shared repo workspace}  (pull: $(printf %s "$RESP" | jq -r '.pull.status // "?"'))"
```

When the repo is not in the devbox tree, add it first from the dashboard (Configuration →
GitHub/Gitea) or continue with `cloneUrl` from the local `git remote get-url origin`.

### 4) Set the branch + apply the patch in the container

The session's working directory on the VPS is either its own worktree (`$WT` from the step above, the new
repo layout), or the shared repo workspace `/srv/dev/<folder>/<project>/<repo>` (old
layout; when `folder==project`, the path collapses to `/srv/dev/<folder>/<repo>`). On the mac it is
the same via SMB under `/Volumes/dev/...`. **Do not derive the path from folder/project/repo blindly** —
for a session with its own worktree that directory does not exist (or belongs to an unrelated old tree)
and the patch would end in a misleading `PATCH_CONFLICT`.

Get the patch into the working directory via SMB, then apply it in the container:

```bash
if [ -n "$WT" ]; then WS_MAC="/Volumes/dev/${WT#/srv/dev/}"          # the session's own worktree
else WS_MAC="/Volumes/dev/$FOLDER/$PROJECT/$REPO"; [ "$FOLDER" = "$PROJECT" ] && WS_MAC="/Volumes/dev/$FOLDER/$REPO"; fi
cp /tmp/devbox-migrate.patch "$WS_MAC/.devbox-migrate.patch"
ssh "$SSH" "docker exec $ID bash -lc 'cd /workspace && git fetch --all -q && (git checkout $BRANCH 2>/dev/null || git checkout -b $BRANCH) && (git apply --3way .devbox-migrate.patch || echo PATCH_CONFLICT) ; rm -f .devbox-migrate.patch'"
```

`/workspace` inside the container points to the right directory in both layouts (devd
mounts it), so the second line does not change — only the path on the mac differs.

### 5) (PoC) Transfer the conversation transcript

Target in the container: `/home/dev/.claude/projects/-workspace/<uuid>.jsonl` (the shared
claude-home volume; a session in `/workspace` is stored exactly here).

```bash
if [ -n "$UUID" ]; then
  scp "$PROJDIR/$UUID.jsonl" "$SSH:/tmp/$UUID.jsonl"
  ssh "$SSH" "docker exec $ID bash -lc 'mkdir -p ~/.claude/projects/-workspace' && docker cp /tmp/$UUID.jsonl $ID:/home/dev/.claude/projects/-workspace/$UUID.jsonl && docker exec -u root $ID chown 1000:1000 /home/dev/.claude/projects/-workspace/$UUID.jsonl && rm -f /tmp/$UUID.jsonl"
fi
```

**Limitation (hence PoC):** the transcript contains absolute local paths (`/Users/...`)
and a `cwd` that do not match `/workspace` in the container. The conversation shows up in `--resume`
and can be continued, but the tool history points to other paths; it may not continue 1:1.
Treat it as "I have the context, I'll continue", not as a perfect clone.

### 6) Start the migrated session in the devbox (auto-start)

The skill **starts the session by itself** (`cc --resume $UUID`) in a new tmux window and sends
`continue`, so after the migration it is already running — you do not have to do anything manually. At startup the container
launches only a clean session in tmux `main`; it does not know about the migrated transcript, so
we have to kick it off here explicitly. A guard does not create a second copy when `--resume $UUID` is
already running (otherwise sessions pile up in the container).

When you do not have `$UUID` (the transcript was not transferred), skip the auto-start and just print
`dev attach $ID` — in a clean devbox the session is then created normally.

```bash
ssh "$SSH" "docker exec -i $ID bash -s" <<REMOTE
set -u
# 1) Guard: is this resume session already running? If so, do not create a second one.
if pgrep -f -- "--resume $UUID" >/dev/null 2>&1; then
  echo "ALREADY_RUNNING"; exit 0
fi
# 2) Start the resume in a NEW window of group 'main' (does not touch running old sessions; the new
#    window is active, so 'dev attach' lands on it). RC comes up via DEVD_SESSION_ID.
WID=\$(tmux new-window -t main -c /workspace -P -F '#{window_id}' "cc --resume $UUID")
echo "WINDOW=\$WID"
# 3) Wait for the input prompt (max ~40 s), then send 'continue'.
for i in \$(seq 1 20); do
  sleep 2
  if tmux capture-pane -p -t "\$WID" -S -3 | grep -q '❯'; then
    tmux send-keys -t "\$WID" 'continue' Enter
    echo "CONTINUE_SENT WID=\$WID"; exit 0
  fi
done
echo "TIMEOUT WID=\$WID"   # the window was created, the prompt just did not appear in time
REMOTE
```

Evaluate the last line of the output and **verify** (do not rely on "it should be running"):
- `ALREADY_RUNNING` → the session is already running, do not start anything.
- `CONTINUE_SENT WID=@x` → verify with `ssh "$SSH" "docker exec $ID tmux capture-pane -p -t @x -S -10"`;
  when `continue` did not go through (the prompt was still `❯ continue` with no reaction), send it again:
  `ssh "$SSH" "docker exec $ID tmux send-keys -t @x continue Enter"`.
- `TIMEOUT WID=@x` → the window is created, the session will come up; just type `continue` yourself after attaching.

Finally, summarize for the user: the session id, what was transferred (branch pushed? patch
applied/conflict? transcript yes/no), that **the session is already running in the devbox**, and the command
to attach: `dev attach $ID`. Note: there may be several windows in `main` — switch with `Ctrl-b n`
(next) / `Ctrl-b w` (list), detach without killing with `Ctrl-b d`.

## Cleanup on failure
- Delete `.devbox-migrate.patch` from the workspace and `/tmp` on both sides.
- When the session was created by mistake: `dev end <id>` (for solo it asks keep/delete).

## Notes
- Not transferred: running processes, ENV, open ports (you start those again in the devbox).
- A `git apply --3way` conflict = resolve it manually in the devbox (Claude has the context for it there).
- Canonical source of the skill: `tools/skills/local-to-devbox/` in the **VPSbetter** repo,
  symlinked to `~/.claude/skills/local-to-devbox` (so it works from any repo).
  Also published in the **team marketplace** — that is how it is distributed to other machines.
