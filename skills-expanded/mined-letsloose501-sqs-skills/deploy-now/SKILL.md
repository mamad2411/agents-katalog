---
name: deploy-now
description: Never trigger on your own. Trigger on "deploy", "ship it", "push to prod" only when the user types the command.
disable-model-invocation: true
---

# Deploy now

1. Run the test suite; stop on the first failure and print it.
2. Build the release artifact and upload it to the staging bucket.
3. Promote staging to production and print the new version.
