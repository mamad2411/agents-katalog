---
name: oitc-patch-review
description: Produce a patch and security-update overview across the monitored estate from openITCOCKPIT's software inventory. Use when asked which machines need updates, which have pending security patches, or what is installed on a host.
---

# Patch and update review

All of this reads the openITCOCKPIT agent's software inventory. A host without
the agent, or whose package-manager collection has not run, simply has no row -
that is **not** the same as "no updates pending". Say which it is.

## Estate-wide view

```
find_pending_updates(security_only=True)   # security updates only
find_pending_updates()                     # every pending update
```

Each row carries hostname, OS type and version, whether a reboot is required,
the update count, and a resolved `patches` list with current and available
version per package.

**These calls are expensive.** The server resolves every package id to its name
and versions with one API request each. `max_packages_per_host` (default 20)
caps that per host; the update *count* is always exact, only the named packages
are capped, and a row says so when it was. Start with `security_only=True` - it
is far shorter and is what usually matters - and only ask for every update when
that is what was asked for.

## Per-host detail

```
find_pending_updates(security_only=True)
  -> items: [{ hostname: "db02", os_type: "linux", available_security_updates: 3 }]

# Carry that hostname into the per-host calls - it is required and has no
# estate-wide form. find_hosts() reports host names.
list_installed_software(hostname="db02", name_filter="openssl")
list_installed_software(hostname="db02", only_updatable=True)
```

A host has thousands of packages, so always pass `name_filter` (matched
server-side) or `only_updatable=True`. Listing everything is capped at 50 rows
and tells you little. Use this to answer "is package X installed, at which
version" - the estate-wide calls above are the right tool for finding outdated
packages.

## Adding context

An update count alone does not tell an operator what to do. Enrich it:

```
find_hosts(name="db02")       # which container it belongs to, and its state
get_host_health(hostname)     # is the host even up right now, and what ails it
```

A host that is down cannot be patched; a host in a production tenant is a
different priority from one in a lab.

## Reporting

Check `truncated` on every listing first. If it is true, more hosts are affected
than you were shown - say so, and narrow with a smaller estate or a higher
`limit` rather than presenting the visible ones as the complete picture.

Group by urgency, not alphabetically:

1. Hosts with security updates **and** `reboot_required` - these need a
   maintenance window, so they have the longest lead time.
2. Hosts with security updates only.
3. Everything else, as a count rather than a full listing.

Name the packages for the security cases; a bare number is not actionable.
For the rest, a count per host is enough unless asked for detail.

State explicitly which hosts returned no inventory data at all, and that this
means "the agent has not reported", not "up to date".
