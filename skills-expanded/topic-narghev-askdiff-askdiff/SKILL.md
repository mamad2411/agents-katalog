---
name: askdiff
description: Start the askdiff WebSocket server for interactive diff review.
user-invocable: true
allowed-tools: Bash
---

Compute the user's diff, write it to a temp file, then launch the
`askdiff` CLI in the background pointing at that file.

> **Keep Steps 1–4 in sync with `.claude/skills/askdiff-dev/SKILL.md`** —
> only the Step 4c `resolve-session` invocation and Step 5 launch differ
> between the two skills.

## Step 1 — figure out which diff the user wants (and which session)

Look at the message that invoked this skill. Anything after `/askdiff` is
free-form natural language that may carry **two** kinds of information:

1. A **diff description** — what to diff (handled by the table/ladder
   below). This part is what Step 2 turns into a `git diff` command.
2. An optional **session hint** — which Claude session to attach to
   (handled by the *Session hint* subsection at the end of this step,
   then resolved in Step 4).

Either or both may be empty. The diff-description part may be empty
(working tree); the session hint defaults to "the invoking session" when
absent. Treat them independently — first identify and set aside the
session hint, then pass the rest to the diff resolution below.

**Use only the current `/askdiff` line's args.** Read `<command-args>`
strictly from the message that invoked this skill — nothing else. Do
*not* infer or carry over args from earlier conversation turns, from
`SessionStart` hook context (e.g. a "Previous session summary" block
that quotes a prior `/askdiff` invocation verbatim), from CLAUDE.md, or
from memory. If the current line has no text after `/askdiff`, both
`diff_description` and `session_hint` are empty/none — that means
working tree + invoking session, full stop.

| `diff_description` | git command | Suggested label |
|---|---|---|
| (empty) | working tree — see Step 2 | `Working tree` |
| `last commit` | `git diff HEAD~1 HEAD` | `HEAD~1..HEAD` |
| `last 3 commits` | `git diff HEAD~3 HEAD` | `HEAD~3..HEAD` |
| `the 5th latest commit` | `git diff HEAD~5 HEAD~4` | `HEAD~5..HEAD~4` |
| `current branch against feature/test` | `git diff feature/test...HEAD` (three-dot, PR semantics) | `feature/test…HEAD` |
| `main vs my branch` | `git diff main...HEAD` | `main…HEAD` |
| `abc123 vs def456` | `git diff abc123 def456` | `abc123..def456` |
| `staged` | `git diff --cached` | `staged` |

Defaults when the user is ambiguous:
- "branch X against branch Y" / "X vs Y" between two named refs ⇒ three-dot
  (`git diff X...Y`) — matches how GitHub renders PRs.
- Two arbitrary commits ⇒ two-dot (`git diff A B`).
- "Nth latest commit" ⇒ that single commit's changes
  (`git diff HEAD~N HEAD~(N-1)`).

### When the description is vague

If the description doesn't fit the table (e.g. "the commit where I added
the favicon", "where we ripped out the old auth"), pin down a single
commit with the ladder below, then diff `<sha>^..<sha>`. Try in order
until exactly one commit matches; if several match, pick the most recent
and **tell the user which one you chose**; if none match, stop and ask —
do not guess.

1. **Author.** "by <name>", "<name>'s last", "by my coworker":
   ```bash
   git log --author=<pattern> -i -1 --format='%H %an %s'
   ```

2. **Commit message.** "the migration commit", "where I bumped deps":
   ```bash
   git log --grep=<keyword> -i -1 --format='%H %s'
   ```

3. **Diff content.** "where I added/removed/touched <thing>". `-S` matches
   when a string's count changed in any file; `-G` is a regex over the
   diff text:
   ```bash
   git log -S"<distinctive-string>" -1 --format='%H %s'
   git log -G"<regex>" -1 --format='%H %s'
   ```

4. **File history.** When you can identify the file but not the commit
   (e.g. "where the homepage was added" — search the working tree for a
   plausible path first, then ask git):
   ```bash
   git ls-files | grep -i <hint>                                     # find candidate path
   git log --follow -1 --format='%H %s' -- <path>                    # most recent touch
   git log --follow --diff-filter=A -1 --format='%H %s' -- <path>    # commit that introduced it
   ```

Once a SHA is in hand, build the label as `<short-sha>: <one-line gloss>`
(e.g. `d0b332b: add favicon`) and use `git diff <sha>^ <sha>` as the
diff command. If the user's count and description disagree (e.g. "my 3rd
previous commit, where I added a favicon" but the favicon is at HEAD~2),
trust the description over the count and **flag the off-by-one to the
user** so they know what you picked.

**Stay within git — never read file contents to disambiguate.** Use only
`git log` (with `--author`, `--grep`, `-S`, `-G`, `--follow`,
`--diff-filter`) and `git ls-files | grep` on path names. Don't `cat`,
`grep -r`, `rg`, or `Read` working-tree contents. If the ladder doesn't
pin down a unique commit, AskUserQuestion with the candidates — reading
files during search is a token-cost cliff that requires user consent.

**Validate every ref first.** Run `git rev-parse --verify <ref>^{commit}` for
each ref the user named directly. If any fails, stop and tell the user
which ref didn't resolve — do not launch the server. (Refs returned by the
search ladder are already validated by virtue of `git log` finding them.)

### Session hint (optional)

By default `/askdiff` attaches the WS server to the **invoking** session
(the one running this skill). The user may override that by carrying a
phrase about the target session in their input. Decompose the input into
two parts:

- `diff_description` — what to diff (everything Step 1's table/ladder uses)
- `session_hint` — one of `none`, `explicit-id <uuid-or-prefix>`, or
  `keywords <a, b, c, …>`

A session hint shows up as language about the *session/conversation/chat*
the diff comes from — e.g. "attached to the session …", "in our session
about X", "from the chat where Y", "session id `<uuid>`", or a bare
UUID-shaped token (8+ hex chars).

**Examples:**

| User input | `diff_description` | `session_hint` |
|---|---|---|
| `last commit` | `last commit` | none |
| (empty) | (working tree) | none |
| `the staleness commit attached to the session where we discussed mtime checks` | `the staleness commit` | keywords: "mtime checks" |
| `last commit in our session about pricing rules and tax math` | `last commit` | keywords: "pricing rules", "tax math" |
| `session 322bc90a` | (working tree) | explicit-id: `322bc90a` |
| `abc123 vs def456 in session 322bc90a-714f-41b7-914e-109404e46072` | `abc123 vs def456` | explicit-id: full UUID |

**Be conservative.** If parsing is itself ambiguous (e.g. "the foo session"
— is "session" a noun in the diff or a trigger?), treat the whole input
as `diff_description` (no session hint). Don't ask the user to clarify the
parse — just resolve the diff and proceed; the default attachment to the
invoking session is always safe.

The session hint is consumed in Step 4. Steps 2 and 3 use only
`diff_description`.

## Step 2 — write the diff to a session-stable file

First resolve the parent Claude Code session and project cwd. All `/tmp`
paths the skill writes (diff file, server log, dev-only UI log/pid file)
key off the session UUID so concurrent `/askdiff` runs from different
sessions don't collide:

```bash
session_file="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/sessions/$PPID.json"
session_id=""
project_cwd="$PWD"
if [ -f "$session_file" ]; then
  session_id=$(sed -n 's/.*"sessionId":"\([^"]*\)".*/\1/p' "$session_file")
  manifest_cwd=$(sed -n 's/.*"cwd":"\([^"]*\)".*/\1/p' "$session_file")
  [ -n "$manifest_cwd" ] && project_cwd="$manifest_cwd"
fi
suffix="${session_id:-pid-$$}"
diff_file="/tmp/askdiff-diff.$suffix"
```

No random component on the diff file — re-invoking `/askdiff` from the
same session overwrites in place, which is exactly what a refresh would
do. Different sessions get different suffixes and don't collide. (If
launched outside a CC session, `session_id` is empty and the suffix
falls back to `pid-<bash-pid>` so we still avoid collisions.)

**Working tree (no description).** Untracked files don't appear in
`git diff HEAD`, so we union them in via `--no-index`:

```bash
{
  git -C "$project_cwd" diff HEAD --no-color
  git -C "$project_cwd" ls-files --others --exclude-standard -z \
    | while IFS= read -r -d '' f; do
        git -C "$project_cwd" diff --no-index --no-color -- /dev/null "$f" || true
      done
} > "$diff_file"
```

(In an empty repo with no HEAD, replace `HEAD` with the empty-tree SHA
`4b825dc642cb6eb9a060e54bf8d69288fbee4904`.)

**Description path.** Just run the resolved command:

```bash
git -C "$project_cwd" diff <args> --no-color > "$diff_file"
```

For the description path, if the resulting file is empty, **stop** — tell the
user the requested diff is empty and don't launch. The working-tree path
*can* legitimately be empty (clean tree); launch anyway and the UI will
show "No changes."

Set `volatile=1` for the working-tree path, `volatile=0` otherwise — Step 5
forwards this as `ASKDIFF_DIFF_VOLATILE` (gates per-file mtime staleness).

## Step 3 — pick a short label

Use the "Suggested label" column above. For the working-tree case, use
`Working tree`. Keep it under ~40 chars. This becomes `ASKDIFF_DIFF_LABEL`.

## Step 4 — resolve the target session

Compute `attached_session` and `session_source` from `session_hint`
(from Step 1). Default is the invoking session.

```bash
attached_session="$session_id"      # default = invoking
session_source="invoking"

sessions_dir="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/projects/$(echo "$project_cwd" | tr '/' '-')"
```

### 4a. No hint → invoking session (default)

If `session_hint` is `none`, leave the defaults and skip to Step 5.

### 4b. Explicit ID → resolve

If `session_hint` is `explicit-id <X>`:

```bash
explicit_id="<X>"

if echo "$explicit_id" | grep -qE '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'; then
  # Full UUID: trust it if the file exists.
  if [ -f "$sessions_dir/$explicit_id.jsonl" ]; then
    attached_session="$explicit_id"
    session_source="explicit"
  else
    # → AskUserQuestion: session not found, use current?
    :
  fi
else
  # Short prefix: list and disambiguate via `find` (zsh-compatible — see
  # footgun in CLAUDE.md: `shopt` is bash-only and silently fails in zsh,
  # and zsh arrays are 1-indexed so `${matches[0]}` returns empty).
  matches=()
  while IFS= read -r f; do
    [ -n "$f" ] && matches+=("$f")
  done < <(find "$sessions_dir" -maxdepth 1 -name "${explicit_id}*.jsonl" -type f 2>/dev/null)
  case ${#matches[@]} in
    1)
      # Iterate to dodge bash-vs-zsh first-index difference.
      for f in "${matches[@]}"; do
        attached_session=$(basename "$f" .jsonl)
        session_source="explicit"
      done
      ;;
    0)
      # → AskUserQuestion: no session matches "<prefix>", use current?
      : ;;
    *)
      # → AskUserQuestion: pick one of N candidates (list short-uuid · age)
      : ;;
  esac
fi
```

AskUserQuestion branches: 0 matches → "Use current session" or "Cancel"
(don't launch). Multiple matches → one option per UUID as
`<short-uuid> · <age>` plus "Use current session"; on user pick set
`attached_session` and `session_source="explicit"`.

### 4c. Keywords → resolve-session, decide, possibly ask

If `session_hint` is `keywords <a, b, c, …>`, call the CLI's
`resolve-session` subcommand. It searches recent project JSONLs (mtime
−30d, excluding the invoking session, top 5 by hit count) and prints
single-line JSON: `{"candidates":[{"uuid":"…","count":N,"age":"…"}, …]}`.

```bash
# Pinned by the build script for the npm tarball; in-repo stays "latest".
ASKDIFF_VERSION="latest"

results=$(
  npx -y askdiff@"$ASKDIFF_VERSION" resolve-session \
    --cwd "$project_cwd" \
    --invoking "$session_id" \
    --diff-file "$diff_file" \
    --keyword "<keyword 1>" \
    --keyword "<keyword 2>" \
    --sha "<sha1>" \
    --sha "<sha2>" \
    --branch "<branch1>" \
    --branch "<branch2>"
)
echo "$results"
```

Repeat `--keyword`/`--sha`/`--branch` per value; omit a flag entirely
if its list is empty. Always pass `--diff-file` (changed file paths feed
the search as additional needles regardless of diff source); omit `--sha`
and `--branch` for working-tree diffs (no commit/branch context).

Read `$results` and route on `.candidates`:

| Result | Action |
|---|---|
| empty | AskUserQuestion: "no session matched `<keywords>`. Use current?" → "Use current" or "Cancel and refine" |
| 1 candidate | use that UUID; `attached_session=$uuid`, `session_source="matched"` |
| 2+, top count ≥ 2× second | use top-1; `session_source="matched"` |
| 2–5, comparable counts | AskUserQuestion: one option per candidate as `<short-uuid> · <age> · <count> hits`, plus "Use current session" |

**Don't widen scope automatically** (e.g. by raising `--max-age-days` or
`--top`). Surface 0/unclear results via AskUserQuestion; re-run only on
user request.

## Step 5 — launch

Run as a single Bash command. Substitute `EXTRA_DIFF_FILE` and
`EXTRA_DIFF_LABEL` literally with the values from Step 2/3.

```
set +e

# Pinned by the build script for the npm tarball; in-repo stays "latest".
ASKDIFF_VERSION="latest"

# Filled in by Steps 2/3 — keep Step 2's preamble (session_id, project_cwd,
# suffix) and Step 4's resolution (attached_session, session_source) above.
EXTRA_DIFF_FILE=""
EXTRA_DIFF_LABEL=""

log_file="/tmp/askdiff.$suffix.log"
pid_file="/tmp/askdiff.$suffix.pid"

# 1. Kill any previous server for this session and reuse its port — keeps
#    the open browser tab valid (the WS auto-reconnects).
saved_port=""
if [ -f "$pid_file" ]; then
  read -r old_pid saved_port < "$pid_file" 2>/dev/null
  if [ -n "$old_pid" ] && kill -0 "$old_pid" 2>/dev/null; then
    kill "$old_pid" 2>/dev/null
    if [ -n "$saved_port" ]; then
      for _ in $(seq 1 20); do
        lsof -iTCP:"$saved_port" -sTCP:LISTEN -t >/dev/null 2>&1 || break
        sleep 0.1
      done
    fi
  fi
  rm -f "$pid_file"
fi

# 2. Launch. Reuse port if we have one; otherwise the CLI picks 7837+.
port_arg=""
[ -n "$saved_port" ] && port_arg="--port $saved_port"

cd "$project_cwd" \
  && ASKDIFF_SESSION_ID="$attached_session" \
     ASKDIFF_PROJECT_CWD="$project_cwd" \
     ASKDIFF_DIFF_FILE="$EXTRA_DIFF_FILE" \
     ASKDIFF_DIFF_LABEL="$EXTRA_DIFF_LABEL" \
     ASKDIFF_DIFF_VOLATILE="${volatile:-0}" \
     nohup npx -y askdiff@"$ASKDIFF_VERSION" --no-open $port_arg > "$log_file" 2>&1 &
new_pid=$!
disown

# Wait for the listening line. (`command grep` — see Step 4c footguns.)
for _ in $(seq 1 60); do
  command grep -q "listening on" "$log_file" 2>/dev/null && break
  sleep 0.25
done

# 3. Persist <pid> <port> for the next /askdiff invocation to find and replace.
port=$(sed -nE 's|.*listening on http://localhost:([0-9]+).*|\1|p' "$log_file" | head -1)
[ -z "$port" ] && port=7837
echo "$new_pid $port" > "$pid_file"

url="http://localhost:$port/"

# Auto-open only on first launch — refresh re-invocations have a tab open.
if [ -z "$saved_port" ]; then
  (open "$url" >/dev/null 2>&1 || xdg-open "$url" >/dev/null 2>&1) &
fi

head -10 "$log_file"
echo ""
[ -n "$saved_port" ] && echo "Refreshed: same port, new diff. Browser tab will auto-reconnect."
echo "UI: $url"
echo "Log: $log_file"
echo "PID: $new_pid (saved to $pid_file)"

# 4. Update check (after launch, never blocking; skipped at "latest" or
#    when ASKDIFF_SKIP_UPDATE_CHECK is set; network failures silently ignored).
if [ -z "$ASKDIFF_SKIP_UPDATE_CHECK" ] && [ "$ASKDIFF_VERSION" != "latest" ]; then
  latest=$(curl -fsSL --max-time 2 https://registry.npmjs.org/askdiff/latest 2>/dev/null \
    | sed -n 's/.*"version":"\([^"]*\)".*/\1/p' | head -1)
  if [ -n "$latest" ] && [ "$latest" != "$ASKDIFF_VERSION" ]; then
    echo ""
    echo "── A new version of askdiff is available ──"
    echo "  installed: $ASKDIFF_VERSION"
    echo "  latest:    $latest"
    echo "  to update: npx -y askdiff@latest install-skill --force"
    echo "             (add --global if you installed user-level)"
  fi
fi
```

The user already sees `UI:` / `Log:` / `PID:` / `Refreshed:` / the
new-version block in the bash output. After launch, only narrate:

- if `$session_source` is `explicit` or `matched`, say so (e.g.
  "attached to matched session 322bc90a (was: invoking)") so the user
  knows asks aren't landing in the current session's transcript
- the new-version block verbatim if present — the upgrade command is
  copyable as-is, no `AskUserQuestion` needed
