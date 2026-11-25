---
name: Tech Role Resume
description: Optimize resumes specifically for software engineering, product management, data science, and other technical roles. Use this skill when someone is applying for SWE, PM, data, DevOps, SRE, ML, or other technical positions. Trigger for "tech resume", "engineer resume", "developer resume", "PM resume", "technical skills section", or any request to highlight technical depth, system scale, or engineering achievements.
---

# Tech Role Resume

Structure a resume for technical hiring, where both ATS filters and engineering reviewers need to be satisfied.

## Technical Skills Section

This is the most critical section for ATS matching in tech roles. Organize by category:

```
Languages: [order by relevance to target role]
Frameworks: [web, data, mobile, or testing frameworks]
Databases: [relational and NoSQL]
Infrastructure: [cloud services, containers, CI/CD, monitoring]
Tools: [version control, project management, IDEs, etc.]
```

Only list technologies you can discuss in a technical interview. If you used it once in a tutorial, leave it off.

## Technical Achievement Formula

Every bullet should follow: **[Verb] + [technical what] + [at what scale] + [with what business result]**

Weak: "Built backend services"
Strong: "Designed event-driven order processing service handling 15K transactions per minute with 99.95% uptime, reducing checkout failures by 60%"

### Scale Metrics for Tech
- Users: DAU, MAU, concurrent users
- Throughput: requests/second, events/day, records processed
- Performance: latency reduction (ms), load time improvement
- Reliability: uptime percentage, error rate reduction
- Cost: infrastructure savings ($), resource efficiency
- Speed: deployment frequency, time-to-production reduction

## Role-Specific Emphasis

**Software Engineer:** System design, code quality, performance optimization, debugging complex issues, mentoring

**Product Manager:** Roadmap ownership, user research, cross-functional alignment, feature prioritization, launch metrics

**Data Engineer:** Pipeline architecture, data quality, processing volume, latency improvements, schema design

**DevOps/SRE:** Infrastructure automation, monitoring, incident response, deployment pipelines, cost optimization

**Data Scientist/ML:** Model accuracy, business impact of predictions, data volume, feature engineering, A/B testing

## Projects Section

Critical for junior engineers, bootcamp graduates, and career changers. Format:

```
Project Name | Tech Stack | github.com/user/project
One-sentence description of what it does and why
Key technical highlight (scale, architecture, or clever solution)
```

Include projects where you can explain every architectural decision. Exclude tutorial follow-alongs and trivial apps.

## GitHub Profile Tips

- Pin your 6 best repositories
- Write thorough READMEs (what it does, how to run it, architecture decisions)
- Maintain an active contribution graph
- Include a profile README
