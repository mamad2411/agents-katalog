# /hello — Talk to another project's Claude

Send a message to a Claude instance in another project and get an immediate response.

## When to use

- When the user says `/hello <project> <message>`
- When Claude needs information from another project

## How to execute

```bash
bash "$PLUGIN_DIR/scripts/hello.sh" "<project>" "<message>"
```

The script will:
1. If a live session exists for that project, send the message to its inbox too
2. Spawn a Claude instance against that project to get an immediate answer

## Examples

- `/hello kern-lang what's the current rule count?`
- `/hello kern-lang-landing update the hero section with the new tagline`
- `/hello compiler did you change the ImportDecl interface?`

ARGUMENTS: project message
