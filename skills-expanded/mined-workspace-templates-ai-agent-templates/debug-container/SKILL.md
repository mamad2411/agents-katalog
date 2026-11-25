---
name: debug-container
description: Finds why a Docker container exits, restarts or misbehaves by reading its logs, exit code, config and Dockerfile together.
disable-model-invocation: true
---

Debug this container: $ARGUMENTS (container name or id, or a compose service; if empty, check the most recently exited one).

1. Inspect state with read-only commands: `docker ps -a --filter "name=..."`, `docker inspect --format '{{.State.ExitCode}} {{.State.OOMKilled}} {{.State.Error}}' <c>`, and `docker logs --tail 100 <c>`.
2. Read the exit code: 0 means the main process finished, 1 an app error, 125 to 127 a bad command or missing binary, 137 killed (memory limit or manual stop), 139 a crash, 143 stopped by SIGTERM.
3. Compare the entrypoint and CMD from `docker inspect` with the Dockerfile. Look for shell versus exec form, missing executable bits, wrong WORKDIR, a process that daemonizes and exits, and files removed by .dockerignore.
4. Check configuration: environment variables, mounted volumes, network and published ports, healthcheck result, and depends_on ordering in the compose file.
5. If the container is running, you may use `docker exec <c> ls` or `env` to look inside. Do not change anything.

Report the most likely cause first, the evidence from each step, and the exact fix (a Dockerfile or compose edit). Ask before editing files, restarting, or running `docker rm`.
