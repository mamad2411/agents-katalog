---
name: erlang-otp-release-handling
description: >
  OTP release handling for owned Erlang/Elixir systems: relx/mix release
  structure, versioned apps, config/sys.config/vm.args, upgrade/downgrade
  considerations, cookie/distribution safety, and release scripts. Use when
  building OTP releases, hot upgrade feasibility, or deploy of BEAM releases—
  not GenServer coding alone (see elixir-genserver-basics).
---

# Erlang OTP Release Handling

## Scope And Authorization

- **In scope:** BEAM releases and nodes you operate.
- **Out of scope:** Attaching to production distribution ports without authorization; guessing cookies on foreign nodes.
- Hot upgrades are powerful and risky—prefer rolling cold deploys unless you have tested `appup`/`relup`.
- Erlang cookies are cluster secrets—store and rotate carefully.
- Pair with `elixir-genserver-basics` for process design and `code-quality-standards`.

## When To Use

- Packaging Elixir/Erlang with `mix release` or rebar3/relx.
- Defining release config providers, runtime env, and secrets injection.
- Evaluating hot code upgrade vs rolling restart.
- Hardening distributed Erlang (tls distribution, cookie, port exposure).
- Debugging release start failures (`foreground`, heart, boot scripts).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| GenServer patterns | `elixir-genserver-basics` |
| 12-factor env config general | `env-config-12factor` |
| Container image scanning | `ecr-image-scanning` |
| Secrets program | `secrets-management-hygiene` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Release | Self-contained ERTS + apps under `_build/.../rel` |
| Config | `runtime.exs` / config providers; not only compile-time |
| Names | Permanent app versions for upgrades |
| Upgrade | `appup` instructions; state migration in `code_change` |
| Dist | Cookie + TLS; never open EPMD publicly |
| Scripts | `bin/myapp start|stop|remote` |

## Workflow

### 1. Confirm scope and success criteria

1. Apps included, ERTS version, deploy topology (single node vs cluster).
2. Success: reproducible release artifact; clean start/stop; config via runtime env; dist locked down.

### 2. Inventory current packaging

```bash
# Elixir
cat mix.exs | head
ls rel/ 2>/dev/null
mix release --help | head
# Erlang/rebar3
ls rebar.config _build/default/rel 2>/dev/null
```

1. Note compile-time vs runtime config.
2. Check whether releases embed secrets.

### 3. Baseline run

```bash
MIX_ENV=prod mix release
_build/prod/rel/myapp/bin/myapp start
_build/prod/rel/myapp/bin/myapp rpc 'IO.puts(:ok)'
_build/prod/rel/myapp/bin/myapp stop
```

1. Capture boot errors (missing env, migrations).
2. Record cookie generation behavior.

### 4. Structure a solid release

```elixir
# mix.exs releases sketch
def releases do
  [
    myapp: [
      include_executables_for: [:unix],
      applications: [runtime_tools: :permanent],
      steps: [:assemble, :tar]
    ]
  ]
end
```

1. Use `config/runtime.exs` for secrets and port binding from env.
2. `vm.args` / `REMOTE_IP` carefully for container networking.
3. Include `runtime_tools` for recon in emergencies; control who can remote shell.

### 5. Upgrades and deploys

| Strategy | When |
| --- | --- |
| Rolling restart | Default for most web apps |
| Blue/green | Need instant rollback of whole node |
| Hot upgrade | Long-lived state processes; rare; high discipline |

1. For hot upgrade: maintain `appup` files; test `release_handler` on stage; practice downgrade.
2. Ensure `GenServer.code_change/3` for state format changes.
3. Prefer immutable infra images with new release tarball over in-place patch when team is small.

### 6. Distribution security

```bash
# Do not expose EPMD 4369 / dist ports on public interfaces
# Prefer: -proto_dist inet_tls and proper certificates (modern OTP)
# Cookie via file with 0400 perms or secrets mount — not world-readable
```

1. Disable distributed Erlang if unused.
2. If clustering: network policies, TLS distribution, strong cookies.
3. Audit `bin/myapp remote` access in prod.

### 7. Verify and hand off

```bash
# Version identity
_build/prod/rel/myapp/bin/myapp eval 'IO.inspect(Application.spec(:myapp, :vsn))'
```

1. Start on clean host matching prod OS.
2. Rollback: previous release tarball + data migration reverse plan.
3. Document heart/systemd unit and log locations.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Config | runtime.exs + env | Secrets compiled into beam |
| Dist | TLS + private net | EPMD on 0.0.0.0 public |
| Upgrade | Tested appup or rolling | Live `l(Module)` in prod ad-hoc |
| Cookie | Secret manager | Cookie `secret` in git |
| Artifact | Versioned tarball/SBOM | Copy `_build/dev` to prod |

## Output Checklist

- [ ] Release builds reproducibly in CI
- [ ] Runtime config/secrets via env or provider
- [ ] Start/stop/rpc verified
- [ ] Dist/cookie exposure reviewed
- [ ] Deploy/rollback strategy documented
- [ ] Hot upgrade either tested or explicitly out of scope
- [ ] Residual risk noted

## Rules

- Owned nodes only for remote shells.
- Treat cookies and dist as production credentials.
- Prefer rolling deploys unless hot upgrade is proven.
- Never ship dev builds as releases.
- Process design → `elixir-genserver-basics`.
