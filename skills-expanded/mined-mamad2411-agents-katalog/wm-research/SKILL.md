---
name: wm-research
description: >
  Kick off a Wardley Mapping project. Reads shared organisation research,
  agrees project scope with the client, creates the project directory,
  and produces a coarse landscape sketch in OWM format. Use when starting
  a new Wardley Mapping project for a client that has already been
  researched.
metadata:
  author: monkeypants
  version: "0.2"
  skillset: wardley-mapping
  stage: "1"
  freedom: medium
---

# Wardley Mapping Project Kickoff

You are starting a new **Wardley Mapping project**. Your goal is to
agree on the project scope with the client, set up the project directory,
and produce an initial landscape sketch.

## Prerequisites

Check that the client workspace contains:
- `resources/index.md` (shared research gate)

If missing, tell the user to run `org-research` first.

Identify the project directory. Either:
- The user specifies a project slug
- The `engage` skill has already created one (check `projects/index.md`)
- You create one using the convention `maps-{n}` (check existing projects
  to determine `n`)

The project path is `clients/{org}/projects/{project-slug}/`.

## Step 1: Read research

Read `resources/index.md` and all sub-reports in `resources/`.

Identify:
- Who the organisation's users likely are
- What the organisation's core capabilities appear to be
- Where technology or market evolution is happening
- What constraints exist

## Step 2: Propose project scope

Present a project brief to the client:

```markdown
# Wardley Mapping Brief — {Organisation Name}

## Scope

{What this map will cover: the whole enterprise, a specific division,
a specific product/service, or a specific strategic question}

### Scope boundaries

- **Included**: {explicit list of what is in scope}
- **Excluded**: {explicit list of what is out of scope}
- **Boundary ambiguities**: {areas where the scope boundary is unclear
  and may need revisiting — name them now rather than discovering them
  mid-engagement}

## Trade-off questions

These shape the character of the map. Discuss with the client:

- **Breadth vs depth**: broad enterprise landscape or deep dive into
  one area?
- **Current vs future**: map the organisation as it is, or as it is
  becoming?
- **Single vs multi-stakeholder**: one user perspective or multiple
  competing perspectives?
- **Operational vs strategic**: how the organisation runs today, or
  where it should move?

## Primary user classes (initial)

{Proposed anchors for the map, from research}

## Strategic questions

{What questions should the finished map answer? These are success
criteria — if the map cannot address these questions, it has not
delivered value.}

## Key areas of interest

{What the research suggests are the most interesting things to map}

## Cross-project references

{If other projects exist that could inform this one, note them here}
```

## Step 3: Negotiate and agree

This is a negotiation. The client may:
- Change the scope
- Add or remove user classes
- Redirect focus to different areas
- Reference other projects for context

Iterate until the client confirms.

When the client agrees:
1. If the project is not yet registered (i.e. `engage` was not run
   first), register it now:
   ```
   engage/scripts/register-project.sh --client {org} --slug {slug} \
     --skillset "wardley-mapping" --scope "{agreed scope}"
   ```
   If the project already exists in the registry (engage created it),
   skip this step.
2. Create the project directory (if not already created by engage):
   ```
   projects/{slug}/
   ├── needs/
   │   └── drafts/
   ├── chain/
   │   └── chains/
   ├── evolve/
   │   └── assessments/
   └── strategy/
       └── plays/
   ```
3. Write `brief.agreed.md` with the agreed scope
4. Record the brief agreement and activate the project:
   ```
   wm-research/scripts/record-brief-agreed.sh --client {org} --project {slug} \
     --field "Scope={agreed scope}" --field "Primary users={list}"
   ```

## Step 4: Landscape sketch

Generate `landscape.owm` in the project directory. This is a coarse,
high-level enterprise map with approximately 10-15 components:

- **A sketch**, not a commitment. Positions are approximate.
- **Useful for orientation**. It gives the client something visual early.
- **Expected to be wrong**. The map will be rebuilt through wm-needs,
  wm-chain, and wm-evolve.

Use OWM DSL syntax. Include:
- 1-3 anchors (primary user classes from the agreed brief)
- Major capabilities at approximate visibility/evolution positions
- Key dependencies
- A title and `style wardley`

Add a comment at the top:
```owm
// DRAFT — coarse enterprise landscape from initial research
// This map will be rebuilt through wm-needs, wm-chain, and wm-evolve
```

Render to SVG:
```
bin/ensure-owm.sh clients/{org}/projects/{slug}/landscape.owm
```

## Completion

When all artifacts are written, summarise the agreed scope and tell the
user the next step is `wm-needs` to identify and agree on user needs.
