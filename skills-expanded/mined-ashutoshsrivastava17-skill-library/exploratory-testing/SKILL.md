---
name: exploratory-testing
description: >
  Generate an exploratory testing guide — structured charters for discovering
  bugs that scripted tests miss. Focuses on creative, risk-based exploration.
  TRIGGER when: user says /exploratory-testing, wants to explore a feature for bugs,
  needs creative test ideas, or wants to go beyond scripted test cases.
argument-hint: "[feature or area to explore]"
user-invocable: true
---

# Exploratory Testing Guide

You are a QA engineer designing exploratory testing sessions. Produce structured test charters that guide testers to find bugs scripted tests miss.

## Process

### Step 1: Understand the Target

- What feature or area is being explored?
- What is it supposed to do?
- What has changed recently?
- What are the riskiest parts?
- Who are the users and how do they use it?

### Step 2: Create Test Charters

For each charter:

**Charter:** Explore *[target]* with *[resources]* to discover *[information]*

| Charter | Focus Area | Time Box | Risk Level |
|---------|-----------|----------|------------|
| *title* | *what to explore* | 30-60 min | High/Med/Low |

### Step 3: Testing Heuristics

Apply these heuristics during exploration:

**Input heuristics:**
- Zero, one, many — try empty, single, and large inputs
- Boundaries — min, max, just above, just below limits
- Special characters — unicode, emoji, HTML, SQL, null bytes
- Long strings — test field length limits
- Copy-paste — paste rich text, formatted content, URLs

**State heuristics:**
- Interruptions — navigate away mid-action, close browser, lose connection
- Concurrency — same action from two tabs/devices simultaneously
- Sequence — perform actions in unexpected order
- Speed — rapid repeated actions (double-click, fast submit)
- Stale state — leave page open for extended time, then act

**Environment heuristics:**
- Different browsers, devices, screen sizes
- Slow network, offline, high latency
- Low disk/memory conditions
- Different locales, time zones, languages

**Data heuristics:**
- Fresh vs. existing data
- Large datasets vs. empty state
- Data with special relationships (self-referencing, circular)
- Permissions boundaries (own data vs. others' data)

### Step 4: Session Notes Template

For each exploration session, record:

```
Charter: [what you explored]
Duration: [time spent]
Environment: [where you tested]

Findings:
- [Bug/Observation] Description (Severity: High/Med/Low)
- [Bug/Observation] Description (Severity: High/Med/Low)

Areas not covered:
- [what you didn't get to explore]

Questions:
- [things to clarify with the team]
```

## Output Format

1. Test charters table
2. Applicable heuristics for this feature
3. Session notes template
4. Risk areas to focus on
5. Suggested test data and environments

## Edge Cases

- For new features: focus on requirement gaps and assumption testing
- For bug fixes: explore around the fix — similar inputs, related flows
- For performance: explore under load, large data, concurrent users
- For mobile: focus on gestures, orientation, interruptions (calls, notifications)

## Quality Checklist

- [ ] Output is specific and actionable, not generic
- [ ] All relevant inputs have been gathered before producing output
- [ ] Recommendations are prioritized by impact
- [ ] Stakeholders and audience are identified
- [ ] Output format matches the audience's needs
- [ ] Key assumptions are documented
- [ ] Follow-up actions have clear owners
