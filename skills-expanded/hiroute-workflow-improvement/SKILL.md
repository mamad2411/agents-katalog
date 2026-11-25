---
name: hiroute-workflow-improvement
description: Improve HiRoute iteration by capturing issue-spec CLI and workflow friction, routing labeled feedback to its owner, and assessing adopted improvements when a later task provides suitable context. Use during relevant project work or requested feedback reviews; not ordinary product bugs or automatic upgrades.
---

# Improve issue-spec through evidence

Use HiRoute iteration as the source of concrete improvement evidence: observed
friction becomes feedback, recurring feedback informs CLI/workflow corrections,
and adopted corrections should improve subsequent HiRoute work. These steps can
span weeks and unrelated sessions; no original agent or conversation owns a
continuous follow-up obligation. Labels support
periodic analysis; filing Issues is an intermediate result, not proof of improvement.

Capture observations while doing the original task, such as repeated manual repair,
ambiguous guidance, unnecessary steps or missing command capability. Do not launch
a separate broad audit or require a feedback report for every task.
Continue the original task wherever possible. Feedback is not a new planning,
review or delivery gate, and creating an Issue does not authorize its implementation.

HiRoute's repository policy authorizes filing, recurrence comments and labeling
evidence-backed feedback from its work, including automatic promotion at the
confirmed recurrence threshold below. Honor a user's narrower scope, such as
read-only or no publication.
Do not infer this standing authorization when copying this skill to another project.
Do not start agents, recurring jobs, workflow upgrades or automatic rule rewrites.

## Establish the cause and destination

Read [instruction ownership](../../README.md), the current project's
`issue-spec/config.yaml` rules and shared guidance. Inspect the relevant installed
command's exact `--help`, or the instruction and its owning source. Record the CLI
revision from `issue-spec version --json`, the generated workflow source revision
from `../issue-spec-workflow/release.json`, and the project commit when applicable.
Different installed and generated revisions alone are not a defect.

| Finding | Destination | Category label |
| --- | --- | --- |
| CLI behavior, command UX, unsupported capability, incorrect output or error | `higress-group/issue-spec` | `improvement/cli` |
| Shared workflow or generated instruction gap whose correction remains useful after removing HiRoute names, paths and policy | `higress-group/issue-spec` | `improvement/workflow-generic` |
| HiRoute policy, project supplement, local skill, validation or repository-specific convention | `higress-group/HiRoute` | `improvement/workflow-project` |

Use the smallest source that actually owns the correction. A stale local recipe or
an agent ignoring correct instructions is not automatically a CLI defect. Correct
routine command use first. File only when a concrete usability or instruction gap
remains; transient network/authentication errors alone do not establish one.

For workflow findings, explain whether the fix survives removal of project policy.
If ownership remains uncertain, gather a bounded additional read; keep a local draft
and state the uncertainty instead of guessing the destination. Split genuinely
independent CLI and workflow causes into linked reports, not copies of one symptom.
Never edit generated `issue-spec-*` files to implement upstream suggestions.

## Deduplicate and write

Use the [report and analysis guide](references/feedback.md) for the body fields,
independent-occurrence counting, label definitions, provider commands and
time-window queries.

1. Verify the destination repository and active backend with read-only CLI/auth
   inspection; use explicit `--repo` on each command. HiRoute and the upstream above
   are GitHub repositories. Do not change profiles or credentials to bypass failure.
   If an explicitly selected backend differs, resolve it before writing.
2. Search both open and closed discussions in the destination with one to three
   specific command, symptom or instruction terms using `issue-spec search issues`.
   Read plausible matches with `issue-spec read issue --comments`. Do not rely only
   on titles, labels, the first page of a broad query, or a search snippet. Follow
   relevant remaining pages or narrow the query; disclose bounded search coverage.
3. Reuse an existing Issue for the same cause and expected correction. Add only new
   evidence or a distinct recurrence through `issue-spec comment create`; do not
   create another Issue merely because another task or agent discovered it. Count
   the original observed report as occurrence 1 and each independently evidenced
   recurrence once. Ordinary discussion, retries and handoffs do not add occurrences.
   Link the prior evidence and record the confirmed count or lower bound in the new
   comment. Respect closed/wontfix decisions. A demonstrated regression after a fix
   may warrant a new Issue linked to the old one; do not reopen it automatically.
   Split unrelated causes even if their symptoms match.
4. Prepare a self-contained English body with sanitized reproduction, expected and
   observed behavior, impact, owning layer, suggested correction and acceptance.
   Include the minimal scenario and prerequisites needed by a future session; a
   conversation link or temporary worktree alone cannot carry required context.
   Distinguish measured facts from hypotheses. A design gap can use an observed
   task sequence rather than a failing command. Do not manufacture a bug to fill
   a category or attach private logs, credentials or local absolute paths.
5. On GitHub, provision missing labels first, then create the ordinary suggestion
   with `gh issue create --body-file ... --label ...` so creation includes its
   classification. This is HiRoute's explicit feedback-publication policy. Use
   issue-spec for selected workflow artifacts and ordinary recurrence comments;
   non-GitHub Issue creation follows its configured issue-spec backend. Use installed
   command help rather than invented flags. No Proposal, typed QUESTION/TASK or
   PROCESS is needed just to collect feedback.
6. Apply `improvement/feedback` and exactly one category label from the table to
   every report, including a reused matching Issue. Preserve unrelated labels.
   Provision missing labels without overwriting existing definitions. For a reused
   Issue with conflicting category labels, resolve ownership before changing them;
   do not silently remove others' classification.
   When recorded evidence on an open, unresolved Issue reaches at least
   **3 confirmed occurrences**, automatically promote it to `priority/high` using the
   [counting and promotion rules](references/feedback.md#count-independent-occurrences-and-promote).
   This is part of recording the feedback, without another approval or periodic job.
7. Read back the Issue URL, body/comment and labels. If a create returns an uncertain
   result, search/read before retrying. If labeling fails after creation, retain the
   URL and report the missing labels; retry only that step after resolving the
   failure. Never create a replacement Issue just to retry labels, switch providers
   after a denial, or claim the labeled feedback is complete when it is partial.

Report the Issue URL, category, create/reuse result, confirmed occurrence count,
priority action and any incomplete labeling. If nothing actionable was found,
say so without filing placeholder Issues.

## Review an interval

When asked, collect the umbrella label from both repositories for the requested
interval, including closed Issues. Use creation time for new reports and dated
occurrence comments for recurrences; updated time is only a discovery aid. Group
by underlying cause and layer, link representative evidence, distinguish unique
Issues from occurrences, and prioritize by observed impact and recurrence.
Propose common fixes upstream and project-specific fixes locally. Summarizing
feedback does not authorize implementation, closure, relabeling history or a schedule.

## Bring improvements back into HiRoute

Resume this loop only when a later related task, an authorized adoption, or a
requested periodic review makes a feedback item relevant. Do not keep the current
task open, wait for an upstream release, poll, or scan the entire backlog on every
iteration. A future session can recover the scenario from its Issue and linked
durable evidence using the [resumption guide](references/feedback.md#resume-after-a-gap).

When a relevant feedback item has a proposed or released fix, assess its current
applicability before planning adoption. Read its actual resolution,
linked implementation and available revision; an Issue closure alone is not proof
that a fix exists, is installed or addresses HiRoute's scenario. Batch related
candidates for the user's periodic review instead of repeatedly interrupting work.

- **CLI correction:** identify the tested fix/release and the currently installed
  revision. Propose adoption when needed. Install or change a global CLI only within
  the user's authorized scope; a feedback-filing policy does not authorize upgrades.
- **Shared workflow correction:** use the reviewed CLI revision and the workflow
  preview/apply procedure in [instruction ownership](../../README.md). Review the
  generated diff and project supplements together; preserve the manifest and links.
  Do not hand-patch generated instructions or update them merely to clear a warning.
- **Project correction:** change the owning HiRoute supplement, skill or validation
  path through the normal authorized change and PR process. Avoid copying generic
  upstream rules into local policy when the shared source now supplies them.

Adoption is separate implementation work: propose it when not yet authorized, and
proceed without asking again when the current task already includes it. Keep
feedback Issues linked to the corresponding fix and adoption PR/revision.

When a comparable scenario is available within the current scope, validate an
adopted improvement against the recorded symptom and applicable project checks.
Recheck current requirements and environment first; historical evidence explains
the report but does not override today's contract. Record actual results and source
versions on the feedback Issue or adoption PR.

If the original context is missing, too costly to reconstruct, obsolete or no longer
relevant, record that limitation and leave the benefit unverified or the scenario
no longer applicable. State a useful future trigger only when known, such as the
next task using the affected command. Do not invent a deadline, assign the original
session ongoing ownership, or reconstruct an old environment solely to finish the
feedback loop. This does not waive checks required by an actual adoption change.

Do not claim time savings without measurements, count an upstream release as local
adoption, infer success from silence, or automatically close the report. New relevant
evidence can resume the same thread later; a remaining cause returns there without
requiring continuity of agent, conversation or worktree.
