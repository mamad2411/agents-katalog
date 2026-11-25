---
name: find-skill
description: Search curated, trusted sources for installable agent skills that match what the user is trying to do, and return a short list of candidates with a one-line summary and link to each. Use this skill whenever the user asks to find, discover, look for, browse, or install skills — including phrasings like "is there a skill for X", "find me a skill that does Y", "what skills exist for Z", "I need a skill to handle W", or any time the user describes a repetitive task and wonders aloud whether a packaged skill exists. Also use when the user mentions a tool/workflow gap and is open to extending Claude. This skill only points at candidates — it does not install anything.
---

# Find Skill

Help the user discover installable agent skills that match a task. Default to a quick, scannable list of candidates with summaries — no installation, no long explanations, no padding.

## When to use this

Phrasings that should activate this skill:

- "Find me a skill for X" / "Is there a skill that does Y?"
- "What skills exist for [domain]?"
- "I need a skill to handle [task]"
- "Show me skills for [tool/format]"
- Any moment the user describes a recurring or specialized task and is wondering whether a pre-packaged skill exists for it.

If the request is genuinely ambiguous ("find me a coding skill" — coding is enormous), ask ONE narrowing question before searching. Otherwise, just go.

## Where to search

Search **all** of these sources for every query — don't stop at the first hit. Each marketplace has a different catalog; comprehensive results require hitting several of them.

### Anthropic-controlled (gold standard)

**1. anthropics/skills** — https://github.com/anthropics/skills  
Anthropic's official skill examples (docx, pdf, pptx, xlsx, skill-creator, frontend-design, mcp-builder, etc.). 126k+ stars. The catalog lives at `/skills/` at the repo root. Install via Claude Code with `/plugin install document-skills@anthropic-agent-skills` or via Claude.ai Settings → Features.

**2. anthropics/claude-plugins-official** — https://github.com/anthropics/claude-plugins-official  
Anthropic-managed directory of high-quality, partner-vetted Claude Code plugins. Includes third-party integrations (SonarQube, Upstash Context7, CrowdStrike, GitLab, etc.) alongside skill bundles. Good for enterprise/integration skills beyond document processing.

**3. anthropics/claude-code** — https://github.com/anthropics/claude-code  
The Claude Code repo itself has a `.claude-plugin/marketplace.json` listing bundled plugins (PR review agents, frontend design, hooks toolkit, etc.). Worth checking for coding/workflow skills.

### High-volume community marketplaces

**4. claudemarketplaces.com** — https://claudemarketplaces.com/  
Curated directory of 2,500+ Claude Code plugin marketplaces — acts as a meta-directory. Browse by category (Frontend Development, Backend & APIs, Document & Office, Security, DevOps, etc.). Best for discovering whole plugin collections rather than single skills.

**5. skillsmp.com** — https://skillsmp.com  
Largest raw aggregator — 900,000+ skills auto-synced from GitHub. Cross-platform (Claude Code, Codex CLI, ChatGPT), but Claude Code is a first-class filter. Good breadth; use as a sweep net after checking more curated sources.

**6. skillhub.club** — https://www.skillhub.club  
7,000+ skills with AI quality ratings (S/A/B ranks). Rated on Practicality, Clarity, Automation, Quality, and Impact. Includes a live playground to test skills before installing. Most useful when you want quality assurance alongside discovery.

**7. lobehub.com/skills** — https://lobehub.com/skills  
Broad aggregator spanning Claude, Codex, OpenCode, Cursor, and others. Large catalog but requires filtering for Claude-compatible skills (see Claude-only filter below). Good for surfacing niche skills that don't appear elsewhere.

**8. mcpmarket.com/tools/skills** — https://mcpmarket.com/tools/skills  
Active directory focused on agent skills across Claude.ai, Claude Code, Codex, and ChatGPT. Well-maintained; categorized and searchable.

**9. claudeskills.info/skills/** — https://claudeskills.info/skills/  
Curated Claude-first marketplace (~140+ handpicked skills). Includes the complete official Anthropic collection and notable community contributions. Smaller catalog but more signal per entry.

### Aggregator / open standard reference

**10. agentskills.io** — https://agentskills.io  
The home of the open Agent Skills standard (cross-platform SKILL.md format). Points to conformant skill repositories across all platforms. Use this to understand what cross-platform skills exist and which can be adapted for Claude.

If a source goes stale or a new trusted source emerges, update this list rather than letting it drift.

## How to search each source

- **GitHub repos (anthropics/skills, claude-plugins-official, claude-code):** Use the GitHub Contents API at `api.github.com/repos/{owner}/{repo}/contents/{path}` for a clean file listing. If the API is unreachable, `web_search` for `site:github.com/{owner}/{repo} {query}` works as a fallback. Don't rely on the plain GitHub HTML directory page — it returns navigation chrome, not the file list.
- **Web marketplaces (claudemarketplaces.com, skillhub.club, etc.):** Use `web_search` with the query + site filter, or `web_fetch` the search/category page directly. Most sites have search URLs like `https://skillsmp.com/?q=pdf` that `web_fetch` handles cleanly.
- **Parallel is better than sequential:** Fetch multiple sources simultaneously if your tooling allows. Aim to cover at least sources 1–5 for every query; add 6–10 for broad or hard-to-match requests.

## Quality and popularity signals

Before surfacing a candidate, check whether real people have actually used it. Here's how to read the signals per source:

| Source | Signal to check | Minimum bar |
|---|---|---|
| anthropics/skills | Official = pre-vetted; no threshold needed | Any skill here passes |
| anthropics/claude-plugins-official | Partner-reviewed = pre-vetted | Any skill here passes |
| GitHub repos (community) | Stars on the source repo | ≥ 50 stars on the skill's home repo |
| skillhub.club | AI quality rank (S/A/B/C) + install count | A-rank or higher; skip B and below |
| skillsmp.com | GitHub stars surfaced per skill card | ≥ 50 stars on the source repo |
| lobehub.com | Install count shown on skill cards | ≥ 100 installs |
| mcpmarket.com | View/install count | ≥ 50 installs or views |
| claudeskills.info | Curated inclusion = baseline signal | Any listed skill passes |
| claudemarketplaces.com | Marketplace listing count / activity | Check the underlying repo for stars |

**Reject skills with no visible adoption signal** — if a skill has 0 stars, no install count, no rating, and comes from an account with no other activity, skip it. Don't surface something untested just because it matches the query.

**When nothing with strong signals matches**, say so explicitly rather than padding with low-signal results: "I found candidates but they have very little usage data — do you want me to list them anyway, or would you prefer to build a custom skill?"

**Anthropic-controlled sources are always trusted** regardless of star counts — they're officially maintained and pre-tested.

## Claude-only filter

The Agent Skills format is an open cross-platform standard, but skills written for other ecosystems often depend on platform-specific tools and won't run in Claude as-is. Surface only Claude-compatible skills.

**Reject any candidate prefixed by a competing platform:**

- `openclaw-*`, `voltagent-*`, `manus-*`, `goose-*`, `block/agent-skills/*` (Goose), anything obviously Codex-only or Gemini-only.

**Reject any candidate whose SKILL.md depends on competing-platform tooling:**

- Hard requirements like `pdauth` CLI, the OpenClaw browser tool, the Goose `goose` CLI, Manus's VM, etc.
- Install instructions that route only through a non-Claude path with no Claude-native option.

**Prefer candidates that:**

- Live in an `anthropics/*` namespace.
- Explicitly mention "Claude Code" or "Claude.ai" in the description.
- Install via `/plugin install foo@anthropic-agent-skills`, drop into `~/.claude/skills/`, or upload through Claude.ai Settings → Features.

**When in doubt, peek at the SKILL.md** and check what CLI/tool calls it actually expects.

## Workflow

1. **Restate the task in one sentence.** Make sure you understand what the user wants the skill to do. If it's truly unclear, ask one question; otherwise proceed.

2. **Search broadly — hit multiple sources.** Don't stop at the first match. Start depth-first on the Anthropic-controlled sources (sources 1–3), then sweep the high-volume marketplaces (sources 4–9). For rare or niche requests, check all 10.

3. **Read each candidate's SKILL.md (or at least the frontmatter `description`).** That description field is the gold — it tells you exactly what the skill does and when it triggers. Don't guess from the folder name; folder names lie.

4. **Filter ruthlessly: task fit AND Claude-compatible.** Apply the Claude-only filter before ranking by task fit. Three strong matches beats ten loose ones. If nothing fits after filtering, say so plainly.

5. **Format the output as a scannable list (see below).**

## Output format

Default to this shape — terse, no preamble, no closing pep talk:

```
Here's what I found:

**[skill-name]** — [one line: what it does and when to use it]
Source: [source label] · [direct link] · [adoption signal, e.g. "2.1k ⭐", "A-rank", "official"]

**[another-skill-name]** — [one line]
Source: [source label] · [link] · [signal]

[Optional brief note if matches are weak or if writing a custom skill might be the right move instead.]
```

Conventions:

- Cap at 5 candidates. If there are more, say how many and offer to expand.
- Rank by fit, not by source priority. A perfect match in a community marketplace beats a weak match in the official repo.
- Link directly to the skill folder (e.g., the GitHub tree URL), not the repo root — the user wants to land on something useful.
- If a candidate comes from a less-vetted source, note it briefly (e.g., "Source: skillsmp (community aggregator, less vetted)").
- If you found nothing, say so plainly: "Nothing in the curated sources matches. Closest adjacent skill is X, or you may want to author your own — the skill-creator skill can help." Don't fabricate.

## What this skill does NOT do

- **Install skills.** Just point at them. The user wants candidates and summaries, not setup steps.
- **Editorialize.** Don't critique code quality, predict whether a skill is "good," or rank by anything other than task fit, unless the user asks.
- **Search uncurated terrain.** Random GitHub repos, forum threads, blog posts, gists — skip them. The whole point is trusted sources only.

## Example

User: "Is there a skill that helps with reading messy PDFs and pulling tables out?"

Output:

```
Here's what I found:

**pdf** — Read, extract, and manipulate PDF files. Covers text/table extraction, OCR for scans, form filling, merging, splitting.
Source: anthropics/skills · https://github.com/anthropics/skills/tree/main/skills/pdf · official

**pdf-reading** — Focused on inspecting PDF contents and choosing the right extraction strategy for text-heavy vs. scanned vs. data-heavy docs.
Source: anthropics/skills · https://github.com/anthropics/skills/tree/main/skills/pdf-reading · official

The first is probably what you want unless you're specifically dealing with scanned or data-heavy PDFs.
```
