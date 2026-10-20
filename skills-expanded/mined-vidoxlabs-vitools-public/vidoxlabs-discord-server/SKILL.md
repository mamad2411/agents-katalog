---
name: vidoxlabs-discord-server
description: Use for creating, configuring, or maintaining the Vidoxlabs public Discord server, Vibot bot, L0-L3 role tiers, channel categories, GitHub sync, and community interest features. Activate when user mentions Discord server setup, Vibot, L0 L1 L2 L3 tiers, public community platform for Vidoxlabs, or related planning.
---

# Vidoxlabs Discord Server + Vibot Skill

**Purpose**: Equip the agent with canonical knowledge, templates, and procedures to build and operate the Vidoxlabs Discord server as a compartmentalized, interest-generating hub aligned with Vidoxlabs architecture (VIs, LAs, ARKSRRA, L0-L3 tiers, Agentic Data Sovereignty).

**When to Load**: Any task involving Discord server design, role/permission setup, Vibot implementation, community onboarding, or cross-sync with GitHub/vidoxlabs.dev/ViDocs.

**Core Principle**: The server **mirrors Vidoxlabs compartmentalization**. Public L3 generates interest in v37 cluster, CRS, ViLabs Studio, Memorix, Violet Cabinet. Private tiers (L2 dev sync, L1 admin, L0 ops) enforce least-privilege. Vibot = specialized LA that executes; VIs (esp. Violet) ratify high-risk changes.

## Quick Start (After Loading This Skill)
1. Review current server state (user provides invite or screenshot; or use future Vibot `/server-audit`).
2. Load vilabs-project-management skill.
3. Check/create .plans/ entry for the work (date-based plan or projects/vidoxlabs-discord-server/).
4. Follow ARKSRRA pipeline in all decisions.
5. Use templates below for roles, channels, permissions.
6. All secrets via Infisical (never commit tokens).
7. Validate frontmatter/links before any "commit" equivalent (update NAVIGATION.md).

## L0-L3 Tier Model (Authoritative)
- **L3 Public** (@everyone + optional @Verified): Read public channels, post in limited places after verification. Funnel for interest → contributions.
- **L2 Contributor** (@L2-Contributor): Private L2 category (dev discussions + GitHub-synced channels). Can moderate public. Grant after contribution or L1 approval. Cross-sync Discord ↔ GitHub ↔ (future) vidoxlabs.dev.
- **L1 Admin** (@L1-Admin): Discord management rights (roles/channels in public+L2), L1 private category. Reports to L0.
- **L0 Admin/Ops** (@L0-Admin, @L0-DevOps): Full access including L0 private ops category. Equivalent to Violet office. Destructive actions require explicit ratification (HITL or Violet simulation).

**Role Hierarchy (Discord UI order top-to-bottom)**: @L0-DevOps > @L0-Admin > @L1-Admin > @L2-Contributor > @Verified > @everyone (L3)

**Colors** (Vidoxlabs theme): L0 deep violet (#4B0082), L1 indigo, L2 teal, L3/public light gray or accent.

## Recommended Server Structure

### Public Category (L3+ visible, everyone can read; verified can post in select)
- #rules (pinned: server rules, tier explanation, verification process, links to GitHub/vidoxlabs.dev)
- #welcome (Vibot embed + onboarding DM trigger)
- #announcements (existing public-announcements enhanced; curated updates from CRS, v37, agents)
- #introductions (new members post here)
- #project-showcase (screenshots, wins from v37, CRS consolidation (914 vilabs_cli tests), ViLabs Studio, Memorix)
- #contribute (GitHub links, issue templates, local setup, how L2 access earned)
- #v37-cluster (infra updates, node status summaries — no secrets)
- #crs-updates (Cluster Relations Systems news, vilabs_cli.crs)
- #violet-cabinet (spotlight on VIs: Violet, Wisteria, Xylia, Yarrow, Zinnia; scheduled AMAs)
- #ama (Ask Me Anything — Vibot schedules or routes to appropriate VI context)
- #off-topic (community building)

### L2 Private Category (L2+ only)
- #l2-dev-general
- #l2-github-sync (Vibot posts curated GitHub issues/PRs from vilabs/*; discussion)
- #l2-moderation (reports, mod actions log)
- #l2-vibot-ops (Vibot logs, command usage, config discussion)

### L1 Private Category (L1+)
- #l1-admin-general
- #l1-discord-config (planning channel/role changes)
- #l1-user-management (verification queue, role grants)

### L0 Private Category (L0 only — highest compartmentalization)
- #l0-ops-general
- #l0-secrets-rotation (references Infisical only; DLP redacted)
- #l0-cluster-coordination (v37 links, high-level ops — no creds)
- #l0-vibot-admin (full bot control; actions still require Violet ratification for destructive)

**Vibot Role**: Separate role with scoped permissions (Manage Roles, Manage Channels, Send Messages, Embed Links, Read Message History — minimal). Never give Administrator. Vibot reports to L0/L1.

## Vibot as Lab Assistant (LA)
Vibot is the **Discord-domain LA**. 
- Never makes high-level strategic decisions (that's VIs / Violet Cabinet).
- Executes delegated tasks: role grants, channel sync, logging, basic moderation, GitHub relay.
- On destructive/high-risk (e.g. mass role change, channel delete): Must call `/violet-ratify` or equivalent and wait for confirmation before action.
- Supports temporal awareness: Track time since last GitHub sync, estimate task durations.
- Commands examples (slash):
  - `/vibot-help`
  - `/verify @user` or reaction-based
  - `/grant-role L2 @user` (L1+ only)
  - `/github-sync` (manual trigger for L2 relay)
  - `/arkrra-check` (report on recent decisions or server health)
  - `/server-audit` (future: read-only snapshot of roles/channels/permissions)
  - `/vi-docs-search <query>` (future MCP integration)
- Implementation: Python (discord.py) for alignment with vilabs_cli / vilabs_api / vilabs_mcp. Or Node if preferred for MCP. Store in new repo or vilabs_mcp/vitools/discord/.
- Secrets: Bot token + any API keys via Infisical (v37 secrets pull pattern). Rotate regularly.

## Step-by-Step Setup Procedure (Follow After Ratification)
**Phase 0 (Immediate)**:
1. In Discord: Create roles top-to-bottom per hierarchy.
2. Create categories with permission overwrites (L3 default = everyone read/send limited; L2 category default = L2+; etc.).
3. Move/enhance existing #public-announcements to #announcements. Pin rules + Vibot welcome embed.
4. Seed public channels with initial content from vidoxlabs-masternote.md (glossary, VIs overview, CRS success metrics, contribute links to GitHub).
5. Add Vibot (minimal perms). Test basic presence.
6. Document server invite + config snapshot in ViDocs + this skill's references/.

**Phase 1 (Vibot Core)**:
1. Scaffold Vibot (use la-agent-scaffold-author equivalent or manual).
2. Implement role management + logging commands.
3. Deploy to test server first → then production.
4. Configure GitHub webhooks (vilabs org) → L2 private channel or Vibot listener → curated public posts.
5. Add verification gate (reaction on #rules or form) → L1 manual approve → L2 grant.

**Phase 2+**:
- Expand Vibot with MCP/ViDocs search, temporal reporting.
- Link public channels to vidoxlabs.dev (when live).
- Periodic L0 permission audit (Vibot `/server-audit` + human review).
- Update .plans/NAVIGATION.md and mark plan completed.

## Templates (Copy & Customize)
**Role Create Template** (Discord UI or bot):
```
Name: L2-Contributor
Color: Teal
Permissions: View Channels, Send Messages, Read Message History, Add Reactions, Use External Emojis (no Manage anything)
```
Similar for others. L0 gets full but still scoped by category overwrites.

**Channel Permission Matrix** (high-level):
- Public channels: @everyone = View + Send (limited), @L2+ = full
- L2 category: @everyone = hidden, @L2+ = View + Send
- L0 category: @L0 only

**Onboarding DM from Vibot** (template):
"Welcome to Vidoxlabs! You are currently L3 (Public). To unlock L2 Contributor access (GitHub sync, dev channels): 
1. Read #rules and #contribute
2. Introduce yourself in #introductions
3. Make a contribution on GitHub (vilabs org) or request manual review.
Our VIs (Violet Cabinet) and LAs orchestrate everything. Questions? Use /ama or post in public."

## Security & Governance (Non-Negotiable)
- **NEVER** hardcode bot token or keys in code/markdown.
- Use Infisical + daily `v37 secrets pull` pattern.
- Vibot least-privilege always. Destructive commands require explicit ratification step (simulate Violet).
- Follow Operator Mutation Safety Contract from canon.
- DLP: Vibot redacts any accidental secret paste before logging/relay.
- Audit logs: Enable Discord audit log + Vibot mirror to L0 channel.
- Public interest first: All public content must be accurate, link back to canonical ViDocs/GitHub, avoid over-promising.

## Integration with Vidoxlabs Ecosystem
- **VIs / Violet Cabinet**: Violet = final ratifier for server changes. Wisteria = narrative in #violet-cabinet and public posts. Xylia = risk review of permissions. Yarrow = coherence of channel map. Zinnia = execution sequencing via Vibot.
- **LAs**: Vibot is the Discord LA. Other LAs (la-v37-*, la-code-quality-enforcer) can be delegated via Vibot mentions or future MCP.
- **ViDocs**: Server architecture doc lives in ViDocs. Vibot future command surfaces it.
- **Memorix / MCP**: Future — store Discord state snapshots, temporal analysis of community activity.
- **CRS / vilabs_cli**: L2 sync uses CRS patterns for reliable relay.
- **v37 Cluster**: Mentions in public channels link to docs; private L0 for ops coordination (no direct access from Discord).

## References & Assets (Load on Demand)
- `references/discord-channel-list.md` — Full detailed channel list with topics, permission notes.
- `references/vibot-command-spec.md` — Complete slash command spec + example responses.
- `references/permission-matrix.csv` or md table (detailed overwrites).
- `assets/server-icon.png`, `assets/role-icons/` (future — Vidoxlabs branding).
- `assets/welcome-embed.json` (Discord embed template for #welcome).
- Master source: vidoxlabs-masternote.md (VIs, LAs, ARKSRRA, glossary, architecture canon).
- Plan: .plans/superpowers/plans/2026/06/18/2026-06-18-vidoxlabs-discord-server-skill.md

## Validation Before Changes
Run (when scripts exist):
- python scripts/validate-frontmatter.py (for any new .plans/ docs)
- Manual review of permission simulator in Discord.
- Vibot dry-run in test server.
- Xylia-style risk pass: "What if L2 role leaks to L3?"

## Anti-Patterns to Avoid
- Flat channel list without categories (loses compartmentalization).
- Over-permissioned bot or roles.
- Public channels with unverified sensitive discussion.
- Skipping ARKSRRA or Violet ratification for structural changes.
- Hardcoding secrets or committing .env with token.
- Treating Vibot as VI (it executes; does not orchestrate strategy).

---
**This skill is the single source of truth for Discord work in Vidoxlabs.** Update it when server evolves. All changes go through .plans/ process + NAVIGATION.md update.

*Maintained under Violet Cabinet governance. Zero-hallucination, evidence-backed.*
