---
name: social-health
description: Run a comprehensive health check on social media infrastructure, posting cadence, and engagement metrics.
disable-model-invocation: true
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
argument-hint: [full|quick|infra]
---

# Social Health Check: $ARGUMENTS

Comprehensive health check of the social media system.

## Modes

### `/social-health quick` (or no argument)
Fast status overview:
1. Run `bash System/Cron/post-log-summary.sh` — posting cadence
2. Read `System/Social/queue.md` — pending drafts count
3. Read `System/Social/trends.md` — freshness of trend data
4. Quick summary: posts this week, cadence compliance, pending items

### `/social-health full`
Deep analysis:
1. Run `bash System/Cron/platform-health.sh --verbose` — infrastructure check
2. Run `bash System/Cron/post-log-summary.sh` — posting metrics
3. Run `bash System/Cron/engagement-pull.sh` — engagement status
4. Spawn **social-audience-analyst** agent for metrics analysis
5. Spawn **social-competition-monitor** agent for competitive landscape
6. Generate comprehensive report

### `/social-health infra`
Infrastructure only:
1. Run `bash System/Cron/platform-health.sh --verbose`
2. Verify all social agents exist in `.claude/agents/`
3. Verify all hooks are wired in `.claude/settings.json`
4. Verify all playbooks exist in `.claude/social-media/playbooks/`
5. Verify all data files exist in `System/Social/`
6. Check credential files (existence, not contents)
7. Report any missing or misconfigured components

## Expected Files

### Agents (`.claude/agents/social-*.md`)
- social-strategist, social-trend-scout, social-hook-crafter
- social-content-adapter, social-cultural-translator
- social-community-builder, social-reply-miner
- social-visual-strategist, social-seo-discovery
- social-competition-monitor, social-audience-analyst

### Hooks (`.claude/hooks/social-*.sh`)
- social-brand-voice-gate, social-context-injector
- social-post-logger, social-quality-gate
- social-orphan-draft-catcher, social-engagement-alerter
- social-calendar-reminder

### Data Files (`System/Social/`)
- calendar.md, post-log.md, queue.md
- engagement.md, audience.md, trends.md

### Scripts (`System/Cron/`)
- social-post.sh, platform-health.sh
- engagement-pull.sh, post-log-summary.sh

### Playbooks (`.claude/social-media/playbooks/`)
- reddit.md, bluesky.md, x-twitter.md
- pinterest.md, youtube.md
