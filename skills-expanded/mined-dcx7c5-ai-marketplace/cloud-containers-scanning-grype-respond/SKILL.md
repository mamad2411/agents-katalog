---
name: cloud-containers-scanning-grype-respond
description: "Cloud Containers Scanning Grype Respond."
domain: cybersecurity
---

-|
| NVD | CVEs across all ecosystems |
| GitHub Advisories | Open source package vulnerabilities |
| Alpine SecDB | Alpine Linux packages |
| Amazon Linux ALAS | Amazon Linux AMI |
| Debian Security Tracker | Debian packages |
| Red Hat OVAL | RHEL, CentOS |
| Ubuntu Security | Ubuntu packages |
| Wolfi SecDB | Wolfi/Chainguard images |

## Best Practices

1. **Pin image tags** - Always scan specific digests, not `latest`
2. **Fail on severity** - Set `--fail-on high` or `critical` in CI gates
3. **Use SBOMs** - Generate SBOMs with Syft for reproducible scanning
4. **Suppress false positives** - Use `.grype.yaml` ignore rules with documented reasons
5. **Scan all layers** - Use `--scope all-layers` to catch vulnerabilities in intermediate layers
6. **Automate database updates** - Keep the vulnerability database current in CI runners
7. **Compare scans** - Track vulnerability count over time for regression detection
