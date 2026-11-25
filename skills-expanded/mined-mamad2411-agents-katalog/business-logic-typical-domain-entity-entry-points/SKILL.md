---
name: business-logic-typical-domain-entity-entry-points
description: Promote a standard set of business-logic entry points around a domain-entity type when an agent must decide which entry points to implement. Use when designing, creating, modifying, reviewing, or completing business-logic entry points for a specific domain entity. Prefer basic entity entry points such as create, update, find by id, search, and delete by id; use explicit mark-as entry points for finite-state changes such as enum or boolean status transitions; use explicit assign or add entry points for one-to-many or many-to-many associations between domain entities; and use explicit check-whether-can-be entry points when the business operation needs a boolean answer about whether an action is currently allowed.
---

# Typical Domain-Entity Entry Points for Business Logic

## Goal

When deciding which business-logic entry points to implement around a domain-entity type, prefer a standard set of entry points instead of inventing ad hoc operations.

Treat the domain entity as the organizing center. Start from the entity type, then choose the entry point kind that matches the business operation:

- create
- update
- find by id
- search
- delete by id
- explicit mark-as operations for finite-state changes
- explicit assign or add operations for entity associations
- explicit check-whether-can-be operations for boolean feasibility checks

## Basic Entry Points

Given a domain-entity type, prefer these basic entry points:

1. `create`
   - Creates a new domain entity.

2. `update`
   - Updates only fields whose value space is effectively infinite or quasi-infinite.
   - Typical examples: `string`, `int`, `decimal`, `url`, `date`, `datetime`, text fields, free-form names, descriptions, notes, counters, limits, and similar values.

3. `find by id`
   - Returns exactly one entity by its identity or fails when it does not exist.

4. `search`
   - Returns a collection of entities or results.
   - Supports filtering by any field or combination of fields.
   - Supports pagination and sorting.

5. `delete by id`
   - Deletes the entity identified by its id.

6. `check whether ... can be ...`
   - Returns a boolean indicating whether a business operation is currently allowed.

## Choose the Entry Point by Operation Kind

### Use `update` only for quasi-unbounded fields

Use `update` when the operation changes fields whose possible values are open-ended or effectively unbounded.

Examples:

- `updateUser`
- `updateCourse`
- `updateRole`

Typical fields for `update`:

- name
- description
- email
- phone
- url
- amount
- date
- datetime
- numeric limits or thresholds

Do not use `update` for finite-state or relationship-changing operations when a more explicit entry point is appropriate.

### Use `find by id` for one-or-fail retrieval

Use a dedicated `find by id` entry point when the caller needs one specific entity by identity.

Examples:

- `findUserById`
- `findCourseById`
- `findRoleById`
- `findPermissionById`

The operation should either return the requested entity or fail according to the project's error convention.

### Use `search` for filtering, sorting, and pagination

Use `search` when callers need to retrieve entities by arbitrary criteria, combinations of criteria, sorting, or pagination.

Examples:

- `searchUsers`
- `searchCourses`
- `searchRoles`
- `searchPermissions`

Search should be the flexible query entry point:

- filter by one field
- filter by multiple fields
- sort
- paginate

## Finite-State Changes Need Explicit Mark-As Entry Points

When the business operation changes a field with only a small set of possible values, do not hide that transition inside `update`.

Use an explicit entry point that names the new business state.

Typical finite-state fields:

- enum-based status fields
- boolean fields that represent status
- lifecycle flags whose values carry business meaning

Examples:

- `markUserAsEnabled`
- `markRoleAsDisabled`
- `markCourseAsCancelled`
- `markUserAsDisabled`

Use this pattern when the change is really a business state transition, not just a free-form field edit.

## Relationship Changes Need Explicit Assign or Add Entry Points

When the business operation associates one domain entity with another in a one-to-many or many-to-many relationship, do not hide that change inside `update`.

Use an explicit relationship entry point that names the association operation.

Examples:

- `assignPermissionToRole`
- `addUserToCourse`
- `removeUserFromCourse`
- `unassignPermissionFromRole`

Choose the verb that matches the business meaning of the association:

- `assign`
- `add`
- `remove`
- `unassign`

Prefer the most specific business verb that fits the relationship.

## Feasibility Checks Need Explicit Check-Whether Entry Points

When the business operation is to ask whether something can be done right now, use an explicit check-whether entry point that returns a boolean.

Use this pattern when the caller needs a yes-or-no answer about whether an action is currently allowed before attempting it.

Examples:

- `checkWhetherPostCanBePublished`
- `checkWhetherUserCanBeDisabled`
- `checkWhetherCourseCanBeCancelled`
- `checkWhetherRoleCanBeDeleted`
- `checkWhetherPermissionCanBeAssignedToRole`

Use this kind of entry point for business permission or feasibility checks, not for performing the action itself.

## CQS Alignment

When the project is following Command-Query Separation:

- `create`, `update`, `delete by id`, `mark as ...`, `assign ...`, and `add ...` are commands
- `find by id`, `search`, and `check whether ... can be ...` are queries

Keep this skill focused on choosing the right entry point kind. If other skills already govern CQS return shapes, signatures, or payload typing, keep those rules too.

## Detection Workflow

1. Start from the domain entity.
   - Identify the primary entity type the requested operation acts on.

2. Identify the real business operation.
   - Is the caller creating, editing open-ended fields, retrieving by id, searching, deleting, changing a finite state, associating entities, or checking whether an action is allowed?

3. Choose the standard entry point kind first.
   - Prefer the standard entry point kind before inventing a custom one.

4. Reject overloaded `update` operations when the meaning is more specific.
   - If the change is a finite-state transition, use `mark as ...`.
   - If the change is an association, use `assign ...` or `add ...`.
   - If the operation is a yes-or-no feasibility check, use `check whether ... can be ...`.

## Writing or Changing Entry Points

1. Begin with the standard set.
   - Check whether the requested behavior is simply `create`, `update`, `find by id`, `search`, `delete by id`, or `check whether ... can be ...`.

2. Use `update` narrowly.
   - Restrict `update` to quasi-unbounded fields.
   - Do not let `update` absorb business state transitions or association operations.

3. Name state transitions explicitly.
   - Prefer `mark as ...` naming when the operation changes a finite-state field.
   - Make the resulting business state obvious in the entry point name.

4. Name associations explicitly.
   - Prefer verbs like `assign` or `add` when the operation connects one entity to another.
   - Make both sides of the relationship obvious in the entry point name.

5. Keep `search` broad and structured.
   - Let `search` handle combinations of filters, ordering, and pagination instead of creating many narrow list-style entry points by default.

6. Use explicit check-whether entry points for boolean business decisions.
   - Prefer `check whether ... can be ...` naming when the caller needs to know whether an action is allowed.
   - Return a boolean instead of overloading a command or search operation for that purpose.

## Examples

Prefer this set for a `User` entity:

- `createUser`
- `updateUser`
- `findUserById`
- `searchUsers`
- `deleteUserById`
- `markUserAsEnabled`
- `markUserAsDisabled`
- `addUserToCourse`
- `checkWhetherUserCanBeDisabled`

Prefer this set for a `Role` entity:

- `createRole`
- `updateRole`
- `findRoleById`
- `searchRoles`
- `deleteRoleById`
- `assignPermissionToRole`
- `unassignPermissionFromRole`
- `checkWhetherRoleCanBeDeleted`

Prefer this set for a `Course` entity:

- `createCourse`
- `updateCourse`
- `findCourseById`
- `searchCourses`
- `deleteCourseById`
- `markCourseAsCancelled`
- `addUserToCourse`
- `checkWhetherCourseCanBeCancelled`

Prefer this set for a `Permission` entity:

- `createPermission`
- `updatePermission`
- `findPermissionById`
- `searchPermissions`
- `deletePermissionById`
- `assignPermissionToRole`
- `checkWhetherPermissionCanBeAssignedToRole`

Prefer this set for a `Post` entity:

- `createPost`
- `updatePost`
- `findPostById`
- `searchPosts`
- `deletePostById`
- `markPostAsCancelled`
- `checkWhetherPostCanBePublished`

Avoid these overloaded choices when a more specific entry point exists:

- `updateUserStatus`
- `updateRolePermissions`
- `updateTeamMembers`

Prefer instead:

- `markUserAsEnabled`
- `assignPermissionToRole`
- `addUserToCourse`
- `checkWhetherPostCanBePublished`

## Review Questions

When reading or reviewing code, ask:

- Which domain entity is this entry point organized around?
- Is this operation really create, update, find by id, search, delete by id, or check whether something can be done?
- If not, is it actually a finite-state transition that should be `mark as ...`?
- If not, is it actually an association that should be `assign ...` or `add ...`?
- If not, is it actually a feasibility check that should be `check whether ... can be ...`?
- Is `update` being overloaded with responsibilities better expressed as explicit business operations?

If the answer is yes, apply this skill.

## Report the Outcome

When finishing the task:

- state which domain-entity entry points were identified or changed
- state which standard entry point kinds were used
- state where `update` was replaced by explicit `mark as ...`, `assign ...`, `add ...`, or `check whether ... can be ...` operations
- state how the final entry points align with the entity's business operations
