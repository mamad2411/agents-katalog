<!--
Module 7 Lab — Track B: Cost Anomaly & FinOps
You are writing a FinOps skill for AWS cost anomaly detection.

TRACK COMMITMENT: Stay with Track B through Module 8. Your Module 7
skill will be attached to your Track B profile in Module 8.

STEP 1 of 7: Fill in the YAML frontmatter below.
Each [placeholder] must be replaced with real content.
Quality gate: grep -c '\[' your-skill.md — must return 0 when complete.
-->

---
name: [skill-name-kebab-case]
description: "[One sentence starting with an action verb. Include: what it does, which AWS Cost Explorer metric it targets, when to use it.]"
version: 1.0.0
compatibility: "aws cli v2, HERMES_LAB_MODE=mock|live"
metadata:
  hermes:
    category: "devops"
    tags: [[tag1], [tag2], aws, cost-explorer, [action]]
---

<!-- STEP 2: When to Use — complete Step 1 first.
Reveal: Read LAB.md Step 2 instructions, then add the ## When to Use section here.
Concept: Trigger-based thinking — specific observable cost conditions.
Track B triggers: daily cost spike > X%, EC2 instance type mismatch, unused resources alert.
Env vars for this track: EC2_INSTANCE_ID, AWS_REGION, HERMES_LAB_MODE -->

<!-- STEP 3: Inputs and Prerequisites — complete Step 2 first.
Reveal: Read LAB.md Step 3 instructions, then add ## Inputs and ## Prerequisites sections.
Concept: Skills as functions — explicit inputs.
Track B inputs: AWS_REGION (env var), EC2_INSTANCE_ID (env var), HERMES_LAB_MODE (env var).
Required tools: aws cli v2. -->

<!-- STEP 4: Procedure Phase 1 (Scripts Zone) — complete Step 3 first.
Reveal: Read LAB.md Step 4 instructions, then add ## Procedure / Phase 1.
Concept: Scripts Zone = deterministic CLI commands + expected output.
Track B Phase 1 commands: aws ce get-cost-and-usage, aws ec2 describe-instances -->

<!-- STEP 5: Procedure Phase 2 (Agents Zone) — complete Step 4 first.
Reveal: Read LAB.md Step 5 instructions, then add Phase 2 under ## Procedure.
Concept: Agents Zone = IF/THEN/ELSE decision trees with numeric conditions.
Track B decision: IF daily_cost > baseline * 1.5 THEN ... ELSE IF unused_hours > 72 THEN ... -->

<!-- STEP 6: Escalation Rules and NEVER DO — complete Step 5 first.
Reveal: Read LAB.md Step 6 instructions, then add ## Escalation Rules and ## NEVER DO.
Concept: Safety posture.
Track B never-do: never aws ec2 terminate-instances, never modify Reserved Instances. -->

<!-- STEP 7: Rollback Procedure and Verification — complete Step 6 first.
Reveal: Read LAB.md Step 7 instructions, then add ## Rollback Procedure and ## Verification.
Concept: Reversibility. -->
