# File storage (S3)

Implement the file handling for the user's task.

## Before you start

Read @CLAUDE.md and @.docs/BACKEND.md (if present).

## Implementation

Launch Agent(subagent_type: "s3-expert") with the user's task.

Pass the context: which files, what sizes, what formats, whether signed URLs are needed.

## After implementation

Launch in parallel:

Agent(subagent_type: "architecture-validator"):
- Check the code

Agent(subagent_type: "code-critic"):
- Code review (security: MIME validation, random filenames, no direct public access)

If there is a BLOCK/FAIL — fix it and run the check again.

Show the user the result.
