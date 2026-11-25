---
name: Analytic Story Builder
description: Create grouped detection narratives that tie individual rules into coherent threat stories. Covers Splunk Analytic Stories, Elastic detection rule groups, and Sentinel analytics grouping.
---

# Analytic Story Builder Skill

## Overview

An **analytic story** groups related detections into a narrative around a threat scenario, campaign, or attacker behavior chain. While the "analytic story" concept originated in Splunk's ESCU, the principle — grouping detections by threat context — applies to every SIEM.

| SIEM | Concept | Implementation |
|------|---------|---------------|
| Splunk ESCU | Analytic Story | YAML story file + detection references |
| Elastic Security | Detection rule group / Tag | Tags + rule grouping in Kibana |
| Microsoft Sentinel | Analytics rule template | Grouping via Solution/Content Hub |
| Sigma | Tags / rule collections | `tags` field + directory structure |
| Chronicle SOAR | Playbook grouping | Playbooks referencing detection sets |

## Story Structure (Splunk ESCU Format)

The canonical format. Other SIEMs can adapt this structure to their own grouping mechanism.

```yaml
name: Story Name Here
id: <uuid>
version: 1
date: 'YYYY-MM-DD'
author: Your Name
description: >-
  One to three sentences describing the threat scenario. What is the attacker
  trying to do? Why should a defender care?
narrative: >-
  Three to five sentences providing deeper context. Include references to
  real-world campaigns, common attack chains, and why these detections were
  grouped together. Explain how the detections work together to provide
  coverage across the kill chain.
references:
  - https://attack.mitre.org/techniques/TXXXX/
  - https://relevant-blog-or-advisory.example.com
tags:
  analytic_story: Story Name Here
  category:
    - Malware          # or: Adversary Tactics, Abuse, Cloud Security, etc.
  product:
    - Splunk Enterprise
    - Splunk Cloud
  usecase: Security Monitoring
  mitre_attack:
    - T1059.001
    - T1547.001
```

### Concise Format Guidance

Stories should be **17–19 lines of YAML** (excluding blank lines). Keep it tight:

- `description`: 1–3 sentences. What is the threat?
- `narrative`: 3–5 sentences. Why do these detections belong together?
- `references`: 2–5 links. ATT&CK technique page + source blog/advisory.
- `tags.mitre_attack`: List every technique covered by detections in the story.

**Anti-patterns to avoid:**
- Narratives that just restate the description
- Stories with only 1 detection (group at least 2–3)
- Missing MITRE mappings
- Overly broad stories (e.g., "Windows Attacks") — be specific

## When to Create a Story

Create a new story when:

1. **New threat campaign** — A new adversary campaign warrants grouped coverage (e.g., "STORM-0501 Ransomware")
2. **Technique cluster** — Multiple detections cover related sub-techniques (e.g., "Scheduled Task Abuse" covering T1053.002, T1053.005)
3. **Kill chain segment** — Detections span multiple tactics for a coherent attack path (e.g., "Initial Access via Phishing to Persistence")
4. **Compliance/use case** — A regulatory or operational requirement groups detections (e.g., "PCI DSS Monitoring")

## Story Categories

| Category | Description | Example |
|----------|-------------|---------|
| Malware | Specific malware families | "IcedID", "QakBot Execution Chain" |
| Adversary Tactics | Technique-focused groups | "Windows Persistence Techniques" |
| Abuse | Legitimate tool abuse | "Living Off The Land Binaries" |
| Cloud Security | Cloud-specific threats | "AWS IAM Privilege Escalation" |
| Vulnerability | CVE-specific detection sets | "Log4Shell CVE-2021-44228" |
| Compliance | Regulatory monitoring | "PCI DSS Log Monitoring" |

## Building a Story: Workflow

### Step 1: Identify the Grouping

Start from one of:
- A threat intel report mentioning multiple techniques
- A coverage gap analysis showing related uncovered techniques
- A PR adding multiple related detections

### Step 2: Find Existing Stories

Check if a story already exists that this fits into:

```
search_stories("ransomware")
search_stories("persistence")
```

### Step 3: Draft the Story

Use the YAML format above. Focus on:
- **Clear threat description** — What is the attacker doing?
- **Narrative that connects the dots** — How do these detections work together?
- **Complete MITRE mappings** — Every technique referenced by included detections

### Step 4: Associate Detections

Each detection references its story via tags:

```yaml
# In the detection YAML
tags:
  analytic_story:
    - Story Name Here
```

For non-Splunk SIEMs, use whatever grouping mechanism is available (tags, folders, rule groups).

### Step 5: Validate

- Every detection in the story maps to at least one MITRE technique
- The story's `mitre_attack` list matches the union of all detection technique mappings
- The narrative explains why these detections are grouped (not just "these are all Windows detections")

## Adapting to Other SIEMs

### Elastic Security

Group detections using tags in the rule YAML:

```yaml
tags:
  - "campaign:storm-0501"
  - "story:ransomware-encryption"
```

### Microsoft Sentinel / KQL

Use Sentinel Solutions or Content Hub packages to group related analytics rules. Alternatively, use consistent naming prefixes: `[STORM-0501] - Detection Name`.

### Sigma

Use directory structure and tags:

```
rules/
  windows/
    storm-0501/
      proc_creation_storm0501_initial_access.yml
      proc_creation_storm0501_persistence.yml
```

## Tips

- **Stories evolve.** As new detections are added for a threat, update the story's narrative and technique list.
- **Cross-reference stories.** A detection can belong to multiple stories (e.g., a PowerShell detection might appear in both "Living Off The Land" and "STORM-0501 Ransomware").
- **Use stories for reporting.** Stories make excellent units for executive reporting — "We added coverage for the STORM-0501 campaign (8 new detections across 5 techniques)."
