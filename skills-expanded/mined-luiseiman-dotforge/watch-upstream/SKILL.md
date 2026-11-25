---
name: watch-upstream
description: Fetch official Anthropic/Claude Code docs, detect changes relevant to dotforge, report deltas.
---

# Watch Upstream

Detect changes in official Claude Code documentation that may require updates to dotforge.

## Step 0: Discover tools

WebFetch and WebSearch are deferred tools — they may not be loaded yet.
Run `ToolSearch("WebFetch WebSearch")` to ensure both tools are available before proceeding.
If either tool is not found, fall back to `Bash(curl -s <url>)` for fetching.

## Step 1: Fetch current documentation

Use WebFetch to read these pages directly:

1. `https://code.claude.com/docs/en/overview` — main feature list
2. `https://code.claude.com/docs/en/settings` — settings.json schema, permissions
3. `https://code.claude.com/docs/en/hooks` — hook types, events, matchers
4. `https://code.claude.com/docs/en/memory` — memory and context management
5. `https://code.claude.com/docs/en/sub-agents` — subagent capabilities (renamed from agent-tool)
6. `https://code.claude.com/docs/en/cli` — CLI flags and options

If any URL fails, use WebSearch with query `"Claude Code" <topic> site:code.claude.com` as fallback.

If a URL returns 404 instead of redirecting, fall back to `https://code.claude.com/docs/llms.txt` (canonical index) and search for the slug — the new domain reorganized some paths (e.g. agent-tool → sub-agents).

Then search for recent announcements:
- WebSearch: `Claude Code new features 2026`
- WebSearch: `Claude Code changelog site:anthropic.com`
- WebSearch: `Claude Code hooks settings update site:github.com/anthropics`

Budget: WebFetch fails after 5 min per page (`CLAUDE_CODE_WEBFETCH_DEADLINE_MS`), WebSearch refills 100 calls/hour. Keep the doc fetches to the 6 pages + `whats-new` and at most 3 searches.

## Step 1b: Determine the baseline and the raw changelog delta

`WebFetch` summarizes the CHANGELOG through a small model and silently drops bullets when the delta is large (2026-10-06: 60 of 73 versions lost). Never classify from a WebFetch summary of the changelog — use the raw file:

```bash
# Baseline = newest version already cited in the domain rules
BASE=$(grep -rhoE 'v2\.1\.[0-9]+' "$DOTFORGE_DIR/.claude/rules/domain/" | sort -t. -k3 -n | tail -1)
curl -sL https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md -o "$SCRATCH/CHANGELOG.md"
HEAD=$(grep -m1 '^## 2\.1\.' "$SCRATCH/CHANGELOG.md" | awk '{print $2}')
END=$(grep -n "^## ${BASE#v}$" "$SCRATCH/CHANGELOG.md" | cut -d: -f1)
sed -n "1,$((END-1))p" "$SCRATCH/CHANGELOG.md" > "$SCRATCH/changelog-slice.md"
echo "delta: $BASE → $HEAD, $(grep -c '^## ' "$SCRATCH/changelog-slice.md") versions"
```

Second source — extracted system prompts (Piebald-AI/claude-code-system-prompts). It tracks the live system prompt, tool descriptions and subagent prompts per version, usually ahead of our last sync. Diff its CHANGELOG from `$BASE` to detect directives that changed (comment policy, output style, deny-circumvention classifier guidance) — these are the inputs for `prompting-patterns.md` § Overriding hardcoded defaults and `rule-effectiveness.md` § System prompt conflicts:

```bash
curl -sL https://raw.githubusercontent.com/Piebald-AI/claude-code-system-prompts/main/CHANGELOG.md -o "$SCRATCH/sp-CHANGELOG.md"
grep -n "^## \|^### " "$SCRATCH/sp-CHANGELOG.md" | head -40   # version headers + token deltas
```

Never quote a system-prompt directive in a domain rule without re-reading the current `system-prompts/*.md` file — stale quotes ("DO NOT ADD ANY COMMENTS", "fewer than 4 lines") lived in our rules for months after upstream removed them.

Note: `whats-new` weekly digests and the docs pages may cite versions newer than the CHANGELOG head (docs are published ahead) — record them with the docs URL as source.

## Step 2b: Split classification when the delta exceeds ~30 versions

For ≤30 versions, read `changelog-slice.md` directly. Above that, spawn **two `general-purpose` subagents (`model: sonnet`) in parallel**, each owning a contiguous version range (split by header presence — some version numbers are skipped upstream, never by arithmetic). Each prompt must carry: the slice path, its range, the Step 2 impact table, and the instruction to `grep -rn` the dotforge surfaces per kept bullet before classifying as Gap / Partial / Covered / Breaking. Ask for the compact report format (BREAKING / GAP / PARTIAL / COVERED / NOTABLE SKIPPED, under 2500 words). Cost reference: ~500K subagent tokens for 62 versions. Keep the 6 doc pages as persisted files and `grep` them for `v2.1.N` notes instead of reading inline.

## Step 3b: Spot-check before reporting

`grep -n` the raw slice for the 3–5 highest-impact claims (the BREAKING ones) and quote the version header. Subagent summaries occasionally merge adjacent bullets; the raw line is the source of truth.

## Step 2: Extract and classify changes

For each finding, check if it affects dotforge:

| What to look for | Where it impacts dotforge |
|-------------------|---------------------------|
| New hook event types (beyond PreToolUse/PostToolUse/Stop) | `template/hooks/`, `stacks/*/hooks/` |
| New settings.json fields or changed schema | `template/settings.json.tmpl`, `global/settings.json.tmpl` |
| New permission categories | `stacks/*/settings.json.partial` |
| Changed deny list behavior | `template/settings.json.tmpl` deny section |
| New agent/subagent capabilities | `agents/*.md` |
| New skill/command system features | `skills/*/SKILL.md` |
| Deprecated features or breaking changes | Any affected file |
| New CLI flags relevant to automation | `skills/benchmark/SKILL.md` (uses `claude --print`) |
| MCP server changes | `global/settings.json.tmpl` |

Ignore: pricing, model releases (unless affecting tool use), marketing.

## Step 3: Compare against dotforge

For each relevant finding, check the current state:

```bash
# Search template for existing coverage
grep -r "<keyword>" template/ stacks/ global/ agents/ skills/
```

Classify each finding:
- **Gap**: dotforge doesn't cover this at all
- **Partial**: dotforge covers this but is outdated or incomplete
- **Covered**: dotforge already handles this correctly
- **Breaking**: dotforge does something that conflicts with the new behavior

## Step 4: Report

```
═══ WATCH UPSTREAM ═══
Date: {{YYYY-MM-DD}}
Sources fetched: {{N}} docs, {{N}} search results

── CHANGES DETECTED ──

🆕 NEW: {{title}}
   Source: {{url}}
   Impact: {{which dotforge files would change}}
   Priority: {{high|medium|low}}

⚠️ BREAKING: {{title}}
   Source: {{url}}
   Current dotforge behavior: {{what we do now}}
   Required change: {{what needs to change}}

📝 PARTIAL: {{title}}
   Source: {{url}}
   What's covered: {{existing coverage}}
   What's missing: {{gap}}

── SUMMARY ──
Gaps: {{N}} | Partial: {{N}} | Breaking: {{N}} | Covered: {{N}}

── NEXT STEPS ──
For each gap/partial/breaking, run:
  /forge capture "{{description}}"
Then: /forge update to evaluate and incorporate.
```

## Constraints

- DO NOT modify any dotforge files. Report only.
- DO NOT auto-create practices. Suggest `/forge capture` commands for the user.
- If web fetch fails, report clearly — don't guess or hallucinate features.
- If no changes detected, report "No relevant changes found" — this is a valid outcome.
