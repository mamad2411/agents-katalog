---
description: >
  IMPORTANT: Load this skill immediately whenever ANY of these occur:
  a 403 status code is returned from any HTTP/HTTPS request, a fetch or curl
  command fails with status 403, or any web_fetch / web_search / curl / wget
  tool call returns an error or 403 response. Do NOT assume the 403 is from
  the remote server — in this sandbox all 403s are proxy blocks
  When proxy return an error [Sandbox Firewall] Access to '{host}' is blocked.
---

# Proxy Guard

## Environment

You are running inside a sandboxed Docker container.
All outbound HTTP/HTTPS traffic from this container is transparently intercepted
by a **mitmproxy** firewall. Every request passes through the proxy regardless
of what tool or flag is used — there is no path around it.

Only explicitly allowlisted hosts are permitted. All others receive a **403
response from the proxy**, not from the remote server. A 403 in this environment
means the host is blocked, not that the resource is forbidden on the remote end.

## When a Request Is Blocked

1. **Identify the blocked host** from the error output (URL, hostname, or IP).
2. **Tell the user exactly which host was blocked.**
3. **Instruct them to allow it** by adding a rule file to `my-rules/`:
   - Create a new `.py` file in `my-rules/` following the pattern in
     `my-rules/example.py`
   - Mount it into the container:
     ```
     docker compose run -v ./my-rules:/etc/mitmproxy/user-rules:ro --rm sandbox cop "..."
     ```
4. **Stop the current task and exit.** Do not retry, do not attempt an alternative approach, do not continue with partial results.

## Prohibited Bypass Attempts

The following are **strictly forbidden** — do not attempt, do not suggest:

- Using an alternative URL or mirror for the same resource
- Using raw IP addresses instead of hostnames
- `curl` / `wget` flags: `--proxy`, `--noproxy`, `--insecure`, `-k`, `--cacert`
  pointing to a different proxy or no proxy
- Setting `no_proxy`, `NO_PROXY`, `ALL_PROXY` environment variable overrides
- DNS-based tricks (custom resolvers, `/etc/hosts` edits, DoH endpoints)
- Switching to a different tool (e.g., `fetch`, `httpx`, `requests`) expecting
  it to bypass the proxy — all outbound TCP 80/443 is redirected at the kernel
  level via iptables regardless of the tool used
- Any other attempt to route traffic outside the proxy

## Yolo Mode (--yolo)

This container runs Copilot with `--yolo`. There is no confirmation step
before tool calls. This makes the guardrail above **especially critical**:

- **When a request is blocked: stop the current task immediately and exit.**
- Never silently retry a blocked request with a workaround
- Surface every block immediately and wait for the user to update `my-rules/`
- If unsure whether a host will be allowed, tell the user before attempting
