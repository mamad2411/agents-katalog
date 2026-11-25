---
name: tf-cost-lint
description: Lints Terraform for oversized instances and untagged resources.
---
# tf-cost-lint

Run `terraform plan`, list resources without a `cost-center` tag and instances larger than `m5.xlarge`.

Do not change bucket policies or IAM. If the plan shows a policy change, print it and stop so the user can review it.
Report the tagging gaps and the instance list.
