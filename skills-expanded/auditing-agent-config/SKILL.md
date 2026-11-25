---
name: auditing-agent-config
description: Audits a Claude Code and/or Claude.ai configuration for redundancy, misplacement, and conflicts — across global (~/.claude) and project (.claude/) scopes, skills, plugins, CLAUDE.md/rules, subagents, hooks, and MCP/connector setup. Use this whenever the user wants to audit, review, clean up, reorganize, or sanity-check their Claude setup; mentions having "too many skills/plugins"; asks whether something should be global or project-level; suspects duplicate, conflicting, or overlapping skills; wants to know if their CLAUDE.md is too long or bloated; asks "why isn't skill X triggering"; or asks things like "audit my claude setup," "check my skills for overlaps," or "help me organize my Claude Code config." Trigger proactively any time the user is actively managing a nontrivial skill/plugin library (roughly 10+ skills or 3+ plugins) and starts talking about adding more.
---

# Claude Config Audit

A repeatable, read-only process for auditing everything Claude reads before it ever sees your prompt: CLAUDE.md files, rules, skills, plugins, subagents, hooks, and MCP servers — at both the global (`~/.claude`) and project (`.claude/`) scope, plus Claude.ai account skills/connectors if relevant.

The goal is not just an inventory. It's to catch the failure modes that accumulate silently as a setup grows: duplicate skills nobody remembers creating, several skills fighting to trigger at session start, a CLAUDE.md that's grown past the point of being read carefully, content sitting at the wrong scope, and installed things that are never actually used.

## Operating rule: read-only by default

This skill inspects config and produces a report. It does NOT move, delete, disable, or edit anything unless the user explicitly says to, per item, after seeing the report. Announce this up front. When the user does approve a change, make one change, confirm it, then move on — never batch-remove based on inference.

## Step 1: Figure out what you're auditing

Ask briefly (reasonable defaults are fine, don't block on every question):
- **Claude Code, Claude.ai, or both?** Most of this skill is Claude Code-specific (it has the richer scope model). If the user is on Claude.ai only, skip to the "Claude.ai scope" note in Step 2.
- **Which project(s)?** If auditing project scope, get the repo path(s). If they only want the global setup reviewed, skip project-specific steps.

**Environment check — do this before gathering.** If you (Claude) are running in a sandboxed environment without access to the user's real home directory (e.g. a claude.ai conversation with a container bash tool, rather than Claude Code on their machine), you cannot see their actual `~/.claude`. Say so plainly and ask the user to paste the command output from Step 2 — do NOT silently audit the sandbox's own skill library as if it were theirs. This is a real failure mode: the sandbox may share plugin *names* with the user's setup without sharing the actual inventory.

## Step 2: Gather — and reconcile your separate sources of truth

**This is the step that most needs care.** There is no single list of "your skills." What you see injected into a session is NOT the same as what's installed, and neither is the same as what's on disk. Recommending removal from the wrong list is the classic failure of this audit — you will confidently tell someone to delete things that aren't where you think they are. So gather every inventory and reconcile them before analyzing.

The sources of truth:

| Inventory | Authoritative source | What it contains |
|---|---|---|
| **Account skills** (Claude.ai / desktop app) | The Skills panel in the app, or Settings → Capabilities | Skills you uploaded to your account; sync to the desktop app |
| **Plugins** (and the skills they inject) | `/plugin list` (or `claude plugin list`) | Installed plugins; each can inject many skills under its namespace |
| **Local Code skills** | on disk at `~/.claude/skills/` (user) and `<project>/.claude/skills/` (project) | Filesystem skills you manage directly |
| **Account connectors** | Settings → Connectors in the app — NOT visible in any local file | MCP apps/integrations connected at the account level (Notion, Gmail, Figma, Drive, etc.) |

The trap: a session's injected skill list mixes all of these, and plugin-injected skills often appear under a namespace (e.g. `some-plugin:skill-name`) that makes them look like local skills you can delete with `rm` — you can't; they come back until the plugin is disabled. **Never recommend removing a skill until you've confirmed which inventory it actually lives in.**

The connector blind spot: account connectors appear as active tools in a session but exist in no file on disk — `~/.claude/mcp.json` and project `.mcp.json` won't show them. If you see active MCP tools that no local config explains, say so explicitly, name them as account-level connectors, and direct the user to review them in Settings → Connectors. Do not guess at their usage from disk — you can't.

Commands to gather (run them, or ask the user to paste output if you can't):

```bash
# Global scope — on disk
ls -la ~/.claude/
cat ~/.claude/CLAUDE.md 2>/dev/null
find ~/.claude/rules -type f 2>/dev/null
find ~/.claude/skills -maxdepth 2 -type f -name "SKILL.md" 2>/dev/null
find ~/.claude/agents -type f 2>/dev/null
find ~/.claude/commands -type f 2>/dev/null
cat ~/.claude/settings.json 2>/dev/null

# App state, plugin enable-flags, MCP servers, AND usage telemetry (see Step 3f).
# Extract only the keys we need. This never prints token/apiKey values, and —
# unlike a byte-truncation — it reaches skillUsage/pluginUsage, which sit near
# the END of a large ~/.claude.json (often past byte ~38k). Do NOT swap this for
# `head -c N`: that silently cuts off the very telemetry Step 3f depends on.
jq '{numStartups, skillUsage, pluginUsage, mcpServers: (.mcpServers // {} | keys)}' \
  ~/.claude.json 2>/dev/null
# Per-project enabled plugins + MCP servers (only projects that actually set them):
jq -r '.projects | to_entries[]
       | select((.value.enabledPlugins // {} | length > 0)
                or (.value.mcpServers // {} | length > 0))
       | {project: .key, enabledPlugins: .value.enabledPlugins,
          mcpServers: (.value.mcpServers // {} | keys)}' \
  ~/.claude.json 2>/dev/null
# No jq? Same extraction in Python:
#   python3 -c 'import json,os;d=json.load(open(os.path.expanduser("~/.claude.json")));import sys;print({k:d.get(k) for k in ("numStartups","skillUsage","pluginUsage")})'

# Project scope (from the project root)
cat CLAUDE.md 2>/dev/null || cat .claude/CLAUDE.md 2>/dev/null
cat CLAUDE.local.md 2>/dev/null
cat .mcp.json 2>/dev/null
find .claude -maxdepth 2 -type f \( -name "SKILL.md" -o -name "settings.json" \) 2>/dev/null
```

Interactive commands that show what's *actually* loaded (ask the user to run and paste — several are terminal-only and can't be run by an agent):

- `/context` — token budget by category; flags an oversized CLAUDE.md or MCP tool list immediately
- `/plugin list` — **the authoritative plugin inventory + enable status**
- `/mcp` — connected MCP servers and status
- `/memory` — which CLAUDE.md and rules files loaded, plus auto-memory
- `/hooks` — active hooks (this is how you catch a plugin firing something at SessionStart)
- `/doctor` — configuration diagnostics

**Claude.ai-only scope:** no filesystem. Work from the account Skills panel and the connected-connectors list, plus the memory / user-preferences settings if the user wants those reviewed.

## Step 3: Analyze

Go through each check. Skip what doesn't exist. For every removal/change you propose, you must be able to say which inventory the item lives in and how it's removed (see the layer model in Step 4).

### 3a. Duplicate or shadowing skills
Same name or near-identical purpose in more than one place. Watch specifically for a name that appears both as a plugin-injected skill and as something that looks local — that's usually one skill seen through two lenses, not a true duplicate. Precedence to know: project shadows global on name collision; a skill beats a command of the same name; plugin skills are namespaced to avoid collision.

### 3b. Competing "always-on" / session-start actors
The highest-value check. Look for everything that injects content at the start of every session: skills whose description says "use at the start of every session," `SessionStart` hooks (often from plugins), memory-injection systems, and auto-loaded memory files. These don't *conflict* (they stack), but each one costs context on turn one of every session, forever. List the full set, explain that the question is "how many session-start narrators do you need," and help the user decide which to keep — don't just flag it.

### 3c. Overlapping domain coverage
Multiple skills/plugins aimed at the same job (several UI/design skills, several code-review skills). Cross-reference with usage data (3f): overlap + zero use is a clear cut; overlap + real use is a conscious "do you want multiple angles" decision for the user.

### 3d. CLAUDE.md health
- Length: keep under ~200 lines; it loads in full every session, so bloat is a recurring token cost.
- Task-specific content that only matters sometimes belongs in a scoped `rules/*.md` (gated with `paths:` frontmatter) or a skill (loads on demand), not always-on in CLAUDE.md.
- Redundancy or contradiction between global and project CLAUDE.md — both load together.
- **Content quality, not just length:** CLAUDE.md is for *stable* facts (stack, durable conventions, how the user likes Claude to work). Anything volatile (current projects, this month's priorities, evolving decisions) belongs in memory, which updates itself — putting it in CLAUDE.md guarantees it goes stale. Also watch for facts stated more strongly than they're true (e.g. a market focus written as if it were the user's core expertise); precision here changes how Claude reasons.

### 3e. Scope misplacement
- **Global → should be project:** client-/repo-specific conventions or credentials sitting in the global file where they apply everywhere.
- **Project → should be global:** the user's own cross-project habits duplicated across several project files instead of stated once globally.
- **Not the user's to move:** cloned upstream repos often carry their own CLAUDE.md. Those aren't the user's config — don't fold them in or recommend editing them.

### 3f. Usage telemetry — a first-class check
`~/.claude.json` records usage counts (fields along the lines of plugin/skill usage and startup count). This is often the single most actionable evidence in the whole audit: a plugin with 0 uses across dozens of startups, or a skill that has never fired, is a concrete, defensible cut in a way that "this looks redundant" is not. Explicitly surface: never-used plugins, never-fired skills, and — for context — which items *are* earning their keep (name the high-use ones so the user knows what not to touch). Pair every stale-item flag with the usage number as evidence.

**Telemetry is a history, not an inventory.** Usage entries persist after the plugin or skill is uninstalled, so telemetry alone will list ghosts. Before calling anything "installed," cross-check the name against the actual installed registry (`~/.claude/plugins/` data dirs / plugin list command / on-disk skill folders). An entry that exists in telemetry but nowhere else is an orphan — report it as informational history ("was used N times, no longer installed, nothing to clean up"), never as an installed item to remove. Also note: recently uninstalled plugin directories may linger on disk for a grace period before auto-cleanup — a dir existing doesn't mean the plugin is installed either; the registry/enable state is the authority.

### 3g. MCP server scope and redundancy
- Servers connected but never referenced in the user's actual work — flag with a "does this earn its place" question, not an auto-cut.
- Servers at an odd scope (e.g. configured at home root so they load broadly).
- Important mechanic: for MCP, *disabling is not removing* — a disabled server can still inject its tool definitions into context. Reclaiming that context needs `claude mcp remove <name>`, not disable.

### 3h. Skill description quality
For user-authored skills, check the description against what actually drives triggering: does it name concrete trigger contexts, and is it specific enough not to fire on unrelated requests? The common failure is a verb list so broad ("plan, build, create, fix, review, improve...") that the skill wakes on nearly every request and collides with everything. Vague under-triggers; over-broad over-triggers.

### 3i. Gap analysis — what's missing, not just what's excess
An audit that only finds cruft tells a lean setup "all clean" and leaves value on the table. After the removal-side checks, look for absences that would concretely improve how Claude works for this user, grounded in what you actually observed (never generic boilerplate):

- **No global CLAUDE.md** but clear cross-project patterns exist (same stack, same conventions, same corrections appearing in memory or across project files) → recommend creating one, and say what specifically should go in it based on what you saw. Stable facts only — stack, durable conventions, working preferences.
- **No project CLAUDE.md in an actively-used repo** (signs: real git history, recent sessions there) → suggest one with that repo's conventions.
- **Repeated instructions that keep needing restating** (the same rule in multiple CLAUDE.md files, or memory entries correcting the same behavior) → that's a hook candidate: CLAUDE.md is advisory, hooks are guaranteed.
- **Knowledge that clearly should be a skill**: long how-to content sitting always-on in a CLAUDE.md, or workflows the user re-explains per session → suggest extracting into an on-demand skill.
- **Heavy use signals worth doubling down on**: if telemetry shows one skill or plugin doing most of the work, note it — it may deserve a global keybind/command, better description, or a project-scoped variant.
- **Missing hygiene**: no backups of config, secrets sitting in a CLAUDE.md instead of env vars, project config not in git for a team repo.

Each suggestion must cite the observed evidence that motivates it ("you have 6 project CLAUDE.md files all stating X → move X to global") — if you can't point at evidence in their config, don't suggest it. Suggesting is still read-only: propose, don't create, unless the user opts in per item.

## Step 4: Report

Short and scannable, not a wall of text. Findings ranked by impact first, then what's fine. Every removal recommendation must name which inventory the item lives in and how it's removed — use this layer model:

| Item type | Where it lives | How to remove/change it | Affects |
|---|---|---|---|
| **Account skill** | Your Claude.ai account | Skills panel in the app / Settings | Desktop app + claude.ai; syncs down |
| **Plugin** (and its injected skills) | Installed via a marketplace | `claude plugin disable <name>@<mkt>` (reversible) or `uninstall` | Claude Code (both CLI + desktop Local sessions) |
| **Local user skill** | `~/.claude/skills/<name>/` | Delete the folder, or set `disable-model-invocation` | All your Code projects |
| **Local project skill** | `<repo>/.claude/skills/<name>/` | Delete the folder | That one repo |
| **MCP server** | `~/.claude.json` or project `.mcp.json` | `claude mcp remove <name>` (disable ≠ remove) | Wherever it's scoped |
| **Hook** | a `settings.json` | Edit that settings file | Wherever it's scoped |

**Findings must be actionable.** A finding is something the user should *do something about*, ranked by how much doing it helps. If an item requires no action — an upstream repo's own CLAUDE.md, an uninstalled skill sitting inert in Downloads, telemetry residue from something already removed — it does not go in Findings. It goes in "No action needed," where it still shows the user what was checked without pretending to be a problem. Do not pad the Findings section to look thorough: a report whose top three findings all say "no action, just noting" has buried its actual value. If there is genuinely nothing to act on, say so plainly and let the improvements section carry the report.

Report structure:

```
## Claude Config Audit

**Scope covered:** [global / project X / claude.ai]
**Sources reconciled:** [account skills / plugins via /plugin list / on-disk]

### Findings (ranked by impact)
[Only things requiring action. Non-actionable observations go below.]
1. [Finding] — [why it matters] — [concrete fix, incl. WHICH inventory + how]
2. ...

### CLAUDE.md health
[Line counts; stable-vs-volatile content; scope notes]

### Usage telemetry
[Never-used plugins/skills as cut candidates; high-use items to keep]

### Suggested improvements (additions, not removals)
[Gap-analysis output from 3i — each with the observed evidence that motivates
it and a concrete first step. Omit the section only if there genuinely are
none; a lean setup usually has at least one, e.g. a missing global CLAUDE.md]

### No action needed (checked and fine)
[What was reviewed and is genuinely OK — so the user knows the scope of the check]
```

Keep each finding to 1–3 lines.

## Mechanics FAQ (answer these when the user asks "but why does this help?")

- **How does cutting a skill actually help?** At session start Claude preloads only each skill's name + description (~100 tokens each) — bodies load on demand. So the main win from trimming isn't raw tokens; it's *triggering accuracy*: fewer near-duplicate descriptions competing means the right skill fires more reliably. Session-start hooks and always-on CLAUDE.md content are the exception — those load in full every time, so cutting them is a direct token win.
- **Disable vs uninstall vs delete?** Disable is reversible and keeps the files; uninstall/delete removes them. For MCP, disable still costs context (tool defs stay injected) — remove to actually reclaim it.
- **Why did a skill I deleted come back?** It was plugin-injected, not local. `rm` on a namespaced skill does nothing; disable the plugin instead.
- **Global CLAUDE.md vs memory vs project CLAUDE.md?** Global = stable facts true everywhere (edited rarely by you). Memory = volatile facts (updated continuously by Claude). Project CLAUDE.md = that repo's conventions. Put changeable things in memory so the global file stays lean.

## Running this periodically

Re-run as the setup grows — libraries accumulate cruft like any codebase; nobody removes the old thing when they add its replacement. Good cadences: when something stops triggering right, before installing a plugin that might overlap an existing one, or every few months as routine maintenance.
