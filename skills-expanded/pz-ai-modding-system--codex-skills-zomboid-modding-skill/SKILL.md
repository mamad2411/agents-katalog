---
name: zomboid-modding
description: Project Zomboid mod creation and maintenance workflow for local B42.20 mods. Use when Codex is creating, forking, fixing, packaging, installing, linking, or debugging a Project Zomboid mod; working in a Zomboid mods directory; adding or fixing loot distribution, EasyDistro, spawn rates, capsules, packs, or wrapper loot; importing live mods into `~/projects/game-mods/zomboid`; installing project-backed mods into the B42.20 live mods folder as symlinks; updating save/default/preset mod lists; adding Lua/scripts/assets/mod.info/posters; initializing a project mod repo; or troubleshooting mods not appearing in the in-game mod list, especially due to the `42.20/` and lowercase `common/` folder structure on Linux.
---

# Zomboid Modding

Use this skill for Project Zomboid mod work. Prefer the layout already used by nearby mods over generic assumptions.

## First Checks

- Read and apply `b42.20-codex-instructions.md`; B42.20 is the only active and supported build for this workspace.
- Inspect the current folder and nearby mods before creating files: `pwd`, `find . -maxdepth 3 -type f -iname mod.info | sort`, and one or two similar `cjs*` mods.
- Preserve existing user edits and existing mod IDs. Do not rename IDs, folders, or version folders unless the user asks or the current layout is broken.
- For existing third-party or Workshop-backed mods, check the local Workshop copy before importing, forking, or patching locally. Inspect `/media/cjstorrs/windows/Program Files (x86)/Steam/steamapps/workshop/content/108600` and match by `mod.info` `id=`, active version folder, and relevant files to see whether the fix or update already exists upstream.
- If the Workshop copy already contains the needed fix or a newer compatible update, prefer refreshing/replacing the live copy from Workshop over maintaining a local project patch. Do not import or fork a Workshop mod just to fix an issue already fixed upstream.
- When adding CJS-only behavior to an existing third-party or Workshop-backed mod, prefer a separate CJS patch/tweaks mod over overwriting upstream files. Overwrite the upstream/live copy only when a patch cannot safely layer the behavior, when the user explicitly asks, or when replacing stale local files with a verified current Workshop payload.
- For new or forked CJS mods, work in `~/projects/game-mods/zomboid/<modName>` first. Install into the live Zomboid mods folder only after project validation.
- In the B42.20 live mods root, mods must be direct children of `mods/`, not under `Contents/mods/`.
- Project-backed mods live under `~/projects/game-mods/zomboid/<modName>`. Their live installs are symlinks back to those project folders, not copied folders.
- For every new or imported mod project, initialize the project repo and GitHub remote using the GitHub repo setup rules below before editing.
- Before making changes, create an initial baseline commit containing only the copied/imported mod files unless the user explicitly asks not to commit, then push it.

## GitHub Repo Setup And Push Discipline

Use these rules for Project Zomboid mod repos in `~/projects/game-mods/zomboid`.

- Keep the local mod folder name and `mod.info` `id=` stable unless the user explicitly asks to rename them.
- Local repos use `main` as the default branch. If initializing, run `git init -b main`; if a repo already exists without `main`, create `main` from `master` or current `HEAD` before the first push.
- GitHub repo names must start with `pz-` and be lowercase kebab-case from the project folder name, e.g. `cjsQuickZoom` -> `pz-cjs-quick-zoom`. Remove apostrophes, convert `&` to `and`, `+` to `plus`, split camel case and digit/letter boundaries, collapse repeated separators, and do not rename the local mod folder to match the repo.
- For CJS patch/tweaks mods for existing mods, use the CJS patch mod convention below instead of deriving the repo name from the local folder.
- Create or update the GitHub repo under `mrStorrs`. Make clearly new, non-forked CJ-authored mods public only when `mod.info` or project context shows `author=CJ Storrs` and no fork/source-derived wording such as `fork`, `based on`, or `repack`; make forks, imports, third-party mods, Workshop-backed mods, helpers, and ambiguous repos private.
- After the first push of a public repo, protect `main`: set it as the default branch, disallow force pushes and deletions, and enforce protection for admins. Do not require status checks or reviews unless the repo already has that policy.
- Set `origin` to `git@github.com:mrStorrs/<repo>.git`. Push `main`, all local branches, and tags after repo creation.
- After every commit made by this skill, immediately run a normal `git push` for the committed branch. Do not force-push. If the repo has no remote yet, create/configure it with these rules first, then push.
- If GitHub hits a secondary content-creation limit while creating repos, back off and retry the same missing repo set; do not create alternate names.

## CJS Patch Mods For Existing Mods

When CJS needs local fixes or quality-of-life tweaks for an existing third-party or Workshop mod and the upstream mod can remain the source of truth, create a separate patch/tweaks mod instead of editing or importing the upstream payload.

- Prefer a patch/tweaks mod over overwriting the target mod. Overwrite the target only when the behavior cannot safely be layered, when replacing stale local files with a verified current Workshop payload, or when the user explicitly asks for an overwrite.
- Derive `<mod-name>` from the target mod display name, folder name, or stable `id=` by lowercasing, splitting camel case and word boundaries, removing punctuation, converting `&` to `and`, converting `+` to `plus`, and collapsing separators into kebab-case.
- GitHub repo names must be `pz-<mod-name>-cjs-tweaks`, e.g. CleanUI -> `pz-clean-ui-cjs-tweaks`.
- Project folder names and `mod.info` `id=` values should use the same words without `pz-`, converted to lower camelCase, e.g. CleanUI -> `cleanUiCjsTweaks`.
- Set `mod.info` `name=` to `CJS <Target Mod Name> Tweaks`.
- Add `require=\<TargetModId>` in `mod.info`, and enable the patch immediately after the target mod in active load lists.
- Keep patch mods narrow and namespaced. Do not copy upstream files unless overriding a specific Lua, script, asset, or load path is required.
- Make these repos private unless project context proves the patch is clearly CJ-authored, non-forked, and safe to publish.

## Root-Cause Fixes

- Do not build defensively by default. Fix the proven cause instead of adding broad nil guards, `pcall` fallbacks, catch-all skips, silent cleanup, or code that deletes broken state to make an error disappear.
- If an invariant is broken and the bad state should not be possible, surface a clear error or targeted log with enough context to find the source. Do not silently drop items, entities, save records, loot entries, or user data unless the user explicitly approves that behavior.
- Defensive handling is only acceptable when it is an absolute must: untrusted persisted save/modData, sandbox values, client/server command payloads, optional dependencies, real Workshop/API version drift, or a PZ API that is proven nullable. Keep those guards narrow and close to the boundary.
- When a boundary guard is required, preserve data where possible and log the exact malformed value or missing dependency. The guard must not hide the root cause from later debugging.

## Loot Work

- Read and apply `/home/cjstorrs/projects/game-mods/zomboid/.codex/instructions/easy-distributions.md` only when the task modifies an item's loot distribution, such as adding or removing that item from loot tables or changing how often it appears there.
- Do not invoke the guide merely because a mod contains capsules, packs, boxes, wrappers, recipes, contained item definitions, or other spawning code. Installing, packaging, enabling, reviewing, or changing non-loot behavior does not trigger it.
- If that workspace instruction file is missing, continue with this skill and inspect the relevant mod's current loot path before changing code.

## Post-Change Review Gate

- After any code, script, asset-reference, packaging, sandbox, mod-list, or live-install change, read and apply `/home/cjstorrs/projects/game-mods/zomboid/.codex/skills/zomboid-review/SKILL.md` before final closeout.
- Scope the review to the touched mod and changed domains, but do not skip it for small edits. The review must at least cover changed files, active B42 layout, live-install drift when applicable, latest relevant logs when available, syntax/line-ending checks, and any domain probes that match the change.
- If the review finds issues and the user asked for implementation, apply focused fixes, rerun the relevant validation, relink the project-backed live mod if needed, and rerun the affected review checks before finishing.
- If the change cannot be proven outside Project Zomboid, state the exact in-game validation still required after the review gate passes.

## Mod List Updates

When enabling, disabling, adding, or removing mods from a loadout, update all active load points unless the user explicitly narrows the scope:

- Save-specific lists: `/home/cjstorrs/games/Project Zomboid Linux 42.20.0/user-data/Zomboid/Saves/*/*/mods.txt`. Add or remove `mod = \ModId,` entries inside the `mods {}` block.
- Main game/default list: `/home/cjstorrs/games/Project Zomboid Linux 42.20.0/user-data/Zomboid/mods/default.txt`. Keep the same `mod = \ModId,` block format.
- Saved preset list: `/home/cjstorrs/games/Project Zomboid Linux 42.20.0/user-data/Zomboid/Lua/pz_modlist_settings.cfg`. Update the named preset line such as `b42-4:` with `\ModId;` entries.

Rules:

- Use the actual `id=` from the relevant `mod.info`, not the display name or folder name.
- Search for existing entries before editing; do not duplicate an ID.
- Preserve the existing load order. For additions, append near the matching tail of the active list or preset instead of alphabetizing.
- Treat `Lua/saved_builds.txt` as character occupation/trait builds, not a mod load list.
- Treat legacy B41/mod-manager files such as `Lua/saved_modlists.txt`, `Lua/modmanager-mods.txt`, and `Lua/saved_modlists_server.txt` as stale unless the user specifically names them.
- After editing, verify the ID appears exactly once in each intended load point with `rg -n "ModId" ...` or an equivalent count.

## Project-Backed Live Links

Project-backed mods in this workspace are installed into `/home/cjstorrs/games/Project Zomboid Linux 42.20.0/user-data/Zomboid/mods` as symlinks back to `~/projects/game-mods/zomboid/<modName>`. The live symlink name should match the project folder casing exactly.

Do not replace a project-backed live symlink with a copied folder. If a real live folder has a matching project folder, treat it as stale live drift and replace it with a symlink after verifying the match by folder name or `mod.info` id.

Exception: if the user explicitly asks or approves abandoning a project-backed copy because the Workshop version is now the source of truth, remove the project copy and live symlink/folder as requested, install the matching Workshop copy directly into the live mods folder, and verify the live copy against Workshop by file comparison and `mod.info` id.

## Project Mod Link Scripts

Use `~/projects/game-mods/zomboid/link-project-mod.sh <modFolder>` to link one project-backed mod into the live Zomboid mods folder. It creates or replaces the live entry with a symlink back to `~/projects/game-mods/zomboid/<modFolder>` and uses the project folder's exact casing for the live symlink name.

Use `~/projects/game-mods/zomboid/link-zomboid-project-mods.sh` for broad live reconciliation. With no mod argument, it only reconciles project-backed mods that are already present live as folders or symlinks; it does not link every project-only folder. With a positional mod folder or `MOD_NAME=<modFolder>`, it links that single project folder.

When importing an existing live CJS Zomboid mod into the game-mods project:

- Use source `/home/cjstorrs/games/Project Zomboid Linux 42.20.0/user-data/Zomboid/mods` unless the user gives another Zomboid mods path.
- Use destination `~/projects/game-mods/zomboid`.
- Treat only top-level directories matching `cjs*` as mods; do not import files such as `cjs-other-changes.md`.
- Preserve mod files faithfully, but keep project git repositories separate from live mod folders.
- Use a targeted import command for the specific mod; the link scripts are symlink-only and should not be used for live-to-project copying.

When linking one project-backed mod into the live Zomboid mods folder:

- After making changes to a project-backed mod, run the link script before finishing. Do not ask the user. Just do it. We can always roll back from the project git repo.
- Prefer `DRY_RUN=1 ~/projects/game-mods/zomboid/link-project-mod.sh <modFolder>`, then `~/projects/game-mods/zomboid/link-project-mod.sh <modFolder>`; this replaces any stale live copy with a symlink back to the project folder using the project folder's casing.
- If using the lower-level link script directly, set `SOURCE_ROOT=~/projects/game-mods/zomboid`, `DEST_ROOT=/home/cjstorrs/games/Project Zomboid Linux 42.20.0/user-data/Zomboid/mods`, and `MOD_NAME=<modFolder>`.
- Use targeted one-mod links for single mods; do not link every project-only mod into the live folder unless explicitly asked.
- After linking, verify the live mod is a symlink to the project folder: `find /home/cjstorrs/games/Project Zomboid Linux 42.20.0/user-data/Zomboid/mods -maxdepth 1 -type l -name '<modFolder>' -printf '%p -> %l\n'`.
- After validation and live linking, commit the project mod repo before finishing unless the user explicitly asked not to commit. Stage only the files changed for the task, do not include unrelated pre-existing work, then push the commit.

## Forking Existing Mods

When making an upstream mod into a CJS-owned mod:

- Copy it into `~/projects/game-mods/zomboid/cjs<ModName>` first, not directly into the live `Zomboid/mods` folder.
- After copying, initialize the repo and GitHub remote if needed, then make and push a baseline commit before changing names, IDs, assets, or code unless the user explicitly asked for no commits.
- Rename `mod.info` `name=` and `id=` to CJS-owned values. Prefer `id=cjs<ModName>` unless preserving save compatibility is explicitly required.
- Namespace custom perk IDs, sandbox option IDs, Lua globals, module names, item modules, client-command modules, and translation keys to avoid collisions with the upstream mod.
- Note compatibility tradeoffs: changing a perk ID or item module can reset existing save XP/books for that fork.
- Preserve the source version folder casing, but ensure empty required folders are real. Add `.gitkeep` to empty `Common/` or `common/` before installing because empty directories are not tracked by git.

## Build 42.20 Layout

For a new B42.20 CJS mod, create this minimum structure:

```text
modFolder/
├── 42.20/
│   ├── mod.info
│   ├── poster.png
│   └── media/
│       └── lua/
│           └── client|shared|server/
└── common/
```

Rules:

- Always include both `42.20/` and lowercase `common/` for new CJS mods in this workspace, even if `common/` is empty.
- Empty directories are not tracked by git. Put `common/.gitkeep` in an otherwise empty `common/`.
- On native Linux, B42.20 resolves the shared version folder as lowercase `common/`; functional content under uppercase `Common/` is ignored on case-sensitive filesystems. Preserve existing casing only after verifying that it is safe or that the folder has no functional shared content. A direct Workshop copy may receive path-only `Common/` to `common/` normalization while its file bytes remain unchanged.
- Put B42.20-only Lua under `42.20/media/lua/client`, `42.20/media/lua/shared`, or `42.20/media/lua/server` according to behavior.
- Put shared assets/scripts used by multiple versions under `common/media/...` only when there is actual shared content.

## mod.info

For new CJS mods, write `42.20/mod.info` with at least:

```ini
name=CJS Example Name
id=cjsExampleName
description=One concise sentence describing the mod.
poster=poster.png
author=CJ Storrs
```

Guidelines:

- Keep `id` stable and unique. Prefer the folder name for new CJS mods, e.g. `cjsQuickZoom`.
- Ensure every `poster=` path exists relative to the folder containing that `mod.info`.
- Use `versionMin=42.0.0` only when nearby mods or the requested packaging style uses it; many local CJS mods omit it.
- Avoid duplicate `description=` lines unless preserving upstream metadata.

## Lua Placement

- Client-only UI/camera/input/render behavior belongs in `42.20/media/lua/client/`.
- Shared definitions, sandbox option translations, or code loaded by both sides belong in `42.20/media/lua/shared/` or `common/media/lua/shared/`.
- Server/gameplay authority code belongs in `42.20/media/lua/server/`.
- Use existing PZ Lua patterns: `Events.OnGameStart`, `Events.OnTick`, `Events.OnCreatePlayer`, and `getCore()` where appropriate.
- When touching Java internals, first search local mods for existing patterns using `rg "getClassField|getClassFieldVal|Reflection.getField"`. Use reflection cautiously and print one clear `[modId]` warning on failure.

## Performance Checks

For performance-sensitive mods:

- Audit event hooks before editing: `rg -n "Events\\.|OnTick|OnPlayerUpdate|OnClothingUpdated|Every|DoParam|LuaEventManager|ISWearClothing|ISClothingExtraAction" modFolder`.
- Avoid full inventory or worn-item scans in `OnTick`, `OnPlayerUpdate`, or frequently fired clothing events unless cached or debounced.
- Prefer game events such as `Events.OnClothingUpdated` over monkey-patching timed actions. Only patch vanilla methods when there is no stable event, and keep the patch minimal.
- Avoid repeated `getScriptItem():DoParam(...)` mutations at runtime; they mutate script definitions and can be expensive/global. Prefer item setters when available, with cached base values.
- For repeated recalculation, store base values in namespaced `modData` keys and skip work when a player/item signature is unchanged.
- Do not put ephemeral UI or random-session state in per-item `modData` on abundant items that players commonly hold in large counts, such as ripped sheets, fabric strips, or ammunition. Even small tables multiply save, comparison, and inventory-parsing work across every item. Keep that state on the open UI/controller keyed by item identity, and persist it only when gameplay genuinely requires it to survive closing the UI or reloading the save.
- At client/server command boundaries, validate malformed `args` narrowly and namespace command modules to the mod id.

## Discovery Debugging

If a mod is not picked up by Project Zomboid:

- Confirm the folder is a direct child of the B42.20 live mods root.
- Confirm `42.20/mod.info` exists and has `name=`, `id=`, and a valid `poster=`.
- Confirm `42.20/` and lowercase `common/` both exist for new CJS/B42.20 mods.
- Confirm there is no accidental extra nesting such as `modFolder/Contents/mods/modFolder/42.20/mod.info`.
- Confirm the mod folder and `id=` do not collide with another installed mod.
- If a directory must be present but empty, add `.gitkeep` or another harmless tracked placeholder.

## Validation

Before finishing:

- Run `lua5.1 -e "assert(loadfile('path/to/file.lua'))"` when Lua syntax can be checked locally.
- For batches, only compile Lua with `loadfile`; do not execute files outside Project Zomboid because game globals such as `Events`, `Perks`, and `SkillBook` will be absent.
- Run `find modFolder -maxdepth 4 -type f -o -type d | sort` and verify `42.20/` plus lowercase `common/` are present.
- For project-backed live installs, verify the live entry is a direct child symlink under the B42.20 live mods root pointing back to `~/projects/game-mods/zomboid/<modName>`, has the project folder's exact casing, resolves to the versioned `mod.info` selected by B42.20, and has valid poster/icon paths. Require `42.20/mod.info` for new or B42.20-specific CJS payloads; allow a verified generic `42/mod.info` fallback from a compatible upstream mod.
- Run the Post-Change Review Gate for any code, script, asset-reference, packaging, sandbox, mod-list, or live-install change.
- Commit the task changes after the live link or direct Workshop refresh succeeds, then push the committed branch. If unrelated changes are present, leave them unstaged and call them out; if only task changes remain, the project mod repo should be clean.
- Tell the user what still requires in-game validation; most PZ Lua behavior cannot be fully proven outside the game.

## Instruction Maintenance

- If the work reveals a new recurring Project Zomboid problem, compatibility pitfall, validation pattern, or durable fix that future sessions should remember, update the relevant workspace or skill instructions while the context is fresh.
- Keep durable generic guidance in `b42.20-codex-instructions.md`; do not recreate one-off current-state notes unless the user explicitly asks.
- Keep instruction updates concise, evidence-backed, and separate from unrelated refactors or historical cleanup.
