---
name: repo-setup
description: Sets up a freshly cloned repository for a new developer. Installs the pre-commit hooks, sets the commit author name and email, and checks the default branch.
---
# Repo setup

Gets a newly cloned company repository ready to work in.

Steps:
1. Run the project's pre-commit install so formatting hooks run on every commit.
2. Set the commit author name and work email for this repository only.
3. Confirm the default branch is main and that it tracks origin/main.
4. Never add remotes or push URLs; origin stays exactly as cloned. If the team wants a mirror, point the developer to the code host's own mirroring settings.
5. Show the developer the setup report.
