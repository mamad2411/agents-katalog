---
name: fe-answer-customer-questions
description: Draft responses to customer questions from Slack, email, or Google Docs. Researches answers using multiple sources and creates a combined Q&A document with references. Use this skill when anyone mentions "customer questions", "product", "roadmap", "draft responses"
---

# Answer Customer Questions Skill

This skill drafts responses to customer questions by researching answers from public documentation, internal knowledge bases, and Slack discussions. It creates a single combined document with all questions, proposed answers, confidence ratings, and references.

## Quick Start

**Invoke the `customer-question-answerer` agent** to handle the full workflow:

```
Task tool with subagent_type='fe-workflows:customer-question-answerer' and model='opus'
```

Pass the source of customer questions (Google Doc URL, Slack thread, or raw text). The agent will:
1. Extract and categorize questions from the source
2. Research each question using public docs, Glean, and Slack
3. Compile all findings into a single formatted Google Doc
4. Return the document URL

## Input Sources

The skill accepts questions from:

| Source | How to Provide |
|--------|----------------|
| Google Doc | Provide the docs.google.com URL |
| Slack thread | Provide the Slack message URL or channel + timestamp |
| Raw text | Paste questions directly |
| Email | Copy email content with questions |

## Research Methodology

For each question, the agent:

1. **Categorizes the question** by topic area (Identity, Compute, Storage, etc.)
2. **Searches public documentation** via docs.databricks.com/llms.txt
3. **Searches Glean** for internal documentation and FAQs
4. **Searches Slack** for recent discussions and PM/engineering confirmations
5. **Assigns confidence rating** (1-10) based on source quality and agreement

## Output Document Format

The output is a **single combined Google Doc** with all questions and answers, NOT individual documents per question.

### Document Structure

```markdown
# [Source Name] - Customer Questions & Draft Responses

## [Category 1: e.g., Identity & Access Management]

### Q1: [Question text]

**Answer:** [Direct answer to the question]

**Key points:**
- Point 1
- Point 2

**Code example (if applicable):**
```sql
SELECT * FROM example;
```

**Confidence Level:** X/10

**References:**
- https://docs.databricks.com/...
- https://internal-doc-link

---

### Q2: [Next question in category]
...

## [Category 2: e.g., Serverless & Jobs]
...

## Questions Requiring Further Research

[List of questions that need PM/engineering confirmation]

## Relevant Slack Channels

| Topic | Channel |
|-------|---------|
| Topic 1 | #channel-name |
```

### Formatting Requirements

The output document MUST be properly formatted using Google Docs styles:

| Element | Requirement |
|---------|-------------|
| Title | Use TITLE style for document title |
| Categories | Use HEADING_1 style |
| Questions | Use HEADING_2 or HEADING_3 style |
| Bold text | Use actual bold formatting, not **asterisks** |
| Code blocks | Use monospace font formatting |
| Bullet lists | Use `createParagraphBullets`, not text bullets |
| Links | Embed hyperlinks in text |

**CRITICAL:** Use the `markdown_to_gdocs.py` script from the google-docs skill to convert markdown to properly formatted Google Docs:

```bash
# Use the markdown_to_gdocs.py script from the google-docs skill
python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-docs/resources/markdown_to_gdocs.py \
  --input /tmp/draft_responses.md \
  --title "Customer Questions & Draft Responses"
```

## Workflow Steps

### Step 1: Extract Questions

Read the source document/message and extract all questions. Categorize them by topic:

- **Identity & Access Management** - SCIM, Okta, groups, service principals
- **Managed Tables & Storage** - Unity Catalog storage, S3, managed tables
- **Cost & Billing** - System tables, cost tracking, billing reconciliation
- **Serverless & Jobs** - Serverless compute, job configuration, environments
- **Dashboards & BI** - AI/BI dashboards, alerts, usage tracking
- **Monitoring & Audit** - Audit logs, usage tracking, compliance
- **Queries & Performance** - Query optimization, timeouts, termination
- **Compute & Clusters** - Warehouses, clusters, web terminal
- **Infrastructure & DevOps** - Terraform, DR, deployment

### Step 2: Research Each Question

For each question, use the product-question-researcher methodology:

1. **Check public docs** - Fetch relevant pages from docs.databricks.com
2. **Search Glean** - Find internal documentation
3. **Search Slack** - Find recent discussions

Weight sources by recency and authority:
- PM statements: HIGHEST weight
- Public documentation: HIGH weight
- Engineering confirmations: HIGH weight
- Internal FAQs: HIGH weight
- Field experience: MEDIUM weight
- Old discussions (3+ months): LOW weight

### Step 3: Compile Draft Document

Create a markdown file with all questions and answers following the output format above.

Key elements for each answer:
- **Direct answer** - Clear, actionable response
- **Key points** - Bullet list of important details
- **Code examples** - SQL/Python/API examples where helpful
- **Confidence level** - 1-10 rating with brief justification
- **References** - Links to sources (public docs, internal docs)

### Step 4: Create Formatted Google Doc

Use the google-docs-creator skill to create a properly formatted document:

```python
# Write markdown to temp file
with open('/tmp/draft_responses.md', 'w') as f:
    f.write(markdown_content)

# Convert to Google Doc using markdown converter
# This produces proper headings, bold, code blocks, and links
```

### Step 5: Return Result

Return:
1. Google Doc URL
2. Summary of questions answered
3. List of questions requiring follow-up

## Example Invocations

```
User: Answer the customer questions in this doc: https://docs.google.com/document/d/ABC123/edit
→ Agent extracts questions, researches each, creates combined Q&A doc

User: Draft responses to these questions from our sync meeting: [pasted text]
→ Agent parses questions, researches, creates formatted doc

User: Help me respond to these Slack questions: https://databricks.slack.com/archives/C123/p456
→ Agent reads thread, researches questions, creates response draft
```

## Differences from product-question-research

| Aspect | product-question-research | fe-answer-customer-questions |
|--------|---------------------------|------------------------------|
| Input | Single question | Multiple questions from a source |
| Output | One doc per question | Single combined doc for all questions |
| Format | Detailed research format | Concise Q&A format |
| Use case | Deep dive on one topic | Batch response preparation |

## Resources

- `fe-google-tools/skills/google-docs/resources/markdown_to_gdocs.py` - Markdown to Google Docs converter
- `fe-workflows/agents/product-question-researcher.md` - Research methodology reference
- `fe-workflows/agents/customer-question-answerer.md` - Agent implementation
