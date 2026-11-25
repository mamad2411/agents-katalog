---
name: ystack-upgrade
description: >-
  Upgrade ystack to the latest version: pull the checkout, re-run its setup for the same agent hosts
  (and agent files, if installed), update the ystack marketplace and installed ystack mods, and show
  what changed. Use when asked to "upgrade ystack", "update ystack", or "get the latest ystack".
---

# /ystack-upgrade

Upgrade the user's ystack checkout and everything installed from it, then report what changed. Run
the steps in order with the Bash tool. Stop and report on any failure; never reset, stash or discard
the user's changes to make a pull succeed.

Shell variables may not survive between separate Bash calls. Each step prints the values it found
(`YSTACK_DIR`, `HOSTS`, `OLD`, `NEW`); set them again at the top of the next call, or run the steps
together in one call.

## Step 1: find the checkout

Skills installed by ystack point back at the checkout: a symlink resolves into `<checkout>/skills/`,
and a copied skill carries a `.ystack` file whose `source=` line names it.

```bash
YS=""
for d in "$HOME/.claude/skills" "${CODEX_HOME:-$HOME/.codex}/skills" "$HOME/.config/opencode/skills"; do
  for e in "$d"/*; do
    if [ -L "$e" ]; then
      t="$(cd -P "$e" 2>/dev/null && pwd -P)" || continue
      r="$(dirname "$(dirname "$t")")"
    elif [ -f "$e/.ystack" ]; then
      r="$(sed -n 's/^source=//p' "$e/.ystack")"
    else
      continue
    fi
    if [ -f "$r/setup" ] && grep -q '"name": *"ystack"' "$r/.claude-plugin/marketplace.json" 2>/dev/null; then
      YS="$r"; break 2
    fi
  done
done
if [ -z "$YS" ] && [ -f "$HOME/ystack/setup" ]; then YS="$HOME/ystack"; fi
echo "YSTACK_DIR=${YS:-NOT_FOUND}"
```

If it prints `NOT_FOUND`, ask the user where their ystack checkout is (the folder that holds `setup`),
and set `YS` to that path. If they don't have one, tell them how to get it and stop:
`git clone https://github.com/ychampion/ystack.git ~/ystack && ~/ystack/setup`.

## Step 2: work out what was installed

Re-run setup for the hosts that already hold ystack skills, and with `--agents` if ystack installed
agent files before.

```bash
HOSTS=""
DEVIN_SKILLS="$HOME/.config/devin/skills"
case "$(uname -s 2>/dev/null)" in MINGW*|MSYS*|CYGWIN*)
  [ -n "${APPDATA:-}" ] && DEVIN_SKILLS="$(cygpath -u "$APPDATA" 2>/dev/null || echo "$APPDATA")/devin/skills" ;;
esac
for pair in "claude:$HOME/.claude/skills" "codex:${CODEX_HOME:-$HOME/.codex}/skills" "opencode:$HOME/.config/opencode/skills" \
            "antigravity:$HOME/.gemini/config/skills" "devin:$DEVIN_SKILLS"; do
  h="${pair%%:*}"; d="${pair#*:}"
  for e in "$d"/*; do
    if { [ -L "$e" ] && case "$(cd -P "$e" 2>/dev/null && pwd -P)" in */skills/*) true ;; *) false ;; esac; } || [ -f "$e/.ystack" ]; then
      HOSTS="$HOSTS,$h"; break
    fi
  done
done
HOSTS="${HOSTS#,}"
AGENTS_FLAG=""
[ -f "$HOME/.claude/agents/.ystack-manifest" ] && AGENTS_FLAG="--agents"
echo "HOSTS=${HOSTS:-auto} AGENTS=${AGENTS_FLAG:-no}"
```

A symlink only counts if it resolves into a ystack checkout; the check above is a quick filter, and
setup itself applies the strict ownership rule, so a stray user symlink is never touched.

## Step 3: pull

```bash
: "${YS:?set YS from step 1}"
cd "$YS" || { echo "PULL_FAILED: cannot cd to $YS"; exit 1; }
git rev-parse --git-dir >/dev/null 2>&1 || { echo "PULL_FAILED: $YS is not a git checkout"; exit 1; }
git status --porcelain | head -5
OLD="$(git rev-parse HEAD)" || { echo "PULL_FAILED: no commit checked out in $YS"; exit 1; }
if ! git pull --ff-only; then echo "PULL_FAILED OLD=$OLD"; exit 1; fi
NEW="$(git rev-parse HEAD)"
echo "OLD=$OLD NEW=$NEW"
```

- If the output contains `PULL_FAILED`, or the block exits non-zero, stop. Tell the user what git said
  and leave the checkout as it is. Never treat a failed pull as "already up to date". A folder that
  isn't a git checkout (a zip download) can't be upgraded this way: tell the user to clone it instead.
- Local changes in the checkout are fine as long as the pull succeeds; mention them in the report.
- If `OLD` equals `NEW`, ystack was already up to date. Still run Step 4 (it repairs anything removed
  by hand) and skip the change list.

## Step 4: re-run setup

```bash
: "${YS:?set YS from step 1}"
LOG="$(mktemp "${TMPDIR:-/tmp}/ystack-setup.XXXXXX")" || { echo "SETUP_FAILED: mktemp failed"; exit 1; }
"$YS/setup" --host "${HOSTS:-auto}" $AGENTS_FLAG >"$LOG" 2>&1
rc=$?
if [ "$rc" -ne 0 ]; then echo "SETUP_FAILED rc=$rc; last lines:"; tail -n 20 "$LOG"; rm -f "$LOG"; exit 1; fi
cat "$LOG"; rm -f "$LOG"
```

- If the output starts with `SETUP_FAILED`, stop before Step 5. Show the user the lines printed
  under it (they include setup's `FAILED (reason)` lines) and say nothing else was upgraded.
- Setup never replaces a skill or agent file that isn't ystack's, or a ystack copy the user edited;
  its summary lists anything it skipped and why. Pass those lines on to the user.
- If Step 2 found no hosts, `--host auto` installs into every agent host folder that exists, not
  only ones that had ystack before. Say so in the report.

## Step 5: update the mods

```bash
if ! command -v claude >/dev/null 2>&1; then
  echo "CLAUDE_CLI=missing"
elif ! mk="$(claude plugin marketplace list --json 2>&1)"; then
  echo "MARKETPLACE_LIST=failed: $(printf '%s\n' "$mk" | head -1)"
elif ! printf '%s' "$mk" | grep -q '"name": *"ystack"'; then
  echo "MARKETPLACE=not_added"
else
  if claude plugin marketplace update ystack; then echo "MARKETPLACE_UPDATE=ok"; else echo "MARKETPLACE_UPDATE=failed"; fi
  if ! pl="$(claude plugin list --json 2>&1)"; then
    echo "PLUGIN_LIST=failed: $(printf '%s\n' "$pl" | head -1)"
  else
    echo "PLUGIN_LIST=ok"
    for id in $(printf '%s' "$pl" | grep -o '"id": *"[^"]*@ystack"' | sed 's/.*"\([^"]*\)"$/\1/'); do
      if claude plugin update "$id"; then echo "UPDATED $id"; else echo "FAILED $id"; fi
    done
  fi
fi
```

Report from the marker lines, not from the exit code:
- `CLAUDE_CLI=missing`: mods were not updated (no `claude` CLI).
- `MARKETPLACE=not_added`: the ystack marketplace isn't added, so there are no ystack mods to update.
  Say so; don't add it unasked.
- `MARKETPLACE_LIST=failed` or `PLUGIN_LIST=failed`: say that setup couldn't tell which mods are
  installed, with the error. Never report that as "no mods to update".
- `MARKETPLACE_UPDATE=failed`: the mod updates below it may have used the old marketplace copy; say so.
- `UPDATED <id>` and `FAILED <id>`: list each. Updated mods load after Claude Code restarts.

## Step 6: report

```bash
: "${YS:?set YS from step 1}" "${OLD:?set OLD from step 3}" "${NEW:?set NEW from step 3}"
[ "$OLD" = "$NEW" ] || git -C "$YS" log --oneline "$OLD..$NEW"
```

Report, in this order:
1. Old and new commit (short SHAs), or "already up to date".
2. What changed: the `git log` lines, grouped in plain words (new skills, mod changes, fixes).
3. Setup's summary per host, including anything skipped and why.
4. Which mods were updated (`UPDATED` lines), which failed (`FAILED` lines), and that Claude Code
   needs a restart to load the updated ones.
5. On Windows (copied skills), remind the user that `/ystack-upgrade` or `./setup` refreshes the
   copies after every pull.
