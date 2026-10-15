---
name: rblxsync
description: >-
  Declaratively manage Roblox experience metadata (Universe settings, Game
  Passes, Developer Products, Badges, Places) from a YAML file via the rblxsync
  CLI / GitHub Action. Use when setting up rblxsync in a Roblox project, writing
  or editing rblxsync.yml, syncing/publishing game passes, developer products,
  badges, places or universe settings, wiring the generated Config.luau into
  Luau game code, debugging ROBLOX_API_KEY / ROBLOX_COOKIE errors, or adding
  rblxsync to CI. Triggers on "rblxsync", "rblxsync.yml", "sync game passes",
  "Open Cloud metadata", "publish place", "Config.luau", "rblxsync-lock.yml".
---

# rblxsync

`rblxsync` is a Rust CLI + GitHub Action that **declaratively** manages Roblox
experience metadata via the Open Cloud API. One YAML file (`rblxsync.yml`) is the
source of truth for Universe settings, Game Passes, Developer Products, Badges,
and Places. Running it is idempotent: resources are matched by **name**
(case-insensitive), created if missing, updated (PATCH) if present.

Use this skill to set rblxsync up in a user's Roblox project, author/edit their
config, run syncs safely, and wire the generated `Config.luau` into game code.

## Mental model (read this first)

- **`rblxsync.yml`** = desired state, hand-edited, committed.
- **`rblxsync-lock.yml`** = generated state (resource IDs + icon hashes).
  **Commit it.** Never hand-edit it — it is overwritten on the next sync.
- **`Config.luau`** (only if `output_path` is set) = generated, typed Luau module
  of all resource IDs. Game code `require`s it. Never hand-edit it.
- **Matching is by name (case-insensitive).** This is the one thing most likely
  to bite a user. Renaming a Game Pass / Developer Product / Badge in the YAML
  does **not** rename the existing resource — rblxsync no longer finds a match by
  the new name, so it **creates a brand-new resource and orphans the old one**.
  Example: changing a Developer Product from `"100 coins"` to `"100 coins [SALE]"`
  creates a *second* product; the original keeps existing (and keeps selling).
  - **Why this is bad:** duplicate resources, wasted Robux on duplicate badges,
    and **split/broken analytics & sales history** — each ID accrues its own
    purchase data, so renaming silently fragments the numbers you report on.
  - **Only a pure case change** (`"vip pass"` → `"VIP Pass"`) is treated as an
    update, because matching ignores case. Any other text change = new resource.
  - **To actually rename:** change the display name in Roblox (Creator Hub),
    keep the YAML `name` matching it, or edit the name in `rblxsync-lock.yml`'s
    existing entry so the ID is preserved. Do **not** just edit the YAML name.
  - **Always flag a rename to the user before syncing it**, and prefer
    `--dry-run` to prove no unexpected "create" appears in the diff.

## Golden rules

1. **Never run a mutating sync without previewing first.** Always do
   `rblxsync run --dry-run` and show the user the diff before `rblxsync run`.
2. **Never commit, print, or paste `ROBLOX_API_KEY` or `ROBLOX_COOKIE`.** They
   live in a gitignored `.env` (local) or CI secrets. Treat them like passwords.
3. **The `--config` flag is global and goes BEFORE the subcommand.**
   `rblxsync --config prod.yml run` ✅ — `rblxsync run --config prod.yml` ✗.
4. **Creating a badge costs 100 Robux each.** Confirm with the user before a sync
   that adds new badges.
5. **Never rename a resource by editing only the YAML `name`.** Matching is by
   name, so a rename creates a duplicate and orphans the original (fragmenting its
   sales/analytics — see the Mental model). If a user wants to rename a Game Pass,
   Developer Product, or Badge, warn them first and rename it in Roblox + lock
   state, not just the config. In a `--dry-run` diff, treat an unexpected "create"
   for a resource that already exists as a rename mistake.
6. **Confirm before destructive or paid actions**: new badges (Robux), publishing
   places (goes live), any first real `run`.

## Setup workflow (new project)

Run these steps when adding rblxsync to a codebase that doesn't have it yet.

1. **Confirm install.** Check `rblxsync --version` / `which rblxsync`. If absent,
   install (`cargo install --path .` from source, or a tool-manager pin once
   binaries are published — see `references/cli-and-ci.md`).
2. **Create `.env`** with `ROBLOX_API_KEY=...` and ensure `.env` is gitignored.
   Add `ROBLOX_COOKIE=...` *only* if the config will set universe settings (see
   the cookie gotcha below). Never write real secret values yourself — leave
   placeholders and tell the user to fill them in.
3. **Write a minimal `rblxsync.yml`** — only `universe.id` is required. Start
   small; add sections incrementally. Copy `assets/rblxsync.example.yml` as a
   starting point and trim it to what the user actually needs.
4. **Validate:** `rblxsync validate` (no API key / network needed).
5. **Preview:** `rblxsync --config rblxsync.yml run --dry-run`.
6. **Apply:** `rblxsync run` once the user approves the preview.
7. **Commit** `rblxsync.yml` and `rblxsync-lock.yml` (NOT `.env`). If `output_path`
   is set, commit the generated `Config.luau` too.

## Minimal config

Only `universe.id` is required:

```yaml
universe:
  id: 123456789

game_passes:
  - name: "VIP Pass"
    price: 100
```

For the full field-by-field schema, defaults, and every gotcha, read
`references/config-schema.md`. A complete annotated sample is in
`assets/rblxsync.example.yml`.

## Commands

| Command | What it does |
| --- | --- |
| `rblxsync run [--dry-run]` | Sync universe settings + game passes, products, badges. Default command. Writes `rblxsync-lock.yml` and (if set) `Config.luau`. |
| `rblxsync publish` | Publish `.rbxl` places where `publish: true`. Always publishes (no "save"). Does NOT need the cookie. |
| `rblxsync validate` | Parse + check the YAML (dup names, etc.). No API key, no network. |
| `rblxsync export [-o PATH] [--lua]` | One-way snapshot of live resources to a flat Luau/Lua table. NOT a config you can feed back in, and NOT the same shape as `Config.luau`. |

Full command reference, flags, the GitHub Action, environment variables, and
Open Cloud permission scopes are in `references/cli-and-ci.md`.

## The cookie gotcha (very common error)

`rblxsync run` **hard-fails demanding `ROBLOX_COOKIE`** whenever *any* universe
field is set — including `genre` and `max_players`, which are local-only and
never actually call a cookie API. So a config that sets only `genre` still
requires the cookie even though no cookie request is made.

If a user hits "ROBLOX_COOKIE is not set" and doesn't want to provide a cookie,
the fix is to **remove all `universe.*` fields except `id`** from the config (move
name/description/etc. tracking elsewhere). Universe *settings* updates use
`.ROBLOSECURITY` cookie auth against `develop.roblox.com` — an API key alone
cannot update them. See `references/cli-and-ci.md` for how to obtain the cookie
safely.

## Fields that don't sync (surface these, don't silently rely on them)

- **`genre`** and **`max_players`** — tracked in lock/`Config.luau` but **never
  pushed to Roblox** (`max_players` is a per-place setting).
- **Developer Product `is_active`** — parsed but **not** synced; has no effect.
- **Game Pass `is_for_sale`** — this one *is* synced.

Do not type game code against a Developer Product `IsActive` field — the generated
`DeveloperProduct` type has no such field (`{ Id, Name, Description, Price }`).

## Integrating with game code

If the user wants resource IDs available in Luau, set `output_path` (e.g.
`src/shared/Config.luau` or a Rojo-mapped path) and `require` the generated module:

```lua
local Config = require(game.ReplicatedStorage.Shared.Config)
local vipId = Config.GamePasses[1].Id
print(Config.Universe.Name)
```

Wiring it cleanly (lookup by name, Rojo paths, regenerate-on-sync, lock-file
commits) is covered in `references/integration.md` — read it before editing a
user's existing Luau to consume rblxsync output.

## Adding to CI

A ready-to-use workflow template is in `assets/github-workflow-sync.yml`. Copy it
to `.github/workflows/`, set repo secrets (`ROBLOX_API_KEY`, optionally
`ROBLOX_COOKIE`), and pin the action to a published ref (e.g. `@v0.1.0`). The CI
gotchas (the `args` input word-splits and cannot contain spaces; only published
tags exist) are in `references/cli-and-ci.md`.

## When unsure

- Schema / field semantics / defaults → `references/config-schema.md`
- CLI flags, Action inputs, env vars, permission scopes → `references/cli-and-ci.md`
- Consuming output in Luau, lock-file handling, idempotency → `references/integration.md`
- Authoritative upstream docs: the project's `README.md` and `docs/API.md`.
