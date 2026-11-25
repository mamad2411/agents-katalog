# /project:staging-validation

**Interactive Staging Environment Testing & Sign-Off**

Works in: Cursor IDE chat + Claude Code + CLI

## Usage

```
/project:staging-validation AB#123
/project:staging-validation AB#123 --scope=sit
/project:staging-validation AB#123 --sign-off
```

## What This Does

1. **Deploys** to staging environment
2. **Runs smoke tests** (basic functionality)
3. **Executes test suite** (unit, integration, E2E)
4. **Monitors stability** (error rates, latency)
5. **Collects sign-off** from QA and product
6. **Creates validation report** for release readiness

## Interactive Flow

```
User: /project:staging-validation AB#123

Claude: 🚀 Staging Validation & Sign-Off

✅ STORY LOADED:
  Story: Phone verification & OTP (AB#123)
  Version: v1.2.0
  Deployment: Staging environment (eks-staging)

🔄 DEPLOYMENT TO STAGING:

Deploying v1.2.0 to staging...
✓ Container built and pushed to ECR
✓ Database migrations applied
✓ Service deployed (3 replicas)
✓ Health checks passing

📋 TEST EXECUTION:

Running test suite (26 tests):
  ✓ Unit tests: 8/8 passed (2 min)
  ✓ Integration tests: 12/12 passed (3 min)
  ✓ E2E tests: 4/4 passed (5 min)
  ✓ Performance baseline: P95 = 145ms ✓
  ✓ Smoke tests: All critical paths passing

Total: 26/26 tests passed ✓

⏱️ STABILITY MONITORING (10 min):

  P50: 65ms ✓
  P95: 178ms ✓
  P99: 285ms (slightly above, acceptable)
  Error rate: 0.02% ✓
  Availability: 100% ✓
  Memory: 340MB (normal) ✓
  CPU: 45% (normal) ✓

✅ STAGING VALIDATION PASSED

REQUIRE SIGN-OFF?
  [1] Request QA sign-off
  [2] Request Product sign-off
  [3] Request both
  [4] Skip sign-off, proceed

User: [3]

👤 SIGN-OFF REQUESTS:

Sending sign-off requests to:
  • QA Lead: Eve@example-org.com
  • Product Manager: Raj@example-org.com

Waiting for responses...

[30 minutes later...]

✓ QA Sign-off: APPROVED
  Eve: "All test cases passed, ready for UAT"

✓ Product Sign-off: APPROVED
  Raj: "Feature meets acceptance criteria, ready for release"

📊 VALIDATION REPORT:

Test Summary:
  • 26 tests executed
  • 26 tests passed (100%)
  • Coverage: 87%
  • Duration: 15 min

Performance:
  • P95 latency: 178ms (target: <200ms) ✓
  • Error rate: 0.02% (target: <0.1%) ✓
  • Throughput: 1050 RPS (target: >1000 RPS) ✓

Sign-offs:
  • QA: ✓ Approved
  • Product: ✓ Approved

Status: ✅ READY FOR RELEASE

NEXT STEP?
  [1] Create release candidate tag
  [2] Schedule release date
  [3] Proceed to pre-production
  [4] Cancel

User: [3]

Deploying to pre-production...
✓ Pre-prod deployment complete
✓ Validation report saved to .sdlc/memory/staging-validation-AB#123.md
```

## CLI Mode

```bash
$ sdlc skill staging-validation AB#123 --scope=sit
$ sdlc skill staging-validation AB#123 --sign-off
$ sdlc skill staging-validation AB#123 --run-tests
```

## Outputs

- **Test Results**: Full suite execution report
- **Stability Report**: 10-minute baseline metrics
- **Sign-off Records**: QA and Product approvals
- **Validation Report**: PDF summary for release team

## G8 Gate Clear Conditions

Gate G8 is CLEAR when:
- All tests passing on staging (100%)
- Performance baseline meets NFRs
- No critical bugs discovered
- QA sign-off obtained
- Product sign-off obtained

## Next Commands

- `/project:release-prep AB#123` - Release readiness final check
- `/project:deployment AB#123` - Production deployment
- `/project:monitoring AB#123` - Monitoring setup

---

## Model & Token Budget
- **Model Tier:** Haiku (test result processing)
- Input: ~1K tokens (test results + story)
- Output: ~1.5K tokens (report generation)

