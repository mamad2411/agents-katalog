---
name: tls-certificates
description: Owns the TLS certificate over its whole life, not just the day it is installed: obtaining it, installing it on the terminating layer, enforcing HTTPS with a redirect and HSTS, renewing it automatically before it expires, monitoring for the expiry that takes a site down anyway, and keeping the private key out of the repository and the logs. Covers development versus production certificates and the reverse proxy that terminates them. Use for any HTTPS setup, certificate renewal or expiry incident.
license: MIT
metadata:
  category: devops-skills
  version: 1.0.0
  depends_on: [engineering-core, devops-core]
  outputs: [certificate-plan, tls-configuration, renewal-automation, expiry-monitoring]
---

# TLS Certificates

The certificate that serves HTTPS is not a one-time install; it expires, and a
site whose certificate expired is as down as a site that crashed, with a
browser warning that scares every visitor away. This skill owns the whole life:
obtaining, installing, enforcing, renewing, monitoring, and keeping the private
key safe.

## 1. Obtaining

```
automated (ACME)    the default: a certificate authority that issues and
                    renews over ACME, such as the free ones, so renewal can be
                    automatic. Right for almost every public site.
commercial          when an organisation requires a named issuer, extended
                    validation, or a longer support contract
wildcard vs SAN     a wildcard covers every subdomain of one level; a SAN
                    (multi-domain) certificate names each host. Choose by how
                    many and how dynamic the hosts are.
```

The choice is driven by whether renewal can be automated, because a certificate
that must be renewed by hand is a certificate that will one day be forgotten.

## 2. Installing, on the terminating layer

TLS is terminated somewhere: a reverse proxy, a load balancer, the platform's
edge, or the application. Install the certificate where termination actually
happens, and know where that is.

```
reverse proxy or load balancer   the common case: the certificate lives there,
                                 the application speaks plain HTTP behind it on
                                 a private network
platform edge                    a managed platform terminates TLS for you; the
                                 certificate is the platform's to manage, and
                                 the job is configuration, not files
application                      only when nothing sits in front; then the
                                 application loads the certificate and the key
```

## 3. Enforcing HTTPS

A certificate installed but not enforced leaves a plain-HTTP door open.

```
redirect    plain HTTP redirects to HTTPS, permanently
HSTS        the Strict-Transport-Security header tells the browser to use
            HTTPS for a stated period; add includeSubDomains and consider
            preload once the whole domain is HTTPS and will stay so
cookies     session and sensitive cookies carry the Secure flag, so they never
            travel over plain HTTP
```

HSTS is owned jointly with `security-headers`; the certificate makes it safe to
send, and enforcement makes it true.

## 4. Renewing, before it expires

Renewal is the item that gets forgotten, so it is automated and it is watched.

```
automate    ACME renewal on a schedule that runs well before expiry, with a
            reload of the terminating layer so the new certificate is served
prove       the automation is verified to have actually renewed once, not
            assumed to work; a renewal cron that silently fails is a time bomb
margin      renew with room to spare, so one failed attempt still leaves days
            to fix it before the certificate expires
```

## 5. Monitoring the expiry that happens anyway

Automation fails silently; monitoring is the backstop.

```
watch       the served certificate's expiry date, from outside, on every served
            hostname, and alert well before it expires
alert       to somewhere a human sees, with enough lead time to act
scope       every hostname, including the ones added later that the renewal
            automation did not know about
```

A site goes down on an expired certificate not because renewal is hard but
because nobody was watching the one that renewal missed.

## 6. Development versus production

Do not reach for a production certificate to develop against, and do not ship a
development certificate.

```
development   a locally trusted certificate (a tool that creates and trusts a
              local authority), or a self-signed one accepted knowingly. Never
              a real production key on a developer machine.
production    the real, publicly trusted certificate, on the terminating layer,
              renewed automatically
```

## 7. The private key never leaks

The private key is the one secret that makes the certificate meaningful.

```
never in     the repository, a log, a screenshot, a container image layer, an
             environment printed to output
stored in    the platform's certificate store or a secret manager, read by the
             terminating layer, per secrets-management
rotated      if it is ever exposed, the certificate is reissued with a new key
             and the old one revoked; deleting the leaked key does not undo the
             exposure
```

## 8. Protocol

1. Establish where TLS terminates: proxy, load balancer, platform edge, or
   application.
2. Obtain the certificate by a method whose renewal can be automated; choose
   wildcard or SAN by the hosts.
3. Install it on the terminating layer, and confirm the certificate covers
   every served hostname.
4. Enforce HTTPS: redirect plain HTTP, set HSTS with `security-headers`, mark
   cookies Secure.
5. Automate renewal with margin, and verify it actually renewed once.
6. Monitor the served expiry from outside on every hostname, alerting with
   lead time.
7. Use a locally trusted certificate in development, never a production key,
   and keep the private key out of the repository, the logs and the images.

## 9. Auto-critique

Score from 0 to 5: termination is located before installing, the obtaining
method allows automated renewal, HTTPS is enforced with a redirect and HSTS,
renewal is automated with margin and proven once, expiry is monitored from
outside on every hostname, development uses a local certificate not a
production key, and the private key is out of the repository, the logs and the
images.

Threshold: no axis below 3, average at least 4. A private key in the
repository, or a renewal assumed rather than proven, scores 0 overall, because
the first is a leaked secret and the second is a certificate that will expire
unwatched.

## 10. Interfaces

- Upstream: `engineering-core`, `devops-core`.
- Lateral: `security-headers` for HSTS and the Secure cookie, and the header
  set generally; `secrets-management` for the private key's storage and
  rotation; `deployment-engineering` for the terminating layer and the rollout;
  `environment-management` for the per-environment certificate configuration.
- Downstream: `observability` for the expiry alert; `incident-response` when a
  certificate expired in production.
