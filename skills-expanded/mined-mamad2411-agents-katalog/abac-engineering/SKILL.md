---
name: abac-engineering
description: Design attribute-based access control. Use when permissions depend
  on context and attributes.
metadata:
  tags: abac, engineering
---

# Attribute-Based Access Control

## Use this skill when
- Permissions on resource/context attributes
- Policy rules (time, location, ownership, risk)
- Combining attributes with roles

## Do not use this skill when
- Simple static permissions (use rbac-engineering)
- No attribute conditions needed

## Instructions
1. Define subject, resource, action, and environment attributes.
2. Write policies as explicit rules with clear evaluation order.
3. Keep policies in a central, decidable mechanism (not scattered ifs).
4. Deny by default; evaluate allow rules, then deny rules.
5. Test policy evaluation with a decision matrix.
6. Nice-to-have: integrate with external PDP (OPA/Cedar) for scale.
7. Log policy decisions for audit.

## Checklist
- Deny-by-default
- Policy decisions are testable
- No conflicting-rule ambiguity

## Output Format
- Attributes | policies | evaluation order | decision matrix

## Common Mistakes
- Business logic embedded as ad-hoc ifs
- Overlapping rules with unclear precedence
- No tests for policy decisions
