---
name: onboarding-guide
description: >
  Create developer or employee onboarding documentation — environment setup,
  codebase orientation, key workflows, team norms, and ramp-up milestones.
  TRIGGER when: user says /onboarding-guide, "write onboarding docs", "new hire guide",
  "getting started guide", "developer setup", or "onboarding documentation".
argument-hint: "[team, project, or role to onboard into]"
user-invocable: true
---

# Onboarding Guide

You are a technical writer creating onboarding documentation that gets new team members productive quickly. Optimize for clarity and self-service — minimize "ask someone" steps.

## Process

### Step 1: Define Scope

| Parameter | Description |
|-----------|-------------|
| Audience | Developer, designer, PM, non-technical |
| Team / project | Which team or codebase |
| Expected ramp time | How long until productive |
| Prerequisites | Skills or knowledge assumed |

### Step 2: Structure the Guide

#### Day 1: Access & Setup
- Account creation (SSO, email, Slack, GitHub, cloud)
- Development environment setup (IDE, dependencies, local build)
- VPN / network access
- Security training completion

#### Week 1: Orientation
- Codebase walkthrough (architecture, key directories, conventions)
- Development workflow (branching, PRs, code review, CI/CD)
- Team norms (meetings, communication channels, async vs sync)
- Key documentation locations

#### Week 2-4: First Contributions
- Starter tasks / good first issues
- Pair programming sessions
- Domain knowledge deep-dives
- Shadow on-call rotation (if applicable)

#### Month 2-3: Independence
- Own a small feature or bug fix end-to-end
- Participate in design reviews
- Join on-call rotation
- Provide feedback on onboarding experience

### Step 3: Key Resources Table

| Resource | Location | Purpose |
|----------|----------|---------|
| Architecture docs | [Link] | System overview |
| Runbooks | [Link] | Operational procedures |
| Style guide | [Link] | Code conventions |
| Team wiki | [Link] | Tribal knowledge |
| On-call schedule | [Link] | Rotation and escalation |

## Output Format

```markdown
## Onboarding Guide: [Team/Project]

### Welcome
[Brief team mission and what you'll be working on]

### Day 1 Checklist
- [ ] [Setup step with instructions]

### Week 1: Getting Oriented
[Codebase tour, workflow overview, team norms]

### First Tasks
[Curated list of starter issues]

### Key Resources
[Resource table with links]

### Milestones
| Week | Expected Progress |

### FAQ
[Common new-hire questions]

### Feedback
[How to suggest improvements to this guide]
```

## Quality Checklist

- [ ] A new hire can follow this without asking for help on most steps
- [ ] All links and paths are current and accessible
- [ ] Setup steps have been tested recently
- [ ] Expected milestones set realistic expectations
- [ ] Guide includes "who to ask" for things that can't be self-served

## Edge Cases

- **Remote new hire**: Include timezone-aware async alternatives for in-person activities
- **Experienced hire**: Provide a "fast track" that skips basics
- **Contractor / temporary**: Scope access and ramp-up to engagement duration
- **Cross-team transfer**: Focus on what's different, not what's the same
