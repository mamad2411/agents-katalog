# /scope — Set what this session is working on

Update the session's scope description so other sessions know what you're doing.

## When to use

- When the user says `/scope "description"`
- When Claude starts a major task and should announce it to other sessions

## How to execute

```bash
bash "$PLUGIN_DIR/scripts/set-scope.sh" "<description>"
```

## Examples

- `/scope "refactoring the AST rule engine"`
- `/scope "updating landing page docs"`
