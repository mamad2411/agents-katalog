---
name: product-analytics
description: >
  Design product analytics — event taxonomy, tracking plan, metric definitions,
  dashboard requirements, and insight workflows.
  TRIGGER when: user says /product-analytics or asks about product instrumentation and usage tracking.
argument-hint: "[product or feature to instrument]"
user-invocable: true
---
# Product Analytics Design
## Process
### Step 1: Define Analytics Goals
| Question | Analytics Needed |
|----------|-----------------|
| Are users activating? | Activation funnel events |
| Are users engaged? | Session, feature usage events |
| Are users retaining? | Return frequency, churn events |
| Are users expanding? | Upsell, feature adoption events |
| Where do users struggle? | Error, rage-click, drop-off events |
### Step 2: Design Event Taxonomy
| Convention | Format | Example |
|-----------|--------|---------|
| Object_Action | noun_verb (past tense) | `project_created`, `report_exported` |
| Properties | snake_case, consistent types | `plan_type: "pro"`, `item_count: 5` |
| Naming rules | No abbreviations, consistent casing | `subscription_upgraded` not `sub_up` |
### Step 3: Create Tracking Plan
| Event | Trigger | Properties | Priority |
|-------|---------|-----------|----------|
| page_viewed | Page load | page_name, referrer | Must |
| button_clicked | CTA click | button_name, location | Must |
| feature_used | Feature activation | feature_name, duration | Must |
| error_occurred | Error displayed | error_type, error_message | Must |
| search_performed | Search submitted | query, results_count | Should |
### Step 4: Define Metrics
| Metric | Definition | Formula |
|--------|-----------|---------|
| DAU/MAU | Daily/Monthly active users | Unique users with session | 
| Activation rate | Users completing setup | Activated / Signed up |
| Feature adoption | Users using feature X | Feature users / MAU |
| Retention (D7) | Return after 7 days | Active D7 / Cohort size |
### Step 5: Design Dashboards
| Dashboard | Audience | Metrics |
|-----------|----------|---------|
| Executive | Leadership | MAU, retention, revenue |
| Product | PM/Design | Feature adoption, funnels |
| Growth | Marketing | Acquisition, activation |
| Engineering | Dev team | Errors, performance |
### Step 6: Establish Insight Workflow
1. Weekly metrics review (automated report)
2. Anomaly investigation (dig into unusual changes)
3. Hypothesis formation (why did metric change?)
4. Experiment design (A/B test to validate)
5. Decision and iteration
## Output Format
```markdown
## Analytics Plan: [Product]
### Event Taxonomy: [Naming convention and key events]
### Tracking Plan: [Event table]
### Metrics: [Definitions and targets]
### Dashboards: [Requirements by audience]
```
## Quality Checklist
- [ ] Event naming is consistent and documented
- [ ] All key user actions have tracking events
- [ ] Metrics have clear definitions and formulas
- [ ] Dashboard requirements match stakeholder needs
- [ ] Privacy and consent handled properly
## Edge Cases
- For mobile apps, track offline events with batched upload
- For multi-platform, ensure consistent event names across platforms
- If GDPR applies, implement consent management before tracking
