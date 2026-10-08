---
name: memorylake-status
description: Diagnose the MemoryLake plugin setup -- CLI, login, config, connectivity, conversation sync. Use when the user asks whether MemoryLake is working, or when recall or sync misbehaves.
name_en: MemoryLake status
description_en: Diagnose the MemoryLake plugin setup -- CLI, login, config, connectivity, conversation sync
user-invocable: true
argument-hint: Optional; run it as is
argument-hint-en: Optional; run it as is
---

Run the checks below in order, with your shell tool, and report each one as pass or fail with the
detail shown. Do not stop at the first failure — the user needs the whole
picture. End with the single most useful next action.

## 1. CLI installed

```bash
command -v memorylake || ls "$HOME/.memorylake/bin/memorylake" "$HOME/.local/bin/memorylake" 2>/dev/null
```

Report which location was found (a PATH install takes precedence, then the
plugin's private download, then the installer's `~/.local/bin`) and its
`memorylake version`. Missing everywhere → the plugin cannot do anything;
point at the memorylake-init skill, which can download a prebuilt binary.

## 2. jq installed

```bash
command -v jq
```

Missing → the plugin is inert and reports it: the session-start line says
recall is unavailable, no conversation is synced, and `ml-recall` refuses to
run. On macOS: `brew install jq`.

## 3. Logged in

```bash
memorylake auth status
```

Report the profile, base URL, and where each came from. Not logged in →
`memorylake auth login --api-key sk-...`.

## 4. Config

Two levels, merged key by key, the more specific one winning:

1. `.claude/memorylake.local.md` from the working directory up (walk up to
   `/`) -- optional per-folder override
2. `~/.memorylake/harness/config.md` -- the global default, shared with the
   other MemoryLake harnesses on this machine

Report which files are in effect and the values of `enabled`, `workspace`,
`actor`, `recall_reminder`, `sync_conversations` (and `sync_on_write`, which
it falls back to), and `status_line`. Neither file exists -> point at the
memorylake-init skill.

`workspace` is the only strictly required field; without it every hook exits
silently. Conversation sync additionally needs `actor`.

Also resolve and report this folder's **conversation-sync policy with its
source**: folder-file `sync_conversations` (explicit) > global `sync_deny`
prefix match > global `sync_conversations` > global `sync_on_write`. E.g.
"conversation sync: OFF -- matched `sync_deny: ~/work`".

## 5. Connectivity

Only if steps 1, 3, and 4 passed:

```bash
memorylake project list --workspace <workspace from config>
```

Report the project count. A failure here means recall is unavailable — say so
explicitly, because a silently unavailable memory backend is
indistinguishable from an empty memory unless someone says it out loud.

## 6. End-to-end recall

Only if step 5 passed:

```bash
"$HOME/.qwenworkcn/plugins-custom/memorylake/bin/ml-recall" "test" --top-k 1
```

An empty result is a pass — it proves the path works. A non-zero exit is a
failure; show stderr verbatim.

## 7. Conversation sync

```bash
ls -t "$HOME"/.memorylake/harness/state/qwenwork/*/sync.json 2>/dev/null | head -n 3 | xargs -I{} sh -c 'echo "== {}"; cat "{}"; echo'
```

Each file is one QwenWork session; the newest is almost certainly this one.
Report `last_state`, `last_detail`, `last_at`, and `pending` (messages still
queued for the next attempt). `last_state: error` with a non-zero `pending`
means turns are being kept locally and retried after every turn -- name the
detail and the fix (login, network, missing actor). No file at all while
sync is ON means no turn has finished since it was enabled.
