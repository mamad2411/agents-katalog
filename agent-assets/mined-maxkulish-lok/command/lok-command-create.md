# /design-doc:create - Create Design Documents from Linear Tasks

**Purpose**: Fetch Linear task details and generate a structured design document for the project, following established architecture patterns.

**Usage**:
- `/design-doc:create [clo-XX]` - Create design doc from Linear task
- `/design-doc:create [clo-XX] --probe` - Include discovery probe results in Prior Research
- `/design-doc:create` - Interactive mode

---

## Project Context

| Setting | Value |
|---------|-------|
| Linear Workspace | cloud-ai |
| Issue Prefix | CLO (e.g., CLO-123) |
| Branch Format | `{prefix}/clo-<number>-<short-desc>` (prefix: feat, fix, chore) |

---

## Command Execution Instructions

When this command is invoked, follow these steps:

### Step 1: Extract Task Number

1. **If user provided task number** (e.g., `/design-doc:create clo-36`):
   - Extract the CLO-XX identifier
   - Check for `--probe` flag (enables inclusion of discovery probe results, see Step 3.7)
   - Normalize to uppercase for Linear API (e.g., "clo-36" -> "CLO-36")
   - Proceed to Step 2

2. **If no task number provided** (e.g., `/design-doc:create`):
   - Ask user: "Which Linear task do you want to create a design document for? (e.g., CLO-36)"
   - Wait for response
   - Extract and normalize the task number
   - Proceed to Step 2

### Step 2: Fetch Linear Task Details

**Use Linear MCP to get task information**:

```
mcp__linear-server__get_issue(id="CLO-XX")
```

**Extract from response**:
- `title`: Task title
- `description`: Full task description (may contain requirements, context)
- `state.name`: Current status
- `labels`: Any labels/tags
- `assignee`: Assigned developer

**Also fetch comments** for additional context:

```
mcp__linear-server__list_comments(issueId="CLO-XX")
```

**If task not found**:
- Display error: "Linear task CLO-XX not found."
- Ask user if they want to create a design doc without Linear context
- If yes: Proceed to Step 3 (Manual Mode)
- If no: Exit command

### Step 3: Read Architecture Document (if exists)

**Check for architecture document**: `docs/arch` or `docs/architecture.md`

**If found, extract relevant context**:
- Overall system architecture
- Technology stack
- Design patterns and conventions
- Integration points

**If not found**: Continue without architecture reference.

### Step 4: Generate Short Description

**From the Linear task title**, generate a URL-friendly short description:

1. Take the task title
2. Convert to lowercase
3. Replace spaces with hyphens
4. Remove special characters
5. Truncate to ~30 chars if needed

**Examples**:
- "Add User Authentication" -> `user-authentication`
- "Implement WebSocket Support" -> `websocket-support`
- "Create CLI Parser Module" -> `cli-parser-module`

### Step 5: Generate Design Document

**Create file**: `docs/design-docs/clo-XX-[short-description].md`

**Required format**:

```markdown
# CLO-XX: [Task Title]

**Linear Task**: https://linear.app/cloud-ai/issue/CLO-XX
**Status**: Design
**Author**: [from Linear assignee or "Team"]
**Created**: [Current Date]

---

## Summary

[2-3 sentence summary of what this task accomplishes and why it's needed]

---

## Background

[Context from Linear task description]
[How this fits into the overall architecture]
[Any relevant prior discussions or decisions]

### Prior Research

[If `--probe` flag was used: Include discovery probe results from `/tmp/clo-XX-probe-ollama.md` and Perplexity output. Summarize key approaches, risks, and edge cases identified during the discovery probe. If no `--probe` flag: omit this subsection.]

---

## Architecture

### Component Overview

[Describe where this component fits in the overall system]

```mermaid
[Include relevant portion of the architecture diagram, or create a focused diagram]
```

### Affected Components

| Component | Change Type | Description |
|-----------|-------------|-------------|
| `[component]/` | New/Modified | [What changes] |

### Dependencies

- **Internal**: [Other modules this depends on]
- **External**: [External dependencies, libraries, services]

---

## Detailed Design

### Implementation Approach

[Describe the technical approach]

### Code Structure

```rust
// Key structure definitions or module layout
```

### API/Interface Design

| Function/Method | Parameters | Returns | Description |
|-----------------|------------|---------|-------------|
| [name] | [params] | [type] | [Description] |

---

## Implementation Plan

### Phase 1: [Phase Name]

- [ ] Task 1
  - [ ] Subtask 1.1
  - [ ] Subtask 1.2
- [ ] Task 2

### Phase 2: [Phase Name]

- [ ] Task 3
- [ ] Task 4

### Phase 3: Testing & Validation

- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

---

## Constraints

**Must**:
- [Hard requirements that cannot be violated - architecture rules, safety invariants]

**Must-not**:
- [Forbidden approaches - e.g., "must not block the tokio runtime"]

**Prefer**:
- [Soft preferences - e.g., "prefer existing error types over new ones"]

**Escalate when**:
- [Conditions that require stopping and asking the user - e.g., "if Backend trait changes are needed"]

---

## Acceptance Criteria

Each criterion must be specific, measurable, and verifiable with a command or exact manual step.

- [ ] [Criterion 1 — e.g., "`cargo test backend` passes with 0 failures"]
- [ ] [Criterion 2 — e.g., "`cargo test` passes with new functionality"]
- [ ] [Criterion 3 — e.g., "lok.toml config changes are backward compatible"]

**Verification method**: [How to run all criteria — e.g., `cargo test && cargo clippy`]

---

## Evaluation

Measurable test cases proving the implementation is correct. Add these BEFORE starting implementation.

| # | Test | Expected Result | Command / Steps |
|---|------|-----------------|-----------------|
| 1 | [test description] | [exact expected output] | [command or numbered steps] |
| 2 | | | |

**Edge cases to cover**:
- [e.g., what happens when LLM backend becomes unavailable mid-query?]
- [e.g., what happens on config schema mismatch with existing lok.toml?]

---

## Testing Strategy

- **Unit Tests**: [What to test at unit level, specific function names if known]
- **Integration Tests**: [Integration test approach]
- **Manual Testing**: [Exact steps to verify manually]

---

## Open Questions

- [ ] [Any unresolved questions from Linear task or comments]

---

## References

- [Linear Task](https://linear.app/cloud-ai/issue/CLO-XX)
- [Architecture Document](../arch) (if exists)
```

### Step 5b: Fill in Constraints and Evaluation (REQUIRED)

After generating the template, **actively populate** these sections — do not leave them as placeholders:

**Constraints**:
- Check `docs/context/system-patterns.md` for invariants that apply (e.g., Cleanup must never lose text)
- Check `CLAUDE.md` Escalation Triggers — any that apply here become Must/Must-not constraints
- Add at least one Escalate-when trigger specific to this task

**Acceptance Criteria**:
- Every criterion must include a verification method (specific `cargo test` filter, or numbered manual steps)
- Avoid generic items like "all tests pass" — specify which tests and what they should output
- Aim for 3-5 criteria that cover the happy path, one error path, and one integration point

**Evaluation table**:
- Add at least one row per Acceptance Criterion
- Include edge cases from the task domain (LLM backend becomes unavailable mid-query, config migration, API failures)

### Step 6: Customize Based on Task Type

**Adjust template sections** based on task type:

#### For API/Backend Tasks:
- Add endpoint definitions
- Include request/response schemas
- Reference database changes if any

#### For CLI Tasks:
- Add command usage examples
- Include argument parsing details
- Add help text formatting

#### For Library/Module Tasks:
- Add public API documentation
- Include usage examples
- Document error types

### Step 7: Post Design Doc Link to Linear

**Use Linear MCP to create comment**:

```
mcp__linear-server__create_comment(
  issueId="CLO-XX",
  body="## Design Document Created

A design document has been created for this task.

**Document**: `docs/design-docs/clo-XX-[description].md`

**Key Sections**:
- Summary & Background
- Architecture & Dependencies
- Detailed Design
- Implementation Plan
- Acceptance Criteria

Please review the design document and provide feedback before implementation begins.

**Next Steps**:
1. Review design document
2. Address open questions
3. Begin implementation"
)
```

### Step 8: Create Git Branch

**Create a git branch** following the naming convention for Linear-GitHub integration:

**Branch naming format**: `{prefix}/clo-<number>-<short-desc>` (prefix: feat, fix, chore; 2-3 words max)

The branch name MUST include the issue identifier (e.g., `clo-5`) so Linear can automatically link commits and pull requests to the issue.

**Generate branch name**:
1. Take the issue identifier (e.g., `CLO-6`)
2. Convert to lowercase (e.g., `clo-6`)
3. Append the short description from Step 4 (e.g., `websocket-support`)
4. Result: `feat/clo-6-websocket-support`

**Create and checkout the branch**:
```bash
git checkout -b feat/clo-<number>-<short-description>
```

**Example**:
```bash
git checkout -b feat/clo-6-websocket-support
```

**Important**: The branch name format ensures:
- Linear automatically links the branch to the issue
- GitHub PRs are tracked in Linear
- Commits on this branch appear in the Linear issue timeline

### Step 9: Update Linear Task State (Optional)

**Ask user**: "Would you like to update the Linear task status to 'In Progress'? (yes/no)"

If yes:
```
mcp__linear-server__update_issue(id="CLO-XX", state="In Progress")
```

### Step 10: Confirm to User

```
SUCCESS: Design document created!

File: docs/design-docs/clo-XX-[description].md
Branch: feat/clo-XX-[description]
Linear: Comment posted to CLO-XX

Document sections:
- Summary
- Background (from Linear task)
- Architecture
- Detailed Design
- Implementation Plan
- Acceptance Criteria

Next steps:
1. Review: docs/design-docs/clo-XX-[description].md
2. Update open questions
3. Get design review/approval
4. Push branch: git push -u origin feat/clo-XX-[description]
5. Begin implementation
```

---

## Special Cases

### Case 1: docs/design-docs/ folder doesn't exist

- Create folder: `mkdir -p docs/design-docs`

### Case 2: Design doc already exists

```
Design document already exists: docs/design-docs/clo-XX-[description].md

Options:
1. [overwrite] - Regenerate and overwrite
2. [open] - Open existing document (exit command)
3. [cancel] - Exit without changes

Your choice:
```

### Case 3: Linear task has no description

```
WARNING: Linear task CLO-XX has no description

The design document will have limited context. You can:
1. [continue] - Create design doc with minimal context
2. [cancel] - Exit and add description to Linear first

Your choice:
```

If continue: Generate template with placeholders for user to fill in.

---

## Example Execution

**User input**: `/design-doc:create clo-10`

**Command execution**:

1. Extract task: CLO-10
2. Fetch from Linear:
   - Title: "Implement WebSocket Handler"
   - Description: "Create WebSocket support for real-time communication..."
3. Read architecture doc for context (if exists)
4. Identify component: networking/websocket
5. Generate short description: `websocket-handler`
6. Create: `docs/design-docs/clo-10-websocket-handler.md`
7. Post comment to Linear CLO-10
8. Create branch: `git checkout -b feat/clo-10-websocket-handler`
9. Ask about status update
10. Confirm: "SUCCESS: Design document created!"

---

## Implementation Notes

- Use `mcp__linear-server__get_issue` to fetch task details
- Use `mcp__linear-server__list_comments` to get additional context
- Use `Read` tool to read architecture documents
- Use `Write` tool to create design document
- Use `mcp__linear-server__create_comment` to post link
- Use `Bash` with `mkdir -p` to create directories if needed
- Follow branch naming: `feat/clo-XX-short-desc` (not `clo-XX-description`)
