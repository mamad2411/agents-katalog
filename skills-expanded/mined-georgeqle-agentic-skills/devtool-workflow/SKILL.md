---
name: devtool-workflow
description: Use only for developer-facing tools, libraries, SDKs, CLIs, APIs, and infrastructure products
type: planning
version: v0.3
required_conventions: [alignment-page]
invocation: orchestrator
context_intake: artifact_only
visual_tier: visual
---

# Devtool Workflow

Invoke as `$devtool-workflow`.

Use this skill when the project is primarily developer-facing.

## Process

1. Read `.agents/project.json` and confirm `project_type` is `devtool`.
2. If the devtool pack is not enabled, install it with `scripts/pack.sh install devtool` from this source checkout, or `npx skillpacks install devtool` from the project shell when using the published package.
3. Route research through developer workflow, integration, DX, adoption, positioning, monetization, and docs checks.

## Output

Recommend the next single devtool-pack skill to run and explain the missing artifact or decision that makes it next. In the final response, include `Recommended next skill: <command>` using the `## Next-Skill Routing` rules below.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/devtool-workflow-{topic}.html`. By default, report results inline and write only this skill's normal durable artifacts; create an alignment page only when explicitly requested or when a concrete clarification/review need cannot be handled cleanly inline.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
