# Cursor AI Rules for Research Project

## Project Context

⚠️ **Important Context Anchor**  
To understand the overall research direction, assumptions, and current focus, **always refer to these files first** before making high-level suggestions or changes:

1. **Overall project**: `working_notes/project_overview.md` - Main research direction and assumptions
2. **Project-specific**: Each project has a README in its folder:
   - `working_notes/qdcnn/README.md` - QDCNN project details
   - `working_notes/qhydra/README.md` - Quantum Hydra project details
   - `working_notes/shared/README.md` - Shared concepts across projects

This repository contains multiple loosely coupled research projects focused on quantum machine learning.

## Directory Structure

```
/
├── src/                    # Source code (models, data processing, training)
├── docs/                   # Documentation and team meetings
│   └── _cursor_commands/   # Custom commands and roles
├── working_notes/          # Research notes (main knowledge base)
│   ├── project_overview.md # Overall project context
│   ├── qdcnn/             # QDCNN project
│   │   ├── README.md      # Project-specific context
│   │   ├── literature/    # Paper summaries
│   │   ├── concepts/      # Concept notes
│   │   ├── ideas/         # Idea bank
│   │   ├── experiment_design/  # Experimental plans
│   │   └── results/        # Results analysis
│   ├── qhydra/            # Quantum Hydra project
│   │   ├── README.md      # Project-specific context
│   │   └── [same structure as qdcnn]
│   ├── shared/            # Cross-project concepts
│   │   └── README.md      # Shared context
│   ├── scribble/          # Raw exploratory thoughts
│   └── daily_log/         # Daily reading notes
├── notebooks/             # Jupyter notebooks for exploration
└── scripts/               # Utility scripts
```

## Understanding Projects

**When working on a specific project:**
1. Read the project's README first: `working_notes/{project_name}/README.md`
2. Check `working_notes/project_overview.md` for overall context
3. Explore project-specific folders: `literature/`, `concepts/`, `experiment_design/`, `results/`

**Project folders:**
- `qdcnn/` - Quantum Dilated Convolutional Neural Networks
- `qhydra/` - Quantum Hydra
- `shared/` - Cross-project concepts and background

## Coding Style

- Use Python type hints for function signatures
- Follow PEP 8 style guidelines
- Use descriptive docstrings (Google style)
- Keep functions focused and modular
- Comment complex logic, especially quantum operations

## Research Notes Style

- **Project-specific notes**: Each project (`qdcnn/`, `qhydra/`) has its own `literature/`, `concepts/`, `ideas/`, `experiment_design/`, `results/`
- **Shared notes**: `shared/` contains cross-project concepts
- **Raw thoughts**: `scribble/` for exploratory ideas (may be promoted to structured notes)
- **Daily logs**: `daily_log/` for reading notes and connections
- Use markdown links to connect related files: `[[path/to/file.md]]`
- Keep notes concise and concept-focused

## File Naming Conventions

- Literature: `YYYY-MM-DD_paperTitle.md`
- Daily logs: `YYYY-MM-DD.md`
- Concepts/Ideas: `concept_name.md` or `idea_name.md`
- Experiments: `0001_name/`, `0002_name/`
- Config files: `config.yaml`

## Key Concepts

- **QDCNN**: Quantum Dilated Convolutional Neural Networks
- **Dilated Convolution**: Expanding receptive field with dilation rate
- **NISQ Era**: Noisy Intermediate-Scale Quantum devices
- Focus on understanding concepts, not just implementation

## When Writing Code

- Add docstrings explaining the purpose and key concepts
- Include type hints
- For quantum operations, explain the quantum concept being used
- Reference related papers or notes when relevant

## When Suggesting Changes

- **Check project context first**: Read the relevant project README (`working_notes/{project}/README.md`)
- Consider the research context and learning goals
- Maintain connections to literature and working notes
- Keep experiments reproducible and well-documented
- Suggest improvements that enhance understanding, not just performance

## Before pushing to GitHub

Comment out or remove all blocks between `<!-- LOCAL-ONLY: begin -->` and `<!-- LOCAL-ONLY: end -->`

## Custom Commands
When user types `@` followed by a file path (Cursor will auto-complete file names), read the corresponding command file from `docs/_cursor_commands/` and execute it.

Commands are organized into two categories:
- **Tasks** (`tasks/`): Workflow-oriented commands that execute a procedure and complete. These are **objective and fact-based**.
  - **Priority**: Tasks have **absolute priority** over any previously adopted roles
  - When a task is executed, **ignore all previous roles** and execute in a completely objective, fact-based manner
  - Tasks must not include any subjective interpretations, opinions, or role perspectives
- **Roles** (`roles/`): Perspective-oriented commands that adopt a role/persona (may persist in conversation). These may include **subjective interpretation**.
  - Roles are overridden when a task is executed

**Important**: 
- Tasks override roles: When a task is executed, it ignores any previously adopted roles
- Do not mix tasks and roles in the same command
- Tasks should remain objective and fact-based
- Use roles separately for perspectives and feedback

**Task-oriented commands** (`docs/_cursor_commands/tasks/`):
- `promote.md` - Promote scribble content to concepts/ideas/experiment_design (supports tag-based linking)
- `analyze.md` - Provide structured, factual analysis
- `summarize.md` - Create concise, factual summaries
- `compare.md` - Compare items factually
- `meeting_to_team.md` - Transform meeting log to structured team meeting summary
- `find_by_tag.md` - Find files by tag (`@concept/`, `@metric/`, `@model/`, `@phenomenon/`)

**Role-based commands** (`docs/_cursor_commands/roles/`):
- `LeadAuthor.md` - Lead Author/PI role
- `Reviewer.md` - Constructive but skeptical reviewer
- `Coder.md` - Senior Research Engineer
- `Visualizer.md` - Scientific Visualization expert
- `Editor.md` - Senior Copy Editor
- `LitExpert.md` - Literature Expert
- `Reader.md` - General audience reader
- `CursorDesigner.md` - Cursor AI System Designer & Workflow Optimizer (system-level design, structure review, workflow optimization)

**Usage**: Type `@` and let Cursor auto-complete the file name. Example: `@docs/_cursor_commands/tasks/analyze.md` or `@analyze.md` (if Cursor finds it).

Command files location: `docs/_cursor_commands/tasks/` and `docs/_cursor_commands/roles/`
