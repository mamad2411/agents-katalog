---
description: Conventions for the core pipeline and orchestration layer
globs: src/marketmenow/core/**
alwaysApply: false
---

# Core Pipeline Rules

## Platform Agnosticism

This package must never import from `src/adapters/` directly. The exceptions are
`registry_builder.py` and `workflow_registry.py`, which use lazy imports inside
try/except blocks.

## Pipeline (`pipeline.py`)

`ContentPipeline.execute(content, platform)` runs four stages:
1. `ContentNormaliser.normalise()` — match/case on content type
2. `bundle.renderer.render()` — platform-specific transformation
3. `sanitise_text()` — strip em/en-dashes from all text fields (anti-AI-detection)
4. `bundle.uploader.upload_batch()` — media upload, refs stored in `extra._media_refs`
5. `bundle.adapter.publish()` (or `send_dm()` for DIRECT_MESSAGE)

## Orchestrator (`orchestrator.py`)

`Orchestrator.run_campaign(campaign)` validates targets against the registry,
then runs executable targets in parallel via `asyncio.gather`. Returns
`CampaignResult` with results and errors.

## Distributor (`distributor.py`)

`ContentDistributor.distribute(content, platforms=None)` resolves target platforms
from `DistributionMap` (or explicit override), intersects with registered adapters,
builds a `Campaign`, and delegates to `Orchestrator`.

## Registry Builder (`registry_builder.py`)

`build_registry()` calls `_try_<platform>()` for each adapter. Each function:
1. Lazy-imports the adapter's bundle factory and settings class
2. Constructs settings (reads env vars)
3. Builds the bundle and registers it
4. Catches all exceptions — missing config silently skips that platform

When adding a new adapter, add a corresponding `_try_yourplatform()` here.

## Workflow System (`workflow.py`, `workflow_registry.py`)

`Workflow` is a named sequence of `WorkflowStep` instances sharing a `WorkflowContext`.
Steps implement the `WorkflowStep` protocol: `name`, `description`, `execute(ctx)`.
The context carries `params` (CLI args) and `artifacts` (step outputs).

`build_workflow_registry()` auto-discovers built-in workflows from `workflows/` via
lazy imports. When adding a new workflow, add a `_try_register()` call here.

## Scheduler (`scheduler.py`)

In-process scheduler for timed campaign execution. Uses `ScheduleRule` from
`models/campaign.py`.
