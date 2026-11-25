---
name: prompt-templates
description: Library of fill-in-the-blank prompt templates for common dev workflows — debugging, code review, refactoring, system design, learning a new concept, interview prep, and more. Each template uses {{PLACEHOLDER}} slots to be replaced with specifics. Use when the user asks for a prompt template, says "give me a prompt for X", or is building a reusable workflow for AI-assisted coding. Not for one-off prompt writing — use ai-usage skill for that.
---

# Skill: Prompt Templates

> **Purpose**: Reusable, dynamic prompt templates for common development workflows.  
> Replace `{{placeholders}}` with your actual values before use.

## How to Use

1. Copy the template you need
2. Replace all `{{PLACEHOLDER}}` values with your specifics
3. Paste into your AI assistant or use in your workflow

---

## 1. 🐛 Debug

### Quick Debug
```
I have a bug in my {{LANGUAGE}} code.

**What I expected**: {{EXPECTED_BEHAVIOR}}
**What actually happens**: {{ACTUAL_BEHAVIOR}}
**Error message**: {{ERROR_MESSAGE_OR_NONE}}

Here's the relevant code:
```{{LANGUAGE}}
{{YOUR_CODE}}
```

What changed recently: {{RECENT_CHANGES}}

Help me find the root cause and fix it.
```

### Deep Debug (With Stack Trace)
```
I'm stuck on a {{LANGUAGE}} issue and need systematic debugging help.

**Environment**: {{RUNTIME_OR_FRAMEWORK}} / {{VERSION}}
**Error type**: {{ERROR_TYPE}} (e.g., TypeError, NullPointer, 500 error)
**Stack trace**:
{{PASTE_STACK_TRACE}}

**Steps to reproduce**:
1. {{STEP_1}}
2. {{STEP_2}}
3. {{STEP_3}}

**What I already tried**:
- {{ATTEMPT_1}}
- {{ATTEMPT_2}}

Isolate the root cause. Don't guess — walk me through it step by step.
```

---

## 2. ⚡ Generate Code

### Feature / Function
```
Write a {{LANGUAGE}} function that:

**Purpose**: {{WHAT_IT_DOES}}
**Input**: {{INPUT_DESCRIPTION_AND_TYPES}}
**Output**: {{OUTPUT_DESCRIPTION_AND_TYPE}}
**Edge cases to handle**: {{EDGE_CASES}}

Requirements:
- {{REQUIREMENT_1}}
- {{REQUIREMENT_2}}
- Follow clean code practices (descriptive names, single responsibility)

Include a usage example and brief explanation.
```

### API Endpoint
```
Create a {{FRAMEWORK}} API endpoint:

**Method**: {{GET/POST/PUT/DELETE}}
**Route**: {{/api/your-route}}
**Purpose**: {{WHAT_IT_DOES}}

**Request body/params**:
{{REQUEST_SCHEMA}}

**Response format**:
{{RESPONSE_SCHEMA}}

**Validation rules**:
- {{RULE_1}}
- {{RULE_2}}

**Error responses to handle**:
- 400: {{BAD_REQUEST_CASE}}
- 404: {{NOT_FOUND_CASE}}
- 500: Internal server error

Include error handling, input validation, and a test example.
```

### Database Query
```
Write a {{SQL/MONGODB/ORM}} query for:

**Database**: {{DATABASE_TYPE_AND_VERSION}}
**Table(s)/Collection(s)**: {{TABLE_NAMES}}
**Goal**: {{WHAT_YOU_NEED_TO_RETRIEVE_OR_MODIFY}}
**Filters**: {{CONDITIONS}}
**Sort by**: {{SORT_FIELD_AND_DIRECTION}}
**Pagination**: {{YES_NO_AND_PAGE_SIZE}}

Schema for reference:
{{PASTE_SCHEMA_OR_DESCRIBE_COLUMNS}}

Optimize for {{SPEED/READABILITY}} and explain the query.
```

---

## 3. 🚨 Error Handling

### Add Error Handling to Existing Code
```
Add proper error handling to this {{LANGUAGE}} code:

```{{LANGUAGE}}
{{YOUR_CODE_WITHOUT_ERROR_HANDLING}}
```

Requirements:
- Handle these failure scenarios: {{FAILURE_SCENARIOS}}
- Log errors with context (not silently catch)
- Use {{TRY_CATCH / RESULT_TYPE / ERROR_BOUNDARY}} pattern
- Return meaningful error messages to the caller
- Don't crash the application on recoverable errors

Show me the before/after with explanations.
```

### Design Error Strategy
```
I need an error handling strategy for my {{LANGUAGE}} {{APP_TYPE}} application.

**Current pain points**:
- {{PAIN_POINT_1}}
- {{PAIN_POINT_2}}

**Components involved**:
- {{COMPONENT_1}} (e.g., API layer)
- {{COMPONENT_2}} (e.g., Database layer)
- {{COMPONENT_3}} (e.g., External service calls)

Design a consistent error handling approach with:
1. Custom error classes/types
2. Where to catch vs. where to propagate
3. User-facing vs. internal error messages
4. Logging strategy
5. Code examples for each layer
```

---

## 4. 🔍 Analyze Code

### Code Review
```
Review this {{LANGUAGE}} code for:

```{{LANGUAGE}}
{{YOUR_CODE}}
```

Check for:
- [ ] Bugs or logic errors
- [ ] Security vulnerabilities
- [ ] Performance issues
- [ ] Readability and naming
- [ ] Missing error handling
- [ ] {{CUSTOM_CHECK}}

Rate severity: 🔴 Critical | 🟡 Warning | 🟢 Suggestion

For each issue, show the fix.
```

### Architecture Analysis
```
Analyze the architecture of my {{PROJECT_TYPE}}:

**Tech stack**: {{LANGUAGES_FRAMEWORKS_TOOLS}}
**Current structure**:
{{PASTE_FOLDER_STRUCTURE_OR_DESCRIBE}}

**Current problems**:
- {{PROBLEM_1}}
- {{PROBLEM_2}}

**Goals**:
- {{GOAL_1}} (e.g., easier to test)
- {{GOAL_2}} (e.g., better separation of concerns)

Suggest improvements with:
1. What to change and why
2. Migration steps (smallest changes first)
3. File/folder restructuring if needed
```

---

## 5. 🔄 Refactor

### Clean Up Code
```
Refactor this {{LANGUAGE}} code to improve {{READABILITY/PERFORMANCE/TESTABILITY}}:

```{{LANGUAGE}}
{{YOUR_MESSY_CODE}}
```

Constraints:
- Keep the same external behavior (inputs/outputs)
- {{CONSTRAINT_1}} (e.g., must stay under 20 lines per function)
- {{CONSTRAINT_2}} (e.g., no new dependencies)

Show the refactored version with:
1. What changed and why
2. Before/after comparison for key sections
```

### Extract & Modularize
```
This {{LANGUAGE}} file is too large ({{LINE_COUNT}} lines). Help me split it:

```{{LANGUAGE}}
{{YOUR_CODE_OR_DESCRIBE_STRUCTURE}}
```

Current responsibilities in this file:
1. {{RESPONSIBILITY_1}}
2. {{RESPONSIBILITY_2}}
3. {{RESPONSIBILITY_3}}

Split into separate modules following single responsibility principle.
Show the new file structure and the code for each file.
```

---

## 6. 🧪 Testing

### Write Unit Tests
```
Write {{TEST_FRAMEWORK}} tests for this {{LANGUAGE}} code:

```{{LANGUAGE}}
{{YOUR_CODE}}
```

Cover these scenarios:
- ✅ Happy path: {{NORMAL_CASE}}
- ❌ Error case: {{ERROR_CASE}}
- 🔲 Edge case: {{EDGE_CASE}}
- 🔲 Boundary: {{BOUNDARY_CASE}}

Use {{DESCRIBE_IT / GIVEN_WHEN_THEN}} style.
Mock these dependencies: {{DEPENDENCIES_TO_MOCK}}
```

### Generate Test Data
```
Generate test data for my {{LANGUAGE}} {{ENTITY_NAME}}:

Schema:
{{PASTE_SCHEMA_OR_INTERFACE}}

Generate:
- {{N}} valid records (realistic, varied data)
- {{N}} invalid records (with specific validation violations)
- Edge case records: {{DESCRIBE_EDGE_CASES}}

Format: {{JSON/SQL_INSERT/CODE_OBJECTS}}
```

---

## 7. 🚀 Performance

### Optimize Code
```
This {{LANGUAGE}} code is too slow. Help me optimize it:

```{{LANGUAGE}}
{{YOUR_SLOW_CODE}}
```

**Current performance**: {{CURRENT_METRIC}} (e.g., 3s for 10K records)
**Target performance**: {{TARGET_METRIC}} (e.g., under 500ms)
**Input size**: {{DATA_SIZE}}
**Bottleneck (if known)**: {{SUSPECTED_BOTTLENECK}}

Analyze time/space complexity and suggest optimizations.
Show the optimized code with complexity comparison.
```

### Database Performance
```
This {{SQL/MONGODB}} query is slow:

```sql
{{YOUR_SLOW_QUERY}}
```

**Table size**: {{ROW_COUNT}} rows
**Current execution time**: {{CURRENT_TIME}}
**Existing indexes**: {{LIST_INDEXES}}

Analyze and suggest:
1. Query rewrite
2. Index recommendations
3. Explain plan analysis
4. Caching strategy if applicable
```

---

## 8. 📖 Documentation

### Document Code
```
Generate documentation for this {{LANGUAGE}} code:

```{{LANGUAGE}}
{{YOUR_CODE}}
```

Include:
- JSDoc/Javadoc comments for each function
- Parameter descriptions with types
- Return value description
- Usage examples
- {{ADDITIONAL_DOC_REQUIREMENT}}

Style: {{CONCISE/DETAILED}}
```

### Write README
```
Generate a README.md for my project:

**Project name**: {{PROJECT_NAME}}
**What it does**: {{ONE_LINE_DESCRIPTION}}
**Tech stack**: {{TECHNOLOGIES}}
**Target audience**: {{WHO_IS_IT_FOR}}

Include sections:
- Overview
- Quick Start (install + run in under 2 minutes)
- Configuration
- API reference (if applicable)
- Contributing guide
- License: {{LICENSE_TYPE}}
```

---

## 9. 🔐 Security Audit

```
Audit this {{LANGUAGE}} code for security vulnerabilities:

```{{LANGUAGE}}
{{YOUR_CODE}}
```

**Application type**: {{WEB_API/CLI/LIBRARY}}
**Handles user input**: {{YES/NO}}
**Connects to**: {{DATABASE/EXTERNAL_API/FILESYSTEM}}

Check for:
- [ ] Injection (SQL, NoSQL, command)
- [ ] Authentication/authorization flaws
- [ ] Data exposure (logging secrets, error leaks)
- [ ] Input validation gaps
- [ ] Dependency vulnerabilities
- [ ] {{CUSTOM_SECURITY_CHECK}}

For each finding: severity, exploit scenario, and fix.
```

---

## 10. 🧠 Explain & Learn

### Explain Code
```
Explain this {{LANGUAGE}} code like I'm a {{JUNIOR/MID/SENIOR}} developer:

```{{LANGUAGE}}
{{CODE_TO_EXPLAIN}}
```

Break down:
1. What it does (one sentence)
2. How it works (step by step)
3. Why it's written this way
4. Any patterns or concepts used
5. Potential gotchas or improvements
```

### Explain Concept
```
Explain {{CONCEPT_NAME}} in {{LANGUAGE/FRAMEWORK}}:

1. One-sentence definition
2. Real-world analogy
3. Simple code example
4. Common mistake example
5. When to use it vs. when NOT to use it

Keep it practical — no academic theory dumps.
```

---

## Quick Reference Table

| Template | When to Use |
|----------|-------------|
| **Debug** | Something broke, need to find root cause |
| **Generate Code** | Building new features or endpoints |
| **Error Handling** | Adding resilience to existing code |
| **Analyze** | Code review or architecture assessment |
| **Refactor** | Cleaning up messy or oversized code |
| **Testing** | Writing tests or generating test data |
| **Performance** | Slow code or queries need optimization |
| **Documentation** | Adding docs or creating README |
| **Security** | Auditing code for vulnerabilities |
| **Explain** | Understanding unfamiliar code or concepts |

---

*Copy → Replace placeholders → Paste → Ship.* 🚀
