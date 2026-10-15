---
name: address-ticket
version: 3.6.0
description: End-to-end ticket implementation with a multi-agent team using TDD. Retrieves JIRA ticket details and Figma designs, spawns a PO to write requirements, gets developer approval, then proposes a test plan for review. Once tests are approved, implements tests first (red), then production code to pass them (green).
argument-hint: ""
---

Read the JIRA ticket for the current branch and drive it to completion using a multi-agent team with TDD: a PO writes requirements, the developer approves, then a test plan is proposed and reviewed. Once confirmed, tests are written first (red), then production code is implemented to make them pass (green).

**Usage:**
- `/address-ticket` - Retrieve the ticket and drive it to full implementation with a team

**Instructions:**

## Phase 1 — Gather Context

1. **Validate that the Atlassian CLI is available and authenticated:**
   - Run `acli auth status` to check if the CLI is installed and authenticated
   - If the command is not found, display the following error and STOP:
     ```
     Atlassian CLI (acli) is not installed.
     This skill requires the Atlassian CLI.
     Install it with: brew tap atlassian/acli && brew install acli
     ```
   - If the command fails with an authentication error, display the following error and STOP:
     ```
     Atlassian CLI is not authenticated.
     This skill requires an authenticated Atlassian CLI.
     Please run `acli auth login` to authenticate before using /address-ticket.
     ```

2. **Extract the JIRA ID from the current branch name:**
   - Run `git branch --show-current` to get the current branch name
   - Extract the JIRA ID by matching the pattern `[A-Z][A-Z0-9]+-[0-9]+` (e.g., `PROJ-123`, `AB-1`, `MYAPP-4567`)
   - The JIRA ID can appear anywhere in the branch name (e.g., `fix/PROJ-123`, `feat/PROJ-123`, `PROJ-123-some-description`, `feature/PROJ-123-add-login`)
   - If no JIRA ID is found in the branch name, display the following error and STOP:
     ```
     No JIRA ID found in branch name: "<current-branch>"
     Expected a branch name containing a JIRA ID (e.g., PROJ-123).
     Examples: fix/PROJ-123, feat/MYAPP-456, PROJ-123-add-login
     ```

3. **Fetch the JIRA ticket:**
   - Use the Atlassian CLI to retrieve the issue by its JIRA ID:
     ```bash
     acli jira workitem view <JIRA-ID> --fields '*all' --json
     ```
   - This fetches **all available fields** on the ticket. Beyond the standard fields (summary, description, issue type, priority, comments), use every field that provides useful context — for example, bugs often have "Expected Behavior" and "Actual Behavior" fields, stories may have "Acceptance Criteria" fields, etc. Custom fields vary by project, so read whatever the ticket provides.
   - **Attachments**: The JSON response includes an `attachment` array with metadata for each attached file (`id`, `filename`, `content`, `mimeType`, `size`). The `acli` CLI does not have a built-in download command for attachments, so use the **Jira REST API** directly with the `acli` auth token to download them.

     **a) Create a local directory for attachments:**
     ```bash
     mkdir -p /tmp/<JIRA-ID>-attachments
     ```

     **b) Download each attachment** via the Jira REST API. Each attachment object contains a `content` field — this is the REST API download URL (format: `https://<site>.atlassian.net/rest/api/3/attachment/content/<id>`). Use `acli auth token` to authenticate:
     ```bash
     curl -s -L -H "Authorization: Bearer $(acli auth token)" \
       -o "/tmp/<JIRA-ID>-attachments/<filename>" \
       "<content-url>"
     ```
     If the `content` URL is missing from the response, construct it manually from the site URL (extracted from the `self` field) and the attachment `id`:
     ```bash
     curl -s -L -H "Authorization: Bearer $(acli auth token)" \
       -o "/tmp/<JIRA-ID>-attachments/<filename>" \
       "https://<site>.atlassian.net/rest/api/3/attachment/content/<attachment-id>"
     ```
     Repeat for every attachment in the array. Download all of them — images (screenshots, mockups, diagrams), documents (PDFs, CSVs), data files (JSON, XML), logs, config files, etc.

     **c) Analyze the downloaded files:**
     - **Images** (PNG, JPG, GIF, SVG, WebP): Read them to understand visual context — UI expectations, bug screenshots, mockups, diagrams, workflow illustrations
     - **Text-based files** (CSV, JSON, XML, log files, config files, `.txt`): Read their content to extract data, error patterns, configuration details, or reproduction steps
     - **PDFs**: Read them for requirements, specifications, or design documents
     - **Other formats**: Note the filename and MIME type; if unreadable, skip gracefully

     **d) Track all downloaded file paths** — they will be passed to the PO, test planner, test authors, and developer agents so every agent has access to the original ticket attachments.

   - If an individual attachment download fails or the file is too large to process, **continue working** with the remaining attachments but notify the developer:
     ```
     Could not download/analyze attachment: "<filename>" (<reason: download failed / too large / unsupported format / etc.>)
     Proceeding with the available information.
     ```
   - If the JIRA fetch fails (issue not found, permission denied, etc.), offer a fallback: use `AskUserQuestion` to ask the developer if they want to paste the ticket content manually. If the developer declines, STOP. If the developer provides content, continue with that.

4. **Retrieve Figma designs (if referenced):**

   Figma design links can appear in two places: directly as URLs in ticket fields, or as associated designs set by the Figma for Jira app ("Add Design" button). Check both sources.

   **a) Check ticket fields for Figma URLs:**
   - Search all ticket fields (description, comments, attachments, custom fields) for Figma URLs (e.g., `https://www.figma.com/design/...`, `https://www.figma.com/file/...`, `https://www.figma.com/proto/...`)

   **b) Check associated designs via Atlassian GraphQL API:**
   - Figma designs added via the "Add Design" button are **not** stored in standard issue fields, remote links, or attachments. They are stored as **associated designs** — a separate data layer accessible only through the Atlassian GraphQL API with basic auth.
   - **OAuth tokens (from `acli`) do NOT work** for this query — the `designs` field is restricted to first-party clients. Basic auth with a personal API token through the tenanted endpoint is treated as first-party.

   - **Get credentials:**
     - Check the `ATLASSIAN_EMAIL` and `ATLASSIAN_TOKEN` environment variables
     - If either is missing, use `AskUserQuestion` to request them:
       > To retrieve Figma designs linked to this ticket, I need your Atlassian credentials (basic auth — not OAuth).
       >
       > - **Email**: Your Atlassian account email
       > - **API Token**: A personal API token from https://id.atlassian.com/manage/api-tokens
       >
       > You can also set `ATLASSIAN_EMAIL` and `ATLASSIAN_TOKEN` environment variables to skip this step in the future.

   - **Get the issue's numeric ID:**
     - From the `acli jira workitem view <JIRA-ID> --json` response (already fetched in step 3), extract the numeric `id` field (not the key — e.g., `150983`, not `PROJ-123`)

   - **Query the GraphQL API:**
     ```bash
     CLOUD_ID="d5b2094b-04bb-467d-b98e-f39df372f11b"
     ISSUE_ID="<numeric-id>"
     ISSUE_ARI="ari:cloud:jira:${CLOUD_ID}:issue/${ISSUE_ID}"
     SITE_ARI="ari:cloud:jira::site/${CLOUD_ID}"
     curl -s -u "${ATLASSIAN_EMAIL}:${ATLASSIAN_TOKEN}" \
       -X POST \
       -H "Content-Type: application/json" \
       -H "X-Query-Context: ${SITE_ARI}" \
       "https://tablecheck.atlassian.net/gateway/api/graphql" \
       -d "{
         \"query\": \"query GetDesigns { jira_issuesByIds(ids: [\\\"${ISSUE_ARI}\\\"]) { key designs @optIn(to: \\\"GraphStoreIssueAssociatedDesign\\\") { edges { node { ... on DevOpsDesign { displayName designUrl: url } } } } } }\"
       }"
     ```
   - Extract all `designUrl` values from the response — these are the Figma URLs
   - If the GraphQL call fails (auth issues, no designs found, etc.), **continue** with the remaining information — this is a best-effort retrieval

   **c) Extract design information using `fcli`:**
   - If Figma URLs are found from either source (step 4a or 4b):
     1. **Validate that `fcli` is available:**
        - Run `fcli auth status` to check if the CLI is installed and authenticated
        - If `fcli` is not found, display the Figma URLs to the developer and use `AskUserQuestion` to request manual design assets (PNG/SVG files), then continue
        - If `fcli` is not authenticated, try setting `FIGMA_ACCESS_TOKEN` env var if available, otherwise inform the developer and fall back to manual asset request

     2. **For each Figma URL, extract design data:**

        **File metadata:**
        ```bash
        fcli file info --url "<FIGMA_URL>" --json
        ```
        Retrieves file name, last modified date, and version info.

        **Document tree (structure and layout):**
        ```bash
        fcli file inspect --url "<FIGMA_URL>" --depth 5
        ```
        Returns a human-readable tree showing the component hierarchy: `TYPE name [id]` with 2-space indentation per level. Use `--depth` to control tree depth (default is 3 for full files). For a specific node (URL with `node-id` param), the depth is unlimited by default.

        For full structural detail (to understand exact properties, constraints, auto-layout settings):
        ```bash
        fcli file inspect --url "<FIGMA_URL>" --depth 5 --json
        ```

        **Export screenshots:**
        ```bash
        mkdir -p /tmp/<JIRA-ID>-figma
        fcli file export --url "<FIGMA_URL>" --scale 2 --output /tmp/<JIRA-ID>-figma/
        ```
        Exports the node(s) referenced in the URL as PNG files (default format). If the URL contains a `node-id` query parameter, that specific node is exported. Use `--ids` to export multiple nodes: `--ids "1:2,3:4"`. Output files are named `{node-id}.png` (colons replaced with hyphens).

        **List components (if the file is a component library or contains reusable components):**
        ```bash
        fcli components list --url "<FIGMA_URL>" --json
        ```
        Returns component names, node IDs, and descriptions — useful for mapping Figma components to codebase components.

        **List styles (colors, typography, effects):**
        ```bash
        fcli styles list --url "<FIGMA_URL>" --json
        ```
        Returns style names, types (FILL, TEXT, EFFECT, GRID), and node IDs.

     3. **Analyze the extracted design data:**
        - Read the exported PNG screenshots to understand the visual design (layout, spacing, colors, typography, component structure, interaction states)
        - Use the document tree to understand the component hierarchy and naming
        - Use components and styles lists to map design tokens to existing codebase patterns
        - Note: `fcli` uses `--url` to avoid shell quoting issues with Figma URLs containing `?` and `&`

     4. **Store the design data** — the tree structure, screenshots paths, components, and styles will be passed to the PO, designer, test planner, and developer agents

   - If no Figma URLs are found from either source, skip this step silently

5. **Determine the conventional commit prefix:**
   - Based on all available ticket fields (issue type, summary, description, custom fields, etc.), deduce the most appropriate conventional commit prefix:
     - `feat` — new functionality or feature
     - `fix` — bug fix
     - `docs` — documentation-only changes
     - `style` — code style changes (formatting, whitespace, etc.)
     - `refactor` — code restructuring without behavior change
     - `perf` — performance improvement
     - `test` — adding or updating tests only
     - `build` — build system or dependency changes
     - `ci` — CI/CD configuration changes
     - `chore` — maintenance tasks, tooling, etc.
     - `revert` — reverting a previous change
   - Use the issue type as the primary signal (e.g., Bug -> `fix`, Story with new functionality -> `feat`)
   - Use the summary and description to refine when the issue type is ambiguous (e.g., a Task could be `refactor`, `chore`, `docs`, etc.)
   - If the branch name already contains a conventional commit prefix (e.g., `fix/PROJ-123`), use it as a hint but verify it makes sense given the ticket content
   - If you hesitate between multiple prefixes, use `AskUserQuestion` to let the developer choose. Present the top candidates with a brief explanation of why each could apply.

6. **Analyze the codebase:**
   - Read all available ticket fields thoroughly — summary, description, comments, and any custom fields (expected/actual behavior, acceptance criteria, steps to reproduce, etc.)
   - Incorporate the downloaded attachments from step 3 into the analysis (e.g., use screenshots to understand UI expectations, use logs to identify error patterns, use mockups to guide implementation, use data files to understand expected inputs/outputs)
   - Explore the codebase to understand:
     - Which files and modules are relevant to the ticket
     - Existing patterns and conventions in the affected areas
     - Any related unit tests that exist or will need updating
     - The e2e test setup: look for Playwright config (`playwright.config.ts`), existing e2e test files, test directory structure, authentication patterns (storage state, global setup), and helper utilities
   - Consider the conventional commit prefix as context for the type of work expected (e.g., `fix` implies a bug fix, `feat` implies new functionality, `refactor` implies restructuring)

7. **Evaluate whether the ticket should be split (only if necessary):**

   After analyzing the ticket and the codebase, assess whether the work is too large for a single PR. PRs should be as small and independently testable as possible. **Only suggest splitting if at least one of these conditions is met:**

   - **Too many changes:** The implementation would touch a large number of files across multiple areas, making the PR hard to review and risky to merge
   - **Distinct, independent concerns:** The ticket covers work in unrelated parts of the app (e.g., backend API + frontend UI + database migration) that can each be delivered and tested independently
   - **Mixed types of work:** The ticket combines fundamentally different types of changes (e.g., a refactor that is a prerequisite for a feature, or a bug fix bundled with a new capability)
   - **Sequential dependencies:** Part of the work must be merged first before the rest can begin (e.g., a shared utility or data model change that other parts depend on)

   **If splitting is warranted**, propose a split to the developer using `AskUserQuestion`:

   > This ticket appears large enough to benefit from being split into smaller, independently reviewable PRs.
   >
   > **Proposed split:**
   > 1. **<Short title>** — <What this chunk covers and why it's independent>
   > 2. **<Short title>** — <What this chunk covers>
   > 3. ...
   >
   > Would you like to split this ticket?

   - **"Yes — split"**: Use the Atlassian CLI to create sub-tasks under the current ticket for each chunk. Then proceed with only the **first chunk** for this session — the remaining chunks will be addressed in future sessions.
     ```bash
     acli jira workitem create --from-json <temp-file.json> --json
     ```
     Each sub-task payload should include:
     ```json
     {
       "project": "<project-key>",
       "type": "Sub-task",
       "summary": "<chunk title>",
       "parent": "<JIRA-ID>",
       "description": { ... ADF description of the chunk scope ... }
     }
     ```
     After creating the sub-tasks, inform the developer which chunk will be addressed now and list the created sub-task IDs.
   - **"No — keep as one"**: Proceed with the full ticket as a single PR.

   **If splitting is NOT warranted** (the ticket is small, focused, or only touches one area), skip this step silently — do not mention splitting at all.

8. **Maintain the epic lore file:**

   Before spawning the PO, check whether the current ticket belongs to a parent epic and maintain a lore file that captures accumulated context about the epic and its child tickets.

   **a) Identify the parent epic:**
   - From the ticket fields fetched in step 3, look for the parent epic link (e.g., the `Epic Link` field, `parent` field, or any field that references an epic).
   - If the ticket has a parent epic, fetch the epic using the Atlassian CLI to get its summary, description, and acceptance criteria:
     ```bash
     acli jira workitem view <EPIC-KEY> --fields summary,description,acceptance-criteria --json
     ```
   - If the ticket has no parent epic, skip this step entirely.

   **b) Check for an existing lore file:**
   - Look for a `lore/` directory at the root of the project.
   - Check if a lore file already exists for this epic. The file should be named after the epic key: `lore/<EPIC-KEY>.md` (e.g., `lore/PROJ-42.md`).

   **c) Create or update the lore file:**
   - **If no `lore/` directory exists**, create it.
   - **If no lore file exists for this epic**, create `lore/<EPIC-KEY>.md` with the following structure:
     ```markdown
     # <EPIC-KEY>: <Epic Summary>

     ## Epic Description
     <Epic description and acceptance criteria from the epic ticket>

     ## Tickets

     ### <JIRA-ID>: <Ticket Summary>
     - **Type:** <issue-type> | **Priority:** <priority>
     - **Description:** <Brief summary of the ticket>
     - **Acceptance Criteria:** <Key acceptance criteria>
     ```
   - **If a lore file already exists for this epic**, append a new entry under the `## Tickets` section for the current ticket:
     ```markdown
     ### <JIRA-ID>: <Ticket Summary>
     - **Type:** <issue-type> | **Priority:** <priority>
     - **Description:** <Brief summary of the ticket>
     - **Acceptance Criteria:** <Key acceptance criteria>
     ```
   - The lore file serves as a living document that builds context as tickets in the epic are worked on. Each ticket entry should be concise but capture enough detail to understand the ticket's purpose within the broader epic.

## Phase 2 — Product Owner: Requirements & Acceptance Criteria

9. **Spawn the Product Owner agent:**

   Use the `Task` tool to spawn a PO agent. This agent is responsible for writing requirements and acceptance criteria based on all the context gathered in Phase 1. The PO agent does NOT implement anything — it only produces a requirements document.

   **a) Prepare the PO prompt:**
   - Pass the PO agent ALL context gathered so far:
     - The full JIRA ticket content (summary, description, all fields, comments)
     - The downloaded attachment file paths from step 3 (so the PO can read images for visual context and text files for data/requirements)
     - Figma design data (if any was retrieved)
     - The conventional commit prefix determined in step 5
     - The codebase analysis from step 6 (relevant files, patterns, conventions, test setup)
     - The epic lore file content (if any)
   - Instruct the PO agent to produce a requirements document with the following structure:

   ```
   ## Ticket: <JIRA-ID>
   **<Summary>**
   Type: <issue-type> | Priority: <priority> | Commit prefix: <conventional-commit-prefix>

   ### Understanding
   <Brief summary of what the ticket is asking for, synthesized from the description, comments, and Figma designs. Call out any ambiguities or conflicting information.>

   ### Requirements
   1. <Requirement 1 — clear, testable statement of what the implementation must do>
   2. <Requirement 2>
   3. ...

   ### Acceptance Criteria
   - [ ] <Criterion 1 — specific, verifiable condition that must be true when done>
   - [ ] <Criterion 2>
   - [ ] ...

   ### Design Needs
   - <Whether this ticket requires design work: Yes / No>
   - <If yes, what aspects need design: UI layout, component design, interaction patterns, etc.>
   - <If Figma designs are provided, note which aspects are already covered and which need further design work>

   ### Implementation Plan
   1. <Step 1 — what to do and which files to touch>
   2. <Step 2>
   3. ...

   ### Files to Modify
   - `path/to/file.ts` — <what changes are needed>
   - `path/to/other.ts` — <what changes are needed>

   ### New Files
   - `path/to/new-file.ts` — <purpose>
   (or "None" if no new files are needed)

   ### Unit Tests
   - <Which unit test files to update or create>
   - <What scenarios to cover>

   ### E2E Tests
   - <Which e2e test files to update or create>
   - <User flows to cover: describe each flow as a sequence of actions and expected outcomes>
   - <Authentication requirements for the test scenarios>
   (or "None — changes are not user-facing" if e2e tests are not applicable)

   ### Risks / Open Questions
   - <Any uncertainties, assumptions, or things to clarify with the team>
   ```

   **b) E2E test planning guidelines (include in the PO prompt):**
   - Include e2e tests for any user-facing changes: new pages, new UI flows, modified interactions, form submissions, navigation changes, etc.
   - Follow the project's existing e2e conventions: file naming, directory structure, authentication approach, helper utilities, and assertion patterns
   - Each e2e test should cover a complete user flow (e.g., "navigate to settings, change profile name, save, verify success toast and updated name")
   - For bug fixes, add an e2e test that reproduces the original bug scenario and verifies it is resolved
   - If the project has no e2e test setup, note this and propose setting one up as part of the implementation
   - Skip e2e tests only for non-user-facing changes (e.g., pure refactors with no behavior change, CI config, build tooling)

   **c) Wait for the PO agent to complete** and collect its requirements document.

10. **Present requirements to the developer for approval:**

   Display the PO's requirements document to the developer and use `AskUserQuestion` to ask for confirmation:
   > The Product Owner has prepared the following requirements and acceptance criteria. Would you like to proceed?

   - **Approve** — requirements are accepted, proceed to Phase 3
   - **Request changes** — the developer provides feedback on what to adjust
   - **Reject** — stop the skill execution entirely

   **If "Request changes":**
   - Use `AskUserQuestion` to collect the developer's feedback
   - Re-spawn the PO agent with the original context plus the developer's feedback, asking it to revise the requirements
   - Present the revised requirements again for approval
   - Repeat until the developer approves or rejects

   **Do NOT proceed to Phase 3 until the developer explicitly approves.**

## Phase 3 — Implementation Team (TDD)

The team follows a strict **Test-Driven Development** workflow: tests are proposed and approved before any code is written, then implemented so they fail (red), and only then is the production code written to make them pass (green).

11. **Determine team composition:**

    Based on the approved requirements, decide which agents to spawn. The team always includes test authors and developers, but designers are conditional.

    **a) Designers — conditional:**
    - If the requirements' "Design Needs" section says **No**: skip designers entirely
    - If the requirements say **Yes** and Figma designs were provided (step 4): spawn **1 designer** agent
    - If the requirements say **Yes** and no Figma designs are available: spawn **2 designer** agents

    **b) Test authors:** always spawn **1–2 test author** agents (they write the tests before any production code exists)

    **c) Developers:** always spawn **2–3 developer** agents (they write production code to make the tests pass)

12. **Spawn designer agents (if needed):**

    If designers are needed, spawn them FIRST and wait for them to complete before proceeding to the test plan.

    **If 1 designer (design assets provided):**
    - Spawn 1 designer agent using the `Task` tool
    - The designer's job is to:
      - Analyze the PNG/SVG design assets provided by the developer in step 4
      - Map visual components in the designs to existing codebase components
      - Produce a design implementation guide: which components to use, spacing, colors, typography, responsive behavior, interaction states
      - Identify any gaps between the design assets and the requirements
    - Pass the agent: the approved requirements, the design asset file paths (so the agent can read/view them), and the codebase analysis (existing components, design system, styling patterns)

    **If 2 designers (no Figma):**
    - Spawn 2 designer agents in parallel using the `Task` tool with `run_in_background: true`
    - **Designer 1 — Research:** Explore the existing codebase for design patterns, component libraries, design tokens, and styling conventions. Document the design system already in use.
    - **Designer 2 — Propose:** Based on the requirements and the existing design patterns (share Designer 1's findings once available), propose a UI/UX approach: component structure, layout, interactions, and visual design decisions.
    - Wait for both to complete and consolidate their output into a design guide for the developers.

    **Pass the design guide to subsequent agents** as additional context.

13. **Propose the test plan:**

    Spawn 1 test planner agent using the `Task` tool. This agent does NOT write test code — it produces a complete list of tests that verify the expected behavior.

    **a) Prompt the test planner agent with:**
    - The full approved requirements and acceptance criteria
    - The implementation plan (files to modify, new files, expected behavior)
    - The codebase analysis (existing test files, test framework, conventions, directory structure)
    - The downloaded attachment file paths from step 3 (so the planner can reference screenshots, data files, or logs when designing test scenarios)
    - The design guide (if designers produced one)
    - The epic lore file content (if any) — so the planner knows what sibling tickets exist and what behavior is planned for future tasks

    **b) The test planner must produce a structured test plan:**

    ```
    ## Test Plan

    ### Unit Tests

    #### <test-file-path> (new / existing)
    - `<test name>` — <what it verifies, expected input → expected output>
    - `<test name>` — <what it verifies>
    ...

    #### <another-test-file-path> (new / existing)
    - `<test name>` — <what it verifies>
    ...

    ### E2E Tests

    #### <e2e-test-file-path> (new / existing)
    - `<test name>` — <user flow: step-by-step actions and expected outcomes>
    ...

    (or "None — changes are not user-facing" if e2e tests are not applicable)

    ### Coverage Summary
    - Total unit tests: <N>
    - Total e2e tests: <N>
    - Acceptance criteria covered: <list which criteria each test addresses>
    - Edge cases covered: <list edge cases>
    ```

    **c) Test plan guidelines:**
    - Every acceptance criterion must be covered by at least one test
    - Include edge cases, error paths, and boundary conditions
    - For bug fixes, include a test that reproduces the original bug
    - Follow the project's existing test naming conventions and file structure
    - Unit tests should be focused and test one behavior each
    - E2E tests should cover complete user flows
    - Specify which existing test files need updates (not just new tests)
    - **Localization:** Never assert against a translated/localized string (e.g., `"Submit"`, `"Enregistrer"`). Always assert against the translation key (e.g., `"common.submit"`) so tests do not break when translations change or when running in a different locale
    - **No intermediate-state tests:** Do not write tests that assert on a temporary state that only exists because a later task hasn't been implemented yet. Tests must verify behavior that is correct in the final state of the epic, not just the current task. Use the epic lore and sibling tickets to understand the full picture. For example, if an epic creates a button with label "Hello" and it is split into task A ("Create the button") and task B ("Add the label"), task A must NOT include a test asserting the button has no text — that assertion would break when task B is implemented. Instead, task A should test what it adds (the button exists, it is clickable, etc.) and leave the label test for task B.

14. **Present the test plan to the developer for review:**

    Display the test planner's complete test plan to the developer and use `AskUserQuestion`:

    > The team has prepared the following test plan. Please review the proposed tests.
    > Would you like to proceed with these tests?

    - **Approve** — test plan is accepted, proceed to step 15
    - **Request changes** — the developer provides feedback on what to add, remove, or modify
    - **Reject** — stop the skill execution entirely

    **If "Request changes":**
    - Use `AskUserQuestion` to collect the developer's feedback
    - Re-spawn the test planner agent with the original context plus the developer's feedback, asking it to revise the test plan
    - Present the revised test plan again for approval
    - Repeat until the developer approves or rejects

    **Do NOT proceed to step 15 until the developer explicitly approves the test plan.**

15. **Implement tests (TDD red phase):**

    Spawn 1–2 test author agents using the `Task` tool with `run_in_background: true`. These agents write the actual test code based on the approved test plan. No production code is written at this stage.

    **a) Prompt each test author agent with:**
    - The approved test plan (the exact list of tests to implement)
    - The full approved requirements and acceptance criteria
    - The project's test setup, conventions, existing test files, and helper utilities
    - The downloaded attachment file paths from step 3 (test authors may need screenshots for visual regression tests or data files for test fixtures)
    - The design guide (if designers produced one)
    - Explicit instruction: **write only test code — do NOT write or modify any production code**
    - For unit tests: write tests that import the modules/functions that will be created or modified, and assert the expected behavior
    - For e2e tests: write tests that perform user actions and assert expected outcomes
    - **Localization:** Never assert against translated/localized strings. Always assert against the translation key so tests are locale-independent and don't break when translations change

    **b) Partition test work across agents:**
    - By test type: one agent handles unit tests, another handles e2e tests
    - Or by feature area: each agent handles all tests (unit + e2e) for a specific area
    - For simple tickets, 1 test author agent is sufficient

    **c) Wait for all test author agents to complete.**

    **d) Verify tests are correctly written:**
    - Run the tests to confirm they fail for the expected reasons (missing implementations, not syntax errors or import failures that indicate broken test code)
    - If tests fail due to test code errors (syntax, wrong imports, incorrect setup), fix the test code before proceeding
    - The goal is: tests are syntactically correct and structurally sound, but fail because the production code they test doesn't exist or doesn't have the expected behavior yet

16. **Implement production code (TDD green phase):**

    Spawn 2–3 developer agents using the `Task` tool with `run_in_background: true`. Their sole objective is to write the production code that makes all the previously written tests pass.

    **a) Partition the work:**
    - Analyze the approved implementation plan and group steps by independence — steps that touch different files or non-overlapping code regions can run in parallel
    - Common partitioning strategies:
      - By feature area (e.g., one agent does the API changes, another does the UI)
      - By layer (e.g., one agent does the backend, another does the frontend)
      - By file group (e.g., one agent modifies existing files, another creates new files)
    - For simple tickets where parallelization isn't beneficial (e.g., a single-file change), 2 agents is fine — one implements, the other reviews and assists
    - If steps have dependencies (e.g., one change depends on another being written first), note this and have the dependent agent wait

    **b) Prompt each developer agent with:**
    - The full approved requirements and acceptance criteria
    - The test files written in step 15 (so developers can see exactly what the tests expect)
    - Their specific assigned steps from the implementation plan
    - The relevant file paths and what changes are needed
    - The coding conventions and patterns observed in the codebase (from step 6)
    - The downloaded attachment file paths from step 3 (developers may need screenshots for UI reference or data files as implementation context)
    - The design guide (if designers produced one)
    - Instructions to follow existing project patterns and not introduce new dependencies or abstractions unless specified in the plan
    - Explicit instruction: **do NOT modify any test files — only write production code to make the existing tests pass**

    **c) Wait for all developer agents to complete.**

    **d) Merge and verify:**
    - Check for conflicts between agents' changes (two agents modifying the same file)
    - If conflicts exist, resolve them by reading both agents' changes and merging intelligently
    - Run a quick sanity check: ensure the codebase compiles/lints after all changes are applied

17. **Verify all tests pass:**

    Run the full test suite (unit + e2e if applicable) to confirm everything passes.

    **a)** If tests fail, analyze the failures:
    - If a test fails because the production code is incorrect, spawn 1 additional developer agent to fix the production code (not the tests — the tests define the expected behavior)
    - If a test fails because of a genuine test defect (e.g., flaky assertion, incorrect setup that doesn't match the approved test plan), fix the test code

    **b)** If tests still fail after the fix attempt, report the remaining failures to the developer

    **c)** Ensure existing tests (that were not part of this change) still pass — no regressions

## Phase 4 — Suggest JIRA Ticket Updates

18. **Suggest ticket edits based on requirements and acceptance criteria:**

    After the team finishes, suggest improvements to the original JIRA ticket based on the requirements and acceptance criteria written during this skill's execution.

    **a) Analyze the gap:**
    - Re-read the original ticket description (from step 3)
    - Compare it against the PO's approved requirements and acceptance criteria (from step 9)
    - Identify what is missing from the ticket:
      - Acceptance criteria that were written by the PO but aren't in the original ticket
      - Requirements that were clarified or expanded during the PO phase
      - Design decisions made by the designers (if applicable)
      - Technical notes on the approach taken

    **b) Draft an improved description:**
    - Write a revised ticket description that incorporates the requirements and acceptance criteria
    - Preserve any useful original content (context, background, links, references)
    - Add or improve:
      - **Clear problem statement** or feature rationale
      - **Acceptance criteria** from the PO's document
      - **Technical notes** on the approach taken (briefly — just enough for future readers)
      - **Files/areas affected** (high-level, e.g., "Authentication module", "Settings page")
    - Keep the tone consistent with existing ticket descriptions in the project

    **c) Present to the developer:**
    - Show the proposed description in a clear before/after format:
      ```
      ## Suggested Ticket Description Update

      ### Current Description
      > <original description, or "(empty)" if there was none>

      ### Proposed Description
      <new description>

      ### What changed
      - <bullet list of key differences>
      ```
    - Use `AskUserQuestion` to ask the developer:
      > Would you like to update the JIRA ticket description with the proposed improvements?
    - Options: **Yes — update the ticket**, **No — skip**

    **d) Update the ticket (if approved):**
    - If the developer approves, write the description as an ADF JSON payload and use `--from-json` to update (see [ADF Format Reference](#adf-format-reference) below):
      ```bash
      acli jira workitem edit --from-json <temp-file.json> --yes
      ```
      The JSON file must contain the full edit payload with the description as an ADF object:
      ```json
      {
        "issues": ["<JIRA-ID>"],
        "description": {
          "version": 1,
          "type": "doc",
          "content": [ ... ADF nodes ... ]
        }
      }
      ```
    - Confirm the update was successful:
      ```
      Ticket <JIRA-ID> description updated.
      ```
    - If the update fails, show the error and provide the proposed description as copyable text so the developer can update it manually

19. **Final report:**

    Present a comprehensive summary to the developer:

    ```
    ## Ticket Complete: <JIRA-ID>
    **<Summary>**

    ### Team
    - PO: requirements and acceptance criteria written
    - Designers: <N> (or "None — no design work needed")
    - Test authors: <N> (wrote tests before implementation)
    - Developers: <N> (wrote production code to pass tests)

    ### Implementation
    - Files modified: <N>
    - Files added: <N>
    - Lines changed: +<additions> / -<deletions>

    ### Tests
    - Unit tests: <N> passing
    - E2E tests: <N> passing (or "N/A")
    - Test fixes needed: <yes/no — how many rounds>

    ### Acceptance Criteria
    - [x] <Criterion 1>
    - [x] <Criterion 2>
    - ...

    ### JIRA Ticket
    - Description updated: <yes/no>

    ### Next Steps
    - <Any remaining manual steps, e.g., "Run database migration", "Update env vars">
    - <Any issues that need human judgment>
    ```

20. **Handle edge cases:**
    - If the ticket description is empty, note it and the PO should base requirements on the summary and comments only
    - If there are no comments, skip that section in the analysis
    - If the codebase exploration reveals the ticket may already be addressed, inform the developer before spawning the PO
    - If the ticket is too vague, the PO should list what is understood and flag open questions for the developer to answer during the approval step
    - If the project has no test framework, note it and skip the TDD phases (steps 13–17) — spawn developers directly to implement the code
    - If designer agents produce conflicting recommendations, present both to the developer and let them choose
    - If developer agents produce conflicting changes to the same file, resolve the conflicts before running the test suite
    - If tests fail after the green phase and fixes loop (fix -> fail -> fix -> fail), stop after 2 attempts and report remaining failures to the developer
    - If the test planner produces tests that cannot be written without production code scaffolding (e.g., type definitions, interfaces), note this and have test authors create minimal type stubs — not implementations

---

## ADF Format Reference

JIRA does **not** render Markdown. Descriptions must use **Atlassian Document Format (ADF)** — a JSON-based document format. The `--description-file` flag treats file content as a plain text string, so it cannot be used for rich descriptions. Use `--from-json` instead.

**Important:** `--from-json` expects a structured JSON file with the full edit payload. The `description` field must be an ADF object, not a string. You can run `acli jira workitem edit --generate-json` to see the expected schema.

**Edit payload format (`--from-json`):**

```json
{
  "issues": ["<JIRA-ID>"],
  "description": {
    "version": 1,
    "type": "doc",
    "content": [
      {
        "type": "heading",
        "attrs": { "level": 2 },
        "content": [{ "type": "text", "text": "Description" }]
      },
      {
        "type": "paragraph",
        "content": [{ "type": "text", "text": "What was implemented." }]
      },
      {
        "type": "heading",
        "attrs": { "level": 2 },
        "content": [{ "type": "text", "text": "Acceptance Criteria" }]
      },
      {
        "type": "taskList",
        "attrs": { "localId": "ac-list" },
        "content": [
          {
            "type": "taskItem",
            "attrs": { "localId": "ac-1", "state": "TODO" },
            "content": [{ "type": "text", "text": "First criterion" }]
          }
        ]
      }
    ]
  }
}
```

**Common ADF node types:**

| Markdown | ADF `type` | Notes |
|----------|-----------|-------|
| `## Heading` | `heading` with `attrs.level` | Levels 1–6 |
| Plain text | `paragraph` with `text` children | |
| `**bold**` | `text` with `marks: [{"type": "strong"}]` | |
| `*italic*` | `text` with `marks: [{"type": "em"}]` | |
| `- item` | `bulletList` > `listItem` > `paragraph` | |
| `1. item` | `orderedList` > `listItem` > `paragraph` | |
| `- [ ] task` | `taskList` > `taskItem` (state: `TODO`/`DONE`) | |
| `` `code` `` | `text` with `marks: [{"type": "code"}]` | Inline code |
| Code block | `codeBlock` with `attrs.language` | |
| `---` | `rule` | Horizontal rule |
| `[link](url)` | `text` with `marks: [{"type": "link", "attrs": {"href": "url"}}]` | |
