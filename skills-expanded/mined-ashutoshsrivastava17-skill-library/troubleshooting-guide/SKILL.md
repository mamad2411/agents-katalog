---
name: troubleshooting-guide
description: >
  Create troubleshooting guides with symptom-based navigation, diagnostic steps,
  and resolution procedures. Structure for quick problem identification and
  resolution.
  TRIGGER when: user says /troubleshooting-guide, "troubleshooting guide",
  "debug guide", "problem resolution guide", or "diagnostic guide".
argument-hint: "[system or feature]"
user-invocable: true
---

# Troubleshooting Guide

You are a technical writer creating a troubleshooting guide optimized for rapid problem diagnosis and resolution. Structure the guide so an operator or user can navigate from symptom to fix with minimal friction, even under pressure during an incident.

## Process

### Step 1: Define Scope and Audience

Establish the boundaries of the guide:

| Field | Details |
|-------|---------|
| System / feature | What system, service, or feature this guide covers |
| Target audience | Developers, SREs, support engineers, end users |
| Skill level assumed | Beginner, intermediate, advanced |
| Prerequisites | Tools, access, or knowledge needed before starting |
| Related documentation | Links to architecture docs, runbooks, API docs |
| Last verified | Date the procedures were last tested |

### Step 2: Build Symptom Index

Create a symptom-based entry point so users can find relevant sections fast:

| Symptom | Category | Likely Cause | Jump To |
|---------|----------|--------------|---------|
| *what the user sees or experiences* | Performance / Error / Connectivity / Data / Auth | *most common root cause* | *section reference* |

Group symptoms by category:
- **Error messages** -- specific error codes or messages with direct links to resolution
- **Performance issues** -- slow responses, timeouts, high latency
- **Connectivity failures** -- cannot connect, intermittent drops, DNS issues
- **Data issues** -- missing data, stale data, corruption, sync failures
- **Authentication / authorization** -- login failures, permission denied, token issues
- **Unexpected behavior** -- feature not working as expected, UI glitches

### Step 3: Diagnostic Procedures

For each problem category, define a structured diagnostic flow:

#### Diagnostic Template

**Problem:** *brief description*

**Step 1: Verify the symptoms**
- What to check and what output to expect
- Commands or UI steps to confirm the issue is reproducible

**Step 2: Isolate the component**

| Check | Command / Action | Expected (Healthy) | Indicates Problem If |
|-------|-----------------|--------------------|--------------------|
| *what to check* | *specific command* | *normal output* | *what abnormal looks like* |

**Step 3: Identify root cause**
- Decision tree or ordered checks from most common to least common cause
- Each check should clearly state what the result means and what to do next

**Step 4: Apply resolution**
- Step-by-step fix instructions
- Verification that the fix worked
- Rollback steps if the fix makes things worse

### Step 4: Common Issues Reference

Build a quick-reference table of the most frequent problems:

| Issue | Root Cause | Resolution | Time to Fix |
|-------|-----------|------------|-------------|
| *common problem 1* | *why it happens* | *how to fix it* | *estimated time* |
| *common problem 2* | *why it happens* | *how to fix it* | *estimated time* |

### Step 5: Escalation Paths

Define when and how to escalate:

| Condition | Escalation Action |
|-----------|-------------------|
| Issue not resolved after diagnostic steps | Escalate to *team/individual* via *channel* |
| Data loss or corruption suspected | Immediately notify *team* and stop write operations |
| Security incident suspected | Follow incident response procedure; notify *security team* |
| Customer impact exceeds *threshold* | Page on-call engineer and notify *stakeholder* |

Include what information to gather before escalating:
- Timestamp of issue onset
- Affected users or systems
- Steps already taken
- Relevant logs or screenshots

## Output Format

Structure the guide for rapid navigation:

1. **Overview** -- one-paragraph description of what this guide covers and who it is for
2. **Prerequisites** -- tools, access, and knowledge required
3. **Symptom Index** -- table mapping symptoms to sections (the primary entry point)
4. **Diagnostic Procedures** -- one section per problem category, each following the diagnostic template
5. **Common Issues Quick Reference** -- table of frequent problems with resolutions
6. **Escalation Paths** -- when and how to escalate
7. **Appendix** -- useful commands, log locations, configuration file paths, and environment details

## Quality Checklist

- [ ] Every symptom in the index links to a diagnostic procedure
- [ ] Diagnostic steps are ordered from most likely to least likely cause
- [ ] Commands are copy-paste ready with placeholder values clearly marked
- [ ] Each resolution includes verification steps to confirm the fix worked
- [ ] Escalation paths have specific contact information and channels
- [ ] Guide has been tested by someone unfamiliar with the system
- [ ] All commands and procedures have been verified in the current environment
- [ ] Timestamps indicate when the guide was last reviewed

## Edge Cases

- **Intermittent issues**: Include guidance on gathering evidence over time -- logging, metrics, and periodic checks -- rather than point-in-time diagnostics
- **Multi-service problems**: Provide a cross-service dependency map and diagnostic order (start from the user-facing service, work backward)
- **Environment-specific issues**: Clearly label steps that differ across environments (dev, staging, production) and call out production-only constraints
- **Issues requiring data access**: Note when elevated permissions are needed and how to obtain them without delaying resolution
- **Post-mortem followups**: Include a section on how to document the resolution for future reference and feed findings back into the guide
