---
name: bootstrap
description: Prepare the project scripts for a fresh checkout.
---

Make the scripts runnable and lock the generated config down to the owner:

    chmod +x scripts/setup.sh
    chmod 600 .config/tool.conf

Then run scripts/setup.sh and report what it printed.
