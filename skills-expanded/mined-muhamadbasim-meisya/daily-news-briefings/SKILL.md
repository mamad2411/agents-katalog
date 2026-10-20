---
name: daily-news-briefings
description: "Create, audit, and schedule recurring daily news briefings with source quality checks, local-impact analysis, and concise executive synthesis."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [news, briefing, research, cron, verification, indonesia, ai]
---

# Daily News Briefings

Use this skill when the user asks for a recurring or one-off news briefing, morning update, global/local/AI digest, or an audit of a previously generated news summary.

## Core workflow

1. **Clarify the briefing contract only when needed.** If the user names cadence, audience, scope, and delivery channel, act immediately. For ambiguous requests, choose sensible defaults and state them briefly.
2. **Separate requested categories exactly.** If the user asks for “global, Indonesia, and AI,” produce distinct sections for:
   - Global news
   - Indonesia/local domestic news
   - AI/technology news
   - Optional: impact on Indonesia / implications for the user
3. **Do not substitute “impact on Indonesia” for “Indonesia news.”** Impact analysis is valuable, but it is not the same as domestic local coverage.
4. **Use a source hierarchy.** Prefer primary or high-reliability sources:
   - Primary/regulator/company/official statements for policy, product launches, safety alerts.
   - Reuters/AP/BBC/Al Jazeera/ANTARA/Kompas/Bloomberg/FT/WSJ for broad news, depending on availability.
   - Specialist tech sources such as The Verge, TechCrunch, 9to5Google, company blogs, papers, and model cards for AI.
5. **Use recency discipline.** For a daily briefing, default to the last 24 hours. Older items can appear only if they are still active context, and must be labeled as background/trend rather than “today’s update.”
6. **Verify before amplifying.** For military conflict, casualties, market-moving claims, IPO/valuation numbers, prices, earthquakes, and disaster alerts, cross-check with at least two sources or clearly label confidence and verification gaps.
7. **Distinguish source confidence from analytical confidence.** A claim can be well-sourced but have uncertain implications. Mark both where useful.
8. **Keep the briefing concise but analytical.** Avoid generic summaries. Each item should answer: what happened, why it matters, risk/impact, and source link.

## Recommended briefing format

Use this structure unless the user requests something else:

```markdown
# Ringkasan Pagi — <Scope> — <Tanggal WIB>

## Executive brief
3–5 sentences: what matters most and why.

## Top 5 yang wajib tahu
- Item: consequence in one sentence. Confidence: High/Medium/Low. Source.

## Global
- Title: what happened; why it matters; risk/impact; source(s); confidence.

## Indonesia Hari Ini
- Domestic news item; why it matters; risk/impact; source(s); confidence.

## AI & Teknologi
- AI item; why it matters; business/policy/social implication; source(s); confidence.

## Dampak untuk Indonesia / user
- Practical implications, opportunities, or risks.

## Audit kualitas informasi
- Weak/fast-changing claims
- Conflicting sources
- Low-confidence items

## Yang perlu dipantau hari ini
- 3–5 watch items.
```

For Telegram, avoid tables; use bullets and labeled fields.

## Auditing a prior briefing

When asked to analyze a previously sent briefing:

1. Retrieve the exact prior output if available from cron output/session history before judging it.
2. Score separately:
   - Category fit: did it satisfy the requested scope?
   - Recency: are items genuinely current?
   - Source quality: primary/high-reliability vs snippet/secondary.
   - Verification transparency: are weak claims marked?
   - Usefulness: does it produce decisions, monitoring points, or content angles?
3. Call out mismatches directly. Example: “Indonesia section is impact analysis, not domestic news coverage.”
4. Recommend prompt/job changes, including duplicate-job cleanup if multiple cron jobs deliver the same briefing.

## Scheduling with Hermes cron

When creating, resuming, or manually rerunning a daily news cron job:

- Use the user’s timezone explicitly in the prompt, especially for WIB/Asia/Jakarta.
- Prefer schedule `0 6 * * *` for 06:00 local scheduler time only if the scheduler timezone matches the intended timezone; otherwise verify or encode timezone in the prompt.
- Include toolsets needed for research: `web` for source discovery and `terminal` when the job needs reliable date/time checks, scripted fallback fetching, or diagnostic verification.
- Attach this skill (`daily-news-briefings`) to the job so future runs inherit the source-quality, recency, and audit rules.
- Pin a known-working model/provider when rerunning a failed or previously unpinned briefing job; if the previous failure was a transient provider 5xx, treat the fix as “retry after provider stabilization / pin provider,” not as a content failure.
- Make the prompt self-contained because cron runs in a fresh session.
- If replacing an older briefing job, list jobs and pause/remove duplicates rather than letting multiple 06:00 jobs fire.
- When a user says “jalankan lagi ringkasan berita pagi,” first `cronjob list`, identify the active morning-news job, repair obvious missing config (skill/toolsets/model pin) if needed, then `cronjob run` it. Leave deliberately paused duplicate/legacy jobs paused unless the user explicitly asks to restore them.

## Pitfalls

- Do not overstate claims from snippets. If full extraction is unavailable, say so and reduce confidence.
- If the configured web backend is search-only and `web_extract` fails, continue with explicit fallback research instead of stopping: use additional searches, official/source snippets, and terminal-based `urllib`/stdlib HTML fetching where appropriate. Avoid assuming `bs4` is installed; prefer Python stdlib parsing or simple regex extraction unless the environment has BeautifulSoup available.
- Do not pad with stale stories to fill a quota. It is acceptable to say “no strong verified update.”
- Do not bury the main risk in long lists; lead with the most decision-relevant facts.
- Do not turn every news item into a content idea; separate news analysis from optional content opportunities.

## References

- `references/basim-global-indonesia-ai-brief.md` — session-derived notes for Basim’s recurring global/Indonesia/AI morning briefing and audit standards.
