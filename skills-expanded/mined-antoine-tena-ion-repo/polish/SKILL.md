---
name: polish
description: Former /nuxt:polish, now /design:polish of ion-design (the design tool of the Ion family, 2 November 2026), for sessions and habits from before the move.
disable-model-invocation: true
argument-hint: "<page path, e.g. /events>"
---

The visual audit of a page is design, not technique: it is now `/design:polish`, plugin
`design@ion-design`, valid for any frontend. `/nuxt:preview` stays here and is what it uses to
capture a Nuxt page.

1. If the `design` plugin is enabled in this session, run `/design:polish $ARGUMENTS` and follow
   it exactly.
2. Otherwise tell the user in one line that the skill moved, and give the commands that install
   it, without running them:
   ```bash
   claude plugin marketplace add antoine-tena/ion-design
   claude plugin install design@ion-design
   ```
   Until then, `/nuxt:preview <page>` still captures and judges the page on three phones and a
   computer.
