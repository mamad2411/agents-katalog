# Linear Module

This directory owns the Linear Issues task provider — an optional `TaskProvider` backed
by Linear's GraphQL API that lets KOTA's builder pull tasks directly from a Linear team.

- Requires `modules.linear.apiKey` (API key or `$ENV_VAR` reference).
- Only activated when `modules.linear.taskProvider.enabled` is `true`.
- Uses Linear's official GraphQL API (`https://api.linear.app/graphql`); no npm dependencies.
- API key is never logged.

## Config

```json
{
  "modules": {
    "linear": {
      "apiKey": "${LINEAR_API_KEY}",
      "taskProvider": {
        "enabled": true,
        "teamKey": "ENG",
        "labelFilter": "kota-task",
        "inProgressState": "In Progress",
        "doneState": "Done"
      }
    }
  }
}
```

## Boundaries

- The module contributes Linear tools plus a task-provider registration when
  enabled. The provider declares read and async mutation capabilities, but not
  bulk maintenance.
- Cache state changes only after Linear acknowledges the mutation. Creation
  resolves configured label names to Linear label ids; unsupported task fields
  fail explicitly.
- Issue state names in config must match exactly the workflow state names in Linear.
