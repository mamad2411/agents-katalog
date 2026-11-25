---
name: fbr
description: Feedback tester'i Chrome'da mobile boyutta calistir. Triggers: /fbr, feedback run.
argument-hint: ""
---

## Feedback Run

1. Varsa onceki run'i kill et
2. `flutter_run` MCP ile `~/Projects/feedback_tester` projesini Chrome'da calistir
3. `--web-browser-flag=--window-size=390,844` (mobile boyut)
