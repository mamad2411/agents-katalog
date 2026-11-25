# Skill Activation Guide Template

This guide provides a structured approach for loading and applying a skill's instructions to accomplish tasks.

## Overview

Activating a skill means loading its content, understanding its purpose, and applying its instructions to the current task. This guide walks through the complete activation process.

## Skill Information to Gather

Before activating a skill, collect:

- **Name**: The skill's identifier
- **Description**: What the skill does
- **Path**: Location of the skill directory
- **SKILL.md Path**: Location of the main skill file
- **Table of Contents**: Structure of the skill document
- **References**: Available reference documentation
- **Scripts**: Available executable scripts

## Activation Instructions

### Step 1: Load the Skill Content

Read the full SKILL.md file to understand:

- Instructions for when and how to apply this skill
- Code examples and patterns to follow
- References to additional documentation
- Prerequisites and dependencies

**Action**: Read the SKILL.md file completely before proceeding.

### Step 2: Understand the Skill's Purpose

After reading the SKILL.md, identify:

| Aspect | Questions to Answer |
|--------|---------------------|
| **Primary Use Cases** | What problems does this skill solve? |
| **Prerequisites** | What must be in place before using it? |
| **Dependencies** | What tools or systems are required? |
| **Expected Inputs** | What information does the skill need? |
| **Expected Outputs** | What will the skill produce? |

### Step 3: Load References as Needed

If the skill includes reference documentation in the `references/` directory:

1. **Identify Available References**
   - List all files in the `references/` directory
   - Note the topic each reference covers

2. **Load References On-Demand**
   - Load a reference when you need detailed information about its topic
   - Don't load all references upfront unless necessary

3. **Reference Loading Pattern**
   ```
   When you need info about [topic]:
     Load: [skill-path]/references/[topic-file].md
   ```

### Step 4: Script Execution

If the skill includes executable scripts in the `scripts/` directory:

#### Before Executing Any Script

1. **Verify Appropriateness**
   - Is this script suitable for the current task?
   - Does the task require script execution?

2. **Understand the Script**
   - Read the script contents first
   - Understand what it will do
   - Identify any side effects

3. **Prepare Arguments**
   - Review the script's expected arguments
   - Gather required input values
   - Validate inputs before execution

#### During Execution

1. **Execute with Proper Arguments**
   - Pass arguments as documented
   - Use appropriate quoting for values

2. **Monitor Output**
   - Watch for error messages
   - Capture output for later use if needed

3. **Handle Errors Gracefully**
   - Don't proceed if a script fails
   - Report errors with context
   - Attempt recovery if appropriate

#### Script Execution Checklist

- [ ] Script contents reviewed
- [ ] Purpose understood
- [ ] Arguments prepared
- [ ] Execution environment appropriate
- [ ] Error handling planned

### Step 5: Apply the Skill

Follow the skill's instructions for your current task:

1. **Follow the Documented Process**
   - Work through the skill's steps in order
   - Don't skip steps unless explicitly allowed

2. **Use Provided Patterns**
   - Apply code examples as templates
   - Follow naming conventions shown
   - Maintain consistency with examples

3. **Reference Documentation When Needed**
   - Consult references for detailed guidance
   - Don't guess when documentation exists

4. **Execute Scripts Appropriately**
   - Run scripts when the task calls for them
   - Use scripts as intended by the skill

## Important Notes

### Security Considerations

- Always verify script contents before execution
- Follow any security guidelines mentioned in the skill
- Report any suspicious or unexpected behavior
- Don't execute scripts that access sensitive data unnecessarily

### Best Practices

- Read the entire SKILL.md before starting
- Understand the "why" not just the "how"
- Ask for clarification if instructions are unclear
- Document any deviations from standard process

### When Skills Don't Apply

A skill may not be appropriate when:

- The task falls outside the skill's stated purpose
- Prerequisites cannot be met
- Dependencies are unavailable
- The skill's approach conflicts with requirements

## Activation Workflow Summary

```
1. LOAD
   └── Read SKILL.md completely

2. UNDERSTAND
   ├── Identify use cases
   ├── Note prerequisites
   └── Map expected inputs/outputs

3. PREPARE
   ├── Load needed references
   └── Verify script availability

4. EXECUTE
   ├── Follow skill instructions
   ├── Run scripts as needed
   └── Handle errors appropriately

5. VERIFY
   └── Confirm task completion
```

## Troubleshooting

### Skill Not Found
- Verify the skill name is correct
- Check if the skill is installed in a recognized location
- Ensure SKILL.md exists in the skill directory

### Script Execution Fails
- Check script has execute permissions
- Verify required tools are installed
- Review script arguments for errors

### References Not Loading
- Verify reference file exists
- Check file path is correct
- Ensure file is readable

### Instructions Unclear
- Re-read the relevant section
- Check for related references
- Look for examples that clarify usage
