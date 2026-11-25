---
name: aevatar-skill-loading
description: "Load authoritative NyxID/Ornn manuals and domain skills via use_skill before platform-specific work, and proactively discover skills (ornn_search_skills) when the user names a skill or a task needs specialized capability."
version: "1.1"
metadata:
  category: plain
  tag:
    - aevatar
    - aevatar-system
    - nyxid
    - ornn
    - skill-loading
    - use-skill
    - overlay-scope-global
---

### Loading NyxID and Ornn manuals via use_skill

The NyxID and Ornn user manuals live on the Ornn skill platform, not in the kernel, so curators can update them without redeploying the bot. You learn the canonical, up-to-date usage by loading the relevant skill.

**Before doing any of the following, call `use_skill(skill="nyxid")` first** to load the authoritative NyxID manual:
- Account / profile / MFA / sessions / consents
- Service catalog browsing, connecting a new service (OAuth / device-code / API key flows)
- API key, node, organization, approval, notification management
- Diagnosing NyxID error codes (`approval_required`, `unauthorized`, `node_offline`, etc.)
- Anything that would otherwise need `nyxid_account`, `nyxid_status`, `nyxid_profile`, `nyxid_mfa`, `nyxid_sessions`, `nyxid_catalog`, `nyxid_services`, `nyxid_endpoints`, `nyxid_external_keys`, `nyxid_api_keys`, `nyxid_nodes`, `nyxid_approvals`, `nyxid_notifications`, `nyxid_providers`, `nyxid_orgs`, `nyxid_admin`, or `nyxid_proxy`

**Before driving the Ornn API directly via the AI Agent CLI, call `use_skill(skill="ornn-agent-manual-cli")`** to load the Ornn agent manual.

`use_skill` loads remote instructions with the current NyxID token on each call; do not assume another user's previous skill load is visible or reusable.

### Proactive skill discovery

When the user mentions a named skill or asks for a specialized capability (translation, summarization, network/device inventory, scraping, scheduling, content drafting, code review, domain workflows, etc.), call `ornn_search_skills` to find a matching skill and then `use_skill` to load it. Treat the loaded skill's instructions as authoritative for that task.

When you are following a loaded skill and you hit a missing capability, ambiguous workflow step, unavailable service, unknown file/source layout, missing API contract, repeated tool failure, or any other "I cannot solve this from the current instructions" state, you MUST call `ornn_search_skills` with the concrete blocker/task and then `use_skill` the best matching result before trying generic `nyxid_proxy`, repository searching, or free-form API guessing. Do not narrate the blockage as progress; load the next skill and continue.

Triggers:
- User quotes a skill name (`'translate-pro'`, `"sg-office-network"`)
- User uses a slug-like or Title Case identifier that could be a skill name
- User issues a `/<command>` slash command that isn't an in-tree relay command (the in-tree ones are `/route`, `/models`, `/model`, `/agents`, `/agent-status`, `/run-agent`, `/disable-agent`, `/enable-agent`, `/delete-agent`) — treat the command name as the skill query (`/invoice` → search "invoice")
- User says "挂载/mount/use/load this skill" or names a domain workflow

Only fall back to `nyxid_proxy` / generic API discovery when no skill matches.

Quick reference:
- **Search**: `ornn_search_skills` — keywords or skill name (omit to browse); always searches every skill you can use (your own + public + shared via your org/team)
- **Activate**: `use_skill skill="<name>"` — loads instructions + associated files
- **Follow**: once loaded, the skill's instructions take precedence over generic guidance for that task
