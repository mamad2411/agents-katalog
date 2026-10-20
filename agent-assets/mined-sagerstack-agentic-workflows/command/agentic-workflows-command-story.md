---
name: story
description: Collaborative storytelling between Claude and Cursor agents with configurable iterations
---

# Purpose

Execute collaborative storytelling between Claude and Cursor agents through a configurable iteration loop. This command creates an engaging narrative by alternating between two AI agents:

- **Claude Agent**: Provides creative story development with vivid details and plot advancement
- **Cursor Agent**: Builds collaboratively on Claude's contributions, introducing new elements while maintaining consistency

The agents work in a bidirectional loop where each agent's output becomes input for the next, creating a seamless collaborative narrative experience. The number of iterations is configurable, allowing for stories of varying length and complexity.

# Input

The command accepts three required arguments:

- **$ARGUMENTS[0]**: `story_theme` - The theme or genre for the story (e.g., "space exploration", "mystery", "fantasy adventure")
- **$ARGUMENTS[1]**: `initial_prompt` - The starting prompt that sets the scene for the story
- **$ARGUMENTS[2]**: `iteration_limit` - Number of complete iterations (must be a positive integer, each iteration includes both Claude and Cursor contributions)

**Example Usage:**
```
/story "space exploration" "brave explorers discover something unexpected" 3
/story "cyberpunk mystery" "a detective investigates digital crimes in neo-tokyo" 2
/story "fantasy quest" "heroes embark on a journey to save their realm" 4
```

**Input Validation:**
- All three arguments are required
- `story_theme` and `initial_prompt` must be non-empty strings
- `iteration_limit` must be a positive integer (1-10 recommended for optimal experience)

# Instructions

Execute the following steps to create the collaborative story:

## 1. Argument Processing and Validation
- Parse and validate all three input arguments
- Ensure `story_theme` and `initial_prompt` are meaningful strings
- Validate `iteration_limit` is a positive integer between 1-10
- If validation fails, display error message with usage examples and exit

## 2. Initialize Story Context
- Set up story variables for context passing between agents
- Initialize iteration counter and progress tracking
- Calculate total steps: `iteration_limit × 2` (claude + cursor per iteration)
- Set dynamic timeout: `(iteration_limit × 2 × 120) + 60` seconds

## 3. Execute Dynamic Iteration Loop
For each iteration from 1 to `iteration_limit`:

### 3a. Claude Agent Story Contribution
- Use Task tool to launch `storytelling-agent` with the following configuration:
  - `description`: "Claude storytelling iteration X"
  - `subagent_type`: "storytelling-agent"
  - `prompt`: Detailed storytelling prompt including:
    - Story theme: `${story_theme}`
    - Initial prompt: `${initial_prompt}` (first iteration only)
    - Previous Cursor contribution (iterations 2+)
    - Instructions to write 2-3 engaging sentences with vivid details
    - Request for raw story text output only
- Configure background CLI process execution with `run_in_background: true`
- Capture Claude agent output and store as `claude_output_X`

### 3b. Cursor Agent Story Continuation
- Use Task tool to launch `general-purpose` agent with the following configuration:
  - `description`: "Cursor storytelling iteration X"
  - `subagent_type`: "general-purpose"
  - `prompt`: Collaborative continuation prompt including:
    - Story theme: `${story_theme}`
    - Claude's contribution from step 3a
    - Instructions to build naturally on Claude's contribution
    - Request for 2-3 sentences maintaining consistency and adding new elements
    - Request for raw story text output only
- Configure background CLI process execution with `run_in_background: true`
- Capture Cursor agent output and store as `cursor_output_X`

### 3c. Progress Update
- Display iteration progress: "Iteration X of Y completed"
- Show current story segment (Claude + Cursor contributions)
- Update context variables for next iteration

## 4. Story Compilation and Final Output
- Compile all Claude and Cursor contributions in chronological order
- Format the complete story with clear section breaks
- Display story metadata (theme, total iterations, word count estimate)
- Handle any error conditions with graceful fallbacks

## 5. Error Handling
- Monitor background processes for timeouts or failures
- Implement fallback mechanisms if agents are unavailable
- Provide meaningful error messages for debugging
- Ensure graceful cleanup of background processes

# Output

The command produces structured output including:

## Progress Updates
- Real-time iteration progress: "Starting iteration X of Y..."
- Agent activity status: "Claude agent working..." / "Cursor agent responding..."
- Story segment display after each agent contribution

## Final Story Presentation
```
=== COLLABORATIVE STORY ===
Theme: [story_theme]
Iterations: [iteration_limit]

[Complete story text with clear formatting]

=== STORY METADATA ===
Total Iterations: X
Total Contributions: Y (X from Claude, X from Cursor)
Estimated Word Count: ~Z words
Execution Time: X.X seconds
```

## Error Output
- Input validation errors with usage examples
- Agent execution errors with troubleshooting guidance
- Timeout notifications with partial story recovery
- Background process management status

The output maintains narrative flow while providing transparency into the collaborative creation process, allowing users to see how each agent contributes to the evolving story.