---
name: terraform-plan-review
description: Review and apply this team's Terraform changes using the saved-plan procedure. Use when preparing, reviewing, or applying Terraform plans for this team's environments.
---

# Terraform plan review

This team reviews the exact saved plan before applying an infrastructure change.

1. Confirm the intended backend, workspace, and environment using the repository's documented procedure.
2. Validate the configuration, then run `terraform plan -out=<plan-file>`.
3. Inspect `terraform show <plan-file>`, highlighting replacements, deletions, and unexpected changes.
4. Obtain the user's explicit approval of that plan before running `terraform apply <plan-file>`.
5. If inputs, configuration, or infrastructure state change, generate a new plan and repeat review.

Verify the apply result and the affected resources using the project's normal checks.
Treat saved plans as sensitive local artifacts; never commit or embed their contents in a skill.
