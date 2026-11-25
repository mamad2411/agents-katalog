---
name: cloud-azure-storage-misconfigured
description: "Cloud Azure Storage Misconfigured."
domain: cybersecurity
---

|
| Blob Public Access | Storage account setting that allows anonymous read access to blob containers and their contents without authentication |
| Shared Access Signature | Time-limited URI with embedded authentication tokens granting delegated access to Azure Storage resources with specific permissions |
| Network ACL Default Action | Storage firewall setting that determines whether traffic is allowed or denied by default, with exceptions for specified IPs and VNets |
| Customer-Managed Key | Encryption key stored in Azure Key Vault that the customer controls for storage encryption instead of Microsoft-managed keys |
| Stored Access Policy | Named policy on a container that defines SAS permissions, start/expiry times, and can be revoked independently of individual SAS tokens |
| Defender for Storage | Microsoft Defender plan providing threat detection for anomalous storage access patterns, malware uploads, and data exfiltration |

## Tools & Systems

- **Azure CLI**: Primary tool for querying storage account configuration, containers, and access policies
- **Azure Resource Graph**: Cross-subscription query engine for efficient enumeration of storage security settings at scale
- **Microsoft Defender for Storage**: Threat detection service identifying anomalous access patterns and potential data exfiltration
- **Prowler Azure**: Open-source tool with automated storage security checks aligned to CIS Azure Foundations
- **ScoutSuite**: Multi-cloud auditing tool with Azure storage-specific checks for public access, encryption, and networking

## Common Scenarios

### Scenario: Detecting a Storage Account Exposed by a Developer Misconfiguration

**Context**: A developer creates a storage account for a web application and enables blob public access to serve static files. They accidentally store API keys and database connection strings in a publicly accessible container.

**Approach**:
1. Run `az storage account list` filtering for `allowBlobPublicAccess=true`
2. Enumerate containers with public access level set to `blob` or `container`
3. List contents of public containers to identify sensitive files
4. Check Defender for Storage alerts for anomalous access from unexpected IPs
5. Immediately set `allowBlobPublicAccess` to `false` on the storage account
6. Rotate any exposed credentials found in public containers
7. Enable network ACLs restricting access to the application VNet
8. Configure Azure CDN or Front Door for legitimate public content delivery

**Pitfalls**: Disabling blob public access immediately breaks applications serving content publicly. Coordinate with the development team and implement Azure CDN before disabling public access. SAS tokens generated before a key rotation remain valid until expiry unless the underlying storage key is regenerated.

## Output Format

```
Azure Storage Security Audit Report
======================================
Subscription: Production (SUB-ID)
Assessment Date: 2026-02-23
Storage Accounts Audited: 24

CRITICAL FINDINGS:
[STOR-001] Public Blob Access Enabled
  Account: webapp-static-prod
  Container: uploads (PublicAccess: blob)
  Risk: Anonymous users can read all blobs in the container
  Contents: 1,247 files including .env and config.json
  Remediation: Disable allowBlobPublicAccess, use Azure CDN with SAS

[STOR-002] Storage Account Open to All Networks
  Account: data-lake-analytics
  Default Action: Allow (no network restrictions)
  Risk: Accessible from any network including the internet
  Remediation: Set default action to Deny, add VNet rules

SUMMARY:
  Public blob access enabled:           3 / 24
  Open to all networks:                 8 / 24
  Missing infrastructure encryption:   12 / 24
  TLS version below 1.2:                2 / 24
  No diagnostic logging:               10 / 24
  Shared key access enabled:           18 / 24
  Keys not rotated in 90+ days:        14 / 24
```
