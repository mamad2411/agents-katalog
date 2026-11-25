---
name: threat-model
description: Structured threat modeling using STRIDE methodology. Identifies assets, entry points, threats, and mitigations with data flow diagrams and risk matrices. USE WHEN threat model, STRIDE analysis, risk assessment, threat analysis, identify threats, security architecture review, attack surface, trust boundaries.
---

# Threat Modeling

Skill for structured threat modeling using STRIDE methodology. Identifies assets, entry points,
threats, and mitigations for systems and applications. Produces formal threat model documents
with data flow diagrams, risk matrices, and prioritized remediation plans.

## When to Use This Skill

Activate when the user requests:
- "create threat model", "threat model this", "threat model [system/app]"
- "what are the threats to", "attack scenarios for", "how would I attack"
- "STRIDE analysis", "risk assessment", "threat analysis"
- "identify threats", "security architecture review"
- "data flow diagram", "trust boundaries", "attack surface analysis"
- Any request involving systematic threat identification and risk assessment

## Process Overview

Follow this 7-step process for every threat model:

```
1. Define Scope --> 2. Identify Assets --> 3. Identify Entry Points
    --> 4. Create Data Flow Diagram --> 5. Identify Trust Boundaries
    --> 6. Enumerate Threats (STRIDE) --> 7. Assess Risk and Propose Mitigations
```

## Step 1: Define Scope

Before modeling, establish:
- **System name and version** -- what exactly is being modeled
- **Boundaries** -- what is in-scope and out-of-scope
- **Depth** -- high-level architecture vs. detailed component analysis
- **Perspective** -- external attacker, insider threat, supply chain, or all

Ask the user to clarify scope if not provided. A threat model without clear boundaries is not useful.

## Step 2: Identify Assets

Catalog everything worth protecting:

### Asset Categories

| Category | Examples |
|---|---|
| Data | User credentials, PII, financial records, API keys, session tokens |
| Services | Authentication service, payment processor, API gateway |
| Infrastructure | Databases, message queues, storage buckets, DNS |
| Intellectual Property | Source code, algorithms, business logic, configurations |
| Availability | System uptime, SLA commitments, critical workflows |

### For Each Asset Document

- Asset name and description
- Classification (public, internal, confidential, restricted)
- Owner/responsible team
- Where it is stored, processed, and transmitted
- Existing protections

## Step 3: Identify Entry Points

Map all ways data or users interact with the system:

### Entry Point Types

| Type | Examples |
|---|---|
| User interfaces | Web UI, mobile app, CLI, admin console |
| API endpoints | REST APIs, GraphQL, gRPC, webhooks |
| Network services | SSH, DNS, SMTP, database ports |
| Data ingestion | File uploads, message queues, ETL pipelines, third-party feeds |
| Authentication | Login forms, SSO/SAML, OAuth flows, API keys |
| Administrative | Admin panels, deployment pipelines, configuration interfaces |

### For Each Entry Point Document

- Entry point name and location
- Protocol and transport
- Authentication requirements
- Input types accepted
- Trust level of typical users

## Step 4: Create Data Flow Diagram (DFD)

Build a text-based DFD showing how data moves through the system.

### DFD Elements

| Symbol | Meaning | Representation |
|---|---|---|
| Rectangle | External entity (user, third-party) | `[User]` |
| Rounded rectangle | Process | `(Auth Service)` |
| Open rectangle | Data store | `[[Database]]` |
| Arrow | Data flow | `-->` |
| Dashed line | Trust boundary | `--- boundary ---` |

### Example DFD (text-based)

```
[Browser User] --HTTPS--> (Load Balancer)
                              |
                  --- DMZ / Internal boundary ---
                              |
                    (API Gateway) --gRPC--> (Auth Service)
                         |                      |
                         |               [[User DB]]
                         |
                    (App Service) --SQL--> [[App DB]]
                         |
                    (Queue) --async--> (Worker Service)
                         |
                  --- Internal / Third-party boundary ---
                         |
                    [Payment Provider API]
```

Adapt the DFD to the actual system being modeled. Include all significant data flows
and processing steps.

## Step 5: Identify Trust Boundaries

Trust boundaries exist wherever the level of trust changes:

### Common Trust Boundaries

| Boundary | Description |
|---|---|
| Internet / DMZ | External users to public-facing services |
| DMZ / Internal | Load balancer to internal application |
| Application / Database | App server to data storage |
| Internal / Third-party | Internal services to external APIs |
| User roles | Regular user to admin, tenant A to tenant B |
| Process boundaries | Container/VM isolation, service mesh |

### For Each Boundary Document

- What crosses the boundary (data, requests, credentials)
- What controls exist at the boundary (firewall, auth, encryption)
- What assumptions are made about trust on each side

## Step 6: Enumerate Threats Using STRIDE

Apply STRIDE to every component and data flow in the DFD.

### STRIDE Categories

| Category | Description | Violates | Question to Ask |
|---|---|---|---|
| **S**poofing | Pretending to be something or someone else | Authentication | Can an attacker impersonate a user, service, or component? |
| **T**ampering | Modifying data or code without authorization | Integrity | Can an attacker modify data in transit, at rest, or in processing? |
| **R**epudiation | Denying having performed an action | Non-repudiation | Can a user deny performing a critical action with no audit trail? |
| **I**nformation Disclosure | Exposing data to unauthorized parties | Confidentiality | Can sensitive data leak through errors, logs, side channels, or weak access control? |
| **D**enial of Service | Making a system unavailable | Availability | Can an attacker exhaust resources or crash the system? |
| **E**levation of Privilege | Gaining higher access than authorized | Authorization | Can an attacker escalate from user to admin, or escape sandbox/container? |

### Threat Enumeration Process

For each component/data flow in the DFD:
1. Walk through each STRIDE category
2. Ask the corresponding question
3. If the answer is "yes" or "maybe", document the threat
4. Assign a threat ID (T01, T02, etc.)

### Threat Table Format

| ID | Component | STRIDE | Threat Description | Attack Vector |
|---|---|---|---|---|
| T01 | Login form | Spoofing | Credential stuffing attack | Automated login attempts with breached credentials |
| T02 | API Gateway | Tampering | Request parameter manipulation | Modified API requests bypass validation |
| T03 | App Service | Info Disclosure | Verbose error messages | Stack traces in 500 responses leak internals |
| T04 | User DB | Elevation | SQL injection to admin | Injected SQL in search field modifies role |

## Step 7: Assess Risk and Propose Mitigations

### Risk Scoring: Likelihood x Impact

**Likelihood Scale:**

| Rating | Score | Description |
|---|---|---|
| Low | 1 | Requires significant skill, insider access, or rare conditions |
| Medium | 2 | Achievable by a motivated attacker with moderate skill |
| High | 3 | Easily exploitable, automated tools available, publicly known |

**Impact Scale:**

| Rating | Score | Description |
|---|---|---|
| Low | 1 | Minor inconvenience, no data exposure, minimal business impact |
| Medium | 2 | Limited data exposure, partial service disruption, moderate business impact |
| High | 3 | Significant data breach, major service outage, severe business impact |
| Critical | 4 | Complete system compromise, mass data breach, existential business impact |

**Risk Score = Likelihood x Impact**

| Risk Score | Rating | Action |
|---|---|---|
| 1-3 | Low | Accept or address in future iteration |
| 4-6 | Medium | Plan remediation within next sprint/quarter |
| 7-9 | High | Prioritize remediation immediately |
| 10-12 | Critical | Stop and fix before deployment/release |

### Risk Matrix Visualization

```
              Impact
              Low(1)  Med(2)  High(3)  Crit(4)
Likelihood
High(3)     |  3    |  6    |   9    |  12   |
Med(2)      |  2    |  4    |   6    |   8   |
Low(1)      |  1    |  2    |   3    |   4   |
```

### Mitigation Format

For each threat, propose specific mitigations:

| Threat ID | Mitigation | Type | Priority | Effort |
|---|---|---|---|---|
| T01 | Implement rate limiting + account lockout | Preventive | High | Medium |
| T02 | Add input validation + parameterized queries | Preventive | Critical | Low |
| T03 | Implement custom error pages, disable stack traces | Detective/Preventive | Medium | Low |
| T04 | Use ORM with parameterized queries, least-privilege DB accounts | Preventive | Critical | Medium |

**Mitigation types:** Preventive (stop the attack), Detective (detect the attack), Corrective (recover from the attack)

## Output Format

Structure the complete threat model document as follows:

```markdown
# Threat Model: [System Name]

## Document Info
- Version: [1.0]
- Date: [date]
- Author: [name/team]
- Scope: [what is modeled]
- Status: [Draft / Review / Approved]

## 1. System Overview
[Brief description of the system, its purpose, and architecture]

## 2. Asset Inventory
[Table of assets with classification and owners]

## 3. Entry Points
[Table of entry points with auth requirements and trust levels]

## 4. Data Flow Diagram
[Text-based DFD with trust boundaries marked]

## 5. Trust Boundaries
[List of boundaries with controls and assumptions]

## 6. Threat Table
[Full STRIDE threat enumeration with IDs, components, descriptions]

## 7. Risk Matrix
[All threats plotted on likelihood x impact grid]

## 8. Mitigations
[Prioritized mitigation plan with effort estimates]

## 9. Residual Risk
[Threats that remain after proposed mitigations, with acceptance rationale]

## 10. Recommendations
[Prioritized action items, follow-up assessments, architecture changes]
```

## Integration with Other Skills

### Web Assessment --> Threat Model
- UnderstandApplication output feeds directly into threat model creation
- Threat model prioritizes what the Web Assessment skill tests

### Threat Model --> Recon
- Threat model identifies infrastructure components that need reconnaissance

### LLM Applications
- If the system includes LLM/AI components, add prompt injection threats
- Reference the Prompt Injection skill for specialized LLM threat enumeration
- Add STRIDE entries for: model manipulation (Tampering), training data poisoning (Tampering),
  prompt leakage (Info Disclosure), resource exhaustion via complex prompts (DoS)

## Available Tools

| Tool | Usage in Threat Modeling |
|---|---|
| WebSearch | Research CVEs, known attack patterns, threat intelligence for specific technologies |
| WebFetch | Fetch architecture documentation, OWASP references, vendor security advisories |
| claude-browser MCP | Review application UI flows, inspect configurations via internal tools |
| System commands | Verify configurations, check network topology if authorized |

## Company Context

When threat modeling your company's systems or features:
- Consider the multi-tenant SaaS architecture
- Pay attention to adapter/plugin trust boundaries for platforms that connect to external systems
- Model API key and credential storage as high-value assets
- Consider supply chain risks from third-party integrations
- Reference internal security documentation via claude-browser if available
- Check ticketing/wiki for existing security architecture decisions

## Examples

### Example 1: New Feature Threat Model
```
User: "Create a threat model for our new file upload feature"
--> Define scope: file upload endpoint, storage, processing pipeline
--> Assets: uploaded files, user data, processing service
--> Entry points: upload form, API endpoint
--> DFD: user --> upload API --> virus scan --> storage --> processing worker
--> STRIDE on each component
--> Risk score and mitigations
```

### Example 2: Architecture Review
```
User: "Threat model our microservices architecture"
--> Define scope: all services, APIs, data stores
--> Map service-to-service communication
--> Identify trust boundaries between services
--> STRIDE on inter-service calls, shared databases, message queues
--> Focus on lateral movement and privilege escalation
```

### Example 3: Quick Threat Assessment
```
User: "What are the main threats to this API?"
--> Focused STRIDE analysis on the API component
--> Top 5-10 threats with risk scores
--> Quick mitigation recommendations
--> Suggest full threat model if warranted
```

---

**Remember:** A threat model is a living document. Update it when the system changes, new threats
emerge, or after security incidents. The goal is not perfection but systematic identification of
risks before attackers find them.
