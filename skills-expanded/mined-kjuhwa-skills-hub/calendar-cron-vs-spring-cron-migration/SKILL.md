---
tags: [backend, calendar, cron, spring, migration]
name: calendar-cron-vs-spring-cron-migration
description: Convert between Spring 6-field cron and Quartz/calendar 7-field cron without DST/leap-year regressions
trigger: Scheduler migration from Spring @Scheduled(cron=...) to Quartz-style CronTrigger, or persisting user-authored cron that must survive both engines
category: backend
source_project: lucida-report
version: 1.0.0
---

# Cron dialect conversion (Spring ↔ Quartz/calendar)

See `content.md`.
