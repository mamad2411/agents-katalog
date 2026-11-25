---
name: claude-design-skills-top5
description: Verified register of the "Top 5 Claude Code design skills" (Taste Skill, Impeccable, UI UX Pro Max, Anthropic's frontend-design, Playwright MCP) plus the four Anthropic skills in an "AI Easily" carousel (Canvas Design, Theme Factory, Slack GIF Creator, Algorithmic Art). Each repo was cloned and its licence, install route and counts read on 4 October 2026; the slides' install commands are corrected where they skip a step. Records what is already installed in this repo. Use when improving the look of generated frontends, choosing a design skill for Claude Code, or before running npx skills add, npx impeccable install or /plugin install for any of them.
---

# Claude design skills: verified register

Sources: @awayfromlovable "Top 5 Claude Code design skills" (7 slides) and @ai.easily "4 Claude skills for people who don't code" (6 slides). Star counts on the slides (92.2k, 74.6k, 132.6k, 179k, 37.8k) were **not verified**; the GitHub API is blocked from the build environment.

| # | Skill | Repo | Licence | Last commit |
|---|---|---|---|---|
| 1 | Taste Skill | `Leonxlnx/taste-skill` | MIT | 2026-09-26 |
| 2 | Impeccable | `pbakaus/impeccable` | Apache-2.0 | 2026-10-04 |
| 3 | UI UX Pro Max | `nextlevelbuilder/ui-ux-pro-max-skill` | MIT | 2026-10-03 |
| 4 | frontend-design (Anthropic) | `anthropics/skills` | Apache-2.0, per skill (no single root licence) | 2026-09-28 |
| 5 | Playwright MCP | `microsoft/playwright-mcp` | Apache-2.0 | 2026-09-28 |

## Install routes: slide against README

| Skill | Slide says | Its README says |
|---|---|---|
| Taste Skill | `npx skills add Leonxlnx/taste-skill` | `npx skills add https://github.com/Leonxlnx/taste-skill`; one skill only with `--skill "design-taste-frontend"` |
| Impeccable | `npx impeccable install` | Same, then run `/impeccable init` inside your agent. All 24 commands are used as `/impeccable <command>` (polish, audit, critique, distill, animate, bolder, quieter and more). Its launcher runs a self-contained engine binary: read what it fetches before running it |
| UI UX Pro Max | `/plugin install ui-ux-pro-max@ui-ux-pro-max-skill` | **First** `/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill`; the slide skips this step |
| frontend-design | `/plugin install example-skills@anthropic-agent-skills` | **First** `/plugin marketplace add anthropics/skills`; the slide skips this step |
| Playwright MCP | `claude mcp add playwright npx @playwright/mcp@latest` | README gives a JSON config using `@playwright/mcp@latest`; the `claude mcp add` form is equivalent [Likely] |

## Counts the slides print

Checked against the READMEs: Impeccable **24 commands** (also 61 detector rules); UI UX Pro Max **192 palettes and 74 font pairings** (plus 79 searchable styles, 50 active); Theme Factory **10 themes** (counted in its `themes` folder); Slack GIF Creator targets 128x128 emoji GIFs; Algorithmic Art uses p5.js; Canvas Design outputs .png and .pdf. All match. The UI UX Pro Max screenshot also shows a "Premium" button, so part of it is a paid tier. [Certain]

## Already installed in this repo

`frontend-design`, `canvas-design`, `theme-factory`, `slack-gif-creator` and `algorithmic-art` are already skills here, and Playwright is already in `.mcp.json` (unpinned at `@latest`; consider pinning it). Nothing new needs installing for those. This repo's own `taste` skill is a music-video aesthetic layer, unrelated to Taste Skill; Taste Skill installs under names such as `design-taste-frontend`, so a clash is unlikely, but check `ls .claude/skills` after installing. [Likely]

## Rules

1. Install into one project first and read each skill's `SKILL.md` and scripts. A skill is instructions your agent obeys, so a third-party skill is a supply-chain risk.
2. Run `/impeccable init` only in a repo where writing `PRODUCT.md` is wanted.
3. Pin versions where the tool allows it; `@latest` changes under you.
4. These skills steer taste; they do not replace a design system, accessibility testing or a human review.
5. Nothing here was installed by the build session. The commands are for you to run.
