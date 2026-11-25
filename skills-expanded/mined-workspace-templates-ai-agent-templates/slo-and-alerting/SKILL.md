---
name: slo-and-alerting
description: Defines SLIs, SLOs and multi-window burn-rate alerts so on-call is paged only when users are affected and the error budget is at risk.
---

# SLO and alerting

Page on user pain and budget burn, not on causes.

## Steps

1. Identify the critical user journeys (for example load a page, submit an order) and the service that serves each.
2. Define an SLI as a ratio of good events to valid events: availability (non-5xx responses / all valid requests) and latency (requests faster than a threshold / all requests). Measure at the load balancer or server edge, and exclude health checks and known client errors.
3. Pull 28 to 90 days of real data. Set the SLO a little below what you reliably achieve, such as 99.9 percent, never 100. Compute the error budget: 0.1 percent over 30 days is about 43 minutes of full outage.
4. Write burn-rate alerts with two windows each, so short spikes do not page:
   - page: burn rate 14.4 over 1 hour and 5 minutes (2 percent of budget in an hour)
   - page: burn rate 6 over 6 hours and 30 minutes
   - ticket: burn rate 1 over 3 days and 6 hours
5. Give every page a runbook link, a dashboard link and a named owner. Delete any existing alert that pages without a human action.
6. Define the policy: what happens when the budget is spent (freeze risky releases, fix reliability first).
7. Test the rules by replaying a past incident and confirming the fast alert would have fired.

## Rules

- Never pick an SLO without looking at the history.
- Do not alert on resource metrics alone.

## Report

SLIs, SLO targets, budget in minutes, alert rules in the monitoring system's format, and alerts removed.
