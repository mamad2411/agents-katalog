# AgentSkillOS

An operating system for navigating an exploding ecosystem by combining (1) skill tree construction (capability hierarchy), (2) skill retrieval (select task-relevant subset), and (3) skill orchestration (compose a multi-skill workflow, often DAG-based). Has both a Web UI (human-in-the-loop) and a headless CLI (batch execution, YAML configs, resume, progress UI). Includes observability/logging, a pluggable registry, and a published benchmark: 30 multi-format creative tasks evaluated via pairwise comparisons aggregated with Bradley–Terry scoring.

## Triggers
- "agent skill os"
- "skill tree construction"
- "skill retrieval"
- "skill orchestration"
- "multi skill workflow"
- "dag based workflow"
- "skill operating system"

## Description
AgentSkillOS is an operating system designed to manage and utilize large ecosystems of AI agent skills (claimed 200,000+ skills). It provides three core functions:
1. Skill tree construction - building capability hierarchies
2. Skill retrieval - selecting task-relevant subsets of skills
3. Skill orchestration - composing multi-skill workflows, often as DAGs

The system includes both a Web UI for human-in-the-loop interaction and a headless CLI for batch execution with YAML configs, resume capability, and progress tracking. It features observability/logging, a pluggable registry for skill discovery, and has been benchmarked on 30 multi-format creative tasks using Bradley–Terry scoring for pairwise comparisons.

## Features
- Skill tree construction (capability hierarchy)
- Skill retrieval (task-relevant subset selection)
- Skill orchestration (multi-skill workflow composition, often DAG-based)
- Web UI for human-in-the-loop interaction
- Headless CLI for batch execution
- YAML configuration support
- Resume capability for interrupted workflows
- Progress tracking and UI
- Observability and logging systems
- Pluggable registry for skill discovery
- Benchmark: 30 multi-format creative tasks (PDF/PPTX/DOCX/HTML/video/images, etc.)
- Bradley–Terry scoring for pairwise comparisons
- Ablation studies showing retrieval + orchestration both matter
- Strategy selection affecting DAG topology

## Usage
Use when you need to manage, retrieve, and orchestrate large numbers of AI agent skills for complex tasks that require multiple capabilities working together.

## Example
```
/agent-skill-os construct skill tree for data analysis tasks
/agent-skill-os retrieve skills for creating a presentation
/agent-skill-os orchestrate workflow: research → outline → design → review
/agent-skill-os run benchmark on 30 creative tasks
/agent-skill-os show skill registry statistics
```
