# Skill: Client Showcase Generator

## Trigger
"Create client showcase" / "Build portfolio demo" / "Demo for {prospect}" / "Show PMM Brain capabilities"

## Process

### Step 1: Load context
- Read `data/brain/pmm_brain.json` — Brain summary for system proof
- Scan `data/output/` — Best output examples across formats
- Reference Obsidian vault structure at `~/Documents/Knowledge-brain-Obsidian/Knowledge Brain/PMM Brain/`

### Step 2: Determine showcase type
Based on user request, generate one or more:

#### A. Pipeline Demo (Full workflow walkthrough)
Walk through a real example end-to-end:
1. **Input:** Theme selection from Brain (show suggest-themes output)
2. **Research:** Evidence sourcing from 13 newsletters, 861 raw posts, 37 mental models
3. **Generation:** 3-angle draft production with format selection
4. **Critique:** Rubber Duck Escalator scoring with real scores
5. **Distribution:** Pillar → micro atomization across 4 formats
6. **Output:** Final content package (LinkedIn + Twitter + Newsletter + Carousel)

#### B. Case Study (2-3 completed content packages)
For each package:
1. **Theme:** What was written about and why
2. **Research brief:** What evidence and models informed it
3. **Critique scores:** Real Escalator scores showing quality bar
4. **Final outputs:** The actual content across formats
5. **Results:** Engagement metrics if available (optional)

#### C. Template Package (System architecture — exportable)
Document the system as a replicable blueprint:
1. **CLAUDE.md pattern:** How the orchestrator routes between skills
2. **Skill structure:** How each skill works (trigger → process → output)
3. **Brain schema:** How knowledge is structured (mental models, evidence bank, topic layers, newsletter insights)
4. **Quality gate:** How the Rubber Duck Escalator ensures output quality
5. **Distribution engine:** How pillar content atomizes into platform-native formats

### Step 3: Generate showcase artifacts
- Write in professional-but-personal tone (Sourav's voice, not corporate)
- Include real numbers: 13 newsletter sources, 37 mental models, 69 evidence stats, 861 raw posts
- Show before/after examples where possible
- Highlight what makes this system different from generic AI content tools

### Step 4: Present to user
Show generated artifacts with clear sections. User can approve, tweak, or request different emphasis.

## Output Format
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CLIENT SHOWCASE: [Type]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Showcase content organized by type]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SYSTEM STATS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Newsletter sources: 13
Raw post notes: 861
Mental models: 37
Evidence bank stats: 69
Content formats: 4 (LinkedIn, Twitter/X, Newsletter, Carousel)
Quality gate: 5-phase Rubber Duck Escalator (threshold: 8+)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
