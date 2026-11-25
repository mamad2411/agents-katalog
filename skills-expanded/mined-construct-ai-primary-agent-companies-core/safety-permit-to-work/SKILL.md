---
title: Permit to Work Management
description: Management of permit-to-work processes including application, approval, execution, and closure for high-risk activities in the ConstructAI HSE system
frequency: Per work activity requiring permit
success_rate: 98%
tags:
  - domainforge_ai
  - safety
  - permit-to-work
  - 02400_safety
docs:
  - docs_construct_ai/disciplines/02400_safety/agent-data/domain-knowledge/02400_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/02400_safety/agent-data/prompts/02400_AI-NATIVE-SAFETY-OPERATIONS-PROMPT.md
---

# Permit to Work Management

## Overview
End-to-end management of permit-to-work (PTW) processes for high-risk activities including hot work, confined space, working at height, electrical isolation, excavation, and lifting operations. Primary agent: HSE Safety Manager.

## Triggers
- Work activity requiring permit identified
- Work method change requiring different permit type
- Permit extension request
- Emergency work requiring expedited permit
- Permit suspension or cancellation

## Prerequisites
- Work scope and location identified
- Risk assessment completed for the activity
- Qualified personnel available for the work
- Required safety equipment identified and available
- Authorization hierarchy defined

## Steps

### Step 1: Permit Type Classification
Classify permit type based on work activity:
- **Hot Work Permit** → Welding, cutting, grinding, open flame
- **Confined Space Permit** → Entry into tanks, vessels, pits, enclosed spaces
- **Working at Height Permit** → Work above 1.8m without edge protection
- **Electrical Isolation Permit** → Work on energized systems or isolation verification
- **Excavation Permit** → Ground excavation, trenching, underground work
- **Lifting Permit** → Critical lifts (over 75% crane capacity, tandem lifts)

### Step 2: Hazard Identification
Identify all hazards associated with the permitted activity:
- Review work location and surroundings
- Check adjacent activities that may conflict
- Identify environmental hazards (weather, atmospheric conditions)
- Identify equipment and material hazards

### Step 3: Control Measures
Define required control measures for each hazard:
- Specify personal protective equipment (PPE)
- Define isolation requirements (LOTO, gas testing, barricades)
- Specify atmospheric monitoring requirements
- Define emergency response arrangements
- Specify supervision and monitoring requirements

### Step 4: Authorization Workflow
Route permit through authorization chain:
1. **Submit** → Issuer submits permit application
2. **Review** → Safety reviewer checks completeness
3. **Approve** → Authorizing person approves permit
4. **Accept** → Performing team accepts permit
5. **Monitor** → Continuous monitoring during work
6. **Close** → Work complete, site cleared, permit closed

### Step 5: Permit Execution & Monitoring
- Verify all control measures are in place before work starts
- Monitor conditions continuously during work
- Conduct periodic checks per permit requirements
- Document any permit suspensions or condition changes
- Ensure permit displayed at work location

### Step 6: Permit Closure
- Verify work complete and site cleared
- Remove all temporary safety measures
- Confirm no outstanding hazards
- Record lessons learned and observations
- Archive permit record

## Success Criteria
- Correct permit type identified and applied
- All hazards identified with appropriate controls
- Authorization chain completed before work starts
- Permit displayed and conditions monitored
- Permit properly closed and archived

## Common Pitfalls
1. **Wrong permit type** → Incorrect classification leads to inadequate controls
2. **Missing adjacent hazards** → Check surrounding activities before approval
3. **Expired permits** → Track permit expiry and extension requests
4. **Incomplete closures** → Ensure all closure steps are verified

## Cross-References
- `safety/hazard-identification/SKILL.md` — Hazard identification source
- `safety/inspection-workflow/SKILL.md` — Permit inspection during execution