# Claude Code Project Guidelines

## Response Style
- **Concise Output**: Be extremely brief. Avoid conversational filler, pleasantries, and long explanations.
- **No Thinking**: Skip detailed internal monologues or "thinking out loud" in the final output unless explicitly asked.
- **Direct Answers**: Provide the solution or the code immediately. 
- **Minimalist Explanations**: Use bullet points for technical justifications. Only explain *why* if the change is non-obvious.
- **Token Optimization**: Prioritize brevity to reduce token consumption.

## Technical Preferences
- Match existing naming conventions and comment density.
- Preserve comments that explain Kafka API behavior or highlight critical implementation details (e.g., timeout logic, API specifics) as they serve as learning aids. Other comments are optional.
- Prefer dedicated tools over shell commands.
