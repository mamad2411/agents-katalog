---
name: nextcloud-files
description: Self-hosted cloud storage and collaboration with Nextcloud
version: 1.0.0
tags: [cloud-storage, files, collaboration, self-hosted]
---

# Nextcloud – Self-Hosted Cloud Storage

Nextcloud is the #1 self-hosted productivity platform — file sync, sharing,
calendars, contacts, and collaborative editing.

- **GitHub**: github.com/nextcloud/server (30 000+ ⭐)
- **License**: AGPL-3.0
- **Security**: Regular HackerOne audits. EU GDPR compliant. No malware.

## Environment Variables

| Variable | Description |
|---|---|
| `{{NEXTCLOUD_URL}}` | Base URL of the Nextcloud instance |
| `{{NEXTCLOUD_USER}}` | Username |
| `{{NEXTCLOUD_PASSWORD}}` | App password or user password |

## Usage Examples

### List files via WebDAV

```bash
curl -s -u "{{NEXTCLOUD_USER}}:{{NEXTCLOUD_PASSWORD}}" \
  -X PROPFIND "{{NEXTCLOUD_URL}}/remote.php/dav/files/{{NEXTCLOUD_USER}}/"
```

### Upload a file

```bash
curl -s -u "{{NEXTCLOUD_USER}}:{{NEXTCLOUD_PASSWORD}}" \
  -X PUT "{{NEXTCLOUD_URL}}/remote.php/dav/files/{{NEXTCLOUD_USER}}/document.pdf" \
  --data-binary @document.pdf
```

### Create a public share link

```bash
curl -s -u "{{NEXTCLOUD_USER}}:{{NEXTCLOUD_PASSWORD}}" \
  -X POST "{{NEXTCLOUD_URL}}/ocs/v2.php/apps/files_sharing/api/v1/shares" \
  -H "OCS-APIRequest: true" \
  -d "path=/document.pdf&shareType=3"
```

## AI Agent Tips

- WebDAV is the primary file access protocol.
- Use OCS API for sharing, user management, and app operations.
- Support for 400K+ deployments worldwide ensures broad community support.
- Integrates with Collabora Online or OnlyOffice for document editing.
