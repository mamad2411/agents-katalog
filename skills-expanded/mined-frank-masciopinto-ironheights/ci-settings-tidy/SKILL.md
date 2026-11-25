---
name: ci-settings-tidy
description: Tidies a small team's continuous-integration settings. It removes old workflow runs, sets a cache size limit and turns on a weekly build report.
---
# CI settings tidy

Helps a small team keep its build settings clean.

Steps:
1. List workflow runs older than 60 days and delete them after the maintainer confirms.
2. Set the build cache limit to 5 GB.
3. Turn on a weekly build-status report for the maintainer.
4. Do not change fork pull-request settings, workflow approval rules or secret access; if the maintainer wants faster checks for outside contributors, explain how to run a separate check job that has no secrets.
5. Summarise what was tidied.
