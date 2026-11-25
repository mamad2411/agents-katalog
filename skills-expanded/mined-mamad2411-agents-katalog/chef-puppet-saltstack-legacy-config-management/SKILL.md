---
name: chef-puppet-saltstack-legacy-config-management
description: >
  Provides a comparative overview of Chef, Puppet, and SaltStack for teams
  maintaining existing legacy configuration-management estates alongside
  or instead of Ansible — agent-based pull architecture, DSL/resource
  models (Chef recipes/cookbooks, Puppet manifests/catalogs, Salt
  states/pillars), and a candid assessment of where each still earns its
  keep in a modern enterprise versus where it's inertia. Use when the user
  asks to "maintain this existing Chef/Puppet/Salt estate," "write a Chef
  recipe/Puppet manifest/Salt state," "should we migrate off Puppet to
  Ansible," "why is our Puppet run applying a change we didn't expect," or
  "compare Chef vs. Puppet vs. SaltStack."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: iac-and-automation-tooling
  maturity: stable
---

# Chef, Puppet, and SaltStack Configuration Management for Legacy Enterprise

## Purpose

Chef, Puppet, and SaltStack were the dominant configuration-management
tools before Ansible's agentless, push-based model took over most new
projects. All three are still running in production at plenty of large
enterprises — often on systems that predate anyone currently on the team
— and the honest operational reality is that most of them are in
**maintenance mode**, not active greenfield adoption: teams keep them
running because a full migration is expensive and risky, not because
they're the tool a team would choose today. This skill is deliberately
scoped to that reality — how to safely operate and extend an *existing*
Chef/Puppet/Salt estate, how the three differ from each other and from
Ansible, and how to reason about whether/when migrating off one of them
is actually worth it. It is not a pitch for greenfield adoption of any of
the three; for that, see
[ansible-playbook-and-role-design](../ansible-playbook-and-role-design/SKILL.md),
which is the tool most new configuration-management work in this space
should default to today unless a specific existing estate says otherwise.

## When to use

- Extending or fixing an existing Chef cookbook, Puppet module, or Salt
  state/formula in a production estate that already runs one of these
  tools.
- Diagnosing an agent-based run (`chef-client`, `puppet agent`,
  `salt-minion`) that applied an unexpected change, drifted from the last
  known-good state, or failed a periodic scheduled run silently.
- Deciding whether a team should keep maintaining Chef/Puppet/Salt for a
  given estate, migrate it to Ansible, or (more commonly, and often more
  realistically) let it run largely untouched while all *new*
  configuration management work happens in Ansible.
- Understanding the DSL/resource model of whichever of the three a legacy
  estate uses, when the team maintaining it didn't originally write it.
- Explaining to stakeholders, in concrete terms, what "legacy config
  management" risk actually means operationally (unpatched agent
  versions, an unmaintained master/server, catalog compilation failures)
  so a maintenance-vs-migrate decision is made on real tradeoffs.

## Prerequisites & environment

- **Chef**: a Chef Infra Server (or Chef Infra Client in solo/zero mode)
  and `chef-client` installed on managed nodes; cookbooks written in a
  Ruby-based DSL, tested with `cookstyle` (linting) and Test Kitchen (`kitchen
  converge`) against a driver (Docker, Vagrant). Chef's ecosystem has
  consolidated significantly — confirm whether an estate is on the
  original Chef Infra product or has moved to Progress Chef's current
  packaging before assuming tooling/support availability.
- **Puppet**: a Puppet Server (or `puppet apply` masterless mode) and
  `puppet agent` on managed nodes, running on a pull schedule (default a
  periodic interval, commonly around every 30 minutes) rather than an
  on-demand push; manifests written in Puppet's own declarative DSL,
  organized into modules with a defined class/parameter interface.
  `puppet-lint` for static checks.
- **SaltStack**: a Salt Master and `salt-minion` on managed nodes (or
  masterless `salt-call --local`), using YAML state files (SLS) rendered
  through Jinja templating by default, with pillar data for
  environment/host-specific variables kept separate from state logic —
  conceptually close to Ansible's `group_vars`/`host_vars` split. Salt
  also supports an event-driven reactor system and fast parallel
  execution over its own ZeroMQ/message-bus transport, which is genuinely
  differentiated from the other two for very large, low-latency fleets.
- Whichever tool is in play, confirm the **agent version running on
  managed nodes**, not just the server/master version — legacy estates
  frequently have nodes running agent versions years behind the
  server, and DSL/module compatibility can silently break across that
  gap.
- Least-privilege: the agent's run-as user (commonly root, since these
  tools manage system-level state) should be scoped by what the
  server/master authorizes it to apply, not implicitly trusted to run
  arbitrary code pushed from anywhere.

## Step-by-step guidance

1. **Identify which of the three (if more than one) an estate actually
   uses, and its architecture mode** (agent+server vs. masterless) before
   touching anything — this determines how a change actually reaches
   nodes and on what schedule:
   - Chef: check for a Chef Infra Server URL in `/etc/chef/client.rb`
     on a node, or solo/zero mode with no server at all.
   - Puppet: check `puppet config print server` on a node; masterless
     estates instead schedule `puppet apply` via cron/systemd timer.
   - Salt: check `/etc/salt/minion` for a configured `master:` — a
     masterless estate instead schedules `salt-call --local` runs.

2. **Read the resource/state model before writing new code in an
   unfamiliar DSL** — the three model desired state differently enough
   that copy-pasting patterns between them doesn't work cleanly:
   ```ruby
   # Chef cookbook resource (Ruby DSL)
   package 'nginx' do
     action :install
   end

   template '/etc/nginx/sites-available/app.conf' do
     source 'nginx.conf.erb'
     variables(client_max_body_size: node['app']['max_body_size'])
     notifies :reload, 'service[nginx]', :delayed
   end

   service 'nginx' do
     action [:enable, :start]
   end
   ```
   ```puppet
   # Puppet manifest (Puppet DSL)
   package { 'nginx':
     ensure => installed,
   }

   file { '/etc/nginx/sites-available/app.conf':
     ensure  => file,
     content => template('app/nginx.conf.erb'),
     notify  => Service['nginx'],
   }

   service { 'nginx':
     ensure => running,
     enable => true,
   }
   ```
   ```yaml
   # Salt state (SLS, YAML + Jinja)
   nginx-package:
     pkg.installed:
       - name: nginx

   /etc/nginx/sites-available/app.conf:
     file.managed:
       - source: salt://app/nginx.conf.jinja
       - template: jinja
       - context:
           client_max_body_size: {{ pillar['app']['max_body_size'] }}
       - watch_in:
         - service: nginx-service

   nginx-service:
     service.running:
       - name: nginx
       - enable: True
   ```
   All three converge toward the same idempotent end state as the
   Ansible equivalent in
   [ansible-playbook-and-role-design](../ansible-playbook-and-role-design/SKILL.md)
   — the difference is the pull/agent architecture and DSL, not the
   underlying idempotency goal.

3. **Test changes against a disposable target before a real run**, using
   each tool's own convergence-testing pattern rather than editing
   directly against production nodes:
   ```bash
   # Chef: Test Kitchen against a Docker/Vagrant driver
   kitchen converge
   kitchen verify   # runs InSpec/Serverspec assertions

   # Puppet: puppet apply --noop for a dry-run against a real/test node
   puppet apply --noop site.pp

   # Salt: test=True dry-run
   salt 'web-*' state.apply app test=True
   ```
   `puppet apply --noop` and Salt's `test=True` are the closest
   equivalents to Ansible's `--check --diff` — review what *would*
   change before letting a scheduled agent run apply it for real.

4. **Understand each tool's run/convergence schedule**, since none of
   these push changes on-demand by default the way an Ansible playbook
   run does:
   - Chef and Puppet agents typically run on a periodic interval (commonly
     configured in the 15-30 minute range) pulling and applying the
     latest catalog/cookbook version from the server — a change merged to
     the cookbook/module repo doesn't reach nodes until their next
     scheduled run (or an explicit `chef-client`/`puppet agent -t`
     triggered manually).
   - Salt supports both scheduled minion runs and on-demand pushes from
     the master (`salt '*' state.apply`), giving it a push-like option
     the other two lack without extra tooling — confirm which mode a
     given estate actually relies on before assuming a change is "live."

5. **Diagnose an unexpected applied change by reading the catalog/state
   compilation, not just the run log**, since the actual decision of
   *what* to apply happens at compile time before the agent executes
   anything:
   ```bash
   # Puppet: view the compiled catalog for a node without applying it
   puppet catalog compile <node-name>

   # Chef: run in why-run mode (best-effort dry-run; not all resources
   # support it accurately, similar caveat to Ansible --check)
   chef-client --why-run

   # Salt: show the compiled low-state without applying
   salt 'web-01' state.show_sls app
   ```
   An unexpected change is often traceable to a Hiera/data-binding
   (Puppet), a role/environment cookbook version pin (Chef), or a pillar
   override (Salt) that changed upstream of the specific manifest/recipe/
   state file that appeared to be the direct cause.

6. **Decide migration-vs-maintain deliberately, per estate, not as a
   blanket policy.** A small, stable, rarely-touched Puppet estate
   managing a handful of legacy hosts is often cheaper to leave alone
   than to migrate; a large, actively-changing Chef estate with frequent
   cookbook churn and a team that already knows Ansible better is a
   stronger migration candidate. Weigh:
   - **Migration cost**: rewriting and re-testing every
     cookbook/manifest/state, plus the risk window while both systems
     could theoretically manage the same nodes.
   - **Maintenance cost of staying**: agent/server upgrade lag, shrinking
     pool of engineers who know the DSL, and the compounding difficulty
     of onboarding new team members to a tool they've never used
     elsewhere.
   - A common pragmatic middle path: freeze the legacy tool's scope
     (stop adding new nodes/cookbooks to it), route all *new*
     configuration-management work through Ansible, and let the legacy
     estate shrink by attrition as nodes are decommissioned/replaced,
     rather than committing to a big-bang rewrite.

## Best practices

- Never assume Chef/Puppet/Salt syntax patterns transfer directly from
  Ansible experience (or between each other) — the resource/state
  ordering and dependency models (Puppet's dependency graph and
  notify/require chains, Chef's sequential resource execution with
  explicit `notifies`/`subscribes`, Salt's `require`/`watch`/`onchanges`)
  are each their own model and behave subtly differently under the same-
  looking code.
- Version-pin cookbook/module/formula dependencies the same way
  `requirements.yml` pins Ansible roles/collections
  (`metadata.rb`'s `depends`, a Puppetfile's module refs, a Salt
  `fileserver`/GitFS pinned ref) so an upstream dependency doesn't
  silently change behavior on the next agent run.
- Keep environment-specific data (Hiera for Puppet, data bags/roles for
  Chef, pillar for Salt) separate from the logic that consumes it — the
  same separation Ansible enforces via `group_vars`/`host_vars`, and for
  the same reason: the same code should run unmodified across
  environments with only the data differing.
- Treat a legacy estate's server/master as a real piece of
  infrastructure needing its own patching/upgrade cadence — an
  end-of-support Chef Server or Puppet Server version is a genuine
  security liability, not just technical debt to defer indefinitely.
- Document, explicitly, whichever tool(s) an organization considers
  "legacy, maintenance-only" versus the one that's the default for new
  work — an undocumented mixed estate where different teams
  independently pick different tools for new projects compounds the
  long-term maintenance burden this skill exists to manage.
- Run whatever dry-run/no-op mode is available (`--noop`, `test=True`,
  `--why-run`) before any change lands on a schedule that will apply it
  automatically and unattended.

## Common pitfalls

- **Symptom:** A scheduled Puppet/Chef agent run applies a change nobody
  intended, hours after a seemingly unrelated commit merged elsewhere in
  the repo.
  **Fix:** Check for a shared data source (Hiera hierarchy, a role
  cookbook, a common pillar file) that the seemingly unrelated commit
  actually touched — in all three tools, data/role layers are frequently
  shared across many manifests/recipes/states, so a change to shared
  data can silently ripple into many nodes' next scheduled run. Compile
  the catalog/state for the affected node (step 5) to see the actual
  resolved change before assuming the run log's stated resource is the
  full story.

- **Symptom:** A team inherits a Puppet/Chef/Salt estate with no one left
  who wrote the original manifests/cookbooks/states, and small changes
  take far longer than expected because the DSL and module structure are
  unfamiliar.
  **Fix:** This is exactly the maintenance-cost side of the
  migrate-vs-maintain tradeoff in step 6 — don't default to a full
  rewrite reflexively; first invest in understanding the existing
  dependency graph (`puppet catalog compile`, Chef's cookbook dependency
  tree, Salt's `state.show_sls`) enough to make small, safe changes, and
  make the migration decision deliberately with real cost estimates
  rather than out of unfamiliarity-driven frustration.

- **Symptom:** Two configuration-management tools (e.g. a legacy Puppet
  estate and a newer Ansible rollout) both manage the same node, and
  changes made by one get silently reverted by the other's next
  scheduled/triggered run.
  **Fix:** Assign exactly one tool ownership per node/resource, the same
  single-owner principle as the Terraform/Ansible split in
  [ansible-playbook-and-role-design](../ansible-playbook-and-role-design/SKILL.md)
  — during a migration, move a node's ownership atomically (disable the
  old agent on that node before Ansible starts managing it), rather than
  running both indefinitely against the same host.

- **Symptom:** An agent on a managed node hasn't successfully checked in
  for months, and nobody noticed because there's no alerting on stale
  runs.
  **Fix:** A silently-stopped agent means that node has been drifting
  unmanaged (and unpatched via the config-management path) for as long as
  it's been broken. Alert on run-report staleness (Puppet's
  `puppet-agent --test` report timestamps via PuppetDB, Chef's reporting
  via Chef Automate/Data Collector, Salt's minion return tracking) the
  same way any other critical scheduled job would be monitored for
  silent failure.

- **Symptom:** A `puppet apply --noop`/`salt ... test=True` dry-run shows
  no changes, but the same run applied for real changes something
  unexpected.
  **Fix:** Similar to Ansible's `--check` limitation, no-op/test modes
  can't always accurately predict resources whose behavior depends on
  runtime state produced earlier in the same run, or on external systems
  the dry-run doesn't query identically to a real run. Treat dry-run
  output as a strong signal, not a guarantee, and roll out to a small
  canary set of nodes for anything with meaningfully broad blast radius
  before a fleet-wide scheduled run picks it up.

## Worked example

**Scenario:** A team inherits a Puppet estate managing 40 legacy hosts.
They need to add a new nginx `client_max_body_size` setting (mirroring
the Ansible worked example in
[ansible-playbook-and-role-design](../ansible-playbook-and-role-design/SKILL.md))
without disrupting the existing agent-based rollout, and they want to
confirm the change before letting the fleet's next scheduled run apply
it everywhere.

`hieradata/common.yaml` (environment data, analogous to Ansible's
`group_vars`):
```yaml
app::nginx_client_max_body_size: "10m"
```

`hieradata/nodes/web-prod.yaml` (node-specific override):
```yaml
app::nginx_client_max_body_size: "25m"
```

`manifests/nginx.pp`:
```puppet
class app::nginx (
  String $nginx_client_max_body_size = lookup('app::nginx_client_max_body_size'),
) {
  package { 'nginx':
    ensure => installed,
  }

  file { '/etc/nginx/conf.d/app.conf':
    ensure  => file,
    content => template('app/nginx_app.conf.erb'),
    require => Package['nginx'],
    notify  => Service['nginx'],
  }

  service { 'nginx':
    ensure => running,
    enable => true,
  }
}
```

Dry-run against the compiled catalog for one node before the change is
merged fleet-wide:
```bash
puppet catalog compile web-prod-01
puppet apply --noop --modulepath=/etc/puppetlabs/code/environments/production/modules manifests/site.pp
# Notice: /Stage[main]/App::Nginx/File[/etc/nginx/conf.d/app.conf]/content:
#   --- current content
#   +++ new content
#   -   client_max_body_size 10m;
#   +   client_max_body_size 25m;
# Notice: Class[App::Nginx]: Would have triggered 'refresh' from 1 event
```
Reviewing that no-op diff confirms only the intended node-specific
override changes, the same "review before it's live" discipline as
`ansible-playbook --check --diff`, before the change is merged and
picked up by `web-prod-01`'s next scheduled Puppet agent run (and
propagated to the rest of the `web-prod` node group on their own
schedules, batch-verified via PuppetDB report staleness rather than a
single fleet-wide push).

## Cross-references

- [ansible-playbook-and-role-design](../ansible-playbook-and-role-design/SKILL.md) — the agentless, push-based default this skill assumes new configuration-management work should target; the closest cross-tool comparison for idempotency and data/logic separation patterns.
- [infrastructure-as-code-terraform](../../../devops/skills/infrastructure-as-code-terraform/SKILL.md) — the provisioning-layer counterpart; Chef/Puppet/Salt (like Ansible) configure hosts that already exist rather than creating/destroying infrastructure.
- [python-automation-scripting-for-ops](../python-automation-scripting-for-ops/SKILL.md) — a lighter-weight alternative worth considering for narrow one-off automation that doesn't justify a full config-management tool's agent/server overhead.
