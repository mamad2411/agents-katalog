---
name: discipline-automation-orchestration
description: Routes discipline automation orchestration tasks to the Discipline Automation Agent for complete workflow automation from knowledge gathering through multi-company execution.
company: promptforge-ai
---

# Discipline Automation Orchestration

## Overview
This skill routes all discipline automation orchestration tasks to the Discipline Automation Agent, enabling complete workflow automation from knowledge gathering through project generation, issue creation, and multi-company execution coordination.

## Routing Criteria

Route to this skill when:
- Complete discipline lifecycle automation is needed
- Multi-phase workflow orchestration across companies
- Cross-platform project generation and coordination
- Automated knowledge synthesis and project intelligence
- Advanced issue generation with dependency mapping
- Multi-company execution package generation
- Learning integration and continuous improvement
- UI/UX design coordination across platforms
- HITL review and approval workflow management

## Workflow Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           DISCIPLINE AUTOMATION WORKFLOW                         │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  Phase 1: Knowledge Synthesis                                                   │
│  └─▶ Gather discipline knowledge → PAGE-KNOWLEDGE.md                            │
│                                                                                  │
│  Phase 2: Project Intelligence                                                  │
│  └─▶ Analyze knowledge → Identify viable projects                               │
│                                                                                  │
│  Phase 3: Issue Generation                                                      │
│  └─▶ Decompose projects → Generate executable issues                            │
│                                                                                  │
│  Phase 4: ⚠️ HITL REVIEW GAP ⚠️                                                 │
│  └─▶ Human review & approval before submission                                   │
│  └─▶ Approve → Request Changes → Reject → Escalate                              │
│                                                                                  │
│  Phase 5: Paperclip Submission                                                  │
│  └─▶ Submit approved issues to Paperclip board                                  │
│                                                                                  │
│  Phase 6: Multi-Company Orchestration                                           │
│  └─▶ Delegate to appropriate companies & agents                                 │
│                                                                                  │
│  Phase 7: Execution Monitoring                                                  │
│  └─▶ Track progress, handle conflicts, ensure completion                        │
│                                                                                  │
│  Phase 8: Learning Integration                                                  │
│  └─▶ Capture learnings → Improve future automation                              │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘

⚠️ CRITICAL: Phase 4 (HITL Review) is MANDATORY before proceeding to Phase 5
All issues must be reviewed and approved by human before Paperclip submission

## Capabilities

### Complete Workflow Automation
- **Knowledge Synthesis**: Automated PAGE-KNOWLEDGE.md generation from existing documentation
- **Project Intelligence**: AI-driven analysis for viable project opportunities
- **Issue Generation**: Advanced decomposition with dependency mapping and optimization
- **Orchestration Preparation**: Multi-company execution packages with conflict resolution

### Cross-Platform Integration
- **Platform Detection**: Automatic identification of desktop/mobile/web requirements
- **Integration Requirements**: API contracts, shared business logic, data synchronization
- **Coordinated Execution**: Synchronized development schedules across platforms

### Multi-Company Coordination
- **Intelligent Assignment**: Optimal distribution across companies and agents
- **Dependency Resolution**: Cross-company dependency management and conflict detection
- **Resource Optimization**: Workload balancing and capacity planning

### Learning & Optimization
- **Performance Analysis**: Feedback collection and continuous improvement
- **Optimization Recommendations**: Automated suggestions for future automation runs
- **Quality Assurance**: Comprehensive validation and audit trails

## Related Skills

- `knowledge-synthesis-management` - Knowledge gathering and structuring
- `project-intelligence-analysis` - AI-driven project opportunity identification
- `issue-generation-optimization` - Advanced issue decomposition and optimization
- `multi-company-orchestration` - Cross-company execution coordination
- `learning-integration-coordination` - Continuous improvement and feedback analysis
- `ui-ux-design-coordination` - Cross-platform design coordination
- `skill-validation-remediation` - Agent skill validation and gap remediation

## Examples

### Complete Discipline Automation
```json
{
  "discipline_code": "01900",
  "automation_type": "full",
  "existing_work_assessment": true,
  "cross_platform_generation": true,
  "learning_integration": true
}
```

### Knowledge-Only Automation
```json
{
  "discipline_code": "02400",
  "automation_type": "knowledge_only",
  "confidence_threshold": 0.8,
  "source_validation": true
}
```

### Project Generation with Cross-Platform
```json
{
  "discipline_code": "01700",
  "automation_type": "project_only",
  "platforms": ["desktop", "mobile"],
  "integration_requirements": true,
  "timeline_coordination": true
}
```

### Multi-Company Orchestration
```json
{
  "discipline_code": "00850",
  "automation_type": "orchestration_only",
  "conflict_resolution": true,
  "resource_optimization": true,
  "audit_trail": true
}
```

---

*This skill routes to the Discipline Automation Agent for comprehensive workflow orchestration across the Paperclip ecosystem.*