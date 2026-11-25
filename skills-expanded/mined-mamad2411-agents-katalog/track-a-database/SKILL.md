<!--
Module 7 Lab — Track A: Database Health & Tuning
You are writing a DBA skill for RDS PostgreSQL health investigation.

TRACK COMMITMENT: Stay with Track A through Module 8. Your Module 7
skill will be attached to your Track A profile in Module 8.

STEP 1 of 7: Fill in the YAML frontmatter below.
Each [placeholder] must be replaced with real content.
Quality gate: grep -c '\[' your-skill.md — must return 0 when complete.
-->

---
name: [skill-name-kebab-case]
description: "[One sentence starting with an action verb. Include: what it does, which RDS/PostgreSQL metric it targets, when to use it. Example: 'Investigate RDS slow queries using pg_stat_statements. Use when CloudWatch CPUUtilization alarm fires on RDS instance or application reports query latency > 500ms.']"
version: 1.0.0
compatibility: "aws cli v2, psql 14+, HERMES_LAB_MODE=mock|live"
metadata:
  hermes:
    category: "dba"
    tags: [[tag1], [tag2], rds, postgresql, [action]]
---

<!-- STEP 2: When to Use — complete Step 1 first.
Reveal: Read LAB.md Step 2 instructions, then add the ## When to Use section here.
Concept: Trigger-based thinking — your skill activates on SPECIFIC observable conditions.
Track A triggers: CloudWatch CPUUtilization > threshold, pg_stat_statements slow query alert,
application reporting query latency > Xms.
Env vars for this track: RDS_INSTANCE_ID, DB_HOST, DB_NAME, HERMES_LAB_MODE -->

<!-- STEP 3: Inputs and Prerequisites — complete Step 2 first.
Reveal: Read LAB.md Step 3 instructions, then add ## Inputs and ## Prerequisites sections.
Concept: Skills as functions — explicit inputs make skills reusable, not one-off.
Track A inputs: RDS_INSTANCE_ID (env var), DB_HOST (env var), HERMES_LAB_MODE (env var).
Required tools: aws cli v2, psql 14+. -->

<!-- STEP 4: Procedure Phase 1 (Scripts Zone) — complete Step 3 first.
Reveal: Read LAB.md Step 4 instructions, then add ## Procedure / Phase 1.
Concept: Scripts Zone = deterministic CLI commands + expected output. No reasoning here.
Track A Phase 1 commands: aws rds describe-db-instances, psql -c "SELECT ... FROM pg_stat_statements" -->

<!-- STEP 5: Procedure Phase 2 (Agents Zone) — complete Step 4 first.
Reveal: Read LAB.md Step 5 instructions, then add Phase 2 under ## Procedure.
Concept: Agents Zone = IF/THEN/ELSE decision trees. All conditions must be numeric.
Track A decision: IF mean_time > 1000ms THEN ... ELSE IF calls > 500/hour THEN ... -->

<!-- STEP 6: Escalation Rules and NEVER DO — complete Step 5 first.
Reveal: Read LAB.md Step 6 instructions, then add ## Escalation Rules and ## NEVER DO.
Concept: Safety posture — hard stops prevent catastrophic actions.
Track A never-do: never ALTER TABLE, never DROP, never VACUUM FULL during business hours. -->

<!-- STEP 7: Rollback Procedure and Verification — complete Step 6 first.
Reveal: Read LAB.md Step 7 instructions, then add ## Rollback Procedure and ## Verification.
Concept: Reversibility — every mutation needs an undo path. -->
