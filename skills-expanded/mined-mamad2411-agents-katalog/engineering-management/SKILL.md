# Engineering Management Skill

**For people managers leading infrastructure, platform, SRE, security, and development teams.**

> This skill focuses on team organization, hiring, career development, resource planning, and people management—not hands-on technical implementation. Complements the technical skills in this repository.

---
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 SKILL ACTIVATED: engineering-management
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


## When to Use This Skill

**You're a manager who needs help with:**
- Organizing teams (platform teams, SRE teams, security teams)
- Hiring engineers and assessing technical skills
- Building career ladders and progression frameworks
- Planning resources and capacity across teams
- Conducting technical interviews
- Running effective 1-on-1s with engineers
- Understanding team structures and reporting lines

**This skill does NOT cover:**
- Hands-on technical implementation (see technical skills)
- Executive strategy (see infrastructure-strategy skill)
- Budget/cost management (see budget-and-cost-management skill)
- Operations/on-call management (see engineering-operations-management skill)

---

## Core Areas

### 1. Team Organization Patterns

**Modern infrastructure team structures:**

```
Traditional Silo Model (❌ Avoid):
├── Development Team (builds features)
├── Operations Team (deploys & maintains)
└── Security Team (audits & blocks)
Result: Friction, blame, slow delivery

Platform Engineering Model (✅ Preferred):
├── Platform Team (builds developer experience)
├── Product Teams (build features using platform)
└── Enabling Teams (SRE, Security, provide expertise)
Result: Autonomy, fast delivery, shared responsibility
```

**Common team patterns:**
- **Platform Engineering Team** - IaC, K8s, CI/CD, internal developer platform
- **SRE Team** - Reliability, monitoring, incident response, SLOs
- **Security Engineering Team** - Security automation, compliance, vulnerability management
- **Cloud Engineering Team** - Cloud architecture, migration, cost optimization
- **Release Engineering Team** - CI/CD pipelines, deployment automation
- **Database Engineering Team** - Database reliability, performance, migrations

**See:** [team-organization-patterns.md](resources/team-organization-patterns.md)

### 2. Hiring & Skill Assessment

**Engineering hiring process:**

```
1. Define Role & Level
   ├── IC levels: Junior (L3) → Senior (L5) → Staff (L6) → Principal (L7+)
   ├── Skills matrix: Must-have vs Nice-to-have
   └── Compensation band

2. Source Candidates
   ├── Job description that attracts right level
   ├── Realistic preview of day-to-day work
   └── Internal referrals (highest quality)

3. Technical Assessment
   ├── Resume screen (filtering for experience level)
   ├── Phone screen (basics + fit)
   ├── Technical interview (deep dive on skills)
   ├── System design (architecture thinking)
   └── Behavioral interview (culture fit)

4. Make Offer
   ├── Sell the role and team
   ├── Competitive compensation
   └── Quick decision loop
```

**Skill assessment frameworks:**
- Platform Engineering: IaC, K8s, CI/CD, GitOps
- SRE: Observability, incident response, automation, Linux
- Security: Threat modeling, compliance, security tools
- Cloud: AWS/Azure/GCP, cost optimization, architecture

**See:** [hiring-and-assessment.md](resources/hiring-and-assessment.md)

### 3. Career Ladders

**Infrastructure engineering career ladder:**

```
Individual Contributor (IC) Track:

L3: Junior Engineer
├── Executes well-defined tasks with guidance
├── Learning fundamentals of systems/cloud/security
└── Focus: Skill development

L4: Engineer
├── Owns small-to-medium projects independently
├── Proficient in core technologies
└── Focus: Execution

L5: Senior Engineer
├── Owns large projects, mentors junior engineers
├── Expert in domain, influences team decisions
└── Focus: Technical leadership + mentorship

L6: Staff Engineer
├── Drives multi-team initiatives, sets technical direction
├── Domain expert, shapes architecture
└── Focus: Technical strategy + broad impact

L7+: Principal/Distinguished Engineer
├── Drives organization-wide technical strategy
├── Industry expert, represents company externally
└── Focus: Vision + strategic impact
```

**Manager Track:**

```
M3: Engineering Manager
├── Manages 5-8 engineers (typically L3-L5)
├── Delivers team roadmap, handles people issues
└── Focus: Team execution + people development

M4: Senior Engineering Manager
├── Manages 8-12 engineers OR 2-3 teams
├── Influences department strategy, mentors other managers
└── Focus: Multi-team coordination + strategy

M5: Director of Engineering
├── Manages 30-50 engineers across multiple teams
├── Sets department vision, resource allocation
└── Focus: Organization building + strategic planning

M6+: VP/SVP/CTO
├── Manages entire engineering organization
├── Sets technical vision for company
└── Focus: Executive strategy + leadership
```

**See:** [career-ladders.md](resources/career-ladders.md)

### 4. Resource Planning

**Capacity planning for managers:**

```
Team Capacity Model:

Available Capacity = Team Size × Available Hours
├── Team Size: Number of engineers
├── Available Hours: ~30 hrs/week per engineer
    ├── 40 hrs/week
    ├── - 2 hrs meetings
    ├── - 3 hrs context switching
    ├── - 2 hrs interruptions
    ├── - 3 hrs toil/ops work
    └── = ~30 productive hours

Capacity Allocation:
├── 70% Feature/project work
├── 20% Tech debt & refactoring
├── 10% Learning & innovation
└── Adjust based on team maturity
```

**When to hire:**
- Team consistently at >90% capacity for 3+ months
- Critical projects delayed due to capacity constraints
- Engineers working unsustainable hours
- Key person risk (single points of failure)

**When NOT to hire:**
- Temporary spike in work
- Process inefficiencies that hiring won't solve
- Unclear scope or requirements
- Budget constraints

**See:** [resource-planning.md](resources/resource-planning.md)

### 5. Technical Interviews

**Interview guide for managers:**

**Phone Screen (30 min):**
```
Goals: Filter for basics + culture fit
├── Background & experience (5 min)
├── Technical basics (15 min)
│   ├── "Walk me through a recent project"
│   ├── "What technologies did you use?"
│   └── "What challenges did you face?"
├── Logistics & expectations (5 min)
└── Q&A (5 min)
```

**Technical Deep Dive (60 min):**
```
Goals: Assess depth of technical knowledge
├── Domain expertise (30 min)
│   ├── Platform: "Design a CI/CD pipeline for microservices"
│   ├── SRE: "How would you debug high latency?"
│   ├── Security: "Threat model this architecture"
│   └── Cloud: "Design multi-region active-active on AWS"
├── Problem solving (20 min)
│   └── Real scenario from your team's work
└── Questions for us (10 min)
```

**System Design (60 min):**
```
Goals: Assess architecture/design thinking
├── Present problem (5 min)
├── Candidate designs solution (40 min)
│   ├── Clarifying questions
│   ├── High-level design
│   ├── Deep dive on components
│   └── Trade-offs and alternatives
├── Feedback & discussion (10 min)
└── Questions (5 min)
```

**Question banks:**
- Platform Engineering: K8s operators, GitOps workflows, IaC patterns
- SRE: SLO design, incident response, observability
- Security: Zero Trust, compliance, threat modeling
- Cloud: Multi-cloud, cost optimization, serverless

**See:** [technical-interviews.md](resources/technical-interviews.md)

### 6. One-on-One Guides

**Effective 1-on-1 structure:**

```
Weekly 1-on-1 (30 min):

First 15 min - Their Agenda:
├── "What's top of mind for you?"
├── Unblock obstacles
├── Discuss challenges
└── Surface concerns early

Last 15 min - Your Agenda:
├── Project updates & priorities
├── Feedback (both directions)
├── Career development
└── Team/org updates
```

**Monthly Career 1-on-1 (60 min):**
```
Focus on growth & development:
├── Progress toward career goals (20 min)
├── Skills to develop (20 min)
├── Projects for growth (10 min)
└── Long-term aspirations (10 min)
```

**Questions to ask:**
- **Engagement:** "What part of your work energizes you? What drains you?"
- **Obstacles:** "What's slowing you down? How can I help?"
- **Growth:** "What skills do you want to develop?"
- **Team:** "How's the team dynamic? Any concerns?"
- **Feedback:** "What could I do differently to support you better?"

**Red flags to watch for:**
- Disengagement (short answers, lack of enthusiasm)
- Burnout signals (working late, weekends, stress)
- Conflict with teammates (complaints, friction)
- Career stagnation (no growth, bored)

**See:** [one-on-one-guides.md](resources/one-on-one-guides.md)

---

## Integration with Other Skills

**This skill works with:**
- **technical-leadership** - For architecture review and tech decision frameworks
- **infrastructure-strategy** - For roadmapping and technology selection
- **engineering-operations-management** - For on-call, incidents, SRE operations
- **budget-and-cost-management** - For headcount and infrastructure budgets

**Technical skills for understanding your team's work:**
- **platform-engineering** - What your platform team does
- **sre** - What your SRE team does
- **devsecops** / **cybersecurity** - What your security team does
- **cloud-engineering** - What your cloud team does

---

## Quick Reference

**Team Organization:**
- Use platform model, not silos
- Clear team charters and responsibilities
- Avoid dependencies between teams

**Hiring:**
- Define level and skills clearly
- Multi-stage interview (phone → technical → system design → behavioral)
- Move fast - top candidates have multiple offers

**Career Development:**
- Clear ladder (L3 → L4 → L5 → L6 → L7+)
- Regular career conversations (monthly)
- Growth opportunities through projects

**Resource Planning:**
- ~30 productive hours/week per engineer
- 70% features, 20% tech debt, 10% innovation
- Hire when consistently >90% capacity for 3+ months

**1-on-1s:**
- Weekly 30 min (their agenda + your agenda)
- Monthly 60 min for career development
- Ask open-ended questions, listen actively

---

## For More Details

Each resource file provides deep dives on specific topics:

1. **team-organization-patterns.md** - Platform teams, SRE teams, security teams, reporting structures
2. **hiring-and-assessment.md** - Job descriptions, interview processes, skill assessment frameworks
3. **career-ladders.md** - IC track, manager track, promotion criteria, compensation
4. **resource-planning.md** - Capacity models, when to hire, allocation frameworks
5. **technical-interviews.md** - Question banks, interview scripts, evaluation rubrics
6. **one-on-one-guides.md** - 1-on-1 templates, questions, career conversation guides

---

**Remember:** Your job as a manager is to:
1. **Hire great people** and help them grow
2. **Remove obstacles** so your team can execute
3. **Set direction** and priorities
4. **Build culture** of collaboration and excellence
5. **Represent your team** to the rest of the organization

You don't need to be the best technical person on the team—you need to enable your team to do their best work.
