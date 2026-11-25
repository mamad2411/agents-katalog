---
name: classic-workflows
description: Read, explain, edit and create Classic Workflows (Dataverse "Prozesse" of category Workflow) via the dataverse-modelling-mcp server. Covers the declarative definition model, the JSON shape for steps and values, validation codes and their fixes, custom code activities, and the architecture behind the format (server-rendered designer, incremental saves, naming conventions). Use when the user asks about classic workflows, background/real-time workflows, workflow XAML, or wants to understand or change an existing process.
version: 1.0
---

# Classic Workflows on Dataverse

Classic Workflows store their logic as WF4 XAML in `workflow.xaml`. **You never write that XAML by
hand.** You describe the logic as a JSON definition; the server generates conventional XAML from it.

Full format reference: `docs/classic-workflows-reference.md` in this repository.

**Related records and the 87 activities of msdyncrmWorkflowTools: see `workflow-tools.md` next to
this file.** Read it before concluding that something "cannot be done with classic workflows" —
team membership, N:N checks, multi-select fields, FetchXML queries and deletes are all available
through that assembly.

## Why the definition model exists

The classic designer is **server-rendered**: every edit is a SOAP call that rewrites the XAML
server-side and returns HTML for display. The designer rebuilds its view from the XAML alone
(`clientdata` is always `null`), and it does so by relying on **naming conventions** — step ids,
`DisplayName` values and variable names. Hand-written XAML that breaks a convention produces
`0x80045037` and the process can no longer be opened.

`workflow_set_definition` owns all naming, so that class of error cannot occur. Everything else is
caught by validation before anything is written.

## Tool map

| Intent | Tool |
|---|---|
| What does this workflow do? | `workflow_explain` |
| Get the logic as editable JSON | `workflow_get_definition` |
| Check a definition before writing | `workflow_validate_definition` |
| Write logic | `workflow_set_definition` |
| Create a new (empty) workflow | `workflow_create` |
| Triggers, mode, scope, subprocess | `workflow_update` |
| Activate / deactivate | `workflow_set_state` |
| Raw XAML for backup or diffing | `workflow_export_xaml` |
| Undo a change | `workflow_restore_xaml` |
| Delete a workflow (and its activation copies) | `workflow_delete` |
| Find out why a definition will not activate | `workflow_diagnose_activation` |
| Change the owner | `workflow_assign` |
| Check an existing workflow (not a definition) | `workflow_validate` |
| Available code activities | `workflow_list_activities` |
| Parameters of a code activity | `workflow_get_activity_parameters` |

## Standard workflows

### Explaining an existing workflow

```
workflow_list (filter) → workflow_explain(workflowId)
```

Read the tail of the report. A **"Not understood"** section means the XAML contains constructs the
parser cannot map. The explanation is then incomplete — and you must not rewrite that workflow with
`workflow_set_definition`, because the unmapped parts would be dropped.

### Changing an existing workflow

```
1. workflow_export_xaml            → keep as restore point
2. workflow_get_definition         → check "fullyUnderstood": true
3. modify the JSON                 → with a script, in a file, never by retyping it
4. workflow_validate_definition    → definitionFile=…, fix all errors
5. workflow_set_definition         → definitionFile=…, backupFile=…, writes only when clean
6. workflow_set_state activate=true
```

If `fullyUnderstood` is false, stop and tell the user which parts are unsupported. Offer to make the
change in the designer instead.

#### Never pass a real definition inline

`definitionJson` and `xaml` exist for small, hand-written payloads. Everything read out of a live
workflow is not that: a definition whose e-mail body carries a base64 signature image runs to ~28.000
characters, its XAML to ~180.000. **Reproducing that corrupts it.** Characters flip, and nothing
catches it — the JSON stays valid, all three validation gates pass, and the damage sits in the payload
the string transports. In August 2026 exactly this destroyed the signature logo in two dunning
workflows; it only surfaced when the PNG chunk checksums were recomputed.

So keep the content on disk and pass paths:

| Direction | Parameter | On |
|---|---|---|
| Definition in | `definitionFile` | `workflow_set_definition`, `workflow_validate_definition`, `workflow_diagnose_activation` |
| Previous XAML out | `backupFile` | `workflow_set_definition` |
| XAML back in | `xamlFile` | `workflow_restore_xaml` |

A too-large tool result is already written to a file for you, so the round trip needs no copy at any
point: read the definition, edit **the file** with a script, pass its path back. Delegating the write
to a subagent does not help — it has the same context window and makes the same mistake.

Verify afterwards rather than assuming: read the definition back and diff it against what you meant to
write (step ids are regenerated, so ignore `stepId`/`branchId`), and for an embedded image decode the
base64 and check the PNG chunk CRCs.

### Creating a new workflow

```
1. workflow_create(name, primaryEntity)        → draft with empty skeleton
2. workflow_set_definition(id, definition)     → the logic
3. workflow_update(id, {"triggeroncreate": true, "createstage": 40})   → trigger (required!)
4. workflow_set_state(id, activate=true)
```

**Step 3 is not optional.** Dataverse refuses to activate an automatic workflow that has no trigger
(`0x80045018`). Pick one:

| Intent | `workflow_update` payload |
|---|---|
| On create | `{"triggeroncreate": true, "createstage": 40}` |
| On change of specific fields | `{"updatestage": 40, "triggeronupdateattributelist": "field1,field2"}` |
| On delete (e.g. to prevent it) | `{"triggerondelete": true, "deletestage": 20}` |
| Started manually | `{"ondemand": true}` |
| Called by another workflow | `{"subprocess": true}` |

Stage `20` = pre-operation (inside the transaction, can block the operation), `40` = post-operation.
Blocking an operation additionally requires a real-time workflow (`{"mode": 1}`) and a
`stopWorkflow` step with `outcome: "cancelled"`.

## The definition shape

```json
{
  "primaryEntity": "lead",
  "steps": [
    {
      "kind": "condition",
      "description": "Only for German leads",
      "conditions": [
        { "attribute": "address1_country", "operator": "Equal",
          "value": { "kind": "literal", "literal": "Germany" } }
      ],
      "then": [
        {
          "kind": "updateRecord",
          "description": "Fill the domain",
          "attributes": [
            { "attribute": "sample_domain",
              "value": { "kind": "field", "fields": ["lead.websiteurl", "lead.emailaddress1"],
                         "fallback": "unknown" } }
          ]
        }
      ],
      "else": [
        { "kind": "stopWorkflow", "outcome": "succeeded",
          "reason": { "kind": "literal", "literal": "Not a German lead" } }
      ]
    }
  ]
}
```

### Step kinds

| `kind` | Purpose | Required fields |
|---|---|---|
| `condition` | If/then/otherwise, or an if/else-if chain | `conditions` + `then`, or `branches`; plus optional `else` |
| `wait` | Wait until a condition holds (background workflows only) | like `condition` |
| `stage` | Grouping. If one step is in a stage, all must be | `children` |
| `createRecord` | Create a record of any table | `entity`, `attributes` |
| `updateRecord` | Update the triggering record | `attributes` |
| `assignRecord` | Change owner | `ownerId`, optional `ownerType` |
| `changeStatus` | Set statecode/statuscode | `state` and/or `status` |
| `customActivity` | Run a code activity | `assemblyQualifiedName`, optional `inputs`/`outputs` |
| `startChildWorkflow` | Start another workflow | `childWorkflowId` |
| `stopWorkflow` | End the workflow | optional `outcome`, `reason` |
| `sendEmail` | Compose and send an e-mail | `attributes` (at least `to` and `subject`) |

`performAction` is **read-only**: it is reported by `workflow_explain` but cannot be generated —
configure it in the designer.

#### Sending an e-mail

A `sendEmail` step composes an `email` record and sends it; the attributes are those of `email`.
The recipient fields (`from`, `to`, `cc`, `bcc`) are **party lists**, so they take
`dataType: "PartyList"` — a fixed recipient as `"systemuser:<guid>"`, a dynamic one as a field:

```json
{
  "kind": "sendEmail",
  "description": "Report assignment",
  "attributes": [
    { "attribute": "from", "value": { "dataType": "PartyList", "literal": "systemuser:<guid>" } },
    { "attribute": "to",   "value": { "kind": "field", "dataType": "PartyList", "fields": ["lead.ownerid"] } },
    { "attribute": "subject", "value": { "literal": "New lead assigned" } },
    { "attribute": "description", "value": { "kind": "concat", "parts": [
        { "literal": "Lead: " }, { "kind": "field", "fields": ["lead.companyname"] } ] } },
    { "attribute": "regardingobjectid",
      "value": { "kind": "field", "dataType": "EntityReference", "fields": ["lead.leadid"] } }
  ]
}
```

`regardingobjectid` links the e-mail to the triggering record — without it, the e-mail does not
appear in any timeline. For an HTML body, `description` is a `concat` of text fragments and fields.

The standard step cannot resolve an e-mail to a **team**; for that there is
`msdyncrmWorkflowTools.Class.EmailToTeam` (see `workflow-tools.md`).

The definition also carries `realtime`, but you do not set it: the server takes it from the workflow
record, because a real-time process must not contain persistence points and the generated XAML
therefore differs by mode.

### Several cases in one condition

The designer allows an **if / else-if chain**: one condition step with several branches, each with its
own comparisons, tested in order — the first that holds runs, the rest are skipped. Use `branches`
instead of `conditions`/`then`; `else` is the default case either way:

```json
{
  "kind": "condition",
  "description": "Check prerequisites",
  "branches": [
    { "conditions": [ { "attribute": "sample_invoicenumber", "operator": "Null" } ],
      "steps": [ { "kind": "stopWorkflow", "outcome": "cancelled" } ] },
    { "conditions": [ { "attribute": "sample_reminderdate", "operator": "NotNull" } ],
      "steps": [ { "kind": "stopWorkflow", "outcome": "cancelled" } ] }
  ],
  "else": [ { "kind": "updateRecord", "attributes": [ … ] } ]
}
```

This is not the same as nesting conditions inside `else`: it produces the shape the designer
produces, one condition step with N branches. The typical use is a guard clause per precondition, each
with its own exit — that is how the payment reminder workflow is built (six cases).

Mixing `branches` with `conditions`/`then` in the same step is rejected as `WF140`.

Several comparisons in one case are combined with `logicalOperator`: `"And"` (default) or `"Or"`.
It sits next to the `conditions` list — in the short form on the step, in a chain on the branch.

### Mixing And and Or: groups

One level combines its comparisons with a single operator, so `A And (B Or C)` needs a bracket. An
entry of `conditions` becomes one by carrying `conditions` of its own plus a `groupOperator`, instead
of an attribute and an operator:

```json
{
  "kind": "condition",
  "logicalOperator": "And",
  "conditions": [
    { "attribute": "new_paymentmethod", "operator": "In",
      "value": {"kind":"literal","dataType":"OptionSetValue","literals":["100000000","100000001"]} },
    { "groupOperator": "Or", "conditions": [
        { "attribute": "new_accountowner", "operator": "Null" },
        { "attribute": "new_bic",          "operator": "Null" } ] }
  ],
  "then": [ … ]
}
```

Groups nest to any depth and work in a `branches` case just as well. Nothing else changes: a level
whose members all share one operator is still written — and read back — as a flat list.

The XAML needs no new construct for this, because the combination has always been a tree:
`EvaluateLogicalCondition` takes a `LeftOperand` and a `RightOperand`, and either may be the result of
another one. A designer-authored example is kept as the `condition-group` fixture.

### Comparison operators

| Group | Operators |
|---|---|
| Equality | `Equal`, `NotEqual` |
| Emptiness (take **no** value) | `Null`, `NotNull` |
| Text | `Contains`, `DoesNotContain`, `BeginsWith`, `DoesNotBeginWith`, `EndsWith`, `DoesNotEndWith` |
| Numbers | `GreaterThan`, `GreaterEqual`, `LessThan`, `LessEqual` |
| Sets | `In`, `NotIn` — use `literals` for the values |
| Ranges | `Between`, `NotBetween` |
| Dates, with a value | `On`, `OnOrAfter`, `OnOrBefore` — often against `{"kind":"now"}` |
| Dates, without a value | `Today`, `Yesterday`, `Tomorrow`, `Last7Days`, `Next7Days`, `LastWeek`, `ThisWeek`, `NextWeek`, `LastMonth`, `ThisMonth`, `NextMonth`, `LastYear`, `ThisYear`, `NextYear` |

Anything else is rejected as `WF072`. An operator that takes no value gets `WF074` if you supply one
anyway; one that needs a value gets `WF073` if you leave it out.

### Value kinds

| `kind` | Meaning | Example |
|---|---|---|
| `literal` | Constant | `{"kind":"literal","literal":"Active","dataType":"String"}` |
| `literal` with `literals` | A set of constants, for `In`/`NotIn` | `{"kind":"literal","dataType":"OptionSetValue","literals":["1","2","3"]}` |
| `field` | One or more fields, first non-empty wins, optional fallback | `{"kind":"field","fields":["lead.websiteurl","lead.emailaddress1"],"fallback":"unknown"}` |
| `stepOutput` | Output of an earlier code activity | `{"kind":"stepOutput","stepOutput":"Domain"}` |
| `now` | Current date and time, evaluated at run time | `{"kind":"now","dataType":"DateTime"}` |
| `concat` | Several values joined into one string | `{"kind":"concat","dataType":"String","parts":[{"literal":"No. "},{"kind":"field","fields":["invoice.sample_invoicenumber"]}]}` |

`concat` is what an e-mail body is made of: constants and field values in order, nested as deep as
needed. `now` works both as a written value and as the right-hand side of a date comparison
(`OnOrAfter`, `OnOrBefore`, …).

#### A deadline: `offset`

Any date value may carry an `offset`, which is how the designer computes a due date. The dunning
workflows use it to set the next dunning level's deadline a week out:

```json
{"kind":"now","dataType":"DateTime","offset":{"days":7}}
```

`offset` takes `years`, `months`, `days`, `hours` and `minutes`; anything omitted is zero, and negative
values move the date backwards. It also applies to a `field`, which then shifts that field's date
instead of the current time.

> An **empty** date is not an offset and not a special kind — it is a `literal` with no `literal` value.
> That is how "clear this field" is expressed, and the reader distinguishes it from a value it failed to
> understand: an unresolvable expression is reported in `unrecognised`, a deliberate clear is not.

`dataType` defaults to `String`. Others: `Integer`, `Boolean`, `DateTime`, `Decimal`, `Double`,
`Money`, `OptionSetValue`, `EntityReference`, `Guid`. Set it whenever the target field is not text —
for a plain field a wrong type produces a runtime failure; on a code activity's input it is caught as
`WF086`.

An `EntityReference` literal is written as `"<entity>:<guid>"`, e.g.
`"team:11112222-3333-4444-5555-666677778888"`.

Field references are always `entity.attribute` with logical names. Which record they are read from
depends on one of three keys — without any of them, only the triggering record is readable:

| Read from | Key | Example |
|---|---|---|
| A directly linked record (one level) | `via` = the lookup attribute leading there | `{"fields":["opportunity.sample_salesrep"],"via":"opportunityid"}` |
| A record an earlier `createRecord` step made | `fromStep` = its step id or the created entity | `{"fields":["email.activityid"],"fromStep":"email"}` |
| The record behind a code activity's output | `fromStepOutput` = the parameter name | `{"fields":["systemuser.fullname"],"fromStepOutput":"InitiatingUser"}` |

`via` reaches one level only; deeper paths need a child workflow or
`msdyncrmWorkflowTools.QueryValues` (see `workflow-tools.md`). With `fromStepOutput` the server emits
the record load itself, so the output being a mere reference is not a problem. All three work in
`conditions[]` as well.

### Code activities

```
workflow_list_activities(nameFilter) → pick the pluginTypeId
workflow_get_activity_parameters(pluginTypeId)
```

Take `assemblyQualifiedName` **verbatim** from the result — it carries the assembly's real
`PublicKeyToken`, and a wrong one makes the workflow fail to load. Use each parameter's
`dependencyPropertyName` as the key in `inputs`/`outputs`, not its display name (`Email`, not
`E-Mail`). Each parameter reports the `dataType` to use, and a lookup reports its allowed
`entityNames`.

You do not have to get the types right by inspection: the server reads the activity's real signature
before writing and reports a wrong name, a wrong `dataType`, a missing required input or a lookup on
the wrong table as `WF085`–`WF089`. Only what it cannot know statically — the target of a lookup
taken from a field — still surfaces at runtime.

Outputs of a step are referencable by later steps as `<stepId>.<ParameterName>` **or by the bare
parameter name**, which is usually what you want: step ids are assigned by the builder, so you cannot
know them when writing the definition. They come back in `stepIds` and are assigned in document
order, so a step can only use outputs of steps declared before it.

#### A value that exists only during the run

There is no "set variable" step, so a value that has to be computed in one place and used in another
looks at first like it needs a helper column. It does not. An activity's output **is** a workflow
variable, scoped to the single run, and it is empty when the activity did not execute. That gives you
a conditional text block without persisting anything:

```
condition (payment method in …)
└─ then: customActivity StringFunctions
           inputs.InputText = {"kind":"concat", …}   ← the builder concatenates
           outputs: ["TrimmedText"]                  ← the same text back out
…
createRecord email
   description = {"kind":"concat","parts":[ …, {"kind":"stepOutput","stepOutput":"TrimmedText"} ]}
```

`msdyncrmWorkflowTools.StringFunctions` is a pure pass-through here — `InputText` in, `TrimmedText`
out. Take the concatenation itself from the builder (`concat`), not from the activity: it cannot
concatenate. Note that the activity computes **all** of its outputs on every run, so give the
substring, padding and replace inputs values that cannot throw (a substring of length 1, padding to
length 0, a non-empty `ReplaceOldValue`).

When the branch does not run, the variable is `Nothing`, and the `Add` behind `concat` tolerates that
— the same way an optional field read without `fallback` does. So the else branch needs no step at all.

Reading back works too: `workflow_get_definition` reduces an input argument to the value it was built
from, even though the XAML stores only a reference into a chain of preparation activities
(`[DirectCast(Step1_1_converted, …)]`). Fixed record references come back as `"entity:guid"`, field
reads with their `via`, and an earlier activity's output as `stepOutput`. If a chain cannot be
reduced, that input is listed in `unrecognised` and `fullyUnderstood` is false — then change the step
in the designer rather than rewriting it.

## Validation

`workflow_validate_definition` and `workflow_set_definition` run the same three gates:

1. **Model** — completeness and consistency of the definition.
2. **Metadata** — every table and attribute must exist in the environment, and the arguments of a
   code activity must match its real signature (both live lookups).
3. **Generated XAML** — well-formed, all variables declared, step ids unique.

Nothing is written unless all three pass. Each issue carries `code`, `path`, `problem` and `fix`.

### Issue codes

| Code | Meaning |
|---|---|
| `WF000` / `WF001` | `definitionJson` is not valid JSON, or the definition is null |
| `WF002` / `WF003` | primary entity or steps missing |
| `WF010`–`WF012` | step kind missing, unknown, or not generatable |
| `WF013` / `WF014` | stage nested, or empty |
| `WF015` | stage without a description (warning — stages are the outline in the designer) |
| `WF020` / `WF021` | create without entity; update targeting a different table |
| `WF030`–`WF032` | assign step: owner missing or malformed |
| `WF040` | change-status without state/status |
| `WF050` / `WF051` | child workflow id missing or malformed |
| `WF060` | stop step with an unknown `outcome` (use `"succeeded"` or `"cancelled"`) |
| `WF070`–`WF076` | condition: no comparisons, missing attribute/operator/value, no branches |
| `WF079` | comparison reads another table without `via`, `fromStep` or `fromStepOutput` |
| `WF077` / `WF078` | condition on a step output: no parameter named, or no earlier step declares it |
| `WF080`–`WF084` | code activity: AssemblyQualifiedName missing/malformed, `PublicKeyToken=null`, empty parameter name |
| `WF085`–`WF089` | code activity checked against its real signature: unknown input (`WF085`), `dataType` not matching the parameter (`WF086`), required input missing (`WF087`), lookup pointing at a table the parameter does not accept (`WF088`), unknown output (`WF089`) |
| `WF090`–`WF092` | attribute assignments: none, unnamed, duplicated |
| `WF100`–`WF102` | value missing, unknown kind, unknown data type |
| `WF110`–`WF114` | literal null, ignored fields, null entry in `literals`, ignored fields on `now`, `concat` without `parts` |
| `WF120`–`WF122` | field value: no fields, bad reference format, non-primary entity |
| `WF130`–`WF132` | stepOutput: missing, malformed, or no matching earlier output |
| `WF140` | `branches` and `conditions` used in the same condition step |
| `WF200`–`WF202` | generated XAML failed self-check (**internal defect — report it**) |
| `WF210` | workflow is activated; deactivate or pass `reactivate=true` |
| `WF300` / `WF301` | table or attribute does not exist (includes name suggestions) |

## Rules and pitfalls

- **A cancellation message that shows only the step name means the message was empty.** Dataverse
  falls back to the display name. The cause is a field read inside the message that names a target
  type: for anything that is not text — a date above all — it comes back empty and takes the sentence
  with it. The builder now reads untyped there, matching the designer. If you see it again, compare
  the `GetEntityProperty.TargetType` of that read against a designer-authored workflow.
- **Active workflows cannot be changed.** Either deactivate first or pass `reactivate=true`. If
  re-activation fails after writing, the response says so and the workflow stays a draft — never
  assume it is active again.
- **Keep the backup.** `workflow_set_definition` returns the previous XAML in `backup`, or writes it
  to `backupFile` if you give it a path — do give it one, both to keep the response readable and
  because `workflow_restore_xaml` can then take `xamlFile` and restore it without a copy.
- **Activating leaves a second row behind.** Dataverse stores an activation copy (`type=2`) that
  neither deactivating nor deleting the definition removes — an environment used for testing fills up
  with them. `workflow_delete` takes them along; it refuses an activated workflow unless
  `deactivateFirst=true`.
- **Don't create workflows with `record_upsert`.** A create without valid `xaml` is rejected with
  `0x80045040`. `workflow_create` supplies a valid skeleton, so use it.
- **`0x80045040` on a write means "XAML not accepted"**, not "wrong access path" — even though the
  message talks about being "created outside of the web application". If you ever see it from
  `workflow_set_definition`, that is a builder defect worth reporting; the tool normally catches
  such cases beforehand.
- **Activation does not validate the logic.** A step with missing configuration activates happily
  and fails at runtime. Validation in this server is stricter than Dataverse on purpose.
- **`updateRecord` writes to the triggering record only.** It uses a temporary entity internally and
  writes the result back.
- **`wait` steps require background mode** (`mode=0`). In a real-time workflow they will not work.
- **Set `mode` before writing the logic.** A real-time workflow must not contain persistence points,
  so the generated XAML differs by mode. Switching a workflow to real-time after writing leaves stale
  `Persist` elements behind; write the logic again afterwards.
- **Activation errors say nothing useful.** `0x80040216` is literally "an unexpected error occurred",
  and `0x80048455` names the composite but not the reason. Do not guess: call
  `workflow_diagnose_activation` with the same definition — it writes subsets into throwaway
  workflows until the culprit step (and case) is isolated, then deletes them again.
- **On a workflow you did not author, start with `dryRun=true`.** `workflow_set_definition` then
  validates and reports in `diff` what would change — including a warning if the current logic
  contains constructs that would be dropped.
- **Environment write policy:** `contoso-dev` is the safe write target. Confirm with the user before
  writing to `contoso-prod` (production).

## Choosing between classic workflow and cloud flow

Classic workflows are legacy but still the right tool when: the logic must run **synchronously**
inside the transaction (real-time, pre-operation), it must **prevent an operation** by throwing, or
it calls an existing **custom code activity**. For anything else prefer a cloud flow — see the
`cloud-flows` skill.
