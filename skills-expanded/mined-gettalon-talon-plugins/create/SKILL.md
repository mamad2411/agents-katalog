---
name: create-skill
description: Design and write a SKILL.md workflow for a specific domain task. Use when the user wants to create a repeatable, step-by-step skill — a structured workflow an agent can follow to complete a complex task.
user-invocable: true
---

# Create Skill — Domain Workflow Designer

Design a SKILL.md file that teaches an agent how to complete a specific domain task through a structured, repeatable workflow.

## What Makes a Good Skill

A skill is NOT just instructions. It's a **repeatable workflow** with:
- Clear trigger conditions (when to activate)
- Step-by-step checklist (track progress)
- Specific tool calls at each step (what data to gather)
- Validation/sanity checks (catch errors before presenting)
- Structured output format (consistent results)

A well-structured skill tells the agent exactly which tools to call, what data to extract, how to calculate, how to validate, and how to present results.

## Process

### Step 1: Understand the Task

Ask one at a time:

1. **What task does this skill perform?**
   - e.g., "Analyze a company's competitive moat"
   - e.g., "Review a pull request for security issues"
   - e.g., "Generate a weekly project status report"

2. **When should the agent activate this skill?**
   - What trigger phrases or questions activate it?
   - e.g., "Triggers on: moat analysis, competitive advantage, defensibility, economic moat"

3. **What tools does the agent need?**
   - web_search, web_fetch, get_financials, read_file, shell, browser, etc.
   - What APIs or data sources are required?

4. **What does the output look like?**
   - Tables, prose, structured report, checklist?
   - Show an example of ideal output if possible.

### Step 2: Design the Workflow

Break the task into 4-8 sequential steps. For each step define:

- **What to do**: Clear action (e.g., "Call get_financials with...")
- **What data to extract**: Specific fields/values
- **Fallback**: What to do if data is missing
- **Validation**: How to check the step succeeded

**Design patterns to follow:**
- Each step should produce data the next step consumes
- Include cross-validation between steps (e.g., compare two independent estimates)
- Cap assumptions (e.g., "growth rate capped at 15%")
- Always include a validation step before final output

### Step 3: Write the SKILL.md

Use this structure:

```markdown
---
name: <skill-name>
description: <one-line description with trigger words>
---

# <Skill Title>

## Workflow Checklist
- [ ] Step 1: <action>
- [ ] Step 2: <action>
...
- [ ] Step N: Present results

## Step 1: <Action>
<Detailed instructions with specific tool calls>
### 1.1 <Sub-step>
**Query:** "<exact query to pass to tool>"
**Extract:** <specific fields>
**Fallback:** <what to do if missing>

## Step 2: <Action>
...

## Step N: Validate Results
<Sanity checks before presenting>

## Output Format
<Structured template for results>
```

### Step 4: Validate the Skill

Before delivering, verify:
1. Every step has a clear action and expected output
2. Tool calls specify exact queries/parameters
3. Fallbacks exist for missing data
4. Validation step catches common errors
5. Output format is concrete (not vague)
6. Trigger description covers common phrasings

### Step 5: Place the File

- If part of an agent: `agents/<agent-name>/skills/<skill-name>/SKILL.md`
- If standalone: `skills/<skill-name>/SKILL.md`
- If adding to existing agent: read the AGENT.yaml and add skill to the skills list

## Anti-Patterns

| Bad | Good |
|-----|------|
| "Gather relevant data" | "Call get_financials with '[TICKER] annual cash flow for last 5 years'" |
| "Analyze the results" | "Calculate 5-year CAGR from extracted FCF values" |
| "Check if reasonable" | "Verify: calculated EV within 30% of reported enterprise_value" |
| "Present findings" | "Table with columns: Metric, Value, Source, Confidence" |

Vague instructions produce vague results. Specific instructions produce reliable results.

$ARGUMENTS
