# Prompts Memory Tool Instructions

## ⚠️ CRITICAL: MANDATORY PROMPT RECORDING ⚠️

**THE MODEL MUST RECORD EVERY USER PROMPT TO THE PROJECT-SPECIFIC PROMPTS MEMORY SYSTEM.**

All user interactions must be logged to maintain historical context and enable effective project continuity.

## Prompts Memory System Overview

### Purpose

- **Project-Specific Context**: Store all user prompts and interactions for the current project
- **Historical Continuity**: Maintain indefinite history for pattern recognition and context preservation
- **Workflow Integration**: Support commit message generation and project documentation

### Storage Location

- **File**: `memory/prompt.jsonl` (project-specific)
- **Format**: JSON Lines format with one JSON object per line
- **Persistence**: Indefinite storage - prompts are never deleted

## Mandatory Workflow

### 1. Prompt Recording

**EVERY user prompt must be recorded immediately** using this JSON structure:

```json
{
  "timestamp": "2025-08-10T15:30:45.123Z",
  "prompt": "User's complete prompt text",
  "context": {
    "branch": "current-branch-name",
    "files_modified": ["list", "of", "files"],
    "session_id": "unique-session-identifier"
  },
  "metadata": {
    "user": "andrew",
    "project": "astronautical-apogee",
    "type": "user_request"
  }
}
```

### 2. Recording Protocol

- Record prompts **before** beginning any work
- Include complete prompt text (no truncation)
- Add relevant context (branch, modified files, session info)
- Use ISO 8601 timestamp format
- Append to existing `memory/prompt.jsonl` file

### 3. Commit Integration

- **Before every commit**: Extract prompts since last commit
- Add summarized prompt context to commit message body
- Format: "Prompts addressed: [brief summary of user requests]"
- Maintain clean commit history with prompt context

### 4. Session Management

- Track related prompts within conversation sessions
- Use consistent session identifiers for multi-prompt conversations
- Preserve prompt order and conversation flow

## Implementation Guidelines

### File Operations

```bash
# Create prompt.jsonl if it doesn't exist
touch memory/prompt.jsonl

# Append new prompt (example)
echo '{"timestamp":"2025-08-10T15:30:45.123Z","prompt":"Create new feature","context":{"branch":"main"},"metadata":{"user":"andrew","project":"astronautical-apogee","type":"user_request"}}' >> memory/prompt.jsonl
```

### Context Extraction

- **Current Branch**: Extract from git status
- **Modified Files**: Track files changed during prompt execution
- **Session ID**: Generate unique identifier for conversation sessions
- **Project State**: Include relevant project context

### Prompt Categories

- `user_request`: Direct user instructions or questions
- `clarification`: User clarifications or corrections
- `approval`: User confirmations or approvals
- `feedback`: User feedback on completed work

## Quality Standards

### Complete Recording

- Record **100% of user prompts** without exception
- Include full prompt text, not summaries
- Preserve original user language and formatting

### Rich Context

- Capture relevant project state at prompt time
- Include branch information and file modifications
- Track conversation continuity with session IDs

### Structured Format

- Use consistent JSON schema for all entries
- Maintain valid JSON Lines format
- Include required timestamp, prompt, context, and metadata fields

## Maintenance Protocol

### No Pruning

- **Prompts are never deleted** - store indefinitely
- Historical context is valuable for long-term project understanding
- Full prompt history enables pattern recognition and learning

### File Management

- Monitor file size and consider rotation at project milestones
- Maintain single `prompt.jsonl` file per project
- Use append-only operations to preserve chronological order

### Backup Integration

- Prompts file is included in regular project backups
- Version control tracking for prompt history preservation

## Success Criteria

### Complete Coverage

- Every user prompt is recorded in `memory/prompt.jsonl`
- No gaps in prompt history or missing interactions
- Consistent recording across all conversation sessions

### Rich Context

- Each prompt entry includes comprehensive context information
- Project state, branch info, and session tracking are present
- Metadata enables effective filtering and analysis

### Workflow Integration

- Prompt context is included in commit messages
- Historical prompts inform current work and decision-making
- Prompts memory system supports project continuity and handoffs

**THE PROMPTS MEMORY TOOL IS MANDATORY AND MUST BE USED FOR EVERY USER INTERACTION.**
