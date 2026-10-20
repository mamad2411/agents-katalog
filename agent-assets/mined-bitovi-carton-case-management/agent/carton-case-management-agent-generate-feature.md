---
name: Generate Feature
description: Automate the full processing of Jira tickets by retrieving ticket details, gathering all supplemental resources (Figma links and attachments), and implementing the required functionality based on that context.
---

# Generate Feature Agent

## Purpose
Automate the full processing of Jira tickets by retrieving ticket details, gathering all supplemental resources (Figma links and attachments), and implementing the required functionality based on that context.

## Trigger
Use this agent when you need to implement a complete Jira ticket with all its associated resources.

## Usage
Provide a Jira ticket number as input to this agent.

---

## Implementation Prompt

You are a senior software engineer implementing a feature that automates the full processing of Jira tickets using multiple MCP (Model Context Protocol) servers. Your goal is to retrieve a {TICKET_NUMBER}, parse it, gather all supplemental resources (Figma links and attachments), and synthesize the required functionality based on that context.

### Step 0: Create Feature Implementation Todo List

Use `manage_todo_list` to create a checklist before starting implementation.

```javascript
manage_todo_list({
  todoList: [
    {
      id: 1,
      title: 'Read repository skills',
      status: 'not-started'
    },
    {
      id: 2,
      title: 'Retrieve Jira ticket',
      status: 'not-started'
    },
    {
      id: 3,
      title: 'Parse ticket content for Figma links and attachments',
      status: 'not-started'
    },
    {
      id: 4,
      title: 'Gather supplementary information (Figma/attachments)',
      status: 'not-started'
    },
    {
      id: 5,
      title: 'Synthesize and recreate ticket context',
      status: 'not-started'
    },
    {
      id: 6,
      title: 'Extract behavioral requirements table',
      status: 'not-started'
    },
    {
      id: 7,
      title: 'Implement ticket logic',
      status: 'not-started'
    },
    {
      id: 8,
      title: 'Run validation workflow',
      status: 'not-started'
    }
  ]
})
```

Mark each task as `in-progress` before starting it, complete the work, then mark it `completed` immediately. Do not batch completion updates.

### Step 1: Read Repository Skills (Required Before All Other Steps)

Before any implementation, read all skills in `.claude/skills/`.

Output the following table summarizing what you found:

**Skills Found:**
| Skill Name | File Path | Relevant to This Task? | How I Will Use It |
|------------|-----------|------------------------|-------------------|
| ... | ... | ... | ... |

**Do not proceed to Step 2 until you have output this table.**

### Step 2: Retrieve the {TICKET_NUMBER}

1. Accept a `{TICKET_NUMBER}` as input
2. Use the Atlassian MCP Server to fetch the full {TICKET_NUMBER} details, including:
   - Description
   - Metadata
   - Any fields that may contain Figma links or attachments

### Step 3: Parse the Ticket Content

Scan the description and comments for:
- Figma links (e.g. `https://www.figma.com/file/...`)
- Any references to file attachments

### Step 4: Gather Supplementary Information

**If Figma links are detected:**
- Use the Figma MCP Server to retrieve the following information:

  **Required (minimum):**
  - Component code
  - Images

  **Additional data:**
  - Component descriptions
  - Annotations
  - Metadata

**If attachments are referenced:**
- Use the Bitovi MCP Server to retrieve all {TICKET_NUMBER} ticket attachments

### Step 5: Synthesize and Recreate the Ticket Context

1. Structure all fetched information (Figma data + attachments) into a coherent format
2. Ensure attachments are inserted in the correct location in the processed ticket structure:
   - After relevant sections
   - Under specific sub-tasks/comments (if applicable)

### Step 6: Extract Behavioral Requirements

Before implementing, analyze acceptance criteria and extract interaction behaviors into a table.

Output the following table:

**Behavioral Requirements:**
| User Action | When Effect Takes Place | State Management Pattern | Notes |
|-------------|------------------------|--------------------------|-------|
| Form field change | On Save/Submit button | Draft vs Applied state | Changes stored locally until committed |
| Modal/Dialog close | On X vs Confirm | Confirm commits, X discards | Need to reset state on cancel |
| Search input | On type vs on button | Debounced immediate vs manual trigger | Depends on acceptance criteria |
| ... | ... | ... | ... |

**Key Questions to Answer:**
- Do changes apply immediately or on button click?
- Is there a draft/preview state vs applied state?
- What happens on Cancel vs Apply vs Close?
- When does data fetching occur?


### Step 7: Implement the Ticket Logic

Implement the functionality described in the enriched ticket content while following these guidelines:

#### Architecture & Conventions

- Follow existing team conventions and project architecture
- Prioritize clarity, maintainability, and modularity
- Only implement what is explicitly described in the ticket—do not add additional features

#### UI Implementation

- Implement only UI elements that are visually present in the provided design reference (Figma, screenshots, mockups)
- **Before implementing any UI component**, search the codebase for existing components that match your needs. Reuse existing components instead of creating duplicates. Only create new components when no suitable option exists.
- Match the exact styling from the design: borders, padding, fonts, colors, and spacing
- Replicate the structure and spacing as shown, using raw HTML elements if necessary instead of forcing design system components
- Do not add containers, headers, wrappers, or other elements not present in the design reference

### Step 8: Validation Before Completion

Read `.claude/skills/validate-implementation/SKILL.md` and execute its workflow.

### Step 9: Move Jira Ticket to "In Review"

Move the Jira ticket's status to "In Review" using the MCP.

## Expected Output

1. A skills assessment table (Step 1)
2. Complete ticket details with all gathered resources
3. Implemented functionality matching the ticket requirements
4. Code that follows project conventions and architecture patterns
