# External service integration

Implement the integration with an external service for the user's task.

## Before you start

Read @CLAUDE.md and @.docs/BACKEND.md (if present).

## Implementation

Launch Agent(subagent_type: "integrations-expert") with the user's task.

The agent must implement the Interface + Mock + Real pattern:
1. Interface for the service
2. Mock implementation (for dev/test)
3. Real implementation (for production)
4. Service Provider binding, switched through .env

## After implementation

Launch in parallel:

Agent(subagent_type: "architecture-validator"):
- Check the Interface + Mock + Real pattern

Agent(subagent_type: "code-critic"):
- Code review of the integration (security, error handling, timeout)

If there is a BLOCK/FAIL — fix it and run the check again.

Show the user the result.
