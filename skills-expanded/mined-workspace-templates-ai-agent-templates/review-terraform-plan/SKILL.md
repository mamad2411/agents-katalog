---
name: review-terraform-plan
description: Summarizes a terraform plan in plain words and flags destroys, forced replacements and changes that could cause an outage.
disable-model-invocation: true
---

Review a Terraform plan: $ARGUMENTS (path to a saved plan file or plan text; if empty, create one).

1. If no file is given, run `terraform plan -out=review.tfplan -input=false` in the current folder, then `terraform show -json review.tfplan`. Never run `terraform apply` or `destroy`.
2. Count resources by action: create, update in place, destroy, replace.
3. List every destroy and replace first. For each replace, name the attribute marked as forcing replacement. State what the resource holds (data, traffic, state) and whether a lifecycle block such as prevent_destroy exists.
4. Flag risky edits: security group or firewall rules opening 0.0.0.0/0, IAM policies with wildcards, encryption turned off, public access on buckets, changes to databases or DNS, and tag-only noise that hides real changes.
5. Note anything computed as "known after apply" that other resources depend on.

Report: a one-paragraph verdict (safe, needs care, or stop), then the destroy and replace table, then the risky edits with the file and line from the configuration. Ask whether to open the findings as review comments.
