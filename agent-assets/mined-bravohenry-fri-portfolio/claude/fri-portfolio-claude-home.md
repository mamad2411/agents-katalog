# components/home/
> L2 | Parent: src/components/CLAUDE.md

Homepage client components — stateful UI with timers, animations, and live data.

## Members

SystemHeader.tsx: Top bar — logo (Workbench font), status dot, POSTS/WORDS gauges (real stats via props), NYC clock (1s tick)
IdentityMatrix.tsx: Top-left identity panel with FRI specs (designation, brain, entries, last post, version) and cycling quote. Props: `diaryCount`, `weeklyCount`, `lastEntryAge` — fed from `getSiteStats()`
TypeWriter.tsx: Type/delete animation for quote strings, consumed exclusively by IdentityMatrix
ArcReactor.tsx: Center-column core — circular video with rotating CSS rings, crosshair grid, random status label, 1s uptime counter since 2026-01-30
Diagnostics.tsx: Right-column panel — real stat boxes (thisWeek/thisMonth counts), static publishing frequency bars from `dailyActivity[]`, service status list (diary/weekly/link_preview/deploy). Props from `getSiteStats()`
NetworkTraffic.tsx: DEPRECATED — no longer imported by Diagnostics. Animated bar chart replaced by static `dailyActivity` bars
ActiveModules.tsx: Left-column bottom panel — AI module statuses with jittery progress bars
Terminal.tsx: Center-column bottom panel — expandable session terminal with real stats, navigation commands (/latest, /stats, /random, /about, /status), and 45ms typing effect. Props: `stats: SiteStats` from `getSiteStats()`
CoreDirectives.tsx: Right-column bottom panel — 7 directive cards (CSS `.directive-reveal` stagger), WEEKLY nav button, social links (GitHub/Discord/Docs/@z1han), hidden diary easter egg. Server component (no `"use client"`)

[PROTOCOL]: Update this file on any member change, then check parent CLAUDE.md
