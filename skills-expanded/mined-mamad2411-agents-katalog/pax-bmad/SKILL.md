---
name: "pax_bmad"
description: "Controls BMAD workflows according to the defined sequence. Invoke when user wants to manage BMAD workflows or needs guidance on workflow steps."
---

# pax_bmad - BMAD Workflow Orchestrator

## Description

pax_bmad is an OpenSkills-compatible agent skill that controls BMAD workflows according to the sequence defined in [BMAD Method Workflow Map](https://docs.bmad-method.org/reference/workflow-map/).

## Features

- **Workflow Control**: Ensures users follow the proper BMAD workflow steps
- **Status Tracking**: Provides current status and available next steps
- **Phase Management**: Guides users through the 4 BMAD phases
- **Step Validation**: Prevents users from executing invalid steps
- **Project Level**: Requires project level initialization
- **TEA Testing Methodology**: Integrated BMAD TEA testing workflows (TMT, TF, TD, CI, AT, TA, RV, TR, NR)

## Usage

### Initialize Workflow
```
/pax_bmad initialize <project_level>
```
Where `<project_level>` can be: low, medium, high

### Check Status
```
/pax_bmad
```

### Execute Steps
```
/pax_bmad <step_id>
```

### Move to Next Phase
```
/pax_bmad next_phase
```

## Available Steps by Phase

### Phase 1: Analysis (Optional)
- `brainstorming` - Brainstorm Project Ideas
- `research` - Validate market/technical/domain assumptions
- `product_brief` - Capture strategic vision
- `teach_me_testing` (TMT) - Learn testing methodology (7 sessions, 1-2 weeks)

### Phase 2: Planning
- `prd` - Define requirements (FRs/NFRs) [Required]
- `ux_design` - Design user experience

### Phase 3: Solutioning
- `architecture` - Make technical decisions explicit [Required]
- `epics_stories` - Break requirements into implementable work [Required]
- `implementation_readiness` - Gate check before implementation [Required]
- `tea_framework` (TF) - Scaffold test framework
- `tea_design` (TD) - Risk-based test planning

### Phase 4: Implementation
- `sprint_planning` - Initialize tracking [Required]
- `create_story` - Prepare next story for implementation [Required]
- `dev_story` - Implement the story [Required]
- `code_review` - Validate implementation quality [Required]
- `correct_course` - Handle significant mid-sprint changes
- `sprint_status` - Track sprint progress and story status [Required]
- `retrospective` - Review after epic completion [Required]
- `tea_ci` (CI) - Set up quality pipeline
- `tea_atdd` (AT) - Failing acceptance tests (TDD)
- `tea_automation` (TA) - Expand automation coverage
- `tea_review` (RV) - Quality audit with scoring
- `tea_req_trace` (TR) - Coverage mapping + gate decision
- `tea_nfr` (NR) - Non-functional requirements evaluation

## Installation

This skill is installed via OpenSkills:
```bash
npx openskills install YeJianXin/pax_bmad/
```

## Support

For issues and feature requests, please visit: https://github.com/YeJianXin/pax_bmad/issues