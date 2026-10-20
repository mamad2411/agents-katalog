---
name: fe-customer-courses
description: Generate customer-specific training course recommendations or training plans based on Salesforce use cases, Google Drive research, and the Databricks course catalog. Creates a customer-facing Google Doc with personalized course suggestions. Use this when the user asks for training recommendations, training courses, or a training plan for a customer.
---

# Customer Training Courses Recommendation Skill

Generate personalized Databricks training course recommendations for specific customers. This skill analyzes customer use cases from Salesforce, researches recent account activity in Google Drive, references the official course catalog, and creates a professional customer-facing document with tailored course recommendations.

## Quick Start

**Invoke the `customer-courses-generator` agent** to handle the full workflow:

```
Task tool with subagent_type='fe-workflows:customer-courses-generator' and model='opus'
```

The agent will:
1. Look up customer use cases in Salesforce
2. Identify personas needing training based on use cases
3. Search Google Drive for recent account documents (last 6 months preferred)
4. Reference the course catalog to find relevant available courses
5. Create a customer-facing Google Doc with personalized recommendations
6. Return the document URL

## Input Requirements

The skill requires:
- **Customer name** - The account name to look up in Salesforce
- **Optional context** - Any specific training focus areas or personas mentioned by the user

## Workflow Overview

### Phase 1: Gather Customer Context

#### 1.1 Look Up Salesforce Use Cases

Use the salesforce-actions skill to query active use cases for the customer:

```bash
# First authenticate with Salesforce (if not already authenticated)
# Then query use cases for the account

sf data query --query "SELECT Id, Name, Use_Case_Description__c, Implementation_Status__c,
Stages__c, Business_Value__c, Implementation_Notes__c, Demand_Plan_Next_Steps__c,
Account__r.Name
FROM UseCase__c
WHERE Account__r.Name LIKE '%<customer_name>%'
AND Active__c = true
ORDER BY Stages__c, Name"
```

**Analysis**: Based on the use cases returned, identify:
- **Primary technology areas** (e.g., ML/AI, Data Engineering, Analytics, Migration) - this informs recommendations but won't be shared in detail
- **Stage of implementation** (U1-U6) to understand maturity level
- **Technical complexity** to gauge skill levels needed
- **Key personas** who would benefit from training:
  - Data Engineers
  - Data Scientists
  - Data Analysts
  - ML Engineers
  - Platform/Infrastructure Engineers
  - Business Users

**IMPORTANT**: Use case names and specific details are confidential and for internal research only. They will NOT appear in the final customer-facing document. Map use cases to generic technology areas (ML/AI, Data Engineering, etc.) for the recommendations.

#### 1.2 Confirm Personas with User

**CRITICAL**: Before proceeding, present your analysis to the user and confirm which personas are the priority for training recommendations.

Use AskUserQuestion to confirm:
```
Based on the use cases, I identified these personas that may need training:
- [Persona 1] - [Justification based on use cases]
- [Persona 2] - [Justification based on use cases]
- [Persona 3] - [Justification based on use cases]

Which personas should I focus on for the training recommendations?
```

#### 1.3 Search Google Drive for Recent Documents

Search Google Drive for documents related to this customer from the last 6 months to understand:
- Current engagement level
- Technical challenges discussed
- Skills gaps mentioned
- Project timelines

Use the google-auth skill first to ensure authenticated, then search:

```bash
# Search for customer-related documents from last 6 months
# Look for meeting notes, technical discussions, architecture docs
```

Focus on finding:
- Meeting notes mentioning training needs
- Technical blockers that training could address
- Project documentation showing skill gaps
- Any previous training discussions or requests

### Phase 2: Reference Course Catalog

#### 2.1 Fetch Available Courses

Access the course catalog spreadsheet:
```
https://docs.google.com/spreadsheets/d/1ekfGIA_dbYlVt3DlYkDW6i3_ZdCk-cm4TzQa-bNVb8I/edit?gid=381494619#gid=381494619
```

Use the google-docs skill (NOT WebFetch) to read the spreadsheet and extract course data.

**CATALOG COLUMN STRUCTURE** - The spreadsheet has these columns:
- Course Name
- Added to Jira for pre-reqs
- Added to Jira for accreditations
- Badge/Accreditation
- **Content links - Docebo (Admin links)** ← COST INFO IS HERE
- Content links - Uplimit (Admin links)
- Technical Pillar/Topic
- Tech Level
- Duration
- **Modalities** ← delivery format ONLY (SP, ILT, Blended, HDC), NOT cost
- Labs available
- Availability

**CRITICAL - PARSING COST FROM DOCEBO LINKS**:
There is **NO dedicated Cost column**. Cost information is embedded in the "Content links - Docebo (Admin links)" column as combined strings. You MUST parse it correctly:

- **Format**: Entries contain tags like `SP All - Free`, `SP Cust - Paid/Lab`, `ILT Cust - Public`
- **"Free" tag** → a free tier is available for this course
- **"Paid" or "Paid/Lab" tag** → a paid tier exists (typically includes lab access)
- **Many courses have BOTH free and paid tiers** listed as numbered entries, e.g.: `1. SP All - Free 2. SP Cust - Paid/Lab`
- **"SP" means Self-Paced (delivery format), NOT Free** — do NOT equate SP with Free pricing
- **"ILT" means Instructor-Led Training (delivery format)**, also NOT a cost indicator

**Cost parsing rules**:
1. If the Docebo field contains ONLY "Free" tags → Cost = "Free"
2. If the Docebo field contains ONLY "Paid" or "Paid/Lab" tags → Cost = "Paid"
3. If the Docebo field contains BOTH "Free" AND "Paid/Lab" tags → Cost = "Free & Paid (with labs)"
4. If the Docebo field is empty or unclear → Cost = "Contact Databricks Academy"

**CRITICAL**: Only consider courses with "Customer" or "Available to Customers" in the Availability column. Do not recommend internal-only courses.

**NOTE**: Course URLs are NOT in the catalog spreadsheet - they will be found in Step 2.3.

#### 2.2 Match Courses to Personas and Use Cases

For each confirmed persona, identify relevant courses that:
- Match the technical level based on use case maturity
- Address the specific use case domains (ML, DE, Analytics, etc.)
- Fit the implementation stage (foundational for U2-U3, advanced for U5-U6)
- Build on each other (prerequisites first)

#### 2.3 Find Course URLs Using WebSearch

**CRITICAL**: Course URLs are NOT in the catalog. Use WebSearch to find them.

For each course you plan to recommend:
1. Use WebSearch with the query: `"Course Name" site:databricks.com/training/catalog`
2. Extract the course URL from the results (typically `https://www.databricks.com/learn/training/course-name`)
3. **Parallelize searches** - Make multiple WebSearch calls in one message for efficiency

**Example batch searches (run in parallel)**:
```
WebSearch: "Generative AI Fundamentals" site:databricks.com/training/catalog
WebSearch: "Machine Learning with Databricks" OR "Get Started with ML" site:databricks.com/training/catalog
WebSearch: "Data Analysis with Databricks" OR "SQL Analytics" site:databricks.com/training/catalog
```

This is required for the Link column in the final document.

### Phase 3: Create Recommendations Document

#### 3.1 Structure the Document

Create a markdown file at `/tmp/customer_training_recommendations.md` with this structure:

```markdown
# Training Course Recommendations for [Customer Name]

## Executive Summary

Based on our analysis of your organization's Databricks implementation and goals, we recommend a tailored training plan to accelerate time-to-value and build internal expertise.

### Target Personas
- **[Persona 1]** - [Brief rationale for focus]
- **[Persona 2]** - [Brief rationale for focus]
- **[Persona 3]** - [Brief rationale for focus]

## Recommended Training Path

The following courses are organized by level, from foundational to advanced. Teams should start with foundation courses before progressing to intermediate and advanced topics. All courses can be accessed through [Databricks Academy](https://customer-academy.databricks.com/learn).

### Foundation Level

| Course Name | Target Audience | Duration | Cost | What You'll Learn |
|-------------|----------------|----------|------|-------------------|
| [Course Title] | [Persona] | [Duration] | Free/Paid | [Key learning outcomes] |
| [Course Title] | [Persona] | [Duration] | Free/Paid | [Key learning outcomes] |

### Intermediate Level

| Course Name | Target Audience | Duration | Cost | What You'll Learn |
|-------------|----------------|----------|------|-------------------|
| [Course Title] | [Persona] | [Duration] | Free/Paid | [Key learning outcomes] |
| [Course Title] | [Persona] | [Duration] | Free/Paid | [Key learning outcomes] |

### Advanced Level

| Course Name | Target Audience | Duration | Cost | What You'll Learn |
|-------------|----------------|----------|------|-------------------|
| [Course Title] | [Persona] | [Duration] | Free/Paid | [Key learning outcomes] |
| [Course Title] | [Persona] | [Duration] | Free/Paid | [Key learning outcomes] |

## Focus Area Recommendations

### [Technology Area - e.g., Machine Learning, Data Engineering, Analytics]

**Recommended for**: [Personas]

**Priority Courses**:
1. **[Course]** ([Free/Paid]) - [Why relevant to this technology area]
2. **[Course]** ([Free/Paid]) - [Why relevant to this technology area]
3. **[Course]** ([Free/Paid]) - [Why relevant to this technology area]

## Implementation Guidance

We recommend starting with Foundation level courses to establish common platform knowledge across your team, then progressing to Intermediate and Advanced courses as team members build expertise. The progression through levels should be based on your team's learning pace and project requirements.

### Support Resources
- **Databricks Academy**: [https://customer-academy.databricks.com/learn](https://customer-academy.databricks.com/learn)
- **Training Catalog**: [https://www.databricks.com/training/catalog](https://www.databricks.com/training/catalog)
- **Community Forums**: [https://community.databricks.com/](https://community.databricks.com/)
- **Documentation**: [https://docs.databricks.com/](https://docs.databricks.com/)

## Next Steps

1. Review and approve the recommended training plan with your leadership team
2. Identify specific individuals for Data Engineer and Platform Engineer tracks
3. Visit [Databricks Academy](https://customer-academy.databricks.com/learn) to register and enroll in courses
4. Schedule foundation training sessions to begin the learning journey
5. Plan hands-on projects aligned with your goals to apply learned skills
6. Establish a process for tracking course completion and knowledge sharing

---

*This training plan was created based on analysis of your organization's Databricks implementation goals. For questions or to customize this plan, please contact your Databricks account team.*
```

#### 3.2 Content Guidelines

**Free vs Paid Clarity** (parsed from the Docebo content links column — see Phase 2.1):
- Use "Free" ONLY when the Docebo links field contains a "Free" tag and NO "Paid" tags
- Use "Paid" when the Docebo links field contains ONLY "Paid" or "Paid/Lab" tags
- Use "Free & Paid (with labs)" when BOTH free and paid tiers exist for the same course
- **DO NOT equate "Self-Paced" (SP) delivery format with "Free" pricing** — SP is a delivery modality, not a cost tier
- Group courses by level (Foundation, Intermediate, Advanced) rather than by cost
- **DO NOT include cost estimates** - paid course pricing varies by customer

**Customer-Facing Language**:
- Professional and consultative tone
- Focus on business value and learning outcomes
- Avoid internal jargon or acronyms (no UCO, stages, etc.)
- **DO NOT include specific timelines or week-based guidance** - learning pace varies widely
- **DO NOT include internal success metrics** - this is an external-facing document

**Table Formatting**:
- Use markdown tables for the training path (Foundation, Intermediate, Advanced)
- **MUST include 6 columns**: Course Name, Target Audience, Duration, Cost, What You'll Learn, Link
- **Link column MUST contain embedded hyperlinks** formatted as `[Course Link](URL)` where URL is from the catalog
- Include a note above the table: "All courses can be accessed through [Databricks Academy](https://customer-academy.databricks.com/learn)"
- Course URLs are found via WebSearch (Step 2.3), NOT from the catalog spreadsheet

**Personalization**:
- **DO NOT reference specific use case names or internal details** - the document may be shared widely
- Use generic technology areas (ML, Data Engineering, Analytics, etc.) instead of specific use case names
- Tie course recommendations to general business goals and common patterns
- Focus on personas and skill development rather than project-specific details
- Use use case data only to inform which technology areas and personas to focus on

#### 3.3 Create Formatted Google Doc

Use the google-docs skill (NOT the MCP) to create a properly formatted document:

```bash
# Use the markdown converter from google-docs skill
# Use the markdown_to_gdocs.py script from the google-docs skill
python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-docs/resources/markdown_to_gdocs.py \
  --input /tmp/customer_training_recommendations.md \
  --title "Training Course Recommendations for [Customer Name]"
```

This ensures:
- Proper heading hierarchy (Title, H1, H2, H3)
- Bold formatting for emphasis
- Embedded hyperlinks
- Formatted tables
- Professional appearance

### Phase 4: Return Result

Return to the user:

```
Created training recommendations document for [Customer Name]: https://docs.google.com/document/d/XXX/edit

Summary:
- Analyzed [N] active use cases
- Identified [N] target personas for training
- Recommended [N] total courses organized by level (Foundation, Intermediate, Advanced)
- Clear distinction between free and paid courses

Personas covered:
- [Persona 1] - [N] courses recommended
- [Persona 2] - [N] courses recommended
- [Persona 3] - [N] courses recommended

Technology areas addressed:
- [Technology Area 1] - [Course count] relevant courses
- [Technology Area 2] - [Course count] relevant courses

Next step: Review and share the document with the customer
```

## Quality Checklist

Before returning, verify:

- [ ] Technology areas (not specific use cases) are represented in customer-facing document
- [ ] All recommended courses are available to customers (checked Availability column)
- [ ] Cost column is parsed from Docebo content links (NOT assumed from delivery format)
- [ ] Courses with both free and paid tiers show "Free & Paid (with labs)"
- [ ] Training path is formatted as tables (Foundation, Intermediate, Advanced)
- [ ] **Tables have 6 columns including Link column with embedded hyperlinks**
- [ ] **Link column uses `[Course Link](URL)` format with actual course URLs from catalog**
- [ ] Table includes note linking to Databricks Academy portal
- [ ] Each course includes target audience and learning outcomes
- [ ] NO cost summary included (pricing varies by customer)
- [ ] NO specific timelines or week-based guidance (learning pace varies)
- [ ] NO internal success metrics (external-facing document)
- [ ] Technology area recommendations are provided (no confidential use case details)
- [ ] Document is professionally formatted (not raw markdown)
- [ ] Implementation guidance is general and flexible
- [ ] Support Resources includes link to customer-academy.databricks.com

## Common Pitfalls

1. **Including internal-only courses** - Always filter by Availability column
2. **Confusing free vs paid** - Parse cost from the Docebo content links column, NOT the Modalities column. "SP" means Self-Paced (delivery format), not Free. Many courses have both free and paid tiers
3. **Not using table format** - Training path must be organized in tables by level
4. **Missing Link column** - Tables MUST have 6 columns including a Link column with embedded hyperlinks
5. **Link column not embedded** - Links must be formatted as `[Course Link](URL)`, not plain URLs
6. **Missing course URLs** - URLs are NOT in catalog; use WebSearch with `site:databricks.com/training/catalog`
7. **Not parallelizing WebSearch** - Make multiple WebSearch calls in one message for efficiency
8. **Missing Academy portal link** - Always include note linking to customer-academy.databricks.com
6. **Including cost estimates** - Never include cost summary or pricing estimates
7. **Including timelines** - No week-based guidance; learning pace varies widely
8. **Including internal metrics** - No success metrics; document is customer-facing
9. **Leaking confidential information** - Never reference specific use case names
10. **Skipping user confirmation** - Always confirm personas before proceeding
11. **Raw markdown output** - Always use markdown_to_gdocs.py converter
12. **Outdated course info** - Always fetch latest catalog data

## Example Invocations

```
User: Create training recommendations for Meta
→ Agent looks up Meta use cases, confirms personas, creates tailored doc

User: Generate a course plan for Acme Corp focusing on data engineering
→ Agent focuses on DE persona, filters courses accordingly

User: Make training recommendations for our ML use cases at BigCo
→ Agent prioritizes ML/AI courses based on use case analysis
```

## Resources

- Course Catalog: https://docs.google.com/spreadsheets/d/1ekfGIA_dbYlVt3DlYkDW6i3_ZdCk-cm4TzQa-bNVb8I/edit?gid=381494619#gid=381494619
- Salesforce UseCase object reference: plugins/fe-salesforce-tools/skills/salesforce-actions/resources/USECASE.md
- Google Docs creation: plugins/fe-google-tools/skills/google-docs/
- Salesforce authentication: plugins/fe-salesforce-tools/skills/salesforce-authentication/
