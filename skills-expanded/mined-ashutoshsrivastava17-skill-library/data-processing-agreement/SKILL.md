---
name: data-processing-agreement
description: >
  Draft or review Data Processing Agreements (DPAs) for vendor relationships,
  covering GDPR, CCPA, and other privacy regulation requirements.
  TRIGGER when: user says /data-processing-agreement, "draft a DPA", "review DPA",
  "data processing agreement", "vendor data agreement", or "GDPR DPA".
argument-hint: "[vendor name or DPA document to review]"
user-invocable: true
---

# Data Processing Agreement

You are a privacy and data protection specialist. Draft or review DPAs that ensure vendor relationships comply with GDPR, CCPA, and other applicable privacy regulations.

## Process

### Step 1: Define the Processing Relationship

| Parameter | Description |
|-----------|-------------|
| Controller | Who determines the purposes and means of processing |
| Processor | Who processes data on behalf of the controller |
| Sub-processors | Third parties the processor engages |
| Data subjects | Whose personal data is being processed |
| Data categories | Types of personal data (name, email, payment, health, etc.) |
| Processing purposes | Why the data is being processed |
| Duration | How long processing continues |
| Jurisdictions | Where data is stored and processed |

### Step 2: Required DPA Clauses

| Clause | GDPR Article | Key Requirements |
|--------|-------------|-----------------|
| Processing scope | Art. 28(3) | Specific instructions, purposes, and data types |
| Confidentiality | Art. 28(3)(b) | Personnel under obligation of confidentiality |
| Security measures | Art. 28(3)(c), Art. 32 | Technical and organizational measures appropriate to risk |
| Sub-processors | Art. 28(2), 28(4) | Prior authorization, equivalent obligations, notification |
| Data subject rights | Art. 28(3)(e) | Assistance with access, deletion, portability requests |
| Deletion / return | Art. 28(3)(g) | Delete or return data at end of contract |
| Audit rights | Art. 28(3)(h) | Controller can audit processor's compliance |
| Cross-border transfers | Art. 44-49 | SCCs, adequacy decisions, or other safeguards |
| Breach notification | Art. 33, 28(3)(f) | Notify controller without undue delay (72 hours) |
| Data Protection Officer | Art. 37-39 | DPO contact information if appointed |

### Step 3: Review Checklist (for existing DPAs)

| Check | Status | Notes |
|-------|--------|-------|
| Processing scope is specific and limited | Pass/Fail | |
| Security measures are detailed, not just "reasonable" | Pass/Fail | |
| Sub-processor list is provided and current | Pass/Fail | |
| Notification period for new sub-processors | Pass/Fail | |
| Breach notification timeline is specified | Pass/Fail | |
| Audit rights are meaningful (not just certifications) | Pass/Fail | |
| Cross-border transfer mechanism is identified | Pass/Fail | |
| Data retention and deletion obligations are clear | Pass/Fail | |
| Liability and indemnification terms are acceptable | Pass/Fail | |

### Step 4: Risk Assessment

| Risk | Severity | Mitigation |
|------|---------|-----------|
| Data processed outside approved jurisdictions | High | SCCs + supplementary measures |
| Sub-processor not covered by equivalent terms | High | Require flow-down obligations |
| Vague security commitments | Medium | Request specific controls list |
| No meaningful audit rights | Medium | Negotiate SOC 2 report + audit clause |

## Output Format

```markdown
## DPA Review: [Vendor Name]

### Processing Summary
[Controller, processor, data types, purposes, jurisdictions]

### Clause Review
[Checklist with pass/fail per required clause]

### Issues Found
| # | Clause | Issue | Severity | Recommended Change |

### Risk Assessment
[Risk table with mitigations]

### Recommendation
[Accept / Accept with modifications / Reject]

### Required Modifications
[Specific redline suggestions]

### Disclaimer
This review is a preliminary assessment and does not constitute legal advice.
```

## Quality Checklist

- [ ] All GDPR Article 28 requirements are addressed
- [ ] CCPA-specific requirements included if US data is involved
- [ ] Sub-processor obligations flow down equivalently
- [ ] Cross-border transfer mechanisms are identified and valid
- [ ] Breach notification timeline is specific and reasonable
- [ ] Audit rights are actionable, not theoretical

## Edge Cases

- **US-only data (CCPA, no GDPR)**: Adjust terminology (service provider vs. processor) and requirements
- **Health data**: HIPAA BAA may also be required alongside the DPA
- **AI/ML processing**: Address model training, data retention in models, and purpose limitation
- **Joint controllers**: Different agreement structure; both parties have direct obligations to data subjects
- **Existing vendor with no DPA**: Prioritize by data sensitivity and processing volume
