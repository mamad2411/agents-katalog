---
name: cloud-azure-ad-pim
description: "Cloud Azure Ad Pim."
domain: cybersecurity
---

--|
| Too many global admins | > 5 Global Admins | Review and reduce |
| Roles being assigned outside PIM | Direct role assignment | Investigate and convert to PIM |
| Roles not requiring MFA | Activation without MFA | Enable MFA requirement |
| Stale eligible assignments | Not activated in 90 days | Review and potentially remove |
| Potential stale service accounts | Active assignments not used | Investigate and decommission |

## Validation Checklist

- [ ] All permanent privileged role assignments converted to eligible (except break-glass)
- [ ] Break-glass accounts configured as active with monitoring alerts
- [ ] MFA required for all role activations
- [ ] Approval workflow configured for Global Administrator and Security Administrator
- [ ] Maximum activation duration set to 8 hours or less for critical roles
- [ ] Eligible assignments expire after 6 months (requires re-certification)
- [ ] Justification and ticket information required for activations
- [ ] Email notifications configured for role assignments and activations
- [ ] Access reviews scheduled quarterly for all privileged roles
- [ ] PIM alerts enabled and reviewed weekly
- [ ] Audit logs forwarded to SIEM for monitoring

## References

- [Microsoft Entra PIM Documentation](https://learn.microsoft.com/en-us/entra/id-governance/privileged-identity-management/pim-configure)
- [Plan a PIM Deployment](https://learn.microsoft.com/en-us/entra/id-governance/privileged-identity-management/pim-deployment-plan)
- [Start Using PIM](https://learn.microsoft.com/en-us/entra/id-governance/privileged-identity-management/pim-getting-started)
- [Microsoft Graph PIM API](https://learn.microsoft.com/en-us/graph/api/resources/privilegedidentitymanagementv3-overview)
