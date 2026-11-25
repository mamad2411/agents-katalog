# Chat Area Design Principles

- **Chronological Ordering**: All elements in the chat area must be rendered in strict chronological order. This includes:
  - User messages appear when sent
  - Tool call accordions appear when the model invokes a tool
  - Tool results (e.g., SQL tables) appear AFTER their corresponding tool call accordion
  - Model commentary appears after tool results
  - **Guardrail**: Never reorder elements for aesthetic reasons. The visual flow must match the actual execution timeline.
- **Formatted Results Visible**: When tool calls successfully return end-user data (e.g., SQL query results), display the formatted/parsed result prominently in the main chat area (not hidden inside an accordion). The accordion should contain raw request/response data and errors for debugging.
