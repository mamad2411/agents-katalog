---
name: new-service-request
license: CC-BY-4.0
description: >-
  Create a new service desk issue from available templates. Use when creating
  GitHub issues for the RDL Service Desk repository with data request, enquiry,
  or ICT request templates.
compatibility: >-
  Requires write access to the private rdl-service-desk/service-desk repository,
  via either the GitHub MCP server or an authenticated GitHub CLI (`gh`).
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# New Service Request Skill

Create a new GitHub issue in the RDL Service Desk repository from one of its
issue templates.

**Repository:** `rdl-service-desk/service-desk`
(<https://github.com/rdl-service-desk/service-desk>)

## How to run it

This is an agent skill, not a CLI — there is no `new_service_request` binary.
When it is invoked (e.g. `/rdl-team:new-service-request`), **you** create the
issue using whatever GitHub tooling is available in the session, preferring:

1. the **GitHub MCP server**'s create-issue tool, or
2. the **`gh` CLI** (worked command below).

If you cannot reach `rdl-service-desk/service-desk` (see *Compatibility*
above), tell the user what access is missing instead of guessing.

## Available templates

| Template | Label | Source | Fields |
|---|---|---|---|
| data-request | `data-request` | `data_request_template.md` | Project title, Approval ID, Workflow Checklist |
| enquiry | `enquiry` | `enquiry_template.md` | Overview, Priority |
| ict | `ICT` | `ict_request_template.md` | Overview, Priority |

Labels are case-sensitive: `ICT` is uppercase, the other two are not.

## Workflow

1. **Template** — use the one the user named; otherwise ask: `data-request`,
   `enquiry`, or `ict`.
2. **Issue number** — the user must supply it; never invent one. It is
   allocated outside this repository, so it cannot be derived or guessed.
3. **Fields** — collect the template's fields (see *Template details*). Ask
   only for what is missing.
4. **Headings** — read the template (the table's *Source* file) and use its `##`
   headings verbatim:

   ```bash
   gh api repos/rdl-service-desk/service-desk/contents/.github/ISSUE_TEMPLATE/enquiry_template.md \
     --jq .content | base64 -d
   ```

   If the repository is unreachable, stop: report the error and the missing
   access (see *Compatibility*), and do not claim an issue exists. If only the
   template read fails, use the headings in *Template details* and say they
   were not confirmed.
5. **Create** the issue in `rdl-service-desk/service-desk`, labelled per the
   table and **assigned to the requesting user** (`--assignee @me` with `gh`).
   A request that supplies the template, number, and fields authorizes
   creating it; do not ask again.
6. **Report** the URL that the create command returned. If the create fails,
   quote the error, state that no issue was created, and give the title and
   body for manual filing.

**Title convention:** the issue number prefixed with `THHSRDLENQ-`, uniform
across all three templates — issue number `9181` becomes the title
`THHSRDLENQ-9181`.

Write the body to a file and pass it with `--body-file`:

```bash
body="$(mktemp)"
printf '## Overview\n\nData management review\n\n## Priority\n\nmedium\n' > "$body"
gh issue create --repo rdl-service-desk/service-desk --title "THHSRDLENQ-9181" \
  --label enquiry --assignee @me --body-file "$body"
```

## Template details

These match the repository's templates at commit `a3f4f4a` (checked
2026-09-29). The repository copy wins when they differ.

### 1. Data Request (`data-request`)
- **Project title** — e.g. "Emergency Examination Authority Presentations in the Emergency Department"
- **Approval ID** — e.g. `THHSAQUIRE-9904` or `SSAQTHS-990002`
- **Workflow checklist** — mark items complete (e.g. repo bootstrapped, released)

### 2. Enquiry Request (`enquiry`)
- **Overview** — brief description (e.g. "Data management review")
- **Priority** — `low`, `medium`, or `high`

### 3. ICT Request (`ict`)
- **Overview** — brief description (e.g. "New user account setup")
- **Priority** — `low`, `medium`, or `high`
