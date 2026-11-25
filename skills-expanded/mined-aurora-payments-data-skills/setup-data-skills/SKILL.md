---
name: setup-data-skills
description: Configure this repo for the data-engineering skills. Set up its issue tracker, triage label vocabulary, domain doc layout, warehouse write-safety rails, data-quality registry, and dashboards config. Run once before first use of the other data-engineering skills.
disable-model-invocation: true
---

# Setup Data Skills

Scaffold the per-repo configuration that the engineering skills assume:

- **Issue tracker**: where issues live (GitHub by default; local markdown is also supported out of the box)
- **Triage labels**: the strings used for the five canonical triage roles
- **Domain docs**: where `CONTEXT.md` and ADRs live, and the consumer rules for reading them
- **Warehouse**: the dev/prod split, cost rails, write dispositions, and rollback commands every skill must respect before running SQL
- **Data-quality registry**: where data-quality findings live and how they get IDs
- **Dashboards**: the BI tool, the org's dashboard rubric, the workbook ↔ model registry, and where dashboard artifacts land
- **Layer docs**: the data canons that layer over base skills this suite doesn't fork, copied in and wired so they actually load

This is a prompt-driven skill, not a deterministic script. Explore, present what you found, confirm with the user, then write.

## Process

### 1. Explore

Look at the current repo to understand its starting state. Read whatever exists; don't assume:

- `git remote -v` and `.git/config`: is this a GitHub repo? Which one?
- `AGENTS.md` and `CLAUDE.md` at the repo root: does either exist? Is there already an `## Agent skills` section in either?
- `CONTEXT.md` and `CONTEXT-MAP.md` at the repo root
- `docs/adr/` and any `src/*/docs/adr/` directories
- `docs/agents/`: does this skill's prior output already exist?
- `.scratch/`: sign that a local-markdown issue tracker convention is already in use
- Is the `triage` skill installed? (a `triage` skill folder alongside this one, or `triage` in your available skills.) This decides whether Section B runs at all.
- Which base skills for the layer docs are installed: `to-tickets`, `triage`, `domain-modeling`, `design-an-interface`, `improve-codebase-architecture`, `git-guardrails-claude-code`. Check the same way: a skill folder alongside this one, or the name in your available skills. Section G installs only the layers whose base is present.
- Transformation-stack signals: `dbt_project.yml` (and the target names in `profiles.yml`), `workflow_settings.yaml` (Dataform core 3.0+) or legacy `dataform.json`, orchestrator code (a `dags/` directory, a Dagster `definitions.py`), a `great_expectations/` or `gx/` directory, `.sqlfluff` or `[tool.sqlfmt]` config, CI workflows that build to the warehouse. These tell you which tools `docs/agents/warehouse.md` should speak, and seed Section D's recommendation.
- An existing data-quality registry: a findings doc with its own ID scheme, a `*_dbt_test__audit` schema (dbt `--store-failures` output), or Elementary's warehouse tables. Seeds Section E.
- BI-surface signals. These name the tool for you, so look before asking. Seeds Section F.
  - **Serialized BI source in the repo**: the strongest signal, because the tool is unambiguous: `*.model.lkml` / `*.view.lkml` / `manifest.lkml` (Looker), `*.twb` / `*.twbx` / `*.tds` (Tableau), `*.pbix` / `*.pbip` / `*.tmdl` (Power BI), `cube.js` or `model/cubes/*.yml` (Cube), `lightdash.config.yml` (Lightdash), a Metabase or Superset serialization export directory.
  - **`exposures:` in the transformation project**: tool-agnostic and the most useful find: each exposure already names a downstream surface, its type, its owner and the models it reads. That is the registry Section F otherwise leaves as a path for the user to fill in.
  - **A BI tool named in the repo docs, CI workflows, or environment templates**: a `SIGMA_*` / `LOOKER_*` variable in `.env.example`, a deploy step, a link in the README.
  - **A workbook catalog or dashboard inventory document** already maintained by hand.
  - **A connected MCP server for a BI tool**: check your available tools. If one is connected, the skills can reach that tool directly, which belongs in the config.
  - Absence of all five means only that the BI surface lives outside this repo, which is the common case. It is not evidence that dashboards don't read this warehouse, which Section F asks about.
- Monorepo signals: more than one transformation project (`dbt_project.yml`, `workflow_settings.yaml`/`dataform.json`), or a `packages/*` / `pipelines/*` layout where each package owns its own sources and models. Present only in a genuinely large multi-project repo; their absence means single-context, which is almost every repo.

### 2. Present findings and ask

Summarise what's present and what's missing. Then take the sections in order, one section and one answer at a time.

Lead each section with the recommended answer so the user can accept it in a word. Give a one-line explainer only when the choice genuinely branches; skip the section entirely when exploration already settled it (Section B when `triage` isn't installed, Section C when there's no monorepo, Sections D, E, and F when exploration found the answers), then just show the drafts in step 3.

**Section A: Issue tracker.**

> Explainer: The "issue tracker" is where issues live for this repo. Skills like `to-tickets`, `triage`, `to-spec`, and `qa` read from and write to it, so they need to know whether to call `gh issue create`, write a markdown file under `.scratch/`, or follow some other workflow you describe. Pick the place you actually track work for this repo.

Default posture: these skills were designed for GitHub. If a `git remote` points at GitHub, propose that. If a `git remote` points at GitLab (`gitlab.com` or a self-hosted host), propose GitLab. Otherwise (or if the user prefers), offer:

- **GitHub**: issues live in the repo's GitHub Issues (uses the `gh` CLI)
- **GitLab**: issues live in the repo's GitLab Issues (uses the [`glab`](https://gitlab.com/gitlab-org/cli) CLI)
- **Local markdown**: issues live as files under `.scratch/<feature>/` in this repo (good for solo projects or repos without a remote)
- **Other** (Jira, Linear, etc.): ask the user to describe the workflow in one paragraph; the skill will record it as freeform prose

Record the choice in `docs/agents/issue-tracker.md`. The GitHub and GitLab templates carry a "PRs as a request surface" flag, defaulted **off**. Leave it off and don't raise it; a user who wants external PRs in the triage queue can flip the flag in the file later.

**Section B: Triage label vocabulary.** Skip this section entirely if the `triage` skill isn't installed (exploration told you), because an uninstalled skill needs no labels.

If it is installed, ask exactly one question:

> Do you want to keep the default triage labels? (recommended: **yes**)

The defaults are the five canonical roles, each label string equal to its name: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. On **yes**, write them as-is. Only if the user says no, usually because their tracker already uses other names (e.g. `bug:triage` for `needs-triage`), collect the overrides so `triage` applies existing labels instead of creating duplicates.

**Section C: Domain docs.** Default to **single-context**, one `CONTEXT.md` plus `docs/adr/` at the repo root. This fits almost every repo; write it without asking.

Offer **multi-context** (a root `CONTEXT-MAP.md` pointing to per-context `CONTEXT.md` files) only when exploration found monorepo signals. Then confirm which layout they want.

**Section D: Warehouse write safety.**

> Explainer: Skills that run SQL need to know where they may write, what a run may cost, and how to undo a mistake. `docs/agents/warehouse.md` is the rail between an agent session and a destructive write to production.

The seed template carries the four sections (environments, cost rails, write dispositions, rollback) with per-platform blocks; propose it whole from exploration (dev/prod split from `profiles.yml` targets or the CI workflow, rollback commands with the **actual configured** window), keeping the platform block that matches and deleting the rest. Ask only what exploration couldn't settle (usually just "is this the dev target?"). Cost rails default **on**. A user who wants them off can edit the file later; don't raise it. When exploration found no transformation stack or warehouse signal at all, ask one question. Does this repo run SQL against a warehouse? If yes, collect the platform and dev/prod targets and proceed; if no, skip this section: no `warehouse.md` is written, and step 4 omits the `### Warehouse` sub-block.

**Section E: Data-quality registry.**

> Explainer: Data bugs recur, because the same root cause resurfaces across models and months, so findings need durable IDs skills can dedupe against instead of re-diagnosing. `docs/agents/dq-registry.md` records where findings live and how they get IDs.

Default posture: the registry **is** the issue tracker, so findings are issues labelled `data-quality`, the ID is the issue number; write that without asking. Two exceptions, both settled without a question: when Section A chose local markdown, the default cannot resolve, because that tracker has no labels and its issue numbers restart per feature directory, so use the seed's standalone-registry branch (`.scratch/dq/NN-<slug>.md`, monotonically allocated `DQ-NN` IDs); and when exploration found an existing registry (a findings doc with its own ID scheme, Elementary tables), keep it and record its path and ID scheme. Record the outcome in `docs/agents/dq-registry.md`.

**Section F: Dashboards.**

> Explainer: Dashboard skills need to know which BI tool the org uses, where its dashboard rubric lives, where build specs and critiques are filed, and which registry maps each shipped surface to the models and freshness columns it reads. `docs/agents/dashboards.md` is that resolution surface.

The seed template carries four sections: surface (tool + rubric pointer), starter hard rules, registry, output homes; propose it whole from exploration.

**Name the tool from what exploration found, rather than asking cold.** Serialized BI source in the repo settles it outright: `.lkml` files mean Looker, `.twb` means Tableau. Confirm the finding instead of opening the question. "This repo has Looker models under `looker/`, so I've set the BI tool to Looker" is a better prompt than "which BI tool do you use?". Ask only when exploration found nothing, and when it found signals for two tools, name both and let the user say which one the dashboards under review actually live in.

**When exploration found `exposures:`, the registry section is already answered.** Record that the registry lives in the transformation project and name the file, rather than leaving a path for the user to fill in. Exposures carry the surface, its type, its owner and the models it reads, which is what the registry section asks for. A repo with exposures should never be handed a blank registry path.

**When an MCP server for the tool is connected, record it in the Surface section**: which server, and that the dashboard skills can query the tool through it. This is the only form of "connect to the BI tool" the suite supports: no skill here builds an API client per vendor, because each would need a live instance of that vendor's product to be worth trusting.

One question exploration can't settle, always asked and always optional: does the org have dashboard guidance to point at, such as a design rubric, style guide, brand palette, or layout and formatting conventions? Whatever they name becomes the rubric pointer; the seed's starter hard rules fill the gap until something exists.

**Tool mechanics file.** `dashboard-review` loads a reference file for the org's BI tool before it touches a workbook. That file holds the mechanics only driving the tool teaches: how to resolve an identifier, how to read an element's underlying query, what breaks when capturing a screenshot. `sigma.md` ships with that skill. If the tool you named has no such file, create a stub at `docs/agents/bi-mechanics-<tool>.md` with the headings below and nothing invented under them, then record its path in `dashboards.md` so the skill loads it:

```markdown
# <Tool>: mechanics for dashboard-review

## Session and identity
_How to authenticate, and how to resolve a dashboard's stable ID from its URL._

## Mechanics
_One row per hard-won detail: how to read an element's query, how to list elements,
which path forms work and which fail._

## Visual capture
_Viewport size, wait-before-capture, and how pagination or virtualization behaves._
```

Say plainly that the file is empty on purpose and that `dashboard-review` fills it in as it learns. **Do not populate it from general knowledge of the tool.** A plausible-sounding API path that turns out to be wrong costs more than a blank heading, because the next reviewer trusts it. Only what someone has actually run belongs there.

When exploration found no BI signal at all, first ask whether dashboards read this warehouse. If no, skip this section: no `dashboards.md` is written, no mechanics stub is created, and step 4 omits the `### Dashboards` sub-block.

**Section G: Layer docs.**

> Explainer: Four of this suite's canons don't ship as skills. They are documents that layer data rules over a base skill the suite deliberately didn't fork (`to-tickets`, `triage`, `domain-modeling`, `git-guardrails-claude-code`), plus two over skills it does ship. A layer doc loads **only if something points at it**, so an uninstalled or unwired canon is silently absent: the base skill runs its stock behavior and looks correct. This section copies the canons in and writes the pointers, which is the only thing that makes them load.

The six layers and the base each one needs:

| Seed | Writes to | Loads only if this base skill is installed |
|---|---|---|
| [layers/data-slicing.md](./layers/data-slicing.md) | `docs/agents/data-slicing.md` | `to-tickets` |
| [layers/data-incident-triage.md](./layers/data-incident-triage.md) | `docs/agents/data-incident-triage.md` | `triage` |
| [layers/data-domain-modeling.md](./layers/data-domain-modeling.md) | `docs/agents/data-domain-modeling.md` | `domain-modeling` |
| [layers/data-interface-canon.md](./layers/data-interface-canon.md) | `docs/agents/data-interface-canon.md` | `design-an-interface` |
| [layers/warehouse-architecture-canon.md](./layers/warehouse-architecture-canon.md) | `docs/agents/warehouse-architecture-canon.md` | `improve-codebase-architecture` |
| [layers/warehouse-guardrails.md](./layers/warehouse-guardrails.md) | `docs/agents/warehouse-guardrails.md` | `git-guardrails-claude-code` |

Default posture: install every layer whose base skill exploration found, and write that set without asking, because a layer is inert unless its base runs, so the installed set is the answer. Show the list in step 3 like any other draft; the user drops what they don't want there.

Two things to state rather than ask:

- **Skip a layer whose base is missing**, and say which and why in step 5, as in "`data-slicing` not installed: `to-tickets` isn't present." A canon layered over an absent skill is dead weight, and a user who installs the base later re-runs this skill.
- **`warehouse-guardrails.md` carries a second install step of its own**: a hook block, described in the file's own text. Copying the doc does not arm it. Write the doc, then tell the user in step 5 that the hook is still theirs to install, and point at the file.

When exploration found none of the six base skills, skip the section entirely: no layer files, no `### Layer docs` sub-block.

### 3. Confirm and edit

Show the user a draft of:

- The `## Agent skills` block to add to whichever of `CLAUDE.md` / `AGENTS.md` is being edited (see step 4 for selection rules)
- The contents of `docs/agents/issue-tracker.md`, `docs/agents/domain.md`, `docs/agents/warehouse.md` (only when Section D ran), `docs/agents/dq-registry.md`, and `docs/agents/triage-labels.md` (only when `triage` is installed)
- The tool-mechanics stub path, when Section F is creating one, with its headings
- The **list** of layer docs Section G will install, each with the base skill it layers over. Give the file names and their bases, not their contents. The canons are long and land verbatim; showing them whole would bury the rest of the draft.

Let them edit before writing.

### 4. Write

**Pick the file to edit:**

- If `CLAUDE.md` exists, edit it.
- Else if `AGENTS.md` exists, edit it.
- If neither exists, ask the user which one to create: don't pick for them.

Never create `AGENTS.md` when `CLAUDE.md` already exists (or vice versa). Always edit the one that's already there.

If an `## Agent skills` block already exists in the chosen file, update its contents in-place rather than appending a duplicate. Don't overwrite user edits to the surrounding sections.

The block:

```markdown
## Agent skills

### Issue tracker

[one-line summary of where issues are tracked]. See `docs/agents/issue-tracker.md`.

### Triage labels

[one-line summary of the label vocabulary]. See `docs/agents/triage-labels.md`.

### Domain docs

[one-line summary of layout: "single-context" or "multi-context"]. See `docs/agents/domain.md`.

### Warehouse

[one-line summary: dev target, prod written by CI only, cost rails on]. See `docs/agents/warehouse.md`.

### Data-quality registry

[one-line summary of where findings live and the ID scheme]. See `docs/agents/dq-registry.md`.

### Dashboards

[one-line summary: BI tool, rubric location, registry location]. See `docs/agents/dashboards.md`.

### Layer docs

Data canons that layer over base skills. Each loads when its base skill runs in this repo.

- `to-tickets` → also read `docs/agents/data-slicing.md`
- `triage` → also read `docs/agents/data-incident-triage.md`
- `domain-modeling` → also read `docs/agents/data-domain-modeling.md`
- `design-an-interface` → also read `docs/agents/data-interface-canon.md`
- `improve-codebase-architecture` → also read `docs/agents/warehouse-architecture-canon.md`
- `git-guardrails-claude-code` → also read `docs/agents/warehouse-guardrails.md`
```

Include the `### Triage labels` sub-block, and write `docs/agents/triage-labels.md`, only when `triage` is installed and Section B ran. Include the `### Warehouse` sub-block, and write `docs/agents/warehouse.md`, only when Section D ran. Include the `### Dashboards` sub-block, and write `docs/agents/dashboards.md`, only when Section F ran. The `### Data-quality registry` sub-block is always included, since every repo has an issue tracker for the default to land on. When a section didn't run, its sub-block and file are both omitted.

In the `### Layer docs` sub-block, keep **one line per layer actually installed** and drop the rest; omit the whole sub-block when Section G installed none. Each line names the base skill first because that is the trigger. The line has to tell a reader running `to-tickets` that a second file applies, which a bare list of canon names would not. Copy each layer's seed to its `docs/agents/` path verbatim; these are canons, not templates, and nothing in them is repo-specific to fill in.

Then write the docs files using the seed templates in this skill folder as a starting point:

- [issue-tracker-github.md](./issue-tracker-github.md): GitHub issue tracker
- [issue-tracker-gitlab.md](./issue-tracker-gitlab.md): GitLab issue tracker
- [issue-tracker-local.md](./issue-tracker-local.md): local-markdown issue tracker
- [triage-labels.md](./triage-labels.md): label mapping (only if `triage` is installed)
- [domain.md](./domain.md): domain doc consumer rules + layout
- [warehouse.md](./warehouse.md): warehouse environments, cost rails, write dispositions, rollback (only if Section D ran)
- [dq-registry.md](./dq-registry.md): data-quality registry location + ID scheme
- [dashboards.md](./dashboards.md): BI tool, reach, mechanics-file pointer, rubric pointer, workbook registry, output homes (only if Section F ran)
- `docs/agents/bi-mechanics-<tool>.md`: the empty tool-mechanics stub, written only when Section F named a tool that has no mechanics file already (there is no seed for this; use the headings in Section F)
- [layers/](./layers/): the six data canons, copied verbatim to `docs/agents/` (only those whose base skill is installed; see Section G)

For "other" issue trackers, write `docs/agents/issue-tracker.md` from scratch using the user's description.

### 5. Done

Tell the user the setup is complete and which engineering skills will now read from these files. Mention they can edit `docs/agents/*.md` directly later, since re-running this skill is only necessary if they want to switch issue trackers or restart from scratch.

If Section F created a tool-mechanics stub, say so and say why it is empty: `dashboard-review` writes into it as it learns the tool, and nothing was invented to fill it. If the tool is Sigma, no stub was needed, because `sigma.md` ships with the skill.

Then close on the two things about layer docs the user can't see from the file list:

- **Which layers were skipped, and why**: name the missing base skill for each ("`data-slicing` skipped: `to-tickets` isn't installed"). Say that installing a base skill later and re-running this skill picks up its layer.
- **`warehouse-guardrails.md` is not armed**: if it was installed, the doc is in place but its hook block still needs installing per the file's own instructions. Point at the file and leave the step with the user.
