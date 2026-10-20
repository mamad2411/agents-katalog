<!--
Module 7 Lab — Track C: Kubernetes Health & Self-Healing
You are writing a K8s skill for pod health diagnosis.

TRACK COMMITMENT: Stay with Track C through Module 8. Your Module 7
skill will be attached to your Track C profile in Module 8.

STEP 1 of 7: Fill in the YAML frontmatter below.
Each [placeholder] must be replaced with real content.
Quality gate: grep -c '\[' your-skill.md — must return 0 when complete.
-->

---
name: [skill-name-kebab-case]
description: "[One sentence starting with an action verb. Include: what it does, which Kubernetes resource it targets, when to use it.]"
version: 1.0.0
compatibility: "kubectl 1.28+, KIND v0.31+, HERMES_LAB_MODE=mock|live"
metadata:
  hermes:
    category: "sre"
    tags: [[tag1], [tag2], kubernetes, [resource], [action]]
---

<!-- STEP 2: When to Use — complete Step 1 first.
Reveal: Read LAB.md Step 2 instructions, then add the ## When to Use section here.
Concept: Trigger-based thinking.
Track C triggers: pod CrashLoopBackOff, OOMKilled, node NotReady.
Env vars for this track: KUBECONFIG, NAMESPACE, HERMES_LAB_MODE -->

<!-- STEP 3: Inputs and Prerequisites — complete Step 2 first.
Reveal: Read LAB.md Step 3 instructions, then add ## Inputs and ## Prerequisites sections.
Concept: Skills as functions.
Track C inputs: KUBECONFIG (env var), NAMESPACE (env var, default: default), HERMES_LAB_MODE.
Required tools: kubectl 1.28+, KIND v0.31+. -->

<!-- STEP 4: Procedure Phase 1 (Scripts Zone) — complete Step 3 first.
Reveal: Read LAB.md Step 4 instructions, then add ## Procedure / Phase 1.
Concept: Scripts Zone.
Track C Phase 1 commands: kubectl get pods, kubectl describe pod, kubectl top pods -->

<!-- STEP 5: Procedure Phase 2 (Agents Zone) — complete Step 4 first.
Reveal: Read LAB.md Step 5 instructions, then add Phase 2 under ## Procedure.
Concept: Agents Zone with numeric conditions.
Track C decision: IF restartCount > 5 AND reason == OOMKilled THEN ... -->

<!-- STEP 6: Escalation Rules and NEVER DO — complete Step 5 first.
Reveal: Read LAB.md Step 6 instructions, then add ## Escalation Rules and ## NEVER DO.
Concept: Safety posture.
Track C never-do: never kubectl delete, never kubectl drain, never kubectl cordon. -->

<!-- STEP 7: Rollback Procedure and Verification — complete Step 6 first.
Reveal: Read LAB.md Step 7 instructions, then add ## Rollback Procedure and ## Verification.
Concept: Reversibility. -->
