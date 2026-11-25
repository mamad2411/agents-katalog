---
name: babysit
description: Keep a PR merge-ready using Kart for shell work and a background CI watcher — not foreground poll loops.
---

@markdownai v1.0

# Babysit PR (Willow)

**b17:** BBSIT · ΔΣ=42

Get a PR to **mergeable + green** without holding the chat thread on `gh pr checks --watch`.

## Lanes

| Work | Tool |
|------|------|
| `gh`, `git`, pytest, push | `agent_task_submit` → `kart_task_run` (see `/kart`) |
| PR metadata, handoff context | Willow MCP or Kart `gh pr view` |
| **Waiting on CI** | **Background shell loop** + sentinel — not agent spin-wait |
| Merge when green | Kart `gh pr merge` (user asked to merge) |

## Foreground pass (once per wake)

1. Resolve repo + PR: `gh pr view <n> --json url,headRefName,baseRefName,mergeable,statusCheckRollup`
2. Triage **comments** — only unresolved; skip Bot noise unless valid.
3. If **merge conflict** — Kart: `git fetch && git merge origin/<base>` (or rebase per repo policy); fix in editor; commit via Kart.
4. If **CI failed** — Kart runs failing job locally or reads `gh run view --log-failed`; fix; commit; push with `allow_net=True`.
5. If **branch behind base** — Kart merge/rebase + push before re-watch.

Do **not** block the session on CI. After push or when CI already running → **arm watcher** (below).

## Background CI watcher (required for “babysit”)

Use the same contract as Cursor **`loop`** skill — monitored shell, unique sentinel.

```bash
# Example: PR #20 on safe-app-willow-grove — adjust REPO and PR
REPO=rudi193-cmd/safe-app-willow-grove
PR=20
SLEEP=90
while true; do
  sleep "$SLEEP"
  STATUS=$(gh pr checks "$PR" --repo "$REPO" 2>&1 | tail -20)
  MERGE=$(gh pr view "$PR" --repo "$REPO" --json mergeable -q .mergeable 2>/dev/null || echo UNKNOWN)
  echo "AGENT_LOOP_TICK_babysit {\"pr\":$PR,\"repo\":\"$REPO\",\"mergeable\":\"$MERGE\",\"checks\":\"$(echo "$STATUS" | tr '\n' ';')\"}"
done
```

1. Start with **Shell `block_until_ms: 0`** (background).
2. Set **`notify_on_output`** pattern `^AGENT_LOOP_TICK_babysit`.
3. Tell the user: **interval**, **PR link**, **“you can keep working — I’ll wake when checks change.”**
4. On wake: parse latest line — if all checks `pass` and `mergeable==MERGEABLE`, offer merge; if fail, **one foreground fix slice** then re-arm.

## Merge (only when user asked)

```text
agent_task_submit(app_id="<agent>", task="gh pr merge <n> --repo <owner/repo> --merge --delete-branch", allow_net=True)
kart_task_run(app_id="<agent>")
```

Never force-push `main`/`master` without explicit user request.

## Stop

User says stop → kill loop PID (from terminal metadata), confirm watcher dead.

## Anti-patterns

- ❌ `gh pr checks --watch` in the main agent thread
- ❌ Repeated `sleep 60` + check in chat without background shell
- ❌ Agent Bash for `git`/`gh` when Kart is available
- ❌ Fixing unrelated CI or weakening workflows to go green

## Related

- Cursor native `babysit` skill — foreground; prefer this file when Willow MCP is up
- `willow/fylgja/skills/kart.md` — execution plane
- `docs/SKILL_AUDIT_CURSOR_VS_WILLOW.md` — full skill map
