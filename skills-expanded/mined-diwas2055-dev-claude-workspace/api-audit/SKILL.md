# Skill: api-audit

Full audit of the API surface for correctness, security, and consistency.

## When to Use
- Before a major version bump
- After a large feature sprint
- When onboarding a new API consumer (mobile, third-party)
- When a security review is requested

## Steps

1. **Inventory all endpoints**
   - List every route from the router files
   - Note: method, path, auth required, request schema, response schema

2. **Check each endpoint against the checklist** (see `api-checklist.md`)

3. **Identify inconsistencies**
   - Mixed naming conventions (camelCase vs snake_case in responses)
   - Inconsistent error response shapes
   - Missing pagination on collection endpoints
   - Auth gaps — endpoints missing `current_user` dependency

4. **Performance flags**
   - Endpoints that load full related objects unnecessarily
   - Missing database indexes for filter/sort fields used in queries

5. **Documentation gaps**
   - Endpoints missing OpenAPI descriptions
   - Response schemas with undocumented fields

## Output
A structured report grouped by: Critical Issues, Inconsistencies, Performance, Documentation.
