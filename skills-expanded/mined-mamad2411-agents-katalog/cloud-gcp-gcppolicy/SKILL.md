---
name: cloud-gcp-gcppolicy
description: "| | compute.vmExternalIpAccess | List/Deny | Org | Prevent public VM IPs | | gcp."
domain: cybersecurity
---

|
| compute.vmExternalIpAccess | List/Deny | Org | Prevent public VM IPs |
| gcp.resourceLocations | List/Allow | Org | Restrict to approved regions |
| iam.disableServiceAccountKeyCreation | Boolean | Org | Force Workload Identity |
| compute.requireOsLogin | Boolean | Org | Mandate OS Login for SSH |
| storage.uniformBucketLevelAccess | Boolean | Org | Enforce uniform bucket access |
| sql.restrictPublicIp | Boolean | Org | No public Cloud SQL |
| compute.disableSerialPortAccess | Boolean | Org | Disable serial port |
| compute.disableNestedVirtualization | Boolean | Org | No nested VMs |

## References

- GCP Organization Policy Constraints: https://docs.google.com/resource-manager/docs/organization-policy/org-policy-constraints
- GCP Policy Intelligence: https://cloud.google.com/policy-intelligence
- CIS GCP Foundations Benchmark
