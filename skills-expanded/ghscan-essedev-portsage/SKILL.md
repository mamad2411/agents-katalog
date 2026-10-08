---
name: portsage
description: >
  Manages port allocation across development projects.
  Use it when you need to assign ports to a new project, register services,
  kill stuck processes, or check which ports are in use.
---

# Portsage - Port Allocation Manager

Access to the local port database via the Portsage app, with full parity to
its UI: read state, mutate state, and act on live ports (kill / open).

## Available tools

### Read

- **list_all** - all registered projects with their range, ports, active state,
  and resolved process name + pid for each active port. Always call first.
- **scan_active** - every TCP port currently in LISTEN on the machine
  ({port, process, pid}).
- **list_unmanaged** - active ports >= 3000 not registered to any project and
  not on the system-services blocklist. Use to find zombies.
- **next_range** - peek the next free range without reserving.
- **get_config** - returns {base_port, range_size}.
- **find_project_by_path** - given an absolute path (e.g. a working directory),
  returns the project whose registered path equals it or is an ancestor, or
  null. Useful to scope subsequent calls without asking the user.

### Mutate registry

- **reserve_range(project_name, path?)** - reserves the next free range. Pass
  `path` so future `find_project_by_path` calls resolve correctly.
- **update_project(current_name, new_name?, new_path?)** - renames a project
  and/or changes its path, keeping its range and registered ports. Provide at
  least one of `new_name`/`new_path`; pass an empty `new_path` to clear it.
- **register_port(project_name, service, port)** - adds a port to a project's
  range. Returns the row including its id.
- **remove_port(project_name, service)** - removes a single port.
- **release_project(project_name)** - releases the whole range.
- **set_config(key, value)** - only `base_port` and `range_size` are accepted.

### Prune abandoned projects

- **list_stale(days=90)** - projects whose directory is gone, or untouched for
  that many days. Never includes a project with a port listening right now.
  Read-only: report the list and let the user run `portsage prune --apply`,
  which archives them (range and ports kept, `portsage unarchive` brings them
  back). A missing directory is often a move, so suggest `update_project` with
  the new path before suggesting the prune.

### Undo a deletion

Deleted projects and ports are archived for 30 days, not dropped.

- **list_trash()** - what can still be restored, with the id to restore it by.
- **restore_trash(entry_id)** - puts a project back with its original range
  (so existing .env / compose files keep working) or re-registers a single
  port. Ports taken by another project in the meantime come back as
  `skipped_ports`.

### Act on live ports

- **kill_port(port)** - SIGTERM with 2s grace, then SIGKILL. A port published
  by a Docker container is resolved to that container and stopped with
  `docker stop` instead. Returns {outcome: terminated | killed | not_active |
  permission_denied | docker_stopped | docker_cli_missing | docker_daemon_down
  | docker_no_container | docker_error}.
- **kill_project(project_name)** - kills every active port for a project in
  parallel. Returns a list of {port, outcome}.
- **open_in_browser(port)** - opens http://localhost:<port> in the default
  browser. Returns "ok".

## Recommended workflows

### Assigning ports to a new project
1. Call `list_all` to see the current allocation.
2. Call `reserve_range(name, path)` - always pass `path` if you know it.
3. Call `register_port` for each configured service. Use the assigned
   range's ports in docker-compose.yml and vite.config.

### Identifying and freeing a stuck port
1. Call `scan_active` (or `list_all`) to find the port and its pid/process.
2. If it's registered: `kill_port(port)`. If unregistered: same.
3. The result tells you whether it terminated gracefully, was forcibly
   killed, or was already gone.

### Working from inside a project directory
1. Call `find_project_by_path(pwd)` to resolve the project the user is in.
2. From there: `kill_project`, `release_project`, or `register_port` against
   that project, without asking the user to repeat its name.

## Error handling

Every tool returns `{"error": "..."}` on failure. The two most common cases:
- `"Portsage app is not running. Start it first."` - the Unix socket is
  missing. The user must launch the menubar app.
- `"project 'X' not found"` - the project name does not exist in the registry.
