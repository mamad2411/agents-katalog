---
name: oitc-capabilities
description: What this openITCOCKPIT server can and cannot do. Use when a request seems to need a tool you cannot find - acknowledging a problem, scheduling a downtime, deleting or disabling an object, forcing a recheck, or making a newly created host actually monitored. Read this before telling an operator something is impossible, and before inventing a tool name.
---

# What this server can and cannot do

The tool list is the whole surface. There is no hidden endpoint and no way to
pass raw API calls through, so a request that no tool covers cannot be done from
here. Say that plainly and name the alternative rather than inventing a tool
name or describing the click path as though you had performed it.

## What it can do

| Area | Tools |
|---|---|
| Current state | Host and service status, alert log entries, monitoring engine health |
| Incident context | Downtimes and acknowledgements, read-only: who, when, which comment |
| History | Check executions and state transitions, per host or per service |
| Configuration catalogue | Host and service templates, commands, contacts, groups, the container tree |
| Software inventory | Installed packages, pending updates, pending security updates |
| Creating | Hosts, services, templates, commands, contacts, and host, contact and service-template groups |
| Changing | Hosts, services, contacts, contact groups |

Creating and changing exist only when the operator set
`OITC_ENABLE_WRITE_TOOLS=true`. If those tools are absent from your list, they
are switched off, not missing.

## What it cannot do

| Request | Reality |
|---|---|
| Acknowledge a problem | Read-only here. Existing acknowledgements can be read where the tools for it are present; nothing sets one. |
| Schedule or cancel a downtime | Same: the downtime tools only read. Maintenance windows are set in the web interface. |
| Delete anything | No tool deletes a host, service, template, command, contact or group. |
| Disable or enable a host or service | Not exposed. |
| Force a recheck, or reschedule the next check | Not exposed. `nextCheck` reports when it will happen on its own. |
| Restart or reload the monitoring engine | Not exposed. At most its health can be read. |
| Trigger a configuration export | Not exposed. See below - this is the one that surprises people. |
| Read performance graph data or metrics history | Only `perfdata` on individual check rows. There is no time-series tool. |
| Anything about users, roles or permissions | Outside this server entirely. |

For each of these, the honest answer is that the action belongs in the
openITCOCKPIT web interface, and you can say exactly where the operator will
find it rather than pretending to have tried.

## The configuration-export gap

The one on that list that surprises people: a newly created host or service
comes back with `monitored: false` and stays that way until the next
configuration export, and **this server cannot trigger one**. Waiting for check
results that cannot arrive yet is the failure mode. `oitc-host-onboarding`
covers what to tell the operator.

## When an operator asks for something on the second list

State what you cannot do, in one sentence, then give them the two things that do
help: what you *can* read about the object, and where the action lives in the
web interface. For example, asked to acknowledge a critical service, report its
current state and check output, confirm whether an acknowledgement already
exists, and say that setting one is a web-interface action.

Do not offer to do it later, do not describe the API call the operator could
make by hand unless they ask, and never report an action as done.
