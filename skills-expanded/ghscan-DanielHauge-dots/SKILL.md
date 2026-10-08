---
name: jira-writing
description: Draft, create, refine, or estimate Jira tasks and user stories, plus bugs, spikes, and epics, using Atlassian MCP when Jira access is needed. Use for issue writing, not implementing issues or answering general status queries.
---

# Jira writing

Write the smallest independently releasable useful outcome, not a full
implementation spec. Use precise plain English by default; match the user's
language and use active voice without corporate jargon or fluff.
An independent future reader must understand the ticket without this chat.

## Decide what to write

- Identify the intended outcome, why it matters, and observable success conditions.
  Ask one concise question if the outcome or success conditions are missing.
- Keep unknowns visible as questions, not facts, commitments, or promises.
  Implementation unknowns can wait for planning unless they change the outcome.
- Separate independently useful outcomes rather than bundling unrelated work.
- Distinguish verified constraints from possible implementation ideas. Omit ideas
  that add no necessary context; label any retained ideas as nonbinding.
- Do not dictate files, APIs, libraries, or technical design unless the user asks
  for them or a verified contract constrains them.
- Planning, design, grilling, and implementation are separate later phases.
  Do not invoke them automatically while writing an issue.

## Choose an issue type

Use the project's actual types, not an assumed universal type list.

| Type | Use and required detail |
| --- | --- |
| Story | A user-visible, independently releasable feature slice. It must deliver actual value to an identified user when complete, not merely enable future work. Use the story format below and final-value DoD. |
| Task | A technical, operational, or partial implementation deliverable. A Task may make no user-visible change on its own; use technical DoD. A standard Task is normally a peer of a Story, not its child. Use a configured Subtask type when the work must be a native child of a Story. |
| Bug | Observed behavior, expected behavior, and reproduction steps or conditions. Mark missing details explicitly unknown; include a regression check in DoD. |
| Spike | A bounded question and research scope, with a user-provided or agreed timebox. Ask if the timebox is missing. Require findings with evidence, a recommendation even if inconclusive, and proposed follow-ups. No implicit implementation. |
| Epic | A broad milestone, release, or product module composed of Stories, with clear overall completion. Not a vague giant task; do not fabricate child keys or create children without authorization. |

If a requested type is unsupported (including Spike), resolve the choice with the
user. Never silently substitute Task or another type.

## Story hierarchy

- Do not infer a hierarchy from issue names. Confirm the project's available
  work types and its create/edit schema before assigning a parent. Jira's usual
  default is **Epic → standard work item (Story, Task, or Bug) → Subtask**;
  Story and Task are normally peers, and a Subtask cannot have children.
- An Epic groups standard work items. A Story is a complete user-facing feature
  slice. Use a configured Subtask only for work that must be a native child of
  that Story; use a standard Task as a peer when it is not a child in the
  project's supported hierarchy.
- Keep a Story intact until the user can use the feature end to end. API,
  frontend shell, database, infrastructure, and similar partial work belong in
  a configured Subtask or separate standard Task, not separate Stories, unless
  they are independently useful to users.
- A Story can potentially be released when its DoD is met. Do not close it
  because only its implementation Tasks are technically complete.
- When drafting a Story with known implementation work, name the expected
  Subtasks or related standard Tasks at a high level. Create them or establish
  their actual supported hierarchy only when authorized, and never invent issue
  keys.

## Jira hierarchy, dependencies, and links

- A native hierarchy is not a generic issue link. Set the child's `parent` on
  create or update only when the project schema permits the requested parent
  and work type. Use `parent` for an Epic's direct standard work items and for
  a Subtask's direct parent; never use a generic link as a substitute for Epic
  membership or a parent/child relationship. Do not assume legacy `Epic Link`.
- A work item has one native parent. Do not assign parents across company-managed
  and team-managed projects, or assume custom hierarchy levels exist. If the
  target type or parent relationship is unsupported, explain that limitation
  rather than silently creating a related link.
- A request to link issues, including newly created dependent work, requires an
  actual native Jira relation after every referenced issue exists. A description
  bullet, comment, remote link, or invented `additional_fields` entry is not a
  Jira work-item relation.
- Link only when the user explicitly requests it or otherwise authorizes it.
  Use the requested relation only; never invent issue keys, direction, or
  relation semantics. A generic link is for a dependency, duplication, review,
  or other association; it does not make either work item a child.
- For an exact Jira/UI link type, discover or use an exposed Jira operation that
  lists the site's configured link types and creates that type of issue link.
  Use only its returned type and source/target direction inputs. Link types and
  their inward/outward labels are site-configurable; do not hard-code them or
  silently downgrade an exact type to a generic relation. If MCP cannot express
  the requested link type, disclose that and ask before using a generic link.
- For a blocking link, express the direction explicitly: **A blocks B** means
  source/outward issue A and target/inward issue B. Jira should show “blocks B”
  on A and “is blocked by A” on B. Confirm the site's configured labels before
  writing.
- Create all requisite issues before assigning a relation. Verify a hierarchy
  by reading the child's returned `parent`; verify an issue link by reading its
  link data (or the exact relation returned by the exposed tool). Report both
  keys and the verified relation. Do not claim a generic link verified hierarchy
  or Epic membership.

## Core template

Use Markdown headings and checklists by default. Respect an existing team template,
but always include an explicit Definition of Done. Keep success checks in one place;
do not duplicate acceptance criteria and DoD. Incorporate existing criteria into DoD
or reference them precisely if the team requires a separate section.

## Estimation

Estimate every implementation Story and Task in **points that approximate working
days** when the user asks for estimates or the project requires them. Use the
project's estimate field after confirming its name and allowed values; otherwise put
the estimate in the draft. Do not add an estimate to Jira unless authorized.

- One point is roughly one person-day of end-to-end delivery effort, not one day of
  typing code. Use the coarse scale **2, 3, 5, 8, 13** points; do not use 1 point
  for implementation work. Split or re-scope work estimated above 13 points.
- Estimate the whole medium-agentic-engineering lifecycle: intake and context
  gathering, specification grilling and validation, initial implementation, scoped
  agent execution and integration, behavior verification, automated/manual testing
  and QA, review feedback, and release/rollout work when it is in scope.
- Medium agentic engineering speeds bounded exploration, coding, and test execution;
  it does not remove specification, integration, verification, review, or release
  effort. Apply that saving conservatively—do not estimate as if every phase is
  autonomous or parallelizable.
- Include credible uncertainty and dependencies. Unknown requirements, external
  systems, cross-team handoffs, migrations, security-sensitive changes, and release
  coordination increase the estimate or require a Spike first. Do not hide them in
  an optimistic point value.
- Do not derive false precision from hours or provide separate per-phase subtotals
  unless requested. Points express rough delivery days, not a commitment or deadline.

Use this concise draft notation when an estimate is requested:

```markdown
## Estimate
**5 points** (roughly five working days of medium-agentic delivery).
Includes specification validation, implementation, agent-assisted execution,
verification/testing, review, and release work in scope.
```

### Story template

Every Story uses this format unless the team has an equivalent required format:

```markdown
Title: <user-facing feature>

## User story
As a <specific user or role>,
I want to <user-facing capability>,
so that I can <user value or outcome>.

## Scope
<Only the boundaries needed to prevent confusion.>

## Definition of Done
- [ ] <A user can complete the feature through the real product experience.>
- [ ] <The user-observable result or value is correct.>
- [ ] <Relevant user-facing boundary or failure behavior is correct.>

## Implementation tasks
- <Known native Subtask or related standard Task; omit this section when none are known.>
```

Story DoD describes the final, testable feature value—not technical milestones.
For example, “A user can generate a report by clicking **Generate report** and
receive the report” is Story DoD; “The report API is available with Swagger
documentation” and “The frontend is served at `/`” are Task DoD checks.

### Task template

```markdown
Title: <clear action or outcome, specific enough to distinguish this issue>

## Outcome
<What changes and why it matters. Usually one or two sentences.>

## Scope
<Only when needed to establish boundaries. Exclude only likely points of confusion.>

## Definition of Done
- [ ] <Observable technical or operational condition and its evidence.>
- [ ] <Another condition that completes this implementation deliverable.>
- [ ] <Relevant boundary or failure case, if applicable.>
```

Typically use 3–6 DoD checks; use fewer when they fully define a small outcome.
Each check must be testable with a clear yes/no result. Choose evidence relevant
to the work: observed behavior, a verified deliverable, or a recorded finding.
Do not pad the checklist with generic review, testing, security, or documentation
rituals. Add those obligations only when supplied, required, or part of the outcome.
Never fabricate performance targets, deadlines, or other numerical commitments.

Add Context/links, Constraints/dependencies, or Open questions only when material.
Include Bug reproduction details and Spike question/scope/timebox where applicable.
Link to specific evidence and explain its relevance; “as discussed” is not context.
Known constraints and unresolved questions must be distinguishable.

## Authorization and context

- A request for a draft authorizes no Jira writes. Return a paste-ready draft.
- Explicit create/update authorization is sufficient; do not ask for redundant
  confirmation. Resolve ambiguity about site, project, type, or intended meaning
  before writing. Draft what is known while awaiting a necessary decision.
- Read existing linked context only as needed. For an update, read the existing
  issue fully enough to preserve its text and unrelated sections and fields.
- Do not invent assignee, priority, sprint, labels, dependencies, or deadlines.
  Estimate Stories and Tasks only under the Estimation rules above; set an estimate
  field only when authorized and its project-specific field is confirmed. A
  requirement to populate another field does not authorize guessing its value.

## Atlassian MCP workflow

The connected tools' current schemas are authoritative. Names below may have a
client prefix; use the exposed tool and argument names rather than assuming them.

1. When resolving a site, call `getAccessibleAtlassianResources` once per session
   and cache the selected `cloudId`. Clarify multiple candidate sites; never pick
   the first arbitrarily. Pass `cloudId` explicitly at the top level of execute
   calls and primary calls that require it.
2. Use `getJiraIssue` for a known key. Use `atlassian_search` (Rovo search) for
   semantic Jira/Confluence searches unless the user supplies JQL/CQL; in that case
   use a tool supporting that query language, discovering it if necessary.
   Before creating a new issue, search likely duplicates with a narrow,
   project-aware query. Raise a likely match instead of silently duplicating it.
   A search outage is not evidence that no duplicates exist; report the limitation
   and do not block drafting.
3. Use primary tools such as `createJiraIssue`, `editJiraIssue`, and
   `addOrEditJiraIssueComment` directly when available and authorized. For unavailable
   operations, use discovery with verb + object + product, for example
   “list project issue types Jira” or “lookup account id Jira”. Use only returned
   operation names with the matching `executeRead`, `executeWrite`, or
   `executeDestructive` route. Never guess operation names or IDs.
4. Avoid exhaustive schema or metadata fetches. Where supported, `additional_fields`
   resolves human-readable field names. A rejected create lists allowed/required
   values: repair input once from that error, not speculation. Ask about mandatory
   fields that need a user decision. Resolve an assignee through an account lookup
   and use the returned `accountId`, not a guessed ID or display name.
5. Prepare the description in the correct format (see below), then perform only
   the authorized write. For a parent/child hierarchy, read the known parent and
   check the target project/type supports it; create the parent first, then set
   the child's `parent` on creation or an authorized update. Do not add a
   generic link afterwards to simulate hierarchy. For an authorized issue link
   (including blocks/is blocked by), create both issues first and use the exact
   configured relation and direction as specified above. Never blindly retry an
   ambiguous write timeout. Check whether the issue, change, or relation exists
   first; ask the user if this cannot be established. A timeout is not proof that
   a write failed.
6. Verify the authoritative returned issue, or make one targeted read if the
   payload is insufficient. Check title, type, description including DoD, and
   requested fields. Verify each requested parent assignment from the child's
   `parent` and each requested issue link from link data separately. Report
   discrepancies rather than claiming success.
7. Return the verified key/link and any material unresolved questions. For a
   work-item relation, report both keys and its relation. If MCP is unavailable,
   never fall back to shell or curl. Provide a paste-ready draft and state clearly
   that it was not created or updated. If a write may have completed, report its
   outcome as unknown rather than claiming it did not happen.

Changing workflow status requires a transition, not editing a status field.
Only with separate authorization, discover available transitions and select the
requested named transition using its returned ID. Do not automatically transition
issues, create follow-ups, or add comments. A Spike can propose follow-ups in its
findings without authorizing their creation.

## Preserve content formats

- Use Markdown for ordinary new descriptions and headings/checklists.
- Edit bodies containing inline media or rich HTML losslessly using `html`.
  Before authoring HTML, call `getContentFormatGuide` via `executeRead` with
  `toolName: editJiraIssue` or `toolName: createJiraIssue`, as applicable, and the
  top-level `cloudId`. Follow the current schema and returned guide.
- Preserve unrelated description sections, media, and fields. Never overwrite
  fetched HTML with Markdown. If a lossless edit is not possible with the available
  content/tools, explain the limitation and provide a proposed edit without writing.

## Worked tickets

These details are illustrative, not defaults or inferred project requirements.
The Spike timebox below represents an explicitly agreed timebox.

### Story: Show the delivery address before order confirmation

**User story:** As a shopper placing a delivery order, I want to see my selected
delivery address before confirming the order, so that I can avoid sending the
order to the wrong address.

**Scope:** The order review step for orders requiring delivery. Changing saved
addresses and changing the checkout flow are outside this ticket.

**Definition of Done**
- [ ] An order requiring delivery shows its selected delivery address on the
      review step before the shopper confirms the order.
- [ ] When a shopper changes the selected address through the existing flow,
      returning to review shows the newly selected address, not the previous one.
- [ ] An order that does not require delivery shows no delivery-address section.

**Implementation tasks:** Render the address in the review step; supply the
selected address to that step; cover delivery and non-delivery cases.

### Task: Expose the report-generation API

**Outcome:** Provide the backend capability required by the report-generation
Story. This Task is not independently user-facing.

**Definition of Done**
- [ ] The report-generation API is available and its Swagger documentation is
      published.
- [ ] A valid request returns the generated report and invalid requests return
      the documented error response.

### Spike: Determine whether carrier tracking data can explain delivery delays

**Outcome:** Decide whether the carrier's available tracking data can explain
delays to customers without implying a cause the data cannot establish.

**Question and scope:** Review the carrier's published event definitions and the
sample delayed shipments provided by the support team. Can the data distinguish
a failed delivery attempt from a parcel still in transit? No customer feature or
production integration is included.

**Agreed timebox:** One working day. Stop at the limit and record remaining unknowns.

**Definition of Done**
- [ ] Findings link the reviewed event definitions and samples, distinguishing
      supported interpretations from gaps or conflicting evidence.
- [ ] A recommendation states whether to proceed, not proceed, or gather more
      evidence, with reasons; inconclusive findings are an acceptable result.
- [ ] Proposed follow-ups identify the remaining questions and evidence needed,
      or explicitly state that no follow-up is needed. No implementation is assumed.

## Before publishing

- [ ] A future human or agent can identify the outcome, boundaries, completion
       evidence, and material unknowns without this chat.
- [ ] The title and DoD contain no vague “improve”, “support”, or “handle properly”
       without an observable condition; “works as expected” alone is not a check.
- [ ] The issue delivers one independently useful outcome, or is an Epic whose
       Stories and overall milestone outcome are clear.
- [ ] Every Story uses a user-role, capability, and value statement; its DoD
       proves an end-to-end user-facing feature, not implementation progress.
- [ ] Every Task has technical or operational DoD. A standard Task is a peer of
       a Story unless the project explicitly supports that hierarchy; native
       child work uses a supported Subtask type and `parent`. Ordinary Jira links
       are used only when authorized and requested.
- [ ] DoD is explicit, testable, and specific; no duplicated criteria, invented
        commitments, or unnecessary implementation instructions remain.
- [ ] When an estimate is requested or required, it uses the agreed point scale,
        covers the full medium-agentic delivery lifecycle, and states material
        uncertainty or dependencies.
- [ ] Context is self-contained, links are meaningful, and unresolved decisions
       are questions rather than hidden assumptions.
- [ ] The write matches authorization and preserves unrelated existing content.
- [ ] Each authorized parent assignment and issue link was created natively,
       verified using the appropriate data, and reported with both issue keys
       and the relation/direction.
