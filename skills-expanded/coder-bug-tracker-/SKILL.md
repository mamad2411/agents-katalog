# Cursor Rules for No-Code Edition Project

## context_initialization
Always review `.notes/project_overview.md` and `.notes/task_list.md` before generating suggestions.

## operational_protocol
1. Break work into individual tasks (see § 3.2).  
2. You have online access to review related documentation and APIs.  
3. **Avoid modifying working code** unless:
   - A dependency requires it  
   - The user explicitly asks for a change  
   Otherwise, prefer additive changes.

## safety_requirements
- Maintain type safety and error handling  
- Document all new code  
- When generating solutions, Never break existing functionality unless user want to make change 
- Only use one localhost activate the project, if have sample testing or new features, let users know which local host for what features.

## priorities
Prioritize `notes/` folder content as the highest context source when reasoning or answering questions.

## status_labels
| Emoji | Status |
|-------|--------|
| 🗂️ | **backlog** — Not started |
| 🚧 | **in-progress** — Actively being built |
| ✅ | **completed** — Done & verified |
| ❌ | **dropped** — No longer pursued |
| 🔜 | **future-step** — Scheduled for later |
| 📦 | **archived** — Historical reference |

## task_evaluation
Each task must include:
- **Priority**: High / Medium / Low  
- **Relevance_to_MVP**: Yes / Maybe / No

## problem_solving_protocol
When you encounter a blocker or technical issue:
1. Attempt the **best available solution** based on current context.  
2. If it fails or is uncertain, **explore at least one more viable alternative**.  
3. Do **not** rely on the user for technical suggestions.  
4. Log all solution attempts and the final key decision in `meeting_notes.md` if user prompt you.
5. Use the `mcp.json` file with the **MCP date_time tool** to fetch the current timestamp.

## tool-access
Use MCP date_time tool for accurate timestamps in documentation and logs. 