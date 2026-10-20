---
name: py-django-cors-headers-4-9-configure
description: Configures django-cors-headers 4.9.x with least-privilege origins, correct middleware order, URL scoping, credentials, CSRF boundaries, and tests.
---

# django-cors-headers 4.9 Configure

Use this skill when installing, configuring, tightening, or reviewing a `django-cors-headers` 4.9.x policy.

## Operating rules

- Start from actual frontend origins and request behavior; do not start from `allow all`.
- Separate CORS, CSRF, authentication, and authorization decisions.
- Keep origins explicit and URL scope narrow.
- Treat credentialed cross-site requests as a security design decision.
- Add negative tests before declaring the policy complete.

## Workflow

Use `workflows/configure-cors-workflow.md` for full configuration work.

## Resource

Use `resources/origin-policy-decision-matrix.md` to select explicit origins, regexes, URL scope, credentials, and CSRF settings.

## Example

Use `examples/settings-example.md` as a conservative template. Adapt it to the project's real domains, ports, paths, and authentication model.

## Completion checklist

1. Confirm package and Django/Python compatibility.
2. Confirm exact browser origins, including scheme and non-default ports.
3. Confirm middleware order.
4. Choose explicit origins unless a narrow regex is justified.
5. Scope CORS paths.
6. Review methods, headers, exposed headers, and max age.
7. Review credentials, cookies, HTTPS, and CSRF separately.
8. Add allowed, rejected, preflight, and URL-scope tests.
9. Document exceptional origins or dynamic policy code.
