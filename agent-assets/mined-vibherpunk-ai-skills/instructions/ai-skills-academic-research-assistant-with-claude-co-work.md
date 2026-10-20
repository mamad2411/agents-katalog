# Copilot Instructions: Academic Research Assistant With Claude Co Work
Description: A comprehensive skill for using Claude Co-Work to automate and enhance academic research workflows including literature reviews, presentation creation, and research gap analysis.

# Academic Research Assistant with Claude Co-Work

## Overview
Claude Co-Work transforms academic research through agentic workflows, verified data connectors, and reusable skills. This skill document outlines how to leverage these features for literature reviews, presentation creation, and research gap analysis. For foundational concepts, see [Core Concepts](references/core_concepts.md).

## Step-by-Step Workflow

1. **Initial Setup**
   - Install Claude desktop app (ensure sufficient disk space)
   - Configure essential settings as detailed in [Practical Guide](references/practical_guide.md)
   - Add academic connectors (Consensus, PubMed)

2. **Project Creation**
   ```
   1. Click 'Projects' → 'New Project'
   2. Name (e.g., "OPV Devices Review")
   3. Add instructions:
      "Academic project focusing on recent literature about OPV devices for indoor use. Prioritize peer-reviewed sources and identify seminal papers."
   4. Upload reference materials:
      - University writing guidelines
      - Previous literature review examples
   ```

3. **Literature Review Execution**
   ```
   Prompt: "Create an academic literature review about [TOPIC]. Focus on recent literature and seminal papers. Use connected databases for sourcing."
   
   Best Practice: Wait for agent questions (e.g., "How deep should the search go?") to refine output
   Pitfall Avoidance: Verify all citations link properly to Consensus/PubMed
   ```

4. **Presentation Generation**
   ```
   1. Upload paper PDF (must be on same drive)
   2. Prompt: "Turn this into a 10-minute presentation for my group meeting"
   3. Expected Output:
      - Structured slide deck
      - Key findings extraction
      - Speaker notes
   ```

5. **Research Gap Analysis**
   ```
   Invoke skill: /research_gap_finder
   Input: "My PhD project in [FIELD] focuses on [SPECIFIC AREA]"
   Output: List of underexplored research questions with supporting evidence
   ```

6. **Skill Creation**
   After successful task completion:
   ```
   Prompt: "Capture this workflow as a skill for future use"
   Follow skill creator prompts to define:
   - Input parameters
   - Quality checks
   - Output formatting
   ```

## Code/Prompt Templates

**Literature Review Starter**
```
Create an academic literature review about [TOPIC]. Requirements:
1. Include 5-7 seminal papers
2. Focus on last 5 years of research
3. Organize by these themes: [THEME1], [THEME2], [THEME3]
4. Use Consensus connector for verified sources
5. Format citations in [STYLE] style
```

**Presentation Conversion**
```
Convert this paper into a [LENGTH] presentation for [AUDIENCE]. Include:
1. Key findings slide
2. Methods overview
3. 3-5 main results slides
4. Future work suggestions
5. Speaker notes for each slide
```

## Best Practices
1. **File Management**: Keep all research files on the same drive as Claude installation
2. **Skill Development**: Create skills after 2-3 successful manual executions of a workflow
3. **Validation**: Always spot-check 20% of citations in generated literature reviews
4. **Timing**: Schedule long-running tasks (like weekly literature updates) during off-hours

## Common Pitfalls
1. **Cross-Drive Access**: Files not on Claude's drive won't be accessible (transcript example)
2. **Output Time**: Complex tasks take significantly longer than chat (10+ minutes for 14-page review)
3. **Skill Overuse**: Don't create skills for one-off tasks - reserve for truly repetitive workflows

## Validation Steps
1. **Citation Verification**: Sample 5-10 citations to confirm they:
   - Exist in source databases
   - Match the context used
2. **Content Accuracy**: For presentations, verify:
   - Key findings match paper abstract
   - Methods description is technically correct
3. **Skill Testing**: Run new skills 3 times with varied inputs to check consistency

For detailed skill creation methods, see [Skill Creation](references/skill_creation.md).

## Reference Guides

### Core Concepts

# Core Concepts of Claude Co-Work for Academia

Claude Co-Work represents a significant evolution from traditional chat-based AI interactions by introducing an agentic workflow system. Unlike standard chat interfaces where interactions are linear (user prompt → AI response), Co-Work employs multiple specialized agents that collaborate to complete complex tasks. This architecture is particularly valuable for academic research where tasks often require multi-step processes and verification.

Key architectural components:
1. **Agentic Workflow**: When given a task, Co-Work spawns specialized sub-agents that handle different aspects (e.g., one for literature search, another for synthesis, another for formatting). These agents communicate and verify outputs before presenting final results.
2. **Skills**: Predefined workflows for common academic tasks (literature reviews, presentation creation, etc.) that ensure consistent, high-quality outputs. Skills can be created from successful workflows using the meta 'skill creator' skill.
3. **Connectors**: API-based integrations with academic databases and tools (Consensus, PubMed, BioRender) that provide verified data sources and reduce hallucination risks.
4. **Projects**: Persistent workspaces that maintain context, instructions, and reference materials for ongoing research initiatives.

Academic applications demonstrated in the transcript include:
- Automated literature reviews with proper citations (14-page output)
- Paper-to-presentation conversion (understanding technical content)
- Research gap identification using specialized skills

The system's effectiveness stems from its ability to maintain process consistency through skills while accessing verified data via connectors, addressing two major pain points in academic AI use: output variability and source reliability.

### Practical Guide

# Practical Guide to Setting Up Claude Co-Work for Research

## System Requirements
- Ensure sufficient hard drive space (transcript notes installation failures due to space constraints)
- Windows-compatible system (Mac compatibility not discussed in transcript)

## Initial Setup
1. Download and install Claude desktop application from official source
2. Log in with your Claude account credentials
3. Verify successful launch with three main tabs visible: Chat, Co-Work, and Code

## Essential Configuration
1. **Enable Memory**: Navigate to Settings → Conversations → Turn on 'Generate memory from chat history'
2. **Tool Access**: Enable all relevant capabilities under Settings → Capabilities:
   - Browser use
   - Computer use
   - Visuals
   - Code execution
3. **Connectors**: Add academic-relevant connectors via Customize → Connectors:
   - Consensus (for literature searches)
   - PubMed
   - BioRender (for scientific illustrations)

## Storage Best Practices
- Keep all research files on the same drive as Claude installation (transcript notes cross-drive access issues)
- Maintain organized project folders for easy reference

## Performance Considerations
- Co-Work tasks take significantly longer than chat (10+ minutes for complex tasks)
- Scheduled tasks require computer to remain awake (enable 'Keep computer awake' in Settings if needed)

## Academic Workflow Optimization
1. Create dedicated projects for each research initiative
2. Pre-load project spaces with:
   - University guidelines
   - Example papers/presentations
   - Writing templates
3. Develop custom skills for repetitive tasks (literature reviews, weekly paper summaries)

### Skill Creation

# Creating and Using Academic Skills in Claude Co-Work

## What Are Skills?
Skills are predefined workflows that encapsulate successful processes for recurring academic tasks. Unlike one-off prompts, skills ensure consistent methodology and output quality across repetitions.

## Built-in Academic Skills
From the transcript, these pre-existing skills are particularly useful:
1. **Literature Review Helper**: Creates comprehensive, cited reviews
2. **Presentation Generator**: Converts papers into slide decks
3. **Research Gap Finder**: Identifies underexplored areas in your field

## Creating Custom Skills
Follow this proven workflow from the transcript:
1. First complete the task manually through Co-Work interaction
2. At successful completion, prompt: "Capture this as a skill"
3. The meta 'skill creator' will:
   - Analyze the workflow
   - Identify key decision points
   - Generate a reusable skill file

## Skill Invocation
Access skills by typing backslash (/) followed by skill name. Example:
`/literature_review_helper`

## Academic Skill Examples
**Literature Review Skill Components:**
1. Automated search via connected databases (Consensus/PubMed)
2. Seminal paper identification
3. Recent literature filtering
4. Thematic organization
5. Proper citation formatting

**Presentation Skill Components:**
1. Paper structure analysis
2. Key finding extraction
3. Slide deck structuring
4. Visual element suggestions
5. Speaker note generation

## Skill Maintenance
- Store skills in relevant projects for easy access
- Update skills when methodologies change
- Share skills across research groups for consistency

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[Claude Cowork for Academics: Full Setup & Use Cases](https://www.youtube.com/watch?v=ldwjRjx8xIQ)** by Andy Stapleton