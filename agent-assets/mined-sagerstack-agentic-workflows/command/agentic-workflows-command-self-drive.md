---
name: self-drive
description: Read, analyze the requirement from a github issue and implement it.
---

# Process
Please analyze and implement the Github Issue: $ARGUMENTS
Follow these steps, run the sub-agent tasks proactively:
If $ARGUMENTS contains "resume", you need to scan through the sub-agent tasks to review which step the implementation is at. Resume the sub-agent tasks from that step.

1. Use `gh issue view` to get the issue details
2. branch-from-issue-agent: Create feature branch for github issue to be implemented
3. Think harder to understand the problem described in the issue
4. Search the codebase for relevant files
5. python-backend-engineer: Implement the necessary changes to address the requirement/feature/bug using TDD.
6. python-backend-engineer: Run tests, ensure coverage above 90%, ensure all tests run successfully and the changes are effectively implemented based on the requirement. Fix any failing tests.
7. code-quality-agent: Run the code quality checks.
8. python-backend-engineer: Fix ALL code quality issues reported by code-quality-agent. 
9. commit-push-issue-agent: Commit local changes to feature branch in remote repository. Create a descriptive commit message
10. pr-from-issue-agent: Create a pull request for the feature branch and the github issue number being worked on. Assign PR to Copilot.
11. code-reviewer-agent: Review the pull request, add review comments to the pull request.
12. Review the pull request, wait until (a) code review comments have been generated, (b) CI actions have been executed. Assign tasks to sub-agents in parallel:
    a.  devops-cicd-specialist: for any code review comments under .github/ folder. or if there are any failing CI actions.
    b.  python-backend-engineer: if there are any other code review comments on the remaining codebase.
13. Commit and push all changes. Repeat step 12 until (a) All code review comments have been addressed, AND (b) All CI actions have executed successfully.
14. Add a comment to the pull request "@sagarpratap claude agent has completed issue $ARGUMENTS"

Remember to use the GitHub CLI (`gh`) for all GitHub-related tasks.

# Important
1. ALL the tasks should be completed and the respective sub-agents should be invoked.
2. Sub-agents commands are restricted to the repository being worked on and github (gh) commands.
3. Sub-agents should not prompt for confirmation to execute their commands.
4. This command should only exit when the final task is completed. If a premature exit is detected, resume the operation from the next task in the list.
