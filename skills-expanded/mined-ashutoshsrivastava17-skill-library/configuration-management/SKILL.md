---
name: configuration-management
description: >
  Manage configuration items — CMDB design, CI relationships, discovery
  automation, change impact analysis, and data quality assurance.
  TRIGGER when: user says /configuration-management, needs CMDB guidance,
  or asks about configuration item management.
argument-hint: "[IT environment or CMDB scope]"
user-invocable: true
---

# Configuration Management

## Process
### Step 1: Define CMDB Scope
| CI Type | Examples | Priority |
|---------|---------|----------|
| Infrastructure | Servers, VMs, containers, network devices | High |
| Applications | Services, databases, middleware | High |
| Endpoints | Laptops, mobile devices | Medium |
| Cloud resources | Instances, storage, networking | High |
| Licenses | Software licenses, SaaS subscriptions | Medium |

### Step 2: Design CI Schema
| Attribute | Required For |
|-----------|-------------|
| CI ID | All (unique identifier) |
| Name | All |
| Type/Class | All |
| Owner | All |
| Environment | Servers, Applications |
| Dependencies | Applications, Services |
| SLA tier | Services |
| Cost center | All |

### Step 3: Map Relationships
| Relationship | From → To | Purpose |
|-------------|----------|---------|
| Runs on | Application → Server | Impact analysis |
| Depends on | Service → Service | Dependency chain |
| Managed by | CI → Team | Ownership |
| Licensed by | Application → License | Compliance |

### Step 4: Automate Discovery
| Method | What It Finds |
|--------|-------------|
| Agent-based | Installed software, hardware config |
| Network scan | Connected devices, open ports |
| Cloud API | Cloud resources, tags, relationships |
| Service mesh | Service dependencies, traffic patterns |

### Step 5: Enable Impact Analysis
When a change is proposed:
1. Identify affected CI
2. Traverse dependency graph
3. List all downstream services/users impacted
4. Calculate risk score based on CI criticality

### Step 6: Maintain Data Quality
| Check | Frequency | Target |
|-------|-----------|--------|
| Completeness | Monthly | > 95% required fields populated |
| Accuracy | Quarterly | > 90% match reality (spot check) |
| Freshness | Monthly | > 90% updated within 30 days |
| Orphan CIs | Monthly | < 5% CIs with no relationships |

## Output Format
```markdown
## CMDB Design: [Scope]
### CI Types: [table with schema]
### Relationships: [dependency model]
### Discovery: [automation approach]
### Quality: [metrics and targets]
```

## Quality Checklist
- [ ] CI types cover critical infrastructure and applications
- [ ] Relationships enable impact analysis
- [ ] Discovery automation reduces manual maintenance
- [ ] Data quality metrics are tracked
- [ ] Change management integrates with CMDB

## Edge Cases
- For cloud-native environments, treat infrastructure as ephemeral
- If starting from scratch, focus on critical services first
- For hybrid environments, ensure cross-platform visibility
