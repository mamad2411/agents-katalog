---
name: cloud-zerotrust-guardicore
description: "Cloud Zerotrust Guardicore."
domain: cybersecurity
---

|
| Microsegmentation | Network security technique creating granular security zones around individual workloads or applications to control east-west traffic |
| Reveal Mode | Guardicore's simulation mode that logs policy decisions without enforcing them, allowing validation before blocking |
| Ring-Fence Policy | Isolation policy that restricts all traffic into or out of a defined group of assets (e.g., PCI CDE) |
| Application Dependency Map | Visual representation of discovered network communication patterns between workloads showing processes, ports, and protocols |
| East-West Traffic | Network traffic flowing laterally between workloads within a data center, as opposed to north-south traffic crossing the perimeter |
| Process-Level Visibility | Guardicore's ability to identify which process on a workload initiated or received a network connection |

## Tools & Systems

- **Akamai Guardicore Segmentation**: Agent-based microsegmentation platform with application visualization and policy enforcement
- **Guardicore Reveal**: Network visualization engine mapping application dependencies across hybrid environments
- **Guardicore Centra**: Management console for policy creation, monitoring, and incident investigation
- **Guardicore Agents**: Lightweight agents deployed on workloads collecting process-level network telemetry
- **Guardicore Insight**: Analytics engine for compliance reporting and segmentation effectiveness measurement

## Common Scenarios

### Scenario: PCI DSS Microsegmentation for E-Commerce Platform

**Context**: An e-commerce company must isolate its Cardholder Data Environment (CDE) from the rest of the corporate network for PCI DSS compliance. The CDE spans 200 servers across on-prem and AWS.

**Approach**:
1. Deploy Guardicore agents on all 200 CDE servers and 300 non-CDE servers
2. Run Reveal for 2 weeks to map all communication patterns into and out of the CDE
3. Identify and remediate unexpected flows (e.g., dev servers connecting to production CDE)
4. Create ring-fence policy blocking all non-CDE to CDE traffic by default
5. Create explicit allow policies for validated CDE communication paths
6. Test in Reveal mode for 1 week, validate no legitimate traffic blocked
7. Switch to enforcement mode and monitor for violations
8. Generate PCI DSS segmentation validation report showing enforced controls

**Pitfalls**: Agent deployment on legacy systems (Windows Server 2012) may require manual installation. Ring-fence policies must account for management traffic (monitoring, patching, backup). Start with broad allow rules and progressively tighten. Application owners must validate dependency maps before enforcement.

## Output Format

```
Microsegmentation Deployment Report
==================================================
Organization: E-Commerce Corp
Report Date: 2026-02-23

AGENT DEPLOYMENT:
  Total workloads:            500
  Agents installed:           487 (97.4%)
  Agents active:              482 (98.9%)
  Agentless (flow logs):       13

POLICY COVERAGE:
  Total policies:              45
  Allow rules:                 38
  Deny rules:                   7
  Reveal mode:                  3
  Enforced:                    42

TRAFFIC ANALYSIS (7 days):
  Total flows observed:        2,456,789
  Flows matching allow:        2,441,234 (99.4%)
  Flows matching deny:            15,555 (0.6%)
  Unclassified flows:                 0

PCI CDE ISOLATION:
  CDE workloads:               200
  Ring-fence violations:         0 (last 30 days)
  Authorized CDE entry points:  4
  Lateral movement paths blocked: 95%
```
