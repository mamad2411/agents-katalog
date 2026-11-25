---
name: add-custom-domain
description: |
  Add a custom domain to a Temps project and provision an automatic SSL/TLS certificate via Let's Encrypt, driven entirely from the `@temps-sdk/cli` CLI. Handles subdomains, apex domains, HTTP-01 and DNS-01 challenges, and wildcard domains. Use when the user wants to: (1) Add a custom domain to their Temps app, (2) Set up HTTPS/SSL for a deployment, (3) Point their own domain at a Temps project, (4) Add a wildcard domain, (5) Configure DNS for Temps. Triggers: "add custom domain", "point my domain at temps", "set up ssl", "https for my app", "wildcard domain", "add domain to project".
---

# Add a Custom Domain

Add a custom domain to a Temps project and get automatic HTTPS. This skill drives
the whole flow from the CLI; the human equivalent is **Project → Domains → Add Domain**
in the dashboard.

## When to use

The user wants their own domain (e.g. `app.example.com`) serving a Temps project,
with an SSL certificate, instead of the auto-assigned subdomain.

## Prerequisites

- The Temps CLI is authenticated. Verify, and log in to the user's instance if needed
  (`login` is a top-level command; the instance URL is the positional argument):
  ```bash
  bunx @temps-sdk/cli whoami || bunx @temps-sdk/cli login "<instance_url>"
  ```
- The user knows the **domain** to add and which **project** it belongs to.
- The user can edit DNS for the domain (or has a DNS provider connected in Temps
  for DNS-01 / wildcard).

## Steps

1. **Identify the project.** If the user gave a name but not an ID, list projects
   and resolve it:
   ```bash
   bunx @temps-sdk/cli projects list --json
   ```
   Note the numeric `id` of the target project. Use it as `<project-id>` below.

2. **Create the DNS record** at the user's DNS provider so the domain points at
   the Temps server. Tell the user exactly what to add (you cannot create this for
   them unless a DNS provider is connected in Temps):
   - **Subdomain** (`app.example.com`): `A` record, name `app`, value = the
     server's public IP. A `CNAME` to the server hostname also works.
   - **Apex** (`example.com`): `A` record, name `@`, value = the server's IP.
     (CNAMEs are not allowed at the zone root.)
   - If the user is on **Cloudflare**, have them set the record to **DNS only**
     (grey cloud) during issuance so Temps' Let's Encrypt challenge isn't proxied.

3. **Add the domain to the project.** Default is the HTTP-01 challenge, handled
   automatically:
   ```bash
   bunx @temps-sdk/cli custom-domains create --project-id <project-id> -d app.example.com -y
   ```
   - **Apex + Cloudflare/another provider connected, or port 80 not reachable:**
     use DNS-01 instead (see Wildcard below) — confirm a DNS provider is connected
     in **Settings → DNS Providers** first.

4. **Wildcard domains** (`*.example.com`) require DNS-01 and a connected DNS
   provider. Confirm the provider is connected, then add the wildcard the same way:
   ```bash
   bunx @temps-sdk/cli custom-domains create --project-id <project-id> -d "*.example.com" -y
   ```
   Temps creates the `_acme-challenge` TXT record automatically via the provider.

## Verify

```bash
bunx @temps-sdk/cli custom-domains list --project-id <project-id>
```

The domain should progress to **active** once DNS propagates and the certificate
is issued (usually under a minute for HTTP-01). You can confirm DNS independently:

```bash
dig +short app.example.com A
```

If the domain stays pending: verify the DNS record resolves to the server, that
port 80 is reachable (HTTP-01), and — on Cloudflare — that the proxy is off during
issuance. Certificates renew automatically ~30 days before expiry.

## Related

- Dashboard path: **Project → Domains → Add Domain**
- Doc: https://temps.sh/docs/add-a-custom-domain
- CLI group: `bunx @temps-sdk/cli custom-domains --help`
- Full CLI reference: the `temps-cli` skill covers all 440+ `bunx @temps-sdk/cli`
  commands.
