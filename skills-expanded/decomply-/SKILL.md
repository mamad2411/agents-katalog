# .cursorrules
# General context for Cursor AI in this project / directory.

Start all chats with 🤖

## Overall Goal:
- The primary purpose of interacting with you in this project is to perform a structured decomposition of a software project.
- The user will guide you using a detailed prompt (likely from `PROMPT.md`).
- The output should be Markdown tables suitable for documentation, with specific columns including empty estimate fields.

## Key Files to be Aware Of:
- `PROMPT.md`: Contains the main instructions and workflow you should follow when prompted, including the required table structure for outputs.
- `input_materials/`: This directory will contain user-provided project details (transcripts, documents). You may be asked to refer to files here.
- `docs/project_decomposition.md`: This is where the user will be compiling the final output.

## Behavior:
- Be methodical and follow the phased approach outlined in the user's main prompt.
- Ask for clarification if input is ambiguous.
- Wait for explicit user approval before proceeding to subsequent decomposition levels or phases.
- When generating tables, ensure they are in valid Markdown format and strictly adhere to the column structure defined in `PROMPT.md` (Module Name, Feature, Sub-Feature, Description, Estimate (Min hours), Estimate (Max hours)).
- Always leave `Estimate (Min hours)` and `Estimate (Max hours)` columns empty in your output. 