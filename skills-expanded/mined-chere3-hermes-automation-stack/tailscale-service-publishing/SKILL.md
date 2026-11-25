---
name: tailscale-service-publishing
description: "Use when publishing services with Tailscale Serve/Funnel."
version: 1.0.0
---

# Tailscale service publishing

Publish an existing local HTTP(S) service either privately to a tailnet with Tailscale Serve or publicly through Tailscale Funnel. Treat public exposure as a security-boundary change even when the application has its own login.

## Choose the exposure mode

- Use **Serve** when only authenticated tailnet devices should reach the service.
- Use **Funnel** when arbitrary internet clients must reach it.
- Do not describe Serve as public: a `*.ts.net` URL can still be tailnet-only.
- Application authentication and network exposure are separate controls. Before enabling Funnel, confirm the target has the intended login/access control and that account registration or anonymous routes match the user's intent.

## Pre-change discovery

Capture the current state before changing it:

```bash
tailscale version
tailscale status --json
tailscale serve status
tailscale funnel status
tailscale funnel status --json
curl -sS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:PORT/
```

Record every existing listener and route. A Serve/Funnel configuration is shared state: changing one port must not silently remove or expose another port.

Confirm that Funnel prerequisites are present: MagicDNS, HTTPS certificates, a supported Tailscale release, and permission through the tailnet's `funnel` node attribute. Funnel supports only its documented TLS ports (currently 443, 8443, and 10000); verify current documentation if that matters.

## Apply the narrow change

Prefer an explicit target, public port, background mode, and non-interactive confirmation:

```bash
sudo tailscale funnel --bg --https=8443 --yes http://127.0.0.1:LOCAL_PORT
```

CLI flags precede the target. If the local user lacks operator permission, either run this one command with `sudo` or, only with user approval, persist operator access using `sudo tailscale set --operator=$USER`.

For private publication, use the corresponding `tailscale serve` command instead. Never run `serve reset` or `funnel reset` merely to change one route; those can disturb unrelated listeners.

## Verify configuration and exposure

A successful CLI message is not enough. Read the exact configuration back:

```bash
tailscale funnel status
tailscale funnel status --json
```

Require all of the following:

1. The intended hostname and port appear under `AllowFunnel`.
2. The proxy target is the expected loopback address and port.
3. Existing unrelated listeners remain in their prior mode.
4. Public DNS has records for the Funnel hostname.
5. An HTTPS request through a public Funnel ingress returns the expected application response with certificate verification enabled.
6. Authentication behavior is checked directly, such as loading `/login` and confirming the expected identity fields; do not infer this from a landing-page link.

Public DNS can take up to about ten minutes to propagate. Recursive resolvers can retain an initial NXDOMAIN response even after the authoritative zone is ready. In that case, query an authoritative nameserver and test with the returned public ingress IP:

```bash
curl --resolve HOST:PORT:PUBLIC_INGRESS_IP https://HOST:PORT/login
```

Do not use `-k`; TLS must still validate the hostname and certificate. `ssl_verify_result=0` from curl is a successful verification result.

See `references/funnel-dns-and-verification.md` for a validated DNS propagation and end-to-end verification recipe. Use `scripts/query_dns_authority.py` when `dig`, `drill`, and `nslookup` are unavailable.

## Rollback

Disable only the listener that was added:

```bash
sudo tailscale funnel --https=8443 off
```

Then read back both Serve and Funnel status and confirm unrelated routes remain unchanged.

## Reporting

Report:

- the exact public or private URL;
- whether the route is Funnel or tailnet-only Serve;
- HTTPS and application response verification;
- authentication/registration posture actually observed;
- any DNS propagation caveat still active.

Never claim the page is publicly reachable solely because `tailscale funnel status` says `Funnel on`; prove the public DNS/TLS path or state precisely what remains unverified.
