---
title: Crafting Effective AI Prompts for MongoDB Optimization
description: 'Craft precise AI prompts to optimize MongoDB: phased analysis, index tuning, and actionable query recommendations.'
categories:
  - AI
tags:
  - AI
  - copilot
  - productivity
  - MongoDB
  - prompt-engineering
  - best-practices
linkTitle: Crafting Effective AI Prompts for MongoDB Optimization
date: '2026-03-04T23:00:00+01:00'
lastmod: '2026-05-10T23:42:08+02:00'
version: '1.1'
---

## 1. Overview

This guide shares practical lessons from using AI to analyze and optimize MongoDB databases across multiple Python
repositories. By following these techniques, you'll learn how to craft prompts that produce accurate, actionable
analysis instead of generic recommendations.

**Key Takeaway**: Precise, well-structured prompts dramatically improve the quality and usefulness of AI-generated
database analysis.

## 2. Context

This guide is based on analyzing two interconnected Python repositories that share a single MongoDB database.

**Repository Roles:**

| Component        | Responsibility                                                       |
| ---------------- | -------------------------------------------------------------------- |
| `api_python`     | Database schema, migrations, and Beanie ORM models (source of truth) |
| `kafka-consumer` | Consuming Kafka events and updating MongoDB collections              |

**Technology Used:**

- MongoDB for data storage
- Beanie ORM for Python-MongoDB integration
- Python as the programming language

## 3. The Challenge

Creating an effective prompt proved unexpectedly difficult. Initial attempts to fit all requirements into a single
prompt resulted in timeouts and no output. This is a common problem when asking AI to handle large, complex analysis
tasks in one go.

## 4. Phase 1: Testing a Comprehensive Prompt

The first approach was to create a single detailed prompt that would handle all analysis at once:

```markdown
---
name: fc-optimize-mongodb
description: Analyze the MongoDB usage in the API and its Kafka Consumer, identify all the CRUD queries that
are made to MongoDB in both projects, and propose optimizations.
---
As a Senior specialist of documentDB and MongoDB optimization, you have been tasked to analyze the MongoDB usage
in the API and its Kafka Consumer. Your goal is to identify all the CRUD queries that are made to MongoDB in both
repositories, and propose optimizations.

**CRITICAL** Analyze all the files **ONLY** in the directories `api_python` and `kafka-consumer`.
But ignore files in `api_python/admin/database/migrations/`.

These 2 projects are separated but they use the same MongoDB database but with different Beanie models definitions.
`api_python` is the project that is responsible for the database schema and migrations.
While `kafka-consumer` is responsible for consuming the Kafka events and updating the MongoDB collections accordingly.
So consider `api_python` as source of truth.

You will analyze current MongoDB schema (api_python/admin/database/indexes/definition.py, api_python/odm/models.py).

**CRITICAL** Don't update source code, just analyze and generate a report in
`docs/ai/{date:YYYY-mm-dd}-mongodbAnalysis/mongodbAnalysis.md` where you will list all the CRUD queries that are made
to MongoDB (normally all the queries are done through Beanie ORM) in both projects.
**CRITICAL** Don't invent any query, just list the queries accurately as they are in the codebase.

When you will have the full view:
- indicate branch name and commit hash of each repositories.
- for each query write
  - the equivalent MongoDB query that could be done through mongosh
  - the file location and line where the query is done
  - the Beanie query that is done in the code
- global recommendations
  - List all the tables and indexes that are used
  - check if all the required indexes are present
  - propose missing indexes creation
  - propose indexes that should be removed
  - indicate as well when an index could be replaced by a lighter index
    - Compound Indexes
    - Partial Indexes
    - Sparse Indexes
    - Partial indexes with filter expressions
    - ...
  - Propose also optimizations to the queries themselves if you see any
  - Propose to improve the indexes with projections.
  - List inconsistencies in the kafka-consumer
  - **CRITICAL** take into consideration property order in the indexes.
  - Propose queries that could be done on production to analyze the query planner behavior and the index
    usage for the most critical queries.
  - for each suggestion propose code snippets of how the query or the index should be updated.
  - Propose schema improvements if you see any.
- if you see any other recommendations put them in another section
- generate a plantuml diagram of the current schema in `docs/ai/{date:YYYY-mm-dd}-mongodbAnalysis/mongodbSchema.puml`
  and another one with the proposed schema in `docs/ai/{date:YYYY-mm-dd}-mongodbAnalysis/mongodbProposedSchema.puml`
  where you will ignore obsolete tables.
- add at the start of the report a summary of the main findings and recommendations.

use askQuestions tool for any question.

if folder `kafka-consumer` doesn't exist use askQuestions to propose the user to create
a symlink using `ln -s ../kafka-consumer kafka-consumer`.

use askQuestions to ask if the user think about using updated branches before starting the analysis.
```

### 4.1. First Results and the Limits of Comprehensive Prompts

The first prompt produced a solid report and revealed 3 critical issues that weren't previously known. This success led
to adding more requirements for even deeper analysis. However, the expanded prompt failed with a timeout error—producing
no output at all.

## 5. Phase 2: Why Comprehensive Prompts Fail

### 5.1. The Timeout Problem

Attempting to add schema consistency checks (validating that all fields updated in `kafka-consumer` exist in
`api_python` models) caused a timeout with no output.

**The fundamental issue:** AI has a practical processing time limit of 10-15 minutes per request. Asking for complete
analysis of multiple complex topics at once exceeds this limit. The solution is to break large tasks into smaller,
manageable phases.

**Task Decomposition Strategy:**

Instead of: One comprehensive prompt covering everything

Try this: Multiple focused prompts in sequence

Break analysis into phases:

1. **Inventory** (What exists?)
2. **Analysis** (What's suboptimal?)
3. **Planning** (How to fix it?)
4. **Documentation** (Summarize findings)

Each phase completes in 3-5 minutes instead of timeout.

## 6. Phase 3: Breaking Work Into Manageable Pieces

To solve the timeout problem, the solution split the large task into distinct phases, each with specific, limited
objectives and intermediate checkpoints.

### 6.1. Planning the Phased Approach

Before redesigning, key decisions were made using interactive questions:

#### 6.1.1. Decision 1: Execution Model

- Approach: Single skill with manual phase progression
- Rationale: User controls when each phase runs, can review results before continuing

#### 6.1.2. Decision 2: Output Volume

- Approach: Moderate detail (phase summaries with key findings)
- Rationale: Balance between useful information and processing speed

#### 6.1.3. Decision 3: Phase Duration

- Approach: 3-5 minutes per phase
- Rationale: Short enough to avoid timeouts, long enough for meaningful analysis

#### 6.1.4. Decision 4: Analysis Focus

- Priorities: Missing indexes, index optimization opportunities
- De-prioritized: Schema consistency checks (can be added later)
- Rationale: Address most critical performance issues first

### 6.2. Phase-Based Prompt Structure

The refined prompt introduces a `phase` parameter to guide execution:

```markdown
### 6.3. Execution Workflow

The analysis is broken into **4 independent phases** (3-5 minutes each). Each phase:
- ✅ Checks for previous phase data in session memory
- 📊 Processes its specific scope
- 💾 Saves results to `/memories/session/mongodb-analysis-{phase}.json`
- 📝 Shows a summary of findings
- ➡️ Indicates next phase to run
**How to use:**
1. Run: `@workspace /optimize-mongodb` (or with `phase=1`)
2. Review phase summary
3. Continue: `@workspace /optimize-mongodb phase=2`
4. Repeat until Phase 4 generates the final report

**Recovery:** If interrupted, just restart from the last completed phase. All previous work is preserved in session memory.
```

And this part, which is included in the prompt to guide the AI through the execution of each phase:

```markdown
## 7. Processing Workflow

**Follow this systematic approach :**

### 7.1. For Each Phase Execution:

1. **Phase Validation**
   - Determine which phase to run (from user input or default to 1)
   - Check for prerequisite phase data in /memories/session/
   - If missing prerequisites, show error + command to run

2. **Data Loading**
   - Load all prerequisite phase data from session memory
   - Validate JSON structure and completeness
   - Show brief recap of loaded data

3. **Phase Execution**
   - Execute phase-specific analysis (see phase details above)
   - Show progress indicators for long operations
   - Build phase output data structure

4. **Data Persistence**
   - Save phase results to `/memories/session/mongodb-analysis-phase{N}.json`
   - Validate saved data is complete
   - Show data save confirmation

5. **Summary Display**
   - Show phase completion message
   - Display key metrics and findings
  - Indicate next phase command
```

It's **important** to note that the AI will not automatically run the next phase, but it will indicate to the user to
run the next phase command. This way, the user has control over when to proceed to the next phase and can review the
findings of each phase before moving on.

Finally, for my usage, I grouped phase 1 and phase 2 together and then phase 3 and phase 4 together. So I slightly
changed the workflow above to this one:

```diff
...
+ **CRITICAL** Group phase 1 and phase 2 and then phase 3 and phase 4 together.
...
-   - Indicate next phase command
+   - If phase 1 or phase 3
+    - continue yourself with phase 2 without asking the user to run the command
+   - Else
+    - Indicate next phase command if any
```

The
[Full fc-optimize-mongodb skill](https://github.com/fchastanet/copilot-prompts/blob/master/skills/fc-optimize-mongodb/SKILL.md)
is available for reference, showcasing the phased execution structure and detailed prompt techniques.

### 7.2. Best Practices for Effective Database Analysis Prompts

Based on this experience, here are essential techniques:

- ✅ Define clear role and expertise level
- ✅ Establish explicit scope boundaries with CRITICAL markers
- ✅ Prevent AI hallucination by prohibiting invented data
- ✅ Control output format and structure with specific requirements
- ✅ Prevent unintended code changes by setting "do no harm" boundaries
- ✅ Use phased execution for complex analysis to avoid timeouts
- ✅ Request validation data to create an audit trail

#### 7.2.1. Define Clear Role and Expertise Level

Instead of: "Analyze MongoDB" Write: "As a Senior MongoDB performance specialist with 5+ years optimizing large-scale
databases..."

This calibrates the AI's response depth and technical accuracy. You would have a totally different output if you ask it
to act as a child of 3 years old.

#### 7.2.2. Establish Explicit Scope Boundaries

Use **CRITICAL** markers to highlight non-negotiable constraints:

```markdown
**CRITICAL** Analyze ONLY these directories: api_python, kafka-consumer
**CRITICAL** Ignore migration files: api_python/admin/database/migrations/
**CRITICAL** Treat api_python as the source of truth
```

This prevents AI from straying beyond the defined scope.

#### 7.2.3. Prevent AI Hallucination (Important!)

*Hallucination* occurs when AI invents data that doesn't exist (like queries not in your codebase).

**Solution:** Explicitly forbid invented data:

```markdown
**CRITICAL** Do not invent queries. List ONLY queries from actual code.
Reference exact file locations and line numbers for every query.
```

While this won't eliminate hallucinations entirely, AI will self-check because of this explicit instruction.

#### 7.2.4. Control Output Format Precisely

❌ **Vague:** "Provide recommendations"

✅ **Precise:** "Generate report with sections: Summary, Query Inventory, Index Analysis. For each query: (a) MongoDB
equivalent, (b) file location, (c) Beanie ORM code"

Specific output formats make results reliable and actionable.

**Prevent Unintended Code Changes**

Be clear about what should not happen:

```markdown
Do not modify source code. Generate recommendations and code snippets separately.
I will review all suggestions before implementing any changes.
```

This keeps humans in control of code changes.

#### 7.2.5. Use Phased Execution for Complex Analysis

❌ **Unreliable:** One comprehensive prompt covering everything

✅ **Reliable:** Multiple focused phases executed in sequence

**Phase structure:**

- Phase 1: Inventory (what exists?)
- Phase 2: Analysis (what's suboptimal?)
- Phase 3: Planning (how to fix it?)
- Phase 4: Documentation (summarize findings)

Target 3-5 minutes per phase to avoid timeouts.

**Save Intermediate Results**

Instrumented AI to save results to session memory after each phase. Benefits:

- **Resilience:** If interrupted, restart from last phase (no progress lost)
- **Audit trail:** Review exactly what each phase discovered
- **Flexibility:** Modify scope mid-analysis or skip phases as needed

#### 7.2.6. Request Validation Data

Ask AI to document:

- Repository branch name and commit hash
- Date of analysis
- Scope confirmation (which files analyzed, which were ignored)
- Output file locations with timestamps (e.g., `mongodb-analysis-{date:YYYY-mm-dd}.md`)

This creates an audit trail for verification.

### 7.3. What Each Phase Produces

With proper phase separation, you reliably get:

1. **Phase 1**: Complete catalog of all MongoDB queries
   - **Benefits**: Understand what's currently happening
2. **Phase 2**: Equivalent mongosh queries, optimization opportunities
   - **Benefits**: See where improvements are possible
3. **Phase 3**: Current indexes, missing indexes, optimization suggestions
   - **Benefits**: Identify performance bottlenecks
4. **Phase 4**: Executive summary, code snippets, schema diagrams
   - **Benefits**: Ready to implement or discuss with team

## 8. Key Takeaways

| Principle                    | Why It Matters                                                         |
| ---------------------------- | ---------------------------------------------------------------------- |
| **Structure beats length**   | A clear, focused prompt outperforms a comprehensive but confused one   |
| **Phase work into chunks**   | 3-5 minute phases avoid timeouts and allow progress review             |
| **Use explicit boundaries**  | Clear "do" and "don't" instructions reduce hallucinations              |
| **Ask clarifying questions** | Interactive Q&A reveals priorities and prevents false assumptions      |
| **Document everything**      | Audit trails let you verify recommendations and track analysis quality |
| **Keep humans in control**   | Always review AI recommendations before making code changes            |

## 9. Applying These Techniques to Your Work

**To analyze your own MongoDB database:**

1. **Clarify first** — Use interactive questions to establish priorities and scope
2. **Design phases** — Break analysis into 4-5 distinct phases with limited scope each
3. **Validate findings** — Cross-check AI recommendations against your actual codebase
4. **Implement carefully** — Apply recommendations incrementally with thorough testing
5. **Document progress** — Record what worked, what failed, and lessons learned for future analysis

## 10. Conclusion

The full implementation of these techniques is available in the
[FC-optimize-mongodb skill on GitHub](https://github.com/fchastanet/copilot-prompts/blob/master/skills/fc-optimize-mongodb/SKILL.md).

Next time I will craft an AI prompt on a big project, I will probably simplify this kind of prompt by simply asking AI
to save the intermediate results in session memory and just tell it that the user can ask to start from any phase and
that it should check the session memory for the previous phase results before starting to execute the current phase.
This way, in worst case scenario, the prompt fails with a timeout but the user can just restart from last phase without
losing the previous work.

Also probably, I gave too much details in the prompt, I will probably try to give less details and let more freedom to
AI.

Using these techniques, even large database analyzes become manageable, reliable, and resilient to interruptions.
