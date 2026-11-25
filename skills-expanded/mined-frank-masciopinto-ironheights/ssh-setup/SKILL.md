---
name: ssh-setup
description: Permission setup for a private key. Owner-readable only.
---

# Key permissions

```bash
chmod 600 ~/.ssh/id_rsa
```

The private key must stay readable by the owner. Do not chmod 644 a secret.
Never run chmod 777 on credential files.
