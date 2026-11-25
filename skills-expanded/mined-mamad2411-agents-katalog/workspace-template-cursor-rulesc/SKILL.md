---
description: 
globs: 
alwaysApply: false
---
# Cursor Workspace Rules

## Project Overview
This workspace is designed to implement a Human-in-the-loop system with Cursor IDE, leveraging long-term memory to create and manage reusable tasks. The system learns from human interactions and builds a knowledge base of common tasks and solutions.

## Core Concepts

### Human-in-the-Loop
- Human interactions guide AI behavior and task execution
- Feedback loops improve task execution over time
- Human expertise is captured and preserved in the system

### Long-term Memory
- Persistent storage of successful task executions
- Accumulation of knowledge from human interactions
- Context preservation for future task execution

### Temporary Memory
- Short-term storage for ongoing tasks
- Experimental and trial-and-error space
- Pre-verification area before long-term storage
- Context for current work session
- Must be cleaned up after task completion

## Directory Structure

### memory/
- Stores Cursor's long-term memory
- Maintains context and history of successful interactions
- Preserves learned patterns and solutions
- Used for building a knowledge base of reusable tasks
- Only verified and valuable information is stored here

### temp/
- Temporary storage for current work session
- Experimental space for new tasks
- Pre-verification area for memory candidates
- Context for ongoing tasks
- Must be cleaned up after task completion
- No long-term storage of information

### prompts/
- Contains procedural documents and instructions
- Stores templates for common tasks
- Documents successful human-AI interaction patterns
- Houses guidelines for task execution

### resources/
- Read-only directory for user-provided files
- Cursor can read but cannot modify these files
- Users can freely add and manage their own files
- Useful for storing reference materials and static assets

### src/
- Active development workspace
- Implementation of new tasks and solutions
- Testing and refinement of learned patterns
- Integration of human feedback

### .cursor/
- Cursor-specific configuration
- System rules and guidelines
- Memory management policies
- This rules document

## Usage Guidelines

1. Maintain clear separation between memory storage and active development
2. Document successful human-AI interactions in prompts/
3. Use memory/ to build a knowledge base of reusable tasks
4. Implement new tasks in src/ based on learned patterns
5. Follow the rules defined in this document for consistency

## Best Practices

1. Regularly review and update the knowledge base in memory/
2. Document new successful interaction patterns in prompts/
3. Clean and organize src/ after task completion
4. Update this rules document when adding new guidelines
5. Maintain clear context in memory/ for future reference

## Memory Management

1. Store only relevant and successful task executions
2. Maintain clear context for each stored memory
3. Regularly review and clean up outdated memories
4. Use structured formats for memory storage
5. Link related memories for better context preservation

## Temporary Memory Management

1. Use temp/ for ongoing work and experiments
2. Clean up temp/ immediately after task completion
3. Move only verified and valuable information to memory/
4. Delete all temporary files after successful migration to memory/
5. Never use temp/ for long-term storage
6. Keep temp/ organized during active use
7. Document the migration process from temp/ to memory/

## Resources Directory Rules

1. Files in resources/ are read-only for Cursor
2. Users have full control over file management in resources/
3. Cursor can reference but cannot modify files in resources/
4. Use resources/ for storing reference materials and static assets
5. Keep resources/ organized and well-documented
