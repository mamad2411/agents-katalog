---
name: contractai
description: "Analyze and review contracts with AI-powered insights, risk detection, and clause recommendations. Use when the user needs contract analysis, legal risk assessment, or template generation for agreements, NDAs, or service contracts."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["OPENAI_API_KEY", "CONTRACTAI_API_KEY"],
        "bins": []
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "⚖️"
    }
  }
---

## Overview

ContractAI is an enterprise-grade contract analysis and review skill that leverages advanced AI models to automate legal document evaluation, identify risks, extract key terms, and generate compliance-aligned recommendations. Perfect for legal teams, procurement departments, and business operations—ContractAI reduces review time from hours to minutes while maintaining institutional knowledge.

### Why ContractAI Matters

- **Risk Detection**: Automatically flag unfavorable clauses, liability gaps, and compliance issues
- **Time Savings**: Analyze 50+ page contracts in under 2 minutes
- **Consistency**: Apply standardized review criteria across all agreements
- **Integration Ready**: Works with document management systems (DocuSign, Box, SharePoint), contract platforms (Ironclad, Airtable), and Slack workflows
- **Customizable Templates**: Generate pre-approved contract templates tailored to your industry and risk profile

---

## Quick Start

Try these prompts immediately to explore ContractAI's capabilities:

### Prompt 1: Analyze an Existing Contract
```
Analyze this NDA for risk factors and provide a summary:

[Paste your NDA text here]

Please identify:
- Red flags in confidentiality clauses
- Termination and liability terms
- Non-compete restrictions
- Recommended revisions
```

### Prompt 2: Extract Key Contract Terms
```
Extract and summarize the key commercial terms from this service agreement:

[Paste contract text]

Format as:
- Payment terms
- Service scope
- Liability caps
- Renewal conditions
- Termination clauses
```

### Prompt 3: Generate a Custom Contract Template
```
Generate a Service Agreement template for [YOUR INDUSTRY] with these requirements:
- 30-day termination notice
- $500K liability cap
- Annual renewal with 10% price adjustment
- IP ownership: [CLIENT/VENDOR]
- Include standard SaaS compliance clauses

Format as a ready-to-use Word/PDF template with bracketed placeholders.
```

### Prompt 4: Compliance Check
```
Review this vendor contract against [INDUSTRY STANDARD - e.g., SOC 2, GDPR, CCPA] compliance requirements.

Contract text:
[Paste contract]

Highlight compliance gaps and provide remediation language.
```

---

## Capabilities

### 1. **Automated Contract Analysis**
- **Full-Text Review**: Process contracts up to 100 pages with semantic understanding
- **Risk Scoring**: Quantified risk assessment (Low/Medium/High) for each clause
- **Clause Extraction**: Automatically identify and categorize contract sections
- **Comparison Analysis**: Compare current contract against your standard template

**Example Usage:**
```
Analyze this employment agreement and compare it against our standard template.
Flag any deviations that increase company liability.
```

### 2. **Risk Detection & Alerts**
- **Liability Flags**: Identify uncapped indemnification, broad warranties, or one-sided limitations
- **Compliance Gaps**: Check against GDPR, CCPA, SOC 2, HIPAA, industry-specific regulations
- **Payment Risk**: Detect unfavorable payment terms, currency risks, or hidden fees
- **IP & Confidentiality**: Assess ownership ambiguities and confidentiality scope issues

**Example Usage:**
```
Check this vendor contract for data privacy risks related to GDPR Article 28 requirements.
```

### 3. **Key Term Extraction**
- Payment terms (net 30, net 60, etc.)
- Service scope and deliverables
- Liability caps and insurance requirements
- Renewal, termination, and auto-renewal clauses
- Governing law and dispute resolution
- Intellectual property ownership

### 4. **Template Generation**
- **Industry-Specific Templates**: SaaS, Vendor, Employment, NDA, Service Agreement
- **Customizable Clauses**: Build contracts with your preferred legal language
- **Compliance Pre-Built**: Templates include SOC 2, GDPR, CCPA standard clauses
- **Bracketed Placeholders**: Ready for quick customization with your terms

**Example Usage:**
```
Generate a Master Service Agreement template for a B2B SaaS company with:
- $1M liability cap
- 12-month commitment
- Auto-renewal with 60-day opt-out
- Vendor owns IP, client owns data
```

### 5. **Negotiation Guidance**
- Recommended clause revisions with justification
- Market-standard language suggestions
- Alternative phrasing for contentious terms
- Prioritization: Which clauses to fight for vs. concede

### 6. **Integration & Workflow Automation**
- **Slack Integration**: Get analysis summaries and alerts in Slack channels
- **Google Workspace**: Extract contracts from Drive, store analysis in Sheets
- **Airtable**: Log contract metadata, risk scores, and action items
- **Zapier/Make**: Trigger reviews on new contract uploads
- **Email Integration**: Send analysis reports via email with customizable templates

---

## Configuration

### Environment Variables (Required)
```bash
# OpenAI API key for GPT-4 contract analysis
OPENAI_API_KEY=sk-...

# ContractAI specialized model access (optional for enhanced legal analysis)
CONTRACTAI_API_KEY=ca-...

# Optional: Document storage integration
GOOGLE_DRIVE_API_KEY=...
AIRTABLE_API_KEY=...
SLACK_BOT_TOKEN=xoxb-...
```

### Setup Instructions

1. **API Configuration**
   ```bash
   export OPENAI_API_KEY="your-openai-key"
   export CONTRACTAI_API_KEY="your-contractai-key"
   ```

2. **Integration Setup** (Choose as needed)
   - **Slack**: Add skill to workspace, enable file uploads
   - **Google Drive**: Authorize folder access for contract scanning
   - **Airtable**: Create "Contracts" base with fields: ContractName, RiskScore, Status, AnalysisDate

3. **Custom Template Library**
   - Store approved templates in `/templates/` directory
   - Reference by name: `Use template: SaaS-Standard-2024`

4. **Risk Profile Configuration**
   ```yaml
   risk_tolerance:
     liability_cap_minimum: $500000
     acceptable_payment_terms: "net-30"
     required_compliance: ["SOC2", "GDPR"]
     auto_flag_keywords: ["unlimited", "perpetual", "sole discretion"]
   ```

---

## Example Outputs

### Output 1: Risk Analysis Report
```
CONTRACT: Vendor_SaaS_Agreement_2024.pdf
RISK SCORE: 6.8/10 (MEDIUM)

KEY FINDINGS:
✓ Payment Terms: Favorable (Net 30)
✓ IP Ownership: Clear (Vendor retains)
⚠ Liability Cap: Uncapped indemnification (MEDIUM RISK)
⚠ Termination: 90-day notice required (vs. standard 30)
✗ GDPR Compliance: Missing Data Processing Agreement (HIGH RISK)

RECOMMENDED ACTIONS:
1. Request liability cap of $1M
2. Negotiate termination to 30 days
3. Require DPA addendum before signing

CONFIDENCE: 92%
```

### Output 2: Extracted Terms Summary
```
SERVICE AGREEMENT - ABC Vendor Inc.

PAYMENT TERMS:
- Monthly: $15,000
- Minimum commitment: 12 months
- Auto-renewal: Annual
- Opt-out: 60 days prior

LIABILITY:
- Cap: $1M or 12 months fees (whichever is greater)
- Excluded: Indirect, consequential damages
- Insurance: $2M general liability required

IP OWNERSHIP:
- Vendor retains: Product, platform, tools
- Client retains: Customer data, content
- Client license: Non-exclusive, non-transferable

TERMINATION:
- For convenience: 30 days notice
- For cause: Immediate (material breach)
- Wind-down: 30-day transition period
```

### Output 3: Generated Template
```
MASTER SERVICE AGREEMENT (Template)

1. SERVICES
   [CLIENT] ("Client") engages [VENDOR] ("Vendor") to provide:
   - [SERVICE DESCRIPTION]
   - Service Level: [SLA DETAILS]
   - Support: [SUPPORT HOURS]

2. FEES & PAYMENT
   - Monthly Fee: $[AMOUNT]
   - Minimum Term: [X] months
   - Payment Terms: Net 30 from invoice date
   - Auto-renewal: Annual unless 60-day opt-out notice

3. CONFIDENTIALITY
   [Standard NDA language with GDPR Article 32 data security requirements]

4. LIABILITY
   - Cap: $[X] or 12 months fees
   - Excludes: Indirect, consequential, punitive damages
   - Insurance: Vendor maintains $[X] coverage

5. INTELLECTUAL PROPERTY
   - Vendor IP: [Vendor retains all product IP]
   - Client IP: [Client retains all content/data]
   - License: Non-exclusive, non-transferable

6. TERMINATION
   - For Convenience: [X] days notice
   - For Cause: Immediate upon material breach
   - Wind-down: [X]-day transition period

7. GOVERNING LAW
   [Your jurisdiction - e.g., State of Delaware]

[Additional sections: Data Processing, Compliance, Insurance, etc.]
```

---

## Tips & Best Practices

### 1. **Maximize Analysis Accuracy**
- **Upload clean PDFs**: OCR-scanned documents work best; avoid handwritten notes
- **Provide context**: Tell ContractAI your industry, risk tolerance, and deal type
- **Use custom templates**: Reference your approved template library for consistency
- **Batch analysis**: Review 5+ contracts to establish patterns and risk trends

### 2. **Integrate with Your Workflow**
- **Slack alerts**: Set up channel notifications for HIGH-risk contracts
- **Airtable tracking**: Log all contracts with risk scores for audit trails
- **Calendar triggers**: Automate renewal reminders 90 days before expiration
- **Email summaries**: Weekly digest of all contract actions and approvals

### 3. **Negotiate Smarter**
- **Prioritize battles**: Focus on liability, IP, and termination clauses first
- **Use market data**: Reference industry benchmarks ContractAI provides
- **Track changes**: Use version control to document negotiation rounds
- **Template consistency**: Always start from your standard template, not vendor's

### 4. **Compliance & Risk Management**
- **Regular audits**: Re-analyze contracts annually for regulatory changes
- **Clause library**: Build a repository of approved language for reuse
- **Red-flag keywords**: Configure ContractAI to auto-flag high-risk terms
- **Escalation rules**: Define thresholds for legal team review

### 5. **Time-Saving Shortcuts**
- **Quick summaries**: Use "Extract key terms" for fast overviews
- **Template matching**: Compare against standard to identify deviations in seconds
- **Bulk processing**: Analyze vendor agreements in batch for pattern detection
- **Renewal tracking**: Set calendar reminders for auto-renewal opt-outs

---

## Safety & Guardrails

### What ContractAI Will NOT Do

❌ **Not a Substitute for Legal Counsel**: ContractAI provides analysis and recommendations but cannot replace qualified legal review. Always have an attorney review contracts before signing.

❌ **No Legal Advice**: This skill does not provide legal opinions, litigation strategy, or formal legal counsel. Use for operational efficiency, not legal strategy.

❌ **No Jurisdiction-Specific Guarantees**: Compliance recommendations are general; local laws vary by jurisdiction. Verify against your specific state/country regulations.

❌ **No Binding Interpretations**: Contract interpretations are AI-generated and may miss context. Human judgment is required.

❌ **No Confidentiality Guarantee**: Contracts uploaded are processed via API. Do NOT upload contracts containing extremely sensitive trade secrets without enterprise encryption.

### Limitations & Boundaries

- **Document Size**: Optimal for contracts up to 100 pages; longer documents may require chunking
- **Language Support**: English-language contracts only (other languages may have reduced accuracy)
- **Handwritten Text**: Scanned documents with handwriting have lower OCR accuracy
- **Proprietary Clauses**: Highly specialized/custom clauses may be misinterpreted
- **Real-Time Updates**: Regulatory compliance recommendations reflect training data; always verify current laws
- **Redacted Content**: Heavily redacted contracts cannot be analyzed effectively

### Recommended Safeguards

1. **Always verify** AI-generated recommendations with legal counsel
2. **Use for triage only**: Let ContractAI flag issues, then have lawyers deep-dive
3. **Audit trail**: Log all analyses for compliance and dispute resolution
4. **Access controls**: Restrict contract uploads to authorized team members
5. **Data retention**: Delete sensitive contract copies after analysis (if required)

---

## Troubleshooting

### Q: ContractAI says "High Risk" but I don't understand why. What should I do?
**A:** Request the detailed analysis with specific clause references. ContractAI will highlight the exact language causing the flag. Review with your legal team and decide if the risk is acceptable for your business.

### Q: Can I use ContractAI to review contracts in languages other than English?
**A:** Currently optimized for English. Non-English contracts may have 20-30% reduced accuracy. Recommend translating to English first, then analyzing.

### Q: How do I integrate ContractAI with my document management system (SharePoint, Box, etc.)?
**A:** Use Zapier or Make.com to trigger ContractAI analysis when new contracts are uploaded. Store results in your DMS as metadata or linked reports.

### Q: What happens to my contracts after analysis?
**A:** Contracts are processed in-memory and not permanently stored by default. For audit compliance, you can configure storage in your own cloud (Google Drive, Airtable, etc.). Never store highly sensitive contracts in public cloud without encryption.

### Q: Can ContractAI generate contracts from scratch?
**A:** Yes! Provide your requirements (industry, deal type, key terms, risk profile) and ContractAI generates a customizable template. Always review with legal counsel before use.

### Q: How often should I re-analyze existing contracts?
**A:** Recommend annual re-analysis to catch regulatory changes. Re-analyze immediately if laws change (GDPR updates, new state regulations, etc.).

### Q: Does ContractAI support version control / negotiation tracking?
**A:** Not natively, but integrate with Google Drive or Airtable to track versions. Store each negotiation round with timestamps and changes logged.

### Q: What's the difference between "Low," "Medium," and "High" risk scores?
**A:**
- **Low (0-3)**: Standard terms, minimal deviations from market norms
- **Medium (4-6)**: Some unfavorable clauses; recommend negotiation or legal review
- **High (7-10)**: Significant risks; strongly recommend legal counsel before signing

### Q: Can I customize the risk scoring criteria?
**A:** Yes! Configure risk profiles in your environment settings to prioritize your specific concerns (e.g., prioritize IP over liability if you're a tech company).

### Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| "Invalid API Key" | OPENAI_API_KEY or CONTRACTAI_API_KEY not set | Run `export OPENAI_API_KEY="your-key"` and verify in environment |
| "Document too large" | Contract exceeds 100 pages | Split into sections and analyze separately |
| "Low confidence score" | Poor OCR quality or handwritten text | Re-scan document at higher resolution (300+ DPI) |
| "Timeout error" | Analysis taking >5 minutes | Reduce document size or try again; complex contracts may need chunking |
| "Compliance check failed" | Unrecognized regulation code | Verify regulation name (e.g., "GDPR" vs "EU-GDPR") |

---

## Support & Resources

- **GitHub Issues**: [github.com/ncreighton/empire-skills/issues](https://github.com/ncreighton/empire-skills)
- **Documentation**: Full API reference and integration guides available on ClawHub
- **Community Templates**: Access pre-built contract templates for 50+ industries
- **Training**: Video tutorials on setup, integration