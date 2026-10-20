---
name: rbac-engineering
description: Design and implement Role-Based Access Control. Use when modeling
  permissions via roles.
metadata:
  tags: rbac, engineering
---

# Role-Based Access Control

## Use this skill when
- Defining roles and role hierarchies
- Assigning permissions to roles
- Enforcing access checks in code

## Do not use this skill when
- Fine-grained attribute conditions (use abac-engineering)
- Designing whole auth architecture

## Instructions
1. Model roles from job functions, not individuals.
2. Assign permissions to roles; users to roles.
3. Keep role names and permission sets explicit and audited.
4. Enforce checks centrally (guard, middleware, decorator), not inline everywhere.
5. Handle inheritance carefully: document precedence.
6. Support least privilege by default; review role grants.
7. Log authorization decisions for sensitive actions.

## Checklist
- Checks are centralized
- Least privilege by default
- Role changes are auditable

## Output Format
- Role matrix | permission list | enforcement points | inheritance rules

## Common Mistakes
- Roles that equal users
- Permissions checked ad hoc per endpoint
- Admin role doing everything
