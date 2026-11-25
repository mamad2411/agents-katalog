---
name: clean-slate
description: Full board-steward teardown for a fresh-user / first-run test. Use when the user wants to wipe ALL board-steward state — kill the board server(s) and ports, remove autostart, purge ~/.board-steward (port registry + .onboarded marker), delete board.json(s), and uninstall the plugin — so a later reinstall starts truly clean and the first-run picker/popup fires. Triggers: "clean slate", "wipe the board", "kill all boards/ports", "fresh user test", "reset board-steward", "tear it all down so reinstall is clean".
---

# clean-slate — wipe board-steward to a fresh-user state

Tears down every piece of board-steward runtime state so the next reinstall
behaves exactly like a brand-new user: no stale server holding a port, no
`.onboarded` marker suppressing the first-run picker, no leftover board.json.

**Always backs up first.** Everything removed is copied to a timestamped
`~/board-steward-cleanslate-backup-<ts>/` dir, restorable by hand.

## When to use
- The user wants to rehearse the first-run experience ("watch the cards fly").
- They fear a reinstall will reuse an old port/server and skip the popup.
- They say: clean slate, wipe the board, kill all ports, reset, fresh user test.

## What it removes
1. **Servers + ports** — kills every listener on the board port range (7891–7999) and stray `serve.py --project` processes.
2. **Autostart** — boots out + deletes the launchd agent (`com.boardsteward.*`).
3. **`~/.board-steward/`** — the port registry **and** the `.onboarded` marker (this is what re-arms the first-run picker).
4. **board.json(s)** — plus runtime sidecars (`index.json`, `.spawn.lock`, `recon_pending.json`, `extraction_*.json`, `.opened-*`, `.subagent_queue.jsonl`, `.stop_recon_state.json`, `.card_before_edit_state.json`) for every registered board + the default repo board.
5. **Plugin** — `claude plugin uninstall board-steward@workboard` (skip with `--no-plugin`).
6. **Plugin cache** — `~/.claude/plugins/cache/*/board-steward` (skip with `--no-plugin`). Uninstall alone leaves the cache, and installs key by **version** — so a same-version reinstall replays **stale** cached code. Clearing it makes a plain reinstall pull **fresh repo code** with no manual version bump.

## How to run
The script is bundled next to this file. Run it:

```bash
bash ~/.claude/skills/clean-slate/clean_slate.sh            # full wipe + plugin uninstall
bash ~/.claude/skills/clean-slate/clean_slate.sh --dry-run  # preview, change nothing
bash ~/.claude/skills/clean-slate/clean_slate.sh --no-plugin # keep plugin, wipe runtime only
bash ~/.claude/skills/clean-slate/clean_slate.sh --repo=/path/to/repo  # non-default board repo
```

Default board repo is `~/Desktop/WorkBoard` (override with `--repo=` or `BOARD_REPO`).

## After running
1. Reinstall the plugin: `claude plugin install board-steward@workboard --scope user`. Because the cache was cleared (step 6), this pulls **fresh** code from the repo even if the version is unchanged — no manual bump needed.
2. Open a NEW terminal, `cd ~`, start `claude` — the first-run picker should fire
   (because `.onboarded` is gone), enumerate the user's projects, and on pick fly
   the cards into a fresh board.
3. Verify clean state:
   - `curl -s --max-time 0.4 http://127.0.0.1:7891/health` → empty (no server)
   - `ls ~/.board-steward` → "No such file or directory"

## Restore (if needed)
Everything is in the printed backup dir. To bring the old board back:
`cp <backup>/boardjson_*.json ~/Desktop/WorkBoard/board/board.json` and
`cp -R <backup>/dot-board-steward ~/.board-steward`, then restart the server /
reinstall autostart.
