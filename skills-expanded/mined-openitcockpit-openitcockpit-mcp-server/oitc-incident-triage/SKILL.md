---
name: oitc-incident-triage
description: Investigate a failing host or service in openITCOCKPIT - find what broke, when, whether it is already handled, and what caused it. Use when someone reports an alert, asks "what is broken", or asks why a service is critical.
---

# Incident triage

Order matters. Each step rules something out, so running them out of sequence
produces confident wrong answers.

## 1. Start with the overview

```
get_problem_overview()
```

Use this first for any "what is broken" question. It separates causes from
consequences: a down host is reported once, with the unreachable hosts and the
services behind it folded underneath, instead of as a hundred separate
problems. What is already acknowledged or in a downtime is listed apart from
what nobody has picked up.

It also reports when the monitoring engine itself is behind. Stale results look
exactly like a real outage, so if the overview says the engine is struggling,
report that and stop. The individual alerts are not trustworthy yet.

## 2. Take names from a result, never from a guess

`get_host_health`, `get_service_health` and `investigate_problem` each work on
one named object. The names come from a tool that reports them:

```
get_problem_overview()
  -> down hosts: ["sw-core-1"], unhandled services: [{host: "web01", service: "HTTP"}]

# Those names now exist as values. Use them literally:
get_host_health(hostname="sw-core-1")
get_service_health(hostname="web01", servicename="HTTP")
```

When you need a name the overview did not report, search for it:

| Need | Call |
|---|---|
| Hosts by name, state, container or group | `find_hosts` |
| Services by host, name, state or group | `find_services` |
| The exact name of a template, group or contact | `list_catalog` |

A call that omits a required argument is answered with the values that would
have worked. Take one of them. Repeating the same call returns the same answer.

## 3. Look at one object

```
get_host_health(hostname="web01")
get_service_health(hostname="web01", servicename="HTTP")
```

Both report the state and since when, the recent state changes, and what likely
explains the problem: a down parent, a running downtime, an acknowledgement. You
do not need separate calls for any of that.

`get_host_health` also lists the host's services by state and which hosts depend
on it. One failing service on an otherwise healthy host is a different story
from a host where everything is red.

A host or service marked as not monitored is configured but not yet known to the
engine, usually because the configuration has not been exported since it was
created. It has no check results. That is not a fault, so do not report it as
one.

## 4. Ask what happened around it

```
investigate_problem(hostname="web01", servicename="HTTP")
```

Use this when the question is why. It reports when the problem began, whether it
happened before and for how long, which other hosts and services failed in the
same minutes, and which configuration changes and exports came shortly before.
It works on the current problem, or on the last one if the object has recovered.

Several unrelated things failing in the same minute point to a shared cause: a
network segment, a dependency, or a change somebody made.

## 5. Check whether it should have alerted

```
explain_notification(hostname="web01", servicename="HTTP")
```

Use this only for "why did nobody hear about this". It checks the conditions
Naemon checks, in the same order, and names the one that stopped the
notification.

## Reporting

State, in this order: what is broken, since when, the verbatim check output,
whether it is acknowledged or in a downtime, and only then your hypothesis,
labelled as a hypothesis. The last check time is not the start of the problem;
use the last state change for that. Quote timestamps as returned and never
convert them.

If a result says it was truncated, more is failing than you were shown. Say so
rather than reporting the visible rows as the full extent.
