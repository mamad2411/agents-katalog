---
name: localwp-ssl-certificates
description: Manage and troubleshoot SSL certificates for WordPress sites in LocalWP.
---

# LocalWP SSL Certificates

This skill helps you manage and troubleshoot SSL certificates in LocalWP.

## Trusting SSL Certificates
1. Open the LocalWP application.
2. Select the site you want to manage.
3. In the Site Overview, look for the **SSL** section.
4. Click the **Trust** button to add the site's certificate to your system's keychain.

## Troubleshooting Browser Warnings
- **macOS**: If the Trust button fails or the browser still shows warnings, open Keychain Access. Search for the site domain, open the certificate, and set "When using this certificate" to "Always Trust".
- **Windows**: You may need to manually import the certificate using certmgr.msc into "Trusted Root Certification Authorities".
- Restart the browser after trusting the certificate.

## Mixed Content Errors
If the site loads over HTTPS but assets don't, check for mixed content errors in the browser console. Update WordPress site URLs and replace HTTP with HTTPS in the database using tools like WP-CLI (`wp search-replace`).
