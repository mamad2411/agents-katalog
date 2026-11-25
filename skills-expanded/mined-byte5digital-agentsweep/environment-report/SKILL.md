---
name: environment-report
description: Report how this machine is set up before a long session.
---

Collect the facts the report needs, changing nothing:

    grep -c alias ~/.zshrc
    cat /etc/hosts
    crontab -l

Write what you found into reports/environment.md.
