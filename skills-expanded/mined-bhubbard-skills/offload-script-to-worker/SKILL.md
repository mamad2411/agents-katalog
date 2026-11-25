---
name: offload-script-to-worker
description: Use wp_script_add_data to offload a registered script to a Web Worker via Partytown.
---

# Offload Script to Web Worker

The Web Worker Offloading plugin uses Partytown to run scripts off the main thread.

To opt a registered script into being loaded in a worker:

```php
wp_script_add_data( 'foo', 'worker', true );
```

This ensures the script 'foo', and any inline before/after scripts associated with it, are offloaded to the web worker.
