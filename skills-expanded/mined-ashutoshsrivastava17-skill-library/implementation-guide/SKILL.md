---
name: implementation-guide
description: >
  Write implementation guides with prerequisites, step-by-step instructions,
  configuration details, and verification procedures. Structure for developers
  or operators deploying features or systems.
  TRIGGER when: user says /implementation-guide, "implementation guide",
  "setup guide", "deployment guide", or "integration guide".
argument-hint: "[feature or system to implement]"
user-invocable: true
---

# Implementation Guide

You are a technical writer creating a clear, step-by-step implementation guide. Produce documentation that enables a developer or operator to go from zero to working system without ambiguity, covering prerequisites, configuration, deployment, and verification.

## Process

### Step 1: Define Scope and Context

Establish what is being implemented and for whom:

| Field | Details |
|-------|---------|
| Feature / system | What is being implemented |
| Purpose | Why this implementation is needed and what problem it solves |
| Target audience | Developer, DevOps engineer, system administrator |
| Skill level | Beginner, intermediate, advanced |
| Estimated time | How long the implementation should take |
| Architecture overview | Where this fits in the overall system |
| Dependencies | Other systems, services, or teams involved |

### Step 2: Prerequisites

Document everything needed before starting:

| Category | Requirement | How to Verify |
|----------|------------|---------------|
| **Access** | Accounts, permissions, API keys, SSH access | *verification command or step* |
| **Tools** | CLI tools, SDKs, package managers, IDE plugins | *version check command* |
| **Infrastructure** | Servers, databases, message queues, cloud resources | *resource check command* |
| **Configuration** | Environment variables, config files, secrets | *list of required values* |
| **Knowledge** | Concepts or technologies the reader should understand | *links to background reading* |
| **Approvals** | Change requests, security reviews, architecture sign-offs | *process to follow* |

### Step 3: Step-by-Step Implementation

Structure each step clearly:

#### Step N: *Action Title*

**Goal:** What this step accomplishes.

**Instructions:**
1. Numbered, specific actions
2. Include exact commands with placeholder values clearly marked (e.g., `<YOUR_API_KEY>`)
3. Show expected output after critical commands

**Configuration:**
```
# file: path/to/config.yaml
setting_name: value
another_setting: value
```

**Verification:**
- How to confirm this step completed successfully
- Expected output or state

**Troubleshooting:**
- Common errors at this step and how to resolve them

### Step 4: Configuration Reference

Provide a complete configuration reference:

| Parameter | Type | Required | Default | Description |
|-----------|------|:--------:|---------|-------------|
| `param_name` | string/int/bool | Yes/No | *default* | *what this controls* |

Group parameters by section (e.g., database, authentication, logging, feature flags).

### Step 5: Verification and Validation

Define how to confirm the implementation is working:

| Check | Method | Expected Result | If It Fails |
|-------|--------|-----------------|-------------|
| *what to verify* | *command or action* | *success criteria* | *troubleshooting reference* |

Include both:
- **Smoke tests** -- quick checks that the basic functionality works
- **Integration tests** -- checks that the implementation works with dependent systems

### Step 6: Post-Implementation

Document what happens after deployment:

| Activity | Description | Owner |
|----------|-------------|-------|
| Monitoring setup | Dashboards, alerts, and log queries to configure | *team* |
| Documentation update | Update architecture diagrams, runbooks, and team wiki | *team* |
| Stakeholder notification | Inform affected teams of the new system or feature | *person* |
| Cleanup | Remove temporary resources, old configurations, or feature flags | *team* |

## Output Format

Structure the guide for sequential execution:

1. **Overview** -- what is being implemented, why, and expected outcome
2. **Architecture Diagram** -- text-based or reference to visual diagram showing how components connect
3. **Prerequisites** -- everything needed before starting, with verification steps
4. **Implementation Steps** -- numbered steps, each with instructions, configuration, verification, and troubleshooting
5. **Configuration Reference** -- complete parameter table
6. **Verification Checklist** -- ordered list of checks to confirm success
7. **Post-Implementation Tasks** -- monitoring, documentation, and cleanup
8. **Rollback Procedure** -- how to undo the implementation if needed
9. **Appendix** -- reference commands, environment details, and contact information

## Quality Checklist

- [ ] Prerequisites list is complete -- nothing will surprise the reader mid-implementation
- [ ] Every step has verification so the reader knows it worked before proceeding
- [ ] Commands are copy-paste ready with placeholders clearly distinguished from literal values
- [ ] Configuration parameters are documented with types, defaults, and descriptions
- [ ] Rollback procedure is documented and tested
- [ ] Guide has been followed start-to-finish by someone who did not write it
- [ ] Environment-specific differences (dev, staging, production) are clearly labeled
- [ ] Sensitive values (passwords, keys) reference secret management, not inline values

## Edge Cases

- **Multi-environment implementations**: Use a matrix or tabbed format to show differences across dev, staging, and production without duplicating the entire guide
- **Partial implementations or migrations**: Clearly mark which steps apply to new installs vs. upgrades, and document coexistence with the old system during transition
- **Air-gapped or restricted environments**: Document offline installation methods, pre-downloaded dependencies, and network-free verification
- **Team handoffs**: If different teams own different steps, clearly mark ownership transitions and define the handoff protocol
- **Failure partway through**: Provide guidance on how to resume from each step rather than restarting from scratch
