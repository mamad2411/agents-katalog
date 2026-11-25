---
name: uniac
description: "Build, run and operate web apps, websites, agents, databases and background workers on Uniac, the cloud platform for AI agents. Use when asked to deploy, host or run an application, an API or an agent in the cloud, and for any task involving uniac.yaml, the uniac CLI or a project on uniac.ai — describing an application, deploying it, debugging a deployment, or reading a project's state."
---

# Uniac

Build and run web apps, websites, agents, databases and background workers
on Uniac, the cloud platform for AI agents. This skill is an expert's
working knowledge of it, compressed for an agent building on it.
Every contract has one authoritative page at https://docs.uniac.ai; this file
and its references summarize them and name the page for each detail. When an
exact field, limit or behavior matters, read the page's Markdown:
`curl -sL https://docs.uniac.ai/<page>.md`.
`https://docs.uniac.ai/llms-full.txt` holds every page in one file; the page
Markdown is the current text.

## The model

- An **account** owns **projects**. A project is a deployment destination with
  its own services, volumes and private network; its name is unique within
  the account and it also has an assigned slug.
- A **service definition** (`type: service` for stateless execution,
  `type: singleton`) holds an image or Dockerfile build, `env`,
  `start_command`, a size and `volumes`. A definition runs once a deployment
  declaration instantiates it.
- A **deployment declaration** (`type: deployment`) instantiates one
  definition as a **service**, and the declaration's name is the service's
  name: its identity in the project and its private hostname. Several
  declarations can reuse one definition.
- **Replicas** are the containers behind that identity. A stateless service
  runs up to four interchangeable ones; a singleton runs at most one, and a
  replacement stops the old replica before the new one starts.
- A **volume** is durable storage with a project-scoped identity
  (`<service>.<name>`), bound to one singleton service at a time. Its data
  outlives replicas, unbinding and service deletion; deleting the volume or
  the project destroys it.
- **Public endpoints** (`public_ports` on the declaration) expose the
  application's listen port: `http` becomes an `https://` address on the
  shared edge, `tcp` a public host with an allocated port. Services reach one
  another privately inside the project.

Platform behavior: [platform.md](references/platform.md).

## The workflow

1. **Describe** the application in `uniac.yaml` at its root
   ([composition.md](references/composition.md)). `uniac init` writes a
   starter for one prebuilt image.
2. **Validate** with `uniac plan`: schema, references and build paths, checked
   locally and offline; `--json` prints the generated description.
3. **Sign in once** with `uniac auth login` (browser). In CI, set
   `UNIAC_ACCESS_TOKEN`.
4. **Choose the destination**: `uniac project create <name>`, then
   `uniac link <name-or-slug>`, which writes `.uniac/deploy.json`. Without a
   binding, `deploy` opens a picker and saves the choice.
5. **Deploy** with `uniac deploy`: every image is built or pulled by the local
   Docker daemon for `linux/amd64`, pushed, and every deployment declaration
   submitted as a new version of its service, which replaces the service's
   replicas; each service is then polled for up to five minutes.
6. **Read state** with `uniac status` (whole project, volumes included) or
   `uniac status <service>`, what the application writes with
   `uniac logs <service>` (`-f` to follow), and what an instance holds with
   `uniac exec <service> -- <command>`, or interactively with
   `uniac exec -it <service> -- sh`.

Commands, destination selection, output and exit codes:
[operations.md](references/operations.md).

## Decisions

| Question | Answer |
|---|---|
| `service` or `singleton`? | `service` for anything that can run as interchangeable copies: APIs, workers, front ends. `singleton` for anything that must be alone or needs a volume: databases, persistent caches, schedulers. |
| Where does state live? | On a singleton's volume, or in an external store. A replica's memory and container files last as long as the replica. |
| How much CPU and memory? | `vcpu` (1–2) and `memory_mib` (512–4096) on the definition. Leave them out to keep the service's current size; a new service gets 1 vCPU and 512 MiB. Size memory for the peak: past it, a process is OOM-killed. |
| How many replicas? | `replicas` on the deployment declaration: 0–4 for a `service`, 0 or 1 for a `singleton`. Leave it out to keep the service's current count, such as one set in the dashboard. |
| Which port? | The application's own listen port, named in `public_ports`. An application that reads `PORT` gets it from a declared `env` value. |
| `http` or `tcp`? | `http` for anything browsers or HTTPS clients call; TLS ends at the edge, and a request has 60 seconds. `tcp` for raw protocols such as databases; Uniac allocates the public port. |
| How do services find each other? | By name: the service `db` is `db` inside its project, on any port the application listens on. `${{db.host}}` inside an `env` value gives that name. |
| How does one service learn another's configuration? | `${{other.VAR}}` reads a variable the other service declares in the same package. |
| `build` or `image`? | `build: <dir>` when the Dockerfile lives in the repository; `image: <ref>` for a published image. Exactly one of the two. |
| One file or a workspace? | One `uniac.yaml` for one application. A `workspace` with `includes` when packages in subdirectories each own a `uniac.yaml`; they deploy to one project, and each package's references stay within it. |

## Behaviors to plan for

- **Deploys use the local Docker daemon.** `uniac deploy` builds or pulls
  every image locally, `image:` sources included, for `linux/amd64`, and
  pushes it; base images need an amd64 variant. `.dockerignore` shapes the
  build context.
- **A declared `replicas` applies on every deploy.** Without it, a service's
  new version keeps the count the service has, set in the dashboard or by an
  earlier deploy, including zero for a paused service; a new service starts
  with one replica.
- **A singleton's replacement stops the old replica first.** Each deploy of a
  singleton has a gap, and a successor that fails to start leaves the service
  stopped until a working deploy.
- **A deploy succeeds once the platform has started the new containers and
  removed the old ones**; it does not judge the application. A container
  that exits after starting does not fail the deploy: its instance status
  shows it. An instance is `healthy` while its process runs, and receives new
  connections only then; the platform restarts an exited container, which is
  `unhealthy` meanwhile, and after five consecutive restarts that each ran
  for less than a minute it stays stopped as `failed`. `healthy` describes
  the process, so request the service's endpoint after a deploy to confirm
  the application answers. `uniac logs <service>` shows what the instances
  wrote, and `--previous` the run before the last restart.
- **Logs belong to the instance's placement.** An instance keeps its current
  run and the one before it, the last 8 MiB of each, on the node that runs
  it. They go when a deploy replaces its version, a scale-down, pause or
  delete removes it, or the platform replaces it after it failed; a move to
  another node starts its runs over. Read a failing version's logs before
  deploying again.
- **`uniac exec` runs one command to completion in a running instance**, as
  the container's own process, with no shell (`-- sh -c '…'` where the image
  has one) and no terminal, and exits with the command's exit code. Its CPU
  and memory count against the instance's. The platform's fixed 120 s
  timeout or an interrupt stops the command's own process only: the rest
  of a shell's pipeline or script and anything in the background keep
  running. Every run executes the command again, so a command that changes
  data is run once on purpose, not retried blindly. A service with several
  instances needs `--instance`.
- **`uniac exec -it` opens a terminal in a running instance**, connected to
  the CLI's own, which must be a terminal; every key reaches the program,
  Ctrl-C included. The command holds at most 512 bytes. A terminal ends when
  its program exits, after 15 minutes without input, at 1 hour, or when its
  connection drops, and then its program gets SIGHUP; background processes
  keep running and nothing resumes it, so `tmux` inside keeps a session. An
  account holds 4 open terminals and an instance 2, apart from execs.
- **References resolve when a service's version is created**, against the
  services serving at that moment. `uniac deploy` creates a service's version
  after the services it references have settled, so references within one
  deploy resolve on its first run; services that reference each other in a
  cycle are created together, and on a first deploy their references to each
  other are left out with a warning until the next deploy. A changed value
  reaches another service in that service's next deployment. Services start
  independently, so applications retry their connections to one another.
- **A service stays until it is deleted.** Removing it from `uniac.yaml`
  leaves it running; `uniac service delete <name>` deletes it. Deleting a
  service keeps its volume, which `uniac volume delete <service>.<volume>`
  destroys. `uniac project delete <name>` deletes the project with its
  services, endpoints and every volume, unbound ones included; the platform
  finishes removing them after the command returns, and the name stays taken
  until it has. The delete commands ask for the typed name in a terminal;
  `--silent` answers that question on the user's behalf, so an agent passes
  it once the user has asked for that deletion, and deletes a project only
  when its user asks for it.
- **Each replica's memory is reserved on a node.** A replica no node has
  room for stays `starting`, and the deploy stays in progress until a node
  has room.
- **A larger `size_gb` (1–4096 GiB) grows a volume in place.** The deploy
  completes without waiting, and the running container sees the added space
  within seconds, without a restart. Until the storage has grown, the growth
  is pending and retried; a deploy that declares the current size or less
  withdraws it. A volume never shrinks: a deploy that declares less than its
  size is accepted and leaves the volume at its size. Storage is
  charged at the grown size. The same volume name binds the same data again,
  even at a new mount path.
- **`public_ports` on redeploy:** omitted keeps the existing exposure,
  including endpoints changed in the dashboard; `[]` removes it; a list
  replaces it. Each service has one `http` and one `tcp` endpoint at most.
- **Each service's submission proceeds on its own.** Accepted work continues
  after a local failure or an interruption; to return to an earlier release,
  deploy that release's sources or images again, which gives every declared
  service a new version. Exit 10 (`pending`) after the five-minute window
  means that service's work is still in progress; services later in
  reference order were not submitted (`not attempted`), so deploy again once
  it finishes.
- **Tokens expire, and each platform accepts only its own.** `uniac auth
  status` shows each session's expiry, issuer and whether its platform
  accepts it; `uniac auth login` stores a new one, one session per platform.
- **`env` values are stored with the deployment** and shown in the dashboard;
  keep a `uniac.yaml` that carries secret values out of version control.

Contracts: [runtime and versions](https://docs.uniac.ai/resources/service.md#runtime-and-deployment-versions), [instances](https://docs.uniac.ai/resources/service.md#instances), [logs](https://docs.uniac.ai/resources/service.md#logs), [exec](https://docs.uniac.ai/resources/service.md#exec), [size](https://docs.uniac.ai/resources/service.md#size),
[resolution](https://docs.uniac.ai/resources/service.md#resolution), [public endpoints](https://docs.uniac.ai/resources/service.md#public-endpoints),
[dashboard and removal](https://docs.uniac.ai/resources/service.md#dashboard-and-removal),
[volume lifecycle](https://docs.uniac.ai/resources/volume.md#lifecycle).

## Reading the CLI

`deploy` prints a stage record — `plan`, `link`, `build`, `push <service>`,
`submit <service>`, `observe <service>` — followed by state rows; `status`
prints state. A `service` row carrying `v<N>` means a serving version was
read. `instance <short> <status>, started <time>` rows give each instance's status
after a deploy and in `status`: a crash loop shows as `unhealthy` or `failed`
rows even when the deploy exits 0. A name-only row or a `state unread` warning means the
submission was accepted and the service's state is unknown, even at exit 0;
`uniac status <service>` reads it. `endpoint http https://… → :8080` is the
public address and the container port. `uniac logs` prints
`[<instance>] <line>` on stdout, the instance named by the start of its key. Exit codes: 2 usage, 3 auth, 4 not
linked, 5 manifest, 6 build, 7 push, 8 deployment failed or a platform read
was refused, 9 platform unreachable, 10 still in progress after five
minutes (pending); `uniac logs` uses the same codes. `uniac exec` exits
with its command's code, or with `docker exec`'s own: 125 when the CLI or the
platform failed, 126 not executable, 127 not found, 130 interrupted. A
command can exit with 125–130 too; each of the CLI's own except 130 also
writes an error block or a `uniac exec:` line on stderr, and so do a timeout,
a stopped container and truncated output. `uniac exec -it` exits the same way,
with a `uniac exec:` line for an idle or 1-hour end, a stopped container and
a connection that closed first.

## A minimal composition

```yaml
runtime: yaml
resources:
  api_definition:
    type: service
    build: .
  api:
    type: deployment
    from: api_definition
    public_ports: [{ port: 8080, type: http }]
```

`uniac plan`, `uniac project create my-app`, `uniac link my-app`,
`uniac deploy`, `uniac status` takes this from a directory holding a
`Dockerfile` that listens on port 8080 to a public HTTPS address. A two-service
composition with a database, a volume and environment references is in
[composition.md](references/composition.md#a-complete-composition); the same
walk-through with expected output is the
[quickstart](https://docs.uniac.ai/quickstart.md).

## Getting help

When sign-in or a deployment fails and the documentation does not resolve
it, tell the user where to get help; joining or writing is the user's action:

- the [Uniac Discord community](https://discord.gg/VR92F2qKjQ), for help with
  a deployment;
- support@uniac.ai, for account matters.

Both are listed under
[Getting help](https://docs.uniac.ai/cli/output.md#getting-help).
