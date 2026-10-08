---
name: concept-interviewing
description: |
  Conducts an interview to define the product concept and identify competitors.

  Triggered when:
  - The user wants to start a patent investigation for a new product, idea, or concept
    (e.g., "start a patent search for a new product", "patent investigation for a new idea")
  - The user explicitly requests:
    * "conduct concept interview"
    * "define product concept"
    * "define search requirements"
---

# Concept Interview

## Purpose

Define the product concept and identify competitors. This establishes the
foundation for patent targeting.

## Prerequisites

No specific prerequisites required.

## Skill Orchestration

**Do NOT delegate to subagents (Agent tool)** — invoke Skills directly from this session.

### Process

#### Step 1: Check Existing Specification

Use the Glob tool to check if `specification.md` exists:

- **If exists**:
  - Read the existing specification
  - Check if "Verified Assignee Names" table contains proper assignee name variations:
    - **If assignee names are listed** with variations: Verification already complete — skip to confirmation
    - **If assignee names are missing** or incomplete: Perform assignee verification (Step 3)
- **If NOT exists**: Proceed to Step 2

#### Step 2: Information Gathering

Extract the following information from the user's input:

**Required Information**:

- **Product Concept**: Detailed description of what they want to realize
- **Competitors**: List of key competitor companies (Mandatory)
- **Target Country**: Where the product will be released (e.g., US, JP)
- **Target Release Date**: Approximate date
- **Cutoff Date**: Calculate `Target Release Date - 20 years`. Patents filed before this date are likely expired

**Extraction Logic**:

- If the user provides a country (e.g., "in the US", "US market"), extract and use that
- If the user provides a release date (e.g., "2025", "June 2025"), extract and use that
- Extract competitors from mentions of company names

**If any required information is missing**:

- Ask the user to provide the missing information
- Do not make assumptions or use default values

> [!NOTE]
> In automated test environments, ensure all required information is provided in
> the initial request to avoid interactive prompts.

#### Step 3: Assignee Identification

For each competitor, verify the correct "Assignee Name" used in patent databases.

1. **Verify**: Invoke Skills in parallel for efficiency:

   ```
   Skill: skill="google-patent-cli:patent-assignee-check" args="<Company Name> --country <Target Country>"
   ```

   - Omit the limit parameter to get all assignee variations (default: 100)
   - **CRITICAL: Check skill response**:
     - Verify the response does NOT contain errors
     - **If skill fails**: Refer to `references/troubleshooting.md` for error handling
     - Do NOT proceed with fabricated or assumed assignee names

2. **Confirm**: Display the top assignee variations found and ask the user if they represent the intended competitor.

3. **Refine**: If incorrect or no hits, try variations (e.g., "Google LLC" instead of "Google").

4. **Finalize**:
   - Fill the **Verified Assignee Names (Canonicalized)** table in `specification.md`
   - Record **all** identified official Assignee Names, including all name variations
   - Record the verification status and any notes (e.g., holding company, subsidiary)

#### Step 4: Transition to Targeting

- Deliverable: `specification.md` created with verified assignee names
- Next skill: `/patent-kit:targeting`

## Output Management

- **Output File**: `specification.md`
- **Template**: Use `assets/templates/specification-template.md`
- **Format**: Markdown (not JSON)
- **Note**: This file is referenced by all subsequent skills (targeting, screening, evaluating, claim-analyzing)

## State Management

### Initial State

- No `specification.md` (proceed with interview)
- OR `specification.md` exists (skip to verification/confirmation)

### Final State

- `specification.md` created with:
  - Product concept clearly defined
  - Target country and release date specified
  - All competitors' assignee names verified
  - Complete information saved

## Quality Gates

- [ ] Product concept is clearly defined.
- [ ] Target country and release date are specified.
- [ ] All competitors' assignee names are verified in the database.
- [ ] Specification file is saved with complete information.
