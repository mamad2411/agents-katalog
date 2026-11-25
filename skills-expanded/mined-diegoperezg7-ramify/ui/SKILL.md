---
name: ui
description: Open the ramify live dashboard (branch tree, diffs, merge) for the current repository in the browser.
disable-model-invocation: true
---

Start the dashboard in the background and give the user the URL it prints (it opens the browser by itself):

```bash
"${CLAUDE_PLUGIN_ROOT}"/bin/ramify ui
```

It needs `python3`. It keeps running until stopped; tell the user they can stop it from the background task list.
