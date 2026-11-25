---
name: makinari-obj-vitrinas
description: Objective skill for delivering frontends built on top of pre-built Vitrina templates. Clone the right branch, inject real data, remove demo content, and deploy. Do NOT initialize a Next.js app from scratch.
types: ['develop', 'content', 'design', 'automation', 'task']
---

# SKILL: makinari-obj-vitrinas

## Objective

Fast-track the delivery of packaged frontends by using pre-built Vitrina templates. A Vitrina is a ready-made Next.js shell (text viewer, gallery, slide viewer, PDF viewer, data table, automation runner) with a declared data contract. Your job is to checkout the right branch and inject real content — not to rebuild the shell.

## Prerequisites

Prefer **`makinari-obj-template-selection`** as plan step 1 so the correct Vitrina branch (or generic baseline) is chosen and recorded before this skill runs. If `requirement.instructions` already declares `BASE: ...` from a prior cycle, skip re-selection and go straight to data injection.

## Execution Rules

### 1. Branch workflow
- The repo at `/vercel/sandbox` is already cloned.
- Checkout the Vitrina base branch:
  ```
  git fetch origin <base_branch>
  git checkout -B feature/{req_id} origin/<base_branch>
  ```
- Edit only the data files — never replace the shell.
- The system handles commit and push after you finish.

### 2. Vitrina types and base branches

| Requirement kind | Vitrina | Base branch |
| --- | --- | --- |
| Content (strategy, copy, articles) | Text / Markdown viewer | `feature/9be0a6a2-5567-41bf-ad06-cb4014f0faf2/424cc56d-510e-4bbf-a4e1-aa2e30700325` |
| Design / Media (visual assets) | Gallery viewer | `feature/9be0a6a2-5567-41bf-ad06-cb4014f0faf2/512ceb6a-f133-4716-9a10-0d2a008c10ed` |
| Presentations (pitch decks, slides) | Slide viewer | `feature/ce1b2fec-3455-49a1-a35d-54671c00d00d` |
| PDF documents | PDF viewer | `feature/16ccdd2c-6636-4b38-a4fc-89ea2c9fe0cc` |
| Data / Analytics | Data table viewer | `feature/6e819746-5da2-4e3a-8192-0a592dff99cc` |
| Automations (webhook runners) | Automation runner UI | `feature/c3dcbbab-585a-46e9-b320-19b149a24aa0` |

### 3. Data injection
- Read the existing data file: typically `src/app/data.json` or `src/data.json` (use `sandbox_list_files` to confirm).
- Replace demo data **entirely** with the real content from the requirement. No mixing.
- Preserve the data schema — the Vitrina code expects specific keys. If a field is missing in the requirement, leave it empty rather than renaming the key.

### 4. Quality floor
- Every Vitrina ships with demo content (placeholder items, example copy). Remove all of it.
- Interactive features (pagination, filtering, search) must still work with the new data.
- Run `sandbox_run_command npm run build` to confirm the shell still compiles after your injection.

### 5. Delivery
- The preview URL is the permanent Vercel deployment URL from the branch push (extracted automatically after push). Do NOT guess URLs.
- Use `requirement_status action="create"` with the preview URL and a message per `makinari-fase-reporteado`.
- The workspace archive is uploaded on each `sandbox_push_checkpoint`.

## Tools

| Tool | When to use |
| --- | --- |
| `sandbox_run_command` | `git fetch` / `git checkout`, `npm run build`, read-only diagnostics. |
| `sandbox_read_file` | Inspect the Vitrina `data.json` schema before replacing. |
| `sandbox_write_file` | Write the updated `data.json` (and only `data.json` / declared content files). |
| `sandbox_list_files` | Find the data file when the path differs by Vitrina variant. |
| `requirements` | Read the content / media / dataset the client supplied. |
| `requirement_status` | Publish the preview URL. |
| `instance_plan` | Report step status via `action="execute_step"`. |

## Artifacts

- **Produces**: updated `src/app/data.json` (or the Vitrina's declared data file), final `requirement_status` with preview URL.
- **Consumes**: `requirement.instructions` content payload, selected Vitrina shell (chosen by `makinari-obj-template-selection`).

## Anti-patterns

- Modifying the Vitrina shell (components, layout, styles). Keep edits scoped to data.
- Running `npx create-next-app` inside a Vitrina. The shell is already initialized.
- Leaving placeholder demo items next to real content.
- Renaming data keys because the requirement's fields don't line up — propose a schema change through the requirement instead.
