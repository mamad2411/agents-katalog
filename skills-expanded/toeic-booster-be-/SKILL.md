# Instructions

During your interaction with the user, if you find anything reusable in this project (e.g. version of a library, model name), especially about a fix to a mistake you made or a correction you received, you should take note in the `Lessons` section in the `.cursorrules` file so you will not make the same mistake again. 

You should also use `.md` file in the folder `tasks` as a Scratchpad to organize your thoughts. Especially when you receive a new task, you should first create a new `task-name.md` file review the content of the Scratchpad, clear old different task if necessary, explain the task, and plan the steps you need to take to complete the task inside that `task-name.md` file. Note that file name of a task should be clear about the new task you receive from user. The format of task name should be `{task-order}-{task-brief-description}.md`.

Each task file should include the following 5 sections:

1. Task Overview  
A brief summary of the task's purpose and scope.

2. Task Status  
Status can be one of the following: `"Planning"`, `"In Progress"`, or `"Done"`.

Whenever you receive user feedback or there are changes in the **Requirements**, update both the **Status** and the **Scratchpad** accordingly.

- **Planning**:  
  Clarify the requirements and outline the approach for completing the task.

- **In Progress**:  
  Actively working on the task — writing code, making changes, or running commands.

- **Done**:  
  All subtasks have been completed and the task is now awaiting user review or feedback.

3. Requirements  
The detailed specifications or expectations from the user for the task.

4. Scratchpad  
A working area for to-dos, or step-by-step execution plans. You can use todo markers to indicate the progress, e.g.
[X] Task 1
[ ] Task 2

5. Task Lessons  
Insights, mistakes, or best practices learned from completing the task.  
This helps improve performance in future tasks and summarize these lesson into a lesson saved in the `Lessons` section in the `.cursorrules` file

--

When creating a task file, please clarify the requirements with the user to ensure the Scratchpad is comprehensive and meets the user's expectations.

After you've created the task file, please confirm with the user before proceeding.

Also update the progress of the task in the that `task-name.md` file in Scratchpad section when you finish a subtask.
Especially when you finished a milestone, it will help to improve your depth of task accomplishment to use the Scratchpad to reflect and plan.
The goal is to help you maintain a big picture as well as the progress of the task. Always refer to the Scratchpad when you plan the next step.

When you finished a milestone, then pause to request user feedback before proceeding.

When the user asks about a specific task, they may also specify the task order. In that case, you should refer to both the task requirements and the progress that has already been made in the corresponding `.md` file.

After completing a task, you should write a note in the `Lessons` section of the `.cursorrules` file. This helps you avoid repeating the same mistake in the future and supports continuous learning from each task.

Refer to historical tasks for context only. Old and done task files must remain unchanged.

# Lessons

## User Specified Lessons

- You have a python venv in ./venv. Always use (activate) it when doing python development. First, to check whether 'uv' is available, use `which uv`. If that's the case, first activate the venv, and then use `uv pip install` to install packages. Otherwise, fall back to `pip`.
- Due to Cursor's limit, when you use `git` and `gh` and need to submit a multiline commit message, first write the message in a file, and then use `git commit -F <filename>` or similar command to commit. And then remove the file. Include "[Cursor] " in the commit message and PR title.
- No need to inject models through constructor as they rarely change
- No need to create interfaces for repositories and services
- Create form request for request validation.
- Favor creating template files using `php artisan` command lines if feasible.

## Cursor learned

- Always create form requests using Laravel commands for consistency and to follow Laravel standards
- Keep validation rules and messages in form request classes for better organization and reusability
- Use $request->validated() instead of $request->all() for better security
- Don't implement authorize() in form request
- Organize form requests by controller namespace for better code organization
- No need to wrap controller action with try catch because the app already has the global exception handler
- When handling file uploads with Cloudinary, store both the URL and public_id to facilitate updates and deletions
- Use PHP 8.1 enums for fields with a fixed set of possible values