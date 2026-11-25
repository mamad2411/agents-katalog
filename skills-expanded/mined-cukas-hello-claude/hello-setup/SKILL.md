# /hello-setup — Register a project

Add a project alias so `/hello` knows where to find it.

## When to use

- When the user says `/hello-setup <name> [path]`
- When `/hello` can't find a project

## How to execute

```bash
bash "$PLUGIN_DIR/scripts/hello-setup.sh" "<name>" "<path>"
```

If path is omitted, it tries `~/GitHub/<name>` automatically.

## Examples

- `/hello-setup kern-lang`
- `/hello-setup landing ~/GitHub/kern-lang-landing`

ARGUMENTS: name [path]
