---
name: financialforce-skill-update
description: View and update the FinancialForce/Certinia Skill Matrix (pse__Skill_Certification_Rating__c). Use when the user asks to view their skills, update skill ratings, add new skills, check certifications, see what skills they're missing, or manage their skill matrix in FinancialForce.
---

# FinancialForce Skill Matrix Update

View, add, and update skill and certification ratings (`pse__Skill_Certification_Rating__c`) in Salesforce/FinancialForce. Allows resources to manage their Skill Matrix — the self-reported inventory of technical skills, certifications, languages, and domain expertise.

## Prerequisites

1. **Salesforce CLI authenticated** — run `sf org display` to verify. If not connected, follow the `salesforce-authentication` skill.
2. **Target org alias** — identify which org to use via `sf org list`. Pass `--target-org <alias>` on every command.

## Data Model

### Skill Catalog — `pse__Skill__c`

The master list of all skills and certifications (≈176 records). Each has:
- **`Name`** — Skill name (e.g., "Python", "Delta Lake", "Data Engineer Associate")
- **`pse__Type__c`** — Category grouping (e.g., "01Programming Languages", "04Data Science and Machine Learning", "07Cloud")
- **`pse__Skill_Or_Certification__c`** — `Skill` or `Certification`
- **`RecordType.Name`** — `Skill`, `Certification`, or `Category`
- **`pse__Group__c`** — Optional sub-group (e.g., "Databricks SME")

### Skill Ratings — `pse__Skill_Certification_Rating__c`

The junction object linking a resource (Contact) to a skill with a proficiency rating:
- **`pse__Resource__c`** — Contact ID (the resource)
- **`pse__Skill_Certification__c`** — Skill ID from the catalog
- **`pse__Rating__c`** — Proficiency level (picklist, context-dependent — see below)
- **`pse__Numerical_Rating__c`** — Numeric version of the rating
- **`pse__Aspiration__c`** — Boolean — the resource wants to learn/improve this skill
- **`pse__Certified__c`** — Boolean
- **`pse__Years_Experience__c`** — Number
- **`pse__Notes__c`** — Freetext notes
- **`pse__Approval_Status__c`** — `Saved`, `Submitted`, `Approved`, `Rejected`
- **`pse__Date_Achieved__c`** — Date the skill/cert was achieved
- **`pse__Last_Used_Date__c`** — Date last used

### Rating Scale

The `pse__Rating__c` picklist values depend on the skill type:

| Context | Value | Numerical |
|---------|-------|-----------|
| **Skills** | `1 - No experience` | 1 |
| | `2 - Can deliver need prep time` | 2 |
| | `3 - Can deliver` | 3 |
| | `4 - SME` | 4 |
| **Languages** | `5 - Can Speak` | 5 |
| | `6 - Can Write` | 6 |
| | `7 - Can Speak & Write` | 7 |
| **Certifications** | `8 - Yes` | 8 |
| | `9 - No` | 9 |
| **Migrations** | `0 - Has done migration` | 0 |

**CRITICAL:** Always use the correct rating values for the skill type. A programming language skill uses 1–4. A spoken language uses 5–7. A certification uses 8–9. Do NOT mix them.

### Skill Categories

| Type Code | Category | Typical Rating Scale |
|-----------|----------|---------------------|
| 01Programming Languages | Python, Java, R, Scala, SQL | 1–4 |
| 02Platform Administration | Terraform, E2, Observability | 1–4 |
| 03Data Engineering | Delta Lake, DLT, Streaming, CI/CD | 1–4 |
| 04Data Science and Machine Learning | MLflow, Deep Learning, NLP & LLMs | 1–4 |
| 05SQL and DW | DBSQL, Data Modeling, Unity Catalog | 1–4 |
| 06Ecosystem | Airflow, dbt, Kafka, Snowflake | 1–4 |
| 07Cloud | AWS/Azure/GCP services | 1–4 |
| Migrations | Hadoop, Teradata, Snowflake migrations | 0 or 1–4 |
| Packages | JumpStart, Lakehouse Buildout, CoE | 1–4 |
| 08Verticals/Domain Expertise | Financial Services, Healthcare | 1–4 |
| Specialty Skills | Geospatial, Graph, Image/Vision | 1–4 |
| 09Languages | English, German, Mandarin, etc. | 5–7 |
| 01Certification | Data Engineer Associate, ML Professional | 8–9 |
| 10Other Skills | Project Management | 1–4 |

## Workflow

### Step 1 — Identify the Resource

The user is typically updating their own skills. Look up the resource by name on the **Contact** object:

```bash
sf data query \
  --query "SELECT Id, Name FROM Contact WHERE Name = '<resource_name>'" \
  --target-org <alias>
```

If unsure of the name, search by partial match:

```bash
sf data query \
  --query "SELECT Id, Name FROM Contact WHERE Name LIKE '%<partial>%'" \
  --target-org <alias>
```

### Step 2 — Query Current Skills

Retrieve all existing skill ratings for the resource:

```bash
sf data query \
  --query "SELECT Id, pse__Skill_Certification__r.Name, \
      pse__Skill_Certification__r.pse__Type__c, \
      pse__Skill_Certification__r.pse__Skill_Or_Certification__c, \
      pse__Rating__c, pse__Numerical_Rating__c, \
      pse__Years_Experience__c, pse__Certified__c, \
      pse__Aspiration__c, pse__Notes__c, \
      pse__Approval_Status__c, pse__Last_Used_Date__c \
    FROM pse__Skill_Certification_Rating__c \
    WHERE pse__Resource__r.Name = '<resource_name>' \
    ORDER BY pse__Skill_Certification__r.pse__Type__c, \
             pse__Skill_Certification__r.Name" \
  --target-org <alias>
```

### Step 3 — Display the Skill Matrix

**You MUST always display the skill matrix grouped by category.** Present in a clear tabular format:

```
**Skill Matrix — <Resource Name>**

### Programming Languages
| Skill | Rating | Aspiration | Notes |
|-------|--------|------------|-------|
| Python | 4 - SME | | |
| SQL | 3 - Can deliver | | |
| Java | 1 - No experience | Yes | Want to learn |

### Data Engineering
| Skill | Rating | Aspiration | Notes |
|-------|--------|------------|-------|
| Delta Lake | 3 - Can deliver | | |
| Streaming | 2 - Can deliver need prep time | | |

### Certifications
| Certification | Status | Date Achieved |
|---------------|--------|---------------|
| Data Engineer Associate | 8 - Yes | 2024-03-15 |
| ML Professional | 9 - No | |

### Languages
| Language | Proficiency |
|----------|-------------|
| English | 7 - Can Speak & Write |
| German | 7 - Can Speak & Write |

**Summary: XX skills rated | XX at SME level | XX certifications earned**
```

Display rules:
- Group by `pse__Type__c` using the friendly category name (strip the number prefix for display, e.g., "01Programming Languages" → "Programming Languages")
- Within each group, sort alphabetically by skill name
- Only show the Aspiration column if any skill in the group has `pse__Aspiration__c = true`
- Only show the Notes column if any skill in the group has notes
- Show the summary line at the bottom with counts

### Step 4 — After Displaying the Matrix

Offer the user actions:

> *"You can:*
> - *Update a rating — "update Python to SME", "change Delta Lake to 4"*
> - *Add a skill — "add Agent Bricks as Can deliver"*
> - *Mark a certification — "mark GenAI Engineer as Yes"*
> - *Set aspiration — "I want to learn Graph"*
> - *Add notes — "add note to NLP: completed LLM bootcamp"*
> - *See what's missing — "what skills don't I have yet?"*
> - *View by category — "show me just my cloud skills"*"

## Updating a Skill Rating

### Update an Existing Rating

When the user asks to update a skill, find the existing `pse__Skill_Certification_Rating__c` record:

```bash
sf data query \
  --query "SELECT Id, pse__Rating__c, pse__Numerical_Rating__c \
    FROM pse__Skill_Certification_Rating__c \
    WHERE pse__Resource__r.Name = '<resource_name>' \
      AND pse__Skill_Certification__r.Name = '<skill_name>'" \
  --target-org <alias>
```

Then update it:

```bash
sf data update record \
  --sobject pse__Skill_Certification_Rating__c \
  --record-id <rating_id> \
  --values "pse__Rating__c='<new_rating>' pse__Numerical_Rating__c=<num>" \
  --target-org <alias>
```

**IMPORTANT:** Always set BOTH `pse__Rating__c` (text) and `pse__Numerical_Rating__c` (number) together. They must be consistent.

The user may express ratings in natural language. Map accordingly:
- "no experience" / "none" / "1" → `1 - No experience` / 1
- "can deliver with prep" / "need prep" / "2" → `2 - Can deliver need prep time` / 2
- "can deliver" / "3" → `3 - Can deliver` / 3
- "SME" / "expert" / "4" → `4 - SME` / 4
- For certifications: "yes" / "have it" / "passed" → `8 - Yes` / 8
- For certifications: "no" / "don't have" → `9 - No` / 9
- For languages: "speak" → `5 - Can Speak` / 5, "write" → `6 - Can Write` / 6, "speak and write" / "fluent" → `7 - Can Speak & Write` / 7

### Add a New Skill Rating

If the resource doesn't have a rating for a skill yet, first find the skill in the catalog:

```bash
sf data query \
  --query "SELECT Id, Name, pse__Type__c, pse__Skill_Or_Certification__c, RecordType.Name \
    FROM pse__Skill__c \
    WHERE Name = '<skill_name>'" \
  --target-org <alias>
```

If the user isn't sure of the exact name, do a fuzzy search:

```bash
sf data query \
  --query "SELECT Id, Name, pse__Type__c \
    FROM pse__Skill__c \
    WHERE Name LIKE '%<partial_name>%' \
    ORDER BY pse__Type__c, Name" \
  --target-org <alias>
```

Then create the rating record:

```bash
sf data create record \
  --sobject pse__Skill_Certification_Rating__c \
  --values "pse__Resource__c='<contact_id>' \
    pse__Skill_Certification__c='<skill_id>' \
    pse__Rating__c='<rating>' \
    pse__Numerical_Rating__c=<num>" \
  --target-org <alias>
```

### Update Additional Fields

The user may also want to update:

- **Aspiration**: `pse__Aspiration__c=true`
- **Notes**: `pse__Notes__c='<text>'`
- **Years of experience**: `pse__Years_Experience__c=<number>`
- **Last used date**: `pse__Last_Used_Date__c=<YYYY-MM-DD>`
- **Certified flag**: `pse__Certified__c=true`

Include these in the `--values` string when updating or creating.

### Bulk Updates

If the user wants to update multiple skills at once (e.g., "set all my cloud skills to 2"), query the matching ratings and update each one individually. Confirm the list before executing:

> *"I'll update these 5 cloud skills to **2 - Can deliver need prep time**:*
> - *AWS Architecture (currently 1)*
> - *AWS CloudFormation (currently 1)*
> - *AWS EMR (currently 1)*
> - *AWS Glue (currently 1)*
> - *AWS Redshift (currently 1)*
>
> *Proceed?"*

## Finding Missing Skills

When the user asks "what skills am I missing?" or "what skills don't I have?":

1. Query all skills in the catalog
2. Query all the user's existing ratings
3. Compare to find skills without ratings

```bash
sf data query \
  --query "SELECT Id, Name, pse__Type__c, pse__Skill_Or_Certification__c \
    FROM pse__Skill__c \
    WHERE pse__Skill_Or_Certification__c != '' \
      AND RecordType.Name != 'Category' \
    ORDER BY pse__Type__c, Name" \
  --target-org <alias>
```

Display the missing skills grouped by category, and offer to add ratings for them:

```
**Skills Not Yet Rated — <Resource Name>**

### Data Science and Machine Learning
- Agent Bricks
- Horovod Model

### Cloud
- AWS (Databricks SME)
- Azure HDInsight

### Certifications
- Data Analyst Associate
- Databricks Certified Generative AI Engineer Associate

**XX skills not yet rated out of XX total in the catalog.**
*Would you like to add ratings for any of these?*
```

## Viewing by Category

When the user asks to see a specific category (e.g., "show my cloud skills"), filter the display:

```bash
sf data query \
  --query "SELECT Id, pse__Skill_Certification__r.Name, \
      pse__Rating__c, pse__Numerical_Rating__c, \
      pse__Aspiration__c, pse__Notes__c \
    FROM pse__Skill_Certification_Rating__c \
    WHERE pse__Resource__r.Name = '<resource_name>' \
      AND pse__Skill_Certification__r.pse__Type__c = '07Cloud' \
    ORDER BY pse__Skill_Certification__r.Name" \
  --target-org <alias>
```

Map the user's natural language to the `pse__Type__c` values:
- "programming" / "languages" (in coding context) → `01Programming Languages`
- "platform" / "admin" → `02Platform Administration`
- "data engineering" / "DE" → `03Data Engineering`
- "data science" / "ML" / "machine learning" / "AI" → `04Data Science and Machine Learning`
- "SQL" / "DW" / "data warehouse" → `05SQL and DW`
- "ecosystem" → `06Ecosystem`
- "cloud" / "AWS" / "Azure" / "GCP" → `07Cloud`
- "migrations" → `Migrations`
- "packages" → `Packages`
- "verticals" / "domain" / "industry" → `08Verticals/Domain Expertise`
- "specialty" → `Specialty Skills`
- "spoken languages" / "languages" (in spoken context) → `09Languages (Choose 5 - 7)`
- "certifications" / "certs" → `01Certification`

## Confirmation

After any create or update operation, confirm success and show the updated entry:

> *"Updated **Python** rating to **4 - SME** for <Resource Name>."*

Or for a new skill:

> *"Added **Agent Bricks** with rating **2 - Can deliver need prep time** for <Resource Name>."*
