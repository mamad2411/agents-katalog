---
name: wm-needs
description: >
  Identify user needs for Wardley Mapping from prior research. Reads
  shared research and the project brief, proposes users and their needs,
  then facilitates negotiation with the client. Produces a markdown
  needs document that must be explicitly agreed before proceeding.
  Use after wm-research is complete and brief.agreed.md exists.
metadata:
  author: monkeypants
  version: "0.2"
  skillset: wardley-mapping
  stage: "2"
  freedom: medium
---

# User Needs Identification for Wardley Mapping

You are conducting the **needs identification phase** of a Wardley mapping
engagement. Your goal is to identify the users/stakeholders and their
needs, then reach agreement with the client.

## Prerequisites

Check that the project directory contains:
- `brief.agreed.md`

Check that the client workspace contains:
- `resources/index.md` and research sub-reports in `resources/`

If `brief.agreed.md` is missing, tell the user to run `wm-research` first.

The project path is `clients/{org}/projects/{project-slug}/`.

## Step 1: Analyse research

Read `brief.agreed.md` for the agreed scope.

Read `resources/index.md` and all sub-reports in `resources/`.

Identify:
- **User classes**: distinct groups of people or organisations who
  depend on or interact with the organisation being mapped. These
  become anchors in the eventual Wardley map.
- **Needs per user class**: what each user class requires from the
  organisation. These become the top-level components in the value chain.

Focus on **external users** first (customers, regulators, partners),
then consider significant **internal users** (operations teams, etc.)
only if they represent a distinct value chain.

## Step 2: Draft per user class

For each identified user class, write a draft to
`needs/drafts/{user-class-slug}.md` containing:

```markdown
# {User Class Name}

## Who they are

{One paragraph: role, relationship to the organisation, scale}

## Their needs

1. **{Need name}** — {What they need and why, from their perspective}
2. **{Need name}** — {description}

## Evidence

- From `resources/{file}`: "{relevant quote or finding}"
- From `resources/{file}`: "{relevant quote or finding}"

## Confidence

{High/Medium/Low} — {reasoning about evidence quality for this user class}
```

Guidelines:
- State needs from the **user's perspective**, not the organisation's.
  Write "Reliable cargo transport" not "Provide reliable cargo transport."
- Keep needs at the right granularity — each need should map to a
  meaningful top-level capability. Too fine and the map becomes unwieldy;
  too coarse and it loses insight.
- A good test: would this need make sense as a direct line from anchor
  to component in a Wardley map?

## Step 3: Synthesise

Consolidate all drafts into `needs/needs.md` using the template in
[needs-template.md](references/needs-template.md).

Include:
- All user classes with their needs
- **Shared needs** — needs appearing across multiple user classes
  (these are important structural signals)
- **Excluded / out of scope** — user classes or needs you considered
  but excluded, with reasoning
- **Open questions** — genuine uncertainties requiring client input

## Step 4: Present to client

Present the consolidated needs document to the client. Explicitly ask:

1. "Are these the right **user classes**? Are any missing? Should any
   be removed or merged?"
2. "For each user class, are these the right **needs**? Are any missing
   or incorrectly stated?"
3. "Is the **scope** right? Should anything be excluded or added?"
4. Address any open questions you identified.

This is a **negotiation**, not a presentation. Expect the client to:
- Add user classes you missed (they know their business better)
- Reword needs to match their internal language
- Challenge your evidence or confidence levels
- Narrow or expand scope

## Step 5: Iterate and agree

Based on client feedback:
1. Update the drafts in `needs/drafts/` as needed
2. Rewrite `needs/needs.md` to reflect agreed changes
3. Ask the client to confirm: "Is this needs document now accurate
   and complete enough to proceed?"

When the client agrees, clean up superseded drafts before writing the
gate artifact:
1. Compare files in `needs/drafts/` against the agreed user classes
2. Move any draft that does not correspond to an agreed user class
   to `needs/drafts/archive/` (merges, renames, and abandoned classes
   all produce superseded drafts)
3. The `needs/drafts/` directory should contain exactly one file per
   agreed user class

Then write the gate artifact:
1. Copy `needs/needs.md` to `needs/needs.agreed.md`
2. Record the agreement:
   ```
   wm-needs/scripts/record-agreement.sh --client {org} --project {slug} \
     --field "Users={list of agreed user classes}" \
     --field "Scope={any scope notes}"
   ```

## Important notes

- **Do not produce an OWM file** at this stage. User needs do not have
  evolution positioning, and representing them in OWM would impose
  false precision on the maturity axis.
- **Do not decompose needs into capabilities**. That is stage 3
  (wm-chain). Keep needs at the level of "what users want," not
  "how the organisation delivers it."
- **The `.agreed.md` file is a gate**. The next skill (wm-chain) will
  refuse to proceed without it.

## Completion

When `needs.agreed.md` is written, tell the user the next step is
`wm-chain` to map the supply chain for each agreed need.
