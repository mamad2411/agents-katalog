# Pre-Start & Upwork Integration Guide

## 🚀 Pre-Start Process

### Purpose
The pre-start phase ensures project readiness before planning begins. It validates business artifacts, capacity, and Upwork contract readiness.

### Required Artifacts
```bash
# Check pre-start completion
ls -la memory-bank/business/
ls -la memory-bank/upwork/
ls -la memory-bank/plan/
```

**Required Business Artifacts**:
- `memory-bank/business/client_score.json` - Client evaluation
- `memory-bank/business/capacity_report.md` - Resource availability
- `memory-bank/business/pricing.ratecard.yaml` - Pricing structure
- `memory-bank/business/estimate_brief.md` - Project estimation
- `memory-bank/plan/proposal.md` - Client proposal

### Pre-Start Execution
```bash
# Run complete pre-start process
python3 tools/prestart/prestart_composite.py

# Check preflight status
cat workflow_state.json | grep phase
```

## 💼 Upwork Integration

### Contract Types & Requirements

#### Fixed-Price Contracts
**Requirements**:
- Escrow must be funded before planning
- Client must have sufficient funds

**Validation**:
```bash
# Check escrow status
cat memory-bank/upwork/offer_status.json | grep escrow_funded
```

#### Hourly Contracts
**Requirements**:
- Work Diary must be enabled
- Weekly cap hours must be set (> 0)

**Validation**:
```bash
# Check hourly contract readiness
cat memory-bank/upwork/offer_status.json | grep -E "(work_diary_ready|weekly_cap_hours)"
```

### Upwork Kits Available
- **Connects Policy** - `.cursor/rules/kits/upwork/connects_policy.mdc`
- **Contract Guard** - `.cursor/rules/kits/upwork/contract_guard.mdc`
- **Upwork Adapter** - `.cursor/rules/kits/upwork/upwork_adapter.mdc`

## 🔒 Pre-Start Gates

### Business Readiness Gate
```bash
# Check business artifacts
python3 tools/prestart/prestart_composite.py --check-business
```

**Gate Conditions**:
- All required business artifacts exist
- Client score meets minimum threshold
- Capacity report shows availability
- Pricing structure is defined
- Estimate is within capacity

### Upwork Readiness Gate
```bash
# Check Upwork readiness
python3 tools/prestart/prestart_composite.py --check-upwork
```

**Fixed-Price Gate**:
- Contract type = "fixed"
- Escrow funded = true

**Hourly Gate**:
- Contract type = "hourly"
- Work Diary ready = true
- Weekly cap hours > 0

## 📋 Pre-Start Kits

### Available Kits
- **Client Screener** - `.cursor/rules/kits/prestart/client_screener.mdc`
- **Capacity Planner** - `.cursor/rules/kits/prestart/capacity_planner.mdc`
- **Pricing Policy** - `.cursor/rules/kits/prestart/pricing_policy.mdc`
- **Estimate Sizer** - `.cursor/rules/kits/prestart/estimate_sizer.mdc`
- **Proposal Builder** - `.cursor/rules/kits/prestart/proposal_builder.mdc`
- **Risk Catalog** - `.cursor/rules/kits/prestart/risk_catalog.mdc`
- **Scope Guard** - `.cursor/rules/kits/prestart/scope_guard.mdc`

### Kit Execution
```bash
# Run specific kit
python3 tools/prestart/[kit_name].py

# Check kit output
ls -la memory-bank/business/
```

## 🚦 Workflow States

### State Transitions
1. **PRE_START** → Initial state after `/preflight`
2. **PLAN** → After all gates pass
3. **EXECUTE** → During AI persona execution
4. **AUDIT** → During quality validation
5. **COMPLETE** → Project completion

### State Monitoring
```bash
# Check current state
cat workflow_state.json

# Monitor state changes
tail -f logs/state_transitions.log
```

## 🔍 Troubleshooting Pre-Start

### Common Issues
1. **Missing Artifacts**: Run specific kit to generate
2. **Gate Failures**: Check validation requirements
3. **Upwork Issues**: Verify contract configuration
4. **Capacity Problems**: Update availability in capacity report

### Debug Commands
```bash
# Enable debug mode
export ADVANCEDRULES_DEBUG=1

# Run pre-start with verbose output
python3 tools/prestart/prestart_composite.py --verbose

# Check specific gate status
python3 tools/prestart/prestart_composite.py --gate-status
```

## ✅ Success Criteria

### Pre-Start Complete
- All business artifacts generated
- Client score meets requirements
- Capacity confirmed available
- Pricing structure defined
- Upwork contract ready

### Ready for Planning
```bash
# Verify readiness
python3 tools/prestart/prestart_composite.py --final-check

# Proceed to planning
python3 tools/run_role.py planning_ai
```
description:
globs:
alwaysApply: true
---
