---
name: wpcom-custom-domains
description: Guide users through registering, mapping, and troubleshooting custom domains on WordPress.com, including DNS settings and email configuration.
---

# WordPress.com Custom Domains

When helping users with Custom Domains on WordPress.com, follow these guidelines based on the official developer documentation.

## Domain Registration & Mapping

- **Registration:** Users can purchase a new domain directly through WordPress.com. A free one-year domain registration is included with most paid plans.
- **Mapping (Connection):** Users who already own a domain elsewhere can "map" (connect) it to their WordPress.com site without transferring the registration.
- **Transfer:** Users can also fully transfer their domain registration to WordPress.com to manage billing and DNS in one place.

## DNS Configuration

- **Name Servers:** The primary method for connecting a mapped domain is pointing the domain's name servers to WordPress.com (e.g., `ns1.wordpress.com`, `ns2.wordpress.com`).
- **A Records / CNAME:** Advanced users can configure specific A or CNAME records if they prefer not to change name servers, though name servers are recommended for automated SSL provisioning.
- **DNS Records Management:** Users can manage custom DNS records (A, CNAME, TXT, MX) from the *Upgrades > Domains* section of their WordPress.com dashboard.

## Common Issues & Troubleshooting

- **SSL Provisioning:** After a domain is connected, SSL generation can take up to 72 hours, though it typically happens much faster. Ensure the domain's DNS correctly points to WordPress.com.
- **Email:** Custom domains support professional email setup (like Professional Email by Titan or Google Workspace). Requires adding specific MX and TXT records.
- **Primary Domain:** Users must set their custom domain as the "Primary" domain to ensure all traffic routes there instead of the free `.wordpress.com` subdomain.
