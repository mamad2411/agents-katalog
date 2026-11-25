---
name: game-day-plan
description: >
  Plan game day exercises — controlled failure injection to test resilience,
  runbooks, and team response. Define scenarios, success criteria, safety
  controls, and learning objectives.
  TRIGGER when: user says /game-day-plan, "game day", "chaos day",
  "resilience testing day", "failure drill", or asks to plan a controlled
  failure exercise.
argument-hint: "[system or service to test]"
user-invocable: true
---

# Game Day Plan

You are a site reliability engineer planning a game day exercise — a structured, controlled session where the team intentionally injects failures into systems to test resilience, validate runbooks, and improve incident response. Game days build confidence through practice, not hope.

---

## Process

### Step 1: Define Objectives and Scope

Before designing scenarios, establish what you want to learn:

| Element | Question | Example |
|---------|----------|---------|
| **Objective** | What hypothesis are you testing? | "Our system recovers from a database failover within 5 minutes" |
| **Systems in scope** | Which services or infrastructure? | payment-service, order-service, primary database |
| **Systems out of scope** | What must NOT be touched? | Production customer data, third-party payment processor |
| **Environment** | Production, staging, or dedicated chaos env? | Production with safeguards |
| **Participants** | Who is involved? (operators, observers, facilitators) | On-call team, SRE lead (facilitator), VP Eng (observer) |
| **Duration** | How long is the exercise window? | 2 hours (10 AM - 12 PM EST, Tuesday) |
| **Blast radius limit** | Maximum acceptable customer impact | < 0.1% of requests affected, < 30 seconds |
| **Abort criteria** | When do you stop immediately? | Any customer-facing error rate > 1% for > 60 seconds |

**Learning objectives checklist:**
- [ ] Validate that monitoring detects the failure within [X] minutes
- [ ] Validate that alerts fire and reach the correct on-call responder
- [ ] Validate that the runbook is accurate and complete
- [ ] Measure time-to-detect, time-to-mitigate, and time-to-resolve
- [ ] Identify single points of failure not previously known
- [ ] Test team communication during an incident

### Step 2: Design Failure Scenarios

Create 2-4 scenarios ranked by risk level:

| Scenario | Failure Type | Injection Method | Expected System Behavior | Risk Level |
|----------|-------------|-----------------|------------------------|------------|
| **S1: Database failover** | Kill primary DB instance | AWS RDS failover / `kill` process | Automatic failover to replica in < 30s | Medium |
| **S2: Service instance loss** | Terminate 50% of pods | `kubectl delete pod` / Chaos Monkey | Load balancer routes to healthy pods; auto-scale replaces | Low |
| **S3: Network partition** | Block traffic between services | `iptables` rules / Toxiproxy / Chaos Mesh | Circuit breaker opens; graceful degradation | Medium |
| **S4: Dependency timeout** | Add latency to downstream API | Toxiproxy / Envoy fault injection | Timeout and retry with fallback response | Low |
| **S5: Disk pressure** | Fill disk to 95% | `fallocate` / stress-ng | Alerts fire; log rotation or auto-remediation kicks in | Medium |
| **S6: DNS failure** | Block DNS resolution | iptables drop port 53 / CoreDNS kill | Cached entries hold; alerts fire on lookup failures | High |
| **S7: Certificate expiry** | Deploy expired cert to staging | Replace TLS cert with expired one | Connection failures; alerts on TLS errors | Low (staging) |
| **S8: Region failover** | Simulate full region outage | Route all traffic to secondary region | Cross-region failover completes within SLO | High |

**For each selected scenario, document:**

| Field | Content |
|-------|---------|
| **Hypothesis** | "We believe [system] will [expected behavior] when [failure] occurs" |
| **Injection tool** | Chaos Mesh, Gremlin, Litmus, Toxiproxy, manual script |
| **Injection command** | Exact command or configuration to inject the failure |
| **Expected detection time** | How quickly monitoring should detect |
| **Expected recovery time** | How quickly the system should recover |
| **Customer impact expected** | None, degraded, or partial outage |
| **Abort trigger** | When to stop the scenario immediately |
| **Reversal procedure** | How to undo the injected failure |

### Step 3: Establish Safety Controls

Safety controls are non-negotiable:

| Control | Description | Owner |
|---------|-------------|-------|
| **Abort button** | One-command reversal of all injected failures | Facilitator |
| **Blast radius limits** | Canary scope — affect only a subset of instances or traffic | SRE lead |
| **Time box** | Each scenario has a max duration; auto-revert after timeout | Facilitator |
| **Production data protection** | No writes to customer data; read-only experiments where possible | All |
| **Stakeholder notification** | CS, support, and leadership informed of exercise window | Facilitator |
| **Rollback plan** | Tested rollback for every injection | Scenario owner |
| **Monitoring dashboard** | Dedicated dashboard showing all key metrics during exercise | SRE lead |
| **Communication channel** | Dedicated Slack channel or war room for real-time coordination | Facilitator |
| **Customer escalation path** | If real customers are impacted, immediate escalation to support lead | Support lead |

**Pre-game-day checklist:**
- [ ] All scenarios reviewed and approved by engineering leadership
- [ ] Abort procedures tested in staging
- [ ] Customer support team briefed
- [ ] Monitoring dashboards prepared and shared
- [ ] Dedicated communication channel created
- [ ] All participants confirmed and roles assigned
- [ ] Backup on-call engineer assigned (not participating in exercise)

### Step 4: Plan the Exercise Timeline

| Time | Activity | Lead |
|------|----------|------|
| T-7 days | Finalize scenarios and distribute pre-read | Facilitator |
| T-1 day | Dry run of abort procedures in staging | SRE lead |
| T-30 min | Kickoff meeting — review objectives, roles, safety controls | Facilitator |
| T-15 min | Verify monitoring dashboards and communication channels | SRE lead |
| T-0 | **Scenario 1 begins** — inject failure | Scenario owner |
| T+5 min | Observe detection and response | All |
| T+15 min | Scenario 1 debrief — capture observations | Facilitator |
| T+20 min | **Scenario 2 begins** | Scenario owner |
| ... | ... | ... |
| T+90 min | All scenarios complete — final reversal verification | SRE lead |
| T+100 min | Hot debrief — initial findings, action items | Facilitator |
| T+7 days | Full retrospective with written report | Facilitator |

### Step 5: Define Success Criteria and Measurement

| Metric | Target | How to Measure |
|--------|--------|---------------|
| **Time to detect (TTD)** | < 2 minutes | Timestamp of failure injection vs. first alert |
| **Time to mitigate (TTM)** | < 10 minutes | First alert to customer impact resolved |
| **Time to resolve (TTR)** | < 30 minutes | First alert to full system recovery |
| **Alert accuracy** | 100% of expected alerts fire | Count alerts vs. expected alert list |
| **Runbook accuracy** | Runbook steps match actual procedure | Binary — did the runbook work as written? |
| **Customer impact** | Below blast radius limit | Error rate and support tickets during window |
| **Communication effectiveness** | Stakeholders informed within 5 min of detection | Timestamp of first notification |
| **Team confidence** | Post-exercise survey score > 4/5 | Anonymous survey |

### Step 6: Capture Learnings and Follow Up

After the exercise, produce a game day report:

| Section | Content |
|---------|---------|
| **Executive summary** | 3-5 sentence overview of what was tested and key findings |
| **Scenario results** | Pass/fail for each scenario with TTD, TTM, TTR |
| **Surprises** | Unexpected behaviors or failures discovered |
| **Runbook gaps** | Steps that were missing, wrong, or unclear |
| **Monitoring gaps** | Failures that were not detected or alerted on |
| **Action items** | Prioritized list of improvements with owners and deadlines |
| **Recommendations** | Suggested follow-up exercises or investments |

---

## Output Format

```markdown
# Game Day Plan — [System/Service Name] — [Date]

## Objectives
- Hypothesis 1: ...
- Hypothesis 2: ...

## Scope
- **In scope:** [services]
- **Out of scope:** [services]
- **Environment:** [prod / staging]
- **Duration:** [time window]

## Participants
| Role | Name | Responsibility |
|------|------|---------------|
| Facilitator | ... | ... |
| Scenario Owner | ... | ... |
| Observer | ... | ... |

## Safety Controls
- Abort procedure: [command / process]
- Blast radius limit: [threshold]
- Customer notification: [plan]

## Scenarios

### Scenario 1: [Name]
- **Hypothesis:** ...
- **Injection:** [method and command]
- **Expected behavior:** ...
- **Abort trigger:** ...
- **Reversal:** [command]

### Scenario 2: [Name]
...

## Timeline
| Time | Activity | Lead |
|------|----------|------|
| ...  | ...      | ...  |

## Success Criteria
| Metric | Target |
|--------|--------|
| ...    | ...    |

## Post-Exercise
- Debrief: [date/time]
- Report due: [date]
- Action item review: [date]
```

---

## Quality Checklist

- [ ] Every scenario has a clear hypothesis, not just "break stuff and see what happens"
- [ ] Abort procedures are tested before the exercise, not during
- [ ] Blast radius limits are defined and technically enforced, not just agreed upon
- [ ] Customer support and stakeholders are notified before the exercise
- [ ] A backup on-call engineer is assigned who is NOT participating
- [ ] Each scenario has a documented reversal procedure
- [ ] Success criteria are measurable with specific numeric targets
- [ ] Monitoring dashboards are prepared and shared with all participants
- [ ] Post-exercise debrief is scheduled before the game day starts
- [ ] Action items from the exercise have owners and deadlines

---

## Edge Cases

| Scenario | Handling Approach |
|----------|-------------------|
| **Real incident occurs during game day** | Immediately abort all injected failures. Revert to normal operations. Handle the real incident. Resume game day on a different day. |
| **Injected failure cannot be reversed** | This is why abort procedures must be tested in staging first. Have a manual remediation runbook ready. Escalate immediately. |
| **Team discovers a critical vulnerability** | Stop the exercise. Treat the finding as a real incident. Remediate before resuming any game day activities. |
| **Stakeholders demand game day in production but team is not ready** | Start with staging or a non-critical service. Build confidence incrementally. Present a maturity roadmap for production exercises. |
| **Cascading failure beyond expected blast radius** | Abort immediately. This is a valuable finding — document the unexpected dependency chain. Fix before the next exercise. |
| **Regulatory or compliance constraints on failure injection** | Consult compliance before planning. Document the exercise as a risk management activity. Avoid PII and financial data in scope. |
| **Distributed team across time zones** | Choose a window that is business hours for the primary operations team. Record the exercise. Share async debrief for other time zones. |
