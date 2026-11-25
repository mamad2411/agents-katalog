# /project:deployment

**Interactive Production Deployment & Verification**

Works in: Cursor IDE chat + Claude Code + CLI

## Usage

```
/project:deployment AB#123
/project:deployment AB#123 --version=1.2.0
/project:deployment AB#123 --canary=5%
```

## What This Does

1. **Deploys release** to production (canary or full)
2. **Monitors deployment** in real-time
3. **Runs smoke tests** against production
4. **Verifies metrics** (latency, errors, availability)
5. **Escalates or completes** rollout
6. **Creates deployment record** in ADO

## Interactive Flow

```
User: /project:deployment AB#123 --version=1.2.0

Claude: 🚀 Production Deployment

✅ RELEASE LOADED:
  Version: v1.2.0
  Release tag: v1.2.0
  Rollout strategy: Canary (5% → 25% → 100%)
  Rollback available: v1.1.9

DEPLOYMENT SCHEDULE:

Phase 1: Canary 5% (5 min monitoring)
Phase 2: Canary 25% (10 min monitoring)
Phase 3: Full rollout 100% (15 min monitoring)

Start deployment?
  [1] Yes, proceed with canary phase 1
  [2] Preview deployment plan
  [3] Schedule for specific time
  [4] Cancel

User: [1]

🚀 PHASE 1: CANARY 5%

Deploying to 5% of production traffic...
  ✓ Service replicas updated (1/20)
  ✓ Load balancer configured
  ✓ Feature flags activated (5%)

⏱️ MONITORING (5 min):

Time: 0:30
  P50: 68ms ✓
  P95: 182ms ✓
  Error rate: 0.01% ✓
  Traffic: 50 RPS (5% of 1000)

Time: 1:00
  P50: 70ms ✓
  P95: 185ms ✓
  Error rate: 0.02% ✓

Time: 1:30
  P50: 72ms ✓
  P95: 190ms ✓
  Error rate: 0.01% ✓

Time: 2:00
  P50: 71ms ✓
  P95: 188ms ✓
  Error rate: 0.03% ✓

Time: 2:30
  P50: 69ms ✓
  P95: 186ms ✓
  Error rate: 0.02% ✓

Time: 3:00
  P50: 70ms ✓
  P95: 187ms ✓
  Error rate: 0.01% ✓

Time: 5:00
  Final P95: 186ms ✓
  Final error rate: 0.015% ✓

✅ PHASE 1 COMPLETE - ALL METRICS PASSING

Proceed to Phase 2?
  [1] Yes, escalate to 25%
  [2] Wait and recheck
  [3] Rollback to v1.1.9
  [4] Pause deployment

User: [1]

🚀 PHASE 2: CANARY 25%

Escalating to 25% of production traffic...
  ✓ Service replicas updated (5/20)
  ✓ Load balancer rebalanced
  
⏱️ MONITORING (10 min):

[Similar monitoring output, all metrics passing...]

✅ PHASE 2 COMPLETE

Proceed to Phase 3 (Full 100%)?
  [1] Yes, full release
  [2] Hold at 25% longer
  [3] Rollback to v1.1.9
  [4] Pause

User: [1]

🚀 PHASE 3: FULL ROLLOUT 100%

Deploying to 100% of production...
  ✓ All service replicas updated (20/20)
  ✓ Load balancer fully switched
  ✓ Feature flag: 100% enabled

⏱️ PRODUCTION MONITORING (15 min):

[Monitoring all healthy...]

✅ DEPLOYMENT COMPLETE

Version: v1.2.0
Status: LIVE in production
Uptime: 100%
P95 latency: 187ms (target: <200ms) ✓
Error rate: 0.015% (target: <0.1%) ✓
Throughput: 1050 RPS

📊 DEPLOYMENT RECORD:

Deployed: 2026-04-12 14:15 UTC
Deployed by: AI SDLC Platform
Rollout strategy: Canary 5% → 25% → 100%
Time to production: 30 minutes
Rollback: Available (1-command rollback to v1.1.9)

Deployment complete and monitored.
Saved deployment record to .sdlc/memory/deployment-AB#123.md

NEXT STEP?
  [1] View production metrics dashboard
  [2] Setup continuous monitoring
  [3] Continue to incident response prep
  [4] Done

User: [3]

v1.2.0 is live in production. Excellent!
```

## CLI Mode

```bash
$ sdlc skill deployment AB#123 --version=1.2.0
$ sdlc skill deployment AB#123 --canary=5%
$ sdlc skill deployment AB#123 --rollback
```

## Monitoring During Deployment

- Real-time latency tracking (P50, P95, P99)
- Error rate monitoring
- Availability verification
- Automatic rollback if thresholds exceeded
- Detailed deployment log

## G11 Gate Clear Conditions

Gate G11 is CLEAR (deployed) when:
- Canary phase 1 passed (5 min monitoring, no errors)
- Canary phase 2 passed (25%, 10 min monitoring)
- Full rollout completed (100%)
- Production metrics meet NFRs
- Deployment record created

## Next Commands

- `/project:monitoring AB#123` - Continuous production monitoring
- `/project:incident-response AB#123` - Incident response automation
- `/project:retrospective AB#123` - Retrospective & learning

---

## Model & Token Budget
- **Model Tier:** Haiku (monitoring result processing)
- Input: ~1K tokens (deployment status)
- Output: ~1.5K tokens (monitoring reports)

