# /project:incident-response

**Interactive Incident Response & Post-Mortem**

Works in: Cursor IDE chat + Claude Code + CLI

## Usage

```
/project:incident-response AB#123 --create-incident
/project:incident-response --incident=INC-2456
/project:incident-response --post-mortem
```

## What This Does

1. **Creates incident** in incident management system
2. **Triggers runbook** execution (automated + manual steps)
3. **Coordinates incident response** (timeline, actions)
4. **Tracks resolution** (fix, deploy, monitoring)
5. **Generates post-mortem** (root cause, prevention)
6. **Closes incident** with full documentation

## Interactive Flow

```
User: /project:incident-response --incident=INC-2456

Claude: 🚨 Incident Response & Resolution

✅ INCIDENT LOADED:
  Incident: INC-2456 (High Error Rate)
  Service: signup-service (v1.2.0)
  Severity: P1 (Critical)
  Start time: 2026-04-12 15:23 UTC
  Duration: 8 minutes so far

🎯 INCIDENT TIMELINE:

15:23 → PagerDuty alert: Error rate >0.1% (1 min)
15:23 → On-call engineer paged
15:25 → War room started (Slack + Zoom)
15:25 → Incident commander assigned
15:26 → Runbook execution started

⚡ INCIDENT CONTEXT:

Alert: Error rate spiked from 0.02% to 2.3%
Errors: 95% are "OtpExpired" exceptions
Pattern: Spike correlates with Twilio API latency increase
Hypothesis: Twilio API degradation causing OTP validation failures

📋 RUNBOOK EXECUTION:

Running incident resolution steps...

Step 1: Check Twilio API status
  ✓ Twilio status page: 1 incident reported (API latency issue)
  ✓ Estimated time to recovery: 15 minutes
  
Step 2: Check fallback mechanism
  ✓ Fallback to in-app OTP available
  ✓ Fallback not currently enabled
  
Step 3: Enable fallback and reroute traffic
  ✓ Feature flag updated: use_twilio_fallback = true
  ✓ 50% of traffic now using fallback
  
Step 4: Monitor error rates
  ✓ Error rate dropped from 2.3% to 0.3%
  ✓ Still above target <0.1%, but improving

Step 5: Escalate to Twilio
  ✓ Support ticket created with Twilio
  ✓ Escalation to Twilio engineering

15:32 → Fallback activated
15:35 → Error rate dropping (2.3% → 0.5%)
15:45 → Twilio API recovered
15:48 → Error rate normal (0.02%)

✅ INCIDENT RESOLVED

Duration: 25 minutes
Impact: 200,000 OTP verification attempts affected
User impact: 1.3% of users experienced "try again" error
Resolution: Fallback mechanism + Twilio recovery
Downtime: No service downtime, graceful degradation

📊 INCIDENT REPORT:

Severity: P1 Critical
Status: RESOLVED
Root cause: Twilio API degradation (external dependency)
Prevention: Implement circuit breaker for Twilio calls

CREATE POST-MORTEM?
  [1] Yes, schedule for tomorrow
  [2] Auto-generate preliminary report now
  [3] Skip, create manually later

User: [2]

Generating preliminary post-mortem...

**POST-MORTEM REPORT: INC-2456**

**Timeline:**
- 15:23 UTC: Alert triggered (error rate >0.1%)
- 15:25 UTC: On-call notified, war room started
- 15:32 UTC: Fallback mechanism activated
- 15:45 UTC: Twilio API recovered
- 15:48 UTC: Error rate normalized

**Impact:**
- Duration: 25 minutes
- Affected users: 1.3% (200k OTP attempts)
- User experience: "Try again" errors shown
- Revenue impact: $0 (no transactions affected, auth only)

**Root Cause:**
- Twilio API experienced latency spike
- Signup service depended entirely on Twilio (no fallback)
- Alert fired immediately, but recovery was blocked on external service

**Why it happened:**
- No circuit breaker on Twilio client
- No fallback mechanism implemented
- Single dependency without redundancy

**What went well:**
- Alert fired immediately (within 2 min of anomaly)
- War room response fast (2 min to triage)
- Fallback mechanism code already existed (just disabled)
- Team communication clear throughout

**What didn't go well:**
- No pre-planned fallback strategy documented
- Manual feature flag update instead of automated (took 7 min)
- No communication sent to users during incident

**Prevention:**
1. Implement circuit breaker on Twilio client (MEDIUM effort)
2. Automate fallback activation (triggers on latency > 200ms)
3. Set up incident communication template (to users + status page)
4. Create integration test for Twilio failure scenario

**Follow-up Actions:**

Add your notes for prevention items (type in chat):

User: "Circuit breaker — assign to backend team, target next sprint.
       Fallback automation — need infra team input first."

POST PREVENTION ITEMS AS COMMENT?
  [1] Yes, post as comment on incident work item
  [2] Edit comment first
  [3] Just save locally

User: [1]

✓ Posted prevention items + user notes as comment on INC-2456
✓ Tagged: `incident-prevention`, `priority:high`
✓ Post-mortem created and shared with team

📋 INCIDENT CLOSURE:

Close incident?
  [1] Yes, mark as resolved
  [2] Keep open for monitoring
  [3] Re-open if new symptoms

User: [1]

✓ Incident INC-2456 CLOSED
✓ Post-mortem shared in #incidents channel
✓ Prevention items posted as ADO comment for team action
✓ Incident saved to .sdlc/memory/incident-response-INC-2456.md

NEXT STEP?
  [1] View incident metrics dashboard
  [2] Schedule post-mortem review meeting
  [3] Continue with retrospective
  [4] Done

User: [4]

Incident response complete. Service is stable and monitored.
```

## CLI Mode

```bash
$ sdlc skill incident-response --incident=INC-2456
$ sdlc skill incident-response --create-incident
$ sdlc skill incident-response --post-mortem --incident=INC-2456
```

## Outputs

- **Incident Report**: Timeline + impact analysis
- **Post-mortem**: Root cause + prevention actions
- **Follow-up Comments**: Posted as ADO comments on work item (user provides notes in chat)
- **Incident Record**: Saved for future reference

## Post-Incident Actions

- Schedule post-mortem meeting (within 24h)
- Assign prevention tasks to team
- Update runbooks based on findings
- Communication to users (if applicable)
- Process improvement tracking

## Next Commands

- Continue SDLC cycle with new features
- Monitor prevention task completion
- Update runbooks after prevention implementation

---

## Model & Token Budget
- **Model Tier:** Sonnet (post-mortem generation + analysis)
- Input: ~2K tokens (incident timeline + impact)
- Output: ~2.5K tokens (post-mortem + ADO comments)

