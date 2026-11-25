---
name: flow-recorder
description: "Record browser workflows and generate autonomous skills from them. Use when user wants to automate a repetitive web task — submitting forms, navigating portals, filing reports, etc. Triggers: 'record flow', 'automate website', 'create browser skill'."
---

# Flow Recorder — create skills from browser workflows

You are a meta-skill. Your job is to walk the user through a routine web process once, record every step, and turn the recording into a standalone skill that can replay the process autonomously.

All browser interaction is done via the **agent-browser** skill. Before you begin, invoke the agent-browser skill to understand how to interact with the browser.

## Modes

This skill operates in two modes:

### 1. Record mode (default)

Record a new flow from scratch.

### 2. Update mode

User says "let's update flow X". You open the existing skill, walk through the steps with the user, and update whichever steps have changed.

---

## Workflow (record mode)

### Step 1. Gather information

Ask the user for:

1. **Flow name** — short slug (becomes the skill name). Examples: `submit-meters`, `file-complaint`, `create-experiment`.
2. **Site URL** — where to go.
3. **Auth type** — one of three:
   - **manual** — user authenticates themselves (corporate SSO, sensitive services). You open the site and wait.
   - **credentials** — user gives you a login and password and you enter them (public / low-sensitivity sites: utilities, municipal portals, forums). Hardcode the login and password directly into the generated skill — this is the user's deliberate choice for convenience.
   - **none** — no authentication needed.
4. **Short description** — what this flow does (one sentence).

### Step 2. Check availability

Verify the site is reachable:

```bash
curl -s -o /dev/null -w "%{http_code}" --max-time 10 <URL>
```

If unreachable — tell the user. They may need a VPN or the site may be down.

### Step 3. Open browser

Navigate to the site URL using the agent-browser skill.

### Step 4. Authentication

Depending on the type:

- **manual**: Tell the user:
  > I've opened [URL]. Please log in. When you're ready — type "done".

  Wait for confirmation. Do nothing until the user confirms.

- **credentials**: Ask the user for login and password. Then take a snapshot, find the login form fields, fill them in, and click sign-in. Record the auth steps in the flow log, and hardcode the login and password directly into the generated skill — so that on subsequent runs authentication happens automatically with no prompts.

- **none**: Skip this step.

### Step 5. Record the flow

Say:

> Great! Starting to record flow **[name]**. Tell me what to click — I'll do it and write it down.

Then work like this:

1. User says: "click the Create button" / "fill the Name field with Test" / "select A/B from the Type dropdown".
2. You take a snapshot, find the element using semantic locators, and perform the action.
3. **Record the step** in your internal log (see format below).
4. If the action succeeds — confirm briefly: "Done, clicked Create. What's next?"
5. If the element is not found or something went wrong — **stop and ask the user**. Do not guess.

#### Step recording format

Keep a step list in this format (this is your draft — the user doesn't see it):

```
Step 1: Click "Create Experiment" button in the navbar
  - find by: text "Create Experiment"
  - fallback: testid "create-experiment-btn"
  - action: click
  - expect: experiment creation form appears

Step 2: Fill "Experiment Name" field
  - find by: label "Experiment Name"
  - fallback: placeholder "Enter experiment name"
  - action: fill "{experiment_name}"
  - variable: experiment_name (asked at runtime)

Step 3: Select "A/B Test" from "Type" dropdown
  - find by: label "Type" → click, then text "A/B Test" → click
  - fallback: testid "type-select"
```

#### How to identify elements

When recording a step, use **semantic locators** in this priority order:

1. **Visible text** — most reliable, only changes on redesign
2. **Label** — for form fields
3. **Placeholder** — for inputs
4. **Test ID** — `data-testid`, set by developers, stable
5. **ARIA role** — semantic role matching
6. **Title / alt**
7. **CSS selector / HTML id** — last resort, only if stable

**Do NOT rely on:**
- CSS classes — often hashed at build time
- Snapshot ref numbers — they change on every render, never save them in the skill

#### Variables

When the user enters a specific value into a field (name, date, number), ask: "Will this value be the same every time, or should it be asked at runtime?"

- If the same — hardcode it.
- If it changes — make it a variable: `{variable_name}`. Remember the name and description.

### Step 6. Finish recording

When the user says "that's it" / "done" / "end of flow":

1. Show the user a brief summary of the recorded steps.
2. Ask: "All correct? Shall I generate the skill?"
3. After confirmation — generate the skill.

### Step 7. Generate the skill

Create the skill file from the template below at `~/.claude/skills/<flow-name>/SKILL.md`.

---

## Generated skill template

```markdown
---
name: <flow-name>
description: "<description>. Triggers: '<flow-name>', '<aliases>', '<keywords>'."
---

# <Flow title>

<Description: what this flow does.>

All browser interaction is done via the **agent-browser** skill.

## Site

- URL: <url>
- Auth: <manual/credentials/none>

## Variables

On launch, ask the user for:

| Variable | Description | Example |
|----------|-------------|---------|
| {var1}   | ...         | ...     |

## Steps

### 1. Check availability

Verify the site is reachable:
\`\`\`bash
curl -s -o /dev/null -w "%{http_code}" --max-time 10 <URL>
\`\`\`
If unreachable — tell the user (may need VPN).

### 2. Open browser

Open <URL> using the agent-browser skill.

### 3. Authentication
<!-- type: manual / credentials / none -->
<!-- manual: ask user to log in, wait for confirmation -->
<!-- credentials: fill login form with hardcoded credentials -->
<!-- none: skip -->

### 4-N. [Recorded steps]

For each step:
- Take a snapshot
- Verify anchor elements are in place (page title, navbar, key buttons)
- If everything looks familiar — proceed
- If something has changed — stop and ask the user

#### Step 4. <Description>
- Find by: <semantic locator — text / label / testid / role>
- Fallback: <alternative locator>
- Action: <click / fill / select / etc.>
- Expect: <what should happen after>

...

## Operating principles

- **Confidence**: if all elements are in place and you know what to do — act without asking unnecessary questions.
- **Caution**: if an element is missing, the page looks different, or you're unsure — STOP and ask the user.
- **This is production**: don't click randomly, don't guess. Better to ask than to break something.

## Changelog

- <date>: Initial version, recorded with the user.
```

---

## Workflow (update mode)

When the user says "update flow X" or "let's update <name>":

1. Read the existing skill from `~/.claude/skills/<flow-name>/SKILL.md`.
2. Show the user the step list: "Here are the current steps: 1... 2... 3... Shall we go through them in order?"
3. Open the browser, handle authentication.
4. Walk through the steps. At each step:
   - Take a snapshot.
   - If the element is in place — execute and say: "Step N done, same as before. Next?"
   - If the user says "this is different now" — record the new version of the step.
   - If the user says "there's a new step here" — insert it.
   - If the user says "this step is no longer needed" — remove it.
5. After all steps — update SKILL.md and append to the changelog.

---

## Important rules

1. **Never guess elements**. If you don't see the button — ask.
2. **Always take a snapshot before acting**. That's your eyes.
3. **Variables > hardcode**. If a value can change between runs — make it a variable.
4. **Log changes** in the "Changelog" section of the generated skill.
5. **One flow = one skill**. Don't mix multiple processes into a single skill.
6. **Ask after each flow**: "Record another flow?"
7. **Never save snapshot refs**. Always use semantic locators (text, label, testid, role).
