# Workflow Engine Skill

**Purpose:** Autonomous workflow execution engine for 10x Team - chains skills together and executes them without manual intervention.

**Developed by:** Team 10x.in

---

## Overview

The Workflow Engine is the execution backbone that:
1. Creates workflow templates from user requests
2. Manages the TLDraw canvas for visualization
3. Executes workflows autonomously after approval
4. Handles inter-skill data passing
5. Generates outputs in multiple formats

---

## Directory Structure

```
.claude/skills/workflow-engine/
├── SKILL.md                    # This file
├── scripts/
│   ├── create_workflow.py      # Create workflow from request
│   ├── execute_workflow.py     # Execute approved workflow
│   ├── canvas_sync.py          # Sync with TLDraw canvas
│   ├── export_workflow.py      # Export workflow results
│   └── utils.py                # Shared utilities
├── templates/
│   ├── marketing_campaign.json # Marketing workflow template
│   ├── outreach_sequence.json  # Outreach workflow template
│   ├── landing_page.json       # Landing page workflow template
│   └── custom.json             # Custom workflow template
└── schemas/
    ├── workflow.schema.json    # Workflow JSON schema
    └── step.schema.json        # Step JSON schema
```

---

## Workflow Lifecycle

```
┌─────────────────────────────────────────────────────────────────┐
│                     WORKFLOW LIFECYCLE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [1] USER REQUEST                                               │
│       ↓                                                         │
│  [2] ANALYZE & PLAN (identify skills, create steps)             │
│       ↓                                                         │
│  [3] CLARIFICATION (ask ALL questions upfront)                  │
│       ↓                                                         │
│  [4] GENERATE TEMPLATE (workflow.json)                          │
│       ↓                                                         │
│  [5] VISUALIZE IN CANVAS (TLDraw on port 3001)                  │
│       ↓                                                         │
│  [6] USER APPROVAL (review and confirm)                         │
│       ↓                                                         │
│  [7] AUTONOMOUS EXECUTION (no interruptions)                    │
│       ↓                                                         │
│  [8] OUTPUT GENERATION (PDF, PPT, JSON, etc.)                   │
│       ↓                                                         │
│  [9] COMPLETION NOTIFICATION                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Canvas Integration

The workflow visualizes in TLDraw canvas:

### Creating Workflow Visualization
1. Claude Code creates workflow template JSON
2. Sends template to canvas via WebSocket (port 3002)
3. Canvas renders workflow as nodes and connections
4. User can view and modify visualization

### Export from Canvas
1. User clicks "Export" in canvas
2. Canvas sends workflow back via WebSocket
3. Claude Code receives and validates workflow
4. Execution begins after confirmation

### WebSocket Protocol

**Send to Canvas:**
```json
{
    "type": "workflow:create",
    "workflow_id": "wf_123456",
    "data": { /* workflow template */ }
}
```

**Receive from Canvas:**
```json
{
    "type": "workflow:export",
    "workflow_id": "wf_123456",
    "data": { /* exported workflow */ }
}
```

---

## Workflow Template Schema

```json
{
    "workflow_id": "wf_<timestamp>_<slug>",
    "name": "Marketing Campaign Workflow",
    "description": "Complete marketing campaign creation",
    "version": "1.0.0",
    "created_at": "2026-01-23T00:00:00Z",
    "status": "draft",

    "metadata": {
        "estimated_duration": "30 minutes",
        "skill_count": 5,
        "autonomous": true
    },

    "user_inputs": {
        "questions": [
            {
                "id": "q1",
                "question": "What is your target audience?",
                "type": "text",
                "required": true
            }
        ],
        "answers": {}
    },

    "steps": [
        {
            "step_id": 1,
            "name": "Research",
            "skill": "research",
            "action": "gather_info",
            "inputs": {
                "topic": "{{user_inputs.q1}}"
            },
            "outputs": {
                "research_data": "output/workflows/{{workflow_id}}/step1_research.json"
            },
            "depends_on": [],
            "timeout": 300,
            "retry_count": 2
        }
    ],

    "outputs": {
        "directory": "output/workflows/{{workflow_id}}",
        "formats": ["pdf", "json"],
        "files": []
    },

    "canvas": {
        "visualized": false,
        "exported_at": null
    }
}
```

---

## Skill Chaining

Skills can pass data to subsequent skills:

```
Step 1: research
    outputs: { research_data: "path/to/data.json" }
           ↓
Step 2: copywriting
    inputs: { context: "{{steps.1.outputs.research_data}}" }
    outputs: { copy: "path/to/copy.md" }
           ↓
Step 3: design
    inputs: { copy: "{{steps.2.outputs.copy}}" }
    outputs: { design_spec: "path/to/design.json" }
```

---

## Execution Engine

### Pre-Execution Checks
1. Validate all user inputs are provided
2. Verify all required skills are available
3. Check dependencies are resolvable
4. Ensure output directories exist

### Execution Loop
```python
for step in workflow.steps:
    # Check dependencies
    if not all_dependencies_complete(step):
        wait_for_dependencies(step)

    # Execute step
    try:
        result = execute_skill(step.skill, step.action, step.inputs)
        step.outputs = result
        step.status = "completed"
        save_output(result, step.output_path)
    except Exception as e:
        if step.retry_count > 0:
            retry_step(step)
        else:
            handle_failure(step, e)

    # Update progress
    update_workflow_status(workflow)
    notify_progress(step)
```

### Post-Execution
1. Compile all step outputs
2. Generate final deliverables (PDF, PPT, etc.)
3. Save to output directory
4. Notify user of completion

---

## Output Formats

### PDF Generation
- Uses ReportLab for PDF creation
- Includes all text content, images, charts
- Professional formatting with 10x.in branding

### PPT Generation
- Uses python-pptx for presentations
- Slide-by-slide content from workflow
- Includes design specifications

### JSON Export
- Raw workflow data and results
- Complete audit trail
- Machine-readable format

---

## Commands

### `/workflow create <description>`
Create a new workflow from natural language description.

### `/workflow visualize <workflow_id>`
Open workflow in TLDraw canvas for visualization.

### `/workflow execute <workflow_id>`
Execute an approved workflow autonomously.

### `/workflow status <workflow_id>`
Check current status of a workflow.

### `/workflow list`
List all workflows with their statuses.

### `/workflow export <workflow_id> <format>`
Export workflow results to specified format.

---

## Integration with Claude Code

Claude Code (the brain) interacts with Workflow Engine:

1. **Request Analysis** → Claude Code parses user request
2. **Skill Identification** → Identifies required skills
3. **Template Creation** → Uses workflow-engine to create template
4. **Clarification** → Claude Code asks questions via AskUserQuestion
5. **Canvas Sync** → Sends to TLDraw for visualization
6. **Approval** → User confirms in canvas or chat
7. **Execution** → workflow-engine executes autonomously
8. **Delivery** → Results returned to user

---

## Error Handling

- **Skill Not Found:** Log error, notify user, skip or abort
- **Timeout:** Retry with increased timeout, then fail gracefully
- **Dependency Failed:** Skip dependent steps, continue where possible
- **User Input Missing:** Prompt for missing input before continuing

---

## Logging

All executions are logged to:
```
output/logs/workflow_<id>_<timestamp>.log
```

Log format:
```
[2026-01-23 12:00:00] [INFO] Workflow wf_123456 started
[2026-01-23 12:00:01] [STEP] Executing step 1: research
[2026-01-23 12:00:30] [OK] Step 1 completed in 29s
[2026-01-23 12:00:31] [STEP] Executing step 2: copywriting
...
```

---

**Developed by Team 10x.in**
