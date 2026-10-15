---
name: library-deep-dive
description: >
  Performs a deep-dive research audit on a single library to determine whether the project
  uses it to its FULL potential. Use this skill when the user asks "are we using X to the max",
  "are we fully leveraging <library>", "deep dive into <library>", "library utilization audit",
  "library adoption review", "library maximization", "are we using <library> correctly",
  "what features of <library> are we missing", "library capabilities audit", "library usage review",
  "do we use <library> to its full potential", or any question about whether a specific dependency
  is underutilized, misused, or behind on features. Also triggers when the user names a library
  (e.g. Prisma, Zod, GORM, sqlc, Effect, RxJS, gorilla/mux, cobra, viper, react-query, zod, drizzle,
  typeorm, ent, elm, dayjs, lodash, immer, zustand, effector) and wants to know if they're getting
  the most out of it. Fires for ANY language and ANY library — JS/TS, Go, Rust, Python, Ruby, etc.
metadata:
  tags: library, dependency, utilization, adoption, audit, deep-dive, research, maximization, coverage, gap-analysis
allowed-tools: bash view edit write ls grep agent agentic_fetch mcp_context7_resolve-library-id mcp_context7_query-docs
---

# Library Deep Dive

Determines whether a project uses a **single specific library** to its full potential. The output is a deep, evidence-backed research report — not a surface scan — delivered as a self-contained, beautifully designed HTML file.

## Why This Matters

Most projects adopt a library for one or two features and never explore the rest. A team pulls in `zod` for simple validation and misses schema composition, discriminated unions, and branded types. They add `gorm` for basic CRUD and miss hooks, custom datatypes, batch operations, and the session API. Every library ships a far larger feature surface than anyone discovers by accident.

Underutilization has real costs: hand-rolled code that duplicates built-in functionality, worse performance because the library's optimized path was never used, and a stale version because nobody knows what newer features would unlock. This skill closes that gap by systematically comparing what the project _does_ with everything the library _offers_.

The deliverable is a point-in-time research report — a snapshot read by humans, never edited again — so it gets the full HTML treatment, not Markdown.

## Inputs

The user names a library (e.g. "deep dive into Zod", "are we using GORM to the max"). From that:

1. **Identify the library** in the project's dependency files (`package.json`, `go.mod`, `requirements.txt`, `Cargo.toml`, `Gemfile`, `pom.xml`, `build.gradle`, etc.).
2. **Capture the exact version** installed — version currency is part of the assessment.
3. If the library is not found in any dependency file, stop and report that to the user with the files checked.

## Process

READ, UNDERSTAND, RESEARCH, REFLECT before each phase. The depth of research is the entire point — do not shortcut it.

### Phase 1: Project Discovery — Understand Current Usage

Catalog exactly how the project uses the library today. This is the baseline for the gap analysis.

1. Find every file that imports or references the library (use `grep`/`rg` across the codebase).
2. Enumerate the **touched API surface**: which functions, classes, methods, hooks, middleware, config options, types, and utilities are actually called.
3. Map the **usage patterns**: How is it configured? Is it wrapped in an adapter? Extended? Used raw? Are there custom layers on top?
4. Record **configuration**: What options are set? What's left at defaults?
5. Note any **workarounds or hand-rolled code** near library usage — these often duplicate functionality the library already provides.

For the complete discovery checklist (per language), load [./references/research-methodology.md](./references/research-methodology.md).

### Phase 2: Capability Research — Understand the Full Potential

This is the core of the deep dive. The goal is to build an exhaustive map of what the library _can_ do, so nothing is missed. Use every research tool available — do not rely on training data alone, which is frequently outdated or incomplete.

1. **Resolve the library** via the Context7 MCP (`mcp_context7_resolve-library-id`) and query its documentation (`mcp_context7_query-docs`) for:
   - The full API surface and configuration options
   - Advanced patterns and recommended usage
   - Migration guides and version-specific features
2. **Fetch official docs** via `agentic_fetch` for topics Context7 doesn't cover deeply — especially configuration reference, middleware/hooks/plugins, performance tuning, and lesser-known features.
3. **Search for best practices and anti-patterns** via `agentic_fetch` — community guides, "tips and tricks", "advanced usage", "common mistakes with <library>".
4. **Check the changelog / release notes** for the installed version and newer versions. What features were added that the project may not know about? Are they behind on a major version?
5. **Enumerate these capability categories** for every library:

| Category                         | What to Look For                                                                   |
| -------------------------------- | ---------------------------------------------------------------------------------- |
| Core API                         | All public functions, classes, methods — not just the ones used                    |
| Configuration                    | Every option, flag, and tunable — many projects leave powerful options at defaults |
| Middleware / Hooks / Plugins     | Extension points the library offers for customization                              |
| Advanced / Lesser-Known Features | Features buried in docs that solve real problems                                   |
| Performance Features             | Caching, batching, streaming, lazy loading, pooling, connection management         |
| Type Safety / DX Features        | Type inference, schema validation, codegen, autocomplete enhancements              |
| Integrations                     | Official adapters, plugins, or compatibility layers for other tools                |
| Testing Utilities                | Built-in test helpers, mocks, fakes, fixtures                                      |
| Error Handling                   | Structured errors, error codes, recovery patterns                                  |
| Observability                    | Logging, metrics, tracing, debug modes the library supports                        |

For the detailed research framework with tool sequencing and search strategy, load [./references/research-methodology.md](./references/research-methodology.md).

### Phase 3: Gap Analysis — Compare Usage vs Potential

For every capability the library offers, determine the project's adoption status. This is where the research pays off — each finding must cite evidence (where in the codebase, or where in the docs).

Grade each capability:

| Status                     | Meaning                                                  | Visual                               |
| -------------------------- | -------------------------------------------------------- | ------------------------------------ |
| **Fully Leveraged**        | Used correctly and optimally — nothing to improve        | 🟢 `.card-solution` / `.score-good`  |
| **Partially Used**         | Used, but a more powerful built-in path exists           | 🟡 `.card-warning` / `.score-warn`   |
| **Missed Opportunity**     | Powerful feature not used at all — high potential impact | 🔴 `.card-problem` / `.score-bad`    |
| **Misused / Anti-Pattern** | Used against best practices — actively harmful           | ⚠️ `.card-problem` + warning callout |
| **Not Applicable**         | Feature exists but doesn't apply to this project's needs | ⚪ muted / excluded from scoring     |

Every "Partially Used", "Missed Opportunity", and "Misused" finding must include:

- **What the library offers** (the capability, with a doc reference)
- **What the project does instead** (the current code, with file:line citation)
- **The impact** — what improves by adopting it (performance, correctness, less code, better DX)
- **A concrete code example** showing the recommended usage

### Phase 4: Scoring & Prioritization

Synthesize the gap analysis into an actionable assessment.

1. **Adoption Score** (0–100): weighted by impact, not just count. A missed performance feature weighs more than an unused convenience helper.
2. **Version Currency**: Is the project on the latest? How many minor/major versions behind? What notable features are in the gap?
3. **Top Opportunities**: Rank all findings by (impact × ease) — the Pareto set that delivers the most value for the least effort.
4. **Risk Assessment**: Are any usages actively dangerous (deprecated APIs, known security issues, footguns)?

### Phase 5: Write the HTML Report

Write a self-contained, zero-dependency HTML file.

**Output path:** `docs/research/<YYYY-MM-DD>_<library-name>-deep-dive.html`

Use `date` CLI for the filename date. Use kebab-case for the library name.

1. Load the shared design system: [./assets/html-report-kit/references/html-output-guide.md](./assets/html-report-kit/references/html-output-guide.md)
2. Start from the **editorial light** template (best for long-form research findings): [./assets/html-report-kit/assets/report-template-editorial.html](./assets/html-report-kit/assets/report-template-editorial.html)
3. For the report-specific section structure, content guidance, and component mapping, load [./references/output-guide.md](./references/output-guide.md)
4. Write the full report with real evidence — every claim cited to code or docs.

### Phase 6: Cross-Skill References

After the report, consider which related skills add value:

- If the library is Go and the project needs better type safety around it → `data-model-review`
- If hand-rolled code duplicates library functionality → `deduplicate-code`
- If the codebase needs a broader quality pass → `code-quality-scan` or `full-code-review`

### Phase 7: Git Workflow

1. Run `git status` to verify what changed.
2. Stage the report: `git add docs/research/<file>.html`.
3. Commit with a VERY DETAILED message describing the library reviewed, the adoption score, key findings, and missed opportunities.
4. Push with `git push`.

## Execution

READ, UNDERSTAND, RESEARCH, REFLECT.
Break this down into multiple actionable steps. Think about them again.
Execute and Verify them one step at a time.
Repeat until done. Keep going until everything works and you think you did a great job!
