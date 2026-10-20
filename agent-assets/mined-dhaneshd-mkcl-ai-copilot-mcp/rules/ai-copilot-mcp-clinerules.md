## CRITICAL: LOOP PREVENTION & INTERACTIVE UPDATES
1.  **5-Turn Checkpoint**: If you are in a research or discovery phase, you MUST pause and provide a summary to the user at least every **5 turns** (using `notify_user` or chat). Never exceed 10 turns without an interactive update.
2.  **Explicit Path Reporting**: When you start a research path (e.g., "I will now look at the API layer"), tell the user your plan *before* executing 5+ tool calls.
3.  **Discovery Loop Block**: If you find yourself repeatedly calling `list_files` (or `list_dir`) on nested folders, PAUSE. Use `get_repo_map` or `scan_directory` instead. Do not "dig" more than 2 levels deep using single-folder listing.
4.  **Finding Validation**: After `record_finding`, immediately summarize the major discovery to the user and ask for confirmation/next steps.

## Tool Naming & Usage
Standardize your tool selection to reduce reasoning overhead:
- **Search**: Prioritize `search_repository` (Grep) or `semantic_search` (Vector) over manual file reading.
- **Mapping**: Use `get_repo_map` (max_depth=3) at the start of any new project analysis.
- **Recursive**: Use `scan_directory` for full tree views.

### Aliases Reference:
- `search_web` -> `web_search_smart`
- `list_dir` -> `list_files`
- `run_command` -> `run_shell_command`
- `grep_search` -> `search_repository`
- `list_dir_recursive` -> `scan_directory`


