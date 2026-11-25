---
name: capability-composer
description: "Find the smallest set of skills, plugins, tools or outside discoveries that would do the current work better. Use when the user asks which skill or tool to use, asks for a capability scan of a project, wants every installed skill checked for update needs, wants product documentation compared with what a workspace actually uses, or asks Capability Composer to audit itself."
metadata:
  short-description: Find better capabilities for the work at hand
---

# Capability Composer

Build the smallest useful capability combination for the work in front of the user, without turning every task into a stack of overlapping skills.

## Settings and look

Before the first answer in a conversation, run `python3 scripts/composer_config.py` from this skill's folder (`py -3` on Windows) and follow what it prints. It resolves one optional JSON file: `CAPABILITY_COMPOSER_CONFIG`, then `.capability-composer.json` in the project, then `~/.config/capability-composer/config.json`. A missing or broken file gives the defaults; never stop because of it.

The settings decide how answers look and what a scan may use:

- `style`, `border`, `label`, `width`, `rings` and `maxSuggestions` shape the answer. Read [references/output-styles.md](references/output-styles.md) for how to produce each style. In Claude Code, when the `/capabilities` mod is installed, its own cards already draw the results; still follow `style` for any text answer.
- `webDiscovery: false` means no web search; say that discovery was skipped.
- `environment` is what discoveries must fit. When it is empty, describe the operating system and the project's stack yourself.
- `skillRoots` adds folders of `<skill>/SKILL.md` to consider. `exclude` names capabilities never to recommend. `stripPrefixes` are name prefixes to leave out when you write a capability's name.
- `routesFile` names the user's own route map; the bundled one is [references/capability-routes.json](references/capability-routes.json).

## Evidence boundary

The current session's skill and tool list is authoritative for what can be invoked. Skills found only on disk, in `skillRoots`, in a plugin cache or on the web are discovery evidence: name them honestly (for example "on disk, not loaded in this session") and never imply they are installed or callable.

## Scan active work on demand

When the user invokes Capability Composer for their project or asks which skills or tools could improve work in progress, read [references/on-demand-scan.md](references/on-demand-scan.md) and enter its task-local scan mode. Inspect the conversation, relevant project files and current work before recommending anything.

When the user describes a missing function and asks what product, service, library, plugin, CLI or other tool could provide it, or when a scan shows outside discovery is the next sensible step, also read [references/tool-discovery.md](references/tool-discovery.md). Keep discovery, adoption and skill-wrapping as separate decisions.

Scan mode is advisory until the user chooses a recommendation. It may continue across turns with controls such as **next**, **search for it**, **use it**, **wrap it as a skill**, **build it** or **stop**, but it never chains capabilities recursively within one turn and stops suggesting once scan mode closes. It must not install a tool or create a skill until the user approves that step.

## Scan the skill estate for update needs

When the user asks which skills need updates, requests a skill health check, or asks for an update scan, read [references/skill-update-scan.md](references/skill-update-scan.md) and run `scripts/scan_skill_updates.py`. This is a read-only, catalog-wide audit, not a project recommendation scan.

## Audit linked documentation against live state

When the user provides or names canonical documentation and asks to compare its possibilities with a workspace, repository, product or workflow, read [references/documentation-capability-audit.md](references/documentation-capability-audit.md). The audit is read-only and may recommend one smallest useful improvement round.

## Audit and improve Capability Composer itself

When the user asks to run Capability Composer against itself, audit it for gaps, or improve its behavior, read [references/self-improvement-mode.md](references/self-improvement-mode.md) and run `scripts/audit_capability_composer.py`. Self-audit is read-only by default; an explicit revision request allows one bounded edit-and-verify cycle.

## Compose or evolve a workflow

1. Read the target skill's `SKILL.md` completely and follow the direct references that affect the combination.
2. Separate responsibilities and compare session-available skills with on-disk and `skillRoots` candidates. Verify drift-prone external candidates against official sources.
3. Classify each relationship:
   - **required** only for an established invariant or user-approved gate;
   - **supporting** when the companion owns a distinct responsibility;
   - **alternative** when only one overlapping capability should be selected.
4. Present the proposed route and any skill edits before changing durable behavior: trigger, guard, rationale, availability, expected context cost, and the likely false-positive boundary.
5. After explicit approval, make the skill change (with a skill-authoring skill when one is available), update the route map, and run `scripts/test_hook_router.py` and `scripts/audit_capability_composer.py`.

## Routing quality

- Prefer explicit skill names and narrow intent phrases over broad keywords.
- Emit at most three matched routes and nothing when no approved route matches.
- Keep required companions distinct from suggestions and alternatives.
- Fail open: a missing or malformed route map or config never blocks or rewrites the user's prompt.
- Keep routing silent. Explain it only when it changes the approach, needs a choice, or the user asks why a capability was picked.
