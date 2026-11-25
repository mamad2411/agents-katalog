---
name: woostack-review
description: Managed agentic PR reviews with parallel matrix execution and skeptical validation.
install: pnpx skills add howarewoo/woostack
requires:
  bins: [gh, jq, node]
recommends:
  skills: [pbakaus/impeccable, coreyhaines31/seo-audit, coreyhaines31/ai-seo, openai/security-best-practices, supabase/supabase-postgres-best-practices]
---

# woostack-review

Spawn a parallel swarm of review sub-agents against a pull request (or the local diff), validate their findings with a Skeptical Validator, and — when a PR is targeted — post a single batched GitHub Review.

This skill is **host-agnostic**: it works in any AI coding agent that supports sub-agent / task spawning (Claude Code, Cursor, Gemini CLI, opencode, etc.). Hosts without parallel sub-agents fall back to a sequential loop.

## Commands

- `/woostack-review` — Auto-detect: if the current branch has an open PR (via `gh pr view --json number`), behave as `/woostack-review <PR#>`. Otherwise review the local diff (no GitHub posting).
- `/woostack-review <PR#>` — Fetch the PR via `gh`, run the swarm, and post a native batched GitHub Review.
- `/woostack-review --fast`, `/woostack-review fast` — One-run fast-tier override for the whole review (`FORCE_TIER = fast`).
- `/woostack-review --deep`, `/woostack-review deep` — One-run deep-tier override for the whole review (`FORCE_TIER = deep`).
- `/woostack-review --full` (or `@review --full` in a PR comment) — Force a complete re-review even when a prior SHA marker exists. Skips the incremental path described below.
- `woostack-review install` — Verify local deps (`gh`, `jq`, `node`) and pre-fetch `impeccable` + `react-doctor` (run once per repo).
- `woostack-review status` — Show the current PR's review status.

### PR-comment triggers (issue #19)

When the companion GitHub Action is installed, the following comment commands re-trigger the review without leaving the PR:

| Comment | Effect |
|---|---|
| `/woostack-review` | Full re-review (sets `incremental=off`). Equivalent to `@review --full`. |
| `/woostack-review recheck` | Incremental review of new commits since the last marker. Same path as a `synchronize` event. |
| `/woostack-review force` | Bypass auto-skip (see *Auto-skip* below). Combinable: `/woostack-review force recheck`. |
| `/woostack-review --fast` / `/woostack-review fast` | Force a one-run fast-tier execution for this run. |
| `/woostack-review --deep` / `/woostack-review deep` | Force a one-run deep-tier execution for this run. |

The legacy `@review` trigger phrase still works; `/woostack-review` is an alias the example workflow's `issue_comment` `if:` recognizes.

### Auto-skip (bot PRs + release rollups)

`prefetch.sh` short-circuits the review with a single one-line PR comment when either condition holds (before fetching the diff, so token cost is ~zero):

- **PR author matches `authors_skip`.** Default list: `dependabot[bot]`, `renovate[bot]`, `github-actions[bot]`. Override with `review.authors_skip` in `.woostack/config.json`; explicit `"review": { "authors_skip": [] }` opts out entirely.
- **PR title matches `release_rollup_pattern`** (Python regex). Default: `^(staging|release|chore\(release\))`. Override with any string; explicit empty string opts out.

The skip comment carries a `<!-- woostack-review:skipped -->` marker; subsequent triggers on the same PR detect the marker and re-skip silently (no comment spam). To force a full review of a skipped PR, post `/woostack-review force`.

## Incremental Mode

By default (`incremental: auto` on the GitHub Action), every posted review carries a hidden watermark:

```
<!-- woostack-review:sha=<headRefOid> -->
```

On the next run, `prefetch.sh` scans **bot-authored** prior review bodies (the same `BOT_NAME_PATTERN` used elsewhere) for the marker — non-bot reviewers cannot forge a marker to narrow the window. If found, prefetch diffs `<last_sha>...HEAD` via the GitHub compare API instead of the full PR diff — only the new commits since the last pass are reviewed. Unresolved prior review threads (any author) are dumped to `$OUTDIR/prior-findings.json` and consumed by the posting stage as an **event floor**: any non-empty priors list keeps the new review at minimum `REQUEST_CHANGES`, a conservative gate so a stale open thread is never auto-resolved by a clean incremental pass.

Override paths:
- Action input `incremental: off` (workflow-level opt-out).
- A trigger comment containing `--full` (e.g. `@review --full`) — fixed-string match, regex-injection safe.
- Force-push that drops `<last_sha>` from the branch history — the compare API returns 404; prefetch emits a `::warning::` and falls back to the full diff for that run.

When the incremental diff has no new commits (i.e. `LAST_SHA == HEAD_SHA`, e.g. someone re-triggers without pushing), prefetch emits `skip=true` with reason `no new commits since last review (<last_sha>)`. To force a re-review of the same SHA, pass `--full` (or set `incremental: off`).

Marker semantics are state-light: the marker IS the state. There is no DB or workflow artifact retention beyond what GitHub already keeps in review history.

## Cross-PR Memory (`.woostack/memory/` + `.woostack/memory.md`)

Reviews stay useful across PRs through the consumer repo's woostack memory store. The preferred write target is the scope-routed **`.woostack/memory/`** directory: one Markdown note per reusable fact, with frontmatter declaring the scope where it applies. The flat **`.woostack/memory.md`** remains the global shard and fallback for repos that have not initialized the scoped store.

When a `.woostack/memory/` scope-routed store exists, `prefetch.sh` composes the per-PR memory context via `recall.sh` ([memory contract](../woostack-init/references/memory.md)) — scope-matched notes, one-hop `[[linked]]` notes, and the global shard — instead of dumping the whole file; the flat `.woostack/memory.md` always serves as the global shard regardless.

### How it's used

- **Read as context.** `prefetch.sh` writes the per-PR memory into `$OUTDIR/memory.md`. When `recall.sh` is available (the `woostack-init` skill is co-installed) it composes that file via recall — scope-matched notes + one-hop links + the global shard (see the paragraph above); otherwise it falls back to a flat copy of `.woostack/memory.md` (100KB cap). Either way, every angle worker and both validator passes treat the result as additional rubric and **drop any finding the memory already records as known/accepted/wontfix**. This is what keeps re-reviews quiet: an issue the team has consciously accepted is not re-flagged on the next PR.
- **Written inline (local).** When you run `/woostack-review` locally and dismiss a finding (or note a gotcha worth remembering), the skill records the **learning** as a scoped note when `.woostack/memory/` exists, or as a flat `.woostack/memory.md` bullet otherwise. It first checks that no existing entry already covers the learning, so memory stays a small deduplicated set of reusable rules rather than a log of every dismissal. The local skill has direct write access — no post-session hook, no permission-isolated job. See Stage 6 below.
- **Curated by humans.** The files are meant to be edited directly. Add or revise a scoped note, delete a stale one, or keep a global bullet in the flat shard when scope is genuinely global.

### Event-floor rule (prior threads)

`prior-findings.json` (unresolved + resolved threads on the *current* PR) is still produced for incremental mode, but it is used for one thing only: **open** prior threads are an event floor — a non-empty set keeps the new review at minimum `REQUEST_CHANGES`. Resolved threads do not gate the event; a clean incremental pass can `APPROVE`.

### Noise control (`severity_floor` + nits)

`severity_floor` **defaults to `high`** and is a **blocking/visibility threshold**, not a drop gate. Findings at/above the floor are normal findings; validated findings **below** the floor are surfaced as non-blocking **nits** (`Nit:` title prefix, `· NIT` footer) rather than dropped. A below-floor finding that is `blocking: true` is never demoted — it surfaces as a normal blocking finding (blocking overrides the floor). Nits are event-neutral: a PR whose only findings are nits still gets `APPROVE`, with the nits posted inline.

The floor is applied in one place — `scripts/intersect-findings.sh` (Stage 4c) — after the adversarial intersection, so swarm, CI, and defender-only paths agree. Widen the floor per-repo with `review.severity_floor` (`"low"` / `"medium"`).

Set **`review.nits: false`** to restore the old behavior: below-floor non-blocking findings are dropped entirely. (Below-floor *blocking* findings still surface — the override is a global safety rule independent of this knob.)

## Knowledge Aggregation

woostack-review wires in domain skills as tool calls inside specific angles, not as a runtime dependency:

| Source | Used by | How |
|---|---|---|
| [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | `design` | `npx -y impeccable detect --json` (run once; feeds both quant + qual passes inside the angle prompt) |
| [millionco/react-doctor](https://github.com/millionco/react-doctor) | `react` | `npx -y react-doctor --diff <base> --offline` |
| [coreyhaines31/seo-audit](https://www.skills.sh/coreyhaines31/marketingskills/seo-audit) framework | `seo` | Embedded as the audit rubric in `prompts/angles/seo.md` |
| [openai/security-best-practices](https://www.skills.sh/openai/skills/security-best-practices) | `security` | Referenced from `prompts/angles/security.md`; fetch `references/<language>-<framework>-<stack>-security.md` via `gh api` |
| [coreyhaines31/ai-seo](https://www.skills.sh/coreyhaines31/marketingskills/ai-seo) | `aeo` | Embedded as the rubric in `prompts/angles/aeo.md`; deeper `references/` (platform-ranking-factors, content-patterns, content-types) fetched on demand via `gh api` |
| [supabase/supabase-postgres-best-practices](https://www.skills.sh/supabase/agent-skills/supabase-postgres-best-practices) | `database` | Referenced from `prompts/angles/database.md`; fetch `references/<family>-<topic>.md` (`security-*`, `query-*`, `schema-*`, `conn-*`, `lock-*`, `data-*`) on demand via `gh api repos/supabase/agent-skills/contents/skills/supabase-postgres-best-practices/references/<file>` |

The audit frameworks themselves are embedded in `prompts/` (inside this skill bundle) so the skill is self-sufficient. Installing the recommended skills only enhances your host agent's general vocabulary.

## Project Rules

Prefetch auto-discovers project rule files (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `.windsurfrules`, `GEMINI.md`) at the repo root, and additionally walks up from each changed file path to collect any `AGENTS.md` / `CLAUDE.md` along the way. The discovered content is concatenated (each section prefixed by a `## SOURCE: <path>` header, 100KB cap) into `$OUTDIR/rules.md` and surfaced to every angle as additional rubric. When that file is present, an extra `conventions` angle fires; the validator drops any finding that claims a rule violation but cannot quote the rule verbatim. Repos without rule files run unchanged.

## Per-repo Configuration (`.woostack/config.json`)

Drop an optional `.woostack/config.json` in the consumer repo to tune the review without forking the skill. **Review settings nest under a top-level `review` object** so the file can hold sibling config namespaces for other woostack tools without collision; keys outside `review` are ignored by the review loader. Prefetch parses the `review` block into `$OUTDIR/config.json` (canonical copy, flattened); downstream stages read from there. Missing file = defaults (`severity_floor: high`). **All keys are optional — specify only the ones you want to override; the rest keep their built-in defaults.** Invalid JSON, a non-object `review`, or an unknown key *inside* `review` → loud `::error file=.woostack/config.json,line=N::<msg>` annotation and the workflow fails (no silent fallback). Sibling top-level keys outside `review` are ignored, not errors.

> **Transition note:** review keys placed at the top level (the pre-nesting layout) are still accepted but emit a deprecation `::warning`. Migrate them under `review`.

Minimal example — override one knob, everything else stays default:

```json
{ "review": { "severity_floor": "medium" } }
```

Full schema (every key shown; all optional):

```json
{
  "review": {
    "angles": {
      "force": ["database"],
      "skip": ["seo"]
    },
    "severity_floor": "high",
    "nits": true,
    "ignore": [
      "**/*.generated.ts",
      "migrations/*.sql"
    ],
    "project_rules": [
      "constitution.md",
      "docs/standards/*.md"
    ],
    "authors_skip": [
      "dependabot[bot]",
      "renovate[bot]"
    ],
    "release_rollup_pattern": "^(staging|release|chore\\(release\\))",
    "models": {
      "fast": "anthropic/claude-haiku-4-5",
      "standard": "openai/gpt-5.4",
      "deep": "anthropic/claude-opus-4-7",
      "openai": {
        "fast": "gpt-5.3-codex-spark",
        "standard": "gpt-5.4",
        "deep": "gpt-5.5"
      },
      "anthropic": {
        "fast": "claude-haiku-4-5",
        "standard": "claude-sonnet-4-6",
        "deep": "claude-opus-4-7"
      }
    },
    "force_tier": "deep",
    "fix_commands": ["pnpm lint:fix", "pnpm format"],
    "disable_adversarial": false,
    "chunking": {
      "max_loc": 4000
    }
  }
}
```

Key reference (JSON has no comments, so the per-key semantics live here):
- **`angles.force`** — always run these, even if not auto-detected. **`angles.skip`** — never run these (`bugs`/`security` cannot be skipped).
- **`severity_floor`** — one of `low` | `medium` | `high`; a blocking/visibility threshold, **not** a drop gate. **Default `high`**. Findings below the floor surface as non-blocking nits (see `nits`); set `low`/`medium` to treat more findings as normal (at/above-floor). Applied once by `intersect-findings.sh` (Stage 4c).
- **`nits`** — `true` | `false`; default **`true`**. When `true`, validated findings below `severity_floor` surface as non-blocking nits instead of being dropped. Set `false` to drop them (the pre-reframe behavior). Below-floor `blocking` findings always surface regardless of this knob.
- **`ignore`** — fnmatch globs; ignored paths skip angle triggers + diff body.
- **`project_rules`** — fnmatch globs appended to auto-discovered `rules.md`.
- **`authors_skip`** — PR author logins that short-circuit the entire review. Defaults: `dependabot[bot]`, `renovate[bot]`, `github-actions[bot]`. Set to `[]` to opt out.
- **`release_rollup_pattern`** — Python regex on the PR title (default shown above; note `\\(` to escape the paren in JSON). Empty string opts out.
- **`force_tier`** — `fast` or `deep`. Single-run override from config. Valid values are the same as `/woostack-review --fast` / `--deep`.
- **`models`** — per-tier slug overrides. Use flat `models.fast` / `.standard` / `.deep` as provider-agnostic fallbacks, or provider-scoped maps such as `models.openai.deep`, `models.anthropic.standard`, `models.google.standard`, and `models.openrouter.fast` when the same repo is reviewed by multiple coding agents. The action input `inputs.model` still wins.
- **`fix_commands`** — reserved for `--loop` mode (issue #15).
- **`disable_adversarial`** — cost-sensitive opt-out for the prosecutor+defender validator (issue #13). When `true`, only the defender pass runs and its output becomes `findings.json` directly.
- **`metrics`**: opt in to per-angle signal/noise metrics (bool, default `false`) — emit `findings.metrics.json` per run and fold a rolling `.woostack/metrics.json` aggregate (local only). Each angle also carries `overlap_total` + `overlap_with` (how often another angle raised the same issue, on the raw pre-validation set — a redundancy signal). Aggregate schema is v2; an older v1 aggregate is reseeded on first fold. See Stage 6.5.
- **`chunking.max_loc`** — diff-chunking threshold (issue #14). When the post-ignore diff exceeds this many changed lines, prefetch splits it into chunks honoring workspace package roots > top-level dirs > file-LOC-balanced groups; each angle fans out as angles × chunks parallel sub-agents. `0` disables chunking; missing => 4000.

**Precedence**: for the angle set, `angles.force` beats `angles.skip` when the same angle is listed in both. For model resolution, precedence is: explicit comment override (`--fast` / `--deep`) → action input `inputs.force_tier` → `review.force_tier` in config → action input `inputs.model` → `models.<provider>.<tier>` → flat `models.<tier>` → table default in `prompts/_header.md`. `ignore` is applied to both file paths and the per-file diff sections before angle gates evaluate.

## `/woostack-review` Workflow

When the user invokes `/woostack-review [PR#]`, the host agent MUST perform the following stages. **All file paths below are relative to `$WOO_REVIEW_ACTION_PATH`**.

### Stage 0 — Resolve skill path

Set `WOO_REVIEW_ACTION_PATH` to the directory containing this `SKILL.md` (the installed skill bundle). All `prompts/` and `scripts/` assets ship inside that directory.

```bash
export WOO_REVIEW_ACTION_PATH="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
# Or however your host exposes the skill's install dir (e.g. $SKILL_DIR).
```

### Stage 1 — Prefetch

Build the same `$OUTDIR/` artifact tree the GitHub Action builds.

> **Atomic state.** `prefetch.sh` wipes `$OUTDIR` (defaults to a per-project `/tmp/pr-review-<hash>` via `scripts/resolve-outdir.sh`) before recreating it. Hosts that invoke individual stages directly (skipping `prefetch.sh`) MUST do the same — stale `findings.<angle>.json` from a prior run will otherwise re-enter the merge step and contaminate the review.
>
> **OUTDIR override.** All scripts (`prefetch.sh`, `load-config.sh`, `detect-angles.sh`, `merge-findings.sh`, `intersect-findings.sh`, `chunk-diff.sh`, `resolve-diff-line.sh`) honor the `OUTDIR` environment variable. Hosts that cannot use `$OUTDIR/` (e.g. sandboxed runtimes with workspace-scoped temp dirs) MUST export `OUTDIR=<their_dir>` to **every** sub-agent. Without that, sub-agents will write findings to a different directory than the merge step reads, silently dropping them.
>
> **Default is per-project.** When `OUTDIR` is unset, scripts derive `/tmp/pr-review-<hash>` from the repo's git toplevel (via `scripts/resolve-outdir.sh`), so different repos on one machine isolate automatically. The orchestrator resolves it once and exports it to every sub-agent; `prefetch.sh` also prints `outdir=<path>`. Two concurrent runs of the *same* repo still share one dir — set `OUTDIR` explicitly to isolate those.

**If a PR number was supplied** — export it and invoke `prefetch.sh` directly. The script handles diff fetch, meta fetch, project-rule discovery, auto-skip checks, and prior-findings extraction. Hosts whose tool gating blocks caller-side `$(...)` substitution (notably Gemini CLI) MUST use this path — `prefetch.sh` self-resolves the PR number from the current branch when none is exported and `GITHUB_ACTIONS != "true"`, so callers never need their own subshell.

```bash
# Resolve the per-project OUTDIR once and export it so prefetch.sh and every
# sub-agent share one tree. Default: /tmp/pr-review-<hash> derived from the git
# toplevel (scripts/resolve-outdir.sh), so different repos on one machine never
# collide. An explicit OUTDIR (e.g. a sandbox temp dir) is respected as-is.
source "$WOO_REVIEW_ACTION_PATH/scripts/resolve-outdir.sh"   # sets + exports OUTDIR
export PR_NUMBER=<n>   # optional; prefetch.sh derives it from the branch when unset
bash "$WOO_REVIEW_ACTION_PATH/scripts/prefetch.sh"   # prints outdir=<path>; honors the exported OUTDIR
```

When prefetch resolves a PR number AND finds an open PR, it produces the full artifact tree (`diff.txt`, `meta.json`, `last_sha.txt`, `prior-findings.json`, `rules.md` when applicable, `memory.md` when the consumer repo has `.woostack/memory/` and/or `.woostack/memory.md`). When no PR resolves, it emits `skip=true` — the host then falls back to local-diff mode below.

**Artifact reference.** All paths are under `$OUTDIR` (default per-project `/tmp/pr-review-<hash>/`):

| Artifact | Written by | Consumed by | Notes |
|---|---|---|---|
| `diff.txt` | `prefetch.sh` | angle workers, `merge-findings.sh` | Full or incremental diff |
| `meta.json` | `prefetch.sh` | all stages | PR metadata (title, files, SHA, author) |
| `last_sha.txt` | `prefetch.sh` | Stage 5 watermark | Present only when a prior watermark was found |
| `prior-findings.json` | `prefetch.sh` | event-floor gate | Unresolved + resolved prior review threads |
| `rules.md` | `prefetch.sh` | `conventions` angle, validator | Concatenated project rule files; triggers `conventions` angle when present |
| `memory.md` | `prefetch.sh` | all angles, validator | Cross-PR memory composed from `.woostack/memory/` and/or `.woostack/memory.md`; findings it records as known/accepted are dropped. Present only when the consumer repo has memory |
| `angles.txt` | `detect-angles.sh` | Stage 3 orchestrator | One angle name per line |
| `findings.<angle>.json` | angle workers | `merge-findings.sh` | Raw per-angle output |
| `raw_findings.json` | `merge-findings.sh` | validator passes | Merged, chunk-collapsed findings |
| `findings.json` | `intersect-findings.sh` | Stage 5 posting | Final validated set |
| `validator-metrics.json` | `intersect-findings.sh` | observability | `prosecutor_count`, `defender_count`, `kept_count`, `disagreement_count`, `mode`, `degraded` |
| `findings.metrics.json` | `intersect-findings.sh` | metrics fold, telemetry | Per-angle signal/noise breakdown. Emitted **only when `review.metrics: true`** in config. Keyed by angle: `raw_count`, `prosecutor_kept`, `defender_kept`, `kept`, `dropped_by_defender`, `dropped_by_prosecutor`, `blocking_count`, `nit_count`, `nonblocking_count` (= `kept − blocking − nit`), `severity`, `overlap_total`, `overlap_with` (per-other-angle co-occurrence counts on the raw set; schema v3) |

**If no PR number resolved (local mode):**

```bash
source "$WOO_REVIEW_ACTION_PATH/scripts/resolve-outdir.sh"   # per-project default OUTDIR (or honors an explicit override)
rm -rf "$OUTDIR"
mkdir -p "$OUTDIR"
BASE="$(git merge-base HEAD origin/main 2>/dev/null || git merge-base HEAD main)"
git diff "$BASE"...HEAD > "$OUTDIR/diff.txt"
# Synthesize meta.json from git for downstream scripts.
git diff --name-only "$BASE"...HEAD \
  | jq -R . | jq -s '{
      headRefOid: "'"$(git rev-parse HEAD)"'",
      baseRefName: "'"$(git rev-parse --abbrev-ref "$BASE@{upstream}" 2>/dev/null || echo main)"'",
      title: "(local diff)",
      body: "",
      files: [.[] | {path: .}]
    }' > "$OUTDIR/meta.json"
```

### Stage 2 — Detect Angles

```bash
bash "$WOO_REVIEW_ACTION_PATH/scripts/load-config.sh"   # parses .woostack/config.json (defaults severity_floor=high)
bash "$WOO_REVIEW_ACTION_PATH/scripts/detect-angles.sh"
```

Read the result from `$OUTDIR/angles.txt` (one angle per line). Always-on angles: `bugs`, `security`. Conditional (auto-detected from changed paths + diff body): `conventions` (when `rules.md` is present), `seo`, `aeo`, `design`, `react`, `database`, `tests`, `api`, `infra`, `observability`, `types`, `i18n`, `docs`, `deps`, `skills` (when a `SKILL.md` is in the diff), `architecture` (when the diff touches general-purpose source files). See `scripts/detect-angles.sh` for per-angle gating heuristics.

Prefetch also produces optional chunking artifacts when the post-ignore diff exceeds `chunking.max_loc` (default 4000 LOC). When present, the host MUST fan out one sub-agent per `(angle, chunk)` pair in Stage 3:

- `$OUTDIR/chunks.txt` — chunk IDs, one per line (`chunk-0`, `chunk-1`, …).
- `$OUTDIR/chunks.json` — manifest: `[{id, files, loc, diff_path, boundary}]`.
- `$OUTDIR/diff.chunk-<id>.txt` — per-chunk diff (a valid `diff --git` stream).

Boundary precedence: workspace packages (`packages/<name>/`, `apps/<name>/`, `services/<name>/`, `libs/<name>/`) → top-level directories → file-LOC-balanced split. When `chunks.txt` is absent the diff is under threshold and chunking is a no-op.

### Stage 3 — Run Bounded Review Swarm (one per angle, × chunk if chunked)

**This is the local swarm step.** Local hosts MUST use bounded execution by default whenever more than one angle or `(angle, chunk)` pair is detected. The default concurrency limit is `6`, because several local hosts can spawn parallel sub-agents but cap active workers below the detected angle count. Set max concurrency to `1` for the sequential fallback.

Bounded execution means:

1. read the expected work items from `$OUTDIR/angles.txt` and, when chunking is active, `$OUTDIR/chunks.txt`;
2. initialize every expected findings artifact to `[]` before workers start;
3. run at most `N` workers at once;
4. drain the full first-pass queue;
5. retry missing, empty, invalid-JSON, or non-array artifacts once after the queue drains;
6. reset still-invalid artifacts to `[]`;
7. write `$OUTDIR/swarm-metrics.json` so the summary can disclose bounded mode and degraded coverage.

For unchunked reviews, the expected artifact is `$OUTDIR/findings.<angle>.json`. For chunked reviews, the expected artifact is `$OUTDIR/findings.<angle>.<chunk_id>.json`.

Use your host's primitive behind the bounded queue:

- Claude Code: `Task` tool, dispatching at most `N` active angle tasks at once.
- Cursor / Composer: parallel subagent dispatch, capped at `N` active workers.
- Gemini CLI: built-in `@generalist` subagent, capped at `N` active workers (see `prompts/google.md`). Parallel-vs-sequential dispatch of multiple `@<agent>` calls in a single turn is not formally documented today; treat as best-effort parallel — the isolation pattern still buys token economy even if Gemini serializes internally.
- opencode: subagent dispatch via the OpenCode runtime's primitive (see `prompts/opencode.md`), capped at `N`; use `N=1` when the build does not support parallelism.

**Shell helper path.** Shell-capable local hosts can use the shipped bounded queue runner:

```bash
bash "$WOO_REVIEW_ACTION_PATH/scripts/run-bounded-swarm.sh" \
  --max-concurrency "${WOO_REVIEW_MAX_CONCURRENCY:-6}" \
  -- <worker command...>
```

The helper exports `WOO_REVIEW_ANGLE` and, when chunking is active, `WOO_REVIEW_CHUNK` for each worker. It preserves the caller's existing environment, including `OUTDIR`, `WOO_REVIEW_ACTION_PATH`, `FORCE_TIER`, provider/model variables, and review config/input variables. The worker command must write `$OUTDIR/findings.$WOO_REVIEW_ANGLE.json` when unchunked, or `$OUTDIR/findings.$WOO_REVIEW_ANGLE.$WOO_REVIEW_CHUNK.json` when chunked.

When a host cannot express sub-agent work as a shell command, implement the same bounded queue natively with the host's task/sub-agent API.

Each sub-agent receives the same brief:

```
You are the <angle> reviewer for this PR. Read:
- $WOO_REVIEW_ACTION_PATH/prompts/_header.md   (shared contract)
- $WOO_REVIEW_ACTION_PATH/prompts/angles/<angle>.md   (your scope)
- $OUTDIR/diff.txt, $OUTDIR/meta.json   (OUTDIR is exported by the orchestrator; prefer it over any literal path)

Execute any shell commands the angle prompt specifies (e.g. impeccable detect,
react-doctor). Write your findings as a JSON array to
$OUTDIR/findings.<angle>.json per the schema in _header.md. The file MUST
start with `[` and end with `]` — no preamble, no commentary, no markdown
fences. Before writing each finding's `line` field, validate it via
`bash $WOO_REVIEW_ACTION_PATH/scripts/resolve-diff-line.sh --file <path> --line <N>`
and drop the finding when the helper prints `null` (the line is not anchorable
on the diff's RIGHT side and the GitHub API will reject the comment). EXIT.
```

**Chunked fan-out.** When `$OUTDIR/chunks.txt` exists, spawn one sub-agent per `(angle, chunk_id)` instead of one per angle. Pass the chunk ID in the brief, and tell the sub-agent to read `$OUTDIR/diff.chunk-<id>.txt` and write `$OUTDIR/findings.<angle>.chunk-<id>.json`. The validator pass still runs **once globally** — `merge-findings.sh` collapses any within-angle duplicates across chunks before validation, and the validator handles cross-angle dedup as today.

Sub-agents MUST NOT post comments, edit the PR, touch other angles' files, run `prefetch.sh`, or delete/recreate `$OUTDIR`. `prefetch.sh` is a Stage-1-only operation; re-running it mid-swarm wipes `meta.json` / `prior-findings.json` and corrupts the posting stage (issue #48).

**Model routing (token optimization, host-agnostic).** Each angle prompt and the validator declare a `tier:` in frontmatter — `fast`, `standard`, or `deep`. The host resolves the tier to a concrete model via the table in `prompts/_header.md`. Tier assignments:

| Stage | Tier | Why |
|---|---|---|
| Context+summary subagent | `fast` | Mechanical summarization. |
| `bugs`, `security` workers | `standard` | Reasoning-heavy: correctness + threat model. |
| `architecture` worker | `standard` | Structural-quality / code-judo judgment; high-subjectivity, needs reasoning depth. |
| `design`, `react` workers | `standard` | Heuristic + Rules-of-Hooks judgment after deterministic tools. |
| `database` worker | `standard` | Postgres correctness, RLS reasoning, plan/index judgment. |
| `tests`, `api`, `infra` workers | `standard` | Coverage/contract/IaC reasoning. |
| `skills` worker | `standard` | Skill-authoring judgment against the best-practices guide. |
| `seo`, `aeo` workers | `fast` | Rubric checklists; no novel reasoning. |
| `observability`, `types`, `i18n`, `docs`, `deps` workers | `fast` | Pattern matching + diff-anchored hygiene checks. |
| Skeptical Validator | `deep` | Highest-leverage step — strictest false-positive filter pays for itself. |

Per-provider resolution (full table in `_header.md`):

| Tier | Anthropic | OpenAI | Google | OpenRouter |
|---|---|---|---|---|
| `fast` | `claude-haiku-4-5` | `gpt-5.3-codex-spark` | `gemini-3-5-flash` | `openrouter/deepseek/deepseek-v4-flash` |
| `standard` | `claude-sonnet-4-6` | `gpt-5.4` | `gemini-3-5-flash` | `openrouter/deepseek/deepseek-v4-pro` |
| `deep` | `claude-opus-4-7` | `gpt-5.5` + `reasoning_effort: xhigh` | `gemini-3-5-flash` | `openrouter/deepseek/deepseek-v4-pro` + `reasoning_effort: xhigh` |

- **Google** currently exposes only `gemini-3-5-flash` — tier routing is a no-op on Gemini until a larger 3.5 model ships.
- **OpenAI** GPT-5-family reasoning is a `reasoning_effort` parameter, not a slug suffix. Use `gpt-5.5` for the skeptical validator and complex review passes, `gpt-5.4` for everyday review work, and `gpt-5.3-codex-spark` for fast rubric workers and ultra-fast real-time coding checks. Use `gpt-5.4-mini` only as the non-Spark cost-sensitive fallback when Spark is unavailable. There is no `gpt-5-pro`.
- **OpenRouter** exposes only `deepseek/deepseek-v4-flash` and `deepseek/deepseek-v4-pro`; reasoning is the `reasoning_effort` parameter (`high`/`xhigh`). Do not route to `deepseek-r1` — V4 supersedes it.

**Host capability:**

- **Per-call routing** (Claude Code `Task`, opencode `@subagent`): honor each prompt's `tier:` verbatim. Maximum savings.
- **Single model per session** (Codex Action, Gemini CLI): pin the run to a resolved run-tier (`fast` or `deep` via `FORCE_TIER`, otherwise `standard`). `tier:` becomes informational once the run tier resolves. Split into multiple jobs if you want per-angle fast/deep split behavior.

Bounded runners MUST preserve the resolved tier/model context for every queued worker. In single-model hosts, pass the resolved run-tier (`FORCE_TIER` when set, otherwise the host's standard tier) to every worker. In per-call-routing hosts, apply each angle prompt's `tier:` while still preserving any explicit `FORCE_TIER` override. Bounded scheduling must not cause later queued angles to fall back to default model settings.

### Stage 4 — Merge + Adversarial Validation

After every sub-agent has finished:

```bash
bash "$WOO_REVIEW_ACTION_PATH/scripts/merge-findings.sh"
# Produces $OUTDIR/raw_findings.json
```

Validation runs as an **adversarial pipeline** (issue #13): two opposing-bias `deep`-tier validator passes followed by a deterministic intersection. The intersection (findings BOTH passes agree to keep) is what authors see — this trades 2× validator cost for materially higher signal-to-noise.

Read `disable_adversarial` from `$OUTDIR/config.json`:

```bash
DISABLE_ADV="$(jq -r '.disable_adversarial // false' $OUTDIR/config.json 2>/dev/null || echo false)"
```

**Stage 4a — Prosecutor pass** (skip if `DISABLE_ADV == true`):

Run `prompts/validator-prosecutor.md`. Bias: assume each finding is real; drop only the clearly wrong. Writes `$OUTDIR/findings.prosecutor.json` and exits.

**Stage 4b — Defender pass** (`prompts/validator.md`):

1. Dedupe across angles (keep the most actionable description; preserve the winner's `title` / `description` / `fix`).
2. Defense-attorney audit: try to prove each finding wrong. Drop pedantic / style-only / lint-catchable / "maybe" findings.
3. Severity check: you MAY downgrade (HIGH → MEDIUM, blocking true → false). You MAY NOT upgrade.
4. Comment-shape check: every surviving finding has `title` (bold headline ≤60 chars), `description` (issue only, no fix), and `fix` (recommended change in prose). Split overloaded `description` fields when an angle collapsed them.
5. `fix_type` enforcement: every surviving finding MUST carry `fix_type` (`"suggestion"` or `"prose"`). Downgrade any `fix_type: "suggestion"` that violates the ≤10-line / single-file / self-contained / no-placeholder / no-fence-break rules — set `fix_type: "prose"` and `suggestion: null`. Full rule list lives in `prompts/validator.md` step 7.
6. Writes `$OUTDIR/findings.defender.json`.

> **Swarm workers stop here.** In the chat-host swarm the defender writes `findings.defender.json` and EXITs — the orchestrator owns Stage 4c (intersect) and Stage 5 (post). Leave `WOO_REVIEW_SEQUENTIAL_VALIDATE` unset when running as a swarm worker — the GitHub Action's `validate` mode sets it because there one sequential agent owns the whole tail; a swarm host has separate orchestrator and worker roles, so the worker must not see it. Pointing a swarm defender at `validator.md` with the flag unset is the safe default — its Step 3/3b/4 gate keeps it from racing the prosecutor, posting prematurely, or mutating `$OUTDIR`.

**Stage 4c — Intersect**:

```bash
bash "$WOO_REVIEW_ACTION_PATH/scripts/intersect-findings.sh"
```

**Verify + retry (mirror the Stage 3 angle-retry guard).** Before intersect, run this **detection** check; it only reports — you (the orchestrator) perform the re-launch described after it:

```bash
for f in findings.prosecutor.json findings.defender.json; do
  if ! jq -e 'type == "array"' "$OUTDIR/$f" >/dev/null 2>&1; then
    echo "missing/non-array: $f — orchestrator must re-launch this pass once (see below)"
  fi
done
```

Re-launch a missing pass exactly **once** (prosecutor → `validator-prosecutor.md`; defender → `validator.md`), then re-run intersect. If a pass is still missing after the retry, intersect proceeds defender-only and sets `degraded: true` in `validator-metrics.json`.

**Surface degradation.** After intersect, read `validator-metrics.json`:

```bash
jq -r '.degraded // false' $OUTDIR/validator-metrics.json
```

If `true`, tell the user in your orchestrator summary that the review is defender-only / lower-confidence — the posting stage also appends a ⚠️ line to the review body (`_header.md`). A `disable_adversarial: true` opt-out reports `degraded: false` and needs no warning.

Produces `$OUTDIR/findings.json` — the final validated set — and `$OUTDIR/validator-metrics.json` with `prosecutor_count`, `defender_count`, `kept_count`, `disagreement_count`. Intersection is a three-pass match: exact `(file, line, title-stem)`, then a fuzzy pass (`±10` lines, prefix-20 title-stem), then a location-only pass (`±10` lines, no title constraint, ambiguous ties skipped) so the same issue under different titles in the two inputs still intersects. When `disable_adversarial: true` is set or `findings.prosecutor.json` is absent, the script copies defender output verbatim and tags metrics `mode: defender-only`. Severity = `min(prosecutor, defender)`, blocking = `prosecutor.blocking AND defender.blocking`, other fields take the defender's copy.

### Stage 5 — Report

**If invoked with a PR number** — post a single native batched GitHub Review per the procedure in `prompts/_header.md`:

- Build the STATUS_LINE (`APPROVED` / `APPROVED WITH SUGGESTIONS` / `CHANGES REQUESTED`).
- Submit one `gh api repos/<repo>/pulls/<PR>/reviews` POST containing all inline comments + the summary + status line. The review `event` (`APPROVE` / `COMMENT` / `REQUEST_CHANGES`) is the native gate: any blocking finding (or open prior thread) triggers `REQUEST_CHANGES`; a non-nit non-blocking finding triggers `COMMENT`; nits are event-neutral, so a PR whose only findings are nits gets `APPROVE` with the nits posted inline.
- DO NOT modify the PR title or body. DO NOT mutate PR labels.

**If invoked locally (no PR#)** — print the validated findings to the terminal grouped by severity, then stop. If `$OUTDIR/swarm-metrics.json` exists, include a one-line swarm summary. Mention bounded mode and `max_concurrency`. If `.degraded == true`, name the `still_invalid` angles or `(angle, chunk)` items and state that those artifacts contributed `[]` after one retry. Do not touch any remote.

### Stage 6 — Update cross-PR memory (local hosts)

After reporting, when the user **dismisses** a finding as a known/intentional/accepted issue, or tells you a gotcha worth remembering, record the **learning** — not the individual issue resolution. The goal is a small, deduplicated set of generalizable rules ("the team accepts X pattern because Y"), not a growing log of every finding ever dismissed.

Before writing anything:

1. **Read the existing memory** (`$OUTDIR/memory.md`, live `.woostack/memory.md`, and `.woostack/memory/MEMORY.md` when present).
2. **Check coverage.** If an existing entry already captures this learning — even phrased differently, or scoped more narrowly/broadly — do **NOT** append a duplicate. If the existing entry is close but the new dismissal generalizes it (e.g. the same pattern in a second file), edit that entry to widen its scope rather than adding a near-duplicate.
3. **Only when the learning is genuinely new**, record one terse reusable rule — one line, `<pattern>: <reason>`, ideally ≤100 chars, no preamble or narration. Prefer a scoped `.woostack/memory/` note when the scoped store exists; fall back to a flat `.woostack/memory.md` bullet only when it does not.

```bash
# Record ONLY after confirming no existing entry covers this learning.
LEARNING="<general pattern>: <why it is accepted / what not to re-flag>" \
MEMORY_SCOPE="<narrow glob or comma-separated globs>" \
  bash "$WOO_REVIEW_ACTION_PATH/scripts/memory-record.sh"
```

Phrase entries as terse patterns, not instances — prefer "Generated `*.pb.go` files are intentional; do not flag their style" over "dismissed line 42 in user.pb.go". One line per entry, no narration. The local skill writes this memory directly — no post-session hook, no permission-isolated job. Only record on an explicit dismissal or a stated gotcha — never auto-record every finding. Do NOT write memory in CI: the GitHub Action's validator job holds `contents: read` and posts the review only; memory is curated locally and by humans editing the files. Memory is read back as review context on the next run (Stage 1) and the validator drops findings it records.

### Stage 6.5 — Fold per-angle metrics (local hosts, opt-in)

Only when the consumer repo sets `review.metrics: true` in `.woostack/config.json`. The
per-run `findings.metrics.json` (written by `intersect-findings.sh`) is folded into a
rolling, **per-clone** aggregate at `.woostack/metrics.json`. The fold script also
ensures that path is gitignored — the aggregate is local data, never committed
(cross-host aggregation is the job of the opt-in central sink, a separate feature).

```bash
bash "$WOO_REVIEW_ACTION_PATH/scripts/metrics-fold.sh"
```

This is a no-op when `metrics` is off or no per-run record exists. As with memory, the
GitHub Action does **not** fold — its job is `contents: read` + post; metrics persistence
is local only (the action uploads `findings.metrics.json` as a build artifact instead).

**Reading the aggregate.** Rank angles by validator-drop rate (noise candidates first):

```bash
jq -r '.angles | to_entries
  | map({angle: .key,
         raw: .value.raw_total,
         drop_rate: (if .value.raw_total > 0 then .value.dropped_by_defender_total / .value.raw_total else 0 end),
         keep_rate: (if .value.raw_total > 0 then .value.kept_total / .value.raw_total else 0 end)})
  | sort_by(-.drop_rate)[]
  | "\(.angle)\traw=\(.raw)\tdrop=\((.drop_rate*100|floor))%\tkeep=\((.keep_rate*100|floor))%"' \
  .woostack/metrics.json
```

A high `raw` with a high `drop` rate is a noise candidate; a high `keep` rate is a useful angle.

## Architecture

```
detect ─► fan-out (parallel sub-agents, one per angle) ─► merge ─► skeptical validator ─► post
```

This mirrors the cloud GitHub Action exactly — the first-party composite action `action.yml` and the reusable workflow `.github/workflows/reusable-review.yml`, both shipped from this repo — just with sub-agents standing in for GHA matrix jobs.

## Companion GitHub Action

For a fully-managed CI flow, drop this into the consumer repo at `.github/workflows/ai-review.yml`:

```yaml
name: AI PR Review
on:
  pull_request:
    types: [opened, reopened, ready_for_review]
  issue_comment:
    types: [created]

jobs:
  review:
    # Authorization gate. issue_comment fires in the base-repo context where
    # secrets are live, for ANY commenter — so restrict comment-triggered runs
    # to trusted actors. Without this, a fork contributor's comment can spend
    # your token (the GitHub "pwn-requests" pattern).
    if: >-
      github.event_name == 'pull_request' ||
      (github.event_name == 'issue_comment' &&
       github.event.issue.pull_request != null &&
       contains(fromJSON('["OWNER","MEMBER","COLLABORATOR"]'), github.event.comment.author_association))
    uses: howarewoo/woostack/.github/workflows/reusable-review.yml@main
    with:
      provider: anthropic
    secrets:
      anthropic_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
```

The `if:` gate restricts comment-triggered runs to the repo owner / members / collaborators — the `issue_comment` trigger runs in the base-repo context with secrets available to *any* commenter, so dropping it lets a fork contributor's comment spend your token. Pin `@main` to a release tag once one is cut. Zero local setup required in the consumer repo — the action ships its own prompts and scripts (`skills/woostack-review/`) and installs the `react-doctor` / `impeccable` CLIs via `npx` at run time.

## Best Practices

- Always parallelize Stage 3 when the host supports it; the validator pass is calibrated for ~5 angles' worth of input.
- Trust the Skeptical Validator. Disabling it produces noisy reviews.
- Honor angle-prompt tiers (`fast`/`standard`/`deep`) when the host supports per-call model routing. Hosts that run one model per session should pin `gpt-5.5` for maximum validator quality, or `gpt-5.4` when cost matters more than deep validation.
- Pass `disable_angles` to skip optional angles when scope is narrow (e.g. backend-only PR → `disable_angles: "seo,aeo,design,react,i18n"`).
- For a confirmed bug (not a style nit) that the author wants to fix, suggest investigating it with [`woostack-debug`](../woostack-debug/SKILL.md): `/woostack-debug <target>` (gated — it finds the root cause before any fix). Review never dispatches `woostack-debug --auto`: it owns no fix behavior and never auto-addresses findings, so it only points the author at the gated command.

## Troubleshooting

- **Missing artifacts** in cloud mode — verify the `detect` job uploaded `review-artifacts`.
- **Empty validator output** — inspect `$OUTDIR/raw_findings.json`. If empty, no angle wrote findings; check each `findings.<angle>.json`.
- **Sub-agents posting prematurely** — re-read the Stage 3 brief; workers must write JSON only.
- **`gh api ... /reviews` returns HTTP 422 "Line could not be resolved"** — a finding's `line` field did not map to a `+` or context line on the diff's RIGHT side. The merge step now drops these via `resolve-diff-line.sh`, but mismatches outside the helper's reach can still slip through. Re-run with the resolver enabled (it runs by default in `merge-findings.sh`) and inspect `$OUTDIR/diff-line-cache.json` to see which lookups returned `null`.
- **Stale findings from a prior run** — `prefetch.sh` now wipes `$OUTDIR` before recreating it. Hosts that skip `prefetch.sh` MUST `rm -rf "$OUTDIR"` themselves; otherwise files like `findings.bugs.json` from an earlier session leak into the merge step.
- **`detect-angles.sh` crashes outside GitHub Actions** — fixed: the script now emits `angles=` / `chunks_json=` lines to stdout and writes `$OUTDIR/angles.json` + `$OUTDIR/chunks-matrix.json` when `$GITHUB_OUTPUT` is unset. Inspect those files when running locally.
- **Sub-agent writes findings to the wrong path** — caused by host workspace drift (the sub-agent's CWD differs from the orchestrator's). Export `OUTDIR` to every sub-agent — see Stage 1.
- **Adversarial validators dropped a finding both passes agreed on** — the intersection applies a fuzzy second pass (`±10` lines, prefix-20 title-stem match) and a location-only third pass (`±10` lines, no title constraint, ambiguous ties skipped). The third pass covers the case where cross-angle dedupe in `merge-findings.sh` left the same issue under different titles in the two validator inputs. Check `$OUTDIR/validator-metrics.json` for `disagreement_count` and the `intersect-findings:` stderr line for the second-/third-pass match counts.
- **Caller-side `PR_NUMBER="$(gh pr view ...)"` blocked by host sandbox** — some hosts (Gemini CLI, sandboxed runtimes) reject inline `$(...)` substitutions on tool calls. Skip the caller-side resolution: `bash $WOO_REVIEW_ACTION_PATH/scripts/prefetch.sh` derives the PR number itself from the current branch when `PR_NUMBER` is unset and `GITHUB_ACTIONS != "true"`.
- **`prefetch.sh` skipped with "bot already commented and trigger is not explicit" on a local run** — fixed: that re-run guard now only applies inside GitHub Actions (`GITHUB_ACTIONS=true`). Local `/woostack-review` invocations are explicit by definition and no longer trip the gate.
- **GitHub API rejects `REQUEST_CHANGES` / `APPROVE` on a self-authored PR** — fixed in `_header.md`: the payload-builder compares `gh api user --jq .login` against `meta.json .author.login` and downgrades the event to `COMMENT` when they match. The STATUS_LINE in the review body still carries the accurate verdict; a small note is appended explaining the downgrade.
- **Sub-agent died mid-run and left no findings artifact** — bounded Stage 3 initializes expected artifacts to `[]`, retries missing/non-array artifacts once after the first queue drains, then records remaining gaps in `$OUTDIR/swarm-metrics.json`. If `.degraded == true`, that angle contributed `[]` and the local summary must disclose it.
- **`merge-findings.sh` failed on bad JSON escapes from a worker** — the recovery path now tries `json.loads(strict=False)` and a fallback that strips bare control bytes + invalid `\<char>` escapes inside strings. Workers that emit raw tabs/newlines or Windows paths inside `description` fields no longer sink the whole merge. The Output Discipline section of `_header.md` documents the escape rules workers should follow up-front.
- **Large diff under-reviewed / a changed file never got findings** — `prefetch.sh` caps the diff at `WOO_REVIEW_DIFF_CAP_BYTES` (default 300KB). The cap is section-aware (issue #150): it keeps whole `diff --git` sections ranked by review value (sections that add lines first; pure file deletions, lockfiles, and generated files last) until the budget is hit, never splitting a section. When sections are dropped it emits a `::warning::` and lists the dropped paths in `$OUTDIR/diff-dropped.txt`. If a real file was dropped, raise the cap (`WOO_REVIEW_DIFF_CAP_BYTES=600000`) or narrow scope with `review.ignore` so low-value paths are excluded before the cap applies.
