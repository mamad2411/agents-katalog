# Sample Prompt:

##### Use the subagent-teams skill to compare two folders in Windows:

Folder A: C:\Projects\TaskAPI\src
Folder B: C:\Projects\TaskAPI\backup

Step 1: Assign one subagent to list all files and subfolders in Folder A.
Step 2: Assign another subagent to list all files and subfolders in Folder B.
Step 3: Have a third subagent compare the two lists and identify:

- Files present in Folder A but missing in Folder B
- Files present in Folder B but missing in Folder A
- Files with the same name but different sizes or timestamps

Step 4: Summarize the differences in a clear report, highlighting mismatches and missing files.

Claude should act as the coordinator, delegating tasks to subagents and merging their outputs into a final comparison summary.
