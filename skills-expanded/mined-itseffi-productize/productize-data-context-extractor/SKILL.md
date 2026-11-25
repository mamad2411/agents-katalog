---
name: productize-data-context-extractor
description: >-
  Generate or improve a company-specific data analysis skill by extracting tribal knowledge
  from analysts. Use to bootstrap warehouse context, document schemas and metrics, or update
  an existing data skill with tables, terminology, filters, and query patterns.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Data Context Extractor

## Productize Preamble

Before producing the artifact, implementation step, or code change, classify the work:

- **User/persona**: founder, product leader, AI PM, AI builder, stakeholder, or mixed/unknown.
- **Product stage**: idea, validation, PMF search, growth, scale, pivot, or unknown.
- **Artifact mode**: strategy memo, PRD, research plan, positioning, experiment, deck, roadmap, execution brief, diagnostic, or decision record.
- **Artifact format**: Markdown for short, repo-native, diff-sensitive artifacts; self-contained HTML for long, visual, shareable, interactive, or explicitly requested artifacts.
- **Evidence standard**: what is known, assumed, missing, and risky.
- **Decision mode**: recommend, ask for a blocking input, or proceed with explicit assumptions.

Operating rules:

1. Do not produce generic product strategy filler. Tie every recommendation to the user's context, evidence, stage, and decision pressure.
2. Separate facts from assumptions. Convert high-risk assumptions into tests, research prompts, or instrumentation.
3. Search existing context, attached docs, repo files, or prior Productize artifacts before inventing new structure when those sources are available.
4. Ask only for inputs that materially change the output. If the next step is obvious, proceed and state assumptions.
5. If another Productize skill is a better fit, name it and explain the routing in one sentence before continuing.
6. Enforce the output contract for this skill. Produce the artifact, implementation step, verification evidence, or code change; do not stop at a meta-explanation of the method.
7. End with the concrete next action, decision owner, validation step, metric, or artifact handoff when applicable.
8. Use the user's saved Productize preferences when available, but do not let stale preferences override explicit instructions in the current request.
9. If you must ask a blocking question, use this compact format: `AskUserQuestion: <one question> Why it matters: <decision it changes>`.
10. Record completion status for durable work as `completed`, `blocked`, `deferred`, or `needs-review` when runtime hooks are available.

Artifact format policy:

- Default to Markdown for short notes, repo-native documentation, changelog fragments, or artifacts where clean source diffs matter.
- Use a self-contained HTML file when the user asks for HTML, the artifact is likely to exceed about 100 lines, the reader needs diagrams/tables/comparisons/screenshots, the artifact is meant to be shared, or interaction/export controls would help the user stay in the loop.
- Route by product job first, then choose the format. Do not create a generic HTML workflow when a Productize playbook, gate, or routed skill owns the work.
- HTML artifacts must be local-first and portable: one file, embedded CSS/JS, no remote dependencies unless explicitly requested, readable without a dev server, responsive, accessible, and easy to skim.
- Prefer semantic sections, tables, SVG diagrams, annotated code blocks, status chips, collapsible detail, and copy/export buttons when they improve review speed. Avoid decorative complexity that hides the decision.
- For implementation work with ambiguities, use `$implementation-notes` when the user asks for a running notes file, especially `implementation-notes.html` or `implementation-notes.md`.

Runtime hooks, if available:

- Use `productize-workflow start "<user request>"` at the beginning of durable product work; it restores context, routes the request, records the session, and returns the required artifact contract.
- Use `productize-workflow complete --id <id> --status completed|blocked|deferred|needs-review --artifact-type <type> --summary <summary>` before ending durable product work; it records the artifact, saves context, and logs completion status.
- Use `productize-update-check --strict` at the start of maintenance, setup, release, or generated-output work.
- Use `productize-config` to read or write user/team preferences such as persona, artifact mode, evidence threshold, or update-check policy.
- Use `productize-session-log` to record important workflow decisions.
- Use `productize-artifact-log` when a durable artifact is produced.
- Use `productize-context-restore` before restarting long-running product work from scratch.
- Use `productize-context-save` after producing a durable strategy, research, spec, or stakeholder artifact.
- Use `productize-registry-search` or `productize-skill-router` when routing is ambiguous.
- Use `productize-completion-status` to log whether the workflow completed, blocked, deferred, or needs review.

Telemetry standard:

- Keep telemetry local by default in `.productize/` or `PRODUCTIZE_STATE_DIR`.
- Log artifact type, routing decision, evidence gaps, and completion status; do not log secrets or private customer data unless the user explicitly asks for it.

Current skill metadata:

- **Skill**: `data-context-extractor`
- **Lifecycle**: Measure
- **Category**: Analytics
- **Primary artifact**: Data Context Extractor analytics diagnosis with metric readout, caveats, decision, and next instrumented step

Create or improve a company-specific data analysis skill by extracting warehouse knowledge from analysts.

## Modes

### Bootstrap Mode

Use when the user wants a new data context skill for a warehouse.

Triggers include:
- "Create a data context skill"
- "Set up data analysis for our warehouse"
- "Help me create a skill for our database"
- "Generate a data skill for [company]"

### Iteration Mode

Use when the user has an existing skill and wants to add context.

Triggers include:
- "Add context about [domain]"
- "The skill needs more info about [topic]"
- "Update the data skill with [metrics/tables/terminology]"
- "Improve the [domain] reference"

## Bootstrap Workflow

### 1. Identify Warehouse

Ask what warehouse is used: BigQuery, Snowflake, PostgreSQL/Redshift, Databricks, or another system. Check available MCP or connector tools before assuming.

### 2. Explore Schema

Use connected data tools to:
- List datasets, schemas, or databases.
- Identify the 3-5 most queried tables.
- Pull schema details for key tables.

If tools are not connected, ask the analyst for schema exports, table samples, or representative queries.

### 3. Extract Tribal Knowledge

Ask conversationally:
- Entity disambiguation: what do "user", "customer", "account", and "organization" mean here?
- Primary identifiers: what IDs matter, and which are stable?
- Key metrics: top 2-3 metrics, exact formulas, tables, time windows, caveats.
- Data hygiene: filters that must always be applied.
- Gotchas: timezone issues, null behavior, snapshots vs current state, misleading column names.

### 4. Generate Skill

Create:

```text
[company]-data-analyst/
├── SKILL.md
└── references/
    ├── entities.md
    ├── metrics.md
    ├── tables/
    │   ├── [domain].md
    │   └── ...
    └── dashboards.json
```

The generated SKILL.md should include:
- Frontmatter with name and description.
- When to use the skill.
- Warehouse dialect notes. Load `references/sql-dialects.md` and include only the matching warehouse section.
- Knowledge base navigation.
- Query safety and validation rules.
- Instructions to load only relevant reference files.

Use `references/skill-template.md` as the starting structure for the generated `SKILL.md`. Remove unused sections and replace every placeholder before delivery.

If unsure what "good" looks like, load `references/example-generated-skill.md` as a fictional quality example. Do not copy ShopCo-specific details into real customer skills.

### 5. Package Skill

When the user wants a distributable archive, run the bundled packager:

```bash
python scripts/package_data_skill.py /path/to/[company]-data-analyst /path/to/output-dir
```

The script validates the generated skill and writes a `.skill` zip archive that can be shared or installed elsewhere.

## Iteration Workflow

1. Locate or ask for the existing skill folder or zip.
2. Read SKILL.md and references to understand current coverage.
3. Ask what domain, metric, table, or terminology is missing.
4. Explore relevant tables or ask targeted analyst questions.
5. Add or update the relevant reference file.
6. Update SKILL.md navigation.
7. Repackage with `scripts/package_data_skill.py` when the user needs a distributable archive, or summarize changed files when they only need local edits.

## Reference Standards

Table docs include location, description, primary key, update frequency, key columns, relationships, sample queries, and gotchas.

Metric docs include name, definition, formula, source tables, filters, caveats, and examples.

Entity docs include definition, primary table, ID fields, relationships, standard filters, and terminology notes.

Use `references/domain-template.md` when creating domain reference files under `references/tables/`.

## Quality Checklist

- SKILL.md has valid name and description.
- Entity definitions are unambiguous.
- Metric formulas are exact.
- Standard exclusions are documented.
- SQL dialect is named.
- Each domain has sample queries.
- Reference files are linked from SKILL.md.
