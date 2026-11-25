---
name: skill-agent-factory
description: Generate component-specific coder agents from project brain and approved component scopes.
category: workflow
---

# Skill: Agent Factory

Use after onboarding and user approval to create generated coder agents.

## Required inputs

```text
Project brain
Service catalog
Test policy
Approved service list
Agent coder template
```

## Generated coder contract

```text
service identity
allowed read paths
allowed write paths
forbidden paths
required escalation cases
test policy
critical checks
handoff obligations
```

## Rules

```text
Create narrow agents, not generic repo-wide coders.
Use service evidence from onboarding.
Keep agent registry in sync.
Ask before expanding write scope.
```

---

## Stack skill injection contract

When creating or updating a service coder agent, Agent Factory must attach skills in layers.

Layer 1: required workflow skills for every coder.

- `skill-project-brain`
- `skill-service-coder`
- `skill-dev-verification`
- `skill-memory-update`
- `skill-workflow-policy`

Layer 2: coordination skills when the service participates in a multi-service task.

- `skill-coder-leader`
- `skill-task-analysis`
- `skill-qc-handoff`
- `skill-bug-routing`

Layer 3: stack-specific skills from `.maestro/registry/skills.yaml`.

- Select stack skills from Project Brain, Component Knowledge, task evidence, and skills.yaml selection rules.
- Prefer the minimum useful set, not all installed skills.
- If stack evidence is weak, ask the user before attaching broad or risky third-party skills.
- Record the selected skills in the generated coder agent file and agent registry.
- Record skipped-but-relevant skills as optional recommendations, not active skills.
- Never attach skills marked `requires_user_approval: true` without Coordinator approval.
- Do not attach skills marked `installed: false`; list them as unavailable if task evidence would otherwise require them.

Coder generation is not complete until the generated agent states its service scope, allowed paths, forbidden paths, memory sources, verification policy, handoff contract, and selected skill list.

---

## Workspace service write path rule

**Deployment model:** component paths come from `.maestro/registry/components.yaml`; they may live under
apps, services, packages, infra, or tests and may be monorepo folders or independent repositories.

```text
1. Read component.path (e.g. services/service-a) from .maestro/knowledge/components/<component-id>.yaml.
2. Prefix all allowed_write_paths with component.path.
   Good: services/service-a/src, services/service-a/tests
   Bad:  src  (ambiguous — resolves inside maestro, not the service)
3. If component.path is empty or missing → stop, raise to Coordinator.
4. Record the resolved paths in agents.yaml alongside the coder entry.
5. Never default to unrecorded directories for services.
```

The path recorded in the component knowledge during onboarding is the single source of truth.

---

## Language and UI stack selection extension

When generating coder agents, Agent Factory must detect language and framework evidence before assigning these skills.

Java/Spring coder:

- Required when detected: <code>java-architect</code>
- Add for Spring Boot services: <code>spring-boot-engineer</code>, <code>spring-framework</code>, <code>java-spring-development</code>
- Do not assign Java/Spring skills to Kotlin-only or generic JVM services without evidence.

Go coder:

- Required when detected: <code>golang-pro</code>, <code>go-style-core</code>
- Add focused skills by task: <code>go-context</code>, <code>go-concurrency</code>, <code>go-error-handling</code>, <code>go-testing</code>, <code>go-performance</code>, <code>go-linting</code>
- Do not attach all Go micro-skills unless the coder is explicitly a broad Go maintainer agent.

Rust coder:

- Required when detected: <code>rust</code>, <code>rust-knowledge-patch</code>
- Add focused skills by crate/framework: <code>tokio-knowledge-patch</code>, <code>axum-knowledge-patch</code>, <code>serde-knowledge-patch</code>, <code>sqlx-knowledge-patch</code>, <code>tauri-knowledge-patch</code>
- If Rust appears only as a build dependency, do not create a Rust coder agent.

UI framework coder:

- Tailwind service: <code>tailwindcss</code>, optionally <code>tailwind-design-system</code>
- MUI service: <code>mui</code>
- MUI plus Tailwind service: include both and force the coder to document CSS layer/order constraints before coding.

---

## Batch 3 full-stack selection extension

Agent Factory must select Batch 3 skills by service evidence, not by broad availability.

Selection rules:

- .NET/C# services get C#/.NET skills only when <code>.sln</code>, <code>.csproj</code>, <code>Program.cs</code>, ASP.NET Core, EF Core, or Blazor evidence exists.
- PHP/Laravel services get PHP/Laravel skills only when <code>composer.json</code>, Laravel framework packages, Artisan, Eloquent, migrations, or Blade evidence exists.
- Ruby/Rails services get Ruby/Rails skills only when <code>Gemfile</code>, Rails, ActiveRecord, RSpec, or Rails folder conventions exist.
- Python backend services get FastAPI or Django skills only when package/dependency evidence identifies the framework.
- Angular, Svelte, SvelteKit, and Astro services get their matching framework skill only when framework config or dependency evidence exists.
- Mobile/native services get Flutter, Android/Kotlin, or Swift skills only when native project files prove the stack.
- ORM/database skills are added by dependency evidence and task scope; do not add every database skill to every backend coder.
- Skills with visible risk notes in <code>.maestro/engine/docs/external-skills.md</code> require explicit mention in the generated coder agent before use.

Generated coder agents must list selected Batch 3 skills under <code>Selected skills</code> with a one-line reason for each.

---

## Medusa stack selection extension

When Project Brain or Component Knowledge detects MedusaJS, Agent Factory must generate focused coder agents based on the Medusa layer being changed.

Medusa backend coder:

- Required: <code>building-with-medusa</code>
- Add: <code>typescript-advanced-types</code>, <code>nodejs-backend-patterns</code>
- Add database/ORM skills only when detected.

Medusa Admin coder:

- Required: <code>building-admin-dashboard-customizations</code>
- Add React, Tailwind, MUI, Shadcn, or design-system skills only when detected.

Medusa storefront coder:

- Required: <code>building-storefronts</code>, <code>storefront-best-practices</code>
- Add frontend framework skills based on the actual storefront stack.

Do not attach <code>learning-medusa</code> to production coder agents unless the user asks for tutorial/training mode. Do not attach <code>medusajs-developer</code> unless the official Medusa skills are insufficient and the user approves, because the registry marks it high risk.

---

## Messaging, cache, and container stack selection extension

Agent Factory must attach broker/cache/infra skills only when evidence exists in Project Brain or Component Knowledge.

Kafka coder:

- Required when detected: <code>kafka-development</code>
- Add language/framework skills for the producer or consumer implementation.
- Add schema/contract notes to the coder scope when Schema Registry, Avro, Protobuf, or JSON schema appears.

RabbitMQ/message queue coder:

- Required when detected: <code>loom-event-driven</code>
- Add <code>celery-expert</code> only after review because registry marks it critical risk.
- For Django Celery, prefer <code>django-celery-expert</code>.

Redis/cache coder:

- Required when detected: <code>redis-development</code>
- Add <code>redis-js</code> when Upstash or JavaScript Redis SDK is detected.
- Add <code>upstash-redis-kv</code> only after review because registry marks it Snyk High Risk.
- Treat Redis usage as cache, session store, queue, pub/sub, stream, lock, or rate limiter depending on evidence.

Docker/container coder:

- Required when detected: <code>docker</code>, <code>docker-knowledge-patch</code>
- Add <code>kubernetes-knowledge-patch</code>, <code>terraform-knowledge-patch</code>, <code>nginx-knowledge-patch</code>, or <code>traefik-knowledge-patch</code> only when those files/configs are in scope.

For cross-service messaging tasks, Coder Leader must coordinate producer and consumer coders separately and require a shared event contract in the task plan and QC handoff.

## ReactJS and Oracle selection extension

When generating a service coder, do not attach only one skill. Build a skill set from project evidence and task scope.

ReactJS mapping:

- Attach react for any ReactJS application, component, hook, or frontend service using React.
- Attach react-query when server-state, query caching, mutations, invalidation, loading/error states, or async API calls are in scope.
- Attach redux-toolkit when Redux store, slices, middleware, thunks, RTK Query, or centralized global state is detected.
- Attach zustand-state-management when Zustand stores or lightweight global state are detected.
- Attach react-modernization when the work is migration/refactor of older React patterns, class components, outdated lifecycle methods, or legacy state management.
- Combine with next-best-practices, tailwindcss, shadcn, mui, accessibility-a11y, framer-motion, gsap, vite, or typescript-advanced-types based on repository evidence.

Oracle mapping:

- Attach oracle-database for Oracle SQL, PL/SQL, packages, procedures, functions, triggers, migrations, indexes, sequences, locks, or Oracle driver behavior.
- Attach query-expert with oracle-database whenever SQL correctness or query behavior is part of the task.
- Attach database-architect with oracle-database for schema design, migration, modeling, or ownership boundaries.
- Attach database-optimizer with oracle-database for query tuning, index design, partitioning, execution-plan, or performance work.
- Attach discover-database during onboarding and when the service database engine is unclear.
- Attach oracle-cloud only when OCI infrastructure, Oracle managed services, networking, cloud deployment, or cloud operations are in scope.

Factory output requirement:

Each generated coder agent must include a skills section with:

- required_skills: skills always loaded for this coder scope.
- conditional_skills: skills loaded only when the specific task evidence matches.
- excluded_skills: skills intentionally not attached, with reason.

## Payment, Notification, AWS, and Azure selection extension

Payment mapping:

- Attach payment-platform for every payment, billing, subscription, refund, dispute, invoice, checkout, PCI, provider webhook, or marketplace payout task.
- Attach stripe-best-practices and stripe-integration for Stripe implementation tasks.
- Attach upgrade-stripe for Stripe API or SDK upgrade tasks.
- Attach paypal-integration for PayPal implementation tasks.
- Attach payment-integration for generic gateway, multi-provider, or unknown-provider payment tasks.
- Attach customer-billing-ops or finance-billing-ops for billing operation workflows.
- Attach notification-delivery when payment events send notifications.

Notification mapping:

- Attach notification-delivery for every email, SMS, push, in-app, webhook alert, message center, notification queue, template, preference, suppression, retry, or delivery-status task.
- Attach resend for Resend email tasks.
- Attach email-ops for operational email workflows.
- Attach messages-ops for message-center or messaging workflows, with risk review.
- Attach unified-notifications-ops for cross-channel notification orchestration.
- Attach capacitor-push-notifications for mobile push notification work.
- Attach payment-platform when notification is tied to payment, billing, invoice, refund, dispute, or subscription state.

AWS mapping:

- Attach cloud-platform-routing for every AWS task.
- Attach lambda for Lambda/serverless compute.
- Attach sqs for queueing.
- Attach eventbridge for event bus, schedule, or event routing.
- Attach iam for permissions, roles, policies, and least privilege.
- Attach cognito for AWS user authentication.
- Attach s3 for object storage.
- Attach dynamodb for DynamoDB.
- Attach cloudwatch for monitoring, logs, alerts, dashboards, and troubleshooting.
- Attach cloudformation for CloudFormation IaC.
- Use aws-cloud-services only when safer service-level skills do not cover the task because it was installed with Critical/High risk.

Azure mapping:

- Attach cloud-platform-routing for every Azure task.
- Attach azure-functions for Azure Functions/serverless.
- Attach cloud-solution-architect and microsoft-docs for Azure architecture or platform design.
- Attach kql for Kusto, Log Analytics, Application Insights, or Azure Monitor query work.
- Attach azure-cost and cost-optimization for Azure cost work.
- Attach azure-kubernetes for AKS.
- Attach azure-enterprise-infra-planner, azure-quotas, azure-upgrade, or microsoft-foundry when project evidence matches.
- Do not attach azure-ai, azure-observability, azure-compute, azure-messaging, azure-cloud-migrate, or azure-hosted-copilot-sdk unless future installation succeeds.
