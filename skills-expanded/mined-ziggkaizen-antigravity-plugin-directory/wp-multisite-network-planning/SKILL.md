---
name: wp-multisite-network-planning
description: Plans and reviews WordPress Multisite topology, prerequisites, conversion readiness, domains, rewrites, shared resources, governance, and recovery. Use before creating, converting, moving, or materially restructuring a network.
---

# WordPress Multisite Network Planning

Use this skill before network creation, single-site conversion, topology changes, major domain changes, or migrations into Multisite.

## Required Inputs

Collect:

- business reason for Multisite
- expected site count and growth
- trust boundary between site owners
- shared and site-specific plugins/themes
- domain-based or path-based preference
- DNS, wildcard DNS, TLS, proxy, CDN, cache, and mail constraints
- hosting and database limits
- backup, restore, staging, and rollback capabilities
- WordPress, PHP, database, web-server, and WP-CLI versions

## Decision Rules

- Choose Multisite only when shared governance, shared code, and centralized operations outweigh isolation needs.
- Prefer separate WordPress installations when sites need independent release cadence, security boundaries, databases, hosting, or ownership.
- Decide domain-based versus path-based before implementation; changing later is possible but operationally risky.
- Treat shared users as identity sharing, not automatic site membership.
- Treat site content and most site settings as isolated in per-site tables.
- Plan upload storage, object cache keying, cron volume, mail, search, analytics, and observability for many sites.

## Workflow

Use `workflows/network-readiness-workflow.md`.

## Resources

Use `resources/network-topology-decision-matrix.md`.

## Example

Use `examples/network-readiness-record.md` as a planning record.
