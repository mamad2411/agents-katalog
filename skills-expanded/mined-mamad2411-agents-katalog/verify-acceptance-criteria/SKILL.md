---
name: verify-acceptance-criteria
description: |
  Verify acceptance criteria quality and identify gaps.
  
  Use this skill whenever you need to evaluate acceptance criteria (ACs) to ensure they meet quality standards. Trigger on: "review these ACs", "check if these acceptance criteria are good", "validate my user story criteria", "improve our acceptance criteria", "audit these requirements", "do these ACs pass review", or similar requests. Also use proactively when someone shares acceptance criteria that look hastily written or vague. The skill analyzes criteria against five key dimensions (clarity, testability, outcome-focus, measurability, independence), scores issues by severity (critical/major/minor), and generates a structured report. It can also rewrite poor criteria into better ones or convert them to user story format.
compatibility: "Requires filesystem access to project directory. Works best with markdown and project context documents."
version: 1.0.0
argument-hint: "[paste ACs or describe feature]"
allowed-tools: [Read, Write, Bash]
---

# Acceptance Criteria Verifier

## When to Use

Use this skill to evaluate acceptance criteria quality. It's most valuable when:
- Reviewing criteria before development starts (catch issues early)
- Auditing existing criteria that have caused confusion or rework
- Ensuring criteria align with product standards
- Converting vague requirements into precise, testable statements
- Preparing criteria for team handoff to engineering

## Input Format

The skill accepts acceptance criteria in multiple formats:
- **Plain text**: A list pasted directly into the message
- **Markdown**: Bullet points or numbered lists
- **CSV/Excel**: Uploaded spreadsheet files
- **JSON**: Structured data
- **Mixed**: Any combination of the above

Example inputs:
```
Given the user is logged in
When they navigate to the dashboard
Then they should see a list of their recent items
```

Or:
```
- Display loads within 2 seconds
- All product images render correctly
- User can filter by category
```

## Evaluation Framework

Each acceptance criterion is evaluated against **five dimensions of quality**:

### 1. Clarity & Conciseness
- Is the language plain and unambiguous?
- Can all stakeholders interpret it the same way?
- Is it free of jargon or unexplained terms?
- Does it say exactly one thing, clearly?

**Critical Issues**: Ambiguous terms with multiple interpretations  
**Major Issues**: Vague language; jargon without definition  
**Minor Issues**: Wordy phrasing that could be tightened

### 2. Testability
- Can this criterion be objectively verified?
- Can it be mapped to one or more executable tests?
- Is there a clear pass/fail outcome?
- Would a QA engineer know exactly how to test it?

**Critical Issues**: No way to objectively verify the criterion  
**Major Issues**: Testability requires subjective judgment; unclear success state  
**Minor Issues**: Testable but the test path is not obvious

### 3. Outcome-Focused
- Does it describe the result, not the recipe?
- Does it focus on what the user experiences?
- Is it free of implementation details?
- Does it avoid prescribing the "how"?

**Critical Issues**: Criterion specifies technical implementation steps  
**Major Issues**: Mixes outcome with technical approach  
**Minor Issues**: Slight hints of implementation preference

### 4. Measurability
- Are expectations quantified where possible?
- Is there a definitive pass/fail threshold?
- Can success be objectively verified with data?
- Would different teams measure it the same way?

**Critical Issues**: No quantifiable metrics; purely subjective  
**Major Issues**: Quantification is vague ("fast", "many", "some")  
**Minor Issues**: Could be more precise (e.g., "300px" instead of "large")

### 5. Independence
- Does this criterion stand alone?
- Would it make sense without the others?
- Does it depend on other criteria to be meaningful?
- Can it be tested in isolation?

**Critical Issues**: Cannot be understood or tested without multiple other criteria  
**Major Issues**: Requires significant context from other criteria  
**Minor Issues**: Minor reference to another criterion for context

## Output Format

The skill generates a structured JSON report:

```json
{
  "summary": {
    "total_criteria": 5,
    "passed": 2,
    "failed": 3,
    "critical_issues": 2,
    "major_issues": 4,
    "minor_issues": 1,
    "overall_score": 65
  },
  "evaluations": [
    {
      "id": 1,
      "criterion": "The page should load fast",
      "status": "failed",
      "issues": [
        {
          "dimension": "Measurability",
          "severity": "critical",
          "description": "The term 'fast' is not quantified. What constitutes fast? 1 second? 5 seconds?"
        },
        {
          "dimension": "Testability",
          "severity": "major",
          "description": "Without a specific metric, QA cannot objectively verify this criterion."
        }
      ],
      "rewritten_option": "The page loads and displays all content within 2 seconds on a standard 4G connection"
    }
  ],
  "recommendations": [
    "Add specific metrics to 3 criteria that currently use vague descriptors",
    "Clarify technical dependencies between criteria 2 and 4",
    "Consider breaking criterion 5 into two independent criteria"
  ]
}
```

## How the Skill Works

### Step 1: Parse Input
The skill first identifies and extracts all acceptance criteria from the input, regardless of format.

### Step 2: Evaluate Against Five Dimensions
For each criterion, the skill evaluates it against:
- Clarity & Conciseness
- Testability
- Outcome-Focus
- Measurability
- Independence

### Step 3: Identify Issues
The skill identifies specific issues for each criterion and assigns a severity level:
- **Critical** (~45% of score): Issues that prevent testing or create ambiguity
- **Major** (~35% of score): Issues that make the criterion harder to interpret or test
- **Minor** (~20% of score): Issues that could be improved but don't block delivery

### Step 4: Calculate Scores
- Individual criterion score: (5 dimensions - issues) / 5 * 100
- Overall score: average of all criteria
- Pass threshold: 80+ is considered "good" quality

### Step 5: Suggest Improvements
For each failed criterion, the skill proposes a rewritten version that addresses the identified issues.

### Step 6: Generate Report
Output is structured JSON that can be:
- Reviewed directly in the chat
- Saved as a file for documentation
- Integrated into your workflow tools
- Used as the basis for discussions with your team

## Bonus: Rewrite to User Story Format

After generating the report, you can ask the skill to convert the improved acceptance criteria into full user story format:

```
As a [user type],
I want to [action],
So that [benefit].

Acceptance Criteria:
- [Criterion 1]
- [Criterion 2]
...
```

This provides context for engineering teams and helps them understand the "why" behind each criterion.

## Pro Tips

**1. Start with high-level scenarios**: If your input is very technical or vague, ask the skill to first help you write clear Given-When-Then scenarios.

**2. Review one criterion at a time**: For complex features, don't try to perfect all criteria at once. Review, implement, then move to the next.

**3. Use this before planning**: Run this evaluation during backlog refinement, not during sprint planning—catching issues early saves days of rework.

**4. Involve your QA team**: The testability dimension is often where QA engineers catch gaps. Use this report as a conversation starter.

**5. Iterate with stakeholders**: If the skill identifies ambiguity, use the report to drive a quick discussion with product and engineering about what you actually mean.

## Example: From Vague to Good

**Before (Failed):**
```
"The user should be able to search easily and find results quickly"
```

**Issues:**
- Measurability (critical): "easily" and "quickly" are subjective
- Testability (major): No clear way to verify  
- Clarity (minor): What is "search"? Database search, full-text, autocomplete?

**After (Passed):**
```
"The search results page displays at least 10 matching products within 1.5 seconds of the user typing their search query"
```

This version is measurable, testable, clear, and outcome-focused.

---

## How to Trigger This Skill

Ask your assistant to verify acceptance criteria by saying things like:
- "Review these acceptance criteria and tell me if they're good"
- "Check if these ACs will cause problems during testing"
- "Audit our user story criteria against quality standards"
- "Are these acceptance criteria testable?"
- "Rewrite these acceptance criteria to be clearer"
- "Do we have enough detail in these ACs for the team to start work?"

This skill will automatically and generate a structured evaluation report.
