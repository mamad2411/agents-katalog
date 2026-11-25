---
name: aws-connect
description: "Use when writing or reviewing Terraform for Amazon Connect: contact flows and flow modules, a Lambda function invoked from a flow, queues, routing profiles, security profiles and access-control tags, users, approved origins, adopting console-built resources, PHI in flow logs and contact attributes, or contact events to EventBridge and SQS. Not for general Lambda tuning (aws-serverless) or IAM and pipelines (terraform-aws)."
---

# Amazon Connect in Terraform

Connect fails quietly. A flow that references an unassociated Lambda fails to save with no reason given. A security profile tag that matches nothing hides every queue. A value returned from a Lambda is kept for 24 months. Each rule below is here because it fails without an error.

## Decide the owner of each resource first

Before you write or review anything, list each Connect resource and who edits it: Terraform or the console. Most Connect instances already have console-built flows, queues and hours, and people keep editing flows in the console after Terraform arrives.

| Owner | Do this |
| --- | --- |
| Terraform | Manage it. A console edit is drift, and the next apply reverts it. Say so in the repository's agent instructions. |
| Console | If Terraform created or adopted it, take it out of state with a `removed` block and `lifecycle { destroy = false }`, which does not delete it. Then read it with a data source (`aws_connect_queue`, `aws_connect_security_profile`, `aws_connect_contact_flow`). |
| Moving from the console to Terraform | For the transition only, set `lifecycle { ignore_changes = [content] }` on the flow while the console edits are ported into code. Before you remove it, export the live content and port it back, or the apply reverts the console edits. `ignore_changes` keeps the flow in state, so a `type` change or a destroy still replaces or deletes it. |
| Built in the console, Terraform from now on | Adopt it: an `import {}` block, plus `lifecycle { prevent_destroy = true }` when flows, numbers or campaigns depend on it. |

The step is complete when every resource in the root has one owner. If the answer is "both", which forces a `-target` on every apply, report it as a finding. Standing `-target` applies are partial applies that nobody reviews as a whole. The fix is one owner for each resource: move the console edits into code, or hand the resource to the console with `removed` and a data source (`terraform-aws` → `references/terraform-structure.md` → "One owner per resource").

## Rules that fail without an error

### A Lambda function in a flow

- **Create both grants.** `aws_lambda_permission` (principal `connect.amazonaws.com`, `source_arn` the instance ARN) lets Connect invoke the function. `aws_connect_lambda_function_association` puts it on the instance's list. Without the association, the flow or module save fails with `InvalidContactFlowException` and no detail. Add `depends_on` on the association to the flow resource.
- **Fit inside the timeout.** A synchronous invocation has a maximum timeout of 8 seconds, and Connect retries errors within that window. Set the function timeout below 8 seconds, and put every downstream timeout (database connect, statement, HTTP) inside it.
- **Return a status, never data.** Returned values become contact attributes. Attributes go to the contact record, which Connect keeps for 24 months, and to flow logs and Contact Lens. Return codes such as `verified=true` and `reason=FAILED`. Let the agent application fetch details from its own backend by contact ID.
- **Never throw.** Every caught failure returns a status, such as `reason=ERROR`, that the flow can route on. The flow's Error branch then means only a timeout or an INIT failure.

Details, limits and sources are in [`references/lambda-in-flows.md`](references/lambda-in-flows.md).

### PHI and caller input

- Flow logs record what a flow sends to a Lambda function, and the logging setting carries into every flow that the contact is transferred to. Around input collection (a date of birth, an account number), set logging to Disabled before the input block and to Enabled after the Lambda returns, on every path.
- Turn recording on after the input steps, not before them. DTMF is captured as audio.
- Create the flow log group in Terraform with a retention period. A log group that Connect creates never expires.

### Security profiles and access-control tags

- Tags on one profile combine with AND. Profiles on one user combine with OR. To give a supervisor two departments, assign two profiles with one tag each, not one profile with two tags.
- When a tagged and an untagged profile on one user grant the same permission, Connect enforces the untagged one. So check the base agent profile for overlap.
- A resource type that is tag-restricted with no resource carrying the tag shows the user nothing. Tag the queues (adopt them if needed) before you restrict `Queue`.
- `aws_connect_security_profile` cannot set access-control tags. See the provider gaps below.

Details, limits and sources are in [`references/access-control.md`](references/access-control.md).

## Provider gaps

These were checked against the provider docs, verified 2026-11-15.

| Need | `hashicorp/aws` | Alternative |
| --- | --- | --- |
| Access-control tags on a security profile | None (`aws_connect_security_profile` has `permissions` and `tags` only) | `awscc_connect_security_profile` (`allowed_access_control_tags`, `tag_restricted_resources`). Needs Cloud Control API permissions |
| Approved origins (for an embedded CCP) | None | `awscc_connect_approved_origin` |
| Phone number to flow | `aws_connect_phone_number_contact_flow_association` | |
| Instance-level Lambda list | `aws_connect_lambda_function_association` | |

If you fall back to `terraform_data` with a `local-exec` AWS CLI call, Terraform cannot read the result back. A console edit then stays in place until a `triggers_replace` input changes. For access-control tags, that means a widened supervisor scope stays unnoticed. Record the gap, and add a scheduled check that compares `describe-security-profile` against the code.

## Flows as code

A console export is not Connect flow language, so the resource cannot use it. Export with `aws connect describe-contact-flow` and take `.ContactFlow.Content`. To author flows in HCL, and to validate them at plan time, read [`references/flows-as-code.md`](references/flows-as-code.md).

## Contact events and Contact Lens files

Contact events arrive on the default EventBridge bus with source `aws.connect`, on a best-effort basis and in no particular order. Consumers order them by timestamp and stay idempotent. EventBridge drops a permission error without retrying it, and an SQS DLQ does not catch those events. The rule pattern, the target DLQ and the S3 notifications for Contact Lens files are in [`references/access-control.md`](references/access-control.md#contact-events-to-sqs).

## Review checklist

When you review a Connect Terraform root, report each item as PASS, FAIL or NOT APPLICABLE:

1. Every resource has one owner, and applies do not need `-target`.
2. Each flow-invoked function has a permission with `source_arn`, an instance association, and `depends_on` from the flow.
3. Each function timeout is below 8 seconds, and its downstream timeouts fit inside it.
4. No function returns or logs caller data. Flow logging is off around input collection.
5. Log groups (function and flow logs) are in Terraform with retention.
6. Alarms exist and notify someone: function errors and throttles, the status the function returns for failures, DLQ depth, and EventBridge `FailedInvocations`.
7. Tag-restricted security profiles have one tag each, and their scope is read back or checked.
8. A function that opens database connections has reserved concurrency sized against the database's `max_connections`.
9. The provider has `allowed_account_ids`, and the state key and variable file differ per environment.
