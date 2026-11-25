---
name: wm-chain
description: >
  Map the supply chain for agreed user needs in a Wardley Mapping
  engagement. Revisits research through the lens of agreed needs,
  decomposing each need into capabilities and dependencies as a
  markdown dependency tree. Produces a consolidated supply chain
  document. Use after user needs are agreed (needs.agreed.md exists).
metadata:
  author: monkeypants
  version: "0.2"
  skillset: wardley-mapping
  stage: "3"
  freedom: medium
---

# Supply Chain Mapping for Wardley Maps

You are conducting the **supply chain identification phase** of a Wardley
mapping engagement. Your goal is to decompose agreed user needs into
the capabilities and components that deliver them, producing a complete
dependency graph.

## Prerequisites

Check that the project directory contains:
- `needs/needs.agreed.md`

Check that the client workspace contains:
- `resources/index.md` and research sub-reports in `resources/`

If `needs.agreed.md` is missing, tell the user to complete `wm-needs`
first. The `.agreed.md` suffix indicates the client has signed off.

The project path is `clients/{org}/projects/{project-slug}/`.

## Step 1: Re-read research through the lens of needs

Read `needs/needs.agreed.md` to understand the agreed user classes
and their needs.

Then re-read `resources/index.md` and relevant sub-reports in
`resources/`, specifically looking for:
- **Capabilities** the organisation uses to deliver each need
- **Technologies** and platforms underlying those capabilities
- **External dependencies** (suppliers, partners, data sources)
- **Infrastructure** underpinning everything

You are building a mental model of "how does this organisation actually
deliver what users need?"

## Step 2: Decompose each need

For each agreed need, work **top-down**:

1. What capabilities directly deliver this need?
2. For each capability, what does it depend on?
3. Continue recursively until you reach:
   - **Commodities** (electricity, internet, standard hardware)
   - **External services** with no further visible decomposition
   - **Fundamental resources** (raw materials, data, people)

Write each chain to `chain/chains/{need-slug}.md` using the template
in [chain-template.md](references/chain-template.md).

Formatting rules for dependency trees:
```
Need Name
├── Capability A
│   ├── Sub-capability A1
│   │   └── Infrastructure Component
│   └── Sub-capability A2
├── Capability B
│   └── Sub-capability B1
│       ├── External Service
│       └── Data Source
└── Capability C (commodity)
```

Guidelines:
- **Use the tree to represent visibility.** Components near the top
  are visible to the user. Components deeper are increasingly invisible.
  This maps directly to the Y-axis (visibility) of the eventual
  Wardley map.
- **Do NOT attempt to position components on the evolution axis.**
  That is stage 4 (wm-evolve). The horizontal axis has no meaning at
  this stage. Dependency trees are the honest representation — they
  encode what we know (depth/visibility) without pretending to know
  what we don't (evolution).
- **Flag shared components.** When a component appears in multiple
  chains, note it with "(shared)" and list which other needs also
  depend on it. Shared components are structurally important.
- **Stop at sensible boundaries.** Don't decompose "electricity" into
  "power generation -> transmission -> distribution." Stop where the
  organisation's agency ends, unless infrastructure is specifically
  in scope.
- **Use the organisation's language** where possible. If they call it
  a "Fleet Management System" not "Asset Tracking Platform," use
  their term. The client needs to recognise their own supply chain.

Run chains **in parallel** where possible — each need's chain is
independent.

## Step 3: Identify shared components

After all chains are written, look across them for:

- **Shared components**: same capability serving multiple needs.
  These are structurally important — they sit at critical junctions
  and often become strategic leverage points.
- **Implicit dependencies**: components that are assumed but not
  explicit in any single chain (e.g. "identity management" underlying
  multiple systems).
- **Potential duplication**: cases where two chains use different
  names for what might be the same component. Consolidate these.

## Step 4: Synthesise

Write `chain/supply-chain.md` using the consolidated template in
[chain-template.md](references/chain-template.md). Include:

1. **Merged dependency graph** — all chains combined, deduplicating
   shared components
2. **Shared components table** — each shared component with the
   needs it serves and its depth from the user
3. **Component inventory** — a flat table of every unique component
   with its parents, children, and notes
4. **Observations** — structural insights:
   - Bottlenecks or single points of failure
   - Surprisingly deep dependency chains
   - Missing capabilities (things that should exist but weren't found)
   - Clusters of related components
5. **Chain-to-need validation** — before presenting output, verify
   correspondence between chain files and agreed needs:
   - Every chain file in `chain/chains/` must map to at least one
     agreed need in `needs/needs.agreed.md`
   - Every agreed need must have a corresponding chain file
   - Produce an explicit mapping table showing need → chain file(s)
   - Flag orphan chains (no corresponding need) and uncovered needs
     (no corresponding chain) as errors to resolve before proceeding
6. **Open questions** — for client review

## Step 5: Present to client

Present the consolidated supply chain to the client. Ask:

1. "Does this dependency structure match how your organisation
   actually works?"
2. "Are there capabilities missing from these chains?"
3. "Are there capabilities listed that don't actually exist or are
   wrong?"
4. "Do the shared components look right? Are there others?"
5. Address any open questions.

The client will likely:
- Correct component names to match internal terminology
- Add capabilities you couldn't see from public research
- Identify dependencies between components that weren't obvious
- Flag components that are planned but don't exist yet

## Step 6: Iterate and agree

Based on client feedback:
1. Update individual chains in `chain/chains/` as needed
2. Rewrite `chain/supply-chain.md`
3. Ask the client to confirm: "Is this supply chain now accurate
   and complete enough to proceed to evolution assessment?"

When the client agrees:
1. Copy to `chain/supply-chain.agreed.md`
2. Record the agreement:
   ```
   wm-chain/scripts/record-agreement.sh --client {org} --project {slug} \
     --field "Components={total count} unique components identified" \
     --field "Shared components={list of key shared components}" \
     --field "Scope notes={any caveats}"
   ```

## Important notes

- **Output is markdown only.** No OWM files at this stage. The
  evolution axis is unknown, so OWM would require guessing half
  the coordinates. Markdown dependency trees are the honest
  representation.
- **The `.agreed.md` file is a gate.** The next skill (wm-evolve)
  will refuse to proceed without it.
- **Component count matters.** A typical map has 15-30 components.
  If you have fewer than 10, you may be too coarse. If you have
  more than 50, you may need to split into submaps. Discuss with
  the client.

## Completion

When `supply-chain.agreed.md` is written, tell the user the next step
is `wm-evolve` to position components on the evolution axis and
produce the first real Wardley map in OWM format.
