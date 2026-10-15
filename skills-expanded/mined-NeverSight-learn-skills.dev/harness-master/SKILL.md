---
name: harness-master
description: >-
  Audit harness configs, discover gaps, usage signals, apply approved fixes. Use when tuning
  Claude, Codex, Copilot, Cursor, Gemini, Grok, OpenCode, or Cherry. NOT agents, MCP, or app telemetry.
argument-hint: "[discover|audit|usage|apply|install|resume|list] [harness|all] [project|global|both]"
model: opus
license: MIT
compatibility: >-
  Dry-run audit first. Web access recommended. Python 3.12+ for discovery scripts.
metadata:
  author: wyattowalsh
  version: "1.1.0"
---
# Harness Master

Audit AI harness configuration quality, usage posture, and ecosystem options, then apply approved config fixes in the same session.

**NOT for:** creating agents (agent-conventions), building MCP servers (mcp-creator), generic application telemetry (observability-advisor), or generic code review without harness/config focus (review).

**Input:** harness names, level, or natural language. Modes: **Audit**, **Discover** (gap + bounded research), **Usage**, **Apply/Install**, **Journal**. Run `scripts/discovery/classify_intent.py --args "$ARGUMENTS" --json` when mode is ambiguous.

## Dispatch

| `$ARGUMENTS`                                                                      | Mode               | First move                                                                                                                |
| --------------------------------------------------------------------------------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| `Empty`                                                                           | Intake             | Ask for harnesses or `all`, then ask for `project`, `global`, or `both`                                                   |
| `all`                                                                             | Intake             | Ask only for level                                                                                                        |
| `all <level>` / `<level> all`                                                     | Audit              | Dry-run all supported harnesses in deterministic order                                                                    |
| `<harness...>`                                                                    | Intake             | Resolve one or more harnesses, then ask only for missing level                                                            |
| `<level>`                                                                         | Intake             | Resolve level, then ask only for missing harnesses                                                                        |
| `<harness...> <level>` / `<level> <harness...>`                                   | Audit              | Run dry-run review for the selected harnesses and level                                                                   |
| `apply approved`                                                                  | Apply Approved     | Apply the last matching dry-run batch only if the user already approved it in this session                                |
| `apply <harness...> <level>` / `apply <level> <harness...>`                       | Apply Approved     | Apply only if the same scope was already reviewed and approved in this session; otherwise rerun audit first               |
| `install <harness...>`                                                            | Install Guidance   | Show exact `npx skills add ...` commands only; do not edit configs                                                        |
| `discover`                                                                        | Discover full      | W0 scans → scouts → ideate → report per `references/discovery-pipeline.md`                                                |
| `discover audit` / `audit gaps`                                                   | Discover W0        | Gap report only; no scouts                                                                                                |
| `discover resume` / `discover list`                                               | Journal            | Load or list `~/.agents/harness-master/discovery/` sessions                                                               |
| `usage <harness\|all> [level] [days]`                                             | Usage Review       | Collect safe aggregate usage/cost/token/tool signals; read-only                                                           |
| NL: missing skills / expand / find best X for harness                             | Discover (inferred)| Depth: full, focused, candidate, or compare — see discovery-pipeline.md                                                   |
| Natural language: "review/audit/check/tune <harness> config"                      | Audit              | Normalize harnesses + level, then run dry-run review                                                                      |
| Natural language: "review/analyze usage/cost/tokens/tools for <harness>"          | Usage Review       | Normalize harnesses + level, collect safe metadata only, and report optimization lanes                                    |
| Natural language: "find/latest/best plugins/extensions/MCPs/skills for <harness>" | Discover focused   | W0 + category scouts + `source_probe.py`; read-only                                                                       |
| Natural language approval like "approved", "do it", "apply those changes"         | Apply Approved     | Continue only if the immediately preceding `harness-master` review matches the scope and is still current                 |
| Requests to create agents or MCP servers                                          | Refuse + redirect  | Redirect to the correct specialized skill                                                                                 |
| Unsupported harness names                                                         | Refuse + clarify   | List supported harnesses and ask the user to choose from that set                                                         |

### Empty-Args Handler

If the user invokes `/harness-master` with no arguments:

1. Ask which harnesses to review or whether to use `all`.
2. Ask for `project`, `global`, or `both`.
3. Explain that the first pass is always dry-run only.

## Input Normalization

- Supported harnesses: `claude-code`, `claude-desktop`, `chatgpt`, `codex`, `github-copilot-web`, `github-copilot-cli`, `cursor`, `gemini-cli`, `antigravity`, `grok-build`, `opencode`, `perplexity-desktop`, `cherry-studio`
- Supported levels: `project`, `global`, `both`
- Supported research categories: `config`, `plugin`, `extension`, `mcp`, `skill`, `all`
- Supported usage windows: positive day counts such as `7`, `14`, `30`, or `days=14`; default to `14` when absent
- Harness aliases:
  - `claude`, `claude-code` -> `claude-code`
  - `claude-desktop` -> `claude-desktop`
  - `chatgpt`, `chatgpt-desktop`, `openai-chatgpt` -> `chatgpt`
  - `codex` -> `codex`
  - `cursor`, `cursor-agent`, `cursor-editor`, `cursor-desktop`, `cursor-cli`, `agent-cli`, `cursor-cloud`, `cursor-cloud-agent`, `cursor-background-agent`, `cursor-web` -> `cursor`
  - `gemini`, `gemini-cli` -> `gemini-cli`
  - `antigravity`, `google-antigravity` -> `antigravity`
  - `github-copilot`, `copilot`, `gh-copilot` -> expand to `github-copilot-web` and `github-copilot-cli`
  - `github-copilot-web`, `copilot-web`, `copilot-cloud`, `copilot-coding-agent` -> `github-copilot-web`
  - `github-copilot-cli`, `copilot-cli` -> `github-copilot-cli`
  - `grok`, `grok-build`, `grok-cli` -> `grok-build`
  - `opencode`, `open-code` -> `opencode`
  - `perplexity`, `perplexity-desktop`, `perplexity-mac` -> `perplexity-desktop`
  - `cherry`, `cherrystudio`, `cherry-ai`, `cherry-studio` -> `cherry-studio`
- Level aliases:
  - `project`, `repo`, `local` -> `project`
  - `global`, `user` -> `global`
  - `both`, `all-levels` -> `both`
- Split multiple harnesses on commas and whitespace.
- If the user supplies both `all` and named harnesses, ask which form they want.
- Deterministic `all` order: `claude-code`, `claude-desktop`, `chatgpt`, `codex`, `github-copilot-web`, `github-copilot-cli`, `cursor`, `gemini-cli`, `antigravity`, `grok-build`, `opencode`, `perplexity-desktop`, `cherry-studio`
- Unknown tokens are never guessed. Ask one focused clarification question.


### Grok Build (`grok-build`)

- **Instruction entry:** `AGENTS.md` -> `instructions/grok-global.md` -> `instructions/global.md`
- **Policy template:** `config/grok-config.toml` merged into `~/.grok/config.toml` via repo Grok platform adapter sync
- **Ownership:** replace-owned (`models`, `mcp_servers`, `plugins`, `compat`, `telemetry`) vs blend-owned (`ui`, `features`, `session`, `tools`, `toolset`, `subagents`, `memory`)
- **Skills:** no native Skills CLI adapter; install/sync uses `claude-code` alias + mirror to `~/.grok/skills`; inventory also scans repo `.grok/skills` (project scope)
- **Plannotator:** CLI + skills + hooks (no Grok npm plugin). Install: `grok plannotator install` (repo CLI). Policy: `config/grok-plannotator-hooks.json` -> `~/.grok/hooks/plannotator.json`; home shim maps `block` -> `deny`. Curated in `docs/src/authoring/skills/*.mdx`. Contrast OpenCode `@plannotator/opencode@latest`.
- **Env (not in TOML):** `GROK_WEB_FETCH`, `GROK_MEMORY`, `GROK_SUBAGENTS`, `GROK_LSP_TOOLS` — document in `config/grok-env.sh`; verify with `/grok-delegate preflight`
- **Cross-harness delegate:** `/grok-delegate` — native headless `grok -p` / `-r` / worktrees / leader for Codex/OpenCode task graphs (not config sync)
- **Isolated sync:** repo stack sync with `--platforms grok --targets home` (skips other harness home merges; includes Plannotator hook refresh)

## Classification Gate

1. Parse `$ARGUMENTS` into harnesses, level, `all`, install intent, apply intent, and unresolved tokens.
2. If unresolved tokens remain, ask a single clarification question before continuing.
3. If the request is `discover ...`, gap/missing/expand intent, or find-best-for-harness NL, run Discover (infer depth via `classify_intent.py` or discovery-pipeline.md).
4. If the request is `usage ...`, run Usage Review only.
5. If the request is `install ...`, run Install Guidance only.
6. If ad-hoc "find skill for X", redirect to find-skills. If create skill, redirect to skill-creator. If open-ended non-harness research, redirect to `/research`.
7. If the request is `apply ...` or an approval phrase, run Apply Approved only if the matching dry-run review already exists in this session. Otherwise rerun audit first.
8. If the request includes unsupported harnesses, refuse cleanly and list the supported set.
9. If harnesses are missing (audit/usage), ask only for harnesses or `all`.
10. If the level is missing (audit/usage), ask only for `project`, `global`, or `both`.
11. Otherwise run Audit in dry-run mode.

## Classification Logic

1. Route explicit mode tokens first: `discover`, `usage`, `install`, `apply`, `resume`, `list`.
2. Route gap/missing/expand/find-best NL to Discover depths (not Audit).
3. Route complete harness/level scopes to Audit when config tune/fix intent and no discover signal.
4. Route usage/cost/token NL to Usage Review.
5. Route approvals to Apply Approved only when the immediately preceding dry-run audit matches the requested scope.

## Workflow

### Mode A: Audit (default, dry-run first)

1. **Gate 0 — Discover surfaces**
   - Run:
     ```bash
     uv run python scripts/discover_surfaces.py --repo-root . --level <level> --harness <canonical-harness> [--harness ...]
     ```
   - Parse the JSON output and classify each surface as `present`, `missing`, `generated`, `merged`, `repo-observed`, or `blind-spot`.
   - If the script cannot run, fall back to manual discovery with `Glob`, `Read`, and `Grep`.

2. **Gate 1 — Inspect project context before recommending fixes**
   - Read the repo's intent and operating model first: `README.md`, `AGENTS.md`, harness-facing project files, key manifests, CI/workflow signals, and repo-native orchestration logic when present.
   - In this repository, treat the repo-level harness sync script together with `config/tooling-policy.json` and `config/sync-manifest.json` as canonical context for managed/generated/merged harness surfaces.

3. **Gate 2 — Refresh latest official guidance**
   - Read `references/latest-doc-sources.md`.
   - Use `llms.txt` first when available, then first-party docs, then canonical vendor repo docs, then web fallback only if needed.
   - If official docs are unavailable, enter degraded mode and lower confidence.

4. **Gate 3 — Audit each selected harness independently**
   - Load `references/harness-surfaces.md`, `references/harness-checklists.md`, and `references/evidence-boundaries.md` selectively for the selected harnesses only.
   - For `both`, compare project/global precedence before recommending edits.
   - Mark generated surfaces explicitly. Prefer fixing the canonical source over directly editing generated output.
   - Treat missing native surfaces as evidence to assess, not automatic failure.

5. **Gate 4 — Report dry-run findings**
   - Use the structure in `references/output-format.md`.
   - Every finding must include severity, affected surface, evidence tag, why it matters for this project, and the correct home for the fix.
   - Show concrete patch previews when the correct change is clear.
   - Stop after the dry-run report and wait for explicit user approval.

### Mode B: Apply Approved

1. Apply only after an explicit approval gate.
2. Approval is valid only when the immediately preceding `harness-master` dry-run review in the same session already covered the same harness set and level.
3. If the reviewed scope is stale, missing, ambiguous, or contradicted by new evidence, rerun Audit before editing.
4. Restate the approved batch before making changes.
5. Apply the smallest approved batch only. Do not broaden scope silently.
6. If the approved remediation is an install step, use the exact `npx skills add ...` guidance from `references/install-guidance.md`.
7. After edits, rerun surface discovery and targeted dry-run checks for the touched harnesses, then summarize remaining gaps.

### Mode C: Discover

Read-only gap expansion and harness-bounded research. Load `references/discovery-pipeline.md` and `references/discovery/coordinator-contract.md`.

1. Classify depth (full, focused, candidate, compare, w0only, ideate, journal).
2. Run W0 scripts before any scouts when depth requires gaps.
3. Use `source_probe.py` and `candidate_score.py` inside W2/W2b — not as separate user-facing modes.
4. Block apply/install until user confirms; config fixes require Audit + `apply approved`.

### Mode D: Usage Review

Use this mode for `usage` or natural-language requests to review token cost, quota, tool friction, MCP use, skill fit, plugin fit, context health, session attribution, or harness telemetry posture.

1. Treat the entire mode as read-only. Do not edit files, install packages, create jobs, export raw sessions, print raw prompts, print raw traces, or mutate harness configs.
2. Normalize harnesses, level, and usage window. Default missing window to `14` days.
3. Run surface discovery plus the safe usage probe:
   ```bash
   uv run python scripts/usage_probe.py --repo-root . --harness <canonical-harness> --level <level> --days <days> --json
   ```
4. Load `references/usage-review.md`, `references/evidence-boundaries.md`, and `references/output-format.md`.
5. Use runtime tools such as `token_stats`, `token_history`, `token_export`, `insights_collect`, `agent_attribution`, `quota_status`, `gemini_quota`, `workspace-summary`, and `git-smart-status` only when they match the requested harness and privacy class.
6. Normalize findings into usage signals and score source coverage, privacy safety, cost/token posture, tool efficiency, MCP hygiene, skill fit, plugin fit, context health, approval safety, and recommendation actionability.
7. Report recommendation lanes: `keep`, `tune-config`, `tune-skill`, `tune-mcp`, `tune-plugin`, `tune-workflow`, `instrument`, `defer`, or `do-not-change`.
8. If the user asks to apply a Usage Review recommendation, block the apply step and require a matching dry-run Audit plus explicit approval first.

## Scaling Strategy

| Scope                           | Strategy                                                                                                                                                   |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| small                           | 1 harness and 1 level: inline review with one per-harness report                                                                                           |
| medium                          | 2-3 harnesses or one `both` scope: review each harness independently, then add a short synthesis                                                           |
| large                           | 4+ harnesses or `all`: batch discovery where possible, keep per-harness sections strict, then finish with cross-harness synthesis and ranked cleanup order |
| Discover (full/focused)         | Use Pattern F semantics: explore sources, score candidates, synthesize evidence, and stop before apply                                                     |
| Team-capable Discover           | Use Pattern E or nested waves for source-family scouts, with accounting for every dispatched scout                                                         |
| Usage review                    | Prefer aggregate probes and runtime summaries first; avoid raw transcripts, raw traces, secret files, and message-table reads                              |

## Latest-Doc Lookup Policy

Use the most current authoritative guidance available:

1. `llms.txt` or equivalent official index
2. First-party docs pages for config, instructions, rules, MCP, and permissions
3. Canonical vendor repo docs if first-party product docs are incomplete
4. Web fallback only when the above are unavailable

Never claim `latest` without evidence from a current source.

## Per-Harness Review Contract

- Review each harness independently before writing any synthesis.
- Tag every finding as `verified-file`, `verified-doc`, `repo-observed`, or `blind-spot`.
- Surface the authoritative, secondary, generated, and merged config surfaces for the selected level.
- For `both`, report project/global conflicts before recommending changes.
- If a harness-specific native surface is not observable from the current session, mark it as a blind spot instead of inventing behavior.
- Antigravity project-level advice must clearly separate first-party documented global behavior from repo-observed compatibility assumptions.

## Install Guidance Contract

- Load `references/install-guidance.md` only when the user asks how to install `harness-master`, or when missing skill availability is the actual root cause.
- Default surfaced form:
  ```bash
  npx skills add <source> --skill harness-master -y -g --agent <agent>
  ```
- Do not recommend install commands for native config problems.
- Do not suggest project-local install by default. Mention `python scripts/install_skills.py --local --execute` only if the user explicitly asks for project-local installation.

## Validation Contract

After changing this skill, run:

```bash
python scripts/check.py
uv run python scripts/usage_probe.py --repo-root . --harness opencode --level both --days 14 --json
uv run python scripts/discover_surfaces.py --repo-root . --level both --harness claude-code --harness claude-desktop --harness chatgpt --harness codex --harness github-copilot-web --harness github-copilot-cli --harness cursor --harness gemini-cli --harness antigravity --harness opencode --harness perplexity-desktop --harness cherry-studio
```

Completion criteria:

- metadata and eval manifests validate
- packaging remains portable
- surface discovery smoke-check accepts every canonical harness
- dry-run/apply behavior still requires approval before edits
- Discover remains read-only and blocks apply until a matching audit is approved
- usage review remains read-only, redacts sensitive sources, and blocks apply until a matching audit is approved

## Cross-Harness Synthesis Contract

After all per-harness reviews, synthesize:

- Shared issues across harnesses
- Conflicting conventions or precedence rules
- Duplicated instruction sources or MCP definitions
- Generated-vs-canonical drift patterns
- Highest-leverage cleanup order if the user wants a follow-up apply batch

## Output Contract

Every per-harness report must include:

1. Harness
2. Level
3. Files Reviewed
4. Docs Checked
5. Project Context Summary
6. Blind Spots
7. Scorecard
8. Findings
9. Recommended Changes
10. Proposed Patch Preview
11. Confidence

Then add a cross-harness synthesis section when 2+ harnesses were reviewed.

## Reference File Index

| File                                | Content                                                                                              | Read When                                                |
| ----------------------------------- | ---------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| `references/workflow.md`            | Gate-by-gate audit/apply workflow, precedence rules, degraded mode, and approval gate details        | Audit, Apply Approved                                    |
| `references/latest-doc-sources.md`  | Official `llms.txt` and docs URLs per harness, plus fallback order                                   | Latest-doc refresh                                       |
| `references/harness-surfaces.md`    | Project/global surfaces, precedence, install agent names, generated/merged notes                     | Surface interpretation                                   |
| `references/harness-checklists.md`  | Per-harness audit checklist and edge cases                                                           | Per-harness review                                       |
| `references/evidence-boundaries.md` | Evidence tags, blind-spot handling, and contradiction policy                                         | Reporting findings                                       |
| `references/install-guidance.md`    | Exact `npx skills add ...` commands, when to surface them, and anti-patterns                         | Install Guidance                                         |
| `references/output-format.md`       | Per-harness and cross-harness report templates                                                       | Final output                                             |
| `references/discovery-pipeline.md`    | W0–W4 discover waves, depth inference, evidence vs contracts, redirects                             | Discover                                                 |
| `references/discovery/`             | Coordinator contract, scout templates, output formats, research integration                          | Discover scouts and reports                              |
| `references/ecosystem-research.md`  | Legacy source-family notes; prefer discovery-pipeline.md for dispatch                                  | Discover W2 source planning                              |
| `references/source-profiles.md`     | Source families, programmatic access, confidence roles, and degraded-source behavior                 | Discover W2 source planning                              |
| `references/usage-review.md`        | Read-only usage sources, privacy classes, scorecard, signal schema, and recommendation lanes         | Usage Review                                             |
| `data/research-sources.json`        | Machine-readable source registry for source planning and probe scripts                               | Discover W2 source planning                              |

Read only the references needed for the active step. Do not preload all references.

## Progressive Disclosure

Load reference files as indicated by the active mode. Do not load all references at once; use the dispatch table, source plan, and final output needs to choose the smallest relevant set.

## Canonical Vocabulary

These terms are canonical for `harness-master` reports and should be used exactly.

Use these terms exactly throughout:

| Term                | Meaning                                                                                                   | NOT                        |
| ------------------- | --------------------------------------------------------------------------------------------------------- | -------------------------- |
| `harness`           | One supported agent/runtime target                                                                        | `editor`, `toolchain`      |
| `level`             | `project`, `global`, or `both` scope for the review                                                       | `environment`              |
| `project surface`   | Repo-local file or generated artifact used by a harness                                                   | `global config`            |
| `global surface`    | User-level harness config outside the repo                                                                | `project file`             |
| `dry-run`           | Findings + patch preview only; no edits                                                                   | `apply`                    |
| `approval gate`     | Explicit user consent required before edits                                                               | `implied approval`         |
| `blind-spot`        | A surface or behavior that is not observable in the current session                                       | `guess`                    |
| `repo-observed`     | Behavior inferred from the current codebase's real harness wiring                                         | `official-doc evidence`    |
| `patch preview`     | Proposed diff or snippet shown before edits                                                               | `applied change`           |
| `canonical source`  | The file or config that should be changed instead of a generated output                                   | `generated surface`        |
| `source plan`       | Read-only list of sources, URLs/commands, env vars, evidence fields, and failure modes                    | `apply plan`               |
| `candidate dossier` | Normalized evidence bundle for one ecosystem candidate                                                    | `endorsement`              |
| `support tier`      | Adoption readiness class backed by evidence and validation state                                          | `popularity rank`          |
| `quarantine`        | Candidate class for credential, proxy, destructive, offensive, or broad-permission risk                   | `rejection without review` |
| `usage signal`      | Sanitized aggregate evidence about token, cost, quota, tool, MCP, skill, plugin, or workflow behavior     | `raw transcript`           |
| `privacy class`     | Sensitivity class that determines whether a source can be collected, summarized, or must stay manual-only | `permission bypass`        |

## Critical Rules

1. Every new `harness-master` run starts in dry-run audit mode.
2. Never edit before explicit user approval.
3. `Apply Approved` is valid only after a matching dry-run review in the current session.
4. Ask only for missing inputs. Never re-ask resolved harnesses or levels.
5. Always inspect project context before recommending harness changes.
6. Always refresh latest official guidance before claiming a configuration is current or stale.
7. Mark blind spots explicitly. Do not guess hidden or UI-only settings.
8. Prefer edits to canonical sources over generated or merged outputs when this is clear from evidence.
9. Every finding must carry an evidence tag: `verified-file`, `verified-doc`, `repo-observed`, or `blind-spot`.
10. Show concrete patch previews whenever the correct edit is clear.
11. Use `npx skills add ...` only when installation is genuinely the right next step.
12. Unsupported harnesses must be refused cleanly with the supported set listed.
13. Ecosystem research is advisory and read-only. Never apply from a research report alone.
14. Credentialed APIs are optional enrichments. Missing credentials lower confidence but do not block baseline source planning.
15. GitHub GraphQL enriches known candidate repositories; use REST/search or code/file lookup for broad discovery.
16. Usage Review is advisory and read-only. Never apply config changes, install tools, export raw sessions, or print raw prompts/traces from usage findings alone.
17. Usage Review may use aggregate-safe and sanitized metadata sources, but secret files, credential values, raw transcripts, raw traces, and raw message-table bodies are out of scope.
