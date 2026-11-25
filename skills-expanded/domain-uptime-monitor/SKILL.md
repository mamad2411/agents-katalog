---
name: domain-uptime-monitor
description: Probe a list of domains with a real content check per domain, so a suspended deployment or a broken build that still returns HTTP 200 is caught, and alert only when a domain changes state. Use when asked to monitor uptime, watch production domains, set up a health check, or work out why a site looked up but was not.
---

# Domain Uptime Monitor

## The failure this exists for

HTTP 200 is not proof a site is working:

- A suspended or payment-disabled deployment serves a billing page with 200.
- A broken build serves an empty shell with 200.
- A partial deploy serves the old page while the API behind it is gone.
- A misconfigured origin leaves the marketing page at 200 while every signed-in
  action fails.

A monitor that checks the status code reports all four as healthy. Every domain
here declares what a working response actually contains.

## Prerequisites

- Python 3.9 or later, standard library only.
- Outbound HTTPS to the domains you list.
- **No credential is needed to detect.** Email alerting is optional and needs a
  [Resend](https://resend.com) API key in `RESEND_API_KEY` and a sender domain
  verified on that account. Without the key, detection still runs and the report
  is still written; only the send is skipped. `--no-email` turns sending off
  explicitly.

`notify_email` has no default and will not get one. Ask the user for the address.

## Writing the config

Start from [`examples/domains.example.json`](examples/domains.example.json). Each
domain takes a `host`, a `tier`, and a `check`.

**Tier.** `critical` domains alert and set the exit code. `standard` domains are
probed and reported but never alert. Put revenue and API paths in `critical` and
be strict about it: a monitor that alerts on everything gets muted, and then it
alerts on nothing.

**Check types.**

| type | passes when | use for |
| --- | --- | --- |
| `status` | status in `allow`, or any 2xx/3xx if `allow` is absent | redirects, hosts where you have nothing better |
| `marker` | status is `expect_status` (default 200) **and** `marker` is in the body | any rendered page — this is the one that catches a 200 that is really off |
| `json` | status matches, body parses, and the dotted `field` `equals` or `contains` the value | health endpoints; `field` may be nested, e.g. `checks.db` |

**Choosing a marker.** Pick a string only the real page contains: a product name
in the nav, a footer line, a specific heading. Do not use a string that a hosting
error page would also contain, and do not use a build hash — it changes on every
deploy and you will get a false alarm instead of a real one.

**A host that is meant to return 401 or 403** is healthy when it does. Put those
codes in `allow`, or it alerts every single day until someone mutes it.

**Probing one host twice** (the homepage and the checkout page, say) needs a
distinct `name` on each entry. Results are keyed by that label, so the config is
rejected rather than quietly reporting one fewer domain than you listed.

**Compressed responses are decoded before the marker is looked for.** Some servers
gzip even when the request asks for `identity`, and a raw compressed body contains
no readable marker at all. `br` cannot be decoded with the standard library and is
left as-is, so a `br`-only origin needs a `status` or `json` check instead.

**`post_check`** probes an authenticated write path on a domain whose homepage is
fine. Declare the signature of the break you have actually seen in `fail_if`
(`status`, `body_contains`); anything in `ok_status` passes. Only add one where
you know what the broken response looks like — a speculative write probe produces
false alarms and sends traffic to an endpoint on every run.

## Running it

```
python scripts/uptime_probe.py --config domains.json \
    --state .uptime/state.json --report out/report.md \
    --notify-email ops@yourdomain --email-from "Uptime <uptime@yourdomain>"
```

Exit codes: `0` all critical up, `1` a critical domain is down, `2` bad config,
`3` the probe could not run. Put it on cron and let the exit code drive whatever
you already have.

## Alerting

Alerts fire on **state change only**, against `--state`. A domain that has been
down for a week sends one email, not seven, and sends one more when it recovers.

A host with no previous state is new, not a transition, so adding a domain to the
config never pages anyone.

A send failure is printed to stderr and never masks the detection result: the
report and the exit code are correct whether or not the email went out.

## Boundaries

- Read-only against your own domains, plus the `post_check` request where you
  configure one.
- `RESEND_API_KEY` is read from the environment inside the send function. Never
  pass it as an argument and never write it into the config file.
- Do not raise a domain to `critical` to make it more visible. Tier is about who
  gets woken up.
