---
name: dashboard-spec
description: Use this skill when the user asks to specify an internal dashboard, admin tool, back-office UI, operations console, or data-heavy app for a defined audience. Trigger phrases include "spec this dashboard", "admin panel for X", "internal tool", "ops console", "back-office UI", "dashboard de admin", "spec del panel interno". Produces a dashboard spec structured around the question, the user, and the data, with explicit handling of states, roles, and degraded modes.
---

# dashboard-spec

> **Anchor:** A dashboard is a question waiting to be answered. If the question is not written, the dashboard is decoration.

## When to use

Use this skill when the user needs to specify an internal or customer-facing interface whose value is in the data it exposes. Works for:

- Admin consoles for support, billing, or operations.
- Internal data tools for finance, analytics, or compliance.
- Customer-facing account dashboards.
- Operational status pages for an ops team, a partner, or a tenant.

Do not use when:

- The user is designing a product feature for end users. Use `prd-authoring`.
- The user is building event tracking. Use `analytics-instrumentation`.
- The user is reconciling differing numbers across tools. Use `data-reconciliation`.

## Voice rules (apply to all outputs)

- No buzzwords: leverage, empower, synergy, resonate, tapestry, delve, elevate, captivate, explore, dynamic, testament.
- No em dashes.
- No filler openings.
- Decision-oriented over descriptive.
- High-context, no overexplaining.
- Standard sentence case for formal outputs.
- ES outputs match the register of the handbook: direct, self-aware, no reverence for process, comfortable naming failure.
- EN outputs use direct US business register. Do not soften bluntness into corporate-speak.
- Language switches based on audience, not author.

## Bilingual handling

- **ES.** Rioplatense register. Vos over tú. Keep standard terms in English: dashboard, view, empty state, role, permission, audit log, webhook, refresh, schema, SLA.
- **EN.** Direct US business register. Avoid decorative adjectives in specs. A dashboard is either useful or not.
- Column names, metric names, and flag names stay in the language of the data model, not the document.

## Method

### Step 1. Write the decision first

A dashboard exists to support a decision. Write the decision before anything else.

- **Decision.** What will the user do with this data.
- **Cadence.** How often the decision is made.
- **Cost of getting it wrong.** Why accuracy matters.

A dashboard that supports no decision is a screensaver. If the answer is "to be informed", rewrite the section or cut the dashboard.

### Step 2. Name the user and the context

- **User.** The role or team, not a persona name.
- **Seniority or expertise.** Whether the user needs guardrails or raw power.
- **Where they are.** At a desk, on the floor, on call, in a customer meeting.
- **Under what stress.** Time pressure, accountability, frequency.

The same data, shown to a VP vs. an ops analyst vs. a customer, becomes three different dashboards. Pick one.

### Step 3. List the questions it answers

Before any chart name, write the questions. Five to fifteen questions in priority order.

Example:

- "Which accounts used more than 80% of their quota in the last 7 days."
- "Which refunds were issued by which operator in the last hour."
- "Which tenants missed SLA last month, and by how much."

One question becomes one view. A question that has two answers is two questions.

### Step 4. Specify the data model

For each question, name:

- **Source.** The table, warehouse, or API that answers it.
- **Freshness.** How old the data can be before the answer is wrong. Often "real-time", "5 minutes", "daily", "monthly close".
- **Joins and filters.** The shape of the query, at a logical level.
- **Primary metrics.** The values the user will read.
- **Cardinality.** Rough row count the view might show.

Cardinality decides layout. A view that could return 2 rows and a view that could return 2 million rows are different products.

### Step 5. Design the views

One view per question, unless two questions share a natural context.

For each view:

- **Name.** Short, matches the question.
- **Layout.** Filters on top or side. Table vs. chart vs. card. Primary column. Sort order. Pagination or infinite scroll.
- **Drill-down.** What happens when a row is clicked.
- **Time controls.** The user's ability to set a time window.
- **Export.** CSV, copy link, or none.

Avoid the "everything in one view" trap. Visible ≠ usable.

### Step 6. Handle every state explicitly

Every view must define:

- **Loading.** What is shown while data loads.
- **Empty.** What is shown when the query returns no rows. This teaches the user what the tool does.
- **Error.** What is shown on failure. Include who to contact.
- **Partial.** What is shown when one data source is up and another is down.
- **Permission denied.** What non-authorized users see, if they can reach the view at all.
- **Large dataset.** What happens when cardinality exceeds display limits.

A dashboard that has no empty-state design is a dashboard that breaks on first use.

### Step 7. Define roles and permissions

- **Roles.** The set of roles that can access the dashboard.
- **Row-level permissions.** Whether a user sees all tenants or only their own.
- **Write actions.** Which roles can take which destructive actions.
- **Impersonation.** Whether admins can act as another user, and what that requires.

Include a permission matrix if more than three roles exist.

### Step 8. Audit and logging

- **Read audit.** Whether access to the dashboard is logged.
- **Write audit.** Every destructive action logged with actor, timestamp, target, and before/after state.
- **Retention.** How long logs are kept.
- **Review cadence.** Who looks at the audit and when.

For support and admin tools, this section is not optional.

### Step 9. Define SLA, ownership, and change policy

- **Owner.** Who owns the dashboard, including bugs and feature requests.
- **SLA.** Uptime target and data freshness target. Only set SLAs that will be monitored.
- **Monitoring.** Alerts on freshness, errors, and unusual query load.
- **Change policy.** Who can add a view, deprecate one, or change a metric definition.

## Templates

- `templates/en/dashboard-spec.md`: full dashboard specification.
- `templates/en/view-definition.md`: single view inside a dashboard.
- `templates/es/dashboard-spec.md`: especificación completa de dashboard.
- `templates/es/view-definition.md`: definición de una vista dentro del dashboard.

## Related skills

- `analytics-instrumentation`: use it when the work is defining the events behind the views, not the views.
- `data-reconciliation`: use it when the dashboard numbers disagree with another source.
- `prd-authoring`: use it instead when specifying an end-user product feature, not an internal tool.
- `migration-spec`: pairs with this when the dashboard is being rebuilt on a new data source.

## Anti-patterns

This skill must never produce:

- A dashboard spec without a named decision and named user.
- Views named after charts ("bar chart of X") instead of questions.
- A spec that omits empty state or error state.
- A metric whose definition is only in the query.
- "Real-time" as a freshness claim without a latency target.
- A permission model that uses "admin can do everything" as the only role.
- A spec that describes UX polish before data accuracy.
- A dashboard with no audit on write actions.
- A spec that assumes the back-end will exist.

## Checklist before delivery

- [ ] Decision, user, cadence, and cost of being wrong are named.
- [ ] Questions are listed before charts.
- [ ] Each view has a data source, freshness, and cardinality.
- [ ] Every view defines loading, empty, error, partial, permission-denied, and large-dataset behavior.
- [ ] Roles and permissions are explicit.
- [ ] Audit logging for write actions is defined.
- [ ] SLA and owner are named.
- [ ] No buzzwords from the voice rules appear.
