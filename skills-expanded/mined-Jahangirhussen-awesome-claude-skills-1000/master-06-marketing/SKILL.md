---
name: master-06-marketing
description: 06-MARKETING domain of the master skills library (marketing, social, copywriting, email, ads, CRO, growth and market research). Use when the task needs campaign, content, ad, social or conversion work and no more specific installed skill matches. Not when the work is SEO ranking (seo-master).
---

# 06-MARKETING

## Purpose
Index for marketing, social, copywriting, email, ads, CRO, growth and market research: imported skills (read in place) and a pointer to the installed skills in this domain.

## When to use
The task needs campaign, content, ad, social or conversion work.

## When NOT to use
- The work is SEO ranking (seo-master).
- Another domain fits better (see `../ROUTER.md`).

## Inputs
The task, project context, and constraints; domain is inferred by the orchestrator.

## Core workflow
1. Check the imported skills below; if one fits, open its `SKILL.md` and follow it.
2. Otherwise open `INSTALLED.md` in this folder (installed skills per subdomain) and invoke the matching skill with the Skill tool.
3. For cross-domain needs follow `../DEPENDENCIES.md` instead of duplicating instructions.
4. Execute, verify, report.

## Decision rules
- Prefer the most specific skill; prefer installed canonical skills over imported generic ones.
- Open one skill at a time; do not read the whole folder.

## Edge cases and failure handling
- No fitting skill -> use general capability and say no adequate skill exists; do not invent one.
- Imported skill depends on an unavailable external service -> use the nearest installed alternative.

## Validation
Check the chosen skill's instructions match the task and that its output is verified with the matching testing/validation approach.

## Output requirements
The task result as a short `DONE`; no routing narration.

## Example
Request in this domain -> orchestrator selects the skill from the list below or `INSTALLED.md` -> follow its steps -> verify -> report.

## Imported skills (read the SKILL.md at the path when relevant)
- `content/content-repurposer/SKILL.md` - Trigger when the user wants to repurpose, transform, or adapt existing content into a different format. Also trigger for turning a blog post
- `content/content-research-writer/SKILL.md` - Assists in writing high-quality content by conducting research, adding citations, improving hooks, iterating on outlines, and providing real
- `conversion-optimization/landing-page/SKILL.md` - Trigger when the user wants to generate a marketing landing page, pricing page, or product homepage. Also trigger for adding specific sectio
- `email-marketing/newsletter-composer/SKILL.md` - Trigger when the user wants to write, draft, or structure an email newsletter. Also trigger for writing subject lines, preview text, newslet
- `growth/growth-marketer/SKILL.md` - Growth marketing covering experimentation, funnel optimization, acquisition channels, retention, and viral growth. Use when designing A/B ex
- `market-research/competitive-ads-extractor/SKILL.md` - Extracts and analyzes competitors' ads from ad libraries (Facebook, LinkedIn, etc.) to understand what messaging, problems, and creative app
- `paid-ads/conversational-ads/SKILL.md` - Plan, write and measure ads inside AI assistants and AI search (ChatGPT Ads, Google AI Overviews and AI Mode, Microsoft Copilot). Use when t
- `social-media/linkedin-comment-writer/SKILL.md` - Drafts comments on other people's LinkedIn posts that add a specific the post lacked, then gates them offline. Use when commenting on a post
- `social-media/linkedin-content-planner/SKILL.md` - Builds a weekly or monthly LinkedIn publishing plan from content pillars, a posting cadence and a format mix, with a founder-oriented pillar
- `social-media/linkedin-content-repurposer/SKILL.md` - Turns something made for another channel (a thread, a video or talk transcript, a blog post, a newsletter) into a post that reads as native 
- `social-media/linkedin-employee-advocacy/SKILL.md` - Designs and runs an employee advocacy programme: who posts what and how often, review rules, and what is never scripted. Use when getting a 
- `social-media/linkedin-engagement-analytics/SKILL.md` - Segments who reacted to and commented on a post from a CSV or JSON export, and says whether it reached the intended audience. Use when revie
- `social-media/linkedin-hook-analyzer/SKILL.md` - Extracts and classifies the opening-line pattern of LinkedIn posts the user pastes or saves, and turns each into a reusable slot template wi
- `social-media/linkedin-humanizer/SKILL.md` - Audits and rewrites LinkedIn drafts to remove machine-sounding patterns: tiered tell catalogue, emoji-pattern scoring, rule explanations, an
- `social-media/linkedin-post-writer/SKILL.md` - Drafts LinkedIn posts from a brief: picks an angle and opening pattern the author's real material supports, structures the body, and gates t
- `social-media/linkedin-profile-optimizer/SKILL.md` - Audits and rewrites a LinkedIn profile from pasted text: headline, About, experience, skills, Featured, banner and photo. Use when reviewing
- `social-media/linkedin-reply-manager/SKILL.md` - Triages a pasted LinkedIn comment section and drafts replies: which comments to answer, in what order, which to ignore. Use when answering c
- `social-media/linkedin-story-interviewer/SKILL.md` - Interviews a person to surface what they actually have to say, and keeps the answers in a local story bank file that later LinkedIn drafts d
- `social-media/linkedin-thread-tracker/SKILL.md` - Keeps a local log of LinkedIn comments you left, records who replied, and reports follow-ups due, overdue, or dead. Use when logging a comme
- `social-media/social-media-planner/SKILL.md` - Trigger when the user wants to plan, generate, or schedule social media content. Also trigger for creating posts for Twitter/X, LinkedIn, or
- `social-media/twitter-algorithm-optimizer/SKILL.md` - Analyze and optimize tweets for maximum reach using Twitter's open-source algorithm insights. Rewrite and edit user tweets to improve engage

## Related skills
`../ROUTER.md`, `../DEPENDENCIES.md`, `../RULES.md`, `INSTALLED.md`.
