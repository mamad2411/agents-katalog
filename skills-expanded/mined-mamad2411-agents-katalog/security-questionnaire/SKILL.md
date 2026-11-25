---
name: security-questionnaire
description: Complete security questionnaires, assessments, and compliance documentation for customer procurement
user-invocable: true
---

# Security Questionnaire (SQRC) Workflow

This skill guides you through completing security questionnaires and compliance documentation for customer procurement processes using Databricks internal resources.

## Critical Policies

> **🛑 STOP - Azure Databricks:** We are **contractually prohibited** from filling out Azure Databricks questionnaires. This is a liability risk if violated. Route all Azure questionnaires to the Azure team. See go/sqrc/azure for details.

> **⚠️ NO GenAI Answers:** Do NOT use Glean Chat, Perplexity, ChatGPT, or other GenAI tools to generate answers. They frequently contain inaccuracies. **Always use SQRC Search and copy-paste the pre-approved answers.**

> **⚠️ Avoid Custom Answers:** Use pre-built SQRC content whenever possible. Custom answers risk errors and have not been reviewed by security/legal. SQRC answers are reviewed by experts and legal.

> **✅ SQRC First:** Complete **90-95%** of questions using SQRC Search Engine before submitting for review. The SQRC database has 500+ pre-approved answers.

## Prerequisites

Before starting:

1. **Verify NDA status** - Confirm the customer has a signed NDA before sharing sensitive security documentation
2. **Authenticate** - Ensure you have access to:
   - Glean MCP (internal documentation search)
   - Slack MCP (for escalation and expert consultation)
   - Google Docs skill (for reading/creating questionnaire documents)

## Strategy 1: Avoid the Questionnaire

Before filling out a custom questionnaire, **always try to redirect the customer to pre-built content first**. This saves time and ensures accuracy.

**Resources to offer instead of filling custom questionnaires:**

| Resource | Description | Link |
|----------|-------------|------|
| Security & Compliance Package | Comprehensive security documentation bundle | go/scpackage |
| Pre-filled SIG Questionnaire | 700+ pre-answered questions in industry-standard format | go/sig |
| Trust Center | Public security and compliance information | databricks.com/trust |
| Pushback Guide | Scripts for redirecting customers to standard content | go/sqrc/pushback |

**Suggested language to redirect customers:**

> "We have a comprehensive pre-filled security questionnaire with over 700 answers that covers most standard security questions. Would you be willing to review that instead? It's been approved by our security and legal teams."

> "Rather than filling out a custom questionnaire, we can provide our Security & Compliance Package which includes our SOC 2 report, ISO certificates, and detailed security documentation. This typically addresses 90%+ of customer security questions."

**When to proceed with custom questionnaire:**

- Customer explicitly rejects pre-built options
- Questionnaire contains organization-specific questions
- Regulatory requirements mandate specific format

## Phase 1: Triage Flowchart

Follow the decision tree in `resources/TRIAGE_FLOWCHART.md` to determine the appropriate handling path.

```
Read the triage flowchart resource:
/read plugins/fe-workflows/skills/security-questionnaire/resources/TRIAGE_FLOWCHART.md
```

### Quick Decision Summary

1. **Is this Azure Databricks?**
   - **🛑 HARD STOP** - We are contractually prohibited from filling out Azure questionnaires
   - Route ALL Azure Databricks questionnaires to the Azure team - no exceptions
   - See go/sqrc/azure for the proper escalation path

2. **Can go/sqrc answer it?**
   - **ALWAYS** check go/sqrc first for pre-answered questions
   - go/sqrc contains approved responses for 500+ common questions
   - **Copy-paste detailed answers** - do not summarize or paraphrase

3. **Is this ESG/Privacy focused?**
   - ESG (Environmental, Social, Governance) → Route to ESG team
   - Privacy-specific → Route to Privacy team

4. **Deal value threshold**
   - Deals ≥$250K → Submit for review via go/sqrc/submitform
   - Deals <$250K → Self-service using go/sqrc + this skill

## Phase 2: SQRC Completion Workflow

### Step 1: Parse and Categorize Questions

Analyze the questionnaire and categorize each question into one of 9 categories:

| # | Category | Common Topics |
|---|----------|---------------|
| 1 | Policy & People | Training, NDAs, background checks, AUP |
| 2 | Risk Management | Assessments, SOC reports, certifications |
| 3 | Incident Management | SIRT, breach notification, forensics |
| 4 | Physical Security | CSP-inherited, visitor management, media destruction |
| 5 | Infrastructure | Encryption, MFA, patching, network security |
| 6 | Application Security | SDLC, environment segregation, code review |
| 7 | Access Control | SCIM, password policies, least privilege |
| 8 | Business Continuity | DR, RTO/RPO, backups, geographic redundancy |
| 9 | Data Security | PCI, PII, subprocessors, data classification |

See `resources/CATEGORY_GUIDANCE.md` for detailed guidance on each category.

### Step 2: Research Using SQRC (Primary) and Glean (Secondary)

> **⚠️ WARNING:** Do NOT use Glean Chat, Perplexity, or other GenAI tools. Use the SQRC Search API to get **verbatim** pre-approved answers.

**Research Priority Order:**

1. **PRIMARY - SQRC Search API (verbatim answers):** Use Chrome DevTools to query the SQRC database directly and extract word-for-word approved answers. See `resources/SQRC_SEARCH_API.md` for the complete method.
2. **SECONDARY - Glean Search:** Search Glean for supporting evidence (Trust Center docs, security policies, compliance certificates) to supplement SQRC answers.
3. **NEVER:** Generate answers using GenAI - they frequently contain inaccuracies.

**SQRC Search API Quick Reference:**

```
1. Navigate Chrome DevTools to https://platform.sec.databricks.com/kb.html
2. Define the sqrcSearch() function (see resources/SQRC_SEARCH_API.md)
3. Search: JSON.stringify(await sqrcSearch("your query here"), null, 2)
4. Copy the "answer" field VERBATIM into the response
```

For batch searching multiple questions at once, use `batchSqrcSearch()` — see `resources/SQRC_SEARCH_API.md` for the full function and examples.

**Glean for supporting evidence only (not primary answers):**

```bash
# Example: Search for supporting evidence
mcp-cli call glean/glean_read_api_call '{"endpoint": "search.query", "params": {"query": "Databricks SOC 2 Type II report", "page_size": 15}}'
```

See `resources/EVIDENCE_SOURCES.md` for pre-built Glean queries by category.

### Step 3: Apply Maturity Scoring

Score each response using the 1-5 maturity scale:

| Score | Level | Description |
|-------|-------|-------------|
| 5 | Optimized | Continuous improvement, regularly audited, industry-leading |
| 4 | Managed | Measured and controlled, consistently followed (Databricks typical) |
| 3 | Defined | Documented process, may not be consistently applied |
| 2 | Developing | Ad-hoc processes, partial coverage |
| 1 | Initial | No formal process |

See `resources/SCORING_GUIDE.md` for detailed scoring criteria with examples.

### Step 4: Draft Responses

> **CRITICAL - VERBATIM SQRC CONTENT:** When an SQRC source is found, you MUST copy-paste the SQRC answer **word for word, exactly as written**. Do NOT paraphrase, summarize, reword, restructure, or "improve" SQRC content. These answers have been reviewed and approved by security and legal teams. Any modification invalidates that review. The only acceptable change is inserting the customer's name where a placeholder exists.

Use the standard response format from `resources/RESPONSE_TEMPLATE.md`. Every response MUST include an SQRC match status:

```markdown
### Q[#]: [Question text]

**SQRC Match:** [VALIDATED | NO MATCH | UNCERTAIN]
**SQRC Source:** [SQRC entry title/ID or "N/A"]

**Suggested Score:** [1-5]

**Response:** [VERBATIM SQRC answer if VALIDATED. Custom answer flagged for review if NO MATCH.]

**Evidence:**
- [Document/certification 1]
- [Document/certification 2]
```

**SQRC Match definitions:**
- **VALIDATED** - An SQRC entry directly answers this question. Response uses verbatim SQRC content.
- **NO MATCH** - No SQRC entry found. Response is custom and MUST be flagged for security/legal review.
- **UNCERTAIN** - Partial SQRC match exists but question specifics differ. Uses closest verbatim SQRC answer with a note on the difference. Needs review.

### Step 5: Distinguish Databricks vs CSP Controls

**Critical for accurate responses:** Databricks is a separate legal entity from cloud providers.

**Databricks-Owned Controls:**
- ISO 27001/27017/27018/27701 certifications
- SOC 1/2 Type II reports
- PCI-DSS attestation
- HIPAA compliance program
- Security policies and procedures
- Incident response (SIRT)
- Penetration testing program
- SDLC and vulnerability management
- Access control and authentication
- Encryption implementation
- Audit logging

**Inherited from CSPs (AWS, Azure, GCP):**
- Physical data center security
- Physical media destruction
- Network infrastructure redundancy
- Geographic availability zones

**How to frame responses:**
- Lead with Databricks-owned controls
- Reference CSP controls as "inherited" where applicable
- Note that Databricks validates CSP controls through compliance report reviews

## Resources

### Internal Resources

| Resource | URL | Description |
|----------|-----|-------------|
| SQRC Database | go/sqrc | Pre-answered common questions (500+) |
| Submit for Review | go/sqrc/submitform | Submit complex questionnaires for review |
| Trust FAQ | go/trustfaq | Security and compliance FAQ |
| Security Policies | Internal Google Drive | Comprehensive security policy documents |

### Public Resources

| Resource | URL |
|----------|-----|
| Trust Center | https://databricks.com/trust |
| Compliance | https://databricks.com/trust/compliance |
| Security Features | https://databricks.com/trust/security-features |
| Privacy Notice | https://databricks.com/legal/privacynotice |
| Acceptable Use Policy | https://databricks.com/legal/aup |
| Subprocessors | https://databricks.com/legal/databricks-subprocessors |
| Security Addendum | https://databricks.com/legal/security-addendum |

### Documents to Provide to Customers

For customer completion, these documents may be requested:

1. **SOC 2 Type II Report** (NDA required)
2. **SOC 1 Type II Report** (NDA required)
3. **ISO 27001 Certificate**
4. **PCI-DSS Attestation of Compliance** (if applicable)
5. **Enterprise Security Guide** (NDA required, cloud-specific)
6. **Penetration Test Executive Summary** (NDA required)
7. **Data Processing Agreement (DPA)**
8. **Subprocessors List**
9. **Shared Responsibility Model** (cloud-specific)
10. **Security Addendum**

## Escalation Guidelines

### When to Use go/sqrc/submitform

Submit for security team review when:

- Deal value ≥ $250K
- Questions outside standard coverage
- Customer requests custom security terms
- Questions about unreleased features or non-standard configurations
- Azure-specific competitive situations

### When to Engage #security Channel

Use Slack #security channel for:

- Time-sensitive requests
- Clarification on existing answers
- Questions about recent security incidents or vulnerabilities
- Guidance on complex multi-cloud scenarios

### When to Escalate to Trust Team

Contact Trust team directly for:

- Customer-specific security architecture reviews
- Custom compliance attestations
- Regulatory-specific requirements (FedRAMP, StateRAMP, etc.)

## Complex Questionnaires

For questionnaires with 20+ questions or complex security assessments, use the `sqrc-questionnaire` agent:

```
This agent will:
1. Verify this is NOT an Azure questionnaire (HARD STOP check)
2. Parse the entire questionnaire
3. Categorize all questions
4. Research using SQRC Search as primary source
5. Draft responses with evidence (copy-paste from SQRC)
6. Target 90-95% completion before flagging for review
7. Flag items needing escalation
```

## Output: Two Separate Documents

The workflow produces **two separate Google Docs**:

### Document 1: Completed Questionnaire (customer-facing)

Contains ONLY the questions and answers — clean, ready to share with the customer. No internal validation details, no SQRC references, no match statuses. Just the original question numbers/text and the verbatim SQRC answers (or custom answers where no SQRC match exists).

### Document 2: SQRC Validation Report (internal use only)

A separate internal document that validates each answer against SQRC sources. This is for the SA/SE to review before sharing Document 1. Format:

```markdown
# [Customer] Security Questionnaire — SQRC Validation Report

Customer: [Customer Name]
Validated by: Vibe (SQRC Source Validation)
Date: [Date]
Source: go/sqrc (Security and Questionnaire Resource Center)

## Validation Summary

| Question | Validation Status | Notes |
|----------|-------------------|-------|
| Q1 | VALIDATED | Matches SQRC |
| Q2 | VALIDATED (minor note) | Accurate but [detail] not in primary SQRC list |
| Q6 | NEEDS NUANCE | SQRC describes [X]; answer could be more precise |
| Q15 | NO SQRC MATCH | No direct SQRC entry for this question |

## Detailed Validation by Question

### Q[#]: [Full question text]

Questionnaire Answer: [The answer provided in Document 1]

SQRC Validation: [VALIDATED | NEEDS NUANCE | NO SQRC MATCH] — [Detailed explanation
of how the answer compares to SQRC content, including specific SQRC entries referenced
and any discrepancies or notes.]

Sources:
- [SQRC entry title](https://platform.sec.databricks.com/kb.html#/search/{short_id}) — [brief description of what this entry confirms]
- [Supporting document](URL) — [e.g., Trust Center page, DPA, Security Addendum]

---
[Repeat for each question]

## Overall Assessment

- X of Y questions VALIDATED against SQRC sources
- X questions flagged as NEEDS NUANCE
- X questions have NO DIRECT SQRC MATCH

### Key Recommendations
[Specific suggestions for improving flagged answers]
```

## Post-Completion Validation

Before sharing the completed questionnaire (Document 1) with the customer, review the SQRC Validation Report (Document 2):

1. Check all NEEDS NUANCE items — revise answers in Document 1 if the nuance is material
2. Check all NO SQRC MATCH items — these custom answers should be reviewed by security/legal
3. Verify the overall VALIDATED rate meets the 90-95% target
4. Address any Key Recommendations before sharing

## Workflow Summary

```
1. Receive SQRC from customer
   ↓
2. AZURE CHECK (HARD STOP)
   - Is this Azure Databricks? → STOP, route to Azure team
   - Not Azure? → Continue
   ↓
3. Try to AVOID the questionnaire
   - Offer Security Package, SIG, Trust Center
   - Customer insists on custom? → Continue
   ↓
4. Follow Triage Flowchart
   - Check NDA status
   - Check deal value threshold
   - Determine if review needed
   ↓
5. Categorize questions (9 categories)
   ↓
6. Research using SQRC FIRST
   - Search Glean for SQRC answers
   - Copy-paste approved answers (NO GenAI!)
   - Target 90-95% from SQRC
   ↓
7. Draft responses with:
   - SQRC match status (VALIDATED/NO MATCH/UNCERTAIN)
   - VERBATIM SQRC content (do NOT paraphrase)
   - Maturity score (1-5)
   - Supporting evidence
   ↓
8. Distinguish Databricks vs. CSP controls
   ↓
9. Create TWO documents:
   - Document 1: Completed questionnaire (clean, customer-facing)
   - Document 2: SQRC Validation Report (internal review)
   ↓
10. Review Validation Report
   - Check NEEDS NUANCE items
   - Check NO SQRC MATCH items
   - Verify 90-95% VALIDATED target
   ↓
11. Review flagged items with Trust/Security team if needed
    ↓
12. Deliver Document 1 (completed questionnaire) to customer
```
