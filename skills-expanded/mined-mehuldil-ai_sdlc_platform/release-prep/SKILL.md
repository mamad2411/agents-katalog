# /project:release-prep

**Interactive Release Readiness & Compliance Check**

Works in: Cursor IDE chat + Claude Code + CLI

## Usage

```
/project:release-prep AB#123
/project:release-prep AB#123 --version=1.2.0
/project:release-prep AB#123 --final-check
```

## What This Does

1. **Verifies compliance scans** (SAST, DAST, SCA)
2. **Validates changelog** and release notes
3. **Confirms rollback plan** exists
4. **Checks feature flags** (for gradual rollout)
5. **Creates release checklist** with sign-offs
6. **Generates release notes** for communication

## Interactive Flow

```
User: /project:release-prep AB#123 --version=1.2.0

Claude: 📋 Release Preparation Checklist

✅ STORY LOADED:
  Story: Phone verification & OTP (AB#123)
  Version: v1.2.0
  Status: Approved for release

🔒 COMPLIANCE VERIFICATION:

SAST (Fortify):
  ✓ PASSED - 0 critical, 0 high severity issues
  
DAST (OWASP ZAP):
  ✓ PASSED - 0 critical, 1 medium (SQL injection prevention confirmed)
  
SCA (BlackDuck):
  ✓ PASSED - All dependencies reviewed, no CVEs
  
Container Security (K8s scanning):
  ✓ PASSED - Base image updated to latest

All compliance gates: ✓ PASSED

📝 RELEASE DOCUMENTATION:

Changelog:
  ✓ Updated for v1.2.0
  ✓ Lists new features, bug fixes, breaking changes
  
Release Notes:
  ✓ Customer-facing summary prepared
  ✓ Installation instructions included
  ✓ Known limitations documented
  
Rollback Plan:
  ✓ Rollback procedure documented (5 steps)
  ✓ Rollback triggers defined
  ✓ Pre-rollback validation checklist
  ✓ Post-rollback validation checklist
  ✓ Estimated rollback time: 15 minutes

All documentation: ✓ COMPLETE

🚀 FEATURE FLAGS:

Enable gradual rollout?
  [1] Yes, use feature flags (canary deployment)
  [2] No, full release to 100%
  [3] Hybrid (enable feature flag, but release to all)

User: [1]

Setting up feature flags...
  ✓ Feature flag created: `signup_phone_auth_enabled`
  ✓ Initial rollout: 5% of traffic
  ✓ Monitoring: Error rates, latency
  ✓ Escalation plan: If error rate >1%, rollback automatically

📊 FINAL RELEASE CHECKLIST:

✓ Code reviewed and approved
✓ All tests passing (unit, integration, E2E, performance)
✓ Staged validation complete (QA + Product sign-offs)
✓ Compliance scans passing
✓ Changelog updated
✓ Release notes prepared
✓ Rollback plan documented
✓ Feature flags configured
✓ Monitoring alerts configured
✓ Runbooks prepared

All items: ✓ COMPLETE

🎯 FINAL SIGN-OFF:

Require final release approval?
  [1] Request from Release Manager
  [2] Request from CTO
  [3] Request from both
  [4] Proceed without approval

User: [3]

Sending final approval requests...

[Waiting for responses...]

✓ Release Manager approval: GRANTED
  "v1.2.0 approved for production release"
  
✓ CTO approval: GRANTED
  "Security and architecture review complete"

📦 RELEASE READY

Version: v1.2.0
Release date: 2026-04-12 14:00 UTC
Rollout strategy: Canary (5% → 25% → 100%)
Monitoring: Real-time error tracking
Rollback: 1-command rollback to v1.1.9

CREATE RELEASE TAG?
  [1] Yes, tag v1.2.0 in git
  [2] Preview release notes first
  [3] Schedule release date first
  [4] Cancel

User: [1]

✓ Created git tag v1.2.0
✓ Release notes published
✓ Release prep complete
✓ Ready for deployment (see /project:deployment)
```

## CLI Mode

```bash
$ sdlc skill release-prep AB#123 --version=1.2.0
$ sdlc skill release-prep AB#123 --final-check
$ sdlc skill release-prep AB#123 --create-release-tag
```

## Outputs

- **Compliance Report**: SAST, DAST, SCA results
- **Release Notes**: Customer-facing summary
- **Rollback Runbook**: Step-by-step rollback procedure
- **Release Checklist**: All gates passed

## G10 Gate Clear Conditions

Gate G10 is CLEAR when:
- All compliance scans passing
- Changelog updated with v1.x.x
- Rollback plan documented (5 sections required)
- Release notes approved by Product
- Final approval from Release Manager + CTO

## Next Commands

- `/project:deployment AB#123` - Deploy to production
- `/project:monitoring AB#123` - Set up production monitoring
- `/project:incident-response AB#123` - Prepare incident runbooks

---

## Model & Token Budget
- **Model Tier:** Sonnet (compliance analysis + checklist)
- Input: ~1.5K tokens (story + compliance results)
- Output: ~2K tokens (checklist + release notes)

