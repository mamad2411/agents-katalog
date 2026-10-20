# Sql Query

Executes parameterized SQL queries against PostgreSQL and MySQL databases.

## Instructions

You have access to the Synapse `sql_query` skill located at `skills/sql_query/`.

When the user invokes this command, execute the appropriate handler:

- **TypeScript handler**: `skills/sql_query/index.js` — import and call `handler(params, context)`
- **Python handler**: `skills/sql_query/main.py` — import and call `await handler(params, context)`

### Supported Operations
- `execute`

### Example Invocation
```json
{
  "operation": "execute",
  "db_type": "postgres",
  "query": "SELECT * FROM users"
}
```

### Execution Pattern

1. Parse the user's request to determine the operation and parameters.
2. Load the skill schema from `skills/sql_query/sql_query.skill.json` for parameter validation.
3. Run the handler with the constructed params object.
4. Return the formatted result to the user.

### Dependencies
- TypeScript: check `skills/sql_query/package.json`
- Python: check `skills/sql_query/requirements.txt`
