---
name: PR Extension Workflow
description: Analyze pull requests for detection coverage gaps and recommend additional detections, story alignments, and test coverage to extend PRs before merge.
---

# PR Extension Workflow Skill

## Overview

When a PR adds new detections, there are often opportunities to extend coverage before merge — additional sub-techniques, missing analytic story associations, untested scenarios, or related detections that should ship together. This skill provides a systematic workflow for analyzing and extending detection PRs.

## PR Analysis Workflow

### Step 1: Inventory the PR

Examine every detection file in the PR:

- **Detection count:** How many new/modified detections?
- **Techniques covered:** Which MITRE ATT&CK technique IDs?
- **Data sources used:** Which log sources and fields?
- **Story associations:** Which analytic stories are referenced?
- **Severity levels:** Distribution of severity ratings

### Step 2: Identify Coverage Gaps

For each technique in the PR, check:

1. **Sub-technique coverage** — If the PR covers T1059 (Scripting), does it cover the important sub-techniques? (.001 PowerShell, .003 Windows Command Shell, .007 JavaScript)
2. **Tactic coverage** — Does the technique appear under multiple tactics? Are all relevant tactics addressed?
3. **Platform coverage** — If the technique applies to Windows AND Linux, does the PR cover both?
4. **Evasion variants** — Does the detection only catch the obvious case, or does it handle obfuscation/encoding?

### Step 3: Check Story Alignment

For each detection:

1. Is it associated with at least one analytic story?
2. Does a relevant story already exist that this should be added to?
3. Should a new story be created to group this with related detections?

**Finding stories:**

```
search_stories("<threat_name>")
search_stories("<technique_category>")
```

### Step 4: Review Detection Quality

For each detection in the PR:

- [ ] MITRE technique mapping is correct and specific (sub-technique, not just parent)
- [ ] Severity is appropriate (not everything is "high")
- [ ] Description clearly explains what is detected and why it matters
- [ ] Query is optimized for the target SIEM (see **Detection Query Optimizer** skill)
- [ ] Fields used match the expected data model / schema (CIM, ECS, Sigma, or MDE tables)
- [ ] Known false positive guidance is included
- [ ] Kill chain phase / tactic is accurate

### Step 5: Recommend Extensions

Based on the gap analysis, recommend:

1. **Additional detections** — For uncovered sub-techniques or platforms
2. **Story updates** — New or updated analytic stories
3. **Test coverage** — Atomic Red Team tests that should validate the new detections
4. **Related PRs** — Other pending work that should be coordinated

## Extension Recommendation Template

When recommending PR extensions, use this format:

```markdown
## PR Extension Recommendations

### Current Coverage
- Detections: N new, M modified
- Techniques: T1059.001, T1059.003
- Stories: "Windows Command Line Abuse"

### Recommended Additions

#### 1. [Priority: High] Add T1059.007 JavaScript Detection
- **Reason:** PR covers PowerShell and cmd.exe but misses JavaScript/JScript execution
- **Data source:** Sysmon EventCode 1 (process creation)
- **Suggested approach:** Monitor for wscript.exe/cscript.exe with suspicious arguments

#### 2. [Priority: Medium] Create Analytic Story "Script Interpreter Abuse"
- **Reason:** Detections span multiple scripting sub-techniques but no unifying story
- **Suggested detections to include:** All T1059.* from this PR + existing T1059.005

#### 3. [Priority: Low] Add Linux Coverage for T1059.004 (Unix Shell)
- **Reason:** PR is Windows-only but T1059 has Linux sub-techniques
- **Data source:** auditd / syslog process creation
```

## Coverage Gap Identification Queries

Use these to quickly identify what a PR is missing:

```
# Find all sub-techniques under a parent
get_technique("T1059")  → Lists all sub-techniques

# Check existing detection coverage
get_technique_count("T1059.001")  → How many detections exist
get_technique_count("T1059.007")  → Is this sub-technique covered?

# Find similar detections already in the repo
find_similar_detections("JavaScript execution via wscript")

# Check what stories exist for this area
search_stories("command line")
search_stories("scripting")
```

## Common Extension Patterns

| PR Contains | Often Missing | Priority |
|------------|---------------|----------|
| Process creation detections | Parent process context checks | High |
| Single-platform detection | Cross-platform variant | Medium |
| Execution detection | Corresponding persistence detection | High |
| Generic technique detection | Specific sub-technique variants | Medium |
| Detections without story | Story association or new story | Medium |
| High-severity detections | Corresponding hunting queries | Low |
| Signature-based detection | Behavioral/anomaly variant | Medium |

## Integration with CI/CD

If your detection repo has CI/CD validation:

1. Ensure new detections pass schema validation
2. Verify MITRE mappings are valid technique IDs
3. Check that referenced analytic stories / rule groups exist
4. Validate field names match expected data model (CIM for Splunk, ECS for Elastic, MDE tables for Sentinel)
5. Run detection syntax checks per platform:
   - **Splunk:** `contentctl validate`
   - **Sigma:** `sigma check rule.yml` or `sigma convert -t <backend>`
   - **Elastic:** `python -m detection_rules validate-rule`
   - **Sentinel:** KQL syntax validation in Log Analytics

## Tips

- **Don't block PRs for low-priority extensions.** File follow-up issues instead.
- **Group related detections in the same PR** when possible — it's easier to review and test them together.
- **Check the PR author's intent.** If the PR explicitly scopes to one platform, suggesting cross-platform coverage is a "nice to have," not a blocker.
- **Use the coverage tools** to quantify the impact: "This PR takes T1059 coverage from 40% to 75% of sub-techniques."
