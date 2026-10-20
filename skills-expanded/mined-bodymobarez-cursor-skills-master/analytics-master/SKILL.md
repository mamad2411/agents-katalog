---
name: analytics-master
description: Master hub for Analytics, flags & observability. Use for analytics, feature flags, error tracking, LLM analytics, and PostHog workflows. Bundles 73 specialized skills (in skills/<name>/GUIDE.md). Use this for any analytics task.
---

# Analytics, flags & observability — Master Hub

Use for analytics, feature flags, error tracking, LLM analytics, and PostHog workflows.

## How to use this hub

This single skill bundles **all 73 analytics skills**. Each bundled skill's full instructions live in `skills/<name>/GUIDE.md` (plus any `scripts/`, `data/`, `references/` next to it).

**Workflow:**
1. Match the user's request to one or more skills in the list below.
2. Read that skill's `skills/<name>/GUIDE.md` for full instructions before acting.
3. Combine multiple bundled skills when a task spans several areas.

## Bundled skills

- **adding-analytics** — Add PostHog analytics to a web application, including event tracking, page views, feature flags, and session replay.  
  → `skills/adding-analytics/GUIDE.md`
- **adding-error-tracking** — Add Sentry error tracking, performance monitoring, and source maps to a web application.  
  → `skills/adding-error-tracking/GUIDE.md`
- **adding-feature-flags** — Add feature flags to an application for gradual rollouts, A/B testing, and kill switches using PostHog, LaunchDarkly, or a simple local implementation.  
  → `skills/adding-feature-flags/GUIDE.md`
- **posthog-account-handover** — Draft structured handover notes for transitioning a PostHog account from one TAM or CSM to another. Use this skill when a TAM needs to hand over an account, prepare a transition briefing, write han...  
  → `skills/posthog-account-handover/GUIDE.md`
- **posthog-analyzing-experiment-session-replays** — Analyze session replay patterns across experiment variants to understand user behavior differences. Use when the user wants to see how users interact with different experiment variants, identify us...  
  → `skills/posthog-analyzing-experiment-session-replays/GUIDE.md`
- **posthog-auditing-experiments-flags** — Audit PostHog experiments and feature flags for configuration issues, staleness, and best-practice violations. Read when the user asks to audit, health-check, or review experiments or feature flags...  
  → `skills/posthog-auditing-experiments-flags/GUIDE.md`
- **posthog-auditing-warehouse-data-health** — >  
  → `skills/posthog-auditing-warehouse-data-health/GUIDE.md`
- **posthog-authoring-log-alerts** — >  
  → `skills/posthog-authoring-log-alerts/GUIDE.md`
- **posthog-big-fish-lead** — Research, qualify, and suggest outreach for PostHog big fish product-led leads — large companies (500+ or 1000+ employees) using PostHog on free tier without a payment method. Use this skill when a...  
  → `skills/posthog-big-fish-lead/GUIDE.md`
- **posthog-cleaning-up-stale-feature-flags** — Identify and clean up stale feature flags in a PostHog project. Use when the user wants to find unused, fully rolled out, or abandoned feature flags, review them for safety, and then disable or del...  
  → `skills/posthog-cleaning-up-stale-feature-flags/GUIDE.md`
- **posthog-configuring-experiment-analytics** — Configures the analytics side of a PostHog experiment — exposure criteria (default `$feature_flag_called` vs custom exposure events), primary and secondary metrics, the supported metric types (coun...  
  → `skills/posthog-configuring-experiment-analytics/GUIDE.md`
- **posthog-configuring-experiment-rollout** — Configures the rollout shape of a PostHog experiment — the variant split (50/50, 80/20, A/B/C ratios), the overall rollout percentage that gates how many users enter the experiment, and the disambi...  
  → `skills/posthog-configuring-experiment-rollout/GUIDE.md`
- **posthog-copying-flags-across-projects** — Copy a feature flag from one PostHog project to one or more target projects in the same organization. Use when the user wants to duplicate a flag, promote a flag from staging to production, sync fl...  
  → `skills/posthog-copying-flags-across-projects/GUIDE.md`
- **posthog-creating-experiments** — Guides agents through the 3-step experiment creation flow: defining the hypothesis, configuring rollout, and setting up analytics. Delegates rollout decisions to configuring-experiment-rollout and ...  
  → `skills/posthog-creating-experiments/GUIDE.md`
- **posthog-debugging-local-replay** — >  
  → `skills/posthog-debugging-local-replay/GUIDE.md`
- **posthog-diagnosing-experiment-results** — Diagnoses bias, anomalies, and strange-looking results on a specific PostHog experiment. Covers empty / 0-exposure experiments, sample ratio mismatch, identity fragmentation, multi-variant exposure...  
  → `skills/posthog-diagnosing-experiment-results/GUIDE.md`
- **posthog-diagnosing-failed-warehouse-syncs** — >  
  → `skills/posthog-diagnosing-failed-warehouse-syncs/GUIDE.md`
- **posthog-diagnosing-missing-recordings** — >  
  → `skills/posthog-diagnosing-missing-recordings/GUIDE.md`
- **posthog-diagnosing-sdk-health** — >  
  → `skills/posthog-diagnosing-sdk-health/GUIDE.md`
- **posthog-diagnosing-stacktrace-symbolication** — >  
  → `skills/posthog-diagnosing-stacktrace-symbolication/GUIDE.md`
- **posthog-downloading-batch-export-files** — >  
  → `skills/posthog-downloading-batch-export-files/GUIDE.md`
- **posthog-error-tracking-all** — >-  
  → `skills/posthog-error-tracking-all/GUIDE.md`
- **posthog-exploring-apm-traces** — >  
  → `skills/posthog-exploring-apm-traces/GUIDE.md`
- **posthog-exploring-autocapture-events** — >  
  → `skills/posthog-exploring-autocapture-events/GUIDE.md`
- **posthog-exploring-live-traffic** — Inspects PostHog Web analytics Live tab data — current users online, last-30-minutes pageviews, top pages, referrers, devices, browsers, countries, bot traffic, and the per-minute bot/users charts....  
  → `skills/posthog-exploring-live-traffic/GUIDE.md`
- **posthog-exploring-llm-clusters** — Investigate AI observability clusters — understand usage patterns in AI/LLM traffic, compare cluster behavior, compute cost/latency metrics, and drill into individual traces within clusters.  
  → `skills/posthog-exploring-llm-clusters/GUIDE.md`
- **posthog-exploring-llm-costs** — >  
  → `skills/posthog-exploring-llm-costs/GUIDE.md`
- **posthog-exploring-llm-evaluations** — >  
  → `skills/posthog-exploring-llm-evaluations/GUIDE.md`
- **posthog-exploring-llm-traces** — >  
  → `skills/posthog-exploring-llm-traces/GUIDE.md`
- **posthog-feature-flags-all** — >-  
  → `skills/posthog-feature-flags-all/GUIDE.md`
- **posthog-feature-usage-feed** — >  
  → `skills/posthog-feature-usage-feed/GUIDE.md`
- **posthog-finding-deleted-feature-flags** — Find feature flags that were soft-deleted in the active project within a recent time window. Use when the user asks "what flags were deleted in the last N days", "show me recently deleted feature f...  
  → `skills/posthog-finding-deleted-feature-flags/GUIDE.md`
- **posthog-finding-experiments** — Resolves a PostHog experiment reference from natural language to a concrete experiment ID by browsing `experiment-list` (not feature-flag tools), with disambiguation when multiple experiments match...  
  → `skills/posthog-finding-experiments/GUIDE.md`
- **posthog-finding-replay-for-issue** — >  
  → `skills/posthog-finding-replay-for-issue/GUIDE.md`
- **posthog-formatting-insight-axes** — >  
  → `skills/posthog-formatting-insight-axes/GUIDE.md`
- **posthog-grouping-noisy-errors** — >  
  → `skills/posthog-grouping-noisy-errors/GUIDE.md`
- **posthog-hogql** — HogQL queries for PostHog analytics  
  → `skills/posthog-hogql/GUIDE.md`
- **posthog-inbound-lead** — Evaluate and respond to inbound PostHog sales leads from Salesforce. Use this skill when any PostHog TAE needs to triage an inbound lead — deciding whether to qualify for a call, route to self-serv...  
  → `skills/posthog-inbound-lead/GUIDE.md`
- **posthog-inbox-exploration** — >  
  → `skills/posthog-inbox-exploration/GUIDE.md`
- **posthog-instrument-error-tracking** — >-  
  → `skills/posthog-instrument-error-tracking/GUIDE.md`
- **posthog-instrument-feature-flags** — >-  
  → `skills/posthog-instrument-feature-flags/GUIDE.md`
- **posthog-instrument-integration** — >-  
  → `skills/posthog-instrument-integration/GUIDE.md`
- **posthog-instrument-llm-analytics** — >-  
  → `skills/posthog-instrument-llm-analytics/GUIDE.md`
- **posthog-instrument-logs** — >-  
  → `skills/posthog-instrument-logs/GUIDE.md`
- **posthog-instrument-product-analytics** — >-  
  → `skills/posthog-instrument-product-analytics/GUIDE.md`
- **posthog-integration-all** — >-  
  → `skills/posthog-integration-all/GUIDE.md`
- **posthog-investigate-metric** — >  
  → `skills/posthog-investigate-metric/GUIDE.md`
- **posthog-investigating-error-issue** — >  
  → `skills/posthog-investigating-error-issue/GUIDE.md`
- **posthog-investigating-replay** — >  
  → `skills/posthog-investigating-replay/GUIDE.md`
- **posthog-llm-analytics-all** — >-  
  → `skills/posthog-llm-analytics-all/GUIDE.md`
- **posthog-llm-analytics-setup** — PostHog LLM analytics for all supported providers  
  → `skills/posthog-llm-analytics-setup/GUIDE.md`
- **posthog-logs-all** — >-  
  → `skills/posthog-logs-all/GUIDE.md`
- **posthog-managing-experiment-lifecycle** — Guides experiment state transitions: launching, pausing, resuming, ending, shipping variants, archiving, resetting, and duplicating. Covers preconditions, implications for variant assignment and an...  
  → `skills/posthog-managing-experiment-lifecycle/GUIDE.md`
- **posthog-managing-path-cleaning-rules** — Inspects URL paths and proposes, tests, orders, and applies project-level path cleaning rules so dynamic segments (numeric IDs, UUIDs, slugs, dates) collapse into readable aliases. Use when the use...  
  → `skills/posthog-managing-path-cleaning-rules/GUIDE.md`
- **posthog-managing-subscriptions** — Manage PostHog subscriptions — scheduled email, Slack, or webhook deliveries of insight or dashboard snapshots. Use when the user wants to subscribe to an insight or dashboard, check existing subsc...  
  → `skills/posthog-managing-subscriptions/GUIDE.md`
- **posthog-onboarding-lead** — Research and qualify onboarding team referral leads for PostHog. Use this skill when a TAE receives a lead from the onboarding team and needs a full research brief before deciding how to engage. Tr...  
  → `skills/posthog-onboarding-lead/GUIDE.md`
- **posthog-planning-user-interviews** — Plan a user interview topic in PostHog — pick who to target (cohort, emails, or PostHog distinct IDs), draft what to ask about, and prepare the voice-agent context plus a question list. Use when th...  
  → `skills/posthog-planning-user-interviews/GUIDE.md`
- **posthog-posthog-debugger** — Debug and inspect PostHog implementations on any website. Use this skill when a user wants to understand how PostHog is implemented on a page, troubleshoot tracking issues, verify configuration, ch...  
  → `skills/posthog-posthog-debugger/GUIDE.md`
- **posthog-posthog-onboarding** — Help existing PostHog customers improve their PostHog instance. Triggers on "help [customer] improve their PostHog setup", "audit [company]'s PostHog instance", "create tracking plan for [company]"...  
  → `skills/posthog-posthog-onboarding/GUIDE.md`
- **posthog-posthog-survey-creator** — Create and configure surveys in PostHog through guided conversation. Use this skill when a user wants to create a survey, collect user feedback, run NPS/CSAT/CES/PMF surveys, gather product feedbac...  
  → `skills/posthog-posthog-survey-creator/GUIDE.md`
- **posthog-querying-posthog-data** — Required reading before writing any HogQL/SQL or calling execute-sql against PostHog. Use whenever the user wants to search, find, or do complex aggregations PostHog entities (insights, dashboards,...  
  → `skills/posthog-querying-posthog-data/GUIDE.md`
- **posthog-setting-up-a-data-warehouse-source** — >  
  → `skills/posthog-setting-up-a-data-warehouse-source/GUIDE.md`
- **posthog-signals** — >  
  → `skills/posthog-signals/GUIDE.md`
- **posthog-skills-store** — >-  
  → `skills/posthog-skills-store/GUIDE.md`
- **posthog-suggesting-data-imports** — Use when the user asks about revenue, payments, subscriptions, billing, CRM deals, support tickets, production database tables, or other data that PostHog does not collect natively. Also use when a...  
  → `skills/posthog-suggesting-data-imports/GUIDE.md`
- **posthog-suppressing-noisy-errors** — >  
  → `skills/posthog-suppressing-noisy-errors/GUIDE.md`
- **posthog-transition-leads** — Qualify and draft outreach for PostHog product-led leads who are hitting a billing transition — either startup program customers rolling off free credits, or users whose first invoice will be >= $2...  
  → `skills/posthog-transition-leads/GUIDE.md`
- **posthog-triaging-error-issues** — >  
  → `skills/posthog-triaging-error-issues/GUIDE.md`
- **posthog-triaging-visual-review-runs** — >  
  → `skills/posthog-triaging-visual-review-runs/GUIDE.md`
- **posthog-tuning-incremental-sync-config** — >  
  → `skills/posthog-tuning-incremental-sync-config/GUIDE.md`
- **posthog-user-deep-dive** — Deep dive on a PostHog user by email address. Analyze what they do, where they spend time, and what products they use.  
  → `skills/posthog-user-deep-dive/GUIDE.md`
- **posthog-working-with-skills** — >-  
  → `skills/posthog-working-with-skills/GUIDE.md`
- **posthog-workload-analysis** — Generate comprehensive workload analysis visualizations for PostHog customer accounts. Use when user requests account analysis, workload breakdown, SDK analysis, spend allocation, or expansion oppo...  
  → `skills/posthog-workload-analysis/GUIDE.md`

## Note

These bundled skills are intentionally not registered as separate Cursor skills (their files are `GUIDE.md`, not `SKILL.md`) so only this master appears in the skills list. Read the relevant `GUIDE.md` on demand.
