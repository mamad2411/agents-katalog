---
name: procurement-compliance
description: >
  Ensure procurement compliance — policy alignment, regulatory requirements,
  audit trail documentation, exception handling, and training.
  TRIGGER when: user says /procurement-compliance or asks about procurement policy compliance.
argument-hint: "[compliance area or audit finding]"
user-invocable: true
---
# Procurement Compliance
## Process
### Step 1: Map Compliance Requirements
| Source | Requirements |
|--------|-------------|
| Internal policy | Approval thresholds, preferred suppliers, competitive bids |
| Regulatory | Industry-specific procurement rules |
| Contractual | Customer/partner flow-down requirements |
| Financial | Budget controls, segregation of duties |
### Step 2: Assess Current Compliance
| Control | Status | Gap |
|---------|--------|-----|
| Competitive bidding (>$X) | ✅/❌ | [description] |
| Approval authority limits | ✅/❌ | [description] |
| Preferred supplier usage | ✅/❌ | [description] |
| Contract execution | ✅/❌ | [description] |
| Documentation retention | ✅/❌ | [description] |
### Step 3: Address Gaps
| Gap | Remediation | Owner | Timeline |
|-----|-----------|-------|----------|
| [gap] | [action] | [name] | [date] |
### Step 4: Implement Controls
| Control | Automation | Monitoring |
|---------|-----------|-----------|
| Spend thresholds | System-enforced limits | Monthly report |
| Supplier approval | Onboarding workflow | Quarterly review |
| Contract compliance | Expiry alerts | Weekly scan |
### Step 5: Train Stakeholders
| Audience | Content | Frequency |
|----------|---------|-----------|
| Buyers | Policy updates, system training | Quarterly |
| Approvers | Authority limits, red flags | Annual |
| New hires | Procurement policy overview | Onboarding |
## Output Format
```markdown
## Procurement Compliance: [Scope]
### Requirements: [Mapped controls]
### Assessment: [Current compliance status]
### Gaps: [Findings with remediation]
### Training: [Plan]
```
## Quality Checklist
- [ ] All compliance sources mapped
- [ ] Current state assessed against requirements
- [ ] Gaps have remediation plans
- [ ] Controls are automated where possible
- [ ] Training program covers all stakeholders
## Edge Cases
- For government contracting, additional FAR/DFAR requirements apply
- If exceptions are frequent, review whether policies are realistic
- For decentralized purchasing, focus on visibility and monitoring
