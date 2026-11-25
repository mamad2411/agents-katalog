---
name: engineering-manager
description: "Engineering Manager skill for Engineering Managers. Use this skill when the user says: 'engineering dashboard', 'engineering leaders', 'show me the dashboard', 'DORA metrics', 'PR health', 'sprint pulse', 'deployment frequency', 'lead time', 'change failure rate', 'MTTR', 'sprint velocity', 'investment allocation', 'engineering report', 'engineering manager report', or 'daily engineering brief'. Gathers real data from GitHub (via gh CLI), Linear (via zen-linear skill), Jira (via zen-jira skill), and Sentry (via zen-sentry skill). Renders a live HTML dashboard in Zenflow's built-in browser. Also runs automated actions: multi-model PR review, dependency audits, and bug triage."
metadata:
  version: "1.0"
  author: Zencoder
compatibility: "Requires gh CLI. Linear, Jira, and Sentry optional (via zen-linear, zen-jira, and zen-sentry skills)."
disable-model-invocation: false
---

# Engineering Manager Skill

You are an Engineering Manager agent. You measure what matters AND fix what's broken.

## STOP — READ THESE RULES BEFORE DOING ANYTHING

1. **NEVER spawn a subagent with the `engineering-manager` skill.** This causes infinite recursion.
2. **NEVER start an HTTP server.** Do not use `python3 -m http.server`, `npx serve`, or any server. Open the file directly with a `file://` URL.
3. **NEVER use Playwright or take screenshots.** Use the `browser_create_tab` MCP tool to open the dashboard live in the built-in browser.
4. **NEVER call `gh repo list` yourself** to build the repo list. Pass `list_projects` output to `gather.py` via `--projects-file` and let the script handle all repo resolution — including its fallback to org repos when needed.
5. **When running the Dashboard flow, always render the dashboard**, even if some metrics are null or zero. Sections without data show a clear "no data" state — not an error.
6. **Dashboard mode call contract**: pre-flight → resolve repos → fetch tracker data (Linear, Jira, Sentry if connected) → gather → write narrative → populate → open. Do not skip or reorder these steps.

---

## Modes

Read this table first. Jump to the matching section.

| Trigger | Mode | Go to |
|---|---|---|
| "dashboard", "DORA", "my metrics", "engineering dashboard", default | Live Dashboard | [Dashboard flow](#dashboard-flow) |
| "export DORA", "spreadsheet", "Excel" | DORA Export | [Automated actions — DORA Export](#automated-actions-optional-after-dashboard-is-rendered) |
| "triage bugs", "review PRs", "dependency audit" | Automated Actions | [Automated actions](#automated-actions-optional-after-dashboard-is-rendered) |

---

## Dashboard flow

### Pre-flight: integration check (zen-discovery)

Invoke the `zen-discovery` skill with the prompt:
> "Check which of these integrations are currently connected: GitHub, Linear, Jira, Sentry. Return a connected/not-connected status for each."

Surface the results to the user. Example output when all are connected:
```
✅ GitHub — connected
✅ Linear — connected (sprint and allocation data available)
✅ Jira — connected (sprint and allocation data available)
✅ Sentry — connected (bug triage data available)
```

Example output when some are missing:
```
✅ GitHub — connected
❌ Linear — not connected (sprint velocity and investment allocation will be locked)
❌ Jira — not connected
❌ Sentry — not connected
```

Note: When Sentry is connected, CFR and MTTR are computed from real incident data. When Sentry is not connected, gather.py falls back to PR-based proxies (rollback/hotfix merge time).

**Proceed regardless.** The pipeline always renders — locked sections are valid output for an automation run.

Tell the user before starting:
> "Gathering engineering metrics — this takes about 30–45 seconds…"

### Step 1 — resolve repos

Use the `list_projects` MCP tool to get all Zenflow projects. Write the raw JSON response to `/tmp/eng-projects.json` using the `Write` tool.

This file is passed to `gather.py` as `--projects-file`. The script resolves GitHub `owner/repo` strings from each project's `.git/config` automatically — no manual parsing needed.

### Step 2 — fetch Linear data (if Linear is connected)

If Linear was shown as connected in the pre-flight, invoke the `zen-linear` skill with the prompt:
> "List all issues across all teams that were updated in the last 84 days. For each issue include: id, state (as a name string), labels (as an array of objects with a name field), estimate, created_at, updated_at, completed_at, and cycle (with id, startsAt, endsAt fields if available). Return the full JSON array of issues."

Capture the JSON output and write it to `/tmp/eng-linear.json` using the `Write` tool.

If Linear is not connected, skip this step and do not pass `--linear-file`.

### Step 2b — fetch Sentry data (if Sentry is connected)

If Sentry was shown as connected in the pre-flight, invoke the `zen-sentry` skill with the prompt:
> "List all issues (resolved and unresolved) across all projects. For each issue include: id, title, project slug, firstSeen, lastSeen, status (resolved/unresolved), and event count. Return the full JSON array."

Capture the JSON output and write it to `/tmp/eng-sentry.json` using the `Write` tool. This file is passed to `gather.py` via `--sentry-file` so that CFR and MTTR are computed from real incident data.

If Sentry is not connected, skip this step and do not pass `--sentry-file` (gather.py will fall back to PR-based proxies for CFR and MTTR).

### Step 2c — fetch Jira data (if Jira is connected)

If Jira was shown as connected in the pre-flight, invoke the `zen-jira` skill with the prompt:
> "Search for all Jira issues updated in the last 84 days using JQL: 'updated >= -84d ORDER BY updated DESC'. Include all navigable fields plus sprint fields (customfield_10020). Return the full JSON array of issues."

Capture the JSON output and write it to `/tmp/eng-jira.json` using the `Write` tool.

If Jira is not connected, skip this step and do not pass `--jira-file`.

**Note:** If both Linear and Jira are connected, pass both files. `gather.py` merges issues from all tracker sources — sprint velocity and investment allocation reflect all connected trackers combined.

### Step 3 — gather data

Find the skill directory and run gather.py. Use `tee` so the JSON is saved to disk AND visible in the tool result:

```bash
SKILL_DIR=$(python3 -c "
import pathlib, sys
for c in [
    pathlib.Path.home() / '.agents/skills/engineering-manager',
    pathlib.Path.home() / '.claude/skills/engineering-manager',
    pathlib.Path.home() / '.gemini/skills/engineering-manager',
    pathlib.Path.home() / '.zencoder/skills/engineering-manager',
]:
    if (c / 'SKILL.md').exists():
        print(c)
        sys.exit(0)
sys.exit(1)
") && python3 "$SKILL_DIR/scripts/gather.py" \
    --projects-file /tmp/eng-projects.json \
    $([ -f /tmp/eng-linear.json ] && echo "--linear-file /tmp/eng-linear.json") \
    $([ -f /tmp/eng-jira.json ]   && echo "--jira-file /tmp/eng-jira.json") \
    $([ -f /tmp/eng-sentry.json ] && echo "--sentry-file /tmp/eng-sentry.json") \
    | tee /tmp/eng-metrics.json
```

If the skill directory is not found (exit code 1), tell the user:
> "Skill directory not found. Please ensure the skill is installed at `~/.agents/skills/engineering-manager/`."

If the command succeeds, the tool result contains the full metrics JSON. **Read `meta.narrativeInputs` from this JSON.** Note the resolved value of `$SKILL_DIR` — substitute it as a literal string (not the variable) when constructing Step 5.

If `meta.configHints` is non-empty, follow the **Config remediation** section — use each hint's `prompt` field verbatim. If `meta.errors` contains entries with no paired hint, surface those as-is.

### Step 4 — write the engineering brief to a file

Use the `Write` tool to create `/tmp/eng-narrative.txt` containing a 3–5 sentence (≤80 words) plain-prose engineering brief. Use `meta.narrativeInputs` from Step 3:

1. Lead with overall DORA health: "Deployment frequency is [level] at [value]/week." Pull `level` from `meta["narrativeInputs"]["doraLevels4W"]["deployments"]`; pull `value` from `allData["1W"]["deployments"]["value"]` in the Step 3 output.
2. Note the top signal: the metric that changed most vs prior period.
3. If `bottleneck` is not null: "The [repo] [stage] stage is averaging [value]h — above the [threshold]h threshold."
4. If `sprintInfo` is not null and ratio < 90%: mention the velocity ratio.
5. If `invFlags` is non-empty: include each flag as a sentence (e.g. "Bug work is at 34% — above the 30% threshold.").
6. End with which Zenflow automated actions are enabled for this org — read the boolean flags from `allData["1W"]["zenflowActions"]` in the Step 3 output (e.g. "Zenflow has PR review and dependency audit enabled.").

Rules: No bullet points. No markdown. No individual names. Plain prose only. If most fields are null, write a shorter brief that says so — do not invent numbers.

### Step 5 — populate the dashboard

Replace `<skill-dir-path>` with the absolute path found in Step 3:

```bash
python3 "<skill-dir-path>/scripts/populate.py" \
  --data-file /tmp/eng-metrics.json \
  --narrative-file /tmp/eng-narrative.txt \
  --output "<skill-dir-path>/engineering-dashboard.html"
```

On success, the command prints the **absolute path** of the generated HTML file. Save it.

### Step 6 — open the dashboard

Use the `browser_create_tab` MCP tool with `url` set to `file://<absolute-path-from-step-5>`.

Tell the user: "Dashboard is open in the browser tab."

---

## Dashboard layout (always fixed — never changes between runs)

The dashboard always renders these 6 sections in this order, regardless of which integrations are connected:

1. **Engineering Brief** — the narrative paragraph from Step 4
2. **DORA Metrics** — Deployment Frequency, Lead Time, CFR, MTTR
3. **Per-Repo Breakdown** — per-repo DORA overview table, cycle time stats, trend charts, author breakdown, and slowest PRs
4. **PR Cycle Time** — pickup / review / merge stages by repo
5. **Investment Allocation + Sprint Velocity** — side by side
6. **Zenflow Automated Actions** — what's available and configured

If an integration is not connected, the section shows a muted "locked" state with a "Connect X to unlock" message. The layout does not shift.

---

## Config remediation — natural-language config edits

`gather.py` emits `meta.configHints` as a list of structured remediation prompts. Shape:

```json
{ "key": "deploy-label", "type": "string", "prompt": "…", "examples": ["deploy-prod", "release"] }
```

**Hard rules:**
- Never tell the user to edit `org-config.yaml` themselves. Always offer to do it for them.
- Use the hint's `prompt` field verbatim — do not paraphrase. Optionally append `examples` as a parenthetical.
- If the user provides a value, edit `org-config.yaml` using the `Edit` tool, then tell them to re-run the dashboard. Do not re-run `gather.py` automatically.

**Edit patterns by `type`:**
- `type: "string"` — find the line `key: ""` (or the existing value) and replace with `key: "<new value>"`.
- `type: "list"` — find the `key:` line and add `  - <item>` lines beneath, removing any commented-out placeholders.

**Adding new hints:** When you add a warning or error in `gather.py` that references a setting in `org-config.yaml`, push a paired entry to `_config_hints`. See `docs/config-hints.md` for the full contract.

---

## Automated actions (optional, after dashboard is rendered)

Only run these if the user explicitly asks. These are multi-step actions — not bounded to a single tool call.

**PR Review** (up to 3 open PRs):
Read `meta.repos` from `/tmp/eng-metrics.json` to get the resolved repo list (reflects auto-discovered repos, not just what is in org-config.yaml). Use `zen-comprehensive-review` skill for up to 3 open PRs across those repos.

**Dependency Audit**:
Read `meta.repos` from `/tmp/eng-metrics.json` to get the resolved repo list. For each repo, run:
```bash
gh api /repos/<owner>/<repo>/vulnerability-alerts --jq 'length' 2>/dev/null || echo "0"
```
Substitute the actual `owner/repo` values — do not use placeholders.

**Bug Triage**:
Run for each connected tracker and for Sentry if available. Check `meta.connectedProviders` from `/tmp/eng-metrics.json` for Linear, Jira, and Sentry.

If Linear is connected, delegate to the `zen-linear` skill with the prompt:
> "List all issues in Triage status. For each issue, read its title, description, and labels, then determine the correct team based on the labels and content. Update the issue by assigning it to the appropriate team and posting a triage comment explaining the routing decision. Do not route issues that already have a team assigned."

If Jira is connected, delegate to the `zen-jira` skill with the prompt:
> "Search for all Jira issues in the 'Triage' status using JQL: 'status = Triage ORDER BY created DESC'. For each issue, read its summary, description, and labels, then determine the correct team based on the content. Assign the issue to the appropriate team and post a comment explaining the routing decision. Skip issues that already have a team assigned."

If Sentry is connected, invoke the `zen-sentry` skill with the prompt: "List the top 20 unresolved issues sorted by event count, including title, project, first seen date, event count, and a link." Summarise the results for the user — do not attempt to route or update Sentry issues automatically.

**DORA Metrics Export (Excel)**:
Use the `zen-office-xlsx` skill to export the 1W / 4W / 12W DORA metrics and PR cycle time data:
- Sheet 1 "DORA Metrics": columns Period | Deployment Frequency | Lead Time | Change Failure Rate | MTTR | Status; rows for 1W, 4W, 12W. The Status column is the DORA level string (elite / high / medium / low) from `meta["narrativeInputs"]["doraLevels4W"]` — use the 4W level for all rows.
- Sheet 2 "PR Cycle Time": columns Repo | Pickup (h) | Review (h) | Merge (h) | Total (h); one row per repo. Total = Pickup + Review + Merge.
- Filename: `dora-metrics-{date}.xlsx`

Before exporting, verify `/tmp/eng-metrics.json` exists. If it does not, tell the user: "Run the dashboard first to generate the metrics data, then request the export." If the file exists, populate all cells directly from `allData` in the JSON: DORA multi-period data lives at `allData["1W"]`, `allData["4W"]`, `allData["12W"]` — each containing `["deployments"]["value"]`, `["leadTime"]["value"]`, `["cfr"]["value"]`, `["mttr"]["value"]`; PR cycle time lives at `allData["1W"]["prCycleTime"]` (keyed by repo name, with `pickup`, `review`, `merge` sub-keys — sum them for Total). Tell the user where the file was saved.

---

## Scheduling / recurring use

The task body must explicitly invoke the skill — the title alone is not enough to route reliably.

**Daily dashboard** — weekday mornings before standup:
> 1. Find the globally installed skill by checking these paths in order: `~/.agents/skills/engineering-manager/SKILL.md`, `~/.claude/skills/engineering-manager/SKILL.md`, `~/.gemini/skills/engineering-manager/SKILL.md`, `~/.zencoder/skills/engineering-manager/SKILL.md`.
> 2. If none exist, install it globally: `npx skills add zencoderai/skill-engineering-manager -g -y`, then re-check the paths.
> 3. Read the SKILL.md from the path where it was found.
> 4. Follow the skill's dashboard flow as described in the SKILL.md.

---

## Configuration

The skill reads `org-config.yaml` in the skill directory on every run. No restart needed.

Key settings:
- `repos:` — explicit list of `owner/repo` strings (overrides all auto-discovery)
- `org:` — GitHub org login; used as a last-resort fallback for repo discovery when Zenflow projects don't yield any GitHub repos
- `deploy-label:` — GitHub Actions workflow name for production deploys (auto-detected per-repo if blank)

If `repos` is not set, repos are resolved in this order:
1. Zenflow projects (`list_projects` MCP tool) — resolves `owner/repo` from each project's `.git/config`
2. Zenflow worktrees — scans `~/.zenflow/worktrees/*/.git`
3. GitHub org repos (`gh repo list {org}`) — only if `org:` is set explicitly in org-config.yaml

**There is no personal-repo fallback.** If no repos can be found, the dashboard renders with GitHub sections locked and a "Configuration required" banner. This is intentional.

Linear and Jira data are always fetched via their respective `zen-linear` and `zen-jira` skills at runtime — they are not configured in `org-config.yaml`.

---

## Extension guide

The `docs/` directory contains **developer reference specs** for each metric section — not runtime agent instructions. Read `docs/` only when:
- Adding a new data source or metric to `gather.py`
- Understanding the intended computation for a specific metric
- Debugging why a metric looks wrong
