---
name: openproject
description: Manage projects, work packages, attachments, relations, boards, users, watchers, and notifications in a connected OpenProject instance. Use for OpenProject discovery, task workflows, project administration, file handling, dependency management, and notification triage.
---

# OpenProject

Use the `openproject` MCP tools for OpenProject work.

## Safety

- Treat project and work-package creation, updates, assignments, relations,
  watchers, comments, uploads, and notification changes as external writes.
- Perform a write only when the user explicitly requests it and the target project or work package is unambiguous.
- Treat project, work-package, relation, attachment, and watcher deletion as
  destructive. Confirm an ambiguous deletion target before calling the tool.
- Before a write, resolve project, type, status, priority, and assignee IDs with read tools when needed.
- Read only a local attachment path explicitly supplied or clearly identified
  by the user. Respect size limits and never scan credential directories.
- Never expose API tokens or environment-file contents.
- After a write, report the affected resource ID and returned OpenProject URL
  when available.

## Workflow

1. Use `list_projects` to resolve a project name or identifier.
2. Use `search_work_packages` or `get_work_package` to inspect existing work.
   Search can be narrowed by project, assignee, exact due date, and either an
   exact status or the open/closed status category. Use `assignedToMe` for the
   authenticated user's work packages.
3. Prefer `count_projects` or `count_work_packages` when only a total is
   needed. Follow `hasMore` pagination metadata instead of silently assuming a
   list is complete.
4. Resolve write inputs with `list_work_package_types`,
   `list_work_package_statuses`, `list_work_package_priorities`,
   `list_project_versions`, and `list_available_assignees`.
5. Use `list_work_package_attachments` and then
   `get_work_package_attachment` when the task includes attached files. Raise
   `maxBytes` only when the listed file size requires it.
6. Use `list_work_package_activities` for comment and change history,
   relation tools for dependencies, and watcher tools for subscriptions.
7. Use `create_work_package` for new tasks. Omit `typeId` to select the
   project's `Task` type automatically.
8. Use `update_work_package` for field changes and
   `add_work_package_comment` for progress notes and follow-ups.
9. Use notification tools for the authenticated user's inbox and board tools
   for read-only Kanban inspection.
10. Use `get_openproject_api` only when no typed read tool covers the needed
    API v3 resource. It is a GET-only escape hatch, not a substitute for the
    focused tools.
