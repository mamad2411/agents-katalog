---
name: custom
description: Execute custom command definitions stored outside .claude folder with parameter pass-through
---

# Process

Execute custom command: $ARGUMENTS

Follow these steps:

1. **Parse Arguments**: Extract the first parameter as `custom-command` (path to custom command definition file) and remaining parameters as arguments to pass through

2. **Validate Custom Command**: Ensure the custom-command file exists and is accessible

3. **Read Instructions**: ALWAYS thoroughly read the custom instructions provided in the custom-command file before executing

4. **Execute Command**: Execute the instructions in the custom-command together with the remaining input parameters, following these compliance rules:
   - Execute instructions step by step and respect conditional flow
   - Pass all remaining parameters after custom-command to the command as its arguments
   - Follow any control gates or blocking conditions specified in the custom command
   - Use TodoWrite to track progress if the custom command involves multiple steps

5. **Error Handling**: If the custom-command file is not found or inaccessible, display error message and available custom commands

# Usage Examples

```bash
/custom context/product/commands/research.md --pob="docs/globaldex/discovery/pob-globaldex.md"
/custom workflows/deploy.md --env="staging" --branch="feature/auth"
/custom context/product/commands/ideate.md --problem="cross-chain complexity"
```

# Important Notes

- The custom-command parameter is required and must be the first argument
- All parameters after the custom-command are passed through to the custom command
- Custom commands must be readable files containing step-by-step instructions
- This command enforces strict compliance with custom command specifications