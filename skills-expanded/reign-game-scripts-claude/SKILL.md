# Scripts — Dev-Stack Lifecycle

The dev/e2e stacks run via `Taskfile.yml` tasks backed by `scripts/dev/lib.sh`. Operational commands
(what to run) live in `/CLAUDE.md` → Commands. This file covers how the lifecycle works. The shell
pitfalls to know before editing the lifecycle tasks are in a comment block at the head of `Taskfile.yml`.

## How the dev stack works

Services run detached via `nohup ... &`, with stdout+stderr redirected to `./logs/*.log` (gitignored).
`task dev:up` polls each service until healthy before returning:

- **Backend** — hits `/api/health`.
- **Frontend** — waits for port `:5180` to listen.
- **Generator** — waits for its "starting local SQS poller" log line.

Backend and frontend identity is tracked by port (`lsof -ti:PORT`). The generator has no port, so its
PID is persisted to `./logs/generator.pid`; a stale PID is detected and cleaned up. LocalStack
readiness waits for both `/_localstack/health` and the `.localstack/init-aws.sh` script (queue exists +
table ACTIVE). LocalStack runs in Docker via `docker-compose.yml`; `init-aws.sh` creates the DynamoDB
table, SQS queues, and seed CONFIG items.

## Taskfile shell pitfalls (read before editing Taskfile.yml)

Task runs `cmds:` in its built-in interpreter (`mvdan.cc/sh`), not bash. It mostly matches POSIX but
diverges where it bites process-lifecycle code:

- `$!` after a background job returns a goroutine handle, not an OS PID — capturing it stores garbage.
- `kill -0` against external OS PIDs is unreliable.
- `disown` is unimplemented.
- `set -e` around command substitution differs from bash.

When a task tracks a backgrounded process by PID (anything without a port), wrap the block in a bash
heredoc:

```yaml
cmds:
  - |
    bash <<'BASH'
    set -e
    nohup long-running-cmd > log 2>&1 </dev/null &
    echo $! > pid
    BASH
```

Port-based lifecycle (`lsof -ti:PORT`) works fine in Task's shell and is preferred whenever a port
exists.

## Lessons

- **Lockstep config: capture every consumer.** When two services share an identifier (queue URL, table
  name, env var), every site must agree. Define shared constants once in `Taskfile.yml::vars:` and
  reference them from each env block — single source of truth.
