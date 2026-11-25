---
name: hr-workshop-mvp-flow
description: Use when an HR workshop student kicks off the workshop, uploads a filled brainstorm worksheet (any filename), pastes or attaches an idea document, describes an internal tool, or wants to go from a rough idea to PRD, build slice (今日切片), HTML prototype, a running local app, and local run. This is the generic student entry for every group. Do not require a Group 6 / Group 4 wrapper.
---

# HR Workshop MVP Flow

## Purpose

This is the **student kickoff skill for every group**. Guide non-technical HR workshop students from their own idea (usually an uploaded filled brainstorm sheet, any filename) to PRD, a confirmed build slice, an HTML prototype, and one working path running in their own browser.

The MVP is what the product should eventually be. The **Build Slice** is what gets built in this session. Every build stage follows the slice, not the MVP list.

Do not load Group 6 Talent Mapping, Group 4 Pulse Survey, or any other wrapper defaults unless the student's idea already is that product, or the instructor explicitly asks to use an example wrapper.

Keep student-facing output simple, practical, and low-jargon.

Use this skill when the user mentions:
- start / kick off the HR workshop
- brainstorm sheet, PRD worksheet, uploaded/filled worksheet (any name)
- idea document, brief, one-pager, pasted requirements
- HR workshop, L&D workshop, internal HR tool
- rough idea to MVP, PRD, build slice, HTML prototype, Next.js, Supabase, Vercel

## Core Rules

- This skill is enough. Students do not need `grp6-talent-mapping-mvp-flow` or another group wrapper.
- Follow the student's idea document or filled worksheet. Do not steer them into a standard Talent Mapping / Pulse Survey / Attendance MVP if their document is a different tool.
- Filename does not matter. Read whatever they attach or paste. Do not require `prd_brainstorm_sheet.md` or `day3 teaching materials/`.
- If the student already uploaded a filled brainstorm sheet, extract and confirm it. Do not refill it from scratch or re-ask questions they already answered.
- Move one stage at a time. After every stage, ask: "Do you want to proceed to the next step?"
- Do not skip confirmation gates. The student must confirm the MVP functions before PRD generation, and the Build Slice before any build stage.
- Keep the MVP to a maximum of 5 functions. If the idea has more, group or defer functions.
- The 5-function cap limits how many functions exist. It does not limit what gets built. The Build Slice does that.
- Build stages (6 and 7) implement the Build Slice only — never the full MVP function list.
- Default slice ceiling: one user, one happy path, synthetic data, no login, no database.
- If the student asks for something outside the slice during a build stage, do not add it. Write it under "Not In This Build" and continue.
- Prefer plain language over technical terms. If a technical term is necessary, explain it in one short sentence.
- Do not automatically connect Supabase or Vercel. Build or plan the app, then provide step-by-step connection guidance.
- Supabase and Vercel are **handoff** defaults (Stage 8), not build defaults. Inside a session the persistence ceiling is file import/export.
- When generating PRDs, use the `prd-writer` skill if available.
- When the student confirms an HTML or Next.js plan, or says the prototype will not run, follow `workshop-local-run` before `npm` or opening localhost. Pass `mode` (`preflight` or `repair`) and `kind` (`html` or `nextjs`). Do not ask the student to run terminal commands. Detect `projectDir` and `successPath` from this project; do not assume `talent-mapping-next` or `/login`.
- Do not overwhelm the student with architecture details unless they ask.

## Stage Flow

### Stage 1: Collect Input

Students usually start by **uploading a filled brainstorm sheet**. Treat any attached, pasted, or pointed-to file as the source. Ignore the filename.

**Read that first.** Do not search for `day3 teaching materials/prd_brainstorm_sheet.md`. Do not ask them to rename the file.

Decide the input type from **content**, not the name:

| What they gave you | Treat it as | Next |
|---|---|---|
| Covers pain/problem, desired result, and functions (headings may differ; Word/PDF/Markdown/image are all OK) | Filled brainstorm worksheet | Summarize, then Stage 2 Path A. Skip blank filling. |
| A brief, one-pager, or rough idea without a function list | Idea document | Summarize, then Stage 2 Path B |
| Nothing | Missing input | Ask for the sheet or a short idea |

If nothing was provided, ask:

```text
Please upload your filled brainstorm sheet (any filename is fine), or describe your HR tool in 1-3 sentences.
Who uses it, what problem does it solve, and what result should it produce?
```

Do not ask them to rewrite the document in 1-3 sentences if those answers are already in it.

If the idea is still vague after the document, ask at most 2 follow-up questions:
- Who is the main user: HR, manager, employee, leadership, or candidate?
- What painful manual process should this replace?

Then summarize **their** product, not a workshop example:

```markdown
## My Understanding
This tool is for [user group]. It helps them [main job] so that [business result].
```

If it was a **filled worksheet**, end with:

```text
Is this correct? If yes, I will map your sheet and we can confirm the MVP functions.
```

If it was only a **rough idea**, end with:

```text
Is this correct? Do you want to proceed to the worksheet step?
```

### Stage 2: Worksheet — Extract or Fill

Use this structure in chat. Do not depend on a local teaching-file path. Do not edit the student's file unless they ask.

- Part 1: Pain point
- Part 2: Ideal result
- Part 3: Function list
- Part 4: Data
- Part 5: Constraints
- Part 6: Flow
- Final check

#### Path A — Student uploaded a filled sheet (default)

1. Map **their** answers onto Parts 1–6. Keep their wording. Headings do not need to match.
2. Do not write a new worksheet from scratch. Do not re-ask questions they already answered.
3. Mark gaps as `Missing:` and inferences as `Assumption:`.
4. For Part 3, split into four tiers: Must-have MVP (cap 5) / Today's Build Slice (1–2, chosen from must-have) / Nice to have / Future. If they listed more, group or defer — do not invent extra functions.
5. Output the mapped worksheet in chat.

#### Path B — No filled sheet, only a rough idea

Fill the same Parts 1–6 in chat from the Stage 1 idea. Short point form. Mark `Assumption:` clearly. Cap must-have MVP functions at 5, and mark which 1–2 are the candidate Build Slice.

If a local teaching copy of the blank sheet exists, you may use it only as a layout reference. Never require the student to have that file or that filename.

Both paths end with:

```text
Please confirm the MVP functions above. We should keep maximum 5.
Do you want to keep, remove, or combine any function before we pick today's build slice?
```

### Stage 3: Confirm MVP Functions

Present only the MVP function shortlist:

```markdown
## Proposed MVP Functions
1. [Function] - [simple purpose]
2. [Function] - [simple purpose]
3. [Function] - [simple purpose]
4. [Function] - [simple purpose]
5. [Function] - [simple purpose]

## Not In MVP
- [Future function]
- [Future function]

Please confirm: are these the final MVP functions?
```

Do not move on until the user confirms.

### Stage 3B: Confirm the Build Slice

This is a required gate. The MVP list says what the product should become. The slice says what we build today.

Propose one slice, drawn from the confirmed must-have functions:

```markdown
## Build Slice — what we build today
- Slice user: [exactly one role]
- Slice path: [step] → [step] → [step] → [result]   (3–5 steps, one happy path)
- Slice data: synthetic only, [N] example rows. No real employee or customer records.
- Done when: [one test case anyone in the room can repeat]
- One edge case handled: [empty input / missing field / duplicate row]

## Not In This Build
- Login and permissions
- Saving to a database
- Other roles' screens
- Export, email, integrations
- [anything else the student named]

Please confirm this slice. Everything in "Not In This Build" stays a decision we wrote down, not a gap we forgot.
```

Before proposing, check the slice against the ceiling:

- More than one slice user → cut to one.
- More than 5 steps in the path → cut steps, do not merge them into one vague step.
- Needs real company data → replace with synthetic rows and say so.
- Needs login before the path works → move login out and assume the slice user.

Do not move to PRD until the student confirms the slice. Keep the confirmed slice card visible and quote it at the start of Stages 5, 6, and 7.

### Stage 4: Create Concept PRD With prd-writer

Use `prd-writer` mode A. Create the first version: product concept document.

Student-facing output should include:
- Product name
- One-sentence positioning
- Product format
- Target users
- Product value
- Core MVP function directions
- Build slice for this session (one line, quoted from Stage 3B)
- Not in scope
- Open questions

For product format:
- Recommend Web App by default for internal HR tools.
- Explain simply: "A web app works in the browser and is easiest for HR/admin dashboards."

End with:

```text
Does this product direction look right? If yes, we can move to the detailed PRD.
```

### Stage 5: Detailed PRD — Slice Scoped

Only after concept PRD confirmation, create the detailed implementation PRD. **Write it in detail for the Build Slice only.** The remaining MVP functions get one line each as later phases. Do not spend the student's time speccing screens and permissions nobody will build today.

Include:
- Product overview
- The slice user and the one scenario
- The slice path, step by step
- Wireframe in ASCII — the slice screen only
- Detailed description of the slice functions
- Data needed for the slice, with the synthetic example rows
- Done-when test case and the one edge case
- Simple copywriting examples for the slice screen
- Later phases — remaining must-have MVP functions, one line each, no detail
- Remaining questions

Permissions in this document are one line: no login in this build; the slice user is assumed.

Keep the language non-technical. Explain saving and security as:
- "Data needs to be saved safely."
- "In this build the data is fake, so nothing sensitive can leak."

End with:

```text
Please review this. It describes today's slice in full, and lists the rest as later phases.
If it looks right, we can plan the HTML prototype.
```

### Stage 6: Plan HTML Prototype

Create a simple development plan for a single-file HTML prototype. Open the plan by quoting the confirmed slice card, so the scope is on screen while building.

The prototype plan should include:
- Goal — the slice done-when sentence
- Scope — the slice path only
- The one screen the slice user needs
- Mock data — the synthetic rows named in the slice
- The slice path as clicks
- Interactions
- Build order
- Testing checklist — the done-when case plus the one edge case

Default prototype requirements:
- Single HTML file
- Embedded CSS and JavaScript
- Mock data in JavaScript arrays
- One screen for the slice user
- No real login
- No role switcher, unless the confirmed slice explicitly spans two users
- No database
- No Supabase or Vercel yet

Anything outside the slice does not get built. If a button is needed for the screen to make sense, render it visibly disabled and list it under "Not In This Build" — do not implement it.

End with:

```text
Do you want to build this HTML prototype now, or adjust the prototype plan first?
```

If the student chooses to build now: follow `workshop-local-run` with `mode=preflight` and `kind=html` **before** writing the HTML file. If the machine is not ready, finish that skill first. Then build. If later they cannot open the HTML, follow `workshop-local-run` with `mode=repair` and `kind=html`.

### Stage 7: Plan the Running App

Two modes. **Slice mode is the default inside a workshop session.** Only use Full MVP mode when the student explicitly asks for it and there is time outside the session.

#### Slice mode (default)

The goal is the same slice, now opened at a local address instead of a file. Nothing new gets added here.

```markdown
## What changes from prototype to a running app
- Same slice screen — opened at a local address instead of a file.
- Demo data stays synthetic.
- "Save" means export and import a file, not a database.
- Login, permissions, and other roles stay out of this build.
```

Phase plan:
1. Set up the app shell
2. Move the slice screen in — do not regenerate it from the PRD
3. Make the slice path work at the local address
4. Test: the done-when case, the one edge case, and a refresh test
5. Write "Not In This Build" into the project folder

Persistence ceiling in this mode is file import/export. No Supabase, no login, no deployment.

Do not call the app done until all three checks pass: the done-when case, the one edge case, and one other person walking the slice path without the builder touching the keyboard.

#### Full MVP mode

Only on explicit request, outside a session.

Default stack: Next.js, Supabase for database and login, Vercel for deployment.

1. Set up Next.js app
2. Set up Supabase database and login
3. Build pages from prototype
4. Add form save/submit flows
5. Add role permissions
6. Add export
7. Test
8. Deploy to Vercel

End with:

```text
Do you want to build the running slice now, or review the plan first?
```

If the student chooses to implement now, in either mode: follow `workshop-local-run` with `mode=preflight` and `kind=nextjs` **before** `npx create-next-app`, `npm install`, or `npm run dev`. Pass `projectDir`, and set `successPath` to the slice screen. If later they cannot open localhost, follow `workshop-local-run` with `mode=repair` and `kind=nextjs`.

### Stage 8: Post-Build Missing Items

After the app is completed, separate two different kinds of "missing". Students lose confidence when a scope decision they made on purpose is presented back to them as an unfinished item.

Use this format:

```markdown
## What Is Completed
- The slice path works at a local address: [slice path]
- Done-when case passes: [test case]
- Edge case handled: [edge case]

## Deliberately Not In This Build
(These were decisions, not gaps. Quoted from the slice card.)
- [item]
- [item]

## What Is Still Missing Before Real Use
- Supabase project needs to be connected
- Vercel deployment needs to be connected
- Real users and roles need to be created
- Real employee data needs to be imported
- Company privacy/security review is needed
- Email notifications/reminders may still need setup
- Backup/export process should be agreed

## How To Connect Supabase
1. Create a Supabase account.
2. Create a new project.
3. Copy the project URL and anon key.
4. Add them to `.env.local`.
5. Run the database migration SQL.
6. Create test users.
7. Test login and role permissions.

## How To Deploy To Vercel
1. Push the app to GitHub.
2. Create a Vercel account.
3. Import the GitHub repository.
4. Add the same environment variables in Vercel.
5. Click Deploy.
6. Test the live URL.
```

Keep this as a checklist for non-technical HR users. The Supabase and Vercel steps are handoff reference, not homework for the session.

## Output Style

- Use English unless the student uses Chinese/Cantonese; then mirror their language.
- Use tables for worksheets and checklists.
- Avoid long technical explanations.
- Use labels like "Assumption" and "Decision needed".
- Always ask before proceeding to the next stage.

## Common Mistakes

- Do not produce a full technical build plan before MVP functions are confirmed.
- Do not include more than 5 MVP functions.
- Do not start a build stage before the Build Slice is confirmed in Stage 3B.
- Do not build beyond the confirmed slice, even if the student asks mid-build. Record it under "Not In This Build".
- Do not add a role switcher or login when the slice has one user.
- Do not run Stage 7 in Full MVP mode during a session.
- Do not add a database when file import/export satisfies the slice.
- Do not regenerate the screen from the PRD in Stage 7. Move the confirmed prototype in.
- Do not declare the running app done before the done-when case, the edge case, and a refresh test all pass.
- Do not list a deliberate slice decision as a missing item in Stage 8.
- Do not treat the HTML prototype as production.
- Do not claim Supabase/Vercel is connected unless actually configured.
- Do not bury the student in database schema unless they ask for developer details.
- Do not skip the "what is still missing" explanation after the app is completed.
- Do not tell the student to run `pwd`, `cd`, `npm install`, or `npm run dev`. Use `workshop-local-run`.
- Do not start HTML or Next.js implementation until `workshop-local-run` preflight has run for that stage.
- Do not start from Group 6 Talent Mapping (or any other group wrapper) when the student only kicked off this generic skill or pasted a different idea document.
- Do not require the filename `prd_brainstorm_sheet.md` or the path `day3 teaching materials/`.
- Do not refill a brainstorm sheet the student already uploaded. Extract, map, and confirm.
- Do not skip their uploaded functions and invent a new function list.
