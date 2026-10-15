---
name: create-contract
description: Generate a customer-specific enterprise service agreement by filling in the standard template with deal details.
argument-hint: "<proposal file or deal details>"
---

# /create-contract - Enterprise Contract Generation

## MCP connectors

None required. This skill operates on local repo files only.

Generate a customer-specific Enterprise Service Agreement by filling in the standard template with deal-specific details.

**Architecture**: The template lives in `legal/templates/`:
- `enterprise-service-agreement.md` - source of truth (readable, diffable)
- `generate-docx.js` - Node.js script that produces a formatted `.docx` from the template (`npm install docx && node generate-docx.js`)

Customer-specific contracts are generated locally and never committed to git.

**Important**: This produces a draft contract. All contracts must be reviewed by qualified legal counsel before signing.

## Invocation

```
/create-contract <proposal file or deal details>
```

## Workflow

### Step 1: Collect Deal-Specific Fields

The template uses `[TO COMPLETE]` placeholders for all customer-specific information. Collect these from the user's input (proposal, CRM record, or conversation):

**Customer details:**
- Customer legal name
- Jurisdiction and corporate form
- Principal place of business address
- Registry and registration number (if applicable)
- Signatory name and title

**Commercial terms:**
- Enterprise license fee (annual, USD)
- Implementation services fee (one-time, USD)
- Year 1 total
- Renewal fee after Year 1
- Number of implementation days
- Number of follow-up months
- Initial term length (months)

**Scope:**
- Number of tables in initial scope
- Data sources
- Billing contact email
- Technical contacts

If details are missing, prompt the user. For unknown legal entity details, use `[TO COMPLETE]` placeholders and flag them.

### Step 2: Generate the Customer Contract

1. Read the template from `legal/templates/enterprise-service-agreement.md`
2. Fill in all `[TO COMPLETE]` placeholders with the actual deal values
3. Save the filled contract to `legal/_drafts/YYYY-MM-DD_<customer-slug>-enterprise-contract.md`

### Step 3: Generate the formatted .docx

1. Run the docx generator to produce a formatted Word document:
   ```bash
   cd legal/templates && node generate-docx.js
   ```
2. The generator reads the same template and produces `enterprise-service-agreement.docx` with proper formatting (headers, footers, logo, tables, page breaks)
3. Move the generated docx to the drafts folder:
   ```bash
   mv legal/templates/enterprise-service-agreement.docx legal/_drafts/YYYY-MM-DD_<customer-slug>-enterprise-contract.docx
   ```

### Step 4: Review Checklist

Before handing off, verify:
- [ ] All `[TO COMPLETE]` placeholders have been filled
- [ ] Pricing matches the proposal exactly
- [ ] Term and renewal terms are correct
- [ ] Scope of services matches what was proposed
- [ ] Implementation deliverables are listed
- [ ] Customer legal name and address are correct

### Step 5: Summary

Output a deal summary:
- Parties and key contacts
- Total contract value (Year 1 and recurring)
- Key terms (term length, implementation scope)
- Files generated and their locations
- Next steps: legal review, then send for signature

## Notes

- Never fabricate customer legal entity details - use `[TO COMPLETE]`
- Customer-specific files go in `legal/_drafts/` and are gitignored

## Self-improvement

After the CAO reviews and approves a contract:

1. Move the final contract from `legal/_drafts/` to `legal/_published/`
2. Diff what was drafted vs what the CAO (or legal counsel) changed - identify patterns in clause edits
3. Update `legal/_insights.md` with what was changed and why (e.g. "removed auto-renewal for this deal type", "added data residency clause for EU clients")
4. If the edits reveal a recurring pattern, update `legal/templates/enterprise-service-agreement.md` to reflect the new standard position
5. If a contract structure works particularly well for a deal type, save it to `legal/_examples/` as a reference
