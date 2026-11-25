---
name: light-cloud-domains
description: Put a Light Cloud app on the user's own domain (example.com or a subdomain like shop.example.com), tell them which DNS records to add or delete at their DNS provider, check verification, and fix a domain that isn't serving. Use when the user wants a custom domain, asks why their domain doesn't work yet, or wants to remove or change one.
---

# Light Cloud custom domains

Start as every Light Cloud task does: `whoami` for the workspace (`organisation_id`), then `get-workspace-overview` to find the app and any domain it already has. The production `environment_id` comes from `get-application` or `list-environments`. Never ask the user for an id.

Each environment has one custom domain. Adding a new one replaces the old one.

## Add a domain

1. `add-custom-domain` with the app, the environment and the domain. Give `www.example.com` or `example.com`: both are set up, and the other one redirects to it.
2. The result lists, per hostname:
   - `dnsRecords`: the records to create (CNAME for a subdomain, ALIAS or ANAME for a root domain, TXT for the certificate and ownership, CAA when the domain limits who may issue certificates). `host` is the name as typed at the DNS provider (`@` is the root). `required: false` means the record is only needed to switch over without downtime.
   - `removeRecords`: records to delete because they send the domain somewhere else.
   - The detected DNS provider, with a note on whether it supports a root domain, and any issues in plain words.
3. Tell the user, as a short table of type, host and value: the records to add (required ones first) and the records to delete. Pass on the provider note; if their provider can't point a root domain, suggest the `www` name.

Custom domains come with the paid plans. On Free, the first domain is refused with `PLAN_ENTITLEMENT`, naming the plan and its price: tell the user both and get a yes before `choose-plan`. A domain attached earlier keeps working.

## Check it

When the user says the records are in, call `get-custom-domain-status`. It reads public DNS again and lists what is still missing or points elsewhere. DNS changes can take from minutes to a few hours; tell the user what is still missing and check again when they ask.

Once DNS is right but the certificate hasn't been issued, call `retry-custom-domain`.

## Replace or remove

- Replacing a working domain with one whose DNS doesn't point here yet is refused with `DOMAIN_NOT_POINTING_HERE`. Explain that the site is unreachable on the new name until its DNS records exist; only if the user agrees, call `add-custom-domain` again with `force: true`.
- `remove-custom-domain` detaches the domain; the app keeps serving on its `light-cloud.io` address. Name the domain and get a yes first.
