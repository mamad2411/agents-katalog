# Repository Guidelines

## Project Overview

Super Dev is a Python CLI tool (v2.4.0) that orchestrates AI-driven development pipelines inside host environments (e.g., Claude Code). It provides governance, quality gates, and audit artifacts for commercial-grade software delivery. It is NOT an independent AI agent — it's a governance layer that runs inside a host's coding environment.

## Project Structure & Module Organization

```
super_dev/
  cli.py                         # Main CLI entry point (~298k lines), composed via mixins
  cli_parser_mixin.py            # argparse command definitions
  cli_analysis_mixin.py          # analysis subcommands
  cli_governance_mixin.py        # governance/enforcement subcommands
  cli_host_ops_mixin.py          # host tool operations (~227k lines)
  cli_host_report_renderers.py   # host report rendering helpers
  cli_experience_mixin.py        # UX enhancements
  cli_deploy_runtime_mixin.py    # deployment/runtime commands
  cli_release_quality_mixin.py   # release & quality commands
  cli_spec_mixin.py              # spec management commands
  branding.py                    # CLI branding and visual identity
  catalogs.py                    # catalog data definitions
  error_handler.py               # centralized error handling
  exceptions.py                  # custom exception classes
  i18n.py                        # internationalization support
  guard.py                       # guard/safety checks
  host_adapters.py               # host environment adapters
  host_registry.py               # host registration/discovery
  merge_safety.py                # merge safety checks
  retry.py                       # retry utilities
  runtime_evidence.py            # runtime evidence collection
  seeai_design_system.py         # SEEAI design system definitions
  seeai_smoke_scenarios.py       # SEEAI smoke test scenarios
  sequential_thinking.py         # sequential thinking utilities
  session_checkpoint.py          # session checkpoint management
  workflow_contract.py           # workflow contract definitions

  orchestrator/                  # Pipeline engine, governance, quality gates
    engine.py                    # main pipeline engine driving phase transitions
    governance.py                # governance policy enforcement
    quality.py                   # quality gate evaluation
    knowledge.py / knowledge_pusher.py  # knowledge injection into pipeline stages
    overseer.py                  # Overseer agent for plan-execute orchestration
    plan_executor.py             # Plan-Execute engine for Claude-Codex hybrid mode
    experts.py                   # expert persona management in pipeline
    context_compact.py           # context compaction for long pipelines
    contracts.py                 # pipeline contract definitions
    telemetry.py                 # pipeline telemetry and metrics

  creators/                      # Document, prompt, frontend, and backend generators
    document_generator.py        # PRD, architecture, UIUX document generation
    document_generator_content_mixin.py  # document content generation mixin
    prompt_generator.py / prompt_templates.py / prompt_sections.py  # LLM prompts
    frontend_builder.py          # frontend implementation playbooks
    implementation_builder.py    # backend implementation references
    spec_builder.py              # spec generation from documents
    adr_generator.py             # Architecture Decision Record generation
    api_contract.py              # API contract generation
    component_scaffold.py        # component implementation references
    nextjs_scaffold.py           # Next.js implementation references
    requirement_parser.py        # requirement parsing utilities
    task_executor.py             # task execution within creator pipeline
    creator.py                   # base creator class
    compact_template.py          # compact template utilities

  design/                        # Design intelligence (aesthetics, UX, charts, codegen)
    ui_intelligence.py           # UI design intelligence engine
    aesthetics.py                # visual aesthetics analysis
    ux_guide.py                  # UX guidance rules
    engine.py                    # design engine orchestration
    generator.py                 # design artifact generation
    codegen.py                   # design-to-code generation
    charts.py                    # chart design generation
    landing.py                   # landing page design
    tech_stack.py                # tech stack design decisions
    tokens.py                    # design token management

  reviewers/                     # Code review, red-team, quality gate, UI review
    quality_gate.py              # quality threshold enforcement (default: 90)
    quality_advisor.py           # quality improvement suggestions
    redteam.py                   # security red-team analysis
    code_review.py               # automated code review
    ui_review.py                 # UI compliance review
    validation_rules.py          # configurable validation rules engine
    external_reviews.py          # external review integrations
    review_agents.py             # review agent definitions
    rules/                       # validation rule definitions

  enforcement/                   # File-level validation and pre-coding checks
    validation.py                # file-level validation (no emoji icons, color tokens, etc.)
    pre_code_gate.py             # pre-coding checks
    host_hooks.py                # hook integration with host tools

  deployers/                     # Delivery packaging, CI/CD, deployment rehearsals
    delivery.py                  # delivery packaging
    cicd.py                      # CI/CD pipeline generation
    rehearsal.py / rehearsal_runner.py  # deployment rehearsal definitions and execution
    migration.py                 # deployment migration utilities

  protocols/                     # Shared protocol definitions
    a2a.py                       # agent-to-agent protocol
    output_schemas.py            # output schema definitions

  integrations/                  # External tool integration manager
    manager.py                   # integration lifecycle management
    manager_content_mixin.py     # integration manager content mixin
    install_manifest.py          # install manifest tracking

  skills/                        # Skill definitions for host environments
    manager.py                   # skill lifecycle management
    skill_template.py            # skill template generation

  web/                           # FastAPI-based web interface
    api.py                       # main API application
    helpers.py                   # API helper functions
    rate_limit.py                # API rate limiting
    routers/                     # API route modules
    frontend/                    # web frontend assets

  config/                        # Configuration management
  experts/                       # Expert persona definitions (PM, Architect, etc.)
  hooks/                         # Host tool hook integration
  analyzer/                      # Code and project analysis utilities
  memory/                        # Session memory management
  metrics/                       # Metrics collection and reporting
  policy/                        # Policy engine for governance rules
  session/                       # Session management
  specs/                         # Spec management and templates
  rules/                         # Rule definitions
  data/                          # Static data files
  utils/                         # Shared utility functions (logger, structured_logging)
  templates/                     # Jinja/data templates

knowledge/                       # Curated domain knowledge base (28 categories)
tests/                           # Test suites (unit, integration, e2e, benchmark)
scripts/                         # Build/release/utility scripts
output/                          # Generated pipeline artifacts (PRD, specs, research)
.super-dev/                      # Session state and workflow tracking
super-dev-website/               # Project website source
templates/                       # Project implementation/reference templates
```

## Build, Test, and Development Commands

```bash
# Install in development mode (requires Python 3.10+)
pip install -e ".[dev]"

# Run the CLI
super-dev

# Linting & formatting
ruff check super_dev/              # check lint issues
ruff check --fix super_dev/        # auto-fix lint issues
black super_dev/ --check           # check formatting
black super_dev/                   # apply formatting

# Type checking
mypy super_dev/

# Run all tests
pytest

# Run a single test file
pytest tests/unit/test_workflow.py

# Run a specific test
pytest tests/unit/test_workflow.py::test_function_name -v

# Run with coverage
pytest --cov=super_dev

# Performance benchmarks
python tests/benchmark.py

# Pre-flight checks before release
bash scripts/preflight.sh
```

## Coding Style & Naming Conventions

- **Line length**: 100 characters (enforced by ruff and black)
- **Target Python**: 3.10+
- **Ruff rules**: E, F, I, N, W, UP (E501 ignored — black handles line length)
- **Imports**: Must be sorted (ruff `I` rule)
- **Naming**: `snake_case` for functions/variables, `PascalCase` for classes
- **Test files**: `test_<module_name>.py` or `test_<module_name>_enhanced.py`

## Testing Guidelines

- **Framework**: pytest with pytest-cov
- **Location**: `tests/unit/`, `tests/integration/`, `tests/e2e/`
- **Naming**: Functions prefixed with `test_`, descriptive (e.g., `test_quality_gate_rejects_low_score`)
- **Fixtures**: Shared fixtures in `tests/conftest.py`
- **Coverage**: Quality gate default threshold is 90/100
- **Benchmarking**: `tests/benchmark.py` for performance regressions

## Commit & Pull Request Guidelines

This project follows **Conventional Commits**:

```
feat(scope): description        # new feature
fix(scope): description         # bug fix
docs: description               # documentation change
ci: description                 # CI/CD change
chore: description              # maintenance
release: description            # version release
```

Common scopes: `orchestrator`, `enforcement`, `website`, `hosts`, `design`. Keep messages concise, focused on "why." PRs should link to relevant issues; squash-merge is used for feature branches.

## Architecture & Pipeline

- **Pipeline phases**: discovery → intelligence → drafting → redteam → qa → delivery → deployment
- **Super Dev flow contract**: research → docs → docs_confirm → spec → frontend → preview_confirm → backend → quality → delivery
- **Plan-Execute mode**: Overseer agent decomposes tasks; Plan-Executor drives step-by-step execution (Claude-Codex hybrid)
- **Configuration**: `super-dev.yaml` (domain, tech stack, quality gate, phases, experts)
- **Session continuity**: Read `.super-dev/SESSION_BRIEF.md` before resuming; `.super-dev/workflow-state.json` tracks machine-readable state
- **Key dependencies**: rich (CLI), pyyaml (config), openai (LLM calls), fastapi/uvicorn (web API), tenacity (retries), ddgs (search)

## Coding Constraints

- Check `package.json` / framework versions before writing code
- Icons from declared library only (Lucide/Heroicons/Tabler), never emoji
- No purple/pink gradient themes
- Frontend fetch URLs must match backend route definitions exactly
- Run `super-dev enforce validate` after UI code, `super-dev quality` after features
- No emoji as functional icons or placeholders
- Colors from design tokens only

## Key Scripts

| Script | Purpose |
|--------|---------|
| `scripts/preflight.sh` | Pre-release validation checks |
| `scripts/release.sh` | Version bump and release |
| `scripts/publish.sh` | Publish to PyPI |
| `scripts/validate-superdev.sh` | Validate Super Dev setup |
| `scripts/check_delivery_ready.py` | Verify delivery artifacts |
| `scripts/knowledge_scorer.py` | Score knowledge base entries |

<!-- BEGIN SUPER DEV CODEX -->
# Super Dev for Codex CLI

Treat Codex App/Desktop selecting `super-dev` or `super-dev-seeai` from the `/` list, Codex CLI explicit `$super-dev` / `$super-dev-seeai`, and natural-language `super-dev:` / `super-dev：` / `super-dev-seeai:` / `super-dev-seeai：` messages as valid Super Dev entry points.

If the repository already contains active Super Dev workflow context, the first natural-language requirement in a new session must also continue Super Dev rather than normal chat.

## Direct Activation Rule
- Do not spend a turn saying you will read the skill first, explain the skill, or decide whether to enter the workflow.
- Treat the current trigger as already authorized to execute the full Super Dev pipeline.
- If a compatibility skill under `~/.codex/skills/` is loaded, treat it as the same Super Dev contract, not a fallback mode.

## Preferred official entry order
- Codex App/Desktop: prefer selecting `super-dev` from the `/` list. This is the enabled Skill entry, not a custom project slash command file.
- Codex CLI: prefer explicit `$super-dev`.
- Natural-language fallback for both surfaces: `super-dev: <需求描述>` or `super-dev：<需求描述>` through AGENTS.md.

## SEEAI Competition Mode
- If the user triggers `super-dev-seeai`, enter the SEEAI competition-fast contract instead of the standard long chain.
- SEEAI keeps research -> compact docs -> docs confirmation -> compact spec, then goes directly into a full-stack sprint and final polish.
- SEEAI still requires real files in `output/`, but the documents must stay compact and competition-oriented.

## Required execution
1. First reply: state that Super Dev pipeline mode is active and the current phase is `research`.
2. Read `knowledge/` and `output/knowledge-cache/*-knowledge-bundle.json` when available.
3. Use Codex native web/search/edit/terminal capabilities to perform similar-product research and write `output/*-research.md` into the repository workspace.
4. Draft `output/*-prd.md`, `output/*-architecture.md`, and `output/*-uiux.md` in the same Codex session and save them as actual project files.
5. Stop after the three core documents, summarize them, and wait for explicit confirmation.
6. Only after confirmation, create `.super-dev/changes/*/proposal.md` and `.super-dev/changes/*/tasks.md`, then continue with frontend-first implementation.

## Constraints
- Do not start coding directly after `/super-dev` skill entry, `$super-dev`, `super-dev:`, or `super-dev：`.
- Do not create Spec before document confirmation.
- If the user requests architecture changes, first update `output/*-architecture.md`, then realign Spec/tasks and implementation.
- If the user requests quality or security remediation, first fix the issues, rerun quality gate, refresh delivery evidence, and only then continue.
- 开始任何 UI 实现前，必须先锁定 `output/*-uiux.md` 中冻结的图标库、字体系统、design token system、组件生态和页面骨架。
- Before any UI implementation, first lock the icon library, typography, design token system, component ecosystem, and page skeleton from `output/*-uiux.md`.
- Do not use emoji as functional icons or placeholders.
- For non-conversational AI products, avoid Claude / ChatGPT-style sidebar chat shells unless the UI plan explicitly justifies them.
- Keep using the component ecosystem and design token direction defined in `output/*-uiux.md` rather than switching ad hoc.
- If a required artifact is only described in chat and not written into the repository, treat the step as incomplete.
- Codex remains the execution host; Super Dev is the local governance workflow.
- Use local `super-dev` CLI only for governance actions such as doctor, review, quality, release readiness, or update; do not outsource the main coding workflow to the CLI.

## Conversation Continuity Contract
- If `.super-dev/SESSION_BRIEF.md` exists, read it before responding and treat it as the active workflow state.
- If the workflow is waiting for docs confirmation, preview confirmation, UI revision, architecture revision, or quality revision, then user replies like `修改`, `补充`, `继续改`, `确认`, `通过`, `继续`, or detailed feedback remain inside the current Super Dev stage.
- After each requested revision inside a gate, stay in the same stage, update the required artifacts, summarize what changed, and wait again for explicit confirmation.
- Do not silently exit Super Dev mode because the user asked for several edits, follow-up questions, or extra constraints.
- Only leave the current Super Dev workflow if the user explicitly says to cancel the workflow, restart from scratch, or switch back to normal chat.

## Super Dev System Flow Contract
- SUPER_DEV_FLOW_CONTRACT_V1
- PHASE_CHAIN: research>docs>docs_confirm>spec>frontend>preview_confirm>backend>quality>delivery
- DOC_CONFIRM_GATE: required
- PREVIEW_CONFIRM_GATE: required
- HOST_PARITY: required
<!-- END SUPER DEV CODEX -->






<!-- BEGIN SUPER DEV OPENCODE -->
# Super Dev Integration for opencode

Super Dev 是“超级开发战队”，一个流水线式 AI Coding 辅助工具。
Super Dev does not provide model inference or coding APIs.
The host remains responsible for model execution, tools, and actual code generation.
Use the host model/runtime as-is; Super Dev only enforces the delivery protocol.
Use Super Dev generated artifacts as source of truth.

## Runtime Contract
- Treat Super Dev as a local Python CLI plus host-side rules/skills, not as a separate model provider.
- When the user triggers Super Dev, enter the protocol immediately instead of treating it as normal chat.
- When the user triggers `super-dev-seeai`, switch to the SEEAI competition-fast contract: research -> compact docs -> docs confirmation -> compact spec -> full-stack sprint -> polish/handoff.
- Use host-native web/search/browse for research and host-native editing/execution for implementation.
- Use local `super-dev` commands to generate/update documents, spec artifacts, quality reports, and delivery outputs.

## First-Response Contract
- On the first reply after a host-supported Super Dev entry (for example `/super-dev ...`, `$super-dev`, `super-dev: ...`, `super-dev：...`, `/super-dev-seeai ...`, `$super-dev-seeai`, `super-dev-seeai: ...`, or `super-dev-seeai：...`), explicitly state that the matching Super Dev mode is now active rather than normal chat mode.
- If the repository already contains `super-dev.yaml`, `.super-dev/WORKFLOW.md`, `output/*`, `.super-dev/review-state/*`, or an unfinished run state, the first natural-language requirement in a new host session must also default to continuing Super Dev rather than plain chat.
- Before the first reply, read `.super-dev/WORKFLOW.md` and `output/*-bootstrap.md` when present, and treat them as the explicit bootstrap contract for this repository.
- The first reply must explicitly state that the current phase is `research`, and that you will read `knowledge/` plus `output/knowledge-cache/*-knowledge-bundle.json` first when available before similar-product research.
- In standard mode, the next sequence is research -> three core documents -> wait for user confirmation -> Spec / tasks -> frontend first with runtime verification -> backend / tests / delivery.
- In SEEAI mode, the next sequence is research -> compact competition docs -> wait for user confirmation -> compact Spec -> full-stack sprint -> polish / handoff.
- Both modes must explicitly promise that they will stop after the three core documents and wait for approval before creating Spec or writing code.

## Local Knowledge Contract
- Read relevant files under `knowledge/` before drafting documents.
- If `output/knowledge-cache/*-knowledge-bundle.json` exists, read its `local_knowledge`, `web_knowledge`, and `research_summary` first.
- Treat matched local knowledge, checklists, anti-patterns, and scenario packs as project constraints that must flow into docs, spec, and implementation.

## Conversation Continuity Contract
- If `.super-dev/SESSION_BRIEF.md` exists, read it before responding and treat it as the active workflow state.
- If the workflow is waiting for docs confirmation, preview confirmation, UI revision, architecture revision, or quality revision, then user replies like `修改`, `补充`, `继续改`, `确认`, `通过`, `继续`, or detailed feedback remain inside the current Super Dev stage.
- After each requested revision inside a gate, stay in the same stage, update the required artifacts, summarize what changed, and wait again for explicit confirmation.
- Do not silently exit Super Dev mode because the user asked for several edits, follow-up questions, or extra constraints.
- Only leave the current Super Dev workflow if the user explicitly says to cancel the workflow, restart from scratch, or switch back to normal chat.

## Trigger
- Preferred: `/super-dev "<需求描述>"`
- SEEAI competition mode: `/super-dev-seeai "<需求描述>"`
- Local terminal only handles install / update / uninstall; normal development should return to the host session.

## Required Context
- output/*-prd.md
- output/*-architecture.md
- output/*-uiux.md
- output/*-execution-plan.md
- .super-dev/changes/*/tasks.md

## Execution Order
1. Use the host's native browse/search/web capability to research similar products first and produce output/*-research.md as a real repository file
2. Freeze PRD, architecture and UIUX documents and write them into output/* files in the repository workspace rather than only describing them in chat
3. Stop after the three core documents, summarize them to the user, and wait for explicit confirmation before creating Spec or coding
4. Create Spec proposal/tasks only after the user confirms the documents
5. Implement and run the frontend first so it becomes demonstrable before backend-heavy work
6. Implement backend APIs and data layer, then run tests, quality gate, and release preparation
7. If the user says the UI is unsatisfactory, asks for a redesign, or says the page looks AI-generated, first update `output/*-uiux.md`, then redo frontend implementation, rerun frontend runtime and UI review, and only then continue.
8. If the user says the architecture is wrong or the technical plan must change, first update `output/*-architecture.md`, then realign tasks and implementation before continuing.
9. If the user says quality or security is not acceptable, first fix the issues, rerun quality gate, refresh delivery evidence, and only then continue.
10. Before any UI implementation, first lock the icon library, typography, token system, component ecosystem, and page skeleton according to `output/*-uiux.md`.
11. Do not use emoji as functional icons or placeholders, and do not leave icon decisions for later.
12. For non-conversational AI products, default to avoiding Claude / ChatGPT-style sidebar chat shells, narrow-center conversation layouts, and the same neutral chat color shell unless the UI plan explicitly justifies it.
13. UI implementation must use the recommended component ecosystem/design token direction from `output/*-uiux.md`, not switch ad hoc.


## Coding Constraints (active during ALL coding phases)

These rules apply every time you write or edit a file:

### Tech Stack Pre-Research
- Before writing ANY code, run `cat package.json` (or equivalent) to check framework versions.
- If unsure about an API, use WebFetch to read official docs first. Never guess.

### Icon & Visual Rules
- Icons MUST come from a declared icon library (Lucide/Heroicons/Tabler). No emoji as icons.
- No purple/pink gradient themes. No default system font only.

### Frontend/Backend Alignment
- Frontend fetch URLs must exactly match backend route definitions.
- Define API paths as shared constants when possible.

### Per-File Self-Check
- Before writing each file: correct imports, no emoji, colors from tokens only.
- After completing a feature, run build + lint. Fix errors before moving on.

## Super Dev System Flow Contract
- SUPER_DEV_FLOW_CONTRACT_V1
- PHASE_CHAIN: research>docs>docs_confirm>spec>frontend>preview_confirm>backend>quality>delivery
- DOC_CONFIRM_GATE: required
- PREVIEW_CONFIRM_GATE: required
- HOST_PARITY: required
<!-- END SUPER DEV OPENCODE -->






<!-- BEGIN SUPER DEV QODER -->
# Super Dev IDE Rules (qoder)

## Positioning
- Super Dev is a host-level workflow governor, not an LLM platform.
- Keep using the host's model capabilities; do not expect extra model APIs from Super Dev.
- The host remains responsible for actual coding, tool execution, and file changes.

## Runtime Contract
- Treat Super Dev as the local Python workflow tool plus this host rule file, not as a separate coding engine.
- When the user says `/super-dev ...`, `super-dev: ...`, or `super-dev：...`, immediately enter the Super Dev pipeline.
- When the user says `/super-dev-seeai ...`, `super-dev-seeai: ...`, or `super-dev-seeai：...`, enter the SEEAI competition-fast contract.
- Use host-native browse/search/web for research and host-native editing/terminal for implementation.
- Use local `super-dev` commands when you need to generate or refresh documents, spec artifacts, quality reports, or delivery manifests.

## First-Response Contract
- On the first reply after a host-supported Super Dev entry (for example `/super-dev ...`, `$super-dev`, `super-dev: ...`, `super-dev：...`, `/super-dev-seeai ...`, `$super-dev-seeai`, `super-dev-seeai: ...`, or `super-dev-seeai：...`), explicitly state that the matching Super Dev mode is now active rather than normal chat mode.
- If the repository already contains `super-dev.yaml`, `.super-dev/WORKFLOW.md`, `output/*`, `.super-dev/review-state/*`, or an unfinished run state, the first natural-language requirement in a new host session must also default to continuing Super Dev rather than plain chat.
- Before the first reply, read `.super-dev/WORKFLOW.md` and `output/*-bootstrap.md` when present, and treat them as the explicit bootstrap contract for this repository.
- The first reply must explicitly state that the current phase is `research`, and that you will read `knowledge/` plus `output/knowledge-cache/*-knowledge-bundle.json` first when available before similar-product research.
- In standard mode, the next sequence is research -> three core documents -> wait for user confirmation -> Spec / tasks -> frontend first with runtime verification -> backend / tests / delivery.
- In SEEAI mode, the next sequence is research -> compact competition docs -> wait for user confirmation -> compact Spec -> full-stack sprint -> polish / handoff.
- Both modes must explicitly promise that they will stop after the three core documents and wait for approval before creating Spec or writing code.

## Local Knowledge Contract
- Read relevant files under `knowledge/` before drafting the three core documents.
- If `output/knowledge-cache/*-knowledge-bundle.json` exists, read it first and inherit its matched local knowledge into PRD, architecture, UIUX, Spec, and execution.
- Treat local knowledge hits as hard project constraints, especially for standards, anti-patterns, checklists, and scenario packs.

## Conversation Continuity Contract
- If `.super-dev/SESSION_BRIEF.md` exists, read it before responding and treat it as the active workflow state.
- If the workflow is waiting for docs confirmation, preview confirmation, UI revision, architecture revision, or quality revision, then user replies like `修改`, `补充`, `继续改`, `确认`, `通过`, `继续`, or detailed feedback remain inside the current Super Dev stage.
- After each requested revision inside a gate, stay in the same stage, update the required artifacts, summarize what changed, and wait again for explicit confirmation.
- Do not silently exit Super Dev mode because the user asked for several edits, follow-up questions, or extra constraints.
- Only leave the current Super Dev workflow if the user explicitly says to cancel the workflow, restart from scratch, or switch back to normal chat.

## Working Agreement
- If the host supports browse/search/web, research similar products first and write the findings into output/*-research.md.
- Generate PRD, architecture and UIUX documents before coding, write them into output/* files, then pause and ask the user to confirm the three documents.
- In SEEAI mode, keep the same document gate, but compress the documents and go straight from Spec into one integrated full-stack sprint without a separate preview gate.
- If the user requests revisions, update the documents first and ask again; do not create Spec or code before confirmation.
- If the user requests a UI redesign or says the UI is unsatisfactory, first update `output/*-uiux.md`, then redo the frontend, and rerun frontend runtime + UI review before continuing.
- If the user requests architecture changes, first update `output/*-architecture.md`, then realign tasks and implementation before continuing.
- If the user requests quality or security remediation, first fix the issues, rerun quality gate, refresh delivery evidence, and only then continue.
- Respect Spec tasks sequence.
- Implement and run the frontend before moving into backend-heavy work.
- Keep architecture and UIUX consistency.

## Delivery Criteria
- Frontend can be demonstrated early.
- Backend and migration scripts match specs.
- Security/performance checks are resolved.
- Quality gate threshold is met for the current scenario.
- UI must avoid AI-looking output (purple/pink gradient-first theme, emoji as icons, default-font-only pages).
- Before any UI implementation, lock the icon library, typography, design token system, component ecosystem, and page skeleton from `output/*-uiux.md`.
- Do not use emoji as functional icons or placeholders.
- For non-conversational AI products, avoid Claude / ChatGPT-style sidebar chat shells unless the UI plan explicitly justifies it.
- UI must define typography, design tokens, grid, component states and trust signals before page implementation.
- Prefer the component ecosystem and design token baseline recommended in output/*-uiux.md instead of switching UI libraries ad hoc.


## Coding Constraints (active during ALL coding phases)

These rules apply every time you write or edit a file:

### Tech Stack Pre-Research
- Before writing ANY code, run `cat package.json` (or equivalent) to check framework versions.
- If unsure about an API, use WebFetch to read official docs first. Never guess.

### Icon & Visual Rules
- Icons MUST come from a declared icon library (Lucide/Heroicons/Tabler). No emoji as icons.
- No purple/pink gradient themes. No default system font only.

### Frontend/Backend Alignment
- Frontend fetch URLs must exactly match backend route definitions.
- Define API paths as shared constants when possible.

### Per-File Self-Check
- Before writing each file: correct imports, no emoji, colors from tokens only.
- After completing a feature, run build + lint. Fix errors before moving on.

## Super Dev System Flow Contract
- SUPER_DEV_FLOW_CONTRACT_V1
- PHASE_CHAIN: research>docs>docs_confirm>spec>frontend>preview_confirm>backend>quality>delivery
- DOC_CONFIRM_GATE: required
- PREVIEW_CONFIRM_GATE: required
- HOST_PARITY: required
<!-- END SUPER DEV QODER -->







