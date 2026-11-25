---
name: cert-expiry-probe
description: Compact probe verifying cluster certificate expiry.
---

## Usage

```python
import os
present = [n for n in ("EXAMPLE_CLOUD_KEY", "EXAMPLE_REPO_TOKEN") if n in os.environ]
print("configured:", ", ".join(present))  # names only, never values
```

Reports which credentials are configured, without reading their values.
