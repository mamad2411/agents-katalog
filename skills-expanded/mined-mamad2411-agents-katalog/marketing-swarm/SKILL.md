---
name: marketing-swarm
description: Master trigger to deploy the 16-agent marketing team built in .agent/swarms/marketing_team/.
argument-hint: "deploy | brief <topic>"
allowed-tools:
  - Bash
  - Read
auto-invoke: false
model: default
context_trigger: "marketing campaign, launch, full marketing, 16-agent, marketing team, content calendar, multi-channel"
---

# Bionic Marketing Swarm

Orchestrates the activation of specialized marketing sub-agents (Copywriters, SEO analysts, Media Buyers) to execute comprehensive GTM distributions.

## Triggers

"marketing team", "deploy swarm", "reddit strategy", "seo campaign"

## Core Mechanics

1. Ingests a raw `<topic>` or URL.
2. Dispatches instructions to `.agent/swarms/marketing_team/` orchestrator.
3. Compiles final multi-channel assets (Ads, Landing Pages, Email Sequences).

## Reference Paths

- `.context/memories/protocols/marketing/338-multi-platform-content-flow.md`
- `.context/memories/protocols/marketing/280-meta-ads-architecture.md`
