# {Your Company} Product Management Workspace

This is a product management workspace for {Your Company}'s product organisation. It contains strategy documents, research, project files, team notes, and process templates.

## Key context files

Before doing substantive work, read the relevant context files:

- `context/current-priorities.md` — current quarter focus areas, targets, and success metrics
- `data/funnel-context.md` — funnel definitions, core metrics, and how to interpret leading vs lagging indicators
- `pm-playbook/README.md` — entry point for PM process, templates, evidence standards, and training
- `context/product.md` — how the product works end-to-end
- `context/personas/customer-personas.md` and `partner-personas.md` — needs-based personas with prioritisation

<!-- SETUP: Add any additional context files here as you create them, e.g.:
- `strategy/roadmaps/YYYY-qN-roadmap.md` — current quarter roadmap
- `strategy/activation/activation-strategy.md` — activation strategy
- `context/brand/messaging/` — brand voice, tone, and terminology
-->

## About {Your Company}

<!-- SETUP: Replace this section with a 3-5 sentence summary of your company.
Include:
- What your company does and for whom
- Your business model (how you make money)
- Your key funnel stages (e.g. Sign-up → Activation → Purchase → Retention)
- Current strategic focus
- Key executives involved in product decisions

Example:
"{Your Company} is a B2B SaaS platform for [market]. We serve [N] customers
across [segments]. Revenue comes from [model]. The executive team includes
[CEO name] (CEO), [CPO name] (CPO), and [CTO name] (CTO).

Key funnel: **Leads → Trial → Activated → Paid → Retained**

Current strategic focus is activation — reducing the 70% drop-off during onboarding."
-->

## Conventions

- **{Language preference}** throughout all documents (e.g. UK English, US English)
- **Strategy documents** apply Reforge frameworks (activation moments, PNIP pyramid, psych framework, growth loops)
- **Project/experiment documents** follow the template in `pm-playbook/` — always include hypothesis, evidence, success metrics, guardrails, and risks
- **Goals should be outcome-oriented**, not deliverables. "Increase trial-to-paid from 4% to 10%" not "Launch new onboarding flow"
- **Tone** is direct, professional, and concise. No emojis unless explicitly asked. Avoid corporate fluff

## Folder structure

| Folder | Purpose |
|--------|---------|
| `context/` | Background info, current priorities, company context |
| `strategy/` | Roadmaps, OKRs, activation strategies, quarterly tracking |
| `projects/` | Active experiments and project documents |
| `insights/` | Market analysis, competitor research, qualitative research |
| `data/` | Metric definitions, saved queries, reports |
| `data/notebooks/` | Analyst Jupyter notebooks — templates, shared utilities, and automation outputs |
| `pm-playbook/` | PM process docs, templates, best practices |
| `team/` | Team member notes, feedback, agent state (gitignored — private) |
| `scripts/` | Utility scripts and automation infrastructure |

### Analyst notebooks

`data/notebooks/` contains Jupyter notebook templates for programmatic data analysis, run via papermill. The shared utilities module (`utils/pm_helpers.py`) provides data loading, z-score anomaly detection, chart styling, and standardised export helpers.

- **Templates** (`templates/`): `experiment-analysis`, `verify-claim`, `investigation-template`
- **Outputs** (`outputs/`, gitignored): Executed notebooks from papermill runs
- **Charts** (`data/reports/charts/`, gitignored): Generated PNGs, CSVs, and JSON files

Setup: `bash scripts/setup-notebooks.sh` (creates venv, installs deps, registers Jupyter kernel).

## Custom commands

Slash commands live in `.claude/commands/`. We use a naming convention to keep shared and personal commands distinct:

- **Shared commands** (no prefix) — useful for all PMs, documented here
- **Personal commands** (`{initials}-` prefix, e.g. `jk-`) — individual workflows, not expected to work for others

Each command file includes frontmatter with `owner`, `audience`, and `purpose` metadata.

### Shared commands

| Command | Arguments | Purpose |
|---------|-----------|---------|
| `/create-new-project` | — | Guided project/experiment doc creation with Socratic questioning |
| `/setup-agent` | `{initials}, {name}, {agent}` | Set up a new persistent agent — creates workspace, personalises definition, bootstraps context from live sources |
| `/interview-feedback` | `{name}, {level}, {type}` | Generate PM interview scorecard from meeting transcript |
| `/meeting-prep` | `{person name}` (optional) | Generate structured prep brief for a single upcoming meeting |
| `/meeting-schedule` | `{name1}, {name2}, ...` | Find mutual availability and schedule a meeting |
| `/investigate` | `{signal or question}` | Structured investigation: quant data + qual evidence + counter-evidence + hypothesis |
| `/daily-prep` | — | Full daily brief (today's focus + all meeting prep) |
| `/customer-reviews` | — | Weekly customer review summary from review platforms |
| `/todo` | `{initials}, {name}` | Extract action items from meetings, update todo list, refresh Today's Focus |
| `/weekly-review` | `{initials}` | End-of-week review: progress, effectiveness, actions, and goal-setting |
| `/review-design` | `{hypothesis}` (optional) | Structured design review using psych audit, personas, and assumption mapping |
| `/verify-source` | — | Audit evidence accuracy, confidence, and bias |
| `/app-review-digest` | — | Rolling app review digest — top themes with quotes and links |
| `/competitor-monitor` | — | On-demand competitor news search, analysis, and digest generation |
| `/convert-pdf` | `{filepath}` | Convert a PDF to markdown for use in Claude Code conversations |
| `/prototype` | `{hypothesis or opportunity}` | Solution prototyping: 3 concepts, psych audit, persona panels, assumption mapping |
| `/experiment-setup` | `{description or hypothesis}` | Experiment planning: sample size, run time, ROTI, confidence intervals, decision rules |
| `/experiment-writeup` | `{experiment name or file path}` | Structured experiment results analysis with decision recommendation |
| `/export-transcripts` | — | Export meeting transcripts to local markdown files |
| `/product-suggestions-digest` | — | Monthly digest of top product suggestions ranked by votes |
| `/learn-1-discovery` | — | Training: Discovery & Prioritisation (Module 1 of 6) |
| `/learn-2-solution` | — | Training: Solution Prototyping & Validation (Module 2 of 6) |
| `/learn-3-experiment` | — | Training: Experiment Design & Prioritisation (Module 3 of 6) |
| `/learn-4-design` | — | Training: Design Best Practice (Module 4 of 6) |
| `/learn-5-build-launch` | — | Training: Build & Launch (Module 5 of 6) |
| `/learn-6-analyse` | — | Training: Analyse & Learn (Module 6 of 6) |

### Adding a new command

1. Prefix with your initials if it's personal (e.g. `jk-weekly-standup.md`)
2. Add frontmatter at the top of the file:
   ```
   <!-- owner: JK | audience: personal | last-updated: 2026-02 -->
   <!-- purpose: One-line description of what this command does -->
   ```
3. For shared commands, use `owner: shared | audience: all-pms` and add an entry to this table

## Custom agents

Agents are available in `.claude/agents/` for different purposes:

**Perspective agents** — stateless specialist lenses, invoked on-demand:
`executive`, `data-analyst`, `competitive-intel`, `user-researcher`, `customer-success`

<!-- SETUP: Create stakeholder agents for your key executives.
Copy stakeholder-template.md and customise for each person whose pushback
you want to simulate. Example: `ceo.md`, `cfo.md`, `vp-engineering.md` -->

**Panel agents** — review proposals through all personas simultaneously:
`customer-panel` (references your customer personas), `stakeholder-panel` (references your partner/B2B personas)

## Agent team

The workspace has an operational agent team — persistent agents that maintain state files, run on automation schedules, and proactively surface things. This is distinct from the perspective agents above, which are stateless and invoked on-demand.

**Full design doc:** `context/agent-team.md`

### Agent types

All agent files in `.claude/agents/` use frontmatter to identify their type:

| Type | Description |
|------|------------|
| `persistent-agent` | Maintains state file in `team/{initials}/agents/state/`, runs on schedule |
| `perspective` | Stateless specialist lens, invoked on-demand |
| `stakeholder` | Simulates a real exec for stress-testing proposals |
| `panel` | Reviews proposals through multiple personas simultaneously |

### Available persistent agents

| Agent | Short name | Outcome | State file |
|-------|-----------|---------|-----------|
| Chief of Staff | `cos` | Nothing falls through the cracks | `team/{initials}/agents/state/cos.md` |
| UX Researcher | `uxr` | User signals spotted early | `team/{initials}/agents/state/uxr.md` |
| Product & Commercial Analyst | `analyst` | Decisions grounded in accurate data | `team/{initials}/agents/state/analyst.md` |
| Coach | `coach` | You improving as a leader | `team/{initials}/agents/state/coach.md` |
| Manager | `manager` | Direct reports levelling up, standards maintained | `team/{initials}/agents/state/manager.md` |
| Strategist | `strategist` | Leadership has accurate, consistent picture | `team/{initials}/agents/state/strategist.md` |
| Product Manager | `product-manager` | Every investigation builds on prior work | `team/{initials}/agents/state/product-manager.md` |
| Engineer | `engineer` | Workspace runs cleanly and reliably | `team/{initials}/agents/state/engineer.md` |

**Setting one up:** run `/setup-agent {INITIALS}, {Name}, {agent}` (e.g. `/setup-agent SJ, Steve, cos`). One command creates the team directory, personalises the agent definition, bootstraps context from your calendar and meeting notes, and tells you how to test and refine it. See `.claude/agents/examples/README.md` for the full guide on how persistent agents work, how to connect them to messaging, and how to automate them on a schedule.

### State files

Persistent agent state files live at `team/{initials}/agents/state/{short-name}.md`. They follow a strict format with a max 80-line budget (100 for product-manager). See `.claude/agents/examples/example-state.md` for a filled-in example, or `team/TEMPLATE/agents/state/{agent}.md` for the skeleton format.

### Long-term memory

Each persistent agent also has a memory file at `team/{initials}/agents/memory/{short-name}.md` (150-line budget) plus a shared file at `team/{initials}/agents/memory/shared.md` (200-line budget). Memory stores permanent institutional knowledge — data gotchas, seasonal patterns, stakeholder preferences, past investigation conclusions — that survives state pruning and quarterly archives. See `.claude/agents/examples/README.md` for the full pattern.

## MCP integrations

This workspace can use MCP servers for: **meeting notes** (e.g. Granola, Otter), **project management** (e.g. Notion, Linear), **messaging** (e.g. Slack), **data warehouse** (e.g. BigQuery, Snowflake), **calendar** (e.g. Google Calendar), **email** (e.g. Gmail), **analytics** (e.g. Hex, Looker), and **data modelling** (e.g. dbt).

See `.mcp.json.example` for configuration.

## Evidence and insight standards

When pulling evidence, analysing data, or supporting hypothesis formation:

- **State facts, not interpretations.** Report what the data says. If you're drawing a conclusion or making an inference, explicitly label it as a hypothesis or assumption
- **Flag confidence level.** Note when an insight is supported by a single source, a small sample, one user quote, or an uncertain data source. Use phrasing like "Low confidence — based on one user interview" or "Note: this metric is from [source], which may not capture [limitation]"
- **Cite sources precisely.** Always reference the specific file, data source, research session, or document. "The data suggests..." is not acceptable — say where it comes from
- **Don't cherry-pick.** When presenting evidence for or against a hypothesis, actively look for contradictory evidence in the same sources. If you only find supporting evidence, flag that no counter-evidence was found (which is itself a signal worth noting)
- **Distinguish correlation from causation.** If two metrics move together, say so — don't imply one caused the other unless there's a controlled experiment or clear mechanism
- **Note recency and relevance.** Flag if data is from a previous quarter, a different segment, or a context that may not apply to the current question
- **Qual is not quant.** User quotes and interview findings illustrate themes — they don't prove prevalence. Always note sample size and selection method for qualitative research
- **Don't fill gaps with assumptions.** If the data doesn't answer the question, say so. "We don't have evidence for this" is a valid and useful answer

## Working with this repo

- **Don't create new files without asking.** Prefer editing existing files over creating new ones
- **Don't add generic boilerplate.** Documents should be specific to your company's context and grounded in evidence
- **When writing strategy docs**, reference actual data from the funnel context and current metrics where possible
- **The todo list** lives at `team/{initials}/todo_list.md` — follow its existing format when adding items
- **Insights and research** should cite sources and note methodology limitations
