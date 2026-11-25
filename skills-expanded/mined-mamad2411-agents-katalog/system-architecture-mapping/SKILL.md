---
name: system-architecture-mapping
description: >-
  Map a complex multi-component system's architecture, features, and integration
  points through systematic code reading, filesystem exploration, grep
  cross-referencing, and config analysis.
version: "1.0"
author: "Hermes Agent — system investigation pattern"
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [architecture, investigation, codebase, mapping, reconnaissance, documentation, ecosystem]
    triggers: [map architecture, architecture investigation, system architecture, codebase mapping, component analysis, ecosystem documentation, reconstruction guide, document everything, build ecosystem.md, build reconstruction guide, disaster recovery docs, integration reference, professional documentation, system audit, inventory system]
    category: software-development
    related_skills: [systematic-debugging, github, domain-modeling, project-documentation-standards]
---

# System Architecture Mapping Skill

Systematically investigate and document an unfamiliar multi-component system's
full feature surface, architecture, component boundaries, config surfaces,
profiles, integration points, and communication patterns — the kind of deep
investigation needed before refactoring, integrating, operating, or documenting
a system.

This skill is the *investigation* companion to other design/implementation
skills: it maps **what exists**, not what should be built.

## When to Use

- You need to understand an unfamiliar multi-component system end-to-end.
- Someone asks for a "deep investigation" or "comprehensive map" of features.
- You need to discover all configuration surfaces, profiles, toolsets, and
  platform adapters before making changes or writing integration code.
- You are onboarding to a large codebase and need the complete picture.
- You need to document a system's architecture, component inventory, and
  integration points for a report.
- You need to **build an ECOSYSTEM.md** — the master architecture overview for a
  multi-agent system, config repo, or service fleet.
- Someone asks "give me the big picture" or "document everything about this system."

## Prerequisites

- Read access to the system's source code.
- File reading/searching tools (`read_file`, `search_files`, `terminal` with
  grep/find).
- A starting point: the system's README, AGENTS.md, or config file.

## Procedure

### Phase 1: Surface Scan (read first, search later)

Always start with the canonical documentation and config before diving into
implementation. These tell you the system's *intended* shape; implementation
tells you the *actual* shape.

1. **Read the top-level documentation.** AGENTS.md, README.md, CONTRIBUTING.md,
   or the repo's main docs. Extract: project purpose, design philosophy,
   architecture overview, directory structure, and key entry points.

2. **Read the primary config file.** `config.yaml`, `pyproject.toml`, or
   equivalent. Extract active providers, enabled features, configured
   integrations, and environment variables. This is the system's *actual
   runtime shape*.

3. **Scan the directory tree.** Use `search_files(target='files')` or
   `terminal` with `ls -la` to get the top-level structure. Note: entry point
   files, plugins/ directories, profiles/ directories, platform adapters,
   test files.

### Phase 2: Component Discovery (parallel reads, breadth first)

Identify and read all major components in parallel. Independent files can be
read simultaneously — don't serialize independent reads.

4. **List all profiles/tenants/configs.** If the system supports profiles,
   list them all and read their configs in a loop. Extract per-profile model
   config, tools, skills, MCP servers, and platform-specific settings.

5. **Discover all platform adapters.** List the adapters directory and grep for
   platform-specific config keys in the config loader. Build the full platform
   inventory.

6. **Read the tool/plugin registration system.** Understand how tools are
   discovered, registered, and gated (check_fn, required env vars, toolsets).

7. **Map all MCP servers and external integrations.** Read the MCP server
   config section and any service-gated tool requirements.

### Phase 2.5: Live-System Discovery (filesystem, not code)

When documenting a **running multi-agent system** (not just a codebase), you need
to inventory what actually exists on disk. Batch these independent explorations
in parallel wherever possible, using **delegate_task with separate subagents**
for each domain (profiles, skills, scripts, integrations) — this completes in
minutes instead of serial hours.

8. **[PARALLEL] Audit all profile directories.** For each profile in `profiles/<name>/`:
   - Read `AGENTS.md` frontmatter → extract: name, codename, team, reports_to,
     model, provider, tools, mcp_servers, authority_level
   - Check for `SOUL.md`, `PULSE.md`, `gateway/`, `gateway-service/`
   - Quick frontmatter grep is faster than reading each file fully:
     `for f in profiles/*/AGENTS.md; do sed -n '/^---$/,/^---$/p' "$f" | grep -E '^(name:|codename:|team:|reports_to:)' ; done`

9. **[PARALLEL] Inventory MCP servers from config.** Read the `mcp_servers:` block in the
   main config.yaml. For each server extract: command, purpose (infer from
   command name / path / args), enabled status, transport type. Group by
   domain (Knowledge, Browsers, Finance, Dev Tools, Intelligence, Business).

10. **[PARALLEL] Audit scripts directory.** `ls scripts/` catalogues the system's
    operational surface. Group by domain: bridges, PIM pipeline, browser
    automation, real estate, cron/watchdogs, job agent, finance, dashboard.
    Note the total count for scale context.

11. **[PARALLEL] Audit cron jobs.** Read `cron/jobs.json`. For each job extract: name,
    schedule, profile, status, run count, last error. This reveals the
    system's recurring heartbeat pattern.

12. **[PARALLEL] Audit skills library.** `ls skills/` at the category level. Count
    SKILL.md files to get the true skill depth. Note: externally-owned skills
    (under `skills.external_dirs` in config) are read-only to curation.

13. **[PARALLEL] Audit integrations.** Check for:
    - Relay configs (Buzz relay README, Nostr keypairs, channel maps)
    - `.env` key count for scale context
    - `gateway_state.json` — which platforms are connected
    - `channel_directory.json` — routing configuration
    - PIM pipeline files, firefox profiles, browser data directories

14. **Compile a scale summary.**
    ```
    | Dimension | Count |
    |-----------|-------|
    | Profiles  | N     |
    | MCP Srvrs | N     |
    | Skills    | N     |
    | Scripts   | N     |
    | Env vars  | N     |
    | Cron jobs | N     |
    | Integr.   | N     |
    ```

    **Parallel audit pattern for large ecosystems:**
    ```
    delegate_task(tasks=[
        {"goal": "Audit profiles — read AGENTS.md frontmatter for every profile",
         "context": "working_dir: ..."},
        {"goal": "Audit skills — list all skill dirs, read SKILL.md for metadata",
         "context": "skills_dir: ..."},
        {"goal": "Audit scripts + integrations — inventory scripts dir, .env keys, cron jobs",
         "context": "scripts_dir: ..."},
    ])
    ```
    Each subagent returns a structured summary; the parent compiles them into
    the final documentation suite. This avoids blowing context with raw file
    contents.

### Phase 3: Cross-Reference (follow references, grep for terms)

8. **Search for the target platform name across the codebase.** Use
   `terminal` with `grep -rl "discord"` or `grep -n "DISCORD"` to find every
   file that touches that subsystem. This catches: config, tool definitions,
   display defaults, auth logic, channel routing, platform-specific logic.

9. **Read the platform's tool implementation.** Go depth-first on files
   discovered in step 8. Read the full tool file to understand every action,
   its security gates, its error handling, and its per-action manifests.

10. **Read the platform-specific routing/access/display modules.** Profile
    routing, access control, display config defaults, channel directories,
    pairing/authorization — these are spread across separate modules, not in
    the adapter itself.

11. **Cross-reference the profile configs against the platform config**
    to find which profiles actually have platform-specific settings vs.
    which inherit defaults.

### Phase 4: Compile (structured report or ECOSYSTEM.md)

Choose your output format based on the audience:

---

**Option A — Investigation Report** (internal, detailed):

15. **Organize findings into a structured report:**
    - **Core architecture** — what the system is, design philosophy, agent loop
    - **Component inventory** — all major modules with purposes and file locations
    - **Platform integration map** — each platform with its config env vars,
      adapter status (built-in vs plugin), auth mechanism, display defaults
    - **Profile/tenant inventory** — all profiles with their model config,
      tools, skills, MCP servers, and platform-specific settings
    - **Toolset inventory** — all toolsets and their included tools
    - **Communication patterns** — how components talk to each other
    - **Security model** — auth, allowlists, intent gates, access control
    - **Integration points** — MCP servers, plugins, webhooks, relay

---

**Option B — Professional Documentation Suite** (shareable, reconstructable):

When the goal is to make a system **documented, shareable, and reconstructable
from scratch**, produce a 3-document suite instead of a single report:

15. **ECOSYSTEM.md** — Master architecture overview:
    - Executive summary with scale metrics (profiles, MCP servers, skills, scripts)
    - ASCII architecture diagram showing major subsystems and data flows
    - Component index tables organized by domain
    - Annotated data flow diagrams (user→Discord→agent→tools→response)
    - Key paths reference table
    - Operational notes and patterns

16. **RECONSTRUCTION.md** — Disaster recovery playbook:
    - Prerequisites (OS, packages, accounts needed)
    - Clone & restore steps (which repos, which paths)
    - .env file construction table (every key, source, how to obtain)
    - Infrastructure setup (Docker commands, npm installs, download URLs)
    - MCP server recovery (grouped by domain, exact restore commands)
    - Profile restoration strategy (priority tiers, regeneration commands)
    - Scripts restoration (dependencies per script)
    - Cron & watchdog setup
    - Verification checklist (health checks for every component)
    - Target completion time estimate (e.g., "4-8 hours")

17. **INTEGRATIONS.md** — Technical reference for every external connection:
    - Each integration gets: Purpose, Type, Connection Details, Key Files,
      Status, Dependencies, Quick Test
    - OmniRoute model catalog tables
    - Agent-to-agent relay maps (Buzz identities, channels)
    - Pipeline phase diagrams (PIM ingestion, real estate scoring)
    - Browser stack matrix (instance, protocol, port, purpose)
    - MCP server tables grouped by domain

18. **Update README.md** as the front door:
    - Documentation index linking all 3+ docs
    - ASCII architecture diagram (smaller version)
    - Key paths
    - Quick reference commands

19. **Update profile AGENTS.md** with an "Ecosystem Documentation" section
    pointing to the config repo's doc suite.

20. **Commit and push** the full documentation suite:
    ```bash
    git add ECOSYSTEM.md RECONSTRUCTION.md INTEGRATIONS.md README.md
    git commit -m "docs: comprehensive ecosystem documentation suite"
    git push origin main
    ```
    If docs are in a config repo separate from the main system, commit there.

---

**User preference embedding:** When documenting for a user who values
professional, thorough documentation, prioritize:
- Clear section headers with consistent formatting
- Tables with meaningful column alignment
- Shell commands that can be copy-pasted
- Scale metrics that convey the system's complexity at a glance
- "Quick Test" commands after every integration so the reader can verify
- A reconstruction guide so the system is never locked in
- Document all scripts, not just the main ones — scripts ARE the operational surface

---

**Execution strategy for large systems (30+ profiles, 100+ scripts):**

Do NOT attempt to read everything sequentially — it blows context and takes
hours. Instead:

1. **Delegate parallel audits** via `delegate_task(tasks=[...])`:
   - Subagent 1: Profiles — reads all AGENTS.md frontmatter, SOUL.md
   - Subagent 2: Skills — inventories skills directory, reads SKILL.md metadata
   - Subagent 3: Scripts + Integrations — lists scripts dir, .env keys, cron

2. **Collect results** when all subagents finish (they sync on each other).

3. **Compose docs from summaries** — the subagents return structured data,
   not raw file contents. Assemble ECOSYSTEM.md, RECONSTRUCTION.md, and
   INTEGRATIONS.md from these summaries.

4. **Verify and commit** — check file sizes, push to the config repo.

This pattern completes a full ecosystem documentation pass in 5-10 minutes
instead of 1-2 hours.

---

**Option B — ECOSYSTEM.md** (published architecture overview):

This is a formal document type meant to sit in a config repo or system
documentation set alongside README.md. Structure it as follows:

```markdown
# System Name — Architecture Overview

> **Entity · Location**
> *One-liner description*
> **Last updated:** YYYY-MM-DD

---

## Table of Contents

[numbered sections with links]

---

## 1. Executive Summary

- One paragraph on what the system is and who built it.
- **Scale table** — Profiles, MCP servers, Skills, Scripts, Cron jobs,
  Integrations, Env vars, Model aliases — each with real counts from
  Phase 2.5 discovery.
- **Key Integrations** — bullet list of the major external services.

---

## 2. Architecture Overview

ASCII diagram showing the component stack from top to bottom:

```
┌──────────────────────────────────┐
│     User-Facing Platform         │
│  Discord · API Server · Relay    │
└────────────┬─────────────────────┘
             │
┌────────────▼─────────────────────┐
│           Agent Core              │
│  Dispatcher · Profiles · Memory  │
└────────────┬─────────────────────┘
             │
┌────────────▼─────────────────────┐
│      MCP Server Grid             │
│  Knowledge · Browsers · Finance  │
│  Dev Tools · Intelligence        │
└──────────────────────────────────┘
```

---

## 3. Component Index

One subsection per major component class, each with a reference table:

- **Core Agent System** — config highlights, model routing, delegation, memory
- **Agent Profiles** — table: Profile · Codename · Team · Reports To · Role · Gateway
- **MCP Servers** — grouped by domain with command and purpose
- **Cron Jobs & Watchdogs** — Job · Schedule · Profile · Status · Pattern
- **Scripts** — grouped by domain with brief purpose
- **Skills Library** — categories with counts and notable skills
- **Integrations** — Buzz relay, Discord, PIM pipeline, OmniRoute, MemPalace

---

## 4. Data Flow

Annotated flow diagrams showing:
- Discord message → agent response
- Agent-to-agent relay (Buzz Nostr)
- PIM ingestion pipeline (sources → extract → enhance → store)

Use numbered steps with arrows:
```
Step 1: User sends message in Discord channel
  │
  ▼
Step 2: Discord Gateway receives webhook
```

---

## 5. Key Paths Reference

Tables of all important filesystem paths grouped by:
- Root installation
- Profiles
- System scripts & skills
- Configuration repository
- External dependencies

---

## 6. Operational Notes

- Profile activation patterns
- MCP server health notes
- Cron job patterns
- Model routing strategy
- Recovery document pointers
```

---

## Pitfalls

- **Don't assume a built-in directory is exhaustive.** Platform adapters may
  ship as plugins (deferred loading) rather than as files in the built-in
  adapters directory. Search for the platform name across the whole repo.
- **Don't stop at the first reference file.** One grep hit is never the full
  picture — a single platform touches config, tools, display, auth, routing,
  channel directories, and sentinel/monitoring code.
- **Don't skip empty/default profiles.** They reveal the system with no
  overrides, which is the baseline. Some profiles have extensive platform-
  specific config; most have none.
- **Don't serialize independent reads.** Config files, doc files, and profile
  listings don't depend on each other — read them in parallel.
- **Don't stop at one tool per platform.** Discord has 2 tools (core + admin)
  with 15 actions across them. Read the full implementation file.
- **Environment variable names are often the best search key.** If a platform
  uses `DISCORD_BOT_TOKEN`, search for that string — you'll find config
  loaders, tool check functions, docs, and auth code in one hit.
- **Live-system discovery: batch independent explorations.** Profile listings,
  config reads, script listings, cron audits, and skills catalog scans are all
  independent — fire them off in parallel. Each is a separate `terminal` or
  `search_files` call that doesn't depend on the others.
- **Live-system discovery: frontmatter grep beats file-by-file.** Instead of
  reading every AGENTS.md fully, grep the YAML frontmatter blocks to extract
  codename, team, and reports_to in one pass. Then read only the profiles
  that need deeper investigation.
- **ECOSYSTEM.md: verify every number.** Scale tables must be backed by real
  `ls | wc -l` or `grep -c` counts, not estimates. If you're guessing it's
  "about 40 profiles," count them exactly.
- **ECOSYSTEM.md: data flow diagrams must match real architecture.** Don't
  invent flows that sound plausible — trace the actual code path or config
  to confirm. If you can't trace it, note it as "inferred."
- **ECOSYSTEM.md: path references need to be accurate.** Every path mentioned
  (config.yaml, profiles/, scripts/, .env) must reflect the actual
  installation location for the target system, not a generic template.



## Cross-Repository Product Roadmaps with Live CRM Integration

When a user asks to fully build out an operational PWA that must integrate with a live CRM workspace, extend the architecture map into a roadmap family rather than writing one generic plan. First inventory the PWA routes, auth roles, local data model, external adapter modules, source lead assets, and current docs. Then inspect the live CRM read-only: workspace IDs, schema, record counts, custom fields, assignment relation, feature flags, and configured integration presence (never print secrets). Record actual findings separately from proposed architecture.

Use a numbered Markdown document family under `docs/plans/`: a master roadmap, bite-sized phase plans, a system-impact/integration contract, and a stable identifier/data-flow contract. Make ownership explicit across repositories: the PWA owns VA workflow and activity capture, the CRM owns management records/views, and billing/pitch infrastructure remains in its canonical product repo. Define source-of-truth rules, directionality, stable external IDs, idempotency keys, conflict policy, assignment enforcement, and rollback before implementation.

For PWA→CRM work, do not assume filtered views equal security. Enforce assignment scope in the PWA backend, project assignment to the CRM's native owner relation, and test the CRM's full record graph—not only the company list—before claiming isolation. Keep API keys server-side and make sync writes retryable via an outbox/integration-event or dead-letter path. Prefer additive domain models (for example a dedicated sales-lead model) over destabilizing a legacy generic Company model when the new workflow has different fields and lifecycle.

Roadmap acceptance criteria must include a small real pilot (one operator, 10–50 leads), duplicate-free replays, visible sync failures, live health checks, and a clean rollback path. Commit and push the documentation family after validating Markdown, diffs, and document file inventory; report exact live findings, not merely planned capabilities.

See the companion reference `references/pwa-crm-roadmap-contract.md` for the reusable investigation checklist, document-family template, and PWA↔CRM contract fields.

- What is the system's core loop and design philosophy?
- How many platforms does it integrate with? Which ones are built-in vs plugin?
- How many profiles exist? What distinguishes each one?
- What tools does each platform get? How are they gated?
- What env vars configure each platform?
- How do auth, routing, and access control work per platform?
- What external integrations (MCP servers, plugins) are active?

## Reference Files

  full Hermes Agent codebase: agent core, gateway, Discord integration, 47
  profiles, toolsets, MCP servers, delegation, memory, plugins, and relay.
- `references/model-command-pipeline.md` — deep-trace example: the `/model`
  command flow from Discord → gateway → config → model_switch core → OmniRoute
  API call, with file locations, OmniRoute lock detail, and failure-scenario
  recovery table.
- `references/ecosystem-md-worked-example.md` — methodology journal from building
  the ECOSYSTEM.md for the 48-profile Hermes Agent ecosystem: what was explored,
  in what order, what each batch yielded, and the output structure template plus
  key decisions made along the way. Use this as a blueprint for your own
  system architecture overview projects.
