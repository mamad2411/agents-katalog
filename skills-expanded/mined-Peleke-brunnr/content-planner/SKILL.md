---
name: content-planner
description: >
  Scan GitHub activity and buildlog entries, synthesize engineering work into
  publishable content opportunities with fan-out analysis, and output an
  Obsidian-compatible content plan (kanban board + instrumented briefs). Use when
  planning content, updating the content calendar, or generating writing ideas
  from recent engineering work.
metadata:
  openclaw:
    emoji: "\U0001F4F0"
    requires:
      bins: ["gh", "python3"]
---

# Content Planner

Generate a content plan from recent engineering work. Scan GitHub repos + buildlog entries, identify publishable narratives with fan-out opportunities, and output Obsidian-compatible markdown.

## Step 0: Load Conventions

Before doing ANYTHING, read the shared conventions file:

```
Read ${SKILLS_DIR}/_conventions.md
```

This file defines: canonical vault path, folder-to-type mapping, frontmatter contract, valid statuses, tag hierarchy, cross-reference syntax, and the PipelineEnvelope schema. All output from this skill MUST conform to those conventions. If there is a conflict between this SKILL.md and `_conventions.md`, the conventions file wins.

## Workflow

### Step 1: Scan Recent Activity + Buildlog

Run the Python scan script to collect GH data AND buildlog entries:

```bash
python3 ${SKILLS_DIR}/content-planner/scripts/scan_repos.py --days 14 --format summary
```

For JSON output (when you need structured data for processing):

```bash
python3 ${SKILLS_DIR}/content-planner/scripts/scan_repos.py --days 14 --format json
```

To scan specific repos only:

```bash
python3 ${SKILLS_DIR}/content-planner/scripts/scan_repos.py --days 14 --repos "/path/to/repo1,/path/to/repo2"
```

Without `--repos`, the script scans every git repo with a GitHub remote under `CONTENT_PLANNER_PROJECTS_DIR` (default `~/Documents/Projects`). Pass `--repos` to keep the scan to the repos you publish about, listed in priority order (core product first, then tooling, then side projects).

The scan script automatically collects:
- **GitHub**: merged PRs, open issues, recent commits
- **Buildlog entries**: title, sections, commits, word count, depth classification
- **Fan-out analysis**: which content types each entry can generate
- **Metadata**: review learnings, promoted skills, reward events

### Step 2: Read Deep Buildlog Entries

The scan script classifies entries by depth:
- **deep** (800+ words): Full narrative entries. Read these in full — they're gold mines.
- **medium** (300-800 words): Solid entries. Read selectively based on fan-out score.
- **shallow** (<300 words): Quick commit logs. Skim for context, don't build content from these alone.

For each **deep** and high-fanout **medium** entry, read the full file:

```
Read {entry.file}
```

When reading, extract:
1. **The narrative arc**: Goal → Obstacle → Resolution → Insight
2. **Concrete artifacts**: commit hashes, test counts, code snippets, error messages
3. **Quotable moments**: "what went wrong" stories, unexpected discoveries, aha moments
4. **Cross-references**: PR/issue links, other repos mentioned, buildlog entries that connect

### Step 3: Fan-Out Analysis

Each buildlog entry can generate **multiple** content pieces. The scan script tags fan-out opportunities automatically:

| Entry Section | Content Type | Channel | Example |
|---------------|-------------|---------|---------|
| The Goal / Context | **Provocation** | LinkedIn | "Nobody's doing X. Here's what that costs." |
| Architecture / Components | **Architecture** | Blog | "Here's why we chose X over Y." |
| The Journey / What Went Wrong | **Build Log** | Substack | "I shipped X in Y days. Here's how." |
| Improvements / Lessons | **Lessons** | LinkedIn | "I learned X the hard way. Save yourself the trip." |
| Test Results / Benchmarks | **Results** | Blog | "We measured X. The data says Y." |

**Fan-out scoring**:
- `fanout_count >= 4`: High-value entry. Plan 3-5 content pieces from it.
- `fanout_count 2-3`: Medium. Plan 1-2 pieces.
- `fanout_count 0-1`: Low. Combine with other entries or skip.

**Cross-entry fan-out**: Look for entries across repos that tell a connected story. Example:
- core-engine "Memory layer, phase 1" + dev-tool "Rule-level attribution" → Series: "Teaching Your AI to Learn"

### Step 4: Identify Content Opportunities

For each repo's recent activity + buildlog entries, identify narratives in these categories:

| Category | What to Look For | Audience |
|----------|-----------------|----------|
| **Provocation** | Gaps you found in the industry. Claims nobody else is making. | LinkedIn + blog |
| **Architecture** | Novel technical decisions. Why X not Y. The tradeoff. | Blog (technical) |
| **Build Log** | Velocity stories. "Here's what I shipped and how." | Substack + blog |
| **Tutorial** | Something you built that others could learn from. | Blog + HN |
| **Results** | Data. Measurements. Before/after. Convergence curves. | Blog + paper |
| **Personal** | "I noticed X while using my own tool." The visceral moment. | LinkedIn |

For each opportunity, extract:
- **Title**: Punchy, specific, non-generic. "Every AI Framework Has Memory. None of Them Learn." not "My Thoughts on AI Memory."
- **Source material**: Which PRs, issues, code files, buildlog entries, and commits provide the raw material
- **Links**: Full GitHub URLs to PRs, issues, and relevant code paths
- **Buildlog citation**: If sourced from a buildlog entry, include `buildlog://{repo}/{slug}` reference
- **Series**: Does this belong to a multi-part arc? Which one?
- **Channel**: LinkedIn (300-400 words), Blog (1000-3000 words), Substack (800-2000 words), or HN submission
- **Dependencies**: Does this need data/results that don't exist yet? Or can it be written now?

### Step 5: Check Existing Plan

Before generating output, check if a content plan already exists:

```bash
ls "${VAULT}/Writing/"
```

If `Content-Plan.kanban.md` or `Content-Briefs/` already exist, UPDATE them rather than overwriting. Append new opportunities, mark completed items, adjust priorities.

### Step 6: Generate Obsidian Output

Generate TWO outputs:

#### Output A: Kanban Board

Write to: `{vault}/Writing/Content-Plan.kanban.md`

Format (Obsidian Kanban plugin compatible):

```markdown
---
kanban-plugin: basic
---

## Backlog

- [ ] **Title of content piece** #series-name #channel-linkedin
  Source: [PR #62](https://github.com/your-org/core-engine/pull/62)
  Buildlog: `buildlog://dev-tool/rule-level-attribution`
  Brief: [[Content-Briefs/title-slug]]

## Drafting

- [ ] **Title** #series-name #channel-blog

## Review

- [ ] **Title** #channel-substack

## Published

- [x] **Title** #channel-linkedin
  Published: 2026-02-10
```

Rules for the kanban:
- New items go in **Backlog** unless the user says otherwise
- Items that can be written RIGHT NOW (all source material exists) get a `#ready` tag
- Items that need future data/results get a `#blocked` tag with a note saying what's needed
- Use Obsidian tags: `#series-memory-gap`, `#series-building-in-public`, `#series-security`, `#series-learning-layer`, `#channel-linkedin`, `#channel-blog`, `#channel-substack`
- Link to the detailed brief via `[[Content-Briefs/slug]]`
- For fan-out items, group them: same buildlog source → consecutive kanban items with shared source reference

#### Output B: Content Briefs

Write individual brief files to: `{vault}/Writing/Content-Briefs/{slug}.md`

Format for each brief:

```markdown
---
type: content-brief
status: backlog
series: "The Memory Gap"
channel: linkedin, blog
estimated_words: 1500
created: 2026-02-08
ready: true
source_buildlog: "buildlog-template/workflow-enforcement-tiers-1-2"
source_prs: ["buildlog#125"]
fanout_from: "buildlog://buildlog-template/workflow-enforcement-tiers-1-2"
fanout_type: "architecture"
---

# Title of the Piece

## Angle
One sentence: what's the provocation or insight?

## Source Material
- PR: [dev-tool#125 — workflow enforcement](https://github.com/your-org/dev-tool/pull/125)
- Buildlog: `buildlog/2026-02-06-workflow-enforcement-tiers-1-2.md` (1025 words, deep)
- Code: `src/dev_tool/workflow.py` — verify_workflow(), install_hooks()
- Metadata: 10 review learnings, 10 promoted skills from this repo

## Key Points
1. Point one
2. Point two
3. Point three

## Opening Hook
Draft of the first 1-2 sentences. Make it stop-scrolling worthy.

## Series Context
Where this fits in the series arc. What comes before/after.

## Channel Adaptations
- **LinkedIn** (300 words): Focus on [X]. End with [Y].
- **Blog** (1500 words): Full technical depth. Include [Z].

## Dependencies
- [ ] Need: 10+ buildlog experiment sessions for data
- [x] Have: Framework gap analysis completed
- [x] Have: core architecture shipped
```

### Step 7: Suggest Schedule

After generating the kanban and briefs, propose a 2-week schedule:

```markdown
## Suggested Schedule

| Date | Channel | Piece | Source | Status |
|------|---------|-------|--------|--------|
| Mon Feb 10 | LinkedIn | "Title" | buildlog://repo/slug | Ready |
| Wed Feb 12 | LinkedIn | "Title" | PR #X | Ready |
| Fri Feb 14 | Blog | "Title" (Series 1.1) | buildlog://repo/slug | Ready |
| Mon Feb 17 | LinkedIn | "Title" | — | Blocked — needs X |
```

Prioritize:
1. Items tagged `#ready` (can write now, all source material exists)
2. Provocations first (audience-building), then architecture, then results
3. LinkedIn 2x/week, blog/Substack 1x/week
4. Don't schedule blocked items — list them separately as "upcoming when ready"
5. Fan-out items from the same buildlog entry should be spaced out (don't publish 3 pieces from the same entry in one week)

## Quality Gates

Apply these to every content opportunity before including it:

- **Specific**: Not generic advice. Concrete observation from real engineering work.
- **Non-obvious**: Challenges assumptions. "Everyone thinks X, but actually Y because we measured."
- **Instrumented**: Every piece traces to specific PRs, issues, buildlog entries, or code. No hand-waving.
- **Publish-either-way**: If the result is negative, the failure is publishable too.

## Obsidian Vault Path

The vault is at:
```
${VAULT}
```

Content plan goes in `Writing/`. Briefs go in `Writing/Content-Briefs/`.

If the vault syncs to your phone (iCloud, Obsidian Sync), the plan is readable on mobile as soon as it is written.

## Related Skills

This skill is part of a pipeline. Other skills in the content/publishing flow:

| Skill | What It Does |
|-------|-------------|
| `signal-scan` | Scan market signals, Reddit, HN for positioning |
| `decision-log` | Log strategic decisions to Obsidian |
| `persona-extract` | Extract named audience archetypes with real quotes |
| `offer-scope` | Map insights → offers per persona |
| `hunter-log` | Track outreach + lead engagement |
| `content-planner` | Engineering → content pipeline |

A fully automated version of this pipeline runs `buildlog capture → content-planner scan → draft generation → approval → publish`. This skill is the human-in-the-loop version.
