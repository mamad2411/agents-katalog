---
name: ak-threads-booster
description: "Threads growth operating system for topic selection, drafting, analysis, prediction, review, and tracker refresh based on the user's own post history."
version: "2.0.0"
allowed-tools: Read, Glob, Grep
---

# AK體-基於Threads演算法的優化skill

`ak-threads-booster` remains the internal skill id for routing and installation.

Use this as the single entry point for the AK Threads workflow.

This skill is for creators who want to pick stronger topics, write posts with clearer upside, and improve over time using their own Threads history.

It is not a viral-post guarantee engine. It is a decision system:

- find topic angles with real demand
- avoid obvious repetition and red lines
- draft from the user's own voice and history
- review outcomes and feed the learning back into the tracker

## Intent Routing

Classify the user's request first, then open and follow one primary module unless the task clearly needs a short sequence.

Each sub-skill is located via `Glob **/skills/<name>/SKILL.md` so resolution works regardless of where the plugin is installed. Do not assume an absolute path or environment variable.

- Setup / import / initialize / backfill history -> Glob `**/skills/setup/SKILL.md`
- Refresh tracker / update metrics / scrape own profile -> Glob `**/skills/refresh/SKILL.md`
- Analyze a finished post / inspect / AK-review / optimize / improve / 檢查 / 優化 / 診斷 a post the user has written -> Glob `**/skills/analyze/SKILL.md`
- Draft / write from a topic / 起草 / 寫文 (user has **not** written anything yet; generate from a topic) -> Glob `**/skills/draft/SKILL.md`
- Predict likely 24-hour performance / expectation check -> Glob `**/skills/predict/SKILL.md`
- Review actual post performance / compare against prediction -> Glob `**/skills/review/SKILL.md`
- Mine next topics / topic suggestions / 選題 -> Glob `**/skills/topics/SKILL.md`
- Build brand voice / voice analysis -> Glob `**/skills/voice/SKILL.md`
- Local visual panel / dashboard / data cockpit / open panel -> Glob `**/skills/panel/SKILL.md`
- Check skill updates / update AK-Threads-Booster / install weekly auto-update / 更新 skill / 自動更新 -> Glob `**/skills/update/SKILL.md`
- Optimize the skill itself / compound pass / 優化skill / 自我優化 / 閉環 (turn `threads_skill_learnings.log` misses into rule edits) -> Glob `**/skills/optimize/SKILL.md`

## Routing Rules

1. Do not answer from this file alone when a module exists for the request.
2. Open the matched module and follow its workflow.
3. If the user asks for a combined task, use the smallest valid sequence:
   - first-use account workflow -> setup, then voice if needed
   - write from historical data -> setup or voice first if data is missing, then draft
   - post decision flow -> analyze, then predict if the user asks for a range
   - post-publication learning flow -> review
4. Keep outputs grounded in the user's own tracker whenever available.
5. If `threads_daily_tracker.json` is missing, do not pretend the work is data-backed. Ask for fallback history or use the setup path.
6. **Analyze vs Draft routing discipline.** If the user pastes their own text — no matter whether they say "analyze", "check", "optimize", "improve", "幫我看一下", "幫我優化" — route to `/analyze`. `/analyze` gives pointed diagnosis and preserves the user's format; it does **not** rewrite the post. Route to `/draft` only when the user has no existing text and wants something generated from a topic.
7. **Brand voice scope.** `brand_voice.md` is a composition driver **only** in `/draft`. Every other module treats it as observation-only — for flagging drift, never for rewriting the user's submission toward a voice template.
8. **Proactive update offer.** On first setup, installation help, or any repo/skill maintenance conversation, proactively tell the user AK體 can install an opt-in weekly GitHub update checker. Ask whether they want to enable it. Do not install it by default, and do not interrupt normal content tasks like `/draft` or `/analyze` with this offer unless the user asks about maintenance.

## Working Data

Look in the working directory for:

- `threads_daily_tracker.json` - canonical machine-readable tracker
- `style_guide.md` - produced by `/setup`
- `concept_library.md` - produced by `/setup`
- `brand_voice.md` - produced by `/voice`, referenced by `/draft`
- `posts_by_date.md` - human-readable archive
- `posts_by_topic.md` - human-readable topic index
- `comments.md` - human-readable flat comment log
- `threads_freshness.log` - audit log for `/draft` and `/topics` freshness gates, read by `/review`
- `threads_refresh.log` - audit log for `/refresh` runs, read by `/review`

Low-token runtime also looks for derived compiled memory in `compiled/`:

- `compiled/account_wiki.md`
- `compiled/account_state.md`
- `compiled/personal_signal_memory.md`
- `compiled/next_move_queue.md`
- `compiled/post_feature_index.jsonl`
- `compiled/cluster_wiki.json`
- `compiled/exemplar_bank.md`
- `compiled/recent_window.md`
- `compiled/voice_fingerprint.md`
- `compiled/voice_fingerprint.json`

These files are runtime caches only. `threads_daily_tracker.json` remains the source of truth. If compiled memory is missing, stale, or contradicts the tracker, fall back to the tracker and recommend rebuilding compiled memory.

If legacy Chinese companion filenames already exist, treat them as equivalent companion files instead of forcing a rename.

If only the tracker exists, continue in tracker-only fallback mode when the chosen module allows it. If the tracker is missing, do not pretend the work is data-backed - ask for fallback history or use `/setup`.

## Tools Surface

This main `SKILL.md` declares only the read-only tools it actually uses (`Read, Glob, Grep`). Each sub-skill declares its own `allowed-tools` in its frontmatter; some require more:

- `/draft` adds `Write, WebSearch, WebFetch`
- `/review` adds `Write, Edit`
- `/voice`, `/setup`, `/refresh` each extend the surface as needed
- `/update` uses git through shell commands and may create an opt-in Codex automation when the user explicitly accepts weekly auto-update

When auditing permissions, inspect the union of all sub-skill frontmatters, not just this file.

## Persistent-State Policy

Any sub-skill that writes to `threads_daily_tracker.json`, `style_guide.md`, `concept_library.md`, `brand_voice.md`, or `threads_booster_config.json` must follow `templates/FAILSAFE.md` (backup + atomic rename + keep last 5 backups). Append-only logs (`threads_freshness.log`, `threads_refresh.log`, `threads_skill_learnings.log`) follow the append-only rules in the same file.

Compiled memory files under `compiled/` are rebuilt views, not hand-edited state. Rebuild them with `scripts/build_compiled_memory.py` after tracker-changing runs.

## Shared Knowledge

Red-line (R) and signal (S) definitions live in `knowledge/_shared/red-lines.md` — the single source of truth for both `/analyze` and `/draft`. Do not inline R-lists in sub-skill SKILL.md files.

Next-post direction lives in `knowledge/_shared/next-move-engine.md`. Any "next move" recommendation must pass red-line filtering first, name the S signal it is trying to strengthen, and avoid becoming a formula bank or case-study imitation.

Runtime depth, compiled-memory behavior, and output-mode defaults live in `knowledge/_shared/runtime-budget.md`. In `lite` and `standard`, use `knowledge/cards/*` before full `knowledge/*.md` files.

If `runtime.token_mode` is absent or `"ask"`, ask the user to choose **低 token 版** or **高 token 版** before heavy reading. The question must clearly state the tradeoff: low token is faster and cheaper but less detailed; high token is deeper but slower and more expensive.

Compound loop schema — `threads_skill_learnings.log` — is defined in `knowledge/_shared/compound-log-format.md`. `/review` writes misses to it; `/optimize` reads it, proposes rule changes, and appends `supersedes` entries when the user approves edits. No other sub-skill touches the log.

## Precedence and Conflicts

When guidance conflicts, use this order:

1. This main `SKILL.md` — routing and global discipline
2. Sub-skill `skills/<name>/SKILL.md` — module-specific workflow
3. `knowledge/_shared/*.md` — definitions referenced by multiple sub-skills (red-lines, config, discovery, principles, runtime-budget, compound-log-format)
4. `knowledge/*.md` — deeper knowledge bases (psychology, algorithm, ai-detection, data-confidence, chrome-selectors)
5. `templates/*` — shape templates (tracker, style-guide, concept-library, FAILSAFE)

Rules earlier in this list win. If a sub-skill rule contradicts the main SKILL.md (e.g. routes `/analyze` requests to `/draft`), the main SKILL.md wins and the sub-skill is the drift — fix the sub-skill.

A known cross-sub-skill conflict and its resolution:

- **`brand_voice.md` usage.** `/draft` treats it as a composition driver. Every other sub-skill treats it as observation-only. This is stated here (Routing Rules #7) and re-stated in each sub-skill's Scope section. If those ever disagree, this file wins.
