---
name: tech-research
description: Research official documentation for technologies in a spec, generating actionable guides for implementation planning
---

# Tech Research

## Overview

After a spec document is created during brainstorming, use this skill to deeply research the official documentation of technologies mentioned in the spec. This generates a directly actionable technology guide including best practices, syntax, core patterns, and common pitfalls for specific use cases.

**Trigger:** User requests research, typically after spec approval in brainstorming.

**Output:** A comprehensive markdown document saved to `docs/superpowers/research/YYYY-MM-DD-<topic>-tech-research.md`

**Next step:** The generated guide feeds directly into writing-plans for implementation planning.

## When to Use

**流程:** brainstorming 创建 spec → 用户选择是否 research → 如是则执行研究 → 输出给 writing-plans

**Use when:**
- Spec mentions unfamiliar or complex technologies
- Need to verify current best practices before planning
- Team has limited experience with a technology in the spec
- Want to identify pitfalls early to avoid rework

**Skip when:**
- All technologies are well-understood by the team
- Time pressure requires immediate planning
- Spec covers only technologies the team masters

## Process

### Step 1: Extract Technologies from Spec

Read the spec document and identify all technologies, frameworks, libraries, and tools mentioned.

### Step 2: Resolve Versions from Current Project

**Important:** Do NOT use latest stable versions. Always check the project's actual installed versions first.

**npm packages:**
```bash
npm ls <package-name> --depth=0 | sed -n "s/.*<package-name>@([0-9.]*).*/\1/p"
```

**Python packages:**
```bash
pip show <package-name> | grep Version
```

**Docker images:**
```bash
docker images <image-name> --format "{{.Tag}}"
```

**Go modules:**
```bash
go list -m <module-name>
```

If a technology is not installed in the project, note it as "not currently in project" — research the version implied by the spec or latest stable if unspecified.

### Step 3: Dispatch Parallel Research Agents

For each technology (with resolved version), dispatch a parallel subagent research task. Group related technologies when they share documentation (e.g., React + React Hooks).

**Agent File:** `agents/tech-researcher.md`

**Dispatch:**
```typescript
Agent({
  description: `Research ${tech.name} for ${specTopic}`,
  prompt: readFile("agents/tech-researcher.md") + `\n\nInput:\n- TECHNOLOGY: ${tech.name}\n- PROJECT_VERSION: ${tech.resolvedVersion}\n- SPEC_USE_CASE: ${tech.purposeInSpec}\n- OUTPUT_PATH: docs/superpowers/research/temp-${tech.slug}.md`,
  subagent_type: "general-purpose",
  name: `researcher-${tech.slug}`
})
```

### Step 4: Parallel Research Collection

Spawn all research agents concurrently. Wait for all to complete before proceeding to synthesis.

**Monitoring:**
- Agents send messages on completion
- Track completion status per technology
- Handle any agent failures gracefully

### Step 5: Synthesize into Technology Guide

Merge all research into a single markdown document.

### Step 6: Cleanup

1. Remove temporary research files (merged into final guide)
2. Report completion to user

## Output Format Template

See `agents/tech-researcher.md` "Output Template" section for the complete template structure.

## Integration with Writing Plans

After research is complete:

> "Technology research complete and saved to `docs/superpowers/research/<filename>.md`. This guide covers [N] technologies with best practices, core patterns, and identified pitfalls.
>
> Ready to proceed with writing-plans, or would you like me to dive deeper into any specific technology?"
