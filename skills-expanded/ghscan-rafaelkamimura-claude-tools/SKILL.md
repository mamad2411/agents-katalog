# Create New Claude Code Skill

Guides you through creating a new Claude Code skill following Anthropic's official skill structure and best practices.

## Purpose
- Create well-structured skills for Claude Code
- Follow Anthropic's progressive disclosure pattern
- Support both personal and project-specific skills
- Generate proper YAML frontmatter and instructions
- Include optional resources and scripts

## Execution Steps

### Step 1: Gather Skill Information

Output: "Let's create a new Claude Code skill!

What is the skill name? (max 64 characters, use kebab-case like 'api-builder' or 'data-analyzer'):"

WAIT for user's skill name input.

Store skill name as `SKILL_NAME`.

Output: "What does this skill do? Provide a complete description including what the skill does AND when Claude should use it (max 1024 characters):"

WAIT for user's description input.

Store description as `SKILL_DESCRIPTION`.

### Step 2: Determine Skill Scope

Use AskUserQuestion tool:
- question: "Where should this skill be installed? Personal skills are available globally across all projects. Project skills are specific to the current repository."
- header: "Skill Scope"
- multiSelect: false
- options:
  1. label: "Personal (~/.claude/skills/)", description: "Available globally in all projects"
  2. label: "Project (.claude/skills/)", description: "Only available in current project"

If user chooses Personal:
- Set `SKILL_DIR` to `/Users/nagawa/.claude/skills/${SKILL_NAME}`

If user chooses Project:
- Use Bash tool to get current directory:
  - Command: `pwd`
  - Description: "Get current working directory"
- Set `SKILL_DIR` to `${PWD}/.claude/skills/${SKILL_NAME}`

### Step 3: Check for Existing Skill

Use Bash tool to check if skill directory exists:
- Command: `test -d "${SKILL_DIR}" && echo "exists" || echo "new"`
- Description: "Check if skill directory already exists"

If result is "exists":
Output: "Warning: Skill '${SKILL_NAME}' already exists at ${SKILL_DIR}. Overwrite? (yes/no):"

WAIT for user's response.

If user says no:
- Output: "Skill creation cancelled."
- Exit command

### Step 4: Gather Skill Details

Output: "Now let's define the skill structure. I'll ask you a few questions."

Use AskUserQuestion tool:
- question: "What type of skill is this?"
- header: "Skill Type"
- multiSelect: false
- options:
  1. label: "Code Generation", description: "Generates code, builds applications, creates artifacts"
  2. label: "Analysis & Review", description: "Analyzes code, reviews files, performs audits"
  3. label: "Data Processing", description: "Processes data, generates reports, transforms files"
  4. label: "Testing & Debugging", description: "Creates tests, debugs issues, validates code"
  5. label: "Documentation", description: "Generates docs, creates guides, writes specifications"
  6. label: "Workflow Automation", description: "Automates tasks, orchestrates processes"

Store result as `SKILL_TYPE`.

Output: "What tools will this skill need access to? (comma-separated, e.g., 'Read, Write, Bash, Task')
Available tools: Read, Write, Edit, Bash, Grep, Glob, Task, AskUserQuestion, TodoWrite

Enter tools needed (or press Enter for all tools):"

WAIT for user's tools list input.

If user provides tools list:
- Parse comma-separated list into `TOOLS_LIST`

If user provides empty input:
- Set `TOOLS_LIST` to "All available Claude Code tools"

### Step 5: Create Skill Directory Structure

Use Bash tool to create skill directory:
- Command: `mkdir -p "${SKILL_DIR}"`
- Description: "Create skill directory"

### Step 6: Generate SKILL.md Content

Based on gathered information, construct SKILL.md content:

```markdown
---
name: ${SKILL_NAME}
description: ${SKILL_DESCRIPTION}
---

# ${SKILL_NAME}

## Purpose

${SKILL_DESCRIPTION}

## When to Use This Skill

Claude should invoke this skill when:
- [Auto-generate trigger conditions based on SKILL_TYPE and SKILL_DESCRIPTION]

## Available Tools

This skill has access to:
${TOOLS_LIST}

## Instructions

### Step 1: [First Major Action]

[Auto-generate steps based on SKILL_TYPE]

Use [appropriate tool] to [action]:
- [Detailed instruction following our patterns]

### Step 2: [Second Major Action]

[Continue with logical workflow steps]

## Examples

### Example 1: [Common Use Case]

**User Request**: "[Example request]"

**Skill Actions**:
1. [Action 1]
2. [Action 2]
3. [Result]

### Example 2: [Another Use Case]

**User Request**: "[Example request]"

**Skill Actions**:
1. [Action 1]
2. [Action 2]
3. [Result]

## Best Practices

- [Practice 1 based on skill type]
- [Practice 2 based on skill type]
- [Practice 3 based on skill type]

## Error Handling

- If [common error]: [Resolution]
- If [another error]: [Resolution]

## Constraints

- No network access (skills run in isolated environment)
- No runtime package installation
- Only pre-installed packages available
- Maximum instruction size: ~5000 tokens

## Notes

[Additional context or special considerations]
```

Present the generated SKILL.md content to user:

Output: "Generated SKILL.md content:

```markdown
[Show first 50 lines of generated content]
...
```

Review this skill definition. Options:
- 'ok' to save as-is
- 'edit' to make changes
- 'regenerate' to try again with different answers
- 'abort' to cancel

Your choice:"

WAIT for user's response.

If user chooses 'edit':
Output: "What changes would you like to make?"
WAIT for user's editing instructions.
Apply requested changes to SKILL.md content.
Return to presenting content for review.

If user chooses 'regenerate':
Return to Step 4.

If user chooses 'abort':
Output: "Skill creation cancelled."
Exit command.

### Step 7: Save SKILL.md File

Use Write tool to create SKILL.md:
- file_path: `${SKILL_DIR}/SKILL.md`
- content: [generated SKILL.md content]

Output: "✓ Created ${SKILL_DIR}/SKILL.md"

### Step 8: Add Optional Resources

Output: "Would you like to add additional resources to this skill?

Resources can include:
- Additional markdown files (REFERENCE.md, EXAMPLES.md, FORMS.md)
- Python scripts for complex operations
- JSON schemas for data validation
- Template files
- Example files

Add resources? (yes/no):"

WAIT for user's response.

If user says no:
Skip to Step 9.

If user says yes:

Output: "What type of resource would you like to add?
1. Additional markdown file
2. Python script
3. JSON schema
4. Template file
5. Done adding resources

Enter number (1-5):"

WAIT for user's choice.

If user chooses 1 (Additional markdown):
Output: "Enter filename (e.g., REFERENCE.md, EXAMPLES.md):"
WAIT for filename.
Output: "Enter the content for this file (or describe what it should contain):"
WAIT for content.
Use Write tool to create the file in `${SKILL_DIR}/[filename]`
Output: "✓ Created ${SKILL_DIR}/[filename]"
Return to resource type selection.

If user chooses 2 (Python script):
Output: "Enter script filename (e.g., process_data.py):"
WAIT for filename.
Output: "Enter the Python code (or describe what the script should do):"
WAIT for code content.
Use Write tool to create the script in `${SKILL_DIR}/[filename]`
Use Bash tool to make script executable:
- Command: `chmod +x "${SKILL_DIR}/[filename]"`
- Description: "Make script executable"
Output: "✓ Created ${SKILL_DIR}/[filename]"
Return to resource type selection.

If user chooses 3 (JSON schema):
Output: "Enter schema filename (e.g., config-schema.json):"
WAIT for filename.
Output: "Enter the JSON schema content:"
WAIT for schema content.
Use Write tool to create the schema in `${SKILL_DIR}/[filename]`
Output: "✓ Created ${SKILL_DIR}/[filename]"
Return to resource type selection.

If user chooses 4 (Template file):
Output: "Enter template filename (e.g., template.txt):"
WAIT for filename.
Output: "Enter the template content:"
WAIT for template content.
Use Write tool to create the template in `${SKILL_DIR}/[filename]`
Output: "✓ Created ${SKILL_DIR}/[filename]"
Return to resource type selection.

If user chooses 5 (Done):
Proceed to Step 9.

### Step 9: Validate Skill Structure

Use Bash tool to list skill directory contents:
- Command: `ls -lh "${SKILL_DIR}"`
- Description: "List skill directory contents"

Use Read tool to read the created SKILL.md file to validate:
- file_path: `${SKILL_DIR}/SKILL.md`

Perform validation checks:
1. YAML frontmatter present with 'name' and 'description'
2. Name is max 64 characters
3. Description is max 1024 characters
4. Markdown structure follows conventions
5. Instructions use explicit tool invocations

If validation fails:
Output: "Validation issues found: [list issues]"
Output: "Fix issues? (yes/no):"
WAIT for user's response.
If yes, fix issues and re-validate.

If validation passes:
Output: "✓ Skill structure validated successfully"

### Step 10: Test Skill Invocation

Output: "Skill created successfully at: ${SKILL_DIR}

To use this skill in Claude Code, invoke it with:
\`\`\`
/skill ${SKILL_NAME}
\`\`\`

Or reference the skill documentation:
\`\`\`bash
cat ${SKILL_DIR}/SKILL.md
\`\`\`

Would you like to test invoking the skill now? (yes/no):"

WAIT for user's response.

If user says yes:
Output: "Attempting to invoke skill..."

Use Skill tool:
- command: `${SKILL_NAME}`

Output: "Skill invoked. Check the output above to verify it's working correctly."

If user says no:
Output: "Skill creation complete!"

### Step 11: Add to Git (If Applicable)

If SKILL_SCOPE is "Project":

Use Bash tool to check if in git repository:
- Command: `git rev-parse --is-inside-work-tree 2>/dev/null || echo "not-git"`
- Description: "Check if current directory is in git repository"

If result is not "not-git":
Output: "This is a project-specific skill in a git repository.
Would you like to commit the skill to version control? (yes/no):"

WAIT for user's response.

If user says yes:
Use Bash tool to stage skill directory:
- Command: `git add "${SKILL_DIR}"`
- Description: "Stage skill directory"

Use Bash tool to create commit:
- Command: `git commit -m "feat: add ${SKILL_NAME} skill

Add new Claude Code skill for ${SKILL_TYPE}

${SKILL_DESCRIPTION}"`
- Description: "Commit skill to repository"

Output: "✓ Skill committed to git repository"

### Step 12: Summary

Output: "

## Skill Creation Summary

**Skill Name**: ${SKILL_NAME}
**Type**: ${SKILL_TYPE}
**Scope**: ${SKILL_SCOPE}
**Location**: ${SKILL_DIR}

**Files Created**:
[List all files created]

**Next Steps**:
1. Test the skill with: \`/skill ${SKILL_NAME}\`
2. Review and refine the SKILL.md instructions
3. Add more examples and edge cases
4. Test with real-world scenarios

**Documentation**:
- Official Docs: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview
- Skills Repository: https://github.com/anthropics/skills
- Skill File: ${SKILL_DIR}/SKILL.md

Skill creation complete!"

## Skill Type Templates

### Code Generation Template
```markdown
### Step 1: Understand Requirements
Analyze user's request for code generation needs.

### Step 2: Design Structure
Plan the code architecture and file organization.

### Step 3: Generate Code
Use Write tool to create necessary files with generated code.

### Step 4: Validate Output
Review generated code for correctness and best practices.
```

### Analysis & Review Template
```markdown
### Step 1: Gather Files
Use Read/Grep tools to collect files for analysis.

### Step 2: Perform Analysis
Analyze code structure, patterns, and potential issues.

### Step 3: Generate Report
Create detailed analysis report with findings.

### Step 4: Provide Recommendations
Suggest improvements and next steps.
```

### Data Processing Template
```markdown
### Step 1: Load Data
Use Read tool to load input data files.

### Step 2: Process Data
Transform, filter, or aggregate data as needed.

### Step 3: Generate Output
Use Write tool to save processed results.

### Step 4: Validate Results
Check output data for correctness and completeness.
```

### Testing & Debugging Template
```markdown
### Step 1: Analyze Code
Read and understand code structure for testing.

### Step 2: Generate Tests
Create comprehensive test cases.

### Step 3: Run Tests
Use Bash tool to execute test suite.

### Step 4: Debug Failures
Analyze and fix any test failures.
```

### Documentation Template
```markdown
### Step 1: Analyze Codebase
Use Grep/Read tools to understand code structure.

### Step 2: Generate Documentation
Create comprehensive documentation.

### Step 3: Format Output
Use proper markdown formatting and structure.

### Step 4: Validate Documentation
Ensure documentation is complete and accurate.
```

### Workflow Automation Template
```markdown
### Step 1: Define Workflow Steps
Break down automation into clear steps.

### Step 2: Execute Tasks
Use appropriate tools to perform each step.

### Step 3: Handle Errors
Implement error handling and recovery.

### Step 4: Report Results
Provide summary of automation results.
```

## Validation Rules

### YAML Frontmatter
- Must contain 'name' field (max 64 chars)
- Must contain 'description' field (max 1024 chars)
- Both fields are required

### File Structure
- SKILL.md is required
- Additional resources are optional
- All markdown files should use proper formatting

### Instructions Format
- Use explicit tool invocations (not bash examples)
- Follow Step 1, Step 2 structure (not nested phases)
- Include Examples section
- Include Error Handling section
- Keep total size under 5000 tokens

### Best Practices
- Clear, actionable instructions
- Concrete examples
- Proper error handling
- Progressive disclosure (load resources as needed)
- Self-contained (no external dependencies)

## Error Handling

### Skill Already Exists
- Warn user and offer to overwrite
- Back up existing skill if overwriting

### Invalid Skill Name
- Must be kebab-case
- Max 64 characters
- No special characters except hyphens

### Invalid Directory
- Check write permissions
- Create parent directories if needed

### Validation Failures
- Provide specific error messages
- Offer to fix automatically where possible

## Notes
- Skills use progressive disclosure (metadata → instructions → resources)
- Skills have no network access or runtime package installation
- Personal skills: `~/.claude/skills/`
- Project skills: `.claude/skills/`
- Follow established patterns from our slash commands
- Use explicit tool invocations following CLAUDE.md guidelines
