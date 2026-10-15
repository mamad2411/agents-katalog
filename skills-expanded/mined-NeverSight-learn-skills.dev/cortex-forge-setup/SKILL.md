---
name: cortex-forge-setup
behavior: ["configure"]
description: Register or deregister the current vault in Cortex Forge and verify global skills are installed. Run from inside a vault directory.
argument-hint: "Optional sub-task: embeddings | skills | sync | vaults"
---

Setup for Cortex Forge. Run from inside a vault directory (one containing `wiki/`, `AGENTS.md`, and `.git/`). Registers the vault in the global config. Cortex Forge does not rely on agent lifecycle hooks (SessionStart/PreCompact/SessionEnd/PreToolUse) — support for those is too uneven across agents. All memory operations (loading `.cortex/MEMORY.md`, crystallizing, recalling) are invoked manually via skills (`/cortex-crystallize`, `/cortex-recall`) so behavior is identical everywhere. This skill does not install skill files itself — [skills.sh](https://www.skills.sh/) (`npx skills add`) is the sole installer, for every agent it supports, not a hardcoded pair.

## Available scripts

- **`scripts/cortex-index.py`** — Builds/refreshes `.cortex/db/vault.db` when semantic search is enabled (step 6); also copied to `~/.cortex-forge/bin/` for the post-commit reindex hook (step 6c)
- **`scripts/embeddings.py`** — Shared embedding backend, imported by `cortex-index.py`; not invoked directly
- **`scripts/cortex-reindex-post-commit.sh`** — Copied to `~/.cortex-forge/bin/hooks/` and wired into `{vault}/.git/hooks/post-commit` (step 6c)

## Sub-tasks

When an argument is provided, always run step 1 (vault detection) first, then jump directly to the relevant step(s) — skip everything else:

| Argument | Runs |
|---|---|
| `embeddings` | Step 6 — dependency check + tailored offer for semantic search |
| `skills` | Step 4 — verify skills are installed, point to `npx skills add` if not |
| `sync` | Step 3b — sync infrastructure files from upstream repo |
| `vaults` | Steps 2–3a — register/update vault in config |

Always end with the relevant subset of step 9 (confirmation).

## Steps

1. **Detect vault from CWD** — validate that the current directory is a valid vault:
   - Required: `.git/`, `wiki/`, `AGENTS.md`
   - If validation fails, report what's missing and stop.
   - Derive vault name from `basename` of CWD (e.g., `/Users/jp/second-brain` → `second-brain`).

2. **Read existing config** — read `~/.cortex-forge/config.yml` if it exists.
   - Check if the current vault path is already registered.
   - **If not registered** → vault is new. Proceed through steps 3–9 in full, asking each optional step interactively.
   - **If already registered** → vault exists. Skip steps 3–9. Instead show a menu (step 2b) and execute only what the user selects.

2b. **Maintenance menu (existing vault only)** — present a numbered list of available operations. The user can select one or more numbers (comma-separated), or "all":

   ```
   Vault "{name}" is already registered. What would you like to do?

     1. Check skills        — verify all 6 are installed; points to `npx skills add` if not (that's the only installer now)
     2. Sync from upstream  — pull updated templates and bin scripts from the upstream repo
     3. Initialize semantic search — build .cortex/vault.db for the first time (checks what's available, then offers accordingly)
     4. Add post-commit prune    — install the vault-report refresh git hook
     5. Add post-commit reindex  — install the embedding reindex git hook (requires semantic search)
     6. Remove this vault   — deregister from config.yml
     7. Set as default      — make this vault the default
     8. Change locale       — update the vault's locale and re-word AGENTS.md's Vault identity stub accordingly
   ```

   For each selected operation, run the corresponding step in sequence:
   - 1 → step 4
   - 2 → step 3b
   - 3 → step 6 (same tailored dependency-check-then-offer procedure as the new-vault wizard). Skip indexing if `.cortex/db/vault.db` already exists (ask user if they want to re-index instead).
   - 4 → step 6b
   - 5 → step 6c (gate still applies: if vault.db doesn't exist, offer option 3 first)
   - 6 → remove vault from `vaults:`, update default if needed, save config, stop
   - 7 → step 9
   - 8 → steps 3 and 3a (re-run the locale prompt and config write; skip step 8's AGENTS.md stub re-wording if the `## Vault identity` section already has user-written content beyond the stub — ask before overwriting anything the user has since filled in)

   After all selected operations complete, show confirmation (step 10) for only the operations that ran.

3. **Set vault locale (new vault only)** — detect the language of the current conversation and propose it as the default, asking for confirmation:

   ```
   Detected you're writing in {detected-language}. Set this vault's locale to "{code}"?

   This determines the language cortex-assimilate, cortex-crystallize, and
   cortex-imprint use when writing new content to the vault (wiki pages,
   session snapshots, permanent knowledge pages).

     1. {code} (detected — matches this conversation)
     2. en
     3. Other (type an ISO 639-1 code)
   ```

   Use the chosen code (ISO 639-1, e.g. `en`, `es`, `pt`) in steps 3a and 8 below.

3a. **Write config** — add the vault entry in `~/.cortex-forge/config.yml` (new vault only):

   ```yaml
   vaults:
     {name}:
       path: {absolute-path}
       locale: {code}
     # ... other registered vaults preserved as-is
   default: {name}   # set as default only if this is the first vault, or if it was already default
   ```
   - Create `~/.cortex-forge/` if it doesn't exist.
   - Preserve all existing vault entries — never overwrite other vaults.
   - If this is the first vault registered, set it as `default`.
   - If a `default` already exists, leave it unchanged.

3b. **Sync infrastructure from upstream** — pull infrastructure files from the upstream repo and apply them to the current vault.

   **Resolve upstream:**
   - Read `upstream:` from `~/.cortex-forge/config.yml`. Default if absent: `itsmistermoon/cortex-forge`.
   - Format: `{owner}/{repo}` (no protocol, no `.git`).
   - Branch/ref: `main` unless `upstream_ref:` is set in config.

   **Fetch file tree** — one API call:
   ```
   GET https://api.github.com/repos/{upstream}/git/trees/main?recursive=1
   ```
   Extract all `blob` entries whose `path` matches the sync scope (see below). This avoids per-file HEAD requests.

   **Sync scope** — files eligible for update from upstream (confirmation required before any write — see below):
   - `templates/*.md`

   For each file in scope, fetch raw content (`https://raw.githubusercontent.com/{upstream}/main/{path}`) and compare with the local file (if it exists). Files identical to upstream are skipped silently — no report, no confirmation needed for those.

   **Confirm before writing.** Do not overwrite as each diff is found. Collect every file that differs (or is missing locally) into one list first. **Done when:** every file in sync scope has been fetched and compared — zero skipped without a compare.
   - If the list is empty: report "templates up to date" and stop — nothing to confirm.
   - If the list is non-empty: show the full list (path + new vs. modified) and ask once: "Update {N} template(s) from {upstream}? (see list above)" Only after confirmation, write the approved files. If declined, write nothing and report which files were left untouched.

   **Never touch** (hard exclusions — skip even if present in upstream tree):
   - `wiki/` — personal knowledge
   - `.raw/` — primary sources
   - `.cortex/` — session cache and semantic search (gitignored; not synced)
   - `AGENTS.md` — mixed protocol + personal content; compare structure only (see below)

   **Structure-only divergence check** — always run for `AGENTS.md` even though it's excluded from auto-sync. Fetch from upstream, then:

   Extract headings from both upstream and local (`##` and `###` lines). Report:
   - Headings present upstream but missing locally → "sections added upstream — consider adding them"
   - Headings present locally but absent upstream → "local-only sections — safe to keep"
   - Never report body content differences, only structural (heading) changes.
   - Do not overwrite under any circumstance.

   **Deletions** — files that exist locally in sync scope but are absent from the upstream tree:
   - Report them as "present locally, removed upstream" and ask the user whether to delete each one (or list them all and ask once with yes/no).

   **Rate limits** — the GitHub API allows 60 unauthenticated requests/hour. The tree fetch is 1 call; each file download is 1 raw HTTP request (not API). Raw downloads are not rate-limited by the API quota, but are subject to bandwidth limits. If a `GITHUB_TOKEN` env var is set, include it as `Authorization: Bearer {token}` on API calls only.

   **Config fields summary:**
   ```yaml
   upstream: itsmistermoon/cortex-forge   # default; override to point at a fork
   upstream_ref: main                      # optional; branch or tag to sync from
   ```

4. **Verify global skills are installed** — cortex-forge has no installer of its own; the sole distribution channel is [skills.sh](https://www.skills.sh/) (`npx skills add`), which is agent-agnostic by design (installs to whichever of the 40+ agents it recognizes, not a hardcoded pair). Check whether the 6 skills (`cortex-crystallize`, `cortex-forge-setup`, `cortex-recall`, `cortex-assimilate`, `cortex-imprint`, `cortex-prune`) are present under `~/.agents/skills/`.
   - **All present** → this step is done implicitly (running this skill at all means it was already installed by something). Report which skills are present and move on.
   - **Some missing** — do not attempt to install them yourself. Tell the user:
     > Missing skills: {list}. Install them with:
     > ```
     > npx skills add itsmistermoon/cortex-forge --all -g -y
     > ```
     > To limit which agents get symlinks (the default installs to every agent skills.sh recognizes), pass `-a <agent>` instead of `--all` — see the [Supported Agents table](https://github.com/vercel-labs/skills#supported-agents) for the exact flag per agent.
   - Never hand-roll agent-specific symlink logic here — that duplicates what `npx skills add` already does correctly for every agent it supports, not just whichever ones this skill happened to hardcode.

6. **Offer semantic search (new vault only — for an already-registered vault, use maintenance menu option 3 instead)** — check dependencies *before* asking, so the offer itself is tailored to what's actually available. Run the detection procedure in `references/EMBEDDING-SETUP.md` (co-located with this skill), then ask using the tailored wording it returns (ready-to-go confirm, one-step-away confirm, or the full backend menu) — never ask a generic "enable semantic search?" without having checked first. If the user accepts, install anything needed and run `scripts/cortex-index.py` (co-located with this skill) with `{vault}` as its argument; report chunks indexed. If declined or skipped, note in the final summary that semantic search is not active and can be enabled later via `/cortex-forge-setup` (maintenance menu, option 3).

6b. **Post-commit prune (opt-in, separate question)** — ask: "Refresh vault-report.json automatically after each commit? (optional)"
   If yes:
   - **Resolve the `cortex-prune` skill's script:** git hooks run outside any agent session, so they need a fixed absolute path — the same-directory resolution the agent uses when invoking `/cortex-prune` directly doesn't apply here. Locate the `cortex-prune` skill's own directory (typically a sibling of this skill's directory — e.g. `../cortex-prune/scripts/cortex-prune.sh` relative to where this SKILL.md was read from) and copy that file to `~/.cortex-forge/bin/cortex-prune.sh` (create dir if needed; skip copy if already identical). If the file cannot be found anywhere, tell the user the `cortex-prune` skill isn't installed and skip this option.
   - Check `git config core.hooksPath` first — if set (husky-style), install into that directory instead of `.git/hooks/`, or warn and skip.
   - Append the marked block to `{vault}/.git/hooks/post-commit` (create with shebang if missing; never clobber existing content — only add/remove the `>>> cortex-forge prune >>>` … `<<< cortex-forge prune <<<` block) and make it executable:
     ```bash
     # >>> cortex-forge prune >>>
     if [ -f ~/.cortex-forge/bin/cortex-prune.sh ]; then
       (
         bash ~/.cortex-forge/bin/cortex-prune.sh >/dev/null 2>&1 || true
         R="wiki/meta/vault-report.json"
         if [ -f "$R" ] && command -v jq >/dev/null 2>&1; then
           n=$(jq '[.health[] | length] | add' "$R" 2>/dev/null || echo "?")
           echo "$(date '+%F %T') cortex-prune: report refreshed, findings=$n" >> .git/cortex-prune.log
         fi
       ) &
     fi
     # <<< cortex-forge prune <<<
     ```
   - Backgrounded: never delays the commit. Not silent: summary line in `.git/cortex-prune.log`.
   - Uninstall (deregister path): remove only the marked block — a diff against the pre-install file must be empty.

6c. **Post-commit re-index (opt-in, separate question)** — ask: "Re-index vault embeddings automatically after each commit? (recommended if semantic search is enabled)"
   If yes:
   - Check if `.cortex/db/vault.db` exists:
     - **Exists** → proceed normally.
     - **Does not exist** → do NOT skip silently. Run step 6's tailored dependency-check-then-offer procedure now (this happens if the user is reaching this point without having gone through step 6 first — e.g. via maintenance menu option 5 directly). If the user declines there, skip the hook installation and note in the summary that semantic search was not initialized.
   - Check `git config core.hooksPath` first — if set (husky-style), install into that directory instead of `.git/hooks/`, or warn and skip.
   - Copy `scripts/cortex-reindex-post-commit.sh` (co-located with this skill) to `~/.cortex-forge/bin/hooks/` if not already there — same reasoning as 6b: the git hook needs a fixed absolute path outside any agent session, so it can't use "co-located with this skill" resolution.
   - **Copy `scripts/cortex-index.py` and `scripts/embeddings.py`** (both co-located with this skill) to `~/.cortex-forge/bin/` if not already there or if different — same reasoning: the git hook needs to run these from a fixed absolute path, never from inside the vault.
   - Append the marked block to `{vault}/.git/hooks/post-commit` (create with shebang if missing; never clobber existing content — only add/remove the `>>> cortex-forge reindex >>>` … `<<< cortex-forge reindex <<<` block) and make it executable:
     ```bash
     # >>> cortex-forge reindex >>>
     bash ~/.cortex-forge/bin/hooks/cortex-reindex-post-commit.sh
     # <<< cortex-forge reindex <<<
     ```
   - The hook self-gates: exits immediately if `.cortex/db/vault.db` or `~/.cortex-forge/bin/cortex-index.py` don't exist, and only runs when the commit touched `wiki/` files. Runs in the background (`&`) — never delays the commit. Appends a timestamped line to `.git/cortex-reindex.log` (ok or error with exit code).
   - Uninstall (deregister path): remove only the marked block — a diff against the pre-install file must be empty.

6d. **Embedding dependency check** — the procedure step 6 (and its fallback inside 6c) both run. Also triggered if `cortex-index.py` fails with an import error after this check already passed (dependency became unavailable mid-session). See `references/EMBEDDING-SETUP.md` (co-located with this skill) for the full detection-and-offer procedure.

8. **Update AGENTS.md vault identity** — check if `AGENTS.md` contains a `## Vault identity` section.
   - If present: skip silently.
   - If missing: append the stub below to `AGENTS.md` and inform the user (in the vault's own locale, resolved in step 3) that it was added and needs filling out before running `/cortex-assimilate`.
   - **Word the stub in the vault's locale** (from step 3): field labels and the HTML-comment prompts are translated; `<!-- -->` comment syntax and the `**locale**:` value itself (an ISO code, not translated) stay as-is. If `locale` is `en`, use the stub exactly as shown:
     ```markdown
     ## Vault identity

     **locale**: en
     **mission**: <!-- What this vault is for -->
     **domains**: <!-- Comma-separated list of topics in scope -->
     **out of scope**: <!-- Topics to reject at ingestion time -->
     **vocabulary**: <!-- Key terms and preferred names used in this vault -->
     ```
     If `locale` is `es`, translate to:
     ```markdown
     ## Vault identity

     **locale**: es
     **misión**: <!-- Para qué es este vault -->
     **dominios**: <!-- Lista de temas dentro de alcance, separados por coma -->
     **fuera de alcance**: <!-- Temas a rechazar al momento de la ingesta -->
     **vocabulario**: <!-- Términos clave y nombres preferidos usados en este vault -->
     ```
     For any other locale, translate the same five field labels and comment prompts into that language — do not leave them in English.

9. **Set default vault** — if more than one vault is registered:
   - Ask: "Which vault should be the default? ({list of registered names})"
   - Update `default:` in the config with the chosen name.
   - If only one vault is registered, set it as default automatically without asking.

10. **Confirm result**:
   - Registered vaults: list all entries in `vaults:` with their paths and locales, marking the default
   - Skills: all 6 present / missing {list} (with the `npx skills add` command to fix it)
   - Semantic search: active (backend: Ollama/mlx-embeddings/sentence-transformers, N chunks indexed) / not active (declined or skipped — how to enable later)
   - AGENTS.md vault identity: added / already present / skipped
   - Sync (if run): upstream used, files updated (list), files skipped (count), deletions pending user confirmation, AGENTS.md divergence noted if any
   - Next step: fill out vault identity in `AGENTS.md` if just added; invoke `/cortex-crystallize` at the end of any project session

## Memory model (manual, no agent lifecycle hooks)

Cortex Forge does not use SessionStart/PreCompact/SessionEnd/PreToolUse hooks on any agent — support for those events is too uneven across agents to build the suite on top of them. Instead, every agent behaves the same way:

- **Load memory**: the agent reads `.cortex/MEMORY.md` itself (per `AGENTS.md` instructions) at the start of a session, or the user invokes `/cortex-recall`.
- **Save memory**: the user (or the agent, per `AGENTS.md` instructions near the end of a session) invokes `/cortex-crystallize` manually to append a snapshot to `.cortex/MEMORY.md`.

This is deliberately identical across agents — no per-agent hook wiring, no symlink maintenance, no `settings.json`/`hooks.json` merges.

## Rules

- Always run from inside the vault directory — never ask for a path manually
- Do not modify any vault files during setup — read only for validation
- Preserve all existing vault entries when writing config
- Never hand-roll skill installation or agent-specific symlinks — `npx skills add` is the sole installer, for every agent it supports
- Post-commit git hooks (prune, reindex — steps 6b/6c) are the only hooks this skill installs; they are plain git hooks, not agent lifecycle hooks, so they behave identically regardless of which agent is in use
- Always ask for default when there are multiple vaults — never assume
