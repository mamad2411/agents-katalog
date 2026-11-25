Update available: cloakbrowser 0.3.31 → 0.4.8. Run: pip install --upgrade cloakbrowser
# What We Learned Building Cloud Agents | Cognition
Source: https://cognition.com/blog/what-we-learned-building-cloud-agents
What We Learned Building Cloud Agents | Cognition

Menu

Close

* [Home](/)
* [Careers](/careers)
* [Research](/research)
* [Blog](/blog)
* [Contact](/contact)
* [Devin](https://devin.ai)

* [Home](/)
* [Careers](/careers)
* [Research](/research)
* [Blog](/blog)
* [Contact](/contact)

[Devin](https://devin.ai)

# What We Learned Building Cloud Agents

By The Cognition Team04.23.26

Enterprises are converging on cloud agents as the future of software engineering — and many are concluding they should build their own. Posts like Stripe's, detailing how they built a [homegrown cloud agent](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents), make the path look achievable.

Building cloud agent infrastructure requires two investments: the technical infrastructure to run agents securely and autonomously in the cloud, and the change management to make agents productive across your engineering org. We've spent over two years on both, for Devin. What follows is what we've learned.

## **The Right Approach to Building Cloud Agents**

The natural starting point for building cloud agents is straightforward: take a CLI agent, containerize it, and give it access to your repos and toolchain. This successfully moves execution to the cloud — but you quickly run into security, persistence, and orchestration issues that need to be solved.

### **A shared kernel is a security threat**

Containerized agents share a kernel, which means one compromised session can access every other container's filesystems, credentials, and network connections. Agents generate their own code, run arbitrary commands, and probe the environment in unpredictable ways — making a kernel-level escape a real security threat.

![](https://cdn.sanity.io/images/2mc9cv2v/production/b453f6fb2146063f42137230abe555e9727e006e-1691x1000.png?w=1600&fit=max)

The industry consensus for running untrusted code is VM-level isolation — each workload gets its own kernel, with no shared attack surface. This is the direction the broader infrastructure community has been moving toward.

Standing up VM-based isolation for agent workloads is a significant undertaking. Our own implementation of microVMs took over a year of hypervisor engineering, ensuring every agent session runs on its own dedicated kernel with fully isolated storage, networking, and compute. A side benefit is that agents running in dedicated VMs can use a full browser, desktop applications, and arbitrary tool stacks, just like a developer on their workstation.

### **Containerized agents can't complete real engineering work**

Another problem with containerized agents is they cannot survive the async gaps that define most real engineering work. An agent opens a PR, waits on CI, responds to code review, reruns tests, and pushes a follow-up commit. Between each step, there are gaps — minutes, hours, sometimes days — where the agent must preserve its full working state. For bounded work like dependency upgrades, a single-pass agent that completes and exits is enough. But work that spans the async gaps of the SDLC remains out of reach.

![](https://cdn.sanity.io/images/2mc9cv2v/production/124905d593c97bfa5c9a95ca38623ec164fa7910-1687x1025.png?w=1600&fit=max)

The root issue is that containers do not provide a reliable way to snapshot an individual container's full state, shut down compute, and restore it later. A containerized agent can only survive async breaks by burning compute to stay alive — and if the container is rescheduled, times out, or crashes, the session is lost.

We solved this by snapshotting full machine state at the hypervisor level — memory, process trees, and filesystem. Compute shuts down while the agent is idle, and the session resumes exactly where it left off when a CI result or review comment arrives. Making this work reliably across thousands of concurrent sessions, each with different repos, dependencies, and runtime environments, took us longer than any other piece of infrastructure we have built to date.

### **Scaling from one session to hundreds requires its own infrastructure**

Running hundreds of cloud agents across an engineering org requires orchestration, governance, and integrations — each a multi-quarter infrastructure project on its own. A leading cloud data platform company we spoke with attempted this and ultimately moved on after the project scope overwhelmed their infrastructure team. The challenges they ran into:

* **Orchestration:** Each agent session is unique — tied to a specific task and engineer's permissions. Running hundreds concurrently requires provisioning the right environment for each one, routing sessions correctly, predicting demand to keep warm VM pools ready, and keeping every provisioned environment current as codebases change daily.
* **Governance:** Each session must inherit the dispatching engineer's permissions across every system it touches, with every action recorded in a tamper-evident audit trail. Building and maintaining identity chaining, access scoping, and audit logging at enterprise scale is its own engineering project that requires ongoing maintenance.
* **Integrations:** An agent is only as useful as the systems it can reach — CI, monitoring, package registries, documentation, source control. Each has its own authentication model, permission scoping, and maintenance burden. Stripe has an internal MCP server with over 400 tools to keep their agents connected. That is the scale of investment this layer demands.

The pattern we've seen, across conversations with teams attempting this, is that the combined surface area is what becomes untenable — not any single piece, but the fact that all three have to be built, integrated, and maintained indefinitely. We currently staff a dedicated team to manage each layer of this stack. Our solution for the orchestration layer took over three quarters of dedicated engineering to build and can manage thousands of concurrent VMs — handling provisioning, demand prediction, crash recovery, and teardown.

---

## The Right Approach to Deploying Cloud Agents

Everything we have discussed is what we consider the first phase: building the infrastructure to deploy cloud agents at scale. The second is transforming how your engineering organization actually works with them, and this process cannot start until the agents are deployed.

### **Engineering processes need to be rebuilt for agents**

Every engineering process inside an enterprise was designed for a world where humans do the work: how projects get scoped, how teams get staffed, how code gets reviewed and shipped. When agents are doing a significant share of the execution, those processes need to be rebuilt around a different operating model. One where agents execute and humans direct, review, and decide.

Getting there is both a technical and operational challenge. It requires people who understand the engineering systems and the business processes around them, many of which are deeply embedded and often not even documented. The questions it raises touch every part of how an engineering org operates, and none of them have straightforward answers:

* **Engineer fluency:** Engineers need to learn which work to delegate and which to keep, and how to define tasks precisely enough that agents execute without constant correction. Managing concurrent agent sessions is a fundamentally different skill from writing code, and it takes months of practice on real projects to develop.
* **Planning and resource allocation:** Every assumption about team sizing, sprint capacity, and project staffing changes when agent capacity enters the equation. These aren't one-time decisions. They have to be revisited as agents get more capable and engineers get more fluent.
* **Review and quality standards:** The volume of code that needs review increases dramatically, but the review process designed for human-authored code doesn't transfer cleanly. Teams need to establish what rigorous review looks like for agent-produced work at a much higher volume.

Very few of these changes can be designed in advance. Teams develop fluency by operating with agents on real projects over months. Starting earlier means your org is further along the learning curve — and that gap widens over time.

> Itaú, the largest private bank in Latin America, is eleven months in with nearly 17,000 engineers — and has completed migrations 5 to 6x faster, auto-remediated 70% of static-analysis security vulnerabilities, and increased test coverage by 2x.

Building cloud agent infrastructure has been a serious engineering commitment for us, and whether you decide to build in-house or work with an existing platform, we hope this post gave a useful picture of what the investments involve.

If you're thinking about how to get started — [reach out here](https://cognition.ai/contact).

04. ArticlesArticles

[![Estimating the Productivity of an Autonomous AI Software Engineer](/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2F2mc9cv2v%2Fproduction%2F8527b7c1b2b03f309d7ba9189296ac76a1c7b650-1920x1080.jpg%3Fw%3D640%26h%3D360%26fit%3Dcrop&w=1920&q=75)

Estimating the Productivity of an Autonomous AI Software Engineer

06.04.26](/blog/ai-productivity)[![AI should earn its keep: Introducing the AI Productivity Guarantee](/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2F2mc9cv2v%2Fproduction%2Fd378ef146ec6070438bfaeab4d9e47e8b886e55d-1920x1080.jpg%3Fw%3D640%26h%3D360%26fit%3Dcrop&w=1920&q=75)

AI should earn its keep: Introducing the AI Productivity Guarantee

06.04.26](/blog/ai-guarantee)[![Introducing Devin Desktop](/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2F2mc9cv2v%2Fproduction%2F5841a7932386c05dc112f92fda8ff519b38d4f9a-1920x1080.jpg%3Fw%3D640%26h%3D360%26fit%3Dcrop&w=1920&q=75)

Introducing Devin Desktop

06.02.26](/blog/introducing-devin-desktop)[![More Devins in More Places](/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2F2mc9cv2v%2Fproduction%2F58309361c06f31fa49f8c36e307963f21bd3f22b-1382x777.jpg%3Frect%3D1%2C0%2C1381%2C777%26w%3D640%26h%3D360%26fit%3Dcrop&w=1920&q=75)

More Devins in More Places

05.27.26](/blog/series-d)[![Devin in Windsurf](/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2F2mc9cv2v%2Fproduction%2F89fcacf48d33b51277268808596d123237018950-1920x1080.jpg%3Fw%3D640%26h%3D360%26fit%3Dcrop&w=1920&q=75)

Devin in Windsurf

04.15.26](/blog/devin-in-windsurf)[![An Early Preview of SWE-1.6 and Research Update](/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2F2mc9cv2v%2Fproduction%2F6ce843c49d6a38e1c0045e43891aca89fccd8981-1500x844.jpg%3Fw%3D640%26h%3D360%26fit%3Dcrop&w=1920&q=75)

An Early Preview of SWE-1.6 and Research Update

03.01.26](/blog/swe-1-6-preview)[![How Cognition Uses Devin to Build Devin](/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2F2mc9cv2v%2Fproduction%2Fc1e05d959a8c25c8df5e86198a4213e4fd634b61-1500x844.jpg%3Fw%3D640%26h%3D360%26fit%3Dcrop&w=1920&q=75)

How Cognition Uses Devin to Build Devin

02.27.26](/blog/how-cognition-uses-devin-to-build-devin)[![Introducing Cognition for Government](/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2F2mc9cv2v%2Fproduction%2F164f27869605d7c326a68e511efcf1a4077fc2b7-1920x1080.jpg%3Fw%3D640%26h%3D360%26fit%3Dcrop&w=1920&q=75)

Introducing Cognition for Government

02.25.26](/blog/cognition-for-government)[![Introducing Devin 2.2](/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2F2mc9cv2v%2Fproduction%2F5638cfd0a8a65ad3074019b69c3aa05e112577b7-1920x1080.jpg%3Fw%3D640%26h%3D360%26fit%3Dcrop&w=1920&q=75)

Introducing Devin 2.2

02.24.26](/blog/introducing-devin-2-2)

* [Linkedin](https://www.linkedin.com/company/cognition-ai-labs)
* [X [Twitter]](https://x.com/cognition)

* [Website Terms of Use](/legal/website-terms-of-use)
* [Enterprise Terms of Service](/legal/enterprise-terms-of-service)
* [Platform Terms of Service](/legal/platform-terms-of-service)
* [Data Processing Addendum](/legal/data-processing-statement)

* [Privacy Policy](/legal/privacy-policy)
* [Acceptable Use Policy](/legal/acceptable-use-policy)
* [Report Vulnerability](/report-vulnerability)
* [Security](/legal/security)
