---
name: uco-consumption-analysis
description: Analyze Use Case Objects (UCOs) against actual consumption data to validate stages, identify missing UCOs, and create actionable progression plans following the gold standard U1-U6 framework
---

# UCO Consumption Analysis Skill

Comprehensive UCO portfolio analysis that ties Salesforce UCO data to actual product consumption, validates stage alignment, identifies missing UCOs backed by consumption evidence, and provides specific actions to progress UCOs through the U1-U6 lifecycle.

**Gold Standard Reference**: [Consumption Exit Criteria Slide](https://docs.google.com/presentation/d/1PflhGvWgyiRRF9WzsNncOouoR09IEiTSNz3DoqKaYF0/edit?slide=id.g2fec4661351_0_32)

## When to Use This Skill

Use this skill when you need to:
- Validate UCO stages (U1-U6) against actual consumption data
- Identify consumption that isn't captured in any UCO
- Create missing UCOs backed by consumption evidence
- Provide stage progression plans with entry/exit criteria
- Generate UCO-centric reports for leadership

**Key Principle**: UCO tracking should match consumption reality, not lag behind it.

## Prerequisites

Before running this analysis:

1. **Salesforce Authentication**: Use `/salesforce-authentication` skill
2. **Databricks Authentication**: Use `/databricks-authentication` skill
3. **Account Name**: Know which account to analyze (see "My Accounts" scoping below)
4. **Jargon Lookup**: If you encounter unfamiliar acronyms (e.g., DNB, FSI, PubSec), use `/internal-jargon` skill to look them up

### "My Accounts" Scoping

If the user asks to analyze "my accounts" or "my UCOs" without specifying an account name, you must first identify which accounts are theirs. **See `ACCOUNT_LOOKUP.md` and `LOGFOOD_QUERIES.md` in the `salesforce-actions` skill resources for the role-aware scoping approach using AccountTeamMember.**

Quick summary:
1. Get user's Salesforce ID from their email
2. Query `AccountTeamMember` to discover their role and accounts
3. For SAs: filter by `TeamMemberRole = 'Primary Solution Architect'`
4. For AEs: filter by `TeamMemberRole = 'Account Executive'`
5. If no AccountTeamMember entries, fall back to UCO assignment fields (`Primary_Solution_Architect__c`, `Solution_Architect__c`, `rsa__c`, `DSA__c`)

## Instructions

### Step 1: Gather UCO Data from Salesforce

Use the `/salesforce-actions` skill to get all active UCOs for the target account:

```bash
# Find account ID
sf data query --query "SELECT Id, Name FROM Account WHERE Name LIKE '%<ACCOUNT_NAME>%'"

# Get all active UCOs with GenAI/product-specific fields
# NOTE: If the user asked for "my UCOs", add a filter for their assignment:
#   AND (Primary_Solution_Architect__c = '<USER_ID>' OR Solution_Architect__c = '<USER_ID>'
#        OR rsa__c = '<USER_ID>' OR DSA__c = '<USER_ID>')
sf data query --query "SELECT Id, Name, Stages__c, Implementation_Status__c,
  Use_Case_Description__c, Demand_Plan_Next_Steps__c,
  Implementation_Start_Date__c, Full_Production_Date__c,
  UseCaseInPlan__c, Solution_Architect__r.Name,
  Primary_Solution_Architect__r.Name, rsa__r.Name, DSA__r.Name,
  LastModifiedDate, Monthly_DBUs__c, Business_Value__c
  FROM UseCase__c
  WHERE Account__c = '<ACCOUNT_ID>'
  AND Active__c = true
  ORDER BY Stages__c"
```

**Focus Areas**:
- UCOs in U5 (Onboarding) or U6 (Live) - These should have consumption
- Target dates that have passed - Check if actually live
- Health status (Red/Yellow/Green) - Correlate with consumption trends
- "In Plan" status - Should match consumption evidence

### Step 2: Gather Consumption Data

Use the `/logfood-querier` skill to get actual product consumption. This skill uses direct SQL queries against the GTM data tables.

```bash
# Use the logfood-querier skill which references GTM_DATA.md for table schemas
/logfood-querier

# Example queries to run via /databricks-query:
# Get product consumption breakdown (last 3-6 months)
SELECT product_category, SUM(dbu_consumption) as total_dbus, 
       DATE_TRUNC('month', usage_date) as month
FROM main.gtm_data.c360_consumption_monthly
WHERE account_name LIKE '%<ACCOUNT_NAME>%'
  AND usage_date >= DATEADD(month, -6, CURRENT_DATE())
GROUP BY product_category, DATE_TRUNC('month', usage_date)
ORDER BY month, total_dbus DESC

# Get workspace-level consumption details
SELECT workspace_name, workload_type, SUM(dbu_consumption) as total_dbus
FROM main.gtm_data.c360_consumption_monthly  
WHERE account_name LIKE '%<ACCOUNT_NAME>%'
  AND usage_date >= DATEADD(month, -3, CURRENT_DATE())
GROUP BY workspace_name, workload_type
ORDER BY total_dbus DESC
```

**Key Metrics to Capture**:
- Total consumption by product (DBUs and $ cost)
- Monthly trends (growth/decline)
- Top consuming workspaces
- GenAI adoption metrics (if any)
- Product mix percentages

### Step 3: Validate UCO Stages Against Consumption

For each UCO, apply the **Gold Standard U1-U6 Exit Criteria**:

#### **U1 - Validating**
- **Exit Criteria**: Customer ready for technical discussion with SA
- **Consumption**: None expected
- **Validation**: N/A for consumption analysis

#### **U2 - Scoping**
- **Exit Criteria**: Use case prioritized, quick-sized, customer ready to evaluate
- **Consumption**: None expected (planning stage)
- **Validation**: No consumption required

#### **U3 - Evaluating**
- **Exit Criteria**: Technical win achieved and sizing updated
- **To Move to U3**: Customer tech deep dive, preliminary sizing, evaluation plan
- **Consumption**: May have pilot/POC consumption (small, exploratory)
- **Validation**: Check for small workload consumption (pilot DBUs)
- **CRITICAL**: Must reach U3 for funding approval

#### **U4 - Confirming**
- **Exit Criteria**: Customer ready to onboard
- **To Move to U4**: Tech win achieved, sizing update, budget & resources confirmed
- **Consumption**: Should see pilot/POC consumption with measurable DBUs
- **Validation**: Validate consumption exists and aligns with sizing estimates

#### **U5 - Onboarding**
- **Exit Criteria**: Target run rate achieved
- **To Move to U5**: Customer budget & resources confirmed, timelines & business value defined
- **Consumption**: **MUST have measurable production consumption**
- **Validation**:
  - Query consumption for workspaces/workloads related to UCO
  - Verify monthly DBU consumption matches projected run rate
  - Check if implementation start date has passed

#### **U6 - Live**
- **Exit Criteria**: None (final stage)
- **To Move to U6**: Projected DBUs are now in production
- **Consumption**: **MUST have sustained production consumption**
- **Validation**:
  - Verify consumption is stable and sustained (2+ months)
  - Consumption should match or exceed target run rate
  - If Target Live Date passed and no consumption: CRITICAL FLAG
  - All U6 UCOs should be marked "In Plan = Yes"

### Step 4: Identify Stage Mismatches

**Common Mismatches**:

1. **U6 (Live) with No Consumption**
   - **Issue**: UCO marked live but no DBUs detected
   - **Action**: Downgrade to U5 or U4 depending on blocker
   - **Root Cause**: Implementation delayed or failed

2. **U5 (Onboarding) Past Implementation Date with No Consumption**
   - **Issue**: Implementation start date passed but no consumption
   - **Action**: Investigate blocker, update date or downgrade stage
   - **Root Cause**: Customer delays, technical blockers

3. **U4/U5/U6 Marked "Out of Plan" Despite Consumption**
   - **Issue**: UCO generating revenue but not in forecast
   - **Action**: Update "In Plan" status to Yes immediately
   - **Root Cause**: Salesforce hygiene issue

4. **Yellow/Red Health Status Without Investigation**
   - **Issue**: Health flag set but no next steps documented
   - **Action**: Query consumption trends, update Next Steps field
   - **Root Cause**: Lack of consumption visibility

### Step 5: Identify Missing UCOs Backed by Consumption

**Critical Gap Pattern**: Large consumption with no corresponding UCO

**Detection Method**:
1. Sum all U5/U6 UCO consumption (estimated or documented)
2. Compare to total account consumption
3. Gap > 20% = Missing UCO(s)

**Example**:
- Total account consumption: $10,000/month
- UCO portfolio consumption: $2,000/month
- **Gap: $8,000/month (80%) - CRITICAL MISSING UCOs**

**For Each Product with Significant Consumption**:

| Product | Consumption Threshold | Recommended UCO Stage |
|---------|---------------------|---------------------|
| SQL/Warehouse | >$500/month or >10% of total | U6 (Live) if sustained 2+ months |
| GenAI Products | >$100/month or any measurable | U6 if 2+ months, U5 if ramping |
| Delta Lake | >$500/month or >15% of total | U6 (foundational product) |
| Unity Catalog | >$300/month or active migration | U6 if complete, U5 if in progress |
| Model Serving | >$50/month or any measurable | U6 if production, U4 if pilot |
| Vector Search | >$100/month or any measurable | U6 if production, U5 if ramping |
| Serverless | >$500/month or >20% of total | U6 (infrastructure adoption) |

**Missing UCO Template**:
```
UCO Name: [Product] [Use Case Description]
Stage: U6 (Live) or U5 (Onboarding) based on consumption maturity
Implementation Start Date: [When consumption began]
Target Live Date: [Current date if U6, future date if U5]
Health Status: Green (if stable), Yellow (if declining)
In Plan: Yes (if generating revenue)
Monthly DBUs: [Actual consumption from data]
Business Value: [Infer from product type and consumption level]
```

### Step 6: Create Missing UCOs in Salesforce

For each missing UCO identified in Step 5, create it using `/salesforce-actions`:

```bash
# Create UCO
sf data create record --sobject UseCase__c \
  --values "Name='[UCO Name]' \
  Account__c=[ACCOUNT_ID] \
  Stages__c=U6 \
  Implementation_Status__c=Green \
  Implementation_Start_Date__c=2025-08-01 \
  Full_Production_Date__c=2025-10-15 \
  UseCaseInPlan__c=true \
  Monthly_DBUs__c=5000 \
  Active__c=true \
  Use_Case_Description__c='[Description based on consumption patterns]' \
  Demand_Plan_Next_Steps__c='[Date] - [Initials] - Created UCO to capture existing production consumption. Monthly run rate: $X. [Next action]'"

# Verify creation
sf data query --query "SELECT Id, Name, Stages__c FROM UseCase__c WHERE Account__c = '[ACCOUNT_ID]' ORDER BY CreatedDate DESC LIMIT 1"
```

**Best Practices**:
- Always set `Active__c=true`
- Document creation rationale in `Demand_Plan_Next_Steps__c`
- Use actual consumption start date for `Implementation_Start_Date__c`
- Mark `UseCaseInPlan__c=true` if U5+ and consuming
- Assign Solution Architect if known

### Step 7: Create Stage Progression Plans

For each UCO not yet at U6, provide **specific actions** to advance stages:

**Template for Stage Progression**:

```markdown
### UCO: [Name]
**Current Stage**: [U2/U3/U4/U5]
**Target Stage**: [U3/U4/U5/U6]
**Consumption Evidence**: [None/Pilot/Production/Amount]

#### To Move to [Next Stage] (Requirements):
- [Requirement 1 from gold standard exit criteria]
- [Requirement 2]
- [Requirement 3]

#### Exit Criteria:
- [Exit criterion from gold standard]

#### Actions Required:
1. **[Action 1]** - [Owner] - [Timeline]
   - Details: [Specific steps]
   - Success Metric: [How to measure]

2. **[Action 2]** - [Owner] - [Timeline]
   - Details: [Specific steps]
   - Success Metric: [How to measure]

#### Risk Flags:
- [Risk 1]: [Mitigation]
- [Risk 2]: [Mitigation]
```

**Example**:

```markdown
### UCO: Genie Space for Supply Chain Team
**Current Stage**: U3 (Evaluating)
**Target Stage**: U4 (Confirming)
**Consumption Evidence**: None (pilot phase expected)

#### To Move to U4 (Requirements):
- Tech Win Achieved
- Sizing Update
- Customer Budget & Resources Confirmed
- Agreement to Move Forward

#### Exit Criteria:
- Customer ready to onboard

#### Actions Required:
1. **Deploy Genie Space Pilot** - Solution Architect - 30 days
   - Details: Create supply chain Genie space, load sample data, train 3-5 users
   - Success Metric: Users generate 10+ queries with actionable insights

2. **Measure Pilot Consumption** - Solution Architect - During pilot
   - Details: Track DBU consumption, query patterns, user satisfaction
   - Success Metric: Projected run rate of $50-100/month

3. **Document Technical Win** - Account Executive - End of pilot
   - Details: Capture user testimonials, business value metrics, cost savings
   - Success Metric: Executive sponsor approval to proceed

4. **Update Sizing with Actual Data** - Solution Architect - End of pilot
   - Details: Replace preliminary sizing with actual consumption from pilot
   - Success Metric: Updated Monthly_DBUs__c field in Salesforce

5. **Secure Budget & Resources** - Account Executive - Q1 2026
   - Details: Confirm FY26 budget allocation, team capacity
   - Success Metric: Signed commitment to production deployment

#### Risk Flags:
- **No exec sponsor**: Identify and engage supply chain VP
- **User adoption concerns**: Provide hands-on training, use case templates
- **Budget constraints**: Show ROI vs current analytics tooling
```

### Step 8: Generate UCO-Centric Report

**Report Structure** (following the ButcherBox example format):

1. **Executive Summary**
   - UCO portfolio overview (count by stage)
   - Consumption vs UCO tracking gap ($ amount, % untracked)
   - Key finding (e.g., "Consumption ahead of UCO tracking")
   - Immediate actions summary

2. **Current UCO Portfolio by Stage**
   - Table with: Name, Stage, Target Dates, Health, Consumption Evidence, Validation Status
   - Group by stage (U2, U3, U4, U5, U6)

3. **UCO Stage Validation Against Consumption**
   - For each UCO in U5/U6: Validate consumption evidence
   - Flag mismatches (no consumption, dates passed, health issues)

4. **Missing UCOs Backed by Consumption**
   - Total consumption gap ($ and %)
   - For each missing UCO:
     - Recommended stage (U4/U5/U6)
     - Consumption evidence (DBUs, $, product)
     - Business value description
     - Entry criteria met
     - Action: CREATE UCO

5. **Stage Progression Plans**
   - For each UCO not at U6:
     - Current stage validation
     - Next stage requirements (from gold standard)
     - Specific actions with owners and timelines
     - Exit criteria
     - Risk flags

6. **UCO Action Plan by Timeline**
   - **Immediate (This Week)**: CREATE missing UCOs, VALIDATE U5/U6, PROMOTE ready UCOs
   - **Q1 (30-60 Days)**: Progress U3→U4, U4→U5 with specific pilots
   - **Q2 (60-120 Days)**: Progress U5→U6, new U2→U3 evaluations
   - **Q3-Q4 (120+ Days)**: Expansion UCOs, strategic initiatives

7. **Revenue Impact by UCO**
   - Table: UCO Name, Stage, Current Monthly, Target Monthly, FY Total, Status
   - Scenario analysis: Conservative, Base Case, Aggressive
   - Map revenue to specific UCO stages and actions

8. **Key Risks & Mitigations**
   - UCO tracking lag risk
   - Stage misalignment risk
   - Pipeline stagnation risk
   - Each with: Indicator, Impact, Mitigation, Owner

9. **Success Metrics**
   - UCOs with validated consumption (target: 100% of U5+)
   - Consumption captured in UCOs (target: >90%)
   - Stage progression rates (U2→U3, U5→U6)
   - "In Plan" accuracy (target: 100% of U5+)

10. **Conclusion & Next Steps**
    - Week 1 actions (CREATE, VALIDATE, PROMOTE)
    - Month 1-2 actions (PROGRESS stages with specific pilots)
    - Quarter 2-4 actions (ACHIEVE U6, EXPAND existing)

**Format Output As**:
- Google Doc (use `/google-docs` skill with markdown source)
- Include tables with proper formatting
- Bold key metrics (growth rates, revenue targets, gaps)
- Use bullet lists for actions
- Reference gold standard slide in introduction

## Gold Standard U1-U6 Framework Reference

### Stage Definitions & Exit Criteria

| Stage | Name | Exit Criteria | Consumption Expectation |
|-------|------|--------------|------------------------|
| **U1** | Validating | Customer ready for technical discussion | None |
| **U2** | Scoping | Use case prioritized, quick-sized, ready to evaluate | None |
| **U3** | Evaluating | Technical win achieved, sizing updated | Pilot/POC (small) |
| **U4** | Confirming | Customer ready to onboard | Pilot consumption validated |
| **U5** | Onboarding | Target run rate achieved | **Production consumption** |
| **U6** | Live | None (final stage) | **Sustained production** |

### Critical Gates

- **U2 → U3**: Need for funding approval (CRITICAL MILESTONE)
- **U4 → U5**: Budget & resources confirmed, agreement to move forward
- **U5 → U6**: Projected DBUs in production, run rate achieved

### Key Fields by Stage

| Field | U1-U2 | U3 | U4 | U5 | U6 |
|-------|-------|----|----|----|----|
| Implementation_Start_Date__c | Empty | Empty | Empty | **Required** | **Required** |
| Full_Production_Date__c | Empty | Empty | Empty | **Required** | **Required** |
| Implementation_Status__c | - | Optional | Optional | **Required** | **Required** |
| UseCaseInPlan__c | No | No | Optional | Optional | **Yes** |
| Monthly_DBUs__c | - | Preliminary | Refined | **Actual** | **Actual** |
| Demand_Plan_Next_Steps__c | Basic | Detailed | Detailed | **Weekly** | **Weekly** |

## Common Pitfalls

### Pitfall #1: Not Querying Consumption by Workspace/Workload
**Problem**: Can't tie aggregate consumption to specific UCOs
**Solution**: Always query consumption with workspace names and workload types

### Pitfall #2: Assuming U6 Means Consuming
**Problem**: UCOs marked U6 but not validated against consumption
**Solution**: ALWAYS validate U5/U6 UCOs have actual consumption evidence

### Pitfall #3: Not Creating Missing UCOs
**Problem**: Large consumption goes untracked, leadership has blind spots
**Solution**: If consumption >$100/month for 2+ months with no UCO → CREATE UCO

### Pitfall #4: Vague Stage Progression Actions
**Problem**: "Work with customer to progress" (not actionable)
**Solution**: Use gold standard exit criteria → specific actions with owners and timelines

### Pitfall #5: Ignoring "In Plan" Status
**Problem**: U5/U6 UCOs marked "Out of Plan" despite consuming
**Solution**: If U5+ and consuming → set UseCaseInPlan__c = true

### Pitfall #6: Not Documenting Rationale
**Problem**: Why was stage changed or UCO created? (lost context)
**Solution**: Always update Demand_Plan_Next_Steps__c with reasoning and data

## Resources

- **Gold Standard Slide**: [Consumption Exit Criteria](https://docs.google.com/presentation/d/1PflhGvWgyiRRF9WzsNncOouoR09IEiTSNz3DoqKaYF0/edit?slide=id.g2fec4661351_0_32)
- **UCO Fields Reference**: `plugins/fe-salesforce-tools/skills/salesforce-actions/resources/USECASE.md`
- **UCO Weekly Updates**: `/uco-updates` skill (for U2+ UCOs)
- **Salesforce Operations**: `/salesforce-actions` skill
- **Consumption Analytics**: `/logfood-querier` skill
- **Google Docs Creation**: `/google-docs` skill

## Example Output

See the ButcherBox GenAI UCO Analysis as the exemplar:
- **Google Doc**: [ButcherBox GenAI UCO Expansion Plan - FY2026](https://docs.google.com/document/d/16WnPRvNYIAdv1LlVLLVsi6tM1cM6Z0SqqIfFoB4YXBs/edit)
- **Key Features**:
  - 5 existing GenAI UCOs validated against $2,302 consumption
  - 3 missing UCOs identified (Production ML, Vector Search, Foundation Integration)
  - Stage-specific progression plans with actions, owners, timelines
  - Revenue mapped to UCO stages ($11K-15K FY26 target)
  - Immediate/Q1/Q2-Q4 action timeline

---

**Summary**: This skill transforms raw consumption data into actionable UCO intelligence by validating stages against the gold standard U1-U6 framework, identifying gaps, and providing specific progression plans. The output is UCO-centric, leadership-ready, and drives revenue visibility.
