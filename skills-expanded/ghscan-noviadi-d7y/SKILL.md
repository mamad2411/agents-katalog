---
name: starting-initiatives
description: "Starts or resumes a discovery initiative after checking the current session and existing initiatives for the same or related intent. Use when asked to start, open, continue, or decide whether to create an initiative."
compatibility: Requires a D7Y runtime binding that exposes the initiative CLI capability (`d7y initiatives list` / `d7y initiatives check`), the binding's own runtime, and a workspace whose `initiatives/README.md` has been loaded.
metadata:
  maturity: provisional
---

# Starting Initiatives

Reliably select an existing initiative or create the minimum durable container for a new investigation.

## 1. Load the initiative contract

Read `initiatives/README.md` before deciding where or whether to create anything. Use its definition, layout, lifecycle, identity criteria, and minimum artifact as the source of truth.

If the contract is missing, stop and propose establishing it before creating an initiative. If an initiative conflicts with the contract, preserve it and report the mismatch rather than silently restructuring it.

**Complete when:** the canonical location, valid statuses, current-initiative rules, and minimum artifact are known from the repository.

## 2. Form a candidate signature

From the request and current conversation, form a provisional signature containing:

- intended outcome;
- subject, user, or domain;
- problem or opportunity;
- scope boundaries and anti-goals;
- primary uncertainty;
- distinctive names, aliases, and search terms.

Retrieve relevant context already present in the session before asking questions. Mark missing elements as unknown; do not require a complete brief merely to check for overlap.

**Complete when:** there is enough of an outcome-plus-problem signature to compare with existing initiatives, or the specific missing distinction that blocks comparison has been identified.

## 3. Resolve an already-current initiative

Check, in order:

1. whether the user named or linked an initiative;
2. whether the working path is inside `initiatives/<slug>/`;
3. whether the conversation clearly continues a previously selected initiative.

Read the candidate's `initiative.md` and compare its intent with the candidate signature. An `active` status or recent modification alone does not establish that it is current.

If the current initiative still encompasses the request, continue it and skip creation. If the request represents a distinct outcome or decision history, continue to repository-wide matching.

**Complete when:** a session-current initiative has been accepted based on intent or ruled out with a concrete difference.

## 4. Search before creating

Invoke the `d7y` CLI at the path the workspace runtime orientation documents, and run `d7y initiatives list --root <absolute-workspace-root> --json` to validate the organization and produce the complete deterministic inventory. Derive `<absolute-workspace-root>` from the repository whose `initiatives/README.md` you loaded in step 1, not from the process working directory or the skill installation path.

Interpret the result by contract: exit `0` is a valid completed inventory; exit `1` with valid JSON is still a completed inventory that contains contract errors—preserve and report the invalid records rather than treating them as absent; a `d7y` command that cannot be found (the shell reports command not found, exit `127`/`126`), exit `2`, malformed JSON, or an execution denial means the D7Y runtime capability is unavailable or incomplete, so stop and report it rather than replacing deterministic validation with model reasoning. Preserve and report invalid artifacts; do not silently exclude them from comparison when their intent remains recoverable.

Use the inventory to search active and paused initiatives first, then graduated and archived ones, using:

1. exact slug, title, and alias matches;
2. distinctive terms from the outcome, subject, and problem;
3. conceptual similarity of intended outcome and primary uncertainty.

Read every plausible candidate's canonical artifact. Do not classify initiatives from filenames or shared keywords alone.

If no initiative artifacts exist, record that the search completed with an empty set rather than treating the search as skipped.

**Complete when:** the deterministic inventory is complete, every plausible match has been read, and there is a comparison based on outcome, problem, subject, uncertainty, and continuity of decision history.

## 5. Classify the relationship

Choose one relationship from the initiative contract:

- **same:** one coherent intent and history can contain both; use the existing initiative;
- **related:** meaningful overlap exists, but separate outcomes or histories justify distinct initiatives;
- **superseding:** one initiative should replace or absorb another;
- **new:** no material match exists;
- **unclear:** available evidence cannot distinguish the choices.

Prefer continuing an initiative when a revised framing remains part of the same learning loop. Prefer a related initiative when combining them would make the primary uncertainty, evidence, or next decision incoherent.

For `unclear`, present the closest candidates and the material difference, then ask the user to choose. For `superseding`, obtain human confirmation before merging or archiving anything.

**Complete when:** the classification is supported by explicit similarities and differences, and every irreversible action has the required owner.

## 6. Resume or create

### Resume the same initiative

- Use its existing directory and canonical artifact.
- Summarize its provisional intent, status, primary uncertainty, and current state.
- Identify how the new request changes or extends it.
- Propose canonical updates when the new context changes durable understanding; preserve evidence and uncertainty distinctions.
- Do not create a duplicate or a global current pointer.

### Create a new or related initiative

- Derive a concise stable slug and check for a path collision.
- Create `initiatives/<slug>/initiative.md` using the exact minimum structure in the organization contract.
- Set dates to the current local date and status to `active`.
- Fill each section only from what the request states:
  - restate given context in Evidence;
  - confine every inference to Assumptions and label it as inference;
  - leave any section the request does not support as `Unknown`.
- Do not invent specifics the request did not supply — no user segments, sub-activities, mechanisms, or examples. If the request does not name the intended user, Subject reads `Unknown`.
- Keep the artifact proportional to the context given; a name-only request yields a thin artifact, not a fleshed-out one.
- Add reciprocal `related` links when another initiative is materially related.
- Create no additional directories or artifacts until a named need requires them.
- Run `d7y initiatives check --root <absolute-workspace-root> --json` again and resolve every error introduced by the new artifact.

Creation is allowed without another checkpoint when the user explicitly asked to start an initiative and matching is unambiguous. Otherwise propose the selection before creating repository state.

**Complete when:** exactly one canonical initiative has been selected, its artifact satisfies the organization contract, and no duplicate directory was introduced.

## 7. Handoff into discovery

Report:

- whether the initiative was resumed or created;
- its path and status;
- the closest similar or related initiative, if any;
- its provisional outcome and primary uncertainty;
- the smallest useful next discovery move.

Do not run a full discovery methodology as part of initiation. Invoke or recommend the next skill based on the primary uncertainty.

**Complete when:** the user and future agents can identify the selected initiative, understand why it was selected, and know the next learning move.

## Failure handling

- **Missing organization contract:** establish or restore the contract before creation.
- **Checker failure:** preserve existing artifacts, report every deterministic error, and repair only the initiative being created or explicitly selected for maintenance.
- **Unavailable runtime capability:** if `d7y initiatives` cannot be found (exit `127`/`126`), exits `2`, returns malformed output, or is denied, stop and report the missing or incomplete D7Y binding rather than substituting model reasoning for deterministic validation.
- **Malformed candidate:** preserve it, report the missing identity fields, and include it in comparison when its intent is recoverable.
- **Slug collision:** select a distinct stable slug; do not overwrite.
- **Several strong matches:** classify as unclear and request a choice.
- **Conflicting session signals:** prefer an explicit user reference; otherwise show the conflict.
- **Graduated or archived match:** explain the status and ask before reactivating it or creating a successor.
