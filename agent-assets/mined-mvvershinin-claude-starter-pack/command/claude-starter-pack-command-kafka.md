# Kafka integration

Implement the Kafka producer/consumer for the user's task.

## Before you start

Read @CLAUDE.md and @.docs/BACKEND.md (if present).

## Implementation

Launch Agent(subagent_type: "kafka-expert") with the user's task.

Pass the context: topics, message format, consumer groups, whether a Schema Registry is needed.

## After implementation

Launch in parallel:

Agent(subagent_type: "architecture-validator"):
- Check the code

Agent(subagent_type: "code-critic"):
- Code review (security, error handling, DLQ)

If there is a BLOCK/FAIL — fix it and run the check again.

Show the user the result.
