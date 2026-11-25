---
name: mini-sdd-spec
description: 'Create or update a feature spec — define functional requirements and cross-cutting constraints for a single feature in a structured spec.yaml. Use when defining a new feature, capturing a requirement, writing a user story, drafting a spec, or refining an existing spec. Do not use for generating the implementation plan (use mini-sdd-plan) or implementing code.'
disable-model-invocation: true
---

Create or update a feature specification file in `./{ARTIFACT_MAIN_FOLDER}/{SPECS_SUBFOLDER}/`.

Each spec captures a single feature or requirement as a structured `feature.yaml`-style document with clear, testable requirements, serving as the contract between the user intent and the implementation. This skill produces **only** the `spec.yaml` contract — the implementation plan is generated separately by `mini-sdd-plan`.

---

## Hook execution

Check `./{ARTIFACT_MAIN_FOLDER}/mini-sdd.config.yml` for `hooks.spec.pre` and `hooks.spec.post` entries. Run pre-hooks before the Entry point; run post-hooks after the full workflow completes. See [references/hooks.md](./references/hooks.md) for the full execution rules.

---

## Entry point

1. Read `./{ARTIFACT_MAIN_FOLDER}/context.md` if it exists — use it as background for all decisions.
2. Determine the user's intent from the input (e.g., `/mini-sdd-spec user authentication`).
   - If no feature name or description is provided, ask: _"What feature or requirement do you want to spec?"_
3. Derive a **spec name** in dash-case from the feature description (e.g., `user-authentication`, `csv-export`, `dark-mode-toggle`).
4. Check for an existing spec by looking for `./{ARTIFACT_MAIN_FOLDER}/{SPECS_SUBFOLDER}/<spec-name>/spec.yaml` (exact match) and by scanning other spec folders for content similarity.
   - **If a match is found** → read its `feature.status` to get the current status, show a brief summary, and ask:
     > "A spec `<existing-spec-name>` already exists (status: <current-status>). Do you want to **update this spec** or **create a new one** with a different name?"
     - **Update** → proceed to **Update flow**
     - **New** → ask for a different name and proceed to **Creation flow**
   - **If no match is found** → output the derived name and proceed to **Creation flow**:
     > "📝 Spec name: `<spec-name>`"

---

## Creation flow

### 1. Clarify the requirement

Ask the user the following in a **single numbered message** (skip questions already answered in the input or inferred from initial context):

1. **What should this feature do?** — Describe the desired behavior in 2–3 sentences.
2. **Who is the user?** — Who benefits from this feature?
3. **Functional requirements** — List the observable behaviors the feature must have. These become the numbered `requirements` under `components`, grouped by area (e.g. a `LOGIN` group, an `EXPORT` group).
4. **Cross-cutting constraints** — Any non-functional requirements (security, performance, data privacy, accessibility)? These become the `constraints` section.
5. **Technical notes** — Any implementation hints, API details, or architectural considerations?

After collecting the requirements, inspect the existing specs under `./{ARTIFACT_MAIN_FOLDER}/{SPECS_SUBFOLDER}/` and infer whether this spec depends on other specs being completed first. Populate `requires:` automatically from that analysis.

Ask the user about dependencies only if the relationship is ambiguous:
> "I found that `<spec-name>` may need `<dependency-spec>` to be completed first. Should I mark it as a dependency?"

### 2. Generate the spec file

Read the template from `assets/spec.template.yaml` and fill it in using the gathered information, see the template header for the rules.

- Create the folder `./{ARTIFACT_MAIN_FOLDER}/{SPECS_SUBFOLDER}/<spec-name>/` if it does not exist.
- Write the spec to `./{ARTIFACT_MAIN_FOLDER}/{SPECS_SUBFOLDER}/<spec-name>/spec.yaml`.
- Fill the `feature` block: `name` = `<spec-name>` (lowercase, dashes/underscores); `description` = 2–3 sentences including who the user is; optional `version` and `prerequisites` (external dependencies).
- Group functional requirements into `components` with `UPPER_SNAKE` keys (e.g. `LOGIN`, `EXPORT`), unique across components and constraints. Number each requirement as an integer (`1`, `2`); use `<N>-<M>` for sub-requirements (max 1 level, never `-0`). A requirement's ACID is `<spec-name>.<GROUP_KEY>.<ID>`.
- Put non-functional / cross-cutting requirements under `constraints`; omit the section entirely if there are none.
- Keep each requirement an observable, testable (pass/fail) behavior. Be descriptive, not prescriptive.
- In the `feature` block set the mini-sdd tracking fields: `requires: [<spec-name>, ...]` from the inferred dependencies, `created: YYYY-MM-DD`, `updated: YYYY-MM-DD`, and `status: draft`.
- Treat unmet `requires` as a derived blocking condition during implementation, not as a separate stored status.

### 3. Confirm and hand off to the plan

Confirm to the user and point them to the next step:
> "✅ Created `<spec-name>/spec.yaml` (status: draft).
> Next: run `/mini-sdd-plan <spec-name>` to generate the implementation plan."

---

## Update flow

Use this when a spec already exists and the user chose to update it.

1. Read the current spec from `./{ARTIFACT_MAIN_FOLDER}/{SPECS_SUBFOLDER}/<spec-name>/spec.yaml`.
2. Ask: _"What needs to change? New requirements, updated constraints, scope change?"_
3. Apply the changes to the relevant `components` / `constraints` / `feature` fields of `spec.yaml`. When adding requirements, append new numbers (or `<N>-<M>` sub-requirements) so existing IDs/ACIDs stay stable.
4. Re-inspect the other specs in `./{ARTIFACT_MAIN_FOLDER}/{SPECS_SUBFOLDER}/` and re-infer `requires:` from the updated spec content.
5. In the `feature` block set: `requires: [<spec-name>, ...]`, `updated: YYYY-MM-DD`, `status: draft`.
   - Setting `status: draft` signals that no `plan.md` exists yet, or that it is out of date and must be regenerated by `mini-sdd-plan`.
   - If some `requires` are not yet `done`, keep that as a derived blocking condition for implementation.
6. Show a summary of what changed and which dependencies were inferred.
7. Confirm and point to the next step:
   > "✅ Updated `<spec-name>/spec.yaml` (status: draft).
   > The spec changed — run `/mini-sdd-plan <spec-name>` to (re)generate the implementation plan."

---

## Status lifecycle

This skill sets `status: draft` — the spec contract exists but has no implementation plan yet. `mini-sdd-plan` advances a spec to `ready` once the plan is generated. The `in-progress` and `done` statuses are managed exclusively by `mini-sdd-implement`. Whether a spec is currently implementable is also derived from `requires:` — if any dependency is not `done`, implementation must wait.

---

## Output rules

{SKILL_ASSETS_NOTICE}
- One spec per file, one feature per `spec.yaml`
- Keep specs concise — aim for something an AI agent can read and turn into a plan without ambiguity.
- Express requirements as observable, testable (pass/fail) behaviors with stable ACIDs (`<spec-name>.<GROUP_KEY>.<ID>`).
- Focus on functional behavior and key constraints; omit obvious or purely cosmetic requirements.
- Do **not** generate `plan.md` here — that is the responsibility of `mini-sdd-plan`.
- If the user is vague, ask one follow-up, then proceed with best effort and record assumptions in `open_questions`.

## Error handling

- **Spec name conflict**: If the derived dash-case name collides with an existing unrelated spec, show both and ask the user to confirm or pick a different name.
- **No input provided**: Ask _"What feature or requirement do you want to spec?"_ before doing anything else.
- **Spec folder not writable / path missing**: Create the `./{ARTIFACT_MAIN_FOLDER}/{SPECS_SUBFOLDER}/<spec-name>/` directory if it does not exist before writing.
- **User abandons the interview mid-way**: Save whatever was collected, leave unanswered fields as their template placeholders, and confirm the partial spec was written.
