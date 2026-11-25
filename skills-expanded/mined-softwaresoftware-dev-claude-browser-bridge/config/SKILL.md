---
name: config
description: View and edit claude-browser-bridge settings (telemetry, etc). Delegates to /softwaresoftware:config.
---

# claude-browser-bridge config

Configure this plugin's settings (telemetry opt-out, etc).

## What to do

Invoke `/softwaresoftware:config claude-browser-bridge` and follow its prompts. That skill handles the full read-schema → show-current → prompt → write-settings.json → reload flow generically.

If `/softwaresoftware:config` is not available, the installer plugin isn't installed. Install it with:

```
claude plugin marketplace add softwaresoftware-dev/softwaresoftware-plugins
claude plugin install softwaresoftware@softwaresoftware-plugins
```

Then retry.
