---
name: oitc-host-onboarding
description: Add a new host to openITCOCKPIT and give it services, without hitting container-scope rejections. Use when asked to onboard, add or start monitoring a machine. Requires write tools to be enabled.
---

# Host onboarding

Requires `OITC_ENABLE_WRITE_TOOLS=true`. If `create_host` is not in your tool
list, say so and stop.

The single most common failure here is **container scope**: openITCOCKPIT only
lets a host reference templates, contacts and timeperiods visible from its own
container, and its API does *not* check this when writing. The MCP server checks
it for you - but only if you look the values up first.

## 1. Find the target container

```
get_container_tree()                      # top level
get_container_tree("SomeTenant")          # drill down
```

Containers are tenants, locations and nodes. Pick the one the host belongs to.
If the operator named a container, confirm it exists here before using it -
`get_container_tree` returns the real paths.

## 2. Ask what that container allows

```
get_allowed_elements_for_container(object_type="host", container_name="<target>")
```

**Do this before every create.** It returns the host templates, timeperiods,
contacts, contact groups and host groups actually visible there. Choose the host
template from this list, not from `list_catalog` - the latter shows
everything you can read, which is a larger set than what this container accepts.

## 3. Create the host

Plain host:

```
create_host(
  name="web01",
  address="10.0.1.20",
  description="...",
  container_name="<target>",
  hosttemplate_name="<from step 2>",
)
```

Host monitored by the openITCOCKPIT agent in pull mode:

```
create_host(
  name="web01",
  address="10.0.1.20",
  container_name="<target>",
  agent_pull_port=3333,
)
```

With `agent_pull_port` the same tool makes two API calls - it creates the host,
then configures the agent connection - and uses the agent host template unless
you name another. It does **not** discover services from the running agent. You
still add those yourself in step 4.

## 4. Add services

```
get_allowed_elements_for_container(object_type="host", container_name="<target>")
```

Service scope follows the *host*, not the container directly, so the
authoritative list of usable service templates comes from creating against the
host:

```
create_service(hostname="web01", servicetemplate_name="<template>")
```

A service template carries two names: a display name ("Ping check") and an
internal `templateName` (`CHECK_PING`). `list_catalog` reports both and
`create_service` accepts either, but the scope error only ever quotes the
internal one - so a rejection naming templates in SHOUTING_CASE is telling you
which list it matched against, not that your name is wrong.

Leave `fields` out unless you need an override. Everything you don't set is
inherited from the service template, and from there through the host to its host
template - which is the correct, maintainable default. Only set `fields` for a
value that genuinely differs for this one service.

If a template name is rejected, the error lists the closest matches in scope.
Use one of those; do not retry with a guess.

## 5. Verify

```
get_configuration_status()
```

Expect the host and its services under what is configured but not monitored yet.
The objects exist in the configuration, but the monitoring engine only picks
them up on the next export, so there are no check results yet.

Report that plainly: the host and its services are configured, monitoring starts
with the next export. Do not imply the host is already being watched, and do not
read the absence of check results as a problem.

## Before you write anything

State to the operator: the host name and address, the target container, the host
template, and the services you intend to create. Wait for agreement. Creating
monitoring objects is easy to do and tedious to undo.
