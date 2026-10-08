---
description: Execute a raw Jira REST API call through the jirac CLI, including GET, POST, PUT, DELETE, and PATCH requests to any Jira REST endpoint
---

Execute raw Jira REST API requests with the `jirac` CLI.

Steps:
1. Check that `jirac` is available by running `jirac --version`. If it is missing, tell the user to install it with `cargo install jira-commands`.
2. Extract from the user's request:
   - HTTP method
   - API path, for example `/rest/api/3/issue/PROJ-123`
   - JSON body when needed
3. Run the matching command:
   - `jirac api get <PATH>`
   - `jirac api post <PATH> --body '<JSON>'`
   - `jirac api put <PATH> --body '<JSON>'`
   - `jirac api delete <PATH>`
   - `jirac api patch <PATH> --body '<JSON>'`
4. Show the response clearly.
5. If the user does not know the endpoint, help map their goal to the correct Jira REST path before running anything.

Examples:
- "get server info" → `jirac api get /rest/api/3/serverInfo`
- "get issue PROJ-123" → `jirac api get /rest/api/3/issue/PROJ-123`
- "get all projects" → `jirac api get /rest/api/3/project`
- "post to /rest/api/3/issue with body {...}" → `jirac api post /rest/api/3/issue --body '{...}'`
