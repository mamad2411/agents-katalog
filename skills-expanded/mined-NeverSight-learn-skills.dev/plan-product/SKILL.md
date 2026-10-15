---
name: plan-product
description: Generate a step-by-step build plan for any product or feature. Each step is product-first and verifiable — the user can see the result in their browser or dashboard after every step. Use this when you know what you want to build and need a concrete plan before writing code.
---

# Plan Product

This skill generates a plan file that breaks any product or feature into buildable, verifiable steps. The plan file is named after the task (e.g., `feedback-board-plan.md`, `add-payments-plan.md`) and saved in the `docs/` folder.

## The user is non-technical

The person using this skill has never written code before. Every interaction — the plan itself, clarifying questions, error troubleshooting, brainstorming — must reflect this.

- **Talk about the product, not the technology.** Say "the list of feedback on the homepage" not "the Convex query in the page component." Say "the sign-in button" not "the AuthKit provider."
- **When asking for clarification,** ask about what they want the product to do, what behavior they expect, or what they're seeing on screen. Never ask them to inspect code, check a config file, or understand a stack trace.
- **When something breaks,** help them describe the problem in their own terms: what they clicked, what they expected, what they see instead. Then fix it. Don't explain the root cause unless they ask.
- **Never assume they know** what Convex, Next.js, WorkOS, shadcn, React, or any framework is. They know what their product does. That's the shared language.

## Skill integration

When generating the plan, reference the appropriate skills at each step so the agent knows which specialized knowledge to apply:

| Skill | When to reference |
|-------|-------------------|
| **setup-project** | Initial project bootstrapping (if the project isn't set up yet) |
| **frontend-design** | Any step that builds or styles UI |
| **web-design-guidelines** | Layout, accessibility, and responsive design decisions |
| **next-best-practices** | Page structure, routing, data fetching, and React patterns |
| **convex** / **convex-helpers-guide** | Any step that creates or modifies data, queries, or mutations |
| **workos** | Any step involving sign-in, sign-out, or user identity |
| **shadcn** | Any step that uses UI components |
| **deploy-project** | The final deployment step |

In each step's prompt, include a line like: "Reference the **[skill-name]** skill for best practices on this step." Only reference skills that are relevant to that specific step.

## When to use this skill

Use this skill when:
- You know what product you want to build
- You know the features it should have
- You want a step-by-step plan where every step produces something you can see and check

## What the user provides

The user describes:
1. **What they're building** — a short description of the product
2. **The features** — what the product should do, written as behaviors (not technical specs)
3. **The stack** — what tools/frameworks are already set up (check the project's `agent.md` or `package.json` if not stated)

## How to generate the plan

### Ordering principle: instant gratification

Order steps so the user sees results as early as possible. Do not organize by technical layer (schema → API → UI). Instead, organize by product surface — each step completes something the user can interact with.

**Good order:** Set up data + show it on a page (one step) → add another page → add auth → add a form → add a feature
**Bad order:** Set up schema → set up all queries → set up all mutations → build all pages → connect everything

### Each step must include

For every step in the plan, include exactly these sections:

#### What we're building
One sentence describing the product capability this step delivers. Write it as what the user will be able to do, not what the code does.

- Good: "Anyone can visit the site and see a list of all feedback that's been submitted."
- Bad: "Create a Convex query and a React component to fetch and render feedback items."

#### How data flows in this step
Describe what happens to data in this step using five concepts, written in plain, non-technical language. Only include the concepts that are relevant to this step — not all five will apply every time.

- **Storage** — where data is saved (e.g., "Feedback items are saved in the database so they don't disappear when you close the browser")
- **Security** — who can access it (e.g., "Anyone can see feedback, but only signed-in users can submit new items")
- **Processing** — what happens to it (e.g., "When you vote, the system checks if you already voted and either adds or removes your vote")
- **Transmission** — how it moves between systems (e.g., "New feedback appears on everyone's screen instantly without refreshing the page")
- **Presentation** — how the user sees it (e.g., "Each feedback item shows as a card with the title, a preview, vote count, and how long ago it was posted")

Keep descriptions conversational. Never mention database tables, API calls, components, or technical terms. The user should understand the data story of each step without knowing how software works.

#### What to tell the agent
A prompt the user can paste into their AI coding agent. This prompt must:

- Describe the feature in terms of **what it does and how it behaves**, not how to implement it
- Never mention file paths, function names, schema fields, or component names
- Be written so someone with no coding experience can read it and understand what it's asking for
- Reference the plan by its filename: "We're on Step N of docs/[plan-name].md. Read the plan first."
- End with: "When you're done, tell me how to check that it's working."

Example of a good prompt:
```
We're on Step 2 of docs/feedback-board-plan.md. Read the plan first.

Build the homepage of the feedback board. When someone visits the site, they should see a list of all the feedback that's been submitted. Each item should show the title, a short preview of the description, who submitted it, how many votes it has, and how long ago it was posted. Clicking on any item should take you to a page with the full details. Anyone should be able to see this page without signing in. Make it look clean and polished.

When you're done, tell me how to check that it's working.
```

Example of a bad prompt:
```
Create a Convex query called listFeedback in convex/feedback.ts that fetches all documents from the feedback table sorted by createdAt desc. Then create app/page.tsx with a React component that calls useQuery and renders each item using shadcn Card components with title, description substring(0,100), authorName, votes count, and relative time.
```

#### How to verify
Tell the user exactly what to look at and what should be true. Be specific:

- Which page to open (URL or where to click)
- What should appear on screen
- What to interact with (click, type, submit) and what should happen
- If checking the database: which dashboard page, which table, what rows/values to look for

Prefer browser verification over terminal/console verification. The user should be looking at the product, not at logs. Convex dashboard is acceptable for data verification.

#### If something goes wrong
A template for what to tell the agent if the step doesn't work. Keep it conversational — the user describes what they see (or don't see) and pastes any error.

Format: "I [did thing] but [expected result] didn't happen. Instead I see [what's actually there]. Here's the error if there is one: [paste]. Fix it."

### After the agent runs each step

The plan must instruct the user to validate after every step by running:

```bash
npx convex dev --once
```

This checks that the backend compiles. If it fails, fix the errors before moving on.

### The last step

The final step in the plan should always be deployment. It should:
- Push the latest code to GitHub
- Deploy to the hosting platform
- Verify the product works in production (not just locally)

## Output

### File naming

Name the plan file after the task it covers, using lowercase and hyphens. Save it in the `docs/` folder. Create the `docs/` folder if it doesn't exist.

Examples:
- Building the initial product → `docs/feedback-board-plan.md`
- Adding a payments feature → `docs/add-payments-plan.md`
- Redesigning the homepage → `docs/homepage-redesign-plan.md`

If the user doesn't specify a name, derive one from their description of what they're building.

### File format

The file should be scannable — use clear headings, numbered steps, and consistent formatting.

Do not include setup instructions in the plan. The project is already set up when this skill runs. Start with the first buildable feature.

## What NOT to do

- Do not write implementation code in the plan
- Do not specify file paths, function signatures, or schema definitions
- Do not organize steps by technical layer (all backend, then all frontend)
- Do not include steps that have no visible verification ("set up utilities", "create helpers")
- Do not combine multiple features into one step — each step should be independently verifiable
- Do not assume the user knows how to read code, terminal output, or browser DevTools — always give them something visual to check
