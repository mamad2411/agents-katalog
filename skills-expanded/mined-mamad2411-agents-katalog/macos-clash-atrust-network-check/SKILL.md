---
name: macos-clash-atrust-network-check
description: Reuse this when the user asks things like "看看clash和atrust 是不是又干架了" or "看一下网终情况" on the Mac. It provides the repeatable low-level checklist for separating Clash proxy health from direct-routing or aTrust route problems.
argument-hint: "[target-host]"
disable-model-invocation: true
user-invocable: false
allowed-tools:
  - Bash
  - Read
  - Grep
---

# macOS Clash Verge + aTrust network check

## When to use

Use this when:
1. The user asks whether Clash Verge and aTrust are interfering.
2. The user asks for a fresh network-status check on the same Mac.
3. You need to tell apart "Clash proxy is broken" from "direct external routing/DNS is broken".

Do not use this when:
1. The machine is not the user's macOS environment under the user's home directory.
2. The task is general browser/network troubleshooting without Clash Verge, mihomo, aTrust, or EAIO in the picture.

## Inputs / context to gather

1. Confirm the task is on the user's Mac and involves Clash Verge, mihomo, aTrust, or slow/broken external networking.
2. Pick one direct-connect target and one proxied target. Default to `https://www.google.com`; if the user is in a China-network context, also test `https://www.baidu.com`.
3. If the user names a specific node or says "网终情况", plan to inspect Clash `/proxies` state too.

## Procedure

1. Check system proxy state first.
   - Run `scutil --proxy`.
   - Record whether HTTP/HTTPS/SOCKS point to `127.0.0.1:7890`.
2. Check whether both Clash and aTrust stacks are running.
   - Run `ps aux | rg -i 'clash|mihomo|verge|atrust|sangfor|eaio'`.
   - Look for `clash-verge`, `verge-mihomo`, `aTrust`, `aTrustXtunnel`, and `eaio_service`.
3. Inspect listeners and route ownership.
   - Run `lsof -nP -iTCP:7890 -iTCP:7897 -iTCP:9090 -iTCP:3456`.
   - Run `netstat -rn`.
   - Run `ifconfig`.
   - Look for `utun7` or another `utun*` carrying many internal `10.*`, `172.*`, or `198.18.*` routes.
4. Compare direct and proxied traffic against the same external target.
   - Direct: `curl -vL --max-time 12 -o /dev/null https://www.google.com`
   - Proxy: `curl -x http://127.0.0.1:7890 -vL --max-time 12 -o /dev/null https://www.google.com`
   - Optional baseline: `curl -v --max-time 8 -o /dev/null https://www.baidu.com`
5. If Clash itself needs inspection, query mihomo via the unix socket.
   - Use `/tmp/verge/verge-mihomo.sock`.
   - Read `/proxies` and inspect the active selector, current global node, delay history, and `alive` flags.
6. Report the result in the user's preferred style.
   - Lead with whether base networking is up, whether Clash proxy is healthy, and whether the problem is direct external routing.
   - Mention aTrust route ownership only if the evidence supports it.

## Efficiency plan

1. Start with `scutil --proxy`, process check, and direct-vs-proxy `curl`; these three usually answer the main question fastest.
2. Only read `/proxies` when you need node-health detail or the user is likely to switch nodes.
3. Do not spend time on `networksetup` or `ping`; they were low-value in this environment.
4. Stop once you can classify the issue into one of:
   - Clash proxy healthy, direct external route broken
   - Clash proxy unhealthy
   - both look healthy, issue likely elsewhere

## Pitfalls and fixes

- `ps` returns `operation not permitted`
  - Likely cause: the environment blocks low-level process inspection.
  - Fix: use the stronger inspection path available in the environment instead of trusting the failure as evidence.
- `ping` returns `Operation not permitted`
  - Likely cause: sandbox or local environment restriction.
  - Fix: skip `ping`; use `curl` and route/proxy inspection.
- `networksetup` returns `AuthorizationCreate() failed: -60008`
  - Likely cause: this account/environment does not allow that API path.
  - Fix: use `scutil --proxy`, `netstat`, `lsof`, and Clash `/proxies`.
- Direct Google fails but proxy Google succeeds
  - Likely cause: direct external routing/DNS path is bad while Clash is still fine.
  - Fix: report it as a route split, not as "Clash died".

## Verification checklist

1. You checked system proxy state with `scutil --proxy`.
2. You verified whether Clash and aTrust processes are both present.
3. You compared direct and proxied access to the same target.
4. You checked route/interface state enough to support any claim about aTrust ownership.
5. If you mentioned node quality, you actually read `/proxies`.
6. Your conclusion clearly distinguishes proxy health from direct-routing health.
