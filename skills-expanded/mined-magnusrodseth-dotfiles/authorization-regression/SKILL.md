---
name: authorization-regression
description: "Reviews and tests authorization across protected operations and derived data. Use when changing access rules, AI retrieval or output, background jobs, or reviewing those boundaries adversarially."
---

# Authorization regression

Read the selected repository's instructions and authorization context. Use its
domain terms, policy owners, fixtures and testing commands. Resolve missing
policy from code and documented decisions; record conflicting or absent policy
as a gap. A skill describes verification; the application enforces access.

## Map the protected operation

1. Pin the reviewed revision, changed behavior and task mode: review, test design,
   or authorized implementation. Keep existing unrelated weaknesses separate.
2. Trace verified identity and trusted scope to each affected protected read,
   write or external effect. Include alternate callers and internal/service paths.
   Establish who may select the user, customer/tenant, resource and recipient.
3. Write an access matrix for the affected operations. Each row names principal,
   resource, action, expected allow/deny, policy source and enforcement point.
   Distinguish user delegation from an explicitly scoped service authority.
   Map separate customers, tenants, zones or co-owners only where the product
   actually has those concepts. UI visibility and model instructions are not
   enforcement points.

Read [AI and derived data](references/ai-and-derived-data.md) when retrieval,
model input/output, embeddings or tool requests touch the protected information.
Read [background work](references/background-work.md) when execution can wait,
retry, outlive a session, or send to an external recipient.

## Challenge the matrix

4. Pair each relevant denial with an authorized positive control through the
   same entry point. Select cases from the actual policy and changed boundary:
   missing identity, another principal, another customer/tenant, insufficient
   rights, related-resource substitution, revocation and alternate entry points.
   Follow the documented error contract; a denial must also prevent disclosure
   and side effects. A blanket failure that denies everyone does not pass.
5. Trace the strongest existing defense before reporting a defect. Follow the
   real guard, ownership query, serialization and downstream call. Separate
   code evidence from assumptions about deployed configuration or exposure.
   Read-only access can still disclose protected data.
6. In review mode, inspect the real implementation and available tests. Report
   concrete unauthorized paths separately from missing verification. In test
   or implementation mode, exercise the real enforcing boundary with approved
   synthetic fixtures. Mock the model, clock or external delivery as needed;
   keep the claimed authorization control real. Never probe live customers,
   send real notifications, or execute untrusted PR code with review credentials.
   Use the repository's existing test and evidence workflows.
7. Assert both the response and relevant effects: protected data did not reach an
   unauthorized model context, recipient, stored artifact or external call.
   For authorized paths, assert the expected data/effect occurred. Inspect
   relevant logs and traces using synthetic markers, without copying secrets.
   Use a known failing regression or a bounded guard mutation in an isolated
   test copy when needed to establish that a critical test detects its defect.
   Preserve the production guard and committed verification requirements.

## Report the evidence

Record revision and mode, matrix rows and policy sources, enforcing code paths,
commands and observed results. Mark each row **verified allow**, **verified deny**,
**failed**, **gap**, or **not applicable** with its reason. State whether evidence
comes from code inspection or execution and name substituted boundaries.

A finding needs an actor, reachable input-to-effect path, failed control,
consequence and proportionate remedy. Keep the caller's review axes and severity
format. An unrun test or an uncertain policy is a gap, not a confirmed exploit.
Finish when every affected matrix row has evidence or an explicit gap. Passing
cases establish the tested boundaries, not a system-wide security guarantee.
