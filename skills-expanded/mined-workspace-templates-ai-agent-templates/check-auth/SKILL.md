---
name: check-auth
description: Walks every route and handler in an area and confirms each one checks who the caller is and what they may do.
disable-model-invocation: true
---

Check authentication and authorization for: $ARGUMENTS (all routes if empty).

1. Find the route table or controllers for that area and list every handler with its method and path.
2. For each, record: how the caller is authenticated (middleware, decorator, guard, session check, none), and what authorization is applied (role check, permission, ownership check, none).
3. For handlers that load a record by id, read the query and confirm it is scoped to the caller or tenant. Flag any lookup that uses only the id from the request.
4. Look at the defaults: does a new route get protection automatically, or must someone remember to add it? Flag public routes that were clearly meant to be private (admin, export, internal, debug).
5. Check that checks happen on the server and not only in the UI, and that failures return 401 or 403 rather than empty data.

Do not edit code. Report a matrix of route, auth, authz, ownership check, and verdict (ok, weak, missing), with the worst gaps first and a one-line fix each. Ask which gaps to patch.
