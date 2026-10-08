---
name: update-spatie-docs
description: "Update Spatie package documentation by importing docs for a given repo. Use when the user says 'update docs for [package]', 'import docs for [repo]', or invokes /update-spatie-docs [repo-name]. Takes a repo name argument (e.g., 'backup', 'laravel-medialibrary')."
---

# Update Spatie Docs

Run the docs import command for the given repo name.

The repo name is passed as the skill argument (e.g., `/update-spatie-docs backup`).

```bash
cd /Users/freek/dev/code/spatie.be && php artisan docs:import --repo=spatie/{repo_name}
```

If no repo name argument is provided, ask the user for one.
