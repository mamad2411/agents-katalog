---
name: token-wise
description: Tidy up at a natural break so tokens and the machine's resources are used wisely. Stops background work this session started, shuts down simulators it booted, deletes its own scratch and build output, lists (never deletes) the user's own large folders, and recommends exactly one of /clear or /compact plus a model hint. Use when a task is finished, before handing over, after a long build-and-test stretch, or when asked to "tidy up", "save tokens" or "clean up".
allowed-tools: Bash(du *) Bash(xcrun simctl list *) Bash(lsof *) Bash(ps *) Bash(ls *)
---

# Token-wise: tidy up at a natural break

Invoked as `/dev-workflow:token-wise` when installed as a plugin, or `/token-wise` if the folder is copied into `~/.claude/skills/`.

Goal: leave nothing running or lying around that this session created, and make the next part of the work cheap. Quality first: never trade correctness for savings.

## Context
- Booted simulators (macOS with Xcode only; prints "none" elsewhere): !`xcrun simctl list devices booted 2>/dev/null | grep -i booted || echo "none"`
- Listening ports (yours only if this session started them): !`lsof -iTCP -sTCP:LISTEN -n -P 2>/dev/null | head -25 || true`
- Xcode DerivedData: !`du -sh ~/Library/Developer/Xcode/DerivedData 2>/dev/null || echo "none"`

## Steps

0. **Find the project root.** The context lines above describe the folder Claude was started in, which may not be the project the task lives in (for example a fork or a parent folder). If the argument or the task's docs are in another folder, go there and re-check `git status --short --ignored` there before going on. Treat the context lines as hints only.
1. **Audit** (read-only). Use the context above, plus:
   - background shells, monitors and agents this session started (your own task list and their IDs);
   - your scratchpad folder, if the session has one: `du -sh <scratchpad>`, and its largest items (`du -sh <scratchpad>/* | sort -h | tail`);
   - build output this session wrote inside the repo, only if it is untracked and newer than the session (`git status --short --ignored`, then check dates).
2. **Close and delete only what this session started or created.** Open and read [cleanup.md](cleanup.md) first, then follow it to decide. Keep anything a pending step still needs (for example, the last Release build before a `test-feature` rerun, or a file the user is about to review).
3. **List, never touch, everything else that is large:** DerivedData folders per project (`du -sh ~/Library/Developer/Xcode/DerivedData/*`), `node_modules` in projects not opened for 30+ days, big untracked files. Give each one's size and the exact command to remove it. It's the user's decision.
4. **One context recommendation** (at most one per break):
   - `/clear` when the next work is unrelated, or the conversation is long and the work is safely written down. First write `docs/implementation/<task>/handoff.md` (in the project's docs layout) with: where things stand, decisions, files changed, open questions, and the next step. Say that `/clear` is free and that a new session can start from that file.
   - `/compact <instructions>` when the same work continues and the details matter. Give ready-to-paste instructions tailored to the task (keep the spec and plan paths, decisions, files changed, test results and open questions; drop logs and dumps). Note that compacting a long conversation is itself one large request.
   - Nothing, if the conversation is short.
5. **Model hint:** if the session runs on Opus and the next step is mechanical (running tests, copying logs, routine edits), suggest `/model sonnet` for it, and switching back with `/model opus` for specs and reviews. Only a suggestion; the main model is the user's choice.
6. **Report** in a short table: closed, deleted (with sizes), listed for the user (with sizes and commands), and the one recommendation.

## Rules
- Never delete simulators, devices' app data, the Keychain, or anything tracked by git or older than this session.
- Never kill a process this session didn't start. Dev servers you didn't start are listed, not stopped.
- Never run `/clear` or `/compact` yourself (you can't), and never change the user's model setting.
- If unsure whether something is yours, list it instead of deleting it.
