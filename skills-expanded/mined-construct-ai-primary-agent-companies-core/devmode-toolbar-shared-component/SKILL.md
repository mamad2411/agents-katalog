---
memory_layer: durable_knowledge
para_section: pages/skills/devmode-toolbar-shared-component
gigabrain_tags: ui-frontend, development-tools, debugging, workflow-testing, modal-integration, construct-ai
openstinger_context: ui-development, modal-components, development-workflow, agent-debugging
last_updated: 2026-03-30
related_docs:
  - docs_construct_ai/codebase/procedures/ui-frontend/0000_DEVMODE_TOOLBAR_SHARED_COMPONENT_PROCEDURE.md
  - docs_construct_ai/codebase/agents/0000_README.md
related_skills:
  - correspondence-reply-modal
  - state-based-button-display
  - dropdown-implementation
frequency_percent: 65.0
success_rate_percent: 91.0
---

# DevMode Toolbar Shared Component

## Overview
Comprehensive skill for integrating Construct AI's DevModeToolbar shared component into modal interfaces, providing debugging, rule editing, and workflow testing capabilities across multiple discipline-specific modals. This skill transforms complex development tool integration procedures into structured, actionable steps for consistent development experience across all agent modals.

## When to Use This Skill
- Adding development tools to new or existing modal components
- Implementing discipline-specific workflow debugging and rule editing
- Integrating agent communication monitoring in development mode
- Ensuring consistent development experience across modal types
- Troubleshooting workflow stages and agent message handling
- Adding new discipline support to the DevModeToolbar system

## Step-by-Step Procedure

### Step 1: Import and Setup Component
**Duration:** 5-10 minutes
Import the DevModeToolbar component and set up basic integration.

- [ ] **Import DevModeToolbar**: Add import statement at the top of your modal component file
- [ ] **Identify discipline code**: Determine the appropriate discipline code (e.g., '01700' for Logistics, '01900' for Procurement)
- [ ] **Add component to render**: Include `<DevModeToolbar discipline={discipline} />` inside your modal's JSX return
- [ ] **Position appropriately**: Place the toolbar inside modal content but outside main functionality areas
- [ ] **Test basic rendering**: Verify toolbar appears when development mode is active

### Step 2: Implement Workflow Stage Events
**Duration:** 15-25 minutes
Set up event dispatching for workflow stage completion tracking.

- [ ] **Identify workflow stages**: Review your modal's workflow stages (chat, preview, documents, submit, etc.)
- [ ] **Create event dispatchers**: Add event dispatching logic to state change handlers
- [ ] **Include required details**: Ensure events include `stage`, `sessionId`, and `timestamp` in detail object
- [ ] **Use correct event naming**: Follow pattern `${discipline.toLowerCase()}_workflow_stage_completed`
- [ ] **Test event firing**: Verify events are dispatched when workflow stages change

### Step 3: Implement Agent Message Events
**Duration:** 15-25 minutes
Set up event dispatching for agent communication monitoring.

- [ ] **Identify agent interactions**: Locate where agents send messages or communicate in your modal
- [ ] **Create message dispatchers**: Add event dispatching to agent message handlers
- [ ] **Include message details**: Ensure events include `agentType`, `sessionId`, `message`, and `timestamp`
- [ ] **Use correct event naming**: Follow pattern `${discipline.toLowerCase()}_agent_message`
- [ ] **Test message events**: Verify events fire when agents communicate

### Step 4: Configure Discipline-Specific Settings
**Duration:** 10-15 minutes
Ensure your discipline is properly configured in the DevModeToolbar system.

- [ ] **Check existing configuration**: Verify your discipline exists in DevModeToolbar's disciplineConfig
- [ ] **Add new discipline if needed**: Extend configuration object with new discipline settings
- [ ] **Define event names**: Specify workflow and agent message event names
- [ ] **Set CSS selectors**: Provide modal and page selectors for element detection
- [ ] **Configure tab mappings**: Define how workflow stages map to tab names

### Step 5: Test Development Mode Integration
**Duration:** 20-30 minutes
Comprehensive testing of development mode functionality.

- [ ] **Enable development mode**: Set NODE_ENV=development or activate debug mode
- [ ] **Verify toolbar visibility**: Confirm toolbar appears in your modal
- [ ] **Test workflow events**: Check that stage changes trigger correct events
- [ ] **Test agent events**: Verify agent messages are properly dispatched
- [ ] **Test toolbar actions**: Use edit rules, edit prompt, and view metrics features
- [ ] **Cross-browser testing**: Verify functionality in target browsers

### Step 6: Handle Edge Cases and Error Conditions
**Duration:** 10-15 minutes
Implement robust error handling and edge case management.

- [ ] **Handle missing session IDs**: Ensure events work when sessionId is not available
- [ ] **Manage development mode detection**: Handle cases where dev mode detection fails
- [ ] **Graceful degradation**: Ensure modal works when toolbar fails to load
- [ ] **Event listener cleanup**: Properly remove event listeners on component unmount
- [ ] **Error logging**: Add appropriate error logging for debugging

### Step 7: Documentation and Maintenance
**Duration:** 5-10 minutes
Update documentation and prepare for ongoing maintenance.

- [ ] **Update modal documentation**: Document DevModeToolbar integration in modal docs
- [ ] **Add cross-references**: Link to DevModeToolbar procedure in related documentation
- [ ] **Version control**: Commit changes with descriptive commit messages
- [ ] **Update change logs**: Document DevModeToolbar integration in project changelogs
- [ ] **Notify development team**: Inform team about new debugging capabilities

## Success Criteria
- [ ] **DevModeToolbar renders correctly** in development mode within the modal
- [ ] **Workflow stage events dispatch properly** with correct event names and data
- [ ] **Agent message events fire accurately** when agents communicate
- [ ] **Toolbar actions function correctly** (edit rules, edit prompt, view metrics)
- [ ] **No breaking changes** to existing modal functionality in production mode
- [ ] **Cross-discipline compatibility** maintained for shared component usage
- [ ] **Error handling** prevents modal crashes when toolbar encounters issues
- [ ] **Documentation updated** with DevModeToolbar integration details

## Common Pitfalls
1. **Incorrect discipline code** - Use exact discipline codes ('01700', '01900') as defined in configuration
2. **Missing event details** - Always include sessionId, timestamp, and required fields in event details
3. **Wrong event naming pattern** - Follow lowercase discipline prefix pattern exactly
4. **Development mode not detected** - Ensure proper dev mode detection logic is in place
5. **CSS selector mismatches** - Verify selectors match actual DOM elements in your modal
6. **Event listener memory leaks** - Always clean up event listeners in useEffect cleanup
7. **Missing import statement** - DevModeToolbar must be properly imported at component top

## Cross-References

### Source Documentation
- **Primary Procedure**: `docs_construct_ai/codebase/procedures/ui-frontend/0000_DEVMODE_TOOLBAR_SHARED_COMPONENT_PROCEDURE.md`
- **Agent Architecture**: `docs_construct_ai/codebase/agents/0000_README.md`

### Related Skills
- **correspondence-reply-modal**: For modal implementations that benefit from DevModeToolbar
- **state-based-button-display**: For button state management within toolbar-integrated modals
- **dropdown-implementation**: For dropdown menus within development tool interfaces

### Agent Support
- **DevForge**: Component integration and development tool implementation
- **PromptForge**: UI/UX optimization for development interfaces
- **QualityForge**: Testing and validation of development tool functionality

## Performance Metrics
- **Average Implementation Time:** 1.5-2 hours for complete DevModeToolbar integration
- **Success Rate:** 91% - Most failures due to event naming or discipline configuration issues
- **Frequency:** 65% of modal development tasks involve DevModeToolbar integration
- **Maintenance Overhead:** <15 minutes/month for typical DevModeToolbar updates

## Example Usage

### Basic Integration Example
```javascript
import React, { useState } from 'react';
import DevModeToolbar from '../dev/DevModeToolbar';

const ProcurementModal = () => {
  const [currentStage, setCurrentStage] = useState('chat');
  const [sessionId] = useState(generateSessionId());

  const handleStageChange = (newStage) => {
    setCurrentStage(newStage);

    // Dispatch workflow stage event
    const event = new CustomEvent('procurement_workflow_stage_completed', {
      detail: {
        stage: newStage,
        sessionId: sessionId,
        timestamp: new Date().toISOString()
      }
    });
    document.dispatchEvent(event);
  };

  const handleAgentMessage = (message) => {
    // Dispatch agent message event
    const event = new CustomEvent('procurement_agent_message', {
      detail: {
        agentType: message.agentType,
        sessionId: sessionId,
        message: message.content,
        timestamp: new Date().toISOString()
      }
    });
    document.dispatchEvent(event);
  };

  return (
    <div className="modal-content">
      {/* Modal content */}
      <DevModeToolbar discipline="01900" />
    </div>
  );
};
```

### Adding New Discipline Support
```javascript
// In DevModeToolbar.js - extend disciplineConfig
const disciplineConfig = {
  // ... existing disciplines ...
  '02000': {
    label: 'Project Controls',
    stageEvent: 'project_controls_workflow_stage_completed',
    agentEvent: 'project_controls_agent_message',
    modalSelector: '.project-controls-agent-content',
    pageSelector: '.project-controls-page',
    tabMap: { /* stage to tab mapping */ },
    pageTabMap: { /* page tab mapping */ }
  }
};
```
