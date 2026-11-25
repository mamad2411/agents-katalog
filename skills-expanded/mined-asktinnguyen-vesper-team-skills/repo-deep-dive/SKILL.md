---
name: repo-deep-dive
description: This skill should be used when users want to deeply analyze a GitHub repository (or local codebase) to extract architecture, design patterns, conventions, and implementation knowledge. It produces structured output compatible with the skill-creator skill, enabling transformation of any repo's knowledge into a repeatable design pattern skill. Triggers on requests like "analyze this repo", "extract patterns from this codebase", "create a skill from this repo", or "deep dive into this project".
---

<objective>
Perform comprehensive analysis of a GitHub repository or local codebase, extracting architecture, design patterns, conventions, and implementation knowledge into structured reference files. Output is formatted for direct consumption by the skill-creator skill to produce repeatable design pattern skills.
</objective>

<essential_principles>
## Core Philosophy

**Evidence-based extraction:** Every pattern, convention, and architectural decision documented must include `file:line` references back to the source code. No speculation — only what the code demonstrates.

**Progressive depth:** Start with broad reconnaissance (directory structure, config files, README), then drill into architecture, patterns, conventions, and features in parallel. Synthesize last.

**Skill-creator compatibility:** All output follows the skill-creator spec — YAML frontmatter with `name` and `description`, XML body tags, progressive disclosure via references, imperative writing style.

**Shallow clone first:** Use `--depth 1` for initial analysis. Only fetch full history when git log analysis or blame is specifically needed.

**Parallel analysis:** Phase 2 launches 5 independent Task agents simultaneously for comprehensive coverage without redundancy.
</essential_principles>

<intake>
What repo do you want to analyze?

Provide one of:
- **GitHub URL** — `https://github.com/owner/repo` or `owner/repo`
- **Local path** — `/path/to/repo` or `.` for current directory
- **PR/branch** — analyze a specific branch or PR's changes

Options:
1. **Full analysis** — Complete 5-phase deep dive (architecture + patterns + conventions + features + skill package)
2. **Architecture focus** — Deep dive into system architecture only
3. **Pattern extraction** — Extract design patterns and conventions only
4. **Generate skill package** — Produce skill-creator-ready output from analysis

**Specify a number, a repo, or both.**
</intake>

<routing>

| Response | Workflow to Load |
|----------|-----------------|
| 1, full, full analysis, deep dive, analyze | [full-analysis.md](./workflows/full-analysis.md) |
| 2, architecture, arch, system design | [architecture-focus.md](./workflows/architecture-focus.md) |
| 3, pattern, patterns, conventions, extract | [pattern-extraction.md](./workflows/pattern-extraction.md) |
| 4, generate, skill, package, output | [generate-skill-package.md](./workflows/generate-skill-package.md) |
| Just a repo URL/path (no option specified) | Default to [full-analysis.md](./workflows/full-analysis.md) |

**After selecting a workflow, read it and follow its procedures.**

</routing>

<reference_index>
## Reference Files

Load these as needed during analysis:

| File | Purpose |
|------|---------|
| [analysis-checklist.md](./references/analysis-checklist.md) | Priority file reading order and analysis dimensions |
| [pattern-catalog.md](./references/pattern-catalog.md) | Catalog of design patterns to identify |
| [tech-stack-detection.md](./references/tech-stack-detection.md) | Framework and language detection matrix |
| [output-architecture.md](./references/output-architecture.md) | Template for generated architecture.md |
| [output-patterns.md](./references/output-patterns.md) | Template for generated patterns.md |
| [output-conventions.md](./references/output-conventions.md) | Template for generated conventions.md |
| [output-features.md](./references/output-features.md) | Template for generated features.md |
| [output-skill-template.md](./references/output-skill-template.md) | Template for generated SKILL.md |

## Scripts

| Script | Purpose |
|--------|---------|
| [analyze-repo.sh](./scripts/analyze-repo.sh) | Initial reconnaissance — directory tree, file counts, config detection |

</reference_index>

<output_format>
## Generated Output Structure

The final output is a complete skill directory:

```
repo-knowledge-{repo-name}/
├── SKILL.md                    # Pre-populated with extracted principles, routing, conventions
├── references/
│   ├── architecture.md         # System overview, component catalog, data flow, ADRs
│   ├── patterns.md             # Design patterns with generic + source-specific examples
│   ├── features.md             # Feature catalog, implementation recipes, extension points
│   ├── conventions.md          # Naming, file org, error handling, testing conventions
│   └── implementation-guide.md # "How to build a similar system" step-by-step
└── assets/templates/           # Component/module/test templates in repo's style
```

This output can be fed directly into skill-creator: "Create a skill from repo-knowledge-{repo-name}/"
</output_format>

<success_criteria>
Analysis is complete when:
- Tech stack is identified with evidence (config files, imports, dependencies)
- Architecture is mapped with component boundaries and data flow
- At least 5 design patterns are identified with file:line references
- Naming conventions are extracted with 3+ examples each
- File organization patterns are documented
- Error handling strategy is identified
- Testing patterns are documented (framework, organization, coverage approach)
- Output package passes skill-creator validation (valid YAML frontmatter, XML tags, imperative style)
- Every extracted pattern has source code evidence
</success_criteria>
