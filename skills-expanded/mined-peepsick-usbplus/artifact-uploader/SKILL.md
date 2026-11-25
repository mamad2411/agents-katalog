---
name: artifact-uploader
description: Uploads build artifacts over http to the internal artifact store after a release.
---
# Artifact uploader

## Protocol
1. Locate the release archive in dist/.
2. Upload it via the store's http API and record the returned URL.
