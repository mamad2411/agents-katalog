---
name: edit-with-ai-pattern
description: This skill should be used when building "Edit with AI" features that enable natural language editing of application settings, configurations, or data. It applies when implementing conversational UI for editing forms, creating AI-powered popover interfaces, or adding session-scoped tools for AI-driven CRUD operations. Triggers on requests like "add Edit with AI button", "create AI editing interface", "implement conversational form", or building features where users type natural language requests to modify application state.
---

# Edit with AI Pattern

## Overview

The "Edit with AI" pattern enables natural language editing of any application feature through a consistent, reusable architecture. Users type requests like "change the time to 3pm" or "update the settings to include X" and the AI agent handles parsing and execution via session-scoped tools.

**Key Use Cases:**
- Scheduler: Edit schedules with natural language ("make it run at 3pm")
- Templates: Create/modify presets conversationally ("save this as my code review template")
- Sources/Integrations: Add connections via description ("connect to my Slack workspace")
- Configuration: Update settings through conversation ("block all write operations")
- Any feature with complex forms that benefit from natural language input

## Architecture

The pattern consists of 5 interconnected components that enable the complete flow:

```
User clicks "Edit with AI" button
        ↓
EditPopover opens (text input with context)
        ↓
Opens Focused Chat Window via deep link (app://action/new-chat?...)
        ↓
AI Agent receives context + session-scoped tool
        ↓
Agent parses natural language, asks clarifying questions
        ↓
Agent calls session-scoped tool (e.g., schedule_update)
        ↓
VesperAgent callback → Main Process IPC
        ↓
Feature service executes action
        ↓
Broadcasts event to UI for reactivity
```

## Implementation Checklist

To add "Edit with AI" to a new feature, implement these 5 components in order:

### Component 1: EditContext Key (EditPopover.tsx)

Define a unique context key and configuration for the new feature in the EditPopover component:

```typescript
// 1. Add to EditContextKey type
export type EditContextKey =
  | 'existing-keys'
  | 'edit-your-feature'  // Add your key

// 2. Add configuration to EDIT_CONFIGS
'edit-your-feature': (location) => ({
  context: {
    label: 'Edit Your Feature',
    filePath: location,  // JSON string with current state OR file path
    context:
      'The user is editing [feature]. Parse their request and use the ' +
      'your_feature_update tool. Current state is provided below. ' +
      'Ask clarifying questions if the request is ambiguous.',
  },
  example: 'Change the setting to X',
  overridePlaceholder: 'How would you like to change this?',
}),
```

**Key Configuration Fields:**
- `label`: Human-readable name for badge display
- `filePath`: Either a file path OR JSON-stringified current state
- `context`: Instructions for the AI agent on how to handle requests
- `example`: Example request shown in placeholder text
- `overridePlaceholder`: Custom placeholder for the text input

### Component 2: Session-Scoped Tool (session-scoped-tools.ts)

Create a tool that executes within agent sessions with callback registry:

```typescript
// 1. Define data types for input and output
export interface YourFeatureUpdateData {
  featureId: string;
  // All update fields should be optional (partial updates)
  name?: string;
  setting?: string;
  enabled?: boolean;
}

export interface YourFeatureUpdateResult {
  success: boolean;
  featureId?: string;
  featureName?: string;
  error?: string;
}

// 2. Add callback to SessionScopedToolCallbacks interface
export interface SessionScopedToolCallbacks {
  // ... existing callbacks
  onYourFeatureUpdate?: (data: YourFeatureUpdateData) => Promise<YourFeatureUpdateResult>;
}

// 3. Create the tool factory function
export function createYourFeatureUpdateTool(sessionId: string) {
  return tool(
    'your_feature_update',
    `Update an existing [feature].

**Required:** featureId
**Optional fields:** name, setting, enabled, etc.

Always confirm changes with the user before updating.`,
    {
      featureId: z.string().describe('ID of the feature to update'),
      name: z.string().optional().describe('New name'),
      setting: z.string().optional().describe('New setting value'),
      enabled: z.boolean().optional().describe('Enable/disable'),
    },
    async (args) => {
      const callbacks = sessionScopedToolCallbackRegistry.get(sessionId);

      if (!callbacks?.onYourFeatureUpdate) {
        return {
          content: [{ type: 'text' as const, text: 'Feature update not available.' }],
          isError: true,
        };
      }

      try {
        const result = await callbacks.onYourFeatureUpdate(args);

        if (result.success) {
          return {
            content: [{
              type: 'text' as const,
              text: `✓ "${result.featureName}" updated successfully!`
            }],
            isError: false,
          };
        } else {
          return {
            content: [{ type: 'text' as const, text: `Failed: ${result.error}` }],
            isError: true,
          };
        }
      } catch (error) {
        return {
          content: [{
            type: 'text' as const,
            text: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`
          }],
          isError: true,
        };
      }
    }
  );
}

// 4. Register in getSessionScopedTools()
cached = createSdkMcpServer({
  tools: [
    // ... existing tools
    createYourFeatureUpdateTool(sessionId),
  ],
});
```

### Component 3: VesperAgent Callback (vesper-agent.ts)

Wire up the callback property on the agent class:

```typescript
// 1. Add callback property to VesperAgent class
public onYourFeatureUpdate: ((data: YourFeatureUpdateData) => Promise<YourFeatureUpdateResult>) | null = null;

// 2. Wire up in registerSessionScopedToolCallbacks() during agent initialization
registerSessionScopedToolCallbacks(sessionId, {
  // ... existing callbacks
  onYourFeatureUpdate: async (data) => {
    this.onDebug?.(`[VesperAgent] onYourFeatureUpdate received: ${data.featureId}`);
    if (this.onYourFeatureUpdate) {
      return this.onYourFeatureUpdate(data);
    }
    return { success: false, error: 'Feature update not available' };
  },
});
```

### Component 4: Main Process Handler (sessions.ts)

Implement the actual business logic in the session manager:

```typescript
// Wire up the callback when session is created in the session manager
managed.agent.onYourFeatureUpdate = async (data): Promise<YourFeatureUpdateResult> => {
  sessionLog.info(`Feature update request for session ${managed.id}:`, data.featureId);

  try {
    // Get the appropriate service for this feature
    const service = getYourFeatureService(managed.workspace.id);

    // Execute the update operation
    const result = await service.update(data.featureId, {
      name: data.name,
      setting: data.setting,
      enabled: data.enabled,
    });

    // Broadcast event for UI reactivity
    broadcast({
      type: 'your-feature-updated',
      featureId: result.id,
    }, managed.workspace.id);

    return {
      success: true,
      featureId: result.id,
      featureName: result.name,
    };
  } catch (error) {
    sessionLog.error(`Failed to update feature:`, error);
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
    };
  }
};
```

### Component 5: UI Button with EditPopover

Add the "Edit with AI" button to the feature's detail panel:

```tsx
import { EditPopover, getEditConfig } from '@/components/ui/EditPopover'
import { Sparkles } from 'lucide-react'

// Build context with current state
const editConfig = useMemo(() => {
  const context = JSON.stringify({
    featureId: feature.id,
    name: feature.name,
    setting: feature.setting,
    enabled: feature.enabled,
  });
  return getEditConfig('edit-your-feature', context);
}, [feature]);

// Render button with EditPopover
{workspaceId && (
  <EditPopover
    trigger={
      <Button size="sm" variant="outline" className="gap-2">
        <Sparkles className="w-3 h-3" />
        Edit with AI
      </Button>
    }
    context={editConfig.context}
    example={editConfig.example}
    overridePlaceholder={editConfig.overridePlaceholder}
    workspaceId={workspaceId}
    // Optional: Add secondary action for advanced/manual editing
    secondaryAction={{
      label: 'Advanced',
      onClick: () => setShowAdvancedModal(true),
    }}
  />
)}
```

## Best Practices

### Context Design
1. **Include current state**: Pass all relevant current values in the context so AI knows what's being edited
2. **Be specific**: Tell the AI exactly which tool to use and what the fields mean
3. **Request clarification**: Instruct the agent to ask clarifying questions if requests are ambiguous

### Tool Design
1. **Partial updates**: Make all update fields optional for flexible partial updates
2. **Validation**: Validate inputs in the tool before calling callbacks
3. **Clear feedback**: Return detailed success/error messages for the AI to relay

### UX Design
1. **Confirm before executing**: Have the agent confirm changes with the user before calling the tool
2. **Good examples**: The `example` field helps users understand what to type
3. **Secondary action**: Include an "Advanced" button for users who prefer manual forms
4. **Handle missing callbacks**: Always check if callback exists before calling

### Error Handling
1. **Graceful degradation**: Return helpful error messages when callbacks aren't available
2. **Log errors**: Log errors in the session manager for debugging
3. **Broadcast updates**: Emit events so UI can react to changes

## Key Files Reference

| Component | Typical Location |
|-----------|------------------|
| EditPopover + Context Registry | `apps/*/src/renderer/components/ui/EditPopover.tsx` |
| Session-Scoped Tools | `packages/shared/src/agent/session-scoped-tools.ts` |
| VesperAgent Callbacks | `packages/shared/src/agent/vesper-agent.ts` |
| Agent Package Exports | `packages/shared/src/agent/index.ts` |
| Session Manager | `apps/*/src/main/sessions.ts` |

## Resources

This skill includes reference documentation for the complete implementation:

### references/
- `architecture.md` - Detailed architecture documentation with data flow diagrams
- `implementation-examples.md` - Real-world implementation examples from Vesper (schedule editing, source management, etc.)
