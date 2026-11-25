---
name: platform-self-service-api-and-workflow-design
description: >
  Designs the self-service provisioning layer of an internal developer
  platform — Backstage Scaffolder custom actions, Humanitec's API, or a
  bespoke internal API — with policy checks, budget limits, and approval
  steps wired directly into the provisioning flow so "self-service" doesn't
  mean "no oversight." Use when a user asks to "design a self-service API
  for infrastructure requests," "add a Backstage Scaffolder action that
  provisions a database," "add an approval gate to a self-service workflow,"
  "stop developers from provisioning oversized/production resources without
  review," or "wire policy/budget checks into a platform API."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: internal-developer-platform
  maturity: stable
---

# Platform Self-Service API and Workflow Design

## Purpose

Self-service is the core value proposition of an internal developer
platform — a developer requests a database, environment, or new service
without filing a ticket and waiting on a human — but "self-service" and
"no oversight" are not the same thing, and conflating them is how a
platform team ends up with an unreviewable production Kafka cluster
provisioned at 2 a.m. by a script nobody remembers writing. The
provisioning **API/workflow layer** — whether it's a Backstage Scaffolder
custom action, calls against Humanitec's API, or a bespoke internal REST/
gRPC API — is where guardrails either get built in from day one or get
bolted on later as an incident retrospective action item. This skill
covers designing that layer so policy checks, budget/cost limits, and
approval steps are structural parts of the request's execution path, not
optional UI decoration a determined developer (or a bug) can route around.

## When to use

- Designing a new self-service action or API endpoint that provisions
  real infrastructure (a database, a cloud environment, a Kafka topic, an
  IAM role) rather than just generating boilerplate code.
- Writing a Backstage Scaffolder custom action (`createTemplateAction`)
  that calls out to a cloud provider, Terraform, or an internal
  provisioning system.
- Deciding how a Humanitec Application/Environment self-service request
  should be gated before it can bind a Resource Definition in a
  production Environment.
- A security or FinOps stakeholder asks "how do we know self-service
  requests aren't bypassing review" or "how do we cap the cost blast
  radius of a self-service action."
- An incident retrospective finds an oversized/insecure resource was
  provisioned through the self-service tool with no record of who
  approved it, and the platform needs a structural fix, not a policy memo.
- Adding a manual-approval or budget-limit step to an existing self-service
  flow that currently executes unconditionally on submission.

## Prerequisites & environment

- For Backstage: a working Scaffolder installation (`@backstage/plugin-
  scaffolder-backend`), permission to register a custom
  `createTemplateAction`, and a place for the action's backend code to run
  with credentials to call the target provisioning system (cloud API,
  Terraform Cloud/Enterprise API, internal service).
- For Humanitec: an org with the Platform Orchestrator, `humctl`
  authenticated, and an API token (`HUMANITEC_TOKEN`) scoped to the
  Applications/Environments the self-service flow targets — see
  [humanitec-score-workload-specification](../humanitec-score-workload-specification/SKILL.md)
  for the workload-spec side of this.
- A policy engine or rule evaluator reachable synchronously from the
  provisioning path — Open Policy Agent (OPA) with a `/v1/data` HTTP
  endpoint is the common choice; a hand-rolled rule function works for a
  small, stable rule set but doesn't scale past a handful of checks.
- A durable place to record request state (requested → policy-checked →
  pending-approval → approved/rejected → provisioning → completed/failed)
  — a database table or a workflow engine (Temporal, AWS Step Functions,
  or even a simple state column in Postgres) — not just logs, since an
  auditor needs to query "who approved what, when" after the fact.
- An approval channel that's actually staffed — a Slack/Teams
  approval-bot integration, a ServiceNow/Jira approval ticket, or (for
  low-stakes cases) a second engineer's API call — wired to notify the
  right team, not a queue nobody watches.
- A cost-estimation source (cloud pricing API, a static lookup table
  keyed by instance size/type, or a FinOps tool's API) if budget limits
  are part of the guardrail set.

## Step-by-step guidance

1. **Model the request as a state machine, not a single synchronous
   call.** A request that provisions real infrastructure has distinct
   states, and each guardrail attaches to a specific transition —
   collapsing all of this into "call the action, infrastructure appears"
   is what makes bypassing a check trivial:
   ```
   requested → policy_checked → pending_approval → approved → provisioning → completed
                    │                                 │
                    └─ rejected (policy)               └─ rejected (approver) / failed (provisioning)
   ```
   Persist this state explicitly (a `self_service_requests` table with a
   `status` column and a timestamped history), so "was this approved, and
   by whom" is answerable by a query, not by reconstructing intent from
   Slack scrollback.

2. **Write the policy check as a required, server-side gate — never a
   client-side/UI-only validation.** A Backstage Scaffolder custom action
   that calls a policy engine before provisioning:
   ```typescript
   // packages/backend/src/plugins/scaffolder/actions/provisionDatabase.ts
   import { createTemplateAction } from '@backstage/plugin-scaffolder-node';
   import fetch from 'node-fetch';

   export const createProvisionDatabaseAction = () =>
     createTemplateAction<{
       serviceName: string;
       environment: 'dev' | 'staging' | 'production';
       instanceClass: string;
     }>({
       id: 'custom:cloud:provisionDatabase',
       schema: {
         input: {
           required: ['serviceName', 'environment', 'instanceClass'],
           type: 'object',
           properties: {
             serviceName: { type: 'string' },
             environment: { type: 'string', enum: ['dev', 'staging', 'production'] },
             instanceClass: { type: 'string' },
           },
         },
       },
       async handler(ctx) {
         const { serviceName, environment, instanceClass } = ctx.input;

         // 1. Policy check — happens inside the action, not in the UI form.
         const policyResp = await fetch('https://opa.internal.example.com/v1/data/platform/db_provisioning', {
           method: 'POST',
           headers: { 'Content-Type': 'application/json' },
           body: JSON.stringify({ input: { environment, instanceClass, requester: ctx.user?.entity } }),
         });
         const { result } = await policyResp.json();
         if (!result.allow) {
           throw new Error(`Policy denied request: ${result.reasons.join(', ')}`);
         }

         // 2. If policy requires approval, create a pending request and stop —
         //    do NOT provision yet. A separate, approver-triggered call resumes this.
         if (result.requires_approval) {
           const request = await createPendingRequest({
             serviceName, environment, instanceClass,
             requestedBy: ctx.user?.entity,
             policyReasons: result.reasons,
           });
           ctx.output('requestId', request.id);
           ctx.output('status', 'pending_approval');
           ctx.logger.info(`Request ${request.id} awaiting approval — notified #platform-approvals`);
           return; // action ends here; provisioning happens on approval, not now
         }

         // 3. Only auto-provisions if policy explicitly allowed with no approval needed
         //    (e.g. small dev-environment instance classes).
         const result2 = await provisionViaInternalApi({ serviceName, environment, instanceClass });
         ctx.output('resourceId', result2.id);
         ctx.output('status', 'completed');
       },
     });
   ```
   The key structural point: **the action itself cannot provision without
   either an `allow` from the policy engine or a completed, separately
   recorded approval** — there is no code path where submitting the
   template form alone results in a production resource appearing.

3. **Express the policy as data, not as code embedded in the action.** An
   OPA/Rego policy the action above calls, kept in its own repo/bundle so
   it can be updated without redeploying the Scaffolder backend:
   ```rego
   package platform.db_provisioning

   default allow = false
   default requires_approval = false

   # Small dev instances: auto-approved, no human in the loop.
   allow {
     input.environment == "dev"
     input.instance_class in {"db.t3.micro", "db.t3.small"}
   }

   # Any production request is policy-permitted to *proceed to approval*,
   # never auto-provisioned.
   requires_approval {
     input.environment == "production"
   }

   # Oversized instance classes always require approval, even in staging.
   requires_approval {
     input.environment == "staging"
     input.instance_class in {"db.r5.2xlarge", "db.r5.4xlarge"}
   }

   # Hard deny: instance classes above the org's approved ceiling, full stop —
   # no approval path overrides this; it's a guardrail, not a speed bump.
   allow = false {
     input.instance_class in {"db.r5.8xlarge", "db.r5.16xlarge"}
   }
   ```
   Keeping policy external means a budget or security team can tighten a
   rule (e.g. add a new denied instance class after a cost incident)
   through a reviewed PR to the policy bundle, without needing a platform
   engineer to touch or redeploy the Scaffolder action code.

4. **Wire the approval step to an actual notification channel, and make
   the approval call itself the only thing that resumes provisioning** —
   never a status flag a developer can flip on their own request:
   ```typescript
   // Separate, approver-only endpoint — requires an approver role, checked
   // server-side against the platform's RBAC, not just "logged in".
   app.post('/api/self-service/requests/:id/approve', requireRole('platform-approver'), async (req, res) => {
     const request = await getRequest(req.params.id);
     if (request.requestedBy === req.user.id) {
       return res.status(403).json({ error: 'Cannot approve your own request' });
     }
     await recordApproval(request.id, req.user.id);
     await enqueueProvisioning(request.id); // provisioning happens here, not before
     res.json({ status: 'approved', provisioningQueued: true });
   });
   ```
   The `requestedBy === approver` check blocks the most common structural
   bypass: a developer approving their own request because the UI
   technically allowed it.

5. **Attach a budget/cost guardrail as its own explicit check**, separate
   from the allow/deny policy, so cost limits can be tuned by FinOps
   without touching security policy:
   ```rego
   package platform.budget

   import future.keywords.in

   monthly_estimate_usd(instance_class) = cost {
     costs := {"db.t3.micro": 15, "db.t3.small": 30, "db.r5.2xlarge": 950, "db.r5.4xlarge": 1900}
     cost := costs[instance_class]
   }

   requires_approval {
     monthly_estimate_usd(input.instance_class) > 200
   }
   ```
   Combine this with the environment/security policy from step 3 (an
   `OR` across both policy sources triggering `requires_approval`) rather
   than one monolithic rule file mixing security and cost logic — the two
   evolve on different cadences and are usually owned by different teams.

6. **For Humanitec-based self-service, gate Environment creation and
   Resource Definition binding through the same pattern**, not through
   `humctl` calls made directly by developers with standing admin tokens:
   an internal API wraps `humctl score deploy`/environment-creation calls,
   checks policy first, and only production-tier Environments require
   approval — see
   [humanitec-score-configuration-validation](../humanitec-score-configuration-validation/SKILL.md)
   for the dry-run/policy checks that should run in this same gate before
   a real deploy proceeds.

7. **Make the guardrail-compliant path faster than the workaround**,
   deliberately. If a developer can get a database from a cloud console
   in 10 minutes but the self-service flow with its approval step takes 3
   days, the guardrail will get routed around — set an SLA for the
   approval step itself (e.g. auto-escalate an unactioned approval after
   4 business hours) and make routine, low-risk requests (dev-tier, small
   instance classes) genuinely instant per step 3, saving human review
   capacity for the requests that actually carry risk.

8. **Provide one explicit, audited break-glass path for genuine
   emergencies** — never let "this is urgent" become an informal reason
   to call the underlying cloud API directly instead. A break-glass
   request auto-approves but mandatorily creates a retroactive review
   ticket and pages the platform/security on-call, so urgency is
   accommodated without becoming an invisible bypass.

## Best practices

- Put every guardrail (policy check, budget check, approval requirement)
  on the **server side of the API/action**, never only in the Scaffolder
  form's client-side validation or a UI-only confirmation dialog — a
  direct API call must be subject to the identical checks as a UI
  submission.
- Externalize policy and budget rules (OPA/Rego, or at minimum a
  versioned config file) from the action/API's own code, so a rule
  change is a reviewed PR to a policy repo, not a platform-team code
  deploy.
- Persist request state transitions with who/when for every step
  (requested, policy-checked, approved-by, provisioned) — this is the
  audit trail a security review or incident retrospective will need, and
  retrofitting it after the fact from application logs is far more work
  than building it in from the state-machine design in step 1.
- Reject self-approval structurally (the approver-role check in step 4),
  not just as a documented policy nobody enforces in code.
- Separate "hard deny" guardrails (an instance class or region that's
  never allowed) from "requires approval" guardrails (allowed, but only
  with sign-off) — collapsing both into one binary allow/deny either
  blocks legitimate high-tier requests entirely or lets a genuinely
  dangerous request through disguised as "just needs approval."
- Version and test policy rules the same way as application code — a unit
  test asserting `production + db.r5.16xlarge → deny` should fail CI if
  someone accidentally loosens that rule.
- Make the fast, auto-approved path (small/dev-tier resources) genuinely
  fast, so the platform earns compliance with the slower, gated path for
  high-risk requests rather than forcing it against resistance.

## Common pitfalls

- **Symptom:** A Scaffolder template's form shows an "I understand this
  requires approval" checkbox, but the underlying custom action
  provisions the resource immediately regardless of whether the checkbox
  was checked or an approver ever looked at the request.
  **Fix:** This is approval theater, not a guardrail — restructure the
  action so it stops at `pending_approval` (step 2) and only a separate,
  role-checked approval call resumes provisioning; a UI element with no
  corresponding server-side gate provides no actual oversight.

- **Symptom:** Under a deadline, an engineer calls the cloud provider's
  API or console directly to provision a production resource "to be
  fast," bypassing the self-service tool and its approval step entirely,
  and there is no record of the request at all.
  **Fix:** This is exactly the risky shortcut this skill exists to
  prevent — treat it as a finding, not a one-off. Restrict direct
  provisioning API/IAM permissions on production-tier resources to the
  self-service system's own service role (mirroring the
  `codedeploy:CreateDeployment` restriction pattern used for CI/CD
  pipelines), so a production resource can only be created through the
  gated flow, and provide the audited break-glass path from step 8 for
  genuine emergencies instead of leaving direct API access open as an
  informal escape hatch.

- **Symptom:** A developer approves their own self-service request
  because the approval endpoint only checks "is this user an approver,"
  not "is this a different person than the requester."
  **Fix:** Add the `requestedBy !== approver` check shown in step 4 at
  the API level — this is a two-line check that closes the single most
  common self-approval bypass, and it must live in the approval endpoint
  itself, not as a social convention.

- **Symptom:** A policy or budget rule change (e.g. lowering the
  auto-approve cost threshold after a cost overrun) requires a platform
  engineer to edit and redeploy the Scaffolder backend or internal API,
  taking days, while the overspend continues in the meantime.
  **Fix:** Externalize policy to a bundle an OPA sidecar/service loads
  independently (step 3) so a FinOps or security reviewer can ship a
  policy change through its own lightweight PR/review process without
  a platform-team code deploy in the critical path.

- **Symptom:** Two near-simultaneous self-service requests for a
  same-named resource (e.g. a retried request after a timeout) both
  reach the provisioning step, creating duplicate infrastructure or a
  provider-side naming conflict that surfaces as a confusing partial
  failure.
  **Fix:** Require an idempotency key on the provisioning call (derived
  from the request ID, not regenerated per retry) so a retried or
  duplicated request resolves to the same underlying operation instead of
  creating a second resource.

## Worked example

**Scenario:** A platform team wants developers to self-service-provision
a managed Postgres database through a Backstage Scaffolder template,
without every request needing a platform engineer's manual involvement,
while still guaranteeing production databases and any instance above a
cost threshold get a human sign-off, and every provisioned database is
traceable to a specific approved request.

**Scaffolder template** (`templates/provision-database/template.yaml`,
abbreviated):
```yaml
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: provision-postgres-database
  title: Provision a Postgres Database
spec:
  parameters:
    - title: Database details
      required: [serviceName, environment, instanceClass]
      properties:
        serviceName:
          type: string
          description: Owning service (must exist in the catalog)
        environment:
          type: string
          enum: [dev, staging, production]
        instanceClass:
          type: string
          enum: [db.t3.micro, db.t3.small, db.r5.2xlarge, db.r5.4xlarge]
  steps:
    - id: provision
      name: Provision database
      action: custom:cloud:provisionDatabase
      input:
        serviceName: ${{ parameters.serviceName }}
        environment: ${{ parameters.environment }}
        instanceClass: ${{ parameters.instanceClass }}
  output:
    text:
      - title: Request status
        content: ${{ steps.provision.output.status }}
```

**Flow for a `production` / `db.r5.2xlarge` request:**
1. Developer submits the template. The `custom:cloud:provisionDatabase`
   action (step 2 above) calls the OPA policy from step 3: `environment
   == production` sets `requires_approval = true`; the budget policy from
   step 5 independently also flags it (`$950/mo estimate > $200`).
2. The action creates a `pending_approval` request row and posts to
   `#platform-approvals` via a Slack webhook: *"checkout-api requests a
   db.r5.2xlarge Postgres instance in production ($950/mo est.) —
   requested by @jane. Approve: `<link>`"*.
3. A platform engineer (not Jane) reviews and calls `POST
   /api/self-service/requests/req_8f2a/approve`. The `requestedBy !==
   approver` check passes since the approver is a different user.
4. Approval triggers `enqueueProvisioning`, which calls the internal
   provisioning API, tags the resulting RDS instance with
   `request_id=req_8f2a` and `approved_by=<approver>`, and updates the
   request row to `completed`.
5. Six weeks later, a cost audit queries the `self_service_requests`
   table and finds every production database traceable to a specific
   approved request — no orphaned resources with no request record,
   because the provisioning call in step 4 only ever fires from inside
   the gated flow, never from a developer's own cloud credentials.

For a `dev` / `db.t3.micro` request submitted the same way, the OPA
policy's first `allow` rule matches with no `requires_approval`, so the
action provisions immediately — the developer gets their dev database in
seconds, with zero platform-engineer involvement, because the guardrail
correctly reserved human review for the request that actually carried
risk.

## Cross-references

- [no-code-idp-service-catalog-tools-port-cortex-opslevel](../no-code-idp-service-catalog-tools-port-cortex-opslevel/SKILL.md) — Port's self-service Action model and its `reportWorkflowStatus` pattern are a SaaS-hosted equivalent of the Backstage/custom-API workflow designed here.
- [humanitec-score-workload-specification](../humanitec-score-workload-specification/SKILL.md) — the workload-spec side of a self-service request when the provisioning target is a Humanitec Application/Environment rather than a standalone resource.
- [humanitec-score-configuration-validation](../humanitec-score-configuration-validation/SKILL.md) — the dry-run/policy validation this skill's policy-check step should call before a Humanitec-backed self-service request proceeds to approval.
- [golden-path-template-design-for-developer-platforms](../golden-path-template-design-for-developer-platforms/SKILL.md) — the Scaffolder template surrounding the self-service action here is itself a golden path; that skill covers the template's broader defaults and escape hatches beyond the provisioning action alone.
- [backstage-plugin-development](../backstage-plugin-development/SKILL.md) — general Backstage backend-plugin patterns (`createBackendPlugin`, API clients) that a custom Scaffolder action's supporting backend code often reuses.
