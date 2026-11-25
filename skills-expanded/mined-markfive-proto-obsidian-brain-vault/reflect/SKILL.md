---
name: reflect
description: "See your own thinking patterns in Obsidian vaults. Find emerging project clusters, challenge your assumptions, or track how your views have changed. Use when the user wants meta-awareness of their notes and thinking."
license: MIT
metadata:
  author: markfive-proto
  version: "0.1.0"
  pack: cognitive-toolkit
---

# Reflect Pack — "What am I even thinking about?"

Tools for gaining meta-awareness of your own thinking patterns through your vault.

## Commands

### /emerge — Find clusters that could become projects

When the user invokes `/emerge`:

1. Analyze vault structure:
   - `obs tags all --json` — find tag clusters
   - `obs files list --since 1m --sort modified --json` — active areas
   - `obs links orphans --json` — unconnected ideas
2. For heavily-used tags, read a sample of notes to understand the theme
3. Look for clusters:
   - Groups of notes sharing 2+ tags
   - Notes that link to each other frequently
   - Recent activity concentrated in a topic
4. For each potential project cluster:
   - Count related notes
   - Identify the central "hub" note (most linked-to)
   - Check if a MOC (Map of Content) or index already exists
   - Assess maturity: scattered thoughts vs. developing argument
5. Present findings:
   ```
   ## Emerging Projects

   ### 1. [Cluster name] (N notes, M connections)
   Hub note: [[hub]]
   Key notes: [[a]], [[b]], [[c]]
   Tags: #tag1 #tag2
   Maturity: [Scattered / Developing / Ready to synthesize]
   Suggestion: [Create a MOC? Write a synthesis? Start a project note?]

   ### 2. ...
   ```
6. Offer to create a MOC for any cluster the user chooses

### /challenge — Find contradictions in your thinking

When the user invokes `/challenge <topic>`:

1. Gather everything on the topic:
   - `obs search content "<topic>" --json`
   - `obs search path "<topic>" --json`
   - Check related tags for broader context
2. Read each relevant note and extract:
   - Claims, assertions, or positions
   - Evidence or reasoning cited
   - Assumptions (stated or implied)
3. Cross-reference for contradictions:
   - Does Note A claim X while Note B claims not-X?
   - Are there assumptions that contradict evidence elsewhere?
   - Are there positions that have evolved but old versions still exist?
4. Present the analysis:
   ```
   ## Challenging your thinking on "<topic>"

   ### Positions found
   - [Position 1] — from [[note]]
   - [Position 2] — from [[note]]

   ### Contradictions
   - [[note-a]] says X, but [[note-b]] says Y
     Your reasoning: [why each was argued]

   ### Untested assumptions
   - [Assumption from note] — no supporting evidence found in vault

   ### Questions to sit with
   - [Genuine open questions raised by the contradictions]
   ```

### /growth — See how your thinking has changed

When the user invokes `/growth <topic>`:

1. Find all notes on the topic, sorted chronologically:
   - `obs search content "<topic>" --json`
   - Sort results by file modification date
2. Read each note and extract the user's position or understanding at that time
3. Map the evolution:
   - What did you first think?
   - What changed and why?
   - Where are you now?
4. Present as a growth narrative:
   ```
   ## How your thinking on "<topic>" has evolved

   ### Phase 1: [Label] (date range)
   Key notes: [[note1]], [[note2]]
   Position: [What you thought]

   ### Phase 2: [Label] (date range)
   Trigger: [What seems to have caused the shift]
   Key notes: [[note3]]
   Position: [How it changed]

   ### Current: [Label]
   Position: [Where you are now]
   Confidence: [High/Medium/Low based on depth of notes]

   ### Growth insight
   [What this evolution reveals about the user's learning]
   ```

## Tips

- Be honest but gentle. Contradictions aren't failures — they're signs of growth.
- When identifying assumptions, distinguish between "not yet tested" and "contradicted by evidence."
- For /emerge, don't just count tags — read notes to understand if the cluster is coherent.
- Dates matter. Use file modification times to build accurate timelines.
